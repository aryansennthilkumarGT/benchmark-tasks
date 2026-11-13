"""Supplemental articulated MuJoCo mechanism export; never a robot expert.

Joint frames, convex contact pieces and initial joint coordinates come from the
same original scene. Optional position actuators are explicit diagnostic test-rig
inputs, not claimed YAM capabilities. No virtual rack/pawl/cam update exists.
"""
import hashlib,json,math
from pathlib import Path
import xml.etree.ElementTree as ET
import mujoco,numpy as np
from probe_gearing_cpu import add_geoms,fmt
from motion import rotate,conjugate
from cpu_contact import options,solid_default,description


def export(spec,fixed_root=False,actuators=False):
 root=ET.Element('mujoco',model='CARGO_BAR_SUPPLEMENTAL_CPU')
 ET.SubElement(root,'compiler',angle='radian',inertiafromgeom='false',fusestatic='false')
 options(root,spec['physics_dt'],fmt(spec['gravity']))
 if any(j.get('collision_enabled',False) for a in spec['assemblies'] for j in a['joints']):ET.SubElement(root.find('option'),'flag',filterparent='disable')
 solid_default(root,'.5 0 0',spec['material']['contact_offset'])
 assets=ET.SubElement(root,'asset');world=ET.SubElement(root,'worldbody');ET.SubElement(world,'geom',name='table',type='plane',size='2 2 .05',pos=fmt([0,0,spec['table_top']]))
 defs={b['name']:b for a in spec['assemblies'] for b in a['bodies']};js={j['child']:j for a in spec['assemblies'] for j in a['joints']}
 def inertial(node,b):ET.SubElement(node,'inertial',pos=fmt(b.get('center_of_mass',[0,0,0])),mass=str(b['mass']),diaginertia=fmt(b['diagonal_inertia']),quat=fmt([b.get('principal_axes',[0,0,0,1])[3],*b.get('principal_axes',[0,0,0,1])[:3]]))
 def descend(parent,name):
  b=defs[name];j=js[name];pos=np.array(j['pivot_parent'])-np.array(j['pivot_child'])
  node=ET.SubElement(parent,'body',name=name,pos=fmt(pos));inertial(node,b)
  attrs=dict(name=j['name'],type='hinge' if j['kind']=='revolute' else 'slide',axis={'X':'1 0 0','Y':'0 1 0','Z':'0 0 1'}[j['axis']],
             pos=fmt(j['pivot_child']),limited='true',range=fmt([j['lower'],j['upper']]),stiffness=str(j.get('stiffness',0)),
             springref=str(j.get('rest',0)),damping=str(j.get('damping',0)),solreflimit='.0022 1',solimplimit='.99 .999 .0001')
  ET.SubElement(node,'joint',**attrs);add_geoms(assets,node,b['shapes'],name,materials=spec.get('materials',{}))
  for child,link in js.items():
   if link['parent']==name:descend(node,child)
 for name,b in defs.items():
  if name in js:continue
  q=b['quat'];node=ET.SubElement(world,'body',name=name,pos=fmt(b['pos']),quat=fmt([q[3],*q[:3]]))
  if not b.get('anchor'):
   inertial(node,b)
   if not fixed_root:ET.SubElement(node,'freejoint',name=name+'_free')
  add_geoms(assets,node,b['shapes'],name,materials=spec.get('materials',{}))
  for child,link in js.items():
   if link['parent']==name:descend(node,child)
 contact=ET.SubElement(root,'contact')
 for child,j in js.items():
  if not j.get('collision_enabled',False):ET.SubElement(contact,'exclude',body1=j['parent'],body2=child)
 if actuators:
  motors=ET.SubElement(root,'actuator')
  ET.SubElement(motors,'position',name='fixture_handle',joint='handle_rotation',kp='3',kv='.10',forcelimited='true',forcerange='-.25 .25')
  ET.SubElement(motors,'position',name='fixture_rack',joint='telescope',kp='30000',kv='20',forcelimited='true',forcerange='-60 60')
  ET.SubElement(motors,'position',name='fixture_trigger',joint='trigger_pull',kp='3000',kv='2',forcelimited='true',forcerange='-8 8')
 return ET.tostring(root,encoding='unicode')


def initialize(model,data,spec):
 mujoco.mj_resetData(model,data)
 for name,value in spec['initial_joint_values'].items():
  j=mujoco.mj_name2id(model,mujoco.mjtObj.mjOBJ_JOINT,name);data.qpos[model.jnt_qposadr[j]]=value
 if model.nu:
  data.ctrl[mujoco.mj_name2id(model,mujoco.mjtObj.mjOBJ_ACTUATOR,'fixture_handle')]=spec['initial_joint_values']['handle_rotation']
  data.ctrl[mujoco.mj_name2id(model,mujoco.mjtObj.mjOBJ_ACTUATOR,'fixture_rack')]=spec['initial_joint_values']['telescope']
 mujoco.mj_forward(model,data)


def observe(model,data,spec):
 mujoco.mj_forward(model,data)
 joints={}
 for name in spec['initial_joint_values']:
  j=mujoco.mj_name2id(model,mujoco.mjtObj.mjOBJ_JOINT,name);joints[name]=float(data.qpos[model.jnt_qposadr[j]])
 bodies={}
 for a in spec['assemblies']:
  for b in a['bodies']:
   i=mujoco.mj_name2id(model,mujoco.mjtObj.mjOBJ_BODY,b['name']);q=data.xquat[i]
   bodies[b['name']]=dict(pos=data.xpos[i].tolist(),quat=[*q[1:],q[0]])
 return dict(time=float(data.time),joints=joints,bodies=bodies,contact_depth_m=max([0.]+[-float(c.dist) for c in data.contact[:data.ncon]]))


def probe(folder):
 spec=json.loads((folder/'scene.json').read_text())
 from audit_geometry import geometry_module
 initial={b['name']:dict(pos=b['pos'],quat=b['quat']) for a in spec['assemblies'] for b in a['bodies']}
 if geometry_module(folder).maximum_penetration(spec,initial)>.00005:raise ValueError('Initial solid interference: repair CAD before contact simulation')
 xml=export(spec,True,True);model=mujoco.MjModel.from_xml_string(xml);data=mujoco.MjData(model);initialize(model,data,spec)
 rows=[]
 for step in range(4801):
  t=step*spec['physics_dt']
  data.ctrl[2]=.0085
  data.ctrl[0]=min(2.60,max(0.,t-.5)*.8)
  if step:mujoco.mj_step(model,data)
  if step%96==0:rows.append(observe(model,data,spec))
 # Conservative radial bound on each actual nose collider, not an arbitrary
 # minimum hinge angle. Box circumradius subtraction cannot overstate clearance.
 clearances={};final=rows[-1];defs={b['name']:b for a in spec['assemblies'] for b in a['bodies']}
 gear=final['bodies']['gear_set']
 for name in ('holding_pawl','driving_pawl'):
  body=final['bodies'][name];shape=defs[name]['shapes'][1]
  center=np.array(body['pos'])+rotate(body['quat'],shape['pos'])
  local=rotate(conjugate(gear['quat']),center-np.array(gear['pos']))
  radius=float(np.linalg.norm(local[1:]));bound=radius-float(np.linalg.norm(np.array(shape['size'])/2))-.020
  clearances[name]=bound
 contacts=[]
 for i,c in enumerate(data.contact[:data.ncon]):
  force=np.zeros(6);mujoco.mj_contactForce(model,data,i,force)
  if abs(force[0])>.01:
   contacts.append(dict(geom1=mujoco.mj_id2name(model,mujoco.mjtObj.mjOBJ_GEOM,c.geom1),geom2=mujoco.mj_id2name(model,mujoco.mjtObj.mjOBJ_GEOM,c.geom2),normal_force_N=float(force[0]),distance_m=float(c.dist)))
 contacts.sort(key=lambda r:-abs(r['normal_force_N']))
 return dict(kind='SUPPLEMENTAL_MUJOCO_DIAGNOSTIC_CAM_ACTUATION',engine=mujoco.__version__,isaac_executed=False,robot_executed=False,
             contact_export_sha256=hashlib.sha256(xml.encode()).hexdigest(),contact_model=description(spec['material']['contact_offset']),
             test_rig_actuators=True,test_rig_handle_torque_cap_Nm=.25,robot_grasp_validated=False,pawl_clearance_lower_bounds_m=clearances,virtual_gear_constraint=False,checks=rows,actuator_force=data.actuator_force.tolist(),contacts=contacts[:25],
             passed=min(clearances.values())>=.0008 and rows[-1]['joints']['handle_rotation']>2.45 and max(r['contact_depth_m'] for r in rows)<.00035 and all(j['lower']-(.0003 if j['kind']=='prismatic' else .03)<=r['joints'][j['name']]<=j['upper']+(.0003 if j['kind']=='prismatic' else .03) for a in spec['assemblies'] for j in a['joints'] for r in rows))

if __name__=='__main__':
 d=probe(Path(__file__).resolve().parent);print(json.dumps(d,indent=2));raise SystemExit(0 if d['passed'] else 1)
