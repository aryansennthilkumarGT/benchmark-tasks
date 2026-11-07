"""Durable, sequential stage execution. A zero process exit is not validation.

Evidence is local and reproducible, not cryptographically attested simulator provenance.
Never put credentials in commands or result dictionaries. No PR operations live here.
"""
from __future__ import annotations
import contextlib
import datetime as dt
import hashlib
import json
import math
import os
from pathlib import Path
import signal
import subprocess
import time
import uuid


class Incomplete(RuntimeError):
    pass


def utc():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def atomic(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + '.' + uuid.uuid4().hex + '.tmp')
    with temp.open('w', encoding='utf-8', newline='\n') as stream:
        json.dump(value, stream, indent=2, allow_nan=False)
        stream.write('\n')
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temp, path)


def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, allow_nan=False).encode()).hexdigest()


def within(root, path):
    root, path = Path(root).resolve(), Path(path).resolve()
    if path != root and root not in path.parents:
        raise Incomplete('Artifact escapes its evidence directory')
    return path


def artifacts(root):
    root = Path(root).resolve()
    result = {}
    for path in sorted(root.rglob('*')):
        if path.is_symlink():
            raise Incomplete('Evidence may not contain symbolic links')
        if path.is_file() and path.name != 'receipt.json':
            result[path.relative_to(root).as_posix()] = digest(path)
    return result


def verified_receipt(path, key):
    try:
        data = read(path)
        return (data['status'] == 'PASS' and data['key'] == key
                and data['artifacts'] == artifacts(Path(path).parent))
    except (OSError, ValueError, KeyError, Incomplete):
        return False


class Budget:
    """Conservative instance-wall-time bound, including idle time and stage setup.

    This cannot stop cloud billing. Provider shutdown remains an explicit operation.
    The receipt must describe the actual instance, not a guessed GPU hourly rate.
    """
    def __init__(self, receipt, clock=time.time):
        self.receipt = read(receipt)
        self.clock = clock
        r = self.receipt
        for k in ('hourly_usd', 'balance_usd', 'spent_before_start_usd', 'instance_started_unix'):
            v = r.get(k)
            if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) or v < 0:
                raise Incomplete('Invalid budget field: ' + k)
        if not r.get('instance_id') or not r.get('provider_evidence') or not r.get('gpu_uuid'):
            raise Incomplete('Budget receipt needs instance, GPU UUID, and provider evidence reference')
        if r['hourly_usd'] <= 0 or r['instance_started_unix'] > clock():
            raise Incomplete('Invalid hourly rate or future instance start')

    def estimate(self, extra_seconds=0):
        r = self.receipt
        return (self.clock() - r['instance_started_unix'] + extra_seconds) * r['hourly_usd'] / 3600

    def check(self, extra_seconds=0):
        r = self.receipt
        projected = self.estimate(extra_seconds)
        if projected + r['spent_before_start_usd'] > 170 or r['balance_usd'] - projected < 30:
            raise Incomplete('Compute budget/reserve reached. Stop the Brev instance to stop billing.')
        return {'estimated_instance_charge_usd': self.estimate(), 'projected_charge_usd': projected,
                'cap_usd': 170, 'reserve_usd': 30, 'checked_at': utc()}


@contextlib.contextmanager
def exclusive(path):
    """Kernel lock releases on crash. Never remove or steal another process's lock."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('a+b') as stream:
        if os.name == 'nt':
            import msvcrt
            stream.seek(0)
            if not stream.read(1):
                stream.write(b'0'); stream.flush()
            stream.seek(0)
            try:
                msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
            except OSError as exc:
                raise Incomplete('Another pipeline owns this run directory') from exc
        else:
            import fcntl
            try:
                fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError as exc:
                raise Incomplete('Another pipeline owns this run directory') from exc
        try:
            yield
        finally:
            if os.name == 'nt':
                stream.seek(0); msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(stream, fcntl.LOCK_UN)


def execute(argv, cwd, output, timeout, env=None, budget=None):
    """No shell interpretation, no implicit retry, kill the entire owned process group."""
    if budget:
        budget.check(timeout)
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    merged = os.environ.copy()
    merged.update({'PYTHONDONTWRITEBYTECODE': '1', 'PYTHONUNBUFFERED': '1', 'PYTHONUTF8':'1'})
    merged.update(env or {})
    start = time.monotonic()
    with output.open('wb') as log:
        proc = subprocess.Popen([str(x) for x in argv], cwd=cwd, env=merged,
                                stdout=log, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
                                start_new_session=os.name != 'nt')
        try:
            while proc.poll() is None:
                if time.monotonic() - start > timeout:
                    raise Incomplete(f'Command timed out after {timeout}s; see {output}')
                if budget:
                    budget.check()
                time.sleep(0.15)
            if proc.returncode != 0:
                raise Incomplete(f'Command exited {proc.returncode}; see {output}')
        finally:
            if proc.poll() is None:
                if os.name != 'nt':
                    os.killpg(proc.pid, signal.SIGTERM)
                else:
                    proc.terminate()
                try:
                    proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    if os.name != 'nt':
                        os.killpg(proc.pid, signal.SIGKILL)
                    else:
                        proc.kill()
                    proc.wait()
    return {'command': [str(x) for x in argv], 'duration_s': time.monotonic()-start, 'exit_code': 0}


class Ledger:
    def __init__(self, root, resume=False, retry_reason=None):
        self.root = Path(root).resolve()
        self.root.mkdir(parents=True, exist_ok=True)
        self.resume, self.retry_reason = resume, retry_reason
        self.path = self.root/'ledger.json'
        self.data = read(self.path) if self.path.exists() else {'schema': 1, 'tasks': {}}

    def stage(self, slug, name, inputs, action):
        key = fingerprint(inputs)
        history = self.data['tasks'].setdefault(slug, {}).setdefault(name, [])
        matches = [r for r in history if r['key'] == key]
        for row in reversed(matches):
            receipt = within(self.root, self.root/row['receipt'])
            if row['status'] == 'PASS':
                if not verified_receipt(receipt, key):
                    raise Incomplete(f'{slug}/{name}: prior evidence changed or is missing; preserved for investigation')
                if not self.resume:
                    raise Incomplete(f'{slug}/{name} already passed; use --resume to reuse verified evidence')
                return read(receipt)
        if matches and (not self.retry_reason or len(matches) >= 2):
            raise Incomplete(f'{slug}/{name}: unchanged failed/interrupted stage; fix inputs or use --retry-failed REASON once')
        attempt = self.root/slug/name/(key[:16]+'-'+uuid.uuid4().hex[:8])
        attempt.mkdir(parents=True)
        row = {'key': key, 'status': 'RUNNING', 'started_at': utc(),
               'receipt': (attempt/'receipt.json').relative_to(self.root).as_posix(),
               'retry_reason': self.retry_reason if matches else None}
        history.append(row)
        atomic(self.path, self.data)
        receipt = dict(row, inputs=inputs)
        try:
            result = action(attempt)
            if not isinstance(result, dict):
                raise Incomplete('Stage validator did not return an evidence record')
            receipt.update(status='PASS', result=result, artifacts=artifacts(attempt), completed_at=utc())
            if not receipt['artifacts']:
                raise Incomplete('No stage evidence was produced')
            atomic(attempt/'receipt.json', receipt)
            row.update(status='PASS', completed_at=receipt['completed_at'])
            return receipt
        except BaseException as exc:
            row.update(status='FAILED', error=f'{type(exc).__name__}: {exc}', completed_at=utc())
            atomic(attempt/'receipt.json', dict(receipt, **{k:v for k,v in row.items() if k != 'key'}))
            raise
        finally:
            atomic(self.path, self.data)
