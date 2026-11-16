"""Record/verify checkpoint bytes and the immutable source inputs actually reused.

Run after run_all.py. Manifest excludes itself and Python caches; no network needed.
"""
from pathlib import Path
import argparse
import hashlib
import json

D = Path(__file__).resolve().parent
R = D.parents[1]

def record(path, label):
    data = path.read_bytes()
    return {'path': label, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}

def collect():
    files = [record(p, str(p.relative_to(D))) for p in sorted(D.rglob('*'))
             if p.is_file() and p.name != 'MANIFEST.json'
             and '__pycache__' not in p.parts and p.suffix != '.pyc']
    refs = [
        'research/robocurve-acceptance/preflight/access_core.py',
        'research/robocurve-acceptance/preflight/assets/YAM_REFERENCE.json.gz',
        'research/robocurve-acceptance/preflight/assets/YAM_SOURCE_MANIFEST.json',
        'research/robocurve-final-discovery/agents/robot_build/evidence/fetch_yubi_pinned.py',
        'research/robocurve-final-discovery/agents/robot_build/evidence/yubi/docs/AssemblyInstruction/YUBI Glove Assy_AssemblyGuide.pdf',
        'research/robocurve-final-discovery/agents/robot_build/evidence/yubi/docs/BOM/YUBI Glove Assy_BOM.md',
        'research/robocurve-final-discovery/agents/robot_build/evidence/faze4/assembly.txt',
        'research/robocurve-final-discovery/agents/robot_build/evidence/faze4/Assembly instructions 3.1.pdf',
        'research/robocurve-final-discovery/evidence/household/039.txt',
        'research/robocurve-final-discovery/evidence/household/microwave-turntable.png',
    ]
    prefix = 'research/robocurve-final-discovery/agents/robot_build/evidence/faze4/STL_V2/STL_V2/STL/Elbow/J4 cyclo/'
    refs += [prefix + n for n in ['11_1 cyclo disc.STL', 'Joint 4 motor case.STL',
             'Joint 4 Output shaft.STL', 'Eccentric shaft J4.STL', 'Joint 4 top cover.STL']]
    sources = [record(R / p, p) for p in refs]
    original = Path('/tmp/yubi-pinned-source/STEP/glove/YUBI Glove Assy_ver2_R.STEP')
    if not original.exists():
        original = R / 'research/robocurve-final-discovery/agents/robot_build/evidence/yubi/STEP/glove/YUBI Glove Assy_ver2_R.STEP'
    cad = record(original, 'reacquired YUBI Glove Assy_ver2_R.STEP')
    assert cad['sha256'] == '7cffdf898a1cf54b897e95c116aa9dea6ac4307c06964d551001ecf938f321dd'
    sources.append(cad)
    return {'base_research_commit': '3c0a99a80408e6f80c6a6c7cbd01ea827af12e34',
            'scope': 'Checkpoint integrity, not hardware validation; original Toshiba PDF hash/provenance is recorded in SOURCE_AND_ASSUMPTIONS.md',
            'checkpoint_files': files, 'reused_source_inputs': sources}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--verify', action='store_true')
    args = parser.parse_args()
    data = collect()
    if args.verify:
        assert json.loads((D / 'MANIFEST.json').read_text()) == data, 'Checkpoint bytes changed; inspect before regenerating'
        print('Manifest verified:', len(data['checkpoint_files']), 'checkpoint files;', len(data['reused_source_inputs']), 'source inputs')
    else:
        (D / 'MANIFEST.json').write_text(json.dumps(data, indent=2) + '\n')
        print('Recorded', len(data['checkpoint_files']), 'checkpoint files;', len(data['reused_source_inputs']), 'source inputs')
