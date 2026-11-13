"""Cargo-bar expert: native-state feedback, real robot actions, bounded recovery.

No object pose/joint setter, scorer query, attachment or virtual transmission.
Live references compensate for actual bar pose. Physical joint/clearance checks
prevent an empty/slipping grasp from silently completing a manipulation phase.
"""
import copy,math
import numpy as np
try:
 from .motion import Motion,ControlFailure,axis_quat,rotate,multiply,qangle,conjugate
except ImportError:
 from motion import Motion,ControlFailure,axis_quat,rotate,multiply,qangle,conjugate

class Controller:
 def __init__(self,plan,spec):self.phases=plan['phases'];self.spec=spec;self.reset()
 def reset(self):
  self.index=0;self.done=False;self.failed=None;self.events=[];self.grasps={};self.thread=None
  self.motion={s:Motion(s,tracking_error_limit=.025) for s in ('left','right')}
  self.targets={};self.started=None;self.last_time=None;self.stable=None;self.best=float('inf');self.progress_time=None
  self.actions=0;self.recovery=None;self.attempts={}
 def fail(self,message):
  self.failed=message;self.events.append(dict(event='FAIL_STOP',phase=self.index,reason=message,time=self.last_time));raise ControlFailure(message)
 def resolve(self,p,frame):
  if 'reference_body' not in p:return p
  b=frame['bodies'][p['reference_body']];out=dict(p)
  out['target']=dict(pos=(np.array(b['pos'])+rotate(b['quat'],p['reference_offset'])+p.get('world_offset',[0,0,0])).tolist(),
                     quat=multiply(b['quat'],p['reference_quat']).tolist())
  return out
 def bind(self,p,frame):
  if p.get('reference_live'):return p
  out=self.resolve(p,frame);out=dict(out);out.pop('reference_body',None);return out
 def physical_checks(self,p,frame):
  metric=0.;ok=True
  for check in p.get('joint_checks',[]):
   value=frame['joints'][check['name']];distance=max(check['min']-value,0.,value-check['max'])
   metric+=distance*(.02 if check.get('angular') else 1.);ok=ok and distance==0.
  if p.get('pawls_clear'):
   defs={b['name']:b for a in self.spec['assemblies'] for b in a['bodies']};gear=frame['bodies']['gear_set']
   for name in ('holding_pawl','driving_pawl'):
    b=frame['bodies'][name];shape=defs[name]['shapes'][1]
    center=np.array(b['pos'])+rotate(b['quat'],shape['pos']);point=rotate(conjugate(gear['quat']),center-np.array(gear['pos']))
    clearance=np.linalg.norm(point[1:])-np.linalg.norm(np.array(shape['size'])/2)-.020
    gap=max(0.,.0008-clearance);metric+=gap;ok=ok and gap==0.
  if 'root_target' in p:
   distance=math.dist(frame['bodies']['outer_tube']['pos'],p['root_target']);metric+=max(0.,distance-.002)
   ok=ok and distance<=.002
  if p.get('require_still'):
   for body in frame['bodies'].values():
    speed=float(np.linalg.norm(body['linear']));spin=float(np.linalg.norm(body['angular']))
    metric+=max(0.,speed-.008)+.01*max(0.,spin-.15);ok=ok and speed<=.008 and spin<=.15
  return bool(ok),float(metric)
 def begin_recovery(self,p,now):
  count=self.attempts.get(self.index,0)
  if count>=2:self.fail('Grip recovery attempts exhausted: '+p['label'])
  if not p['label'].startswith(('Grip','Regrasp','Squeeze')):self.fail('Motion/physical-feedback stall: '+p['label'])
  retry=copy.deepcopy(p);retry['opening']=min(1.,max(.62,p.get('grasp_width',0.)/.0939+.12));retry['grasp_width']=0.
  retry['dwell']=.3;retry['joint_checks']=[];retry['pawls_clear']=False
  self.attempts[self.index]=count+1;self.recovery=dict(phase=retry,started=now,stable=None);self.targets[p['side']]=retry
  self.events.append(dict(event='REOPEN_AND_REACQUIRE',phase=self.index,attempt=count+1,time=now))
 def step(self,joints,frame):
  q=np.asarray(joints,dtype=float);now=float(frame['time'])
  if q.shape!=(14,) or not np.isfinite(q).all() or not math.isfinite(now):raise ControlFailure('Invalid robot observation')
  if self.failed:raise ControlFailure(self.failed)
  if self.last_time is not None and now<=self.last_time:self.fail('Stale/nonmonotonic native observation')
  if 'bodies' not in frame or 'joints' not in frame:self.fail('Native physical feedback missing')
  self.last_time=now;self.actions+=1
  if self.actions>self.spec['run_limit']:self.fail('Expert action limit exhausted')
  if self.done:return q.copy()
  phase=self.phases[self.index]
  if self.started is None:
   self.started=now;self.progress_time=now;self.best=float('inf');self.stable=None;self.targets[phase['side']]=self.bind(phase,frame)
   self.events.append(dict(event='PHASE_START',phase=self.index,label=phase['label'],time=now))
  active=self.recovery['phase'] if self.recovery else phase;output=q.copy();error=theta=0.
  try:
   for side,p in self.targets.items():
    p=self.resolve(p,frame);start=0 if side=='left' else 7
    action,pe,re=self.motion[side].target(q[start:start+7],p['target']['pos'],p['target']['quat'],p['opening'],speed=p['speed'],angular_speed=.5)
    output[start:start+7]=action
    if side==phase['side']:error,theta=pe,re
  except (ControlFailure,KeyError,ValueError) as exc:self.fail(str(exc))
  offset=0 if phase['side']=='left' else 7;width=active.get('grasp_width',0.)/.0939
  gripped=(max(active['opening']+.01,width-.035)<q[offset+6]<width+.04) if width else abs(q[offset+6]-active['opening'])<.03
  physical,physical_error=self.physical_checks(active,frame)
  reached=error<active['position_tolerance'] and theta<active['angle_tolerance'] and gripped and physical
  if self.recovery:
   r=self.recovery
   if now-r['started']>12.:self.fail('Recovery timeout: '+phase['label'])
   if reached:
    if r['stable'] is None:r['stable']=now
    if now-r['stable']>=active['dwell']:
     self.events.append(dict(event='RECOVERY_COMPLETE',phase=self.index,time=now));self.recovery=None;self.targets[phase['side']]=self.bind(phase,frame)
     self.started=now;self.progress_time=now;self.best=float('inf');self.stable=None
   else:r['stable']=None
   return output
  metric=error+.02*theta+physical_error
  if metric<self.best-.00008:self.best=metric;self.progress_time=now
  if now-self.started>phase['timeout'] or (not reached and now-self.progress_time>8.):self.begin_recovery(phase,now);return output
  if reached:
   if self.stable is None:self.stable=now
   if now-self.stable>=phase['dwell']:
    self.events.append(dict(event='NATIVE_FEEDBACK_PHASE_COMPLETE',phase=self.index,label=phase['label'],time=now,position_error_m=error,rotation_error_rad=theta))
    self.index+=1;self.started=None;self.done=self.index==len(self.phases)
  else:self.stable=None
  return output
