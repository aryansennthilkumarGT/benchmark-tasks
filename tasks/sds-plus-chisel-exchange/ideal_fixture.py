"""Explicit ideal grasps/quasistatic projections for OFFLINE controller diagnosis.

No dynamic robot/grasp/contact claim. The actual expert never imports this file.
Ball race position is sourced from a passing independent capped-force fixture;
exact analytic sphere contacts project its radial coordinate. A loaded tug may
leave up to300um synthetic grasp compliance at the real geometric barrier.
"""
import copy,hashlib,json,math
from pathlib import Path
import numpy as np
from yam_arena.constants import READY
from motion import rotate,multiply,conjugate,interpolate
from feedback import Controller
from audit_geometry import geometry_module
from kinematics import reconstruct
from scoring import Scorer
HERE=Path(__file__).resolve().parent

class IdealFixture:
 def __init__(self,folder=HERE):
  self.folder=Path(folder);self.spec=json.loads((self.folder/'scene.json').read_text());self.plan=json.loads((self.folder/'controller.json').read_text());reference=json.loads((self.folder/'contact-reference.json').read_text())
  if not reference.get('passed') or reference['scene_sha256']!=hashlib.sha256((self.folder/'scene.json').read_bytes()).hexdigest() or reference['probe_source_sha256']!=hashlib.sha256((self.folder/'probe_cycle_cpu.py').read_bytes()).hexdigest():raise ValueError('Missing/failed/stale real force-fixture reference; cannot qualify ideal assumptions')
  from mechanism_cpu import export
  if reference['export_sha256']!=hashlib.sha256(export(self.spec).encode()).hexdigest():raise ValueError('Stale supplemental physical export')
  start=next(e['time'] for e in reference['events'] if e['stage']=='INSERT');end=next(e['time'] for e in reference['events'] if e['stage']=='TUG');data=[r for r in reference['checks'] if start<=r['time']<=end];self.curve=[]
  for r in data:
   x=r['bodies']['replacement_flat_chisel']['pos'][0]
   if not self.curve or x>self.curve[-1][0]:self.curve.append((x,r['bodies']['locking_ball']['pos'][0]))
  if len(self.curve)<10:raise ValueError('Incomplete independent contact trajectory')
  self.q=np.tile(np.r_[READY,1.],2).astype(float);self.time=0.;self.bodies={b['name']:dict(pos=copy.deepcopy(b['pos']),quat=copy.deepcopy(b['quat']),linear=[0.,0.,0.],angular=[0.,0.,0.]) for a in self.spec['assemblies'] for b in a['bodies']};self.joints=self.spec['initial_joint_values'].copy();self.held={};self.residual=0.;self.g=geometry_module(self.folder);self.inserted=False;self.compiled=self.g.compiled_shapes(self.spec);self.judge_geometry=Scorer(self.spec);self.last_x=self.bodies['replacement_flat_chisel']['pos'][0]
  self.defs={b['name']:b for a in self.spec['assemblies'] for b in a['bodies']};self.front_x=self.spec['parameters']['holder_mouth'][0]+self.spec['parameters']['ball_port_x']
 def frame(self):return dict(schema=1,time=self.time,bodies=copy.deepcopy(self.bodies),joints=self.joints.copy(),robot_clearance=None,feedback_kind='SYNTHETIC_IDEAL_GRASPS_AND_GEOMETRIC_PASSIVE_PROJECTION_NOT_PHYSICS')
 def ball_depth(self,z,others):
  ball=self.defs['locking_ball']['shapes'][0];state=copy.deepcopy(self.bodies['locking_ball']);state['pos'][2]=z;cb,hb,ab=self.g.box(state,ball);lo=cb-hb;hi=cb+hb;depth=0.
  for name in others:
   b=self.bodies[name];lower,upper=self._bounds[name];candidates=np.flatnonzero(np.all(upper>lo,axis=1)&np.all(lower<hi,axis=1))
   for i in candidates:
    shape=self.compiled['shapes'][name][i];depth=max(depth,self.g.sphere_pair_depth(state,ball,b,shape))
  return depth
 def radial_projection(self):
  self._boxes,self._bounds=self.g.world_boxes(self.compiled,self.bodies)
  base=self.bodies['tool_holder']['pos'][2];lo,hi=base+.0072,base+.0099
  if self.ball_depth(hi,['tool_holder','used_point_chisel','replacement_flat_chisel'])>1e-7:raise ValueError('No collision-free radial ball placement')
  for _ in range(15):
   mid=(lo+hi)/2
   if self.ball_depth(mid,['tool_holder','used_point_chisel','replacement_flat_chisel'])>1e-7:lo=mid
   else:hi=mid
  self.bodies['locking_ball']['pos'][2]=hi
  return self.ball_depth(hi,['locking_sleeve'])
 def passive(self,tug=False,previous_new=None):
  root=self.bodies['tool_holder'];mouth=self.spec['parameters']['holder_mouth'][0];new=self.bodies['replacement_flat_chisel'];depth=new['pos'][0]-mouth
  if depth>.0415:self.inserted=True
  x=self.front_x if self.inserted or depth<.010 else float(np.clip(np.interp(new['pos'][0],[r[0] for r in self.curve],[r[1] for r in self.curve]),self.front_x,mouth+.0245))
  self.bodies['locking_ball']['pos']=[x,root['pos'][1],root['pos'][2]+.008]
  collision=self.radial_projection()
  if tug and collision>2e-6 and previous_new is not None:
   proposed=copy.deepcopy(new);safe=copy.deepcopy(previous_new);new.update(pos=copy.deepcopy(safe['pos']),quat=copy.deepcopy(safe['quat']))
   if self.radial_projection()>2e-6:raise ValueError('Previous full tug pose is geometrically invalid')
   low,high=0.,1.
   for _ in range(15):
    mid=(low+high)/2;new.update(pos=(np.asarray(safe['pos'])+(np.asarray(proposed['pos'])-safe['pos'])*mid).tolist(),quat=interpolate(safe['quat'],proposed['quat'],mid).tolist())
    if self.radial_projection()>2e-6:high=mid
    else:low=mid
   new.update(pos=(np.asarray(safe['pos'])+(np.asarray(proposed['pos'])-safe['pos'])*low).tolist(),quat=interpolate(safe['quat'],proposed['quat'],low).tolist());self.radial_projection()
  elif collision>self.spec['penetration_limit']:raise ValueError('Passive ball reference cannot fit current rigid-grasp geometry')
 def advance(self,c,command,index):
  previous=copy.deepcopy(self.bodies);self.q=np.asarray(command,dtype=float).copy();p=c.phases[index];side=p['side'];off=0 if side=='left' else 7
  width=p.get('grasp_width',0.)
  if width and self.q[off+6]<width/.0939:self.q[off+6]=width/.0939
  for arm in list(self.held):
   body,relative,grasp_width=self.held[arm];i=0 if arm=='left' else 7
   if self.q[i+6]<=grasp_width/.0939+.035:self.q[i+6]=max(self.q[i+6],grasp_width/.0939)
   if self.q[i+6]>grasp_width/.0939+.035:
    del self.held[arm]
    if body=='used_point_chisel':
     v=self.judge_geometry.vertices(body,self.bodies[body]);tray=self.bodies['used_chisel_tray'];inside=np.all(np.abs(v[:,0]-tray['pos'][0])<.1155) and np.all(np.abs(v[:,1]-tray['pos'][1])<.0355)
     if inside:self.bodies[body]['pos'][2]+=tray['pos'][2]+.002002-v[:,2].min()
  if p['mode']=='grasp' and width and side not in self.held:
   tcp=c.tcp(side,self.q);active=c.targets[side]
   if np.linalg.norm(tcp['pos']-active['target']['pos'])<.0005 and self.q[off+6]<=width/.0939+.015:self.held[side]=(p['body'],c.relative(tcp,self.bodies[p['body']]),width)
  sleeve_held=False
  for arm,(body,rel,grasp_width) in self.held.items():
   pose=c.compose(c.tcp(arm,self.q),rel)
   if body=='locking_sleeve':self.joints['sleeve_retraction']=float(np.clip(pose['pos'][0]-self.bodies['tool_holder']['pos'][0],0.,.008));sleeve_held=True
   else:self.bodies[body].update(pos=pose['pos'].tolist(),quat=pose['quat'].tolist())
  if not sleeve_held:self.joints['sleeve_retraction']=0.
  for name,pose in reconstruct(self.spec,self.bodies['tool_holder'],self.joints).items():self.bodies[name].update(pose)
  self.passive(tug=p['mode']=='tug',previous_new=previous['replacement_flat_chisel'])
  for arm,(body,rel,width) in self.held.items():
   expected=c.compose(c.tcp(arm,self.q),rel);self.residual=max(self.residual,float(np.linalg.norm(expected['pos']-self.bodies[body]['pos'])))
  for name,b in self.bodies.items():b['linear']=((np.asarray(b['pos'])-previous[name]['pos'])*self.spec['control_hz']).tolist();b['angular']=[0.,0.,0.]
  self.time+=1/self.spec['control_hz']
