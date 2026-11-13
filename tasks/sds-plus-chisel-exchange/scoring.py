"""Numeric physical outcomes for chisel exchange; intact alternatives are valid."""
from collections import deque
from dataclasses import dataclass,field
import itertools,math
import numpy as np
try:
 from .motion import rotate,conjugate,qangle
 from .kinematics import reconstruct
 from .interfaces import retained,local
except ImportError:
 from motion import rotate,conjugate,qangle
 from kinematics import reconstruct
 from interfaces import retained,local

@dataclass
class Result:
 score:float=0.
 success:bool=False
 failure:str|None=None
 completed:list=field(default_factory=list)

class Scorer:
 def __init__(self,spec):
  self.spec=spec;self.defs={b['name']:b for a in spec['assemblies'] for b in a['bodies']};self.local_vertices={}
  for name in ('used_point_chisel','replacement_flat_chisel'):
   rows=[]
   for s in self.defs[name]['shapes']:
    if s['kind']=='convex':verts=s['vertices']
    elif s['kind']=='box':verts=list(itertools.product(*[(-v/2,v/2) for v in s['size']]))
    else:
     # Circumscribed32-sided cylinder bounds, disclosed conservative score envelope.
     r=s['radius']/math.cos(math.pi/32);verts=[[r*math.cos(a),r*math.sin(a),z] for a in np.arange(32)*2*math.pi/32 for z in (-s['height']/2,s['height']/2)]
    rows.extend([np.asarray(s['pos'])+rotate(s['quat'],v) for v in verts])
   self.local_vertices[name]=np.unique(np.round(rows,12),axis=0)
  self.reset()
 def reset(self):self.started=False;self.previous_time=None;self.failed=None;self.window=deque();self.result=Result()
 def fail(self,message):self.failed=message;self.window.clear();self.result=Result(failure=message);return self.result
 def vertices(self,name,b):
  rotation=np.column_stack([rotate(b['quat'],v) for v in np.eye(3)]);return self.local_vertices[name]@rotation.T+b['pos']
 def initial_valid(self,frame):
  return all(np.linalg.norm(np.asarray(frame['bodies'][n]['pos'])-b['pos'])<=.002 and qangle(frame['bodies'][n]['quat'],b['quat'])<=.05 for n,b in self.defs.items()) and abs(frame['joints']['sleeve_retraction'])<=.0005
 def integrity(self,f):
  bs=f['bodies'];js=f['joints']
  if set(bs)!=set(self.defs):return 'Missing or substituted physical body'
  for b in bs.values():
   if not np.isfinite([*b['pos'],*b['quat'],*b['linear'],*b['angular']]).all() or abs(np.linalg.norm(b['quat'])-1)>.005:return 'Malformed or nonfinite physical body'
  if not math.isfinite(f['max_penetration']) or f['max_penetration']>self.spec['penetration_limit']:return 'Solid interference exceeds integrity bound'
  for name,b in self.defs.items():
   if b.get('anchor') and (np.linalg.norm(np.asarray(bs[name]['pos'])-b['pos'])>.001 or qangle(bs[name]['quat'],b['quat'])>.01):return 'Fixed fixture moved'
  q=js.get('sleeve_retraction')
  if q is None or not math.isfinite(q) or not -.00005<=q<=.00805:return 'Broken sleeve or exceeded stop'
  expected=reconstruct(self.spec,bs['tool_holder'],js)['locking_sleeve'];actual=bs['locking_sleeve']
  if np.linalg.norm(np.asarray(actual['pos'])-expected['pos'])>.0005 or qangle(actual['quat'],expected['quat'])>.02:return 'Disconnected release sleeve'
  ball=local(bs['tool_holder'],bs['locking_ball']['pos']);x=self.spec['parameters']['ball_port_x']
  if not self.spec['parameters']['authored_ball_race_x_min']<=ball[0]<=self.spec['parameters']['authored_ball_race_x_max'] or abs(ball[1])>.0006 or not .0072<=ball[2]<=.0100:return 'Retaining ball escaped cage'
  for n in ('used_point_chisel','replacement_flat_chisel'):
   p=bs[n]['pos']
   if not -.1<=p[0]<=.9 or not -.65<=p[1]<=.65 or not self.spec['table_top']-.01<=p[2]<=1.4:return 'Chisel lost outside recoverable workspace'
  return None
 def witnesses(self,bs):
  rows=[]
  for n in ('used_point_chisel','replacement_flat_chisel'):
   for v in ([0,0,0],[-.2,0,0],[-.19,.01,0],[-.19,0,.01]):rows.append(np.asarray(bs[n]['pos'])+rotate(bs[n]['quat'],v))
  rows.extend([bs['locking_ball']['pos'],bs['locking_sleeve']['pos']]);return np.asarray(rows)
 def update(self,f):
  if self.failed:return self.result
  try:
   t=float(f['time'])
   if not math.isfinite(t) or self.previous_time is not None and t<=self.previous_time:return self.fail('Nonmonotonic physical observation')
   error=self.integrity(f)
   if error:return self.fail(error)
   if not self.started:
    if not self.initial_valid(f):return self.fail('Wrong initial state; completed setup cannot substitute')
    self.started=True
   if self.previous_time is not None and t-self.previous_time>1.5/self.spec['control_hz']:self.window.clear()
   self.previous_time=t;bs=f['bodies'];js=f['joints'];v=self.vertices('used_point_chisel',bs['used_point_chisel']);h=bs['tool_holder'];R=np.column_stack([rotate(conjugate(h['quat']),a) for a in np.eye(3)]);in_h=(v-h['pos'])@R.T;lo=np.array([-.002,-.012,-.012]);hi=np.array([.055,.012,.012]);removed=bool(np.any(in_h.min(axis=0)>hi+.005) or np.any(in_h.max(axis=0)<lo-.005))
   tray=bs['used_chisel_tray'];R=np.column_stack([rotate(conjugate(tray['quat']),a) for a in np.eye(3)]);inside=(v-tray['pos'])@R.T
   stored=bool(removed and np.all(np.abs(inside[:,0])<=.1155) and np.all(np.abs(inside[:,1])<=.0355) and inside[:,2].min()>=.0017 and inside[:,2].max()<=.021)
   captured=retained(self.spec,bs,js);goals=[];score=0.
   if removed:goals.append('used_chisel_clear');score=.25
   if stored:goals.append('used_chisel_stored');score=.5
   if stored and captured:goals.append('replacement_retained');score=.75
   gap=f.get('robot_clearance');ready=stored and captured and gap is not None and math.isfinite(gap) and gap>=.020
   if not ready:self.window.clear()
   else:
    self.window.append((t,self.witnesses(bs)))
    while len(self.window)>1 and self.window[1][0]<=t-self.spec['hold_seconds']:self.window.popleft()
    w=np.array([r[1] for r in self.window]);drift=np.linalg.norm(w[:,None]-w[None,:],axis=-1).max()
    if drift>.0005:self.window.clear();self.window.append((t,self.witnesses(bs)))
    elif t-self.window[0][0]>=self.spec['hold_seconds']-1e-8:score=1.;goals.append('released_stable_hold')
   self.result=Result(score=score,success=score==1.,completed=goals);return self.result
  except (KeyError,ValueError,TypeError,IndexError) as e:return self.fail('Malformed physical observation: '+str(e))
