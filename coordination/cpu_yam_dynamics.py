"""Supplemental CPU YAM dynamics, never Isaac/PhysX or hardware qualification.

Robot collisions/inertias/joint frames come from the pinned official URDF;
position gains, force limits, gravity compensation and station bases come from
its adapter. No virtual grasps or object pose writes after initialization.
PhysX joint friction coefficients have no direct MuJoCo frictionloss equivalent:
zero Coulomb joint loss is a disclosed diagnostic assumption, not a unit conversion.
"""
from __future__ import annotations
import argparse,hashlib,json,sys,time
from pathlib import Path
import xml.etree.ElementTree as ET
import mujoco,numpy as np
from yam_arena import YAM_URDF,station
from yam_arena.constants import ARM_JOINTS,FINGER_JOINTS,FINGER_OPEN,READY,SHOULDER,WRIST,GRIPPER
from yam_arena.urdf import rpy_matrix,forward_kinematics
from yam_arena.ik import matrix_to_quat_xyzw


def fmt(values):return ' '.join(format(float(v),'.17g') for v in values)
def xyz(node,name,default='0 0 0'):return np.array([float(v) for v in node.get(name,default).split()]) if node is not None else np.zeros(3)
def wxyz(matrix):
 q=matrix_to_quat_xyzw(matrix);return [q[3],*q[:3]]

def robot_sources():
 import yam_arena.constants as constants
 root=ET.parse(YAM_URDF).getroot();paths=[Path(YAM_URDF),Path(constants.__file__),Path(constants.__file__).with_name('robot.py'),Path(constants.__file__).with_name('actions.py'),Path(constants.__file__).with_name('station.py'),Path(constants.__file__).with_name('urdf.py'),Path(constants.__file__).with_name('ik.py')]
 paths.extend((YAM_URDF.parent/m.get('filename')).resolve() for m in root.findall('.//collision/geometry/mesh'))
 return {str(p.relative_to(YAM_URDF.parents[2])) if p.is_relative_to(YAM_URDF.parents[2]) else p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(set(paths))}


def add_robots(root,*,contact_friction=.5,contact_timeconstant=.0022):
 """Add two independently actuated official chains to an existing MJCF tree."""
 urdf=ET.parse(YAM_URDF).getroot();links={n.get('name'):n for n in urdf.findall('link')};children={}
 for j in urdf.findall('joint'):children.setdefault(j.find('parent').get('link'),[]).append(j)
 asset=root.find('asset')
 if asset is None:asset=ET.SubElement(root,'asset')
 world=root.find('worldbody')
 if world is None:world=ET.SubElement(root,'worldbody')
 actuator=root.find('actuator')
 if actuator is None:actuator=ET.SubElement(root,'actuator')
 meshes={}
 def inertia(node,link):
  inertial=link.find('inertial');o=inertial.find('origin');i=inertial.find('inertia');r=rpy_matrix(xyz(o,'rpy'));matrix=np.array([[float(i.get('ixx')),float(i.get('ixy')),float(i.get('ixz'))],[float(i.get('ixy')),float(i.get('iyy')),float(i.get('iyz'))],[float(i.get('ixz')),float(i.get('iyz')),float(i.get('izz'))]])
  tensor=r@matrix@r.T;vals,axes=np.linalg.eigh(tensor)
  if vals.min()<=0:raise ValueError('Nonpositive official robot inertia')
  if np.linalg.det(axes)<0:axes[:,0]*=-1
  ET.SubElement(node,'inertial',mass=inertial.find('mass').get('value'),pos=fmt(xyz(o,'xyz')),diaginertia=fmt(vals),quat=fmt(wxyz(axes)))
 def descend(parent,name,side,joint=None):
  link=links[name];attrs=dict(name=side+'_'+name,gravcomp='1')
  if joint is None:attrs['pos']=fmt(station.BASES[side])
  else:
   origin=joint.find('origin');attrs.update(pos=fmt(xyz(origin,'xyz')),quat=fmt(wxyz(rpy_matrix(xyz(origin,'rpy')))))
  node=ET.SubElement(parent,'body',**attrs);inertia(node,link)
  if joint is not None:
   n=joint.get('name');limit=joint.find('limit');cfg=GRIPPER if n in FINGER_JOINTS else SHOULDER if n in ARM_JOINTS[:3] else WRIST
   jname=side+'_'+n;lo=float(limit.get('lower'));hi=float(limit.get('upper'))
   ET.SubElement(node,'joint',name=jname,type='slide' if joint.get('type')=='prismatic' else 'hinge',axis=fmt(xyz(joint.find('axis'),'xyz')),limited='true',range=fmt([lo,hi]),damping='0',frictionloss='0',actuatorgravcomp='true',actuatorfrclimited='true',actuatorfrcrange=fmt([-cfg['effort'],cfg['effort']]))
   ET.SubElement(actuator,'position',name=jname+'_drive',joint=jname,kp=str(cfg['stiffness']),kv=str(cfg['damping']),ctrllimited='true',ctrlrange=fmt([lo,hi]),forcelimited='true',forcerange=fmt([-cfg['effort'],cfg['effort']]))
  for index,c in enumerate(link.findall('collision')):
   m=c.find('geometry/mesh')
   if m is None:raise ValueError('Unreviewed official robot collider kind')
   path=(YAM_URDF.parent/m.get('filename')).resolve();scale=m.get('scale','1 1 1');key=(path,scale)
   if key not in meshes:
    meshname='official_yam_'+str(len(meshes));ET.SubElement(asset,'mesh',name=meshname,file=str(path),scale=scale,maxhullvert='-1');meshes[key]=meshname
   o=c.find('origin');ET.SubElement(node,'geom',name=side+'_'+name+'_'+str(index),type='mesh',mesh=meshes[key],pos=fmt(xyz(o,'xyz')),quat=fmt(wxyz(rpy_matrix(xyz(o,'rpy')))),contype='2' if side=='left' else '4',conaffinity='5' if side=='left' else '3',friction=fmt([contact_friction,0,0]),density='0',margin='.00002',gap='.00002',solref=fmt([contact_timeconstant,1.]),solmix='1000000')
  for j in children.get(name,[]):descend(node,j.find('child').get('link'),side,j)
 for side in ('left','right'):descend(world,'base',side)
 return root


def export_robot_only(timestep=1/1920):
 root=ET.Element('mujoco',model='SUPPLEMENTAL_OFFICIAL_YAM_CPU')
 ET.SubElement(root,'compiler',angle='radian',inertiafromgeom='false',fusestatic='false')
 ET.SubElement(root,'option',timestep=str(timestep),gravity='0 0 -9.81',integrator='implicitfast',solver='Newton',iterations='120',cone='elliptic',impratio='100')
 world=ET.SubElement(root,'worldbody');ET.SubElement(world,'geom',name='table',type='plane',pos='0 0 .7475',size='2 2 .05',contype='1',conaffinity='6',friction='.5 0 0')
 return ET.tostring(add_robots(root),encoding='unicode')


def indexes(model):
 return {side:[mujoco.mj_name2id(model,mujoco.mjtObj.mjOBJ_JOINT,side+'_'+n) for n in ARM_JOINTS+FINGER_JOINTS] for side in ('left','right')}
def initialize_robot(model,data,q=None):
 q=np.tile(np.r_[READY,1.],2) if q is None else np.asarray(q)
 for side,ids in indexes(model).items():
  off=0 if side=='left' else 7;values=[*q[off:off+6],q[off+6]*FINGER_OPEN,q[off+6]*FINGER_OPEN]
  for jid,value in zip(ids,values):
   data.qpos[model.jnt_qposadr[jid]]=value
   name=mujoco.mj_id2name(model,mujoco.mjtObj.mjOBJ_JOINT,jid);aid=mujoco.mj_name2id(model,mujoco.mjtObj.mjOBJ_ACTUATOR,name+'_drive');data.ctrl[aid]=value
 mujoco.mj_forward(model,data)

def measured(model,data):
 values=[]
 for side,ids in indexes(model).items():
  q=[float(data.qpos[model.jnt_qposadr[j]]) for j in ids];values.extend([*q[:6],(q[6]+q[7])/(2*FINGER_OPEN)])
 return np.asarray(values)

def command_robot(model,data,command):
 q=np.asarray(command,dtype=float)
 if q.shape!=(14,) or not np.isfinite(q).all():raise ValueError('Invalid14D robot action')
 pending=[]
 for side,ids in indexes(model).items():
  off=0 if side=='left' else 7;values=[*q[off:off+6],q[off+6]*FINGER_OPEN,q[off+6]*FINGER_OPEN]
  for jid,value in zip(ids,values):
   name=mujoco.mj_id2name(model,mujoco.mjtObj.mjOBJ_JOINT,jid);aid=mujoco.mj_name2id(model,mujoco.mjtObj.mjOBJ_ACTUATOR,name+'_drive')
   if not model.actuator_ctrlrange[aid,0]-1e-8<=value<=model.actuator_ctrlrange[aid,1]+1e-8:raise ValueError('Action exceeds official robot joint range')
   pending.append((aid,value))
 for aid,value in pending:data.ctrl[aid]=value

def hold(seconds=2.):
 xml=export_robot_only();m=mujoco.MjModel.from_xml_string(xml);d=mujoco.MjData(m);initialize_robot(m,d);q0=measured(m,d);max_error=0.;depth=0.;effort=0.
 for _ in range(round(seconds/m.opt.timestep)):
  mujoco.mj_step(m,d);max_error=max(max_error,float(np.abs(measured(m,d)-q0).max()));depth=max(depth,max([0.]+[-float(c.dist) for c in d.contact[:d.ncon]]));effort=max(effort,float(np.abs(d.qfrc_actuator).max()))
 warnings={mujoco.mjtWarning(i).name:int(row.number) for i,row in enumerate(d.warning) if row.number}
 return dict(kind='SUPPLEMENTAL_MUJOCO_ACTUATED_YAM_HOLD',harness_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),engine=mujoco.__version__,isaac_executed=False,hardware_executed=False,seconds=float(d.time),model_sha256=hashlib.sha256(xml.encode()).hexdigest(),robot_sources=robot_sources(),gains_source='Pinned yam_arena.constants, overriding placeholder URDF effort1',gravity_compensation='Robot bodies only; MuJoCo gravity compensation routed into joint actuator force limits',unmapped_native_friction_coefficients=dict(shoulder=SHOULDER['friction'],wrist=WRIST['friction']),authored_joint_frictionloss=0.,authored_robot_contact_friction=.5,maximum_position_drift=max_error,maximum_contact_depth_m=depth,maximum_abs_actuator_effort=effort,warnings=warnings,passed=bool(max_error<1e-4 and depth<.0002 and not warnings))

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--seconds',type=float,default=2.);p.add_argument('--output',type=Path);a=p.parse_args()
 if not 0.<a.seconds<=30.:raise SystemExit('Bounded CPU hold must be0..30seconds')
 r=hold(a.seconds);s=json.dumps(r,indent=2)+'\n'
 if a.output:a.output.write_text(s)
 else:print(s,end='')
 raise SystemExit(0 if r['passed'] else 1)
