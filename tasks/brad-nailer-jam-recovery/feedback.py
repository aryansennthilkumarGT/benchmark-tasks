"""Original nailer expert, native feedback, 14 robot actions.

No pose setters, attachments, task-joint commands, score access or virtual latch.
Circular motions retain the acquired TCP/body transform. Coupled motions solve
both FK targets before emitting a command and halve the physical arc increment
when either arm cannot meet its limit/rate. No Cartesian hinge chord shortcuts.
"""
import copy,math,hashlib,json
import numpy as np
try:
 from .motion import Motion,ControlFailure,rotate,multiply,conjugate,axis_quat,qangle
 from .interfaces import pin_captured
except ImportError:
 from motion import Motion,ControlFailure,rotate,multiply,conjugate,axis_quat,qangle
 from interfaces import pin_captured


class Controller:
 def __init__(self,plan,spec):
  identity=hashlib.sha256(json.dumps(spec,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()
  if plan.get('scene_content_sha256')!=identity:raise ControlFailure('Controller plan belongs to a different scene; regenerate it after physical edits')
  self.phases=plan['phases'];self.spec=spec;self.reset()
 def reset(self):
  self.index=0;self.done=False;self.failed=None;self.events=[];self.last_time=None;self.actions=0
  self.motion={s:Motion(s) for s in ('left','right')};self.targets={};self.context={}
  self.started=None;self.stable=None;self.progress_time=None;self.best=float('inf');self.attempts={};self.recovery=None
 def fail(self,reason):
  self.failed=reason;self.events.append(dict(event='FAIL_STOP',phase=self.index,time=self.last_time,reason=reason));raise ControlFailure(reason)
 def tcp(self,side,q):
  i=0 if side=='left' else 7;m=self.motion[side];p,r=m.ik.tcp_pose(q[i:i+6],m.base);return dict(pos=p,quat=m.ik.matrix_to_quat_xyzw(r))
 def relative(self,a,b):return dict(pos=rotate(conjugate(a['quat']),np.asarray(b['pos'])-a['pos']),quat=multiply(conjugate(a['quat']),b['quat']))
 def compose(self,a,b):return dict(pos=np.asarray(a['pos'])+rotate(a['quat'],b['pos']),quat=multiply(a['quat'],b['quat']))
 def bind(self,p,frame,q):
  out=copy.deepcopy(p);current=self.tcp(p['side'],q)
  if p.get('release_current'):out['target']={k:list(v) for k,v in current.items()}
  elif 'withdraw_current' in p:
   out['target']=dict(pos=(current['pos']+rotate(current['quat'],[0,0,-p['withdraw_current']])).tolist(),quat=current['quat'].tolist())
  elif 'reference_body' in p:
   b=frame['bodies'][p['reference_body']];out['target']=dict(pos=(np.asarray(b['pos'])+rotate(b['quat'],p['reference_offset'])).tolist(),quat=multiply(b['quat'],p['reference_quat']).tolist())
  if 'arc' in p:
   joint=next(j for a in self.spec['assemblies'] for j in a['joints'] if j['name']==p['arc']['joint'])
   grasp_body='bail_crosspin' if p.get('pin_drive') else joint['child']
   self.context=dict(joint=joint,grasp=self.relative(frame['bodies'][grasp_body],current),arc_reference=float(frame['joints'][joint['name']]))
   if p.get('coupled')=='rigid':self.context['pair']=self.relative(current,self.tcp(p['follower'],q))
   if p.get('coupled')=='hook':self.context['pin_grasp']=self.relative(frame['bodies']['bail_crosspin'],self.tcp(p['follower'],q))
  return out
 def arc_pose(self,p,frame,angle):
  j=self.context['joint'];parent=frame['bodies'][j['parent']];axis={'X':[1,0,0],'Y':[0,1,0],'Z':[0,0,1]}[j['axis']]
  quat=multiply(parent['quat'],axis_quat(axis,angle));pos=np.asarray(parent['pos'])+rotate(parent['quat'],j['pivot_parent'])-rotate(quat,j['pivot_child'])
  child=dict(pos=pos,quat=quat)
  if p.get('pin_drive'):
   # Actuate the free lever through the held physical pin/bail, not a lever
   # joint command. All task state remains read-only.
   pin=self.hook_pose(child,frame)
   return self.compose(pin,self.context['grasp']),child
  return self.compose(child,self.context['grasp']),child
 def arc_goal(self,p,frame):
  if p.get('bail_goal'):
   root=frame['bodies']['nose_body'];E=frame['bodies']['draw_bail']['pos'];local=rotate(conjugate(root['quat']),np.asarray(E)-root['pos'])
   beta=.30 if p['bail_goal']=='outboard' else math.asin((self.spec['parameters']['closed_pin_local'][1]-local[1])/self.spec['parameters']['draw_rest'])
   return beta-frame['joints']['lever_rotation']-frame['joints']['door_rotation']
  return p['arc']['angle']
 def hook_pose(self,lever,frame):
  root=frame['bodies']['nose_body'];params=self.spec['parameters'];rest=params['draw_rest'];nominal=params['closed_pin_local']
  j=next(j for a in self.spec['assemblies'] for j in a['joints'] if j['name']=='bail_rotation')
  E=np.asarray(lever['pos'])+rotate(lever['quat'],j['pivot_parent']);local=rotate(conjugate(root['quat']),E-np.asarray(root['pos']));dy=nominal[1]-local[1]
  if abs(dy)>=rest:raise ControlFailure('Hook mouth lies outside draw-bail reach')
  point=np.array([max(nominal[0],local[0]+math.sqrt(rest*rest-dy*dy)),nominal[1],0.])
  beta=math.atan2(dy,point[0]-local[0]);return dict(pos=np.asarray(root['pos'])+rotate(root['quat'],point),quat=multiply(root['quat'],axis_quat([0,0,1],beta)))
 def hook_target(self,lever,frame):
  root=frame['bodies']['nose_body'];params=self.spec['parameters'];rest=params['draw_rest'];nominal=params['closed_pin_local']
  j=next(j for a in self.spec['assemblies'] for j in a['joints'] if j['name']=='bail_rotation')
  E=np.asarray(lever['pos'])+rotate(lever['quat'],j['pivot_parent']);local=rotate(conjugate(root['quat']),E-np.asarray(root['pos']));dy=nominal[1]-local[1]
  if abs(dy)>=rest:raise ControlFailure('Hook mouth lies outside draw-bail reach')
  point=np.array([max(nominal[0],local[0]+math.sqrt(rest*rest-dy*dy)),nominal[1],0.])
  beta=math.atan2(dy,point[0]-local[0]);pin=dict(pos=np.asarray(root['pos'])+rotate(root['quat'],point),quat=multiply(root['quat'],axis_quat([0,0,1],beta)))
  return self.compose(pin,self.context['pin_grasp'])
 def solve(self,side,q,target):
  start=0 if side=='left' else 7;m=self.motion[side]
  solved,pe,re=m.ik.solve(target['pos'],target['quat'],q_init=q[start:start+6],base_pos=m.base,iters=200,damping=.015,tol=1e-5)
  valid=pe<.00003 and re<.0001 and np.all(solved>m.ik.LOWER+1e-5) and np.all(solved<m.ik.UPPER-1e-5) and np.max(np.abs(solved-(m.reference if m.reference is not None else q[start:start+6])))<=.020001
  return solved,bool(valid)
 def arc_action(self,p,frame,q,output):
  side=p['side'];i=0 if side=='left' else 7;j=self.context['joint'];current=frame['joints'][j['name']];goal=self.arc_goal(p,frame)
  final,_=self.arc_pose(p,frame,goal);tcp=self.tcp(side,q);error=float(np.linalg.norm(tcp['pos']-final['pos']));theta=qangle(tcp['quat'],final['quat'])
  arms=[side]+([p['follower']] if p.get('coupled') else [])
  for arm in arms:
   start=0 if arm=='left' else 7;m=self.motion[arm]
   if m.reference is not None and np.max(np.abs(m.reference-q[start:start+6]))>m.tracking_error_limit:
    for hold in arms:
     off=0 if hold=='left' else 7;ref=self.motion[hold].reference
     if ref is not None:output[off:off+6]=ref
    return output,error,theta
  # Advance the commanded circular reference at0.5rad/s, rather than
  # perpetually commanding25mrad ahead of the measured loaded joint. The
  # latter becomes an artificially slow proportional velocity controller.
  reference=float(self.context.get('arc_reference',current))
  proposed=reference+float(np.clip(goal-reference,-.025,.025))
  proposed=float(np.clip(proposed,current-.12,current+.12))
  delta=proposed-reference
  for _ in range(14):
   target,child=self.arc_pose(p,frame,reference+delta);leader,ok=self.solve(side,q,target);follower=None
   if ok and p.get('coupled'):
    follow=self.compose(target,self.context['pair']) if p['coupled']=='rigid' else self.hook_target(child,frame)
    follower,ok=self.solve(p['follower'],q,follow)
   if ok:
    # Holding a valid reference while an actual actuator catches up is
    # allowed; the existing physical-progress/timeout guards detect stalls.
    self.context['arc_reference']=reference+delta
    output[i:i+6]=leader;self.motion[side].reference=leader.copy()
    if follower is not None:
     off=0 if p['follower']=='left' else 7;output[off:off+6]=follower;self.motion[p['follower']].reference=follower.copy()
    output[i+6]=q[i+6]+float(np.clip(p['opening']-q[i+6],-.05,.05))
    return output,error,theta
   delta*=.5
  raise ControlFailure('Physical arc or coupled follower cannot meet IK/rate/limit constraints')
 def physical(self,p,frame):
  checks=p.get('joint_checks',[])+p.get('joint_checks_final',[])
  metric=0.
  for c in checks:
   value=frame['joints'][c['name']];metric+=max(0.,c['min']-value,value-c['max'])
  if 'arc' in p:metric+=max(0.,abs(frame['joints'][p['arc']['joint']]-self.arc_goal(p,frame))-.015)*.02
  if p.get('pin_capture') and not pin_captured(self.spec,frame['bodies']):metric+=.001
  return metric<1e-9,metric
 def start_recovery(self,p,now,q):
  if not p['label'].startswith(('Grip','Regrasp')):self.fail('Motion/physical-feedback stall: '+p['label'])
  off=0 if p['side']=='left' else 7;width=p.get('grasp_width',0.)
  if q[off+6]>width/.0939+.04:self.fail('Unexpected wide obstruction; stop before reacquiring')
  attempt=self.attempts.get(self.index,0)+1
  if attempt>2:self.fail('Grip recovery attempts exhausted')
  self.attempts[self.index]=attempt
  retry=copy.deepcopy(self.targets[p['side']]);retry.pop('arc',None);retry['opening']=(width+.002)/.0939;retry['grasp_width']=0.;retry['dwell']=.2
  retry['target']['pos']=(np.asarray(retry['target']['pos'])+rotate(retry['target']['quat'],[0,0,-.006])).tolist()
  self.recovery=dict(target=retry,started=now,stable=None);self.events.append(dict(event='OPEN_BACKOFF_REACQUIRE',phase=self.index,attempt=attempt,time=now))
 def step(self,joints,frame):
  q=np.asarray(joints,dtype=float);now=float(frame['time'])
  if q.shape!=(14,) or not np.isfinite(q).all() or not math.isfinite(now):raise ControlFailure('Invalid robot observation')
  if self.failed:raise ControlFailure(self.failed)
  if self.last_time is not None and now<=self.last_time:self.fail('Stale/nonmonotonic native observation')
  if 'bodies' not in frame or 'joints' not in frame:self.fail('Native feedback missing')
  self.last_time=now;self.actions+=1
  if self.actions>self.spec['run_limit']:self.fail('Expert action limit exhausted')
  if self.done:return q.copy()
  p=self.phases[self.index]
  if self.started is None:
   self.targets[p['side']]=self.bind(p,frame,q);self.started=now;self.progress_time=now;self.best=float('inf');self.stable=None
   self.events.append(dict(event='PHASE_START',phase=self.index,label=p['label'],time=now))
  active=self.recovery['target'] if self.recovery else self.targets[p['side']];output=q.copy();error=theta=0.
  try:
   for side,target in self.targets.items():
    if side==p['side']:target=active
    start=0 if side=='left' else 7
    if active.get('coupled') and side==active['follower']:
     # The coupled solve owns this arm's reference for the entire phase.
     # Tracking an earlier world hold here would overwrite it every tick.
     output[start+6]=q[start+6]+float(np.clip(target['opening']-q[start+6],-.05,.05))
     continue
    if 'arc' in target:continue
    action,pe,re=self.motion[side].target(q[start:start+7],target['target']['pos'],target['target']['quat'],target['opening'],speed=target['speed'],angular_speed=.6)
    output[start:start+7]=action
    if side==p['side']:error,theta=pe,re
   if 'arc' in active:output,error,theta=self.arc_action(active,frame,q,output)
  except (ControlFailure,KeyError,ValueError) as exc:self.fail(str(exc))
  off=0 if p['side']=='left' else 7;width=active.get('grasp_width',0.)/.0939
  gripped=(max(active['opening']+.005,width-.02)<q[off+6]<width+.03) if width else abs(q[off+6]-active['opening'])<.03
  physical,pm=self.physical(active,frame);reached=error<active['position_tolerance'] and theta<active['angle_tolerance'] and gripped and physical
  if self.recovery:
   r=self.recovery
   if now-r['started']>12:self.fail('Recovery timeout')
   if reached:
    if r['stable'] is None:r['stable']=now
    if now-r['stable']>=active['dwell']:
     self.recovery=None;self.targets[p['side']]=self.bind(p,frame,q);self.started=now;self.progress_time=now;self.best=float('inf')
   else:r['stable']=None
   return output
  metric=error+.02*theta+pm
  if metric<self.best-.00008:self.best=metric;self.progress_time=now
  if now-self.started>p['timeout'] or (not reached and now-self.progress_time>8):self.start_recovery(p,now,q);return output
  if reached:
   if self.stable is None:self.stable=now
   if now-self.stable>=p['dwell']:
    # Freeze completed references at measured FK, including coupled followers.
    for side in ([p['side'],p['follower']] if p.get('coupled') else [p['side']]):
     held=self.targets[side];held=copy.deepcopy(held);held.pop('arc',None);pose=self.tcp(side,q);held['target']={k:list(v) for k,v in pose.items()};self.targets[side]=held
    self.events.append(dict(event='NATIVE_FEEDBACK_PHASE_COMPLETE',phase=self.index,label=p['label'],time=now,position_error_m=error,rotation_error_rad=theta))
    self.index+=1;self.started=None;self.done=self.index==len(self.phases)
  else:self.stable=None
  return output
