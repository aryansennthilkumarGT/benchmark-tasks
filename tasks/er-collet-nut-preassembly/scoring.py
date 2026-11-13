"""Observable eccentric-groove engagement and supported upright preassembly."""
import copy,math
from dataclasses import dataclass
try:
 from .motion import rotate
except ImportError:
 from motion import rotate


def finite(v,n):return isinstance(v,(list,tuple)) and len(v)==n and all(isinstance(x,(int,float)) and not isinstance(x,bool) and math.isfinite(x) for x in v)

@dataclass(frozen=True)
class Result:
 score:float
 success:bool
 failure:str|None
 completed:tuple

class Scorer:
 def __init__(self,scene):self.spec=scene['score_spec'];self.reset()
 def reset(self):
  self.failed=None;self.previous=None;self.time=None;self.hooked=False;self.stable=None;self.result=Result(0.,False,None,())
 def fail(self,why):
  self.failed=self.failed or why;self.result=Result(0.,False,self.failed,());return self.result
 def update(self,f):
  s=self.spec
  if not isinstance(f,dict) or f.get('schema')!=1:return self.fail('frame_schema')
  if not finite([f.get('time')],1) or f['time']<0:return self.fail('time')
  bodies=f.get('bodies')
  if not isinstance(bodies,dict) or set(bodies)!={'bench_nut','collet','collet_cradle'}:return self.fail('body_set')
  for b in bodies.values():
   if not isinstance(b,dict):return self.fail('body_state')
   for k,n in [('pos',3),('quat',4),('linear',3),('angular',3)]:
    if not finite(b.get(k),n):return self.fail('nonfinite_state')
   if abs(sum(x*x for x in b['quat'])-1)>1e-5:return self.fail('quaternion_norm')
  if f.get('joints')!={}:return self.fail('unexpected_joint')
  if not finite([f.get('max_penetration'),f.get('robot_clearance')],2):return self.fail('contact_telemetry')
  if not 0<=f['max_penetration']<=s['penetration_limit']:return self.fail('penetration')
  t=f['time']
  if self.time is not None and t<=self.time:
   if t==self.time and f==self.previous:return self.result
   return self.fail('time_order')
  if self.time is not None and t-self.time>1.5/s['control_hz']:self.stable=None
  if self.time is None:
   if math.dist(bodies['collet']['pos'],s['initial_collet'])>.003:return self.fail('initial_layout')
  else:
   distance=math.dist(bodies['collet']['pos'],self.previous['bodies']['collet']['pos'])
   if distance>2.*(t-self.time)+.010:return self.fail('unobserved_state_jump')
  self.time=t;self.previous=copy.deepcopy(f)
  if self.failed:return self.fail(self.failed)
  for n,a in s['anchors'].items():
   dot=abs(sum(x*y for x,y in zip(a['quat'],bodies[n]['quat'])))
   if math.dist(a['pos'],bodies[n]['pos'])>s['fixture_tolerance'] or dot<math.cos(s['angle_tolerance']/2):return self.fail('fixture_moved:'+n)
  b=bodies['collet'];p=b['pos'];axis=rotate(b['quat'],[0,0,1]);target=s['target']
  if p[2]<s['loss_plane']:return self.fail('collet_lost')
  # Partial credit describes current geometric hook engagement over a range
  # of valid entry angles. Final seating never requires an exact expert path.
  pivot=s['hook_pivot'];point=rotate(b['quat'],pivot)+p
  hook=math.dist(point,[target[0]+pivot[0],target[1],target[2]])<=.0012 and .05<=math.acos(max(-1.,min(1.,axis[2])))<=.45
  self.hooked=bool(hook)
  seated=math.dist(p[:2],target[:2])<=s['lateral_tolerance'] and abs(p[2]-target[2])<=s['axial_tolerance'] and axis[2]>=math.cos(s['angle_tolerance'])
  still=all(math.sqrt(sum(x*x for x in b['linear']))<=s['speed_limit'] and math.sqrt(sum(x*x for x in b['angular']))<=s['spin_limit'] for b in bodies.values())
  ready=seated and still and f['robot_clearance']>=s['release_clearance']
  if ready:
   if self.stable is None:self.stable=t
  else:self.stable=None
  success=self.stable is not None and t-self.stable+1e-9>=s['hold_seconds']
  goals=tuple(n for n,ok in [('groove_hooked',hook or seated),('supported_preassembly',seated)] if ok)
  score=.75 if seated else (.25 if hook else 0.)
  self.result=Result(1. if success else score,success,None,goals);return self.result
