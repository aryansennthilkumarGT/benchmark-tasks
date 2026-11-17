from pathlib import Path
import subprocess,json,hashlib
D=Path(__file__).resolve().parent
specs=[('CELLO-1204','refs/implementation/cello-pr1204','tasks/helping-hands-cross-wires',['task.json','README.md','helping_hands_cross_wires.py']),('CELLO-1315','refs/implementation/cello-pr1315','tasks/monitor-portrait-locks',['task.json','README.md','numeric_score.py','contract.py']),('CELLO-2396','refs/implementation/cello-pr2396','tasks/aim-a-desk-lamp-onto-an-open-book',['task.json','README.md','task.py','desk_lamp/mech.py']),('CELLO-813','refs/implementation/cello-pr813','tasks/v-wheel-preload', ['task.json','README.md','task.py','parts.py']),('CELLO-2203','refs/implementation/cello-pr2203','tasks/set-timing-belt-tension',['task.json','README.md','belt_task.py','mechanics.py']),('ODRI-2212','refs/implementation/odri-pr2212','tasks/install-a-motor-shaft-encoder',['task.json','README.md','task.py','geom.py']),('ODRI-2014','refs/implementation/odri-pr2014','tasks/fr3-guide-swap',['task.json','README.md','task.py','mechkit.py']),('ODRI-1576','refs/implementation/cello-official-main','tasks/o-ring-into-groove',['task.json','README.md','task.py','ringkit.py'])]
previous=json.loads((D/"OFFICIAL_FILES.json").read_text()) if (D/"OFFICIAL_FILES.json").exists() else []
manifest=[]
for tag,ref,prefix,names in specs:
 if not names:
  paths=subprocess.check_output(['git','ls-tree','-r','--name-only',ref,prefix],text=True).splitlines()
  paths=[p for p in paths if 'belt' in p and p.endswith(('/task.json','/README.md','/task.py'))]
 else:paths=[prefix+'/'+n for n in names]
 resolved=subprocess.run(['git','rev-parse','--verify',ref],capture_output=True,text=True)
 if resolved.returncode:
  pin=next(x['pin'] for x in previous if x['tag']==tag)
  if subprocess.run(['git','cat-file','-e',pin],capture_output=True).returncode:
   subprocess.run(['git','fetch','--no-tags','https://github.com/robocurve/benchmark-tasks.git',pin],check=True)
  ref=pin
 else:pin=resolved.stdout.strip()
 for path in paths:
  r=subprocess.run(['git','show',ref+':'+path],capture_output=True)
  if r.returncode:raise RuntimeError(path)
  p=D/'official'/tag/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(r.stdout)
  manifest.append(dict(tag=tag,pin=pin,original_path=path,local=str(p.relative_to(D)),sha256=hashlib.sha256(r.stdout).hexdigest()))
(D/'OFFICIAL_FILES.json').write_text(json.dumps(manifest,indent=2)+'\n');print(len(manifest),'files captured')
