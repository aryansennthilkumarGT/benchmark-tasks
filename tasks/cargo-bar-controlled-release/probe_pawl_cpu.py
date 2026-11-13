"""Actual contact-driven ratchet pawl positive/negative/released CPU controls.

Initial fixture poses are diagnostic states, not robot actions or Isaac evidence.
"""
import json
import xml.etree.ElementTree as ET
import mujoco
from gearing import ratchet_wheel
from generate_scene import pawl_shapes
from probe_gearing_cpu import fmt,add_geoms
from cpu_contact import options,solid_default,description


def probe(torque=.003,lifted=False):
 root=ET.Element('mujoco',model='AUTHORED_PAWL_CPU_CONTACT')
 ET.SubElement(root,'compiler',angle='radian')
 options(root,1/960,'0 0 0')
 solid_default(root,'.5 0 0',.00002)
 assets=ET.SubElement(root,'asset');world=ET.SubElement(root,'worldbody')
 wheel=ET.SubElement(world,'body',name='wheel');ET.SubElement(wheel,'joint',name='wheel',type='hinge',axis='1 0 0',damping='.00005')
 ET.SubElement(wheel,'inertial',pos='0 0 0',mass='.07',diaginertia='.00001 .00001 .00001')
 shapes=ratchet_wheel()
 for s in shapes:s['pos'][0]+=.016
 add_geoms(assets,wheel,shapes,'wheel')
 pawn=ET.SubElement(world,'body',name='pawl',pos='.0155 -.018 .020')
 ET.SubElement(pawn,'joint',name='pawl',type='hinge',axis='1 0 0',limited='true',range='-.02 .8',stiffness='.02',springref='.65' if lifted else '0',damping='.0004')
 ET.SubElement(pawn,'inertial',pos='0 .0081 -.0025',mass='.008',diaginertia='.0000005 .0000005 .0000001')
 add_geoms(assets,pawn,pawl_shapes(),'pawl')
 model=mujoco.MjModel.from_xml_string(ET.tostring(root,encoding='unicode'));data=mujoco.MjData(model)
 if lifted:data.qpos[1]=.65
 mujoco.mj_forward(model,data);rows=[]
 for step in range(361):
  if step:data.qfrc_applied[0]=torque;mujoco.mj_step(model,data)
  if step%12==0:rows.append(dict(step=step,wheel_rad=float(data.qpos[0]),pawl_rad=float(data.qpos[1]),penetration_m=max([0.]+[-float(c.dist) for c in data.contact[:data.ncon]])))
  if abs(data.qpos[0])>1.0:break
 final=float(data.qpos[0]);expected=(final>.4 if lifted else final<.15 if torque>0 else final<-.4)
 return dict(kind='SUPPLEMENTAL_MUJOCO_CONTACT_RATCHET_PAWL',isaac_executed=False,robot_executed=False,torque_Nm=torque,contact_model=description(.00002),
             initialized_pawl_lifted=lifted,virtual_one_way_rule=False,checks=rows,final_wheel_rad=final,
             passed=bool(expected and max(r['penetration_m'] for r in rows)<.00035))
if __name__=='__main__':
 results=[probe(),probe(-.01),probe(lifted=True)];print(json.dumps(results,indent=2));raise SystemExit(0 if all(d['passed'] for d in results) else 1)
