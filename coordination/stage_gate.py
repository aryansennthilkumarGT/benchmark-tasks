"""Verify real stage prerequisites; a shell EXIT marker alone is insufficient."""
import argparse
import json
import math
from pathlib import Path


INTERRUPTIONS = ('intentional-wait-stop.json', 'interruption-evidence.json',
                 'first-failure-stop.json', 'workload-deadline-stop.json')


def require_no_interruption(root):
    root = Path(root)
    found = [name for name in INTERRUPTIONS if (root/name).exists()]
    if found:
        raise ValueError('Stage was interrupted, not completed: '+str(root)+' '+','.join(found))


def verify(root, exits, record=None, commit=None, mode=None):
    root = Path(root).resolve()
    require_no_interruption(root)
    checked = {}
    for name in dict.fromkeys(['producer-exit.txt', *exits]):
        path = (root/name).resolve()
        if not path.is_relative_to(root) or path.read_text().strip() != '0':
            raise ValueError('Missing/nonzero actual stage exit: '+str(path))
        checked[name] = 0
    proof = None
    if record:
        path = (root/record).resolve()
        if not path.is_relative_to(root):
            raise ValueError('Record escapes stage directory')
        proof = json.loads(path.read_text())
        if (proof.get('kind') != 'REAL_INSPECT_ROLLOUT'
                or proof.get('commit') != commit or proof.get('mode') != mode
                or not isinstance(proof.get('score'), (int, float))
                or isinstance(proof.get('score'), bool)
                or not math.isfinite(proof['score']) or not 0 <= proof['score'] <= 1
                or not isinstance(proof.get('steps'), int) or proof['steps'] <= 0
                or not proof.get('record_id') or not proof.get('log_sha256')):
            raise ValueError('Incomplete/mismatched actual rollout record')
    return {'kind': 'ACTUAL_STAGE_PREREQUISITES', 'root': str(root),
            'exits': checked, 'record_id': proof['record_id'] if proof else None,
            'scope': 'Prerequisite guard; full physics/scoring/media validation remains separate.'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', required=True, type=Path)
    p.add_argument('--exit', action='append', default=[], dest='exits')
    p.add_argument('--record')
    p.add_argument('--commit')
    p.add_argument('--mode', choices=['expert', 'dream'])
    a = p.parse_args()
    if a.record and (not a.commit or not a.mode):
        p.error('--record requires --commit and --mode')
    print(json.dumps(verify(a.root, a.exits, a.record, a.commit, a.mode), indent=2))


if __name__ == '__main__':
    main()
