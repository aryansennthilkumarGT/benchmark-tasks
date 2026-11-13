exec(open('/tmp/cargo_hold_duration.py').read().split('for k in')[0])
import xml.etree.ElementTree as ET
from motion import rotate,conjugate,multiply
for config in ['frozen_internal','frozen_internal_noslip']:
 spec=copy.deepcopy(base)
 for a in spec['assemblies']:
  for j in a['joints']:
   if j['name'] in ('left_compliance','right_compliance'):j['stiffness']=16000.
 root=ET.fromstring(export(spec));defs={b['name']:b for a in spec['assemblies'] for b in a['bodies']}
 for a in spec['assemblies']:
  for j in a['joints']:
   if j['name'] in ('left_compliance','right_compliance'):continue
   node=root.find(".//body[@name='"+j['child']+"']");parent=defs[j['parent']];child=defs[j['child']]
   pos=rotate(conjugate(parent['quat']),np.array(child['pos'])-np.array(parent['pos']));q=multiply(conjugate(parent['quat']),child['quat'])
   node.set('pos',' '.join(str(x) for x in pos));node.set('quat',' '.join(str(x) for x in [q[3],*q[:3]]));node.remove(node.find('joint'))
 if 'noslip' in config:root.find('option').set('noslip_iterations','30')
 m=mujoco.MjModel.from_xml_string(ET.tostring(root,encoding='unicode'));d=mujoco.MjData(m);mujoco.mj_resetData(m,d)
 for name in ('left_compliance','right_compliance'):
  i=mujoco.mj_name2id(m,mujoco.mjtObj.mjOBJ_JOINT,name);d.qpos[m.jnt_qposadr[i]]=spec['initial_joint_values'][name]
 mujoco.mj_forward(m,d);i=mujoco.mj_name2id(m,mujoco.mjtObj.mjOBJ_BODY,'outer_tube');origin=d.xpos[i].copy();samples=[]
 for n in range(4800):
  mujoco.mj_step(m,d)
  if (n+1)%960==0:samples.append(dict(time=d.time,displacement=float(np.linalg.norm(d.xpos[i]-origin)),qvel=d.qvel[:6].tolist()))
 result.append(dict(config=config,samples=samples));print(json.dumps(result[-1]),flush=True)
Path('/tmp/cargo-hold-isolate.json').write_text(json.dumps(result,indent=2))
