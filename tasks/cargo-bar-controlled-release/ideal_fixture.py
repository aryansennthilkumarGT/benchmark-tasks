"""Ideal rigid-grasp/constraint fixture using actual controller robot FK.

Every task observation here is synthetic. No contact, friction, grasp, release
support or native physics is validated. Robot outputs are tracked ideally, while
articulated poses follow explicit rigid-grasp and quasistatic wall assumptions.
The separate MuJoCo probes provide second-engine mechanism evidence only.
"""
import copy,json,math
from pathlib import Path
import numpy as np
from yam_arena import ik,station
from yam_arena.constants import READY,ARM_JOINTS,FINGER_JOINTS,FINGER_OPEN
from yam_arena.urdf import forward_kinematics
from motion import rotate,multiply,conjugate,axis_quat
from kinematics import reconstruct
from robot_geometry import local_hulls
from audit_geometry import geometry_module

class IdealFixture:
 def __init__(self,folder):
  self.folder=folder;self.spec=json.loads((folder/'scene.json').read_text());self.plan=json.loads((folder/'controller.json').read_text());self.g=geometry_module(folder)
  self.q=np.tile(np.r_[READY,1.],2);self.js=self.spec['initial_joint_values'].copy();self.held={};self.time=0.;self.residual=0.
  defs={b['name']:b for a in self.spec['assemblies'] for b in a['bodies']};self.root=copy.deepcopy({k:defs['outer_tube'][k] for k in ('pos','quat')});self.anchor=copy.deepcopy({k:defs['wall_frame'][k] for k in ('pos','quat')})
  ref=json.loads((folder/'cam-reference.json').read_text());self.reference=sorted(ref['checks'],key=lambda r:r['joints']['handle_rotation']);self.previous=None
  groups={}
  for h in local_hulls():groups.setdefault(h['link'],[]).append(h['vertices'])
  self.bounds={}
  for name,parts in groups.items():
   v=np.concatenate(parts);self.bounds[name]=((v.min(axis=0)+v.max(axis=0))/2,(v.max(axis=0)-v.min(axis=0))/2)
 def tcp(self,side):
  start=0 if side=='left' else 7;p,r=ik.tcp_pose(self.q[start:start+6],station.BASES[side]);return p,ik.matrix_to_quat_xyzw(r)
 def states(self):return dict(wall_frame=copy.deepcopy(self.anchor),**reconstruct(self.spec,self.root,self.js))
 def robot_boxes(self):
  boxes=[]
  for side in ('left','right'):
   off=0 if side=='left' else 7;conf={n:float(v) for n,v in zip(ARM_JOINTS,self.q[off:off+6])};conf.update({n:float(self.q[off+6]*FINGER_OPEN) for n in FINGER_JOINTS})
   transforms=forward_kinematics(__import__('yam_arena').YAM_URDF,conf)
   for name,(center,half) in self.bounds.items():
    m=transforms[name];state=dict(pos=(m[:3,3]+station.BASES[side]).tolist(),quat=ik.matrix_to_quat_xyzw(m[:3,:3]).tolist())
    boxes.append(self.g.box(state,dict(kind='box',pos=center,size=2*half,quat=[0,0,0,1])))
  return boxes
 def frame(self,geometric_metrics=True):
  states=self.states();bodies={}
  for name,b in states.items():
   linear=np.zeros(3);angular=np.zeros(3)
   if self.previous and self.time>self.previous['time']:
    old=self.previous['bodies'][name];dt=self.time-self.previous['time'];linear=(np.array(b['pos'])-old['pos'])/dt
    dq=multiply(b['quat'],conjugate(old['quat']))
    if dq[3]<0:dq=-dq
    length=np.linalg.norm(dq[:3])
    if length>1e-12:angular=dq[:3]/length*(2*math.atan2(length,dq[3]))/dt
   bodies[name]=dict(pos=b['pos'],quat=b['quat'],linear=linear.tolist(),angular=angular.tolist())
  f=dict(schema=1,time=self.time,bodies=bodies,joints=self.js.copy(),max_penetration=float(self.g.maximum_penetration(self.spec,states)) if geometric_metrics else None,
         robot_clearance=float(self.g.robot_clearance(self.robot_boxes(),self.spec,states)) if geometric_metrics else None)
  self.previous=copy.deepcopy(f);return f
 def advance(self,controller,command,index):
  p=controller.phases[index];side=p['side'];width=p.get('grasp_width',0.);name=p.get('contact_body')
  if width and (side not in self.held or self.held[side]['body']!=name):
   tcp,q=self.tcp(side);body=self.states()[name]
   self.held[side]=dict(body=name,offset=rotate(conjugate(q),np.array(body['pos'])-tcp),quat=multiply(conjugate(q),body['quat']))
  if not width:self.held.pop(side,None)
  self.q=command.copy()
  for arm,target in controller.targets.items():
   if target.get('grasp_width',0.):
    off=0 if arm=='left' else 7;self.q[off+6]=max(self.q[off+6],(target['grasp_width']+.0003)/.0939)
  poses={}
  for arm,h in self.held.items():
   tcp,q=self.tcp(arm);poses[h['body']]=dict(pos=tcp+rotate(q,h['offset']),quat=multiply(q,h['quat']))
  if 'inner_tube' in poses:self.root['quat']=poses['inner_tube']['quat'].tolist()
  if 'handle' in poses:
   h=poses['handle']
   if 'inner_tube' in poses:
    q=multiply(conjugate(self.root['quat']),h['quat']);angle=(2*math.atan2(q[0],q[3])+math.pi)%(2*math.pi)-math.pi
    self.js['handle_rotation']=angle
   else:self.root['quat']=multiply(h['quat'],conjugate(axis_quat([1,0,0],self.js['handle_rotation']))).tolist()
   self.root['pos']=(h['pos']-rotate(self.root['quat'],[0,0,-.032])).tolist()
  elif 'inner_tube' in poses:self.root['pos']=(poses['inner_tube']['pos']-rotate(self.root['quat'],[0,self.js['telescope'],0])).tolist()
  if 'inner_tube' in poses and 'handle' in poses:
   relative=rotate(conjugate(self.root['quat']),poses['inner_tube']['pos']-np.array(self.root['pos']))
   self.js['telescope']=float(relative[1]);self.residual=max(self.residual,float(np.linalg.norm(relative[[0,2]])))
  self.js['pinion_rotation']=-self.js['telescope']/self.spec['parameters']['authored_pinion_pitch_radius']
  angle=self.js['handle_rotation'];xp=[r['joints']['handle_rotation'] for r in self.reference]
  for name in ('holding_pawl_rotation','driving_pawl_rotation'):self.js[name]=float(np.interp(angle,xp,[r['joints'][name] for r in self.reference]))
  self.js['trigger_pull']=min(.009,max(0.,.034-self.q[13]*.0939)) if 'handle' in poses else 0.
  axis=rotate(self.root['quat'],[0,1,0]);den=axis[1]
  left=np.array(self.root['pos'])+rotate(self.root['quat'],[0,-.584,0]);right=np.array(self.root['pos'])+rotate(self.root['quat'],[0,.584+self.js['telescope'],0])
  self.js['left_compliance']=float(np.clip((-.600-left[1]+.006*den)/den,0,.004))
  self.js['right_compliance']=float(np.clip((.600-right[1]-.006*den)/den,-.004,0))
  self.time+=1/self.spec['control_hz']
