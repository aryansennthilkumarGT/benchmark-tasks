"""Read exact freshly fetched official comparator revisions; never execute task code."""
from pathlib import Path
import subprocess,json,hashlib,sys,importlib.util
D=Path(__file__).resolve().parent;repo=D.parents[2];rows=[]
for tag,ref,slug in [('yubi-neighbor','refs/implementation/pr1872',None),('faze-neighbor','refs/implementation/pr893',None),('toshiba-neighbor','refs/implementation/official-main','refit-a-gas-burner-head-and-cap')]:
 pin=subprocess.check_output(['git','rev-parse',ref],text=True,cwd=repo).strip();paths=subprocess.check_output(['git','ls-tree','-r','--name-only',ref],text=True,cwd=repo).splitlines()
 taskpaths=[p for p in paths if p.endswith('task.json') and (slug is None or '/'+slug+'/' in p)]
 # PR heads contain many unchanged tasks: identify the intended task family.
 if tag=='yubi-neighbor':taskpaths=[p for p in taskpaths if any(k in p for k in ['bungee','strap','hook'])]
 if tag=='faze-neighbor':taskpaths=[p for p in taskpaths if '/gear-train/' in p]
 for p in taskpaths:
  prefix=p.rsplit('/',1)[0]
  files=[f for f in paths if f.startswith(prefix+'/') and ((f.endswith(('task.json','README.md','task.py','gear_train.py','bungeekit.py')) or f.endswith('/'+prefix.rsplit('/',1)[-1].replace('-','_')+'.py')))]
  for f in files:
   b=subprocess.check_output(['git','show',ref+':'+f],cwd=repo);o=D/'official'/tag/f;o.parent.mkdir(parents=True,exist_ok=True);o.write_bytes(b);rows.append(dict(tag=tag,pin=pin,original_path=f,local=str(o.relative_to(D)),sha256=hashlib.sha256(b).hexdigest()))
(D/'OFFICIAL_SNAPSHOT.json').write_text(json.dumps(dict(files=rows,promotion_beyond_CPU=False,limitation='Fresh immutable head contents; pendingstatus/ownership is not certified by Git heads alone'),indent=2)+'\n')
print('Preserved current comparator files',len(rows))
