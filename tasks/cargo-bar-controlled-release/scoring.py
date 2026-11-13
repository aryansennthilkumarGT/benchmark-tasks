"""Current physical unloading, wall clearance and supported release, independent of path.

No stroke counter advances the rack or creates force. Exact source/model contact
and actual joint/body telemetry determine outcomes. CPU synthetic frames are not
robot demonstrations. Clamp stiffness is an authored fixture parameter.
"""
import copy,itertools,math
from dataclasses import dataclass
try:
 from .motion import rotate,qangle
 from .kinematics import reconstruct
except ImportError:
 from motion import rotate,qangle
 from kinematics import reconstruct


def finite(v,n):return isinstance(v,(list,tuple)) and len(v)==n and all(isinstance(x,(int,float)) and not isinstance(x,bool) and math.isfinite(x) for x in v)

@dataclass(frozen=True)
class Result:
 score:float
 success:bool
 failure:str|None
 completed:tuple

class Scorer:
 def __init__(self,spec):
  self.spec=spec;self.bodies={b['name']:b for a in spec['assemblies'] for b in a['bodies']}
  self.joints={j['name']:j for a in spec['assemblies'] for j in a['joints']};self.reset()
 def reset(self):
  self.failed=None;self.previous=None;self.stable=None;self.time=None;self.result=Result(0.,False,None,())
 def fail(self,reason):
  self.failed=self.failed or reason;self.result=Result(0.,False,self.failed,());return self.result
 def update(self,f):
  if not isinstance(f,dict) or f.get('schema')!=1:return self.fail('frame_schema')
  if not finite([f.get('time')],1) or f['time']<0:return self.fail('time')
  bs=f.get('bodies');js=f.get('joints')
  if not isinstance(bs,dict) or set(bs)!=set(self.bodies):return self.fail('body_set')
  if not isinstance(js,dict) or set(js)!=set(self.joints) or not finite(list(js.values()),len(js)):return self.fail('joint_set')
  for b in bs.values():
   if not isinstance(b,dict):return self.fail('body_state')
   for k,n in [('pos',3),('quat',4),('linear',3),('angular',3)]:
    if not finite(b.get(k),n):return self.fail('invalid_'+k)
   if abs(sum(v*v for v in b['quat'])-1)>1e-5:return self.fail('quaternion_norm')
  if not finite([f.get('max_penetration'),f.get('robot_clearance')],2):return self.fail('contact_telemetry')
  if not 0<=f['max_penetration']<=self.spec['penetration_limit']:return self.fail('interpenetration')
  t=f['time']
  if self.time is not None and t<=self.time:
   if t==self.time and f==self.previous:return self.result
   return self.fail('time_order')
  if self.time is None:
   if any(math.dist(bs[n]['pos'],b['pos'])>.003 or qangle(bs[n]['quat'],b['quat'])>.04 for n,b in self.bodies.items()):return self.fail('initial_layout')
   if any(abs(v-self.joints[n].get('initial',0.))>(.03 if self.joints[n]['kind']=='revolute' else .0005) for n,v in js.items()):return self.fail('initial_joint_layout')
  else:
   dt=t-self.time
   if dt>1.5/self.spec['control_hz']:self.stable=None
   for n,b in bs.items():
    if math.dist(b['pos'],self.previous['bodies'][n]['pos'])>2.*dt+.010:return self.fail('state_replacement:'+n)
  self.time=t;self.previous=copy.deepcopy(f)
  if self.failed:return self.fail(self.failed)
  anchor=self.bodies['wall_frame'];actual=bs['wall_frame']
  if math.dist(anchor['pos'],actual['pos'])>.001 or qangle(anchor['quat'],actual['quat'])>.025:return self.fail('frame_moved')
  for n,j in self.joints.items():
   margin=.03 if j['kind']=='revolute' else .00025
   if not j['lower']-margin<=js[n]<=j['upper']+margin:return self.fail('joint_limit:'+n)
  expected=reconstruct(self.spec,bs['outer_tube'],js)
  for n,p in expected.items():
   if math.dist(bs[n]['pos'],p['pos'])>.0006 or qangle(bs[n]['quat'],p['quat'])>.025:return self.fail('broken_joint:'+n)
  for n,b in bs.items():
   definition=self.bodies[n]
   bottom=min((rotate(b['quat'],corner)+b['pos'])[2] for corner in itertools.product(*zip(definition['bounds_min'],definition['bounds_max'])))
   if bottom<self.spec['table_top']-.020:return self.fail('lost_part:'+n)
  # Rack and pinion coupling is a physical integrity condition, not a required
  # number of handle strokes or an expert-specific event sequence.
  if abs(js['telescope']+self.spec['parameters']['authored_pinion_pitch_radius']*js['pinion_rotation'])>.0005:return self.fail('rack_pinion_skipped')
  gaps=[];faces_fit=[]
  for n,sign in [('left_pad',-1),('right_pad',1)]:
   b=bs[n];axis=rotate(b['quat'],[0,1,0]);outer=[b['pos'][i]+sign*.006*axis[i] for i in range(3)]
   face=sign*self.spec['parameters']['wall_span']/2
   gaps.append(sign*(face-outer[1]))
   faces_fit.append(axis[1]>=math.cos(.05))
  unloaded=abs(js['left_compliance'])<=.0005 and abs(js['right_compliance'])<=.0005 and js['telescope']<=self.spec['parameters']['authored_initial_extension']-.002
  clear=unloaded and js['telescope']<=.006 and min(gaps)>=.0045 and all(faces_fit)
  target=self.spec['parameters']['authored_cradle_root']
  resting=clear and math.dist(bs['outer_tube']['pos'],target)<=.002 and js['trigger_pull']<=.001
  still=all(math.sqrt(sum(x*x for x in b['linear']))<=.008 and math.sqrt(sum(x*x for x in b['angular']))<=.15 for b in bs.values())
  ready=resting and still and f['robot_clearance']>=.020
  if ready:
   if self.stable is None:self.stable=t
  else:self.stable=None
  success=self.stable is not None and t-self.stable+1e-9>=self.spec['hold_seconds']
  score=.75 if resting else .5 if clear else .25 if unloaded else 0.
  goals=tuple(n for n,ok in [('preload_released',unloaded),('both_feet_clear',clear),('bar_supported',resting)] if ok)
  self.result=Result(1. if success else score,success,None,goals);return self.result
