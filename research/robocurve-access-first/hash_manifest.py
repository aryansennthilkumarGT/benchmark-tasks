"""Hash new evidence and all reused local inputs, including their base Git blobs."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess

D = Path(__file__).resolve().parent
R = D.parents[1]
BASE = '2530bbf2cc86f5b68c6f2e2de0c2ee15a1867ba6'
MANIFEST = D / 'CHECKPOINT_HASHES.json'
REUSED = [
    'research/robocurve-implementation/common/access.py',
    'research/robocurve-acceptance/preflight/access_core.py',
    'research/robocurve-acceptance/preflight/assets/YAM_REFERENCE.json.gz',
    'research/robocurve-acceptance/preflight/assets/YAM_SOURCE_MANIFEST.json',
    'research/robocurve-acceptance/preflight/assets/LICENSE.i2rt',
    'research/robocurve-next-prototype/odri/sections.py',
    'research/robocurve-next-prototype/odri/results/YAM_ACCESS.json',
    'research/robocurve-next-prototype/odri/yam_access.py',
    'research/robocurve-next-prototype/NEXT_GATE.md',
    'research/robocurve-next-prototype/requirements-cpu.txt',
    'research/robocurve-final-discovery/TOP_15_VERIFIED_TASKS.md',
    'research/robocurve-final-discovery/TOP_15_SOURCE_AND_FEASIBILITY_MATRIX.md',
    'research/robocurve-final-discovery/THIRD_PARTY_SOURCES.md',
]
SOURCE = 'research/robocurve-next-prototype/sources/odri/'
for part in ['foot_structure', 'lower_leg_structure_base', 'lower_leg_structure_fork']:
    REUSED.append(SOURCE + 'step_files/' + part + '.STEP')
REUSED.extend(SOURCE + name for name in [
    'README.md', 'lower_leg.PDF', 'images/foot_sensor_principle_1.jpg',
    'images/lower_leg_1.jpg', 'images/measurement_foot_contact_sensor.png',
])


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def snapshot():
    reused = {}
    for path in REUSED:
        raw = (R / path).read_bytes()
        original = subprocess.check_output(['git', 'show', BASE + ':' + path], cwd=R)
        assert raw == original, f'Reused base input changed: {path}'
        reused[path] = sha(raw)
    files = {str(p.relative_to(D)): sha(p.read_bytes()) for p in sorted(D.rglob('*'))
             if p.is_file() and p != MANIFEST and '__pycache__' not in p.parts
             and p.suffix != '.pyc'}
    return dict(base_commit=BASE, files=files, unchanged_reused_inputs=reused)


parser = argparse.ArgumentParser()
parser.add_argument('--verify', action='store_true')
args = parser.parse_args()
actual = snapshot()
if args.verify:
    assert actual == json.loads(MANIFEST.read_text()), 'Checkpoint hashes changed; inspect differences.'
    print(f'PASS: {len(actual["files"])} new files and {len(REUSED)} unchanged base inputs.')
else:
    MANIFEST.write_text(json.dumps(actual, indent=2) + '\n')
    print(f'Wrote {MANIFEST.relative_to(R)}')
