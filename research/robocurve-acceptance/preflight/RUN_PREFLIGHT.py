#!/usr/bin/env python3
"""Run actual CPU checks; preserve nonzero blocked outcomes rather than invent PASS."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent


def main():
    env = dict(os.environ, OPENBLAS_NUM_THREADS='1', MPLBACKEND='Agg')
    run = {'run_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
           'python': sys.version, 'platform': platform.platform(),
           'scope': 'CPU-only source-geometry/logic preflight. No simulator, physical hardware or GPU evaluation.',
           'commands': []}
    tests = [([sys.executable, '-m', 'unittest', 'discover', '-s', str(ROOT), '-p', 'test_*.py', '-v'], 0, 'UNIT_TEST_OUTPUT.txt')]
    for candidate in ['N040', 'N044', 'N047', 'N022']:
        tests.append(([sys.executable, str(ROOT / f'{candidate}_ACCESS_TEST.py')], 2, f'{candidate}_EXECUTION.txt'))
    for cmd, expected, filename in tests:
        start = time.perf_counter()
        proc = subprocess.run(cmd, text=True, capture_output=True, env=env, cwd=ROOT)
        content = proc.stdout + proc.stderr
        (ROOT / 'results' / filename).write_text(content)
        row = {'argv': cmd, 'returncode': proc.returncode, 'expected_returncode': expected,
               'elapsed_s': time.perf_counter()-start, 'stdout_stderr_file': filename,
               'output_sha256': hashlib.sha256(content.encode()).hexdigest()}
        if proc.returncode != expected:
            row['unexpected_failure'] = True
        run['commands'].append(row)
    run['all_commands_returned_expected_status'] = all(x['returncode'] == x['expected_returncode'] for x in run['commands'])
    outcomes = [json.loads((ROOT/'results'/f'{name}_ACCESS_RESULT.json').read_text()) for name in ['N040','N044','N047','N022']]
    run['candidate_partial_geometric_certificates'] = sum(x['access_decision']=='PARTIAL_GEOMETRIC_CERTIFICATE_ONLY' for x in outcomes)
    run['candidate_tests_blocked'] = sum(x['input_status'].startswith('BLOCKED') for x in outcomes)
    run['full_feasibility_passes'] = 0
    run['code_sha256'] = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(ROOT.glob('*.py'))}
    run['input_sha256'] = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((ROOT/'inputs').glob('*.json'))}
    run['interpretation'] = 'Unit tests PASS is an engine/logic result. Candidate exit2 means BLOCKED, not feasibility PASS or physical infeasibility.'
    (ROOT / 'results/RUN_MANIFEST.json').write_text(json.dumps(run, indent=2) + '\n')
    print(json.dumps(run, indent=2))
    return 0 if run['all_commands_returned_expected_status'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
