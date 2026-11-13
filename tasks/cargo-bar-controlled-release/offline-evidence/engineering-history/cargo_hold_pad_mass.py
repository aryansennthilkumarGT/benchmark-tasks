import sys,json,copy
from pathlib import Path
import numpy as np,mujoco
p=Path('/workspace/cargo-bar/tasks/cargo-bar-controlled-release');sys.path.insert(0,str(p))
from mechanism_cpu import export,initialize,observe
base=json.loads((p/'scene.json').read_text());result=[]
for mass in [.12,.18,.24]:
 k=16000.
 spec=copy.deepcopy(base)
 for a in spec['assemblies']:
  for j in a['joints']:
   if j['name'] in ('left_compliance','right_compliance'):j['stiffness']=k
 
 for a in spec['assemblies']:
  for b in a['bodies']:
   if b['name'] in ('left_pad','right_pad'):
    scale=mass/b['mass'];b['mass']=mass;b['diagonal_inertia']=[v*scale for v in b['diagonal_inertia']]
 m=mujoco.MjModel.from_xml_string(export(spec));d=mujoco.MjData(m);initialize(m,d,spec);origin=np.array(observe(m,d,spec)['bodies']['outer_tube']['pos']);samples=[]
 for n in range(4800):
  mujoco.mj_step(m,d)
  if (n+1)%960==0:
   r=observe(m,d,spec);samples.append(dict(time=r['time'],displacement_m=float(np.linalg.norm(np.array(r['bodies']['outer_tube']['pos'])-origin)),joints=r['joints']))
 row=dict(stiffness=k,pad_mass=mass,samples=samples);result.append(row);print(json.dumps(row),flush=True)
Path('/tmp/cargo-hold-pad-mass-duration.json').write_text(json.dumps(result,indent=2))
