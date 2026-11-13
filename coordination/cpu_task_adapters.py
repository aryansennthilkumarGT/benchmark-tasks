"""Reviewed adapters for unchanged ER/cargo task sources in CPU YAM trials.

These adapters export original geometry and read actual integrated state. They
never command task bodies/joints, attach parts or substitute nominal feedback.
A separate process is required for each independent task source namespace.
"""
from __future__ import annotations
import hashlib,importlib,json
from pathlib import Path
from types import SimpleNamespace
import xml.etree.ElementTree as ET
import mujoco,numpy as np
from yam_arena import ik,station,YAM_URDF
from yam_arena.constants import ARM_JOINTS,FINGER_JOINTS,FINGER_OPEN
from yam_arena.urdf import forward_kinematics


def runtime_hashes(folder):
 files=list(folder.glob('*.py'))+list(folder.glob('*.json'))+list((folder/'assets').glob('*.usda'))
 return {p.relative_to(folder).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)}


def initialize(model,data,spec):
 # Task test-rig initializers sometimes use model.nu as a proxy for their
 # optional fixture actuators. That is false once the two real robots exist.
 # Initialize only actual declared task joints, before ordinary integration.
 mujoco.mj_resetData(model,data)
 for name,value in spec.get('initial_joint_values',{}).items():
  jid=mujoco.mj_name2id(model,mujoco.mjtObj.mjOBJ_JOINT,name)
  if jid<0:raise ValueError('Missing original task joint: '+name)
  data.qpos[model.jnt_qposadr[jid]]=value
 mujoco.mj_forward(model,data)


def observe(model,data,spec):
 mujoco.mj_forward(model,data);joints={};bodies={}
 for name in spec.get('initial_joint_values',{}):
  jid=mujoco.mj_name2id(model,mujoco.mjtObj.mjOBJ_JOINT,name)
  if jid<0:raise ValueError('Missing original task joint: '+name)
  joints[name]=float(data.qpos[model.jnt_qposadr[jid]])
 for a in spec['assemblies']:
  for b in a['bodies']:
   name=b['name'];bid=mujoco.mj_name2id(model,mujoco.mjtObj.mjOBJ_BODY,name)
   if bid<0:raise ValueError('Missing original task body: '+name)
   v=np.zeros(6);mujoco.mj_objectVelocity(model,data,mujoco.mjtObj.mjOBJ_BODY,bid,v,0);q=data.xquat[bid]
   bodies[name]=dict(pos=data.xpos[bid].tolist(),quat=[*q[1:],q[0]],linear=v[3:].tolist(),angular=v[:3].tolist())
 return dict(schema=1,time=float(data.time),joints=joints,bodies=bodies)


class RobotClearance:
 def __init__(self,geometry_module):
  groups={}
  for h in geometry_module.local_hulls():groups.setdefault(h['link'],[]).append(h['vertices'])
  self.bounds={}
  for name,parts in groups.items():
   v=np.concatenate(parts);self.bounds[name]=((v.min(0)+v.max(0))/2,(v.max(0)-v.min(0))/2)
 def boxes(self,q,geometry):
  rows=[]
  for side in ('left','right'):
   off=0 if side=='left' else 7;conf=dict(zip(ARM_JOINTS,q[off:off+6]));conf.update({n:float(q[off+6]*FINGER_OPEN) for n in FINGER_JOINTS})
   transforms=forward_kinematics(YAM_URDF,conf)
   for name,(center,half) in self.bounds.items():
    m=transforms[name];body=dict(pos=(m[:3,3]+station.BASES[side]).tolist(),quat=ik.matrix_to_quat_xyzw(m[:3,:3]).tolist())
    rows.append(geometry.box(body,dict(kind='box',pos=center,size=2*half,quat=[0,0,0,1])))
  return rows


def er_export(folder,spec):
 # Read the actual authored USD material, as the existing standalone CPU probe
 # does; do not invent a scene-level coefficient when this source has none.
 from pxr import Usd,UsdPhysics
 coefficients=set()
 for a in spec['assemblies']:
  stage=Usd.Stage.Open(str(folder/'assets'/(a['name']+'.usda')))
  mat=UsdPhysics.MaterialAPI(stage.GetPrimAtPath('/Asset/Material'))
  coefficients.add((float(mat.GetStaticFrictionAttr().Get()),float(mat.GetDynamicFrictionAttr().Get())))
 if len(coefficients)!=1:raise ValueError('Mixed ER materials require reviewed per-collider mapping')
 static,dynamic=coefficients.pop();probe=importlib.import_module('cpu_contact_probe');boxes=importlib.import_module('convex_box_backend')
 root=ET.fromstring(probe.model_xml(spec,dict(static_friction=static,dynamic_friction=dynamic)))
 # Match the exact eight-corner mesh backend of qualified ER contact probes.
 return ET.tostring(boxes.mesh_boxes(root),encoding='unicode')


def load(folder,slug):
 if slug not in ('er-collet-nut-preassembly','cargo-bar-controlled-release'):
  raise ValueError('No reviewed CPU task adapter: '+slug)
 common={n:importlib.import_module(n) for n in ('feedback','scoring','audit_geometry','robot_geometry')}
 if slug=='cargo-bar-controlled-release':export=importlib.import_module('mechanism_cpu').export
 else:export=lambda spec:er_export(folder,spec)
 common['mechanism_cpu']=SimpleNamespace(export=export,initialize=initialize,observe=observe)
 common['source_identity']=SimpleNamespace(runtime_hashes=runtime_hashes)
 common['robot_clearance']=RobotClearance(common['robot_geometry'])
 return common
