"""Checkpoint integrity; excludes Python caches and the manifest itself."""
from pathlib import Path
import argparse,hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1]
def record(p,label):
 raw=p.read_bytes();return dict(path=label,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
def collect():
 files=[record(p,str(p.relative_to(D))) for p in sorted(D.rglob('*')) if p.is_file() and p.name!='MANIFEST.json' and '__pycache__' not in p.parts and p.suffix!='.pyc']
 paths=['research/robocurve-acceptance/preflight/access_core.py',
        'research/robocurve-acceptance/preflight/assets/YAM_REFERENCE.json.gz',
        'research/robocurve-acceptance/preflight/assets/YAM_SOURCE_MANIFEST.json',
        'research/robocurve-implementation/common/access.py']

 inputs=[record(R/p,p) for p in paths]
 expected={'foot_structure.STEP':'0a8abaa627806dccb68e760d76ef90f5469534658a8ad612c6cd83d373e9550c','lower_leg_structure_base.STEP':'47a20c48fa1434f470af34d0187ee32686e892d595b03198785f6f2a9b14f11c','lower_leg_structure_fork.STEP':'8a2c115de859c8407c759848b42bf4e9b4c9e6f5f9d71d48755f544def5add27'}
 for row in inputs+[record(D/'sources/odri/step_files'/name,'sources/odri/step_files/'+name) for name in expected]:
  name=Path(row['path']).name
  if name in expected:assert row['sha256']==expected[name],name+' source mismatch'
 return dict(base_commit='851a4bb2c2d9edc649c64b75b4babd0a487ba943',source_pins=dict(cello='f4b572107fcd4c2d59bb563462e21ba39d878fa6',chefman_attributed_mirror='fb7bd3c6ad7e26472d89719efe55d281cff8c528',ODRI='66af1522b4fba0ec4a1d7790e66f5e4652208d30'),checkpoint_files=files,reused_source_inputs=inputs)
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--verify',action='store_true');args=parser.parse_args();data=collect()
 if args.verify:assert data==json.loads((D/'MANIFEST.json').read_text()),'Checkpoint changed; inspect before deliberately refreshing'
 else:(D/'MANIFEST.json').write_text(json.dumps(data,indent=2)+'\n')
 print('Verified' if args.verify else 'Recorded',len(data['checkpoint_files']),'checkpoint files and',len(data['reused_source_inputs']),'reused source inputs')
