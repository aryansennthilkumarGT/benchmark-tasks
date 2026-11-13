"""Synthetic rigid-grasp kinematic fixture; explicitly NOT physics evidence.

The real controller and pinned YAM FK execute normally. Grasps and the released
brad settling into its tray are ideal assumptions. Passive opening bail angles
are interpolated from the separately labelled CPU test rig. None of these
operations are available to the native expert or scorer.
"""
import copy,json,math
from pathlib import Path
import numpy as np
from yam_arena import ik,station
from yam_arena.constants import READY
from motion import rotate,multiply,conjugate,qangle
from kinematics import reconstruct


class IdealFixture:
 def __init__(self,folder):
  self.folder=folder;self.spec=json.loads((folder/'scene.json').read_text());self.plan=json.loads((folder/'controller.json').read_text())
  self.q=np.tile(np.r_[READY,1.],2);self.js=self.spec['initial_joint_values'].copy();self.time=0.;self.held={};self.residual=0.;self.previous=None
  defs={b['name']:b for a in self.spec['assemblies'] for b in a['bodies']};self.root=copy.deepcopy({k:defs['nose_body'][k] for k in ('pos','quat')})
  self.free={n:copy.deepcopy({k:defs[n][k] for k in ('pos','quat')}) for n in ('bent_brad','parts_tray')}
  ref=json.loads((folder/'guided-cycle-reference.json').read_text());self.opening=sorted([r for r in ref['checks'] if r['time']<4.01],key=lambda r:r['joints']['lever_rotation'])
  self.door_opening=sorted([r for r in ref['checks'] if 4.0<r['time']<8.01],key=lambda r:r['joints']['door_rotation'])
 def tcp(self,side):
  i=0 if side=='left' else 7;p,r=ik.tcp_pose(self.q[i:i+6],station.BASES[side]);return dict(pos=p,quat=ik.matrix_to_quat_xyzw(r))
 def states(self):return dict(**reconstruct(self.spec,self.root,self.js),**copy.deepcopy(self.free))
 def frame(self,geometric_metrics=False):
  states=self.states();bodies={}
  for n,b in states.items():
   v=np.zeros(3);w=np.zeros(3)
   if self.previous:
    old=self.previous['bodies'][n];v=(np.array(b['pos'])-old['pos'])*self.spec['control_hz'];dq=multiply(b['quat'],conjugate(old['quat']))
    if dq[3]<0:dq=-dq
    length=np.linalg.norm(dq[:3])
    if length>1e-12:w=dq[:3]/length*2*math.atan2(length,dq[3])*self.spec['control_hz']
   bodies[n]=dict(pos=list(b['pos']),quat=list(b['quat']),linear=v.tolist(),angular=w.tolist())
  f=dict(time=self.time,joints=self.js.copy(),bodies=bodies,max_penetration=0.,robot_clearance=.03)
  if geometric_metrics:
   from audit_geometry import geometry_module
   g=geometry_module(self.folder);f['max_penetration']=float(g.maximum_penetration(self.spec,states))
  self.previous=copy.deepcopy(f);return f
 def angle(self,parent,child):
  q=multiply(conjugate(parent['quat']),child['quat']);return (2*math.atan2(q[2],q[3])+math.pi)%(2*math.pi)-math.pi
 def advance(self,controller,command,index):
  p=controller.phases[index];side=p['side'];width=p.get('grasp_width',0.);name=p.get('contact_body');before=self.states()
  if width and (side not in self.held or self.held[side]['body']!=name):
   tcp=self.tcp(side);body=before[name];self.held[side]=dict(body=name,offset=rotate(conjugate(tcp['quat']),np.array(body['pos'])-tcp['pos']),quat=multiply(conjugate(tcp['quat']),body['quat']))
  if not width:self.held.pop(side,None)
  self.q=np.asarray(command).copy()
  for arm,target in controller.targets.items():
   if target.get('grasp_width',0.):
    off=0 if arm=='left' else 7;self.q[off+6]=max(self.q[off+6],(target['grasp_width']+.0003)/.0939)
  poses={}
  for arm,h in self.held.items():
   tcp=self.tcp(arm);body=dict(pos=tcp['pos']+rotate(tcp['quat'],h['offset']),quat=multiply(tcp['quat'],h['quat']))
   if h['body'] in poses:self.residual=max(self.residual,float(np.linalg.norm(body['pos']-poses[h['body']]['pos'])))
   poses[h['body']]=body
  if 'nose_door' in poses:self.js['door_rotation']=self.angle(self.root,poses['nose_door'])
  current=self.states()
  if 'latch_lever' in poses:self.js['lever_rotation']=self.angle(current['nose_door'],poses['latch_lever'])
  if p['label']=='Lift jam-clear lever':
   xp=[r['joints']['lever_rotation'] for r in self.opening]
   self.js['bail_rotation']=float(np.interp(self.js['lever_rotation'],xp,[r['joints']['bail_rotation'] for r in self.opening]));self.js['bail_extension']=float(np.interp(self.js['lever_rotation'],xp,[r['joints']['bail_extension'] for r in self.opening]))
  if p['label']=='Open nose door':
   # The contact fixture's passive draw bail changes angle during door opening.
   # Keeping it artificially locked would invent an inaccessible start state.
   xp=[r['joints']['door_rotation'] for r in self.door_opening]
   for name in ('bail_rotation','bail_extension'):
    self.js[name]=float(np.interp(self.js['door_rotation'],xp,[r['joints'][name] for r in self.door_opening]))
  current=self.states()
  if 'bail_crosspin' in poses:
   pin=poses['bail_crosspin'];self.js['bail_rotation']=self.angle(current['latch_lever'],pin);current=self.states();bail=current['draw_bail'];vector=rotate(conjugate(bail['quat']),pin['pos']-np.asarray(bail['pos']))
   self.js['bail_extension']=float(vector[0]-self.spec['parameters']['draw_rest']);self.residual=max(self.residual,float(np.linalg.norm(vector[1:])))
  if 'bent_brad' in poses:self.free['bent_brad']={k:list(v) for k,v in poses['bent_brad'].items()}
  elif p['label']=='Release brad into tray':
   # Explicitly synthetic support: not a falling/release-contact test.
   self.free['bent_brad']['pos'][2]=self.spec['table_top']+.006
  self.time+=1/self.spec['control_hz']
