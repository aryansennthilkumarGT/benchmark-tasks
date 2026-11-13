import sys,json,copy
from pathlib import Path
import numpy as np,mujoco
p=Path('/workspace/cargo-bar/tasks/cargo-bar-controlled-release');sys.path.insert(0,str(p))
from mechanism_cpu import export,initialize,observe
base=json.loads((p/'scene.json').read_text());result=[]
for k,torsion in [(12000.,.01),(16000.,.005),(16000.,.01)]:
 spec=copy.deepcopy(base)
 for a in spec['assemblies']:
  for j in a['joints']:
   if j['name'] in ('left_compliance','right_compliance'):j['stiffness']=k
 
 import xml.etree.ElementTree as ET
 root=ET.fromstring(export(spec))
 for name in ['left_pad0','right_pad0']:
  g=root.find(f'.//geom[@name="{name}"]');g.set('condim','4');g.set('friction',f'.575 {torsion} 0')
 m=mujoco.MjModel.from_xml_string(ET.tostring(root,encoding='unicode'));d=mujoco.MjData(m);initialize(m,d,spec);origin=np.array(observe(m,d,spec)['bodies']['outer_tube']['pos']);samples=[]
 for n in range(round(10/spec['physics_dt'])):
  mujoco.mj_step(m,d)
  if (n+1)%round(1/spec['physics_dt'])==0:
   r=observe(m,d,spec);samples.append(dict(time=r['time'],displacement_m=float(np.linalg.norm(np.array(r['bodies']['outer_tube']['pos'])-origin)),joints=r['joints']))
 row=dict(stiffness=k,torsional_coefficient_m=torsion,samples=samples);result.append(row);print(json.dumps(row),flush=True)
Path('/tmp/cargo-hold-patch-duration.json').write_text(json.dumps(result,indent=2))
