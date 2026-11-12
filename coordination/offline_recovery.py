"""CPU-only recovery audits of immutable local Git objects; no fetch/push or GPU calls.

Exit 0 means the selected offline checks passed, never submission readiness.
Use --dry-run to inspect targets and --resume to reuse hash-verified results.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tarfile
import xml.etree.ElementTree as ET

from engine import Incomplete, Ledger, atomic, digest, execute, exclusive, read, utc
from evidence import public_text
from submit_ready import validate_metadata

REPO = Path(__file__).resolve().parents[1]
AUDITS = ('verify_assets.py', 'audit_control.py', 'audit_geometry.py',
          'audit_grasps.py', 'audit_motion.py', 'audit_threads.py')


def git(repo, *args):
    return subprocess.check_output(['git', '-C', str(repo), *args], text=True).strip()


def targets(repo, manifest):
    result = []
    for task in manifest['tasks']:
        slug = task['slug']
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', slug):
            raise Incomplete('Unsafe slug')
        branch = task['branch']
        if branch != 'draft/' + slug or task['task_folder'] != 'tasks/' + slug:
            raise Incomplete('Task branch/folder mismatch')
        commit = git(repo, 'rev-parse', '--verify', 'refs/remotes/origin/' + branch + '^{commit}')
        if not re.fullmatch('[0-9a-f]{40}', commit):
            raise Incomplete('Invalid commit')
        result.append(dict(slug=slug, branch=branch, commit=commit, folder=task['task_folder']))
    if len({t['slug'] for t in result}) != len(result) or not result:
        raise Incomplete('Duplicate or empty task selection')
    return result


def extract(archive, destination, prefix):
    destination.mkdir()
    with tarfile.open(archive) as stream:
        members = stream.getmembers()
        for entry in members:
            if not (entry.isfile() or entry.isdir()):
                raise Incomplete('Source archive contains a link or special file')
            path = destination / entry.name
            if not path.resolve().is_relative_to(destination.resolve()):
                raise Incomplete('Source archive path escapes destination')
            if entry.isfile() and not entry.name.startswith(prefix + '/'):
                raise Incomplete('Source archive contains unrelated files')
        stream.extractall(destination, members=members, filter='data')
    return destination / prefix


def check_source(folder):
    validate_metadata(read(folder / 'task.json'))
    manifest = read(folder / 'source_manifest.json')['files']
    if not manifest:
        raise Incomplete('Empty source manifest')
    for name, expected in manifest.items():
        path = (folder / name).resolve()
        if not path.is_relative_to(folder.resolve()):
            raise Incomplete('Source hash path escapes task')
        if hashlib.sha256(path.read_bytes().replace(b'\r\n', b'\n')).hexdigest() != expected:
            raise Incomplete('Source hash mismatch: ' + name)
    for path in folder.rglob('*.py'):
        ast.parse(path.read_text(encoding='utf8'), filename=str(path))
    return public_text(folder)


def junit_counts(path):
    root = ET.parse(path).getroot()
    cases = list(root.iter('testcase'))
    failed = sum(c.find('failure') is not None or c.find('error') is not None for c in cases)
    skipped = sum(c.find('skipped') is not None for c in cases)
    if not cases or failed or len(cases) == skipped:
        raise Incomplete('No passing tests or failed tests in current JUnit report')
    return dict(tests=len(cases), passed=len(cases)-skipped, skipped=skipped, failed=failed)


def run_task(repo, task, out, audits, baseline):
    archive = out / 'source.tar'
    with archive.open('wb') as stream:
        subprocess.run(['git', '-C', str(repo), 'archive', task['commit'], task['folder']],
                       stdout=stream, check=True)
    changed = git(repo, 'diff', '--name-only', baseline, task['commit']).splitlines()
    if not changed or any(not p.startswith(task['folder'] + '/') for p in changed):
        raise Incomplete('Branch differs outside its independent task folder')
    folder = extract(archive, out / 'source', task['folder'])
    before = {p.relative_to(folder).as_posix(): digest(p) for p in folder.rglob('*') if p.is_file()}
    text_check = check_source(folder)
    env = dict(CUDA_VISIBLE_DEVICES='', OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1',
               PYTEST_DISABLE_PLUGIN_AUTOLOAD='1')
    execute([sys.executable, '-m', 'pytest', '-q', '-p', 'no:cacheprovider',
             '--junitxml=' + str(out/'tests.xml'), str(folder)], folder, out/'tests.log', 900, env)
    counts = junit_counts(out/'tests.xml')
    ran = []
    if audits:
        for script in AUDITS:
            execute([sys.executable, str(folder/script)], folder, out/(script+'.log'), 1800, env)
            ran.append(script)
    after = {p.relative_to(folder).as_posix(): digest(p) for p in folder.rglob('*') if p.is_file()}
    if before != after:
        raise Incomplete('Offline checks changed the task source')
    result = dict(kind='OFFLINE_ONLY', task=task, tests=counts, audits_executed=ran,
                  public_text=text_check, source_archive_sha256=digest(archive),
                  branch_independent=True, physics_executed=False, ready_for_submission=False)
    atomic(out/'result.json', result)
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=REPO)
    parser.add_argument('--manifest', type=Path, default=REPO/'coordination/draft-manifest.json')
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--task')
    parser.add_argument('--commit', help='Audit this exact local SHA; requires --task')
    parser.add_argument('--audits', action='store_true')
    parser.add_argument('--resume', action='store_true')
    parser.add_argument('--retry-failed')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args(argv)
    repo = args.repo.resolve()
    output = args.output.resolve()
    if output.is_relative_to(repo):
        parser.error('Keep recovery evidence outside the checkout')
    manifest = read(args.manifest)
    selected = targets(repo, manifest)
    if args.task:
        selected = [t for t in selected if t['slug'] == args.task]
        if not selected:
            parser.error('Unknown task')
    if args.commit:
        if not args.task or not re.fullmatch('[0-9a-f]{40}', args.commit):
            parser.error('--commit requires --task and a full 40-character SHA')
        selected[0]['commit'] = git(repo, 'rev-parse', '--verify', args.commit + '^{commit}')
        selected[0]['source_selection'] = 'explicit_commit'
    if args.dry_run:
        print(json.dumps(dict(kind='OFFLINE_PLAN', tasks=selected, audits=args.audits), indent=2))
        return 0
    packages = sorted((d.metadata['Name'], d.version) for d in importlib.metadata.distributions())
    with exclusive(output/'lock'):
        ledger = Ledger(output, args.resume, args.retry_failed)
        report = dict(kind='OFFLINE_RECOVERY', started_at=utc(), tasks=[],
                      physics_executed=False, ready_for_submission=False)
        for task in selected:
            inputs = dict(task=task, audits=args.audits, baseline=manifest['base_commit'],
                          python=sys.version, packages=packages,
                          runner=digest(__file__), engine=digest(Path(__file__).with_name('engine.py')),
                          evidence=digest(Path(__file__).with_name('evidence.py')))
            try:
                receipt = ledger.stage(task['slug'], 'offline', inputs,
                    lambda out: run_task(repo, task, out, args.audits, manifest['base_commit']))
                row = dict(task, status='PASS', result=receipt['result'])
            except (Incomplete, OSError, ValueError, subprocess.SubprocessError, SyntaxError) as exc:
                row = dict(task, status='FAILED', error=str(exc))
            report['tasks'].append(row)
            print(task['slug'], row['status'], flush=True)
            report['offline_checks_passed'] = all(t['status']=='PASS' for t in report['tasks'])
            atomic(output/'report.json', report)
    return 0 if report['offline_checks_passed'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
