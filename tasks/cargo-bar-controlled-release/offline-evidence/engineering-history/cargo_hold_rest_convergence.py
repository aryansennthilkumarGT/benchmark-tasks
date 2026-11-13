import sys,json,copy
from pathlib import Path
import numpy as np,mujoco
p=Path('/workspace/cargo-bar/tasks/cargo-bar-controlled-release');sys.path.insert(0,str(p))
from mechanism_cpu import export,initialize,observe
base=json.loads((p/'scene.json').read_text());result=[]
for config in ['gap_noslip','gap_ellipse','gap_ellipse_hard','gap_hard_halfdt']:
 k=16000.
 spec=copy.deepcopy(base)
 for a in spec['assemblies']:
  for j in a['joints']:
   if j['name'] in ('left_compliance','right_compliance'):j['stiffness']=k
 
 if 'halfdt' in config:spec['physics_dt']/=2
 xml=export(spec).replace('margin=".00003"','margin=".00003" gap=".00003"')
 if 'noslip' in config:xml=xml.replace('iterations="80"','iterations="120" noslip_iterations="100" noslip_tolerance="1e-12"')
 if 'ellipse' in config:xml=xml.replace('iterations="80"','iterations="120" cone="elliptic" impratio="100"')
 if 'hard' in config:xml=xml.replace('.99 .999 .0001','.9999 .9999 .0001')
 m=mujoco.MjModel.from_xml_string(xml);d=mujoco.MjData(m);initialize(m,d,spec);origin=np.array(observe(m,d,spec)['bodies']['outer_tube']['pos']);samples=[]
 for n in range(round(10/spec['physics_dt'])):
  mujoco.mj_step(m,d)
  if (n+1)%round(1/spec['physics_dt'])==0:
   r=observe(m,d,spec);samples.append(dict(time=r['time'],displacement_m=float(np.linalg.norm(np.array(r['bodies']['outer_tube']['pos'])-origin)),joints=r['joints']))
 row=dict(stiffness=k,config=config,samples=samples);result.append(row);print(json.dumps(row),flush=True)
Path('/tmp/cargo-hold-rest-convergence.json').write_text(json.dumps(result,indent=2))
