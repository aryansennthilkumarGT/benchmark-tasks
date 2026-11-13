import sys,json,copy
from pathlib import Path
import numpy as np,mujoco
p=Path('/workspace/cargo-bar/tasks/cargo-bar-controlled-release');sys.path.insert(0,str(p))
from mechanism_cpu import export,initialize,observe
base=json.loads((p/'scene.json').read_text());result=[]
for config in ['euler','convex_boxes']:
 k=16000.
 spec=copy.deepcopy(base)
 for a in spec['assemblies']:
  for j in a['joints']:
   if j['name'] in ('left_compliance','right_compliance'):j['stiffness']=k
 
 xml=export(spec)
 if config=='euler':xml=xml.replace('integrator="implicitfast"','integrator="Euler"')
 if config=='convex_boxes':
  import xml.etree.ElementTree as ET,itertools
  root=ET.fromstring(xml);assets=root.find('asset')
  for i,g in enumerate(root.findall('.//geom')):
   if g.get('type')!='box':continue
   h=[float(x) for x in g.attrib.pop('size').split()];name='diagnostic_box_'+str(i)
   vertices=list(itertools.product(*[(-v,v) for v in h]))
   ET.SubElement(assets,'mesh',name=name,vertex=' '.join(str(x) for p in vertices for x in p))
   g.set('type','mesh');g.set('mesh',name)
  xml=ET.tostring(root,encoding='unicode')
 m=mujoco.MjModel.from_xml_string(xml);d=mujoco.MjData(m);initialize(m,d,spec);origin=np.array(observe(m,d,spec)['bodies']['outer_tube']['pos']);samples=[]
 for n in range(4800):
  mujoco.mj_step(m,d)
  if (n+1)%960==0:
   r=observe(m,d,spec);samples.append(dict(time=r['time'],displacement_m=float(np.linalg.norm(np.array(r['bodies']['outer_tube']['pos'])-origin)),joints=r['joints']))
 row=dict(stiffness=k,config=config,samples=samples);result.append(row);print(json.dumps(row),flush=True)
Path('/tmp/cargo-hold-backend-duration.json').write_text(json.dumps(result,indent=2))
