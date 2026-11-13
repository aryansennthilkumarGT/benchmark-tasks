"""Supplemental MuJoCo contact model; no robot, Isaac or hardware evidence.

Every transform, inertial frame, contact solid and passive joint comes from the
original scene. Optional actuators are explicitly force-limited diagnostic rigs,
never expert actions. There are no virtual lock or tool-release state rules.
"""
import hashlib,json
from pathlib import Path
import xml.etree.ElementTree as ET
import mujoco,numpy as np
from cpu_contact import options,solid_default,description


def fmt(values):return ' '.join(format(float(v),'.17g') for v in values)


def add_geoms(assets,node,body,materials=None):
 for i,shape in enumerate(body['shapes']):
  q=shape['quat'];name=body['name']+'_'+str(i)
  attrs=dict(name=name,pos=fmt(shape['pos']),quat=fmt([q[3],*q[:3]]))
  material=(materials or {}).get(shape.get('material'))
  if material:attrs['friction']=fmt([material['dynamic_friction'],0,0])
  if not shape.get('collision',True):attrs.update(contype='0',conaffinity='0')
  if shape['kind']=='box':attrs.update(type='box',size=fmt(np.asarray(shape['size'])/2))
  elif shape['kind']=='sphere':attrs.update(type='sphere',size=fmt([shape['radius']]))
  elif shape['kind']=='cylinder':attrs.update(type='cylinder',size=fmt([shape['radius'],shape['height']/2]))
  elif shape['kind']=='convex':
   mesh=name+'_mesh';faces=[]
   for f in shape['faces']:
    for j in range(1,len(f)-1):faces.extend([f[0],f[j],f[j+1]])
   ET.SubElement(assets,'mesh',name=mesh,vertex=fmt(np.asarray(shape['vertices']).ravel()),face=' '.join(str(v) for v in faces))
   attrs.update(type='mesh',mesh=mesh)
  else:raise ValueError('Unsupported physical geometry '+shape['kind'])
  ET.SubElement(node,'geom',**attrs)


def export(spec,actuators=False):
 root=ET.Element('mujoco',model='SDS_CHISEL_SUPPLEMENTAL_CONTACT')
 ET.SubElement(root,'compiler',angle='radian',inertiafromgeom='false',fusestatic='false')
 opt=options(root,spec['physics_dt'],fmt(spec['gravity']));ET.SubElement(opt,'flag',filterparent='disable')
 solid_default(root,fmt([spec['material']['dynamic_friction'],0,0]),spec['material']['contact_offset'])
 assets=ET.SubElement(root,'asset');world=ET.SubElement(root,'worldbody')
 ET.SubElement(world,'geom',name='table',type='plane',size='2 2 .05',pos=fmt([0,0,spec['table_top']]))
 defs={b['name']:b for a in spec['assemblies'] for b in a['bodies']};joints={j['child']:j for a in spec['assemblies'] for j in a['joints']}
 def inertial(node,body):
  q=body['principal_axes'];ET.SubElement(node,'inertial',mass=str(body['mass']),pos=fmt(body['center_of_mass']),diaginertia=fmt(body['diagonal_inertia']),quat=fmt([q[3],*q[:3]]))
 def descend(parent,name):
  body=defs[name];j=joints[name];position=np.asarray(j['pivot_parent'])-j['pivot_child']
  node=ET.SubElement(parent,'body',name=name,pos=fmt(position));inertial(node,body)
  ET.SubElement(node,'joint',name=j['name'],type='hinge' if j['kind']=='revolute' else 'slide',axis={'X':'1 0 0','Y':'0 1 0','Z':'0 0 1'}[j['axis']],pos=fmt(j['pivot_child']),limited='true',range=fmt([j['lower'],j['upper']]),stiffness=str(j['stiffness']),springref=str(j['rest']),damping=str(j['damping']),solreflimit='.0022 1',solimplimit='.99 .999 .0001')
  add_geoms(assets,node,body,spec.get('materials'))
  for child,link in joints.items():
   if link['parent']==name:descend(node,child)
 for name,body in defs.items():
  if name in joints:continue
  q=body['quat'];node=ET.SubElement(world,'body',name=name,pos=fmt(body['pos']),quat=fmt([q[3],*q[:3]]))
  if not body.get('anchor'):inertial(node,body);ET.SubElement(node,'freejoint',name=name+'_free')
  add_geoms(assets,node,body,spec.get('materials'))
  for child,link in joints.items():
   if link['parent']==name:descend(node,child)
 if actuators:raise ValueError('Only declared external diagnostic wrenches are supported')
 return ET.tostring(root,encoding='unicode')


def initialize(model,data,spec):
 mujoco.mj_resetData(model,data)
 for name,value in spec['initial_joint_values'].items():
  i=mujoco.mj_name2id(model,mujoco.mjtObj.mjOBJ_JOINT,name);data.qpos[model.jnt_qposadr[i]]=value
 if model.nu:data.ctrl[:]=0.
 mujoco.mj_forward(model,data)


def observe(model,data,spec,refresh=True):
 if refresh:mujoco.mj_forward(model,data)
 states={};joints={}
 for name in spec['initial_joint_values']:
  i=mujoco.mj_name2id(model,mujoco.mjtObj.mjOBJ_JOINT,name);joints[name]=float(data.qpos[model.jnt_qposadr[i]])
 for a in spec['assemblies']:
  for b in a['bodies']:
   i=mujoco.mj_name2id(model,mujoco.mjtObj.mjOBJ_BODY,b['name']);q=data.xquat[i];v=np.zeros(6)
   mujoco.mj_objectVelocity(model,data,mujoco.mjtObj.mjOBJ_XBODY,i,v,0)
   states[b['name']]=dict(pos=data.xpos[i].tolist(),quat=[*q[1:],q[0]],linear=v[3:].tolist(),angular=v[:3].tolist())
 return dict(time=float(data.time),joints=joints,bodies=states,max_penetration=max([0.]+[-float(c.dist) for c in data.contact[:data.ncon]]),robot_clearance=None)

