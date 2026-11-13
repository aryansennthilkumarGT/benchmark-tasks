"""Actual MuJoCo CPU contact-driven rack/pinion probe, without a gear equality.

No Isaac, robot, measured hardware or expert evidence. Applied torque is an
explicit diagnostic design input; neither gear joint is motor-positioned.
"""
import json,math
from pathlib import Path
import xml.etree.ElementTree as ET
import mujoco
from gearing import pinion,rack,RADIUS,PITCH
from cpu_contact import options,solid_default,description


def fmt(v):return ' '.join(str(float(x)) for x in v)

def add_geoms(assets,b,shapes,name,contact_enabled=True,materials=None):
 for i,s in enumerate(shapes):
  q=s['quat'];a=dict(name=name+str(i),pos=fmt(s['pos']),quat=fmt([q[3],*q[:3]]),contype='1' if contact_enabled else '0',conaffinity='1' if contact_enabled else '0')
  if s.get('material'):
   values=(materials or {'cam':dict(dynamic_friction=.08)}).get(s['material'])
   if values is None:raise ValueError('Missing explicit CPU material: '+s['material'])
   coefficient=values.get('cpu_dynamic_against_default',values['dynamic_friction'])
   a['friction']=fmt([coefficient,0,0])
  if s['kind']=='box':a.update(type='box',size=fmt([v/2 for v in s['size']]))
  elif s['kind']=='convex':
   mesh=name+str(i)+'mesh';triangles=[]
   for face in s['faces']:
    for k in range(1,len(face)-1):triangles.extend([face[0],face[k],face[k+1]])
   ET.SubElement(assets,'mesh',name=mesh,vertex=fmt([v for p in s['vertices'] for v in p]),face=' '.join(str(x) for x in triangles))
   a.update(type='mesh',mesh=mesh)
  else:a.update(type='cylinder',size=fmt([s['radius'],s['height']/2]))
  ET.SubElement(b,'geom',**a)


def probe(friction=.5,margin=.00002,torque=-.0015,contact_enabled=True):
 root=ET.Element('mujoco',model='AUTHORED_GEAR_CPU_CONTACT_PROBE')
 options(root,1/960,'0 0 0')
 solid_default(root,fmt([friction,0.,0.]),margin)
 assets=ET.SubElement(root,'asset');world=ET.SubElement(root,'worldbody')
 for name,pos,shapes,mass,inertia in [('pinion',[0,.04,0],pinion(),.04,[.000004,.000003,.000003]),
            ('rack',[0,0,0],rack(pitch_plane=RADIUS+.00005,phase=PITCH/2),.12,[.00011,.00001,.00011])]:
  b=ET.SubElement(world,'body',name=name,pos=fmt(pos));ET.SubElement(b,'joint',name=name,type='hinge' if name=='pinion' else 'slide',axis='1 0 0' if name=='pinion' else '0 1 0',damping='.00005' if name=='pinion' else '.02')
  ET.SubElement(b,'inertial',pos='0 0 0',mass=str(mass),diaginertia=fmt(inertia))
  add_geoms(assets,b,shapes,name,contact_enabled)
 xml=ET.tostring(root,encoding='unicode');m=mujoco.MjModel.from_xml_string(xml);d=mujoco.MjData(m);rows=[]
 for i in range(241):
  if i:
   d.qfrc_applied[0]=torque;mujoco.mj_step(m,d)
  if i%12==0:
   error=float(d.qpos[1]+d.qpos[0]*RADIUS)
   rows.append(dict(step=i,pinion_rad=float(d.qpos[0]),rack_m=float(d.qpos[1]),lead_error_m=error,
                    penetration_m=max([0.]+[-float(c.dist) for c in d.contact[:d.ncon]])))
 result=dict(kind='SUPPLEMENTAL_MUJOCO_CONTACT_DRIVEN_GEARING',engine=mujoco.__version__,isaac_executed=False,
             robot_executed=False,virtual_gear_constraint=False,applied_torque_Nm=torque,friction=friction,margin_m=margin,contact_model=description(margin),checks=rows,
             passed=bool(d.qpos[1]>.002 and d.qpos[0]<-.15 and max(abs(r['lead_error_m']) for r in rows)<.0003 and max(r['penetration_m'] for r in rows)<.0003))
 return result
if __name__=='__main__':
 result=probe();print(json.dumps(result,indent=2));raise SystemExit(0 if result['passed'] else 1)
