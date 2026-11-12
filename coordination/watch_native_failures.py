"""Stop only an owned native worker after its first real failed case.

The producer reaps its normal nonzero exit; reports are never marked passing.
No instance power operation exists in this module.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import signal
import time
import datetime


def command(pid):
    try:
        return [x.decode() for x in Path(f'/proc/{pid}/cmdline').read_bytes().split(b'\0') if x]
    except FileNotFoundError:
        return []


def children(pid):
    try:
        return [int(x) for x in Path(f'/proc/{pid}/task/{pid}/children').read_text().split()]
    except FileNotFoundError:
        return []


def owned_native_groups(producer, root):
    if str(root/'producer.sh') not in command(producer):
        return []
    pending = list(children(producer))
    seen, groups = set(), []
    outputs = {str(root/name) for name in ['selected-control', 'final-physics', 'final-control']}
    while pending:
        pid = pending.pop()
        if pid in seen:
            continue
        seen.add(pid)
        pending.extend(children(pid))
        argv = command(pid)
        if not argv or Path(argv[0]).name != 'timeout' or not outputs.intersection(argv):
            continue
        try:
            group = os.getpgid(pid)
        except ProcessLookupError:
            continue
        if group == pid and group > 1 and group != os.getpgrp():
            groups.append(group)
    return groups


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--producer', type=int, required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    while str(root/'producer.sh') in command(args.producer):
        for name in ['selected-control', 'final-physics', 'final-control']:
            report_path = root/name/'results.json'
            try:
                raw = report_path.read_bytes()
                report = json.loads(raw)
            except (FileNotFoundError, json.JSONDecodeError):
                continue
            failures = [case for case in report.get('cases', []) if case.get('status') == 'FAIL']
            if not failures:
                continue
            groups = owned_native_groups(args.producer, root)
            signals = []
            for group in groups:
                try:
                    os.killpg(group, signal.SIGTERM)
                    signals.append({'pgid': group, 'signal': 'SIGTERM'})
                except ProcessLookupError:
                    pass
            record = {'at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                      'kind': 'REAL_NATIVE_FAILURE_ABORT_UNCHANGED_REPEATS',
                      'report': str(report_path), 'report_sha256': hashlib.sha256(raw).hexdigest(),
                      'failed_cases': [{'name': f['name'], 'repeat': f['repeat'],
                                       'error': f.get('error')} for f in failures],
                      'signals': signals, 'not_a_passing_test': True,
                      'producer_must_record_actual_nonzero_exit': True,
                      'instance_power_operation': False}
            destination = root/'first-failure-stop.json'
            if destination.exists():
                destination = root/('first-failure-stop-'+str(time.time_ns())+'.json')
            destination.write_text(json.dumps(record, indent=2)+'\n')
            print('Observed genuine failed case; stopped owned worker only; benchmark remains failed.')
            return
        time.sleep(2)


if __name__ == '__main__':
    main()
