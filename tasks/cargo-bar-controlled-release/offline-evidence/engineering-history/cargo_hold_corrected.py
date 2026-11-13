import sys,json,copy
from pathlib import Path
import numpy as np,mujoco
p=Path('/workspace/cargo-bar/tasks/cargo-bar-controlled-release');sys.path.insert(0,str(p))
from mechanism_cpu import export,initialize,observe
base=json.loads((p/'scene.json').read_text());result=[]
for k,substeps in [(12000.,1),(16000.,1),(12000.,2)]:
 spec=copy.deepcopy(base)
 for a in spec['assemblies']:
  for j in a['joints']:
   if j['name'] in ('left_compliance','right_compliance'):j['stiffness']=k
 
 spec['physics_dt']/=substeps
 xml=export(spec).replace('margin=".00003"','margin=".00003" gap=".00003"').replace('iterations="80"','iterations="120" cone="elliptic" impratio="100"')
 m=mujoco.MjModel.from_xml_string(xml);d=mujoco.MjData(m);initialize(m,d,spec);origin=np.array(observe(m,d,spec)['bodies']['outer_tube']['pos']);samples=[]
 for n in range(round(30/spec['physics_dt'])):
  mujoco.mj_step(m,d)
  if (n+1)%round(5/spec['physics_dt'])==0:
   r=observe(m,d,spec);samples.append(dict(time=r['time'],displacement_m=float(np.linalg.norm(np.array(r['bodies']['outer_tube']['pos'])-origin)),joints=r['joints']))
 row=dict(stiffness=k,cpu_substeps=substeps,samples=samples);result.append(row);print(json.dumps(row),flush=True)
Path('/tmp/cargo-hold-corrected-validation.json').write_text(json.dumps(result,indent=2))
