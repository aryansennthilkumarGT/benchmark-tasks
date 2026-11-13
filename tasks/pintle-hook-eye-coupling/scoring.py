"""Observable outcome score; no required expert trajectory, task-phase or force fiction."""
from dataclasses import dataclass,field
from collections import deque
import math
import numpy as np
try:
 from .motion import rotate,qangle
 from .kinematics import reconstruct
 from .interfaces import seated,latched
except ImportError:
 from motion import rotate,qangle
 from kinematics import reconstruct
 from interfaces import seated,latched
@dataclass
class Result:
 score:float=0.
 success:bool=False
 failure:str|None=None
 completed:list=field(default_factory=list)
class Scorer:
 def __init__(self,spec):
  self.spec=spec;self.defs={b['name']:b for a in spec['assemblies'] for b in a['bodies']};self.links={j['name']:j for a in spec['assemblies'] for j in a['joints']};self.reset()
 def reset(self):self.previous_time=None;self.failed=None;self.window=deque();self.result=Result()
 def fail(self,message):self.failed=message;self.window.clear();self.result=Result(failure=message);return self.result
 def integrity(self,f):
  bs=f['bodies'];js=f['joints']
  if set(bs)!=set(self.defs) or set(js)!=set(self.links):return 'Missing or substituted physical body or joint'
  for b in bs.values():
   if len(b['pos'])!=3 or len(b['quat'])!=4 or len(b['linear'])!=3 or len(b['angular'])!=3 or not np.isfinite([*b['pos'],*b['quat'],*b['linear'],*b['angular']]).all() or abs(np.linalg.norm(b['quat'])-1)>.005:return 'Malformed or nonfinite body'
  if not math.isfinite(f['max_penetration']) or not 0.<=f['max_penetration']<=self.spec['penetration_limit']:return 'Solid interference exceeds integrity bound'
  for n,b in self.defs.items():
   if b.get('anchor') and (np.linalg.norm(np.asarray(bs[n]['pos'])-b['pos'])>.001 or qangle(bs[n]['quat'],b['quat'])>.01):return 'Fixed fixture moved'
  for n,j in self.links.items():
   v=js[n]
   if not isinstance(v,(int,float)) or not math.isfinite(v) or not j['lower']-.001<=v<=j['upper']+.001:return 'Broken joint or exceeded stop'
  poses=reconstruct(self.spec,bs['hook_body'],js)
  for n in ('upper_latch','lock_handle'):
   if np.linalg.norm(np.asarray(bs[n]['pos'])-poses[n]['pos'])>.0005 or qangle(bs[n]['quat'],poses[n]['quat'])>.015:return 'Disconnected latch assembly'
  p=bs['drawbar_eye']['pos']
  if not -.1<=p[0]<=.9 or not -.65<=p[1]<=.65 or not self.spec['table_top']-.015<=p[2]<=1.4:return 'Eye lost outside recoverable workspace'
  return None
 def witnesses(self,bs):
  result=[]
  for n,points in [('drawbar_eye',[[0,0,0],[.12,0,0],[0,.06,0]]),('upper_latch',[[0,0,0],[.10,0,0]]),('lock_handle',[[0,0,0],[.04,0,0]])]:
   b=bs[n]
   for v in points:result.append(np.asarray(b['pos'])+rotate(b['quat'],v))
  return np.asarray(result)
 def update(self,f):
  if self.failed:return self.result
  try:
   t=float(f['time'])
   if not math.isfinite(t) or self.previous_time is not None and t<=self.previous_time:return self.fail('Nonmonotonic physical observation')
   invalid=self.integrity(f)
   if invalid:return self.fail(invalid)
   bs=f['bodies'];js=f['joints']
   if self.previous_time is None:
    if any(np.linalg.norm(np.asarray(bs[n]['pos'])-b['pos'])>.002 or qangle(bs[n]['quat'],b['quat'])>.03 for n,b in self.defs.items()) or any(abs(js[n]-v)>.01 for n,v in self.spec['initial_joint_values'].items()):return self.fail('Wrong initial state; completed setup substituted')
   elif t-self.previous_time>1.5/self.spec['control_hz']:self.window.clear()
   self.previous_time=t;score=0.;completed=[];placed=seated(self.spec,bs)
   if placed:score=.25;completed.append('eye_seated')
   if placed and abs(js['latch_rotation'])<=.025:score=.5;completed.append('upper_latch_closed')
   closed=latched(self.spec,bs,js)
   if closed:score=.75;completed.append('lock_handle_flush')
   gap=f.get('robot_clearance');ready=closed and gap is not None and math.isfinite(gap) and gap>=.02
   if not ready:self.window.clear()
   else:
    self.window.append((t,self.witnesses(bs)))
    while len(self.window)>1 and self.window[1][0]<=t-self.spec['hold_seconds']:self.window.popleft()
    w=np.array([v[1] for v in self.window]);drift=np.linalg.norm(w[:,None]-w[None,:],axis=-1).max()
    if drift>.0005:self.window.clear();self.window.append((t,self.witnesses(bs)))
    elif t-self.window[0][0]>=self.spec['hold_seconds']-1e-8:score=1.;completed.append('released_stable_capture')
   self.result=Result(score=score,success=score==1.,completed=completed);return self.result
  except (KeyError,ValueError,TypeError,IndexError) as e:return self.fail('Malformed physical observation: '+str(e))
