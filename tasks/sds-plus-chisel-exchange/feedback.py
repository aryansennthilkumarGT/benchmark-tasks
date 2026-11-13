"""SDS chisel expert: real14D YAM actions, physical sleeve and ball feedback.

No object setters, virtual attachment, phase-switched contact or score access.
A bounded retention tug advances only300um beyond the observed held pose.
"""
import copy,math
from collections import deque
import numpy as np
try:
 from .motion import Motion,ControlFailure,rotate,multiply,conjugate,qangle
 from .plan_controller import scene_digest
 from .interfaces import retained
except ImportError:
 from motion import Motion,ControlFailure,rotate,multiply,conjugate,qangle
 from plan_controller import scene_digest
 from interfaces import retained

class Controller:
 def __init__(self,plan,spec):
  if plan.get('scene_content_sha256')!=scene_digest(spec):raise ControlFailure('Stale scene/controller binding')
  self.phases=plan['phases'];self.spec=spec;self.reset()
 def reset(self):
  self.index=0;self.done=False;self.failed=None;self.actions=0;self.events=[];self.started=None;self.last_time=None;self.targets={};self.motion={s:Motion(s) for s in ('left','right')};self.stable=None;self.progress_time=None;self.best=float('inf');self.context={};self.attempts={};self.recovery=None
 def fail(self,s):self.failed=s;self.events.append(dict(event='FAIL_STOP',phase=self.index,time=self.last_time,reason=s));raise ControlFailure(s)
 def tcp(self,side,q):
  i=0 if side=='left' else 7;m=self.motion[side];pos,r=m.ik.tcp_pose(q[i:i+6],m.base);return dict(pos=np.asarray(pos),quat=m.ik.matrix_to_quat_xyzw(r))
 def relative(self,a,b):return dict(pos=rotate(conjugate(a['quat']),np.asarray(b['pos'])-a['pos']),quat=multiply(conjugate(a['quat']),b['quat']))
 def compose(self,a,b):return dict(pos=np.asarray(a['pos'])+rotate(a['quat'],b['pos']),quat=multiply(a['quat'],b['quat']))
 def bind(self,p,f,q):
  target=copy.deepcopy(p);mode=p['mode'];tcp=self.tcp(p['side'],q);self.context={}
  if mode=='grasp':
   b=f['bodies'][p['body']];quat=np.asarray(p['tool_quat']);pos=np.asarray(b['pos'])+rotate(b['quat'],p['offset'])-rotate(quat,[0,0,p['away']]);target['target']=dict(pos=pos,quat=quat)
  elif mode in ('release','withdraw'):
   target['target']=tcp
   if mode=='withdraw':target['target']['pos']=tcp['pos']-rotate(tcp['quat'],[0,0,p['distance']])
  elif mode=='body_goal':
   b=f['bodies'][p['body']];grasp=self.relative(b,tcp);goal=copy.deepcopy(p['body_goal']);goal['quat']=goal['quat'] if goal['quat'] is not None else b['quat'];target['target']=self.compose(goal,grasp);target['bound_body_goal']=goal;self.context['grasp']=grasp
  elif mode=='tug':
   b=f['bodies'][p['body']];self.context=dict(grasp=self.relative(b,tcp),start=np.array(b['pos']),window=deque());target['target']=tcp
  return target
 def physical(self,p,f):
  metric=0.
  for c in p.get('joint_checks',[]):metric+=max(0.,c['min']-f['joints'][c['name']],f['joints'][c['name']]-c['max'])
  if p.get('require_retained') and not retained(self.spec,f['bodies'],f['joints']):metric+=.001
  if p['mode']=='body_goal':
   b=f['bodies'][p['body']];goal=p['bound_body_goal'];metric+=max(0.,np.linalg.norm(np.asarray(b['pos'])-goal['pos'])-.0006)+.02*max(0.,qangle(b['quat'],goal['quat'])-.025)
  return metric<1e-9,metric
 def retry(self,p,f,q):
  if not p['label'].startswith('Grip'):self.fail('Motion or physical-feedback stall: '+p['label'])
  n=self.attempts.get(self.index,0)+1
  if n>2:self.fail('Bounded grasp recovery exhausted')
  self.attempts[self.index]=n;off=0 if p['side']=='left' else 7;width=p['grasp_width']
  if q[off+6]>width/.0939+.05:self.fail('Unexpected wide obstruction during grip')
  retry=copy.deepcopy(p);retry['opening']=(width+.002)/.0939;retry['grasp_width']=0.;retry['target']['pos']=np.asarray(retry['target']['pos'])-rotate(retry['target']['quat'],[0,0,.006]);self.recovery=dict(target=retry,started=f['time']);self.events.append(dict(event='OPEN_BACKOFF_REACQUIRE',phase=self.index,attempt=n,time=f['time']))
 def step(self,joints,f):
  q=np.asarray(joints,dtype=float);now=float(f['time'])
  if q.shape!=(14,) or not np.isfinite(q).all() or not math.isfinite(now):raise ControlFailure('Malformed robot/native observation')
  if self.failed:raise ControlFailure(self.failed)
  if self.last_time is not None and now<=self.last_time:self.fail('Stale physical observation')
  self.last_time=now;self.actions+=1
  if self.actions>self.spec['run_limit']:self.fail('Action limit exhausted')
  if self.done:return q.copy()
  phase=self.phases[self.index]
  if self.started is None:
   self.targets[phase['side']]=self.bind(phase,f,q);self.started=now;self.progress_time=now;self.best=float('inf');self.stable=None;self.events.append(dict(event='PHASE_START',phase=self.index,label=phase['label'],time=now))
  active=self.recovery['target'] if self.recovery else self.targets[phase['side']];output=q.copy();error=theta=0.;tug_complete=False
  if active['mode']=='tug' and not self.recovery:
   b=f['bodies'][active['body']];ctx=self.context;start=ctx['start'];d=float(start[0]-b['pos'][0]);tcp=self.tcp(active['side'],q);body_tcp=self.compose(b,ctx['grasp'])
   if np.linalg.norm(tcp['pos']-body_tcp['pos'])>.0009:self.fail('Retention tug lost its acquired grasp')
   if d>active['maximum_withdrawal']+.0003 or not retained(self.spec,f['bodies'],f['joints']):self.fail('Replacement pulled free during retention check')
   goal=copy.deepcopy(b);goal['pos']=np.array(b['pos']);goal['pos'][0]=max(start[0]-active['maximum_withdrawal'],b['pos'][0]-active['feedback_overtravel']);active['target']=self.compose(goal,ctx['grasp'])
   ctx['window'].append((now,float(b['pos'][0])))
   while len(ctx['window'])>1 and ctx['window'][1][0]<=now-active['dwell']:ctx['window'].popleft()
   tug_complete=(now-self.started>=.8 and d>=.0005 and now-ctx['window'][0][0]>=active['dwell']-1e-8 and np.ptp([r[1] for r in ctx['window']])<=.0001)
  try:
   for side,p in self.targets.items():
    if side==phase['side']:p=active
    off=0 if side=='left' else 7;cmd,pe,re=self.motion[side].target(q[off:off+7],p['target']['pos'],p['target']['quat'],p['opening'],speed=p['speed'],angular_speed=.65);output[off:off+7]=cmd
    if side==phase['side']:error,theta=pe,re
  except (ControlFailure,KeyError,ValueError) as e:self.fail(str(e))
  off=0 if phase['side']=='left' else 7;width=active.get('grasp_width',0.)/.0939
  grip=(max(active['opening']+.005,width-.02)<q[off+6]<width+.03) if width else abs(q[off+6]-active['opening'])<.03
  physical,pm=self.physical(active,f);reached=(error<active['position_tolerance'] and theta<active['angle_tolerance'] and grip and physical) if active['mode']!='tug' else tug_complete and grip
  metric=error+.02*theta+pm
  if metric<self.best-.00008:self.best=metric;self.progress_time=now
  if self.recovery:
   if now-self.recovery['started']>8:self.fail('Grasp recovery timeout')
   if reached:self.recovery=None;self.targets[phase['side']]=self.bind(phase,f,q);self.started=None
   return output
  if now-self.started>phase['timeout'] or not reached and now-self.progress_time>6:self.retry(active,f,q);return output
  if reached:
   if self.stable is None:self.stable=now
   if active['mode']=='tug' or now-self.stable>=phase['dwell']:
    held=copy.deepcopy(active);held['mode']='world';held.pop('require_retained',None);held.pop('joint_checks',None);held['target']=self.tcp(phase['side'],q);self.targets[phase['side']]=held;self.events.append(dict(event='PHYSICAL_FEEDBACK_PHASE_COMPLETE',phase=self.index,label=phase['label'],time=now,position_error_m=error,rotation_error_rad=theta));self.index+=1;self.started=None;self.done=self.index==len(self.phases)
  else:self.stable=None
  return output
