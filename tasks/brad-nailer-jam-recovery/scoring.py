"""Numeric physical-state scorer; no expert phases or commanded actions used.

Pre-bent fastener removal, actual two-arm pin capture, seated door and stable
past-center lever are the construct. A different intact physical strategy is
valid. Diagnostics and ideal tracking cannot establish native feasibility.
"""
from collections import deque
from dataclasses import dataclass,field
import math
import numpy as np
try:
 from .motion import rotate,conjugate,qangle
 from .kinematics import reconstruct
except ImportError:
 from motion import rotate,conjugate,qangle
 from kinematics import reconstruct

@dataclass
class Result:
 score:float=0.
 success:bool=False
 failure:str|None=None
 completed:list=field(default_factory=list)


class Scorer:
 def __init__(self,spec):
  self.spec=spec;self.defs={b['name']:b for a in spec['assemblies'] for b in a['bodies']};self.joints=[j for a in spec['assemblies'] for j in a['joints']];self.reset()
 def reset(self):self.started=False;self.previous_time=None;self.failed=None;self.window=deque();self.result=Result()
 def fail(self,reason):
  self.failed=reason;self.window.clear();self.result=Result(failure=reason);return self.result
 def local(self,root,point):return rotate(conjugate(root['quat']),np.asarray(point)-root['pos'])
 def nail_vertices(self,body):
  points=[]
  for shape in self.defs['bent_brad']['shapes']:
   if shape['kind']!='box':raise ValueError('Scoring geometry must explicitly support every brad collider')
   import itertools
   for corner in itertools.product(*[(-v/2,v/2) for v in shape['size']]):
    point=np.array(shape['pos'])+rotate(shape['quat'],corner);points.append(np.array(body['pos'])+rotate(body['quat'],point))
  return np.asarray(points)
 def captured(self,bodies):
  root=bodies['nose_body'];pin=bodies['bail_crosspin'];center=self.local(root,pin['pos'])
  axis=rotate(conjugate(root['quat']),rotate(pin['quat'],[0,0,1]));definition=self.defs['bail_crosspin']['shapes'][0]
  if abs(axis[2])<.98:return False
  for z in (-.012,.012):
   t=(z-center[2])/axis[2]
   if abs(t)>definition['height']/2-.001:return False
   point=center+t*axis;radius=definition['radius']
   # Actual rear abutment, lip underside and front retention depth. Merely
   # placing the pin center near the tool is insufficient.
   rear=point[0]-radius-.0935;underside=.0074-(point[1]+radius);depth=.098-(point[0]+radius)
   if not (-.0001<=rear<=.0006 and -.0001<=underside<=.0006 and depth>=.001):return False
  return True
 def past_center(self,bodies,joints):
  lever=bodies['latch_lever'];pivot=np.array(lever['pos']);ecc=np.array(bodies['draw_bail']['pos']);pin=np.array(bodies['bail_crosspin']['pos'])
  direction=ecc-pin;length=np.linalg.norm(direction)
  if length<1e-8:return False
  axis=rotate(lever['quat'],[0,0,1]);derivative=float(np.dot(direction/length,np.cross(axis,ecc-pivot)))
  # Negative length derivative means tensile draw force drives the lever
  # toward its closed upper stop. No arbitrary opening history is required.
  return bool(derivative<=-.0005 and joints['bail_extension']>=.0001 and -.06<=joints['lever_rotation']<=.01)
 def inside_tray(self,vertices,tray):
  local=np.array([self.local(tray,p) for p in vertices])
  return bool(np.all(np.abs(local[:,0])<=.0375) and np.all(np.abs(local[:,1])<=.0425)
              and local[:,2].min()>=.0018 and local[:,2].max()<=.019)
 def initial_valid(self,frame):
  for name,reference in self.defs.items():
   body=frame['bodies'][name]
   if np.linalg.norm(np.array(body['pos'])-reference['pos'])>.002 or qangle(body['quat'],reference['quat'])>.04:return False
  for joint in self.joints:
   tolerance=.0002 if joint['kind']=='prismatic' else .04
   if abs(frame['joints'][joint['name']]-joint['initial'])>tolerance:return False
  return True
 def integrity(self,frame):
  bodies=frame['bodies'];js=frame['joints']
  if set(bodies)!=set(self.defs):return 'Missing or substituted physical body'
  for body in bodies.values():
   values=[*body['pos'],*body['quat'],*body['linear'],*body['angular']]
   if not np.isfinite(values).all() or abs(np.linalg.norm(body['quat'])-1)>.005:return 'Nonfinite or malformed physical state'
  if not math.isfinite(frame['max_penetration']) or frame['max_penetration']>self.spec['penetration_limit']:return 'Solid interference exceeds integrity bound'
  for name in ('nose_body','parts_tray'):
   reference=self.defs[name];actual=bodies[name]
   if np.linalg.norm(np.array(actual['pos'])-reference['pos'])>.001 or qangle(actual['quat'],reference['quat'])>.01:return 'Fixed fixture moved'
  for joint in self.joints:
   value=js.get(joint['name']);tolerance=.00005 if joint['kind']=='prismatic' else .02
   if value is None or not math.isfinite(value) or not joint['lower']-tolerance<=value<=joint['upper']+tolerance:return 'Broken joint or exceeded mechanical stop'
  expected=reconstruct(self.spec,bodies['nose_body'],js)
  for name,pose in expected.items():
   actual=bodies[name]
   if np.linalg.norm(np.array(actual['pos'])-pose['pos'])>.0005 or qangle(actual['quat'],pose['quat'])>.02:return 'Disconnected or deformed mechanism'
  nail=bodies['bent_brad']['pos']
  if not (-.2<=nail[0]<=.9 and -.65<=nail[1]<=.65 and self.spec['table_top']-.01<=nail[2]<=1.3):return 'Fastener lost outside recoverable workspace'
  return None
 def witnesses(self,bodies):
  points=[]
  for name,local in [('nose_door',[.1,0,0]),('latch_lever',[-.045,.002,0]),('bail_crosspin',[0,0,-.012]),('bail_crosspin',[0,0,.012])]:
   b=bodies[name];points.append(np.array(b['pos'])+rotate(b['quat'],local))
  points.extend(self.nail_vertices(bodies['bent_brad']))
  return np.asarray(points)
 def update(self,frame):
  if self.failed:return self.result
  try:
   now=float(frame['time'])
   if not math.isfinite(now) or (self.previous_time is not None and now<=self.previous_time):return self.fail('Nonmonotonic physical observation')
   reason=self.integrity(frame)
   if reason:return self.fail(reason)
   if not self.started:
    if not self.initial_valid(frame):return self.fail('Wrong initial state; cannot substitute a completed setup')
    self.started=True
   if self.previous_time is not None and now-self.previous_time>1.5/self.spec['control_hz']:self.window.clear()
   self.previous_time=now;bodies=frame['bodies'];joints=frame['joints'];root=bodies['nose_body']
   vertices=self.nail_vertices(bodies['bent_brad']);local=np.array([self.local(root,p) for p in vertices])
   # All brad colliders must clear the actual trough/muzzle bounding region.
   box_lo=np.array([.005,-.006,-.014]);box_hi=np.array([.101,.011,.014])
   removed=bool(np.any(local.min(axis=0)>box_hi+.005) or np.any(local.max(axis=0)<box_lo-.005))
   in_tray=removed and self.inside_tray(vertices,bodies['parts_tray'])
   opened=joints['door_rotation']>=1.
   seated=abs(joints['door_rotation'])<=.005
   retained=seated and self.captured(bodies) and self.past_center(bodies,joints)
   goals=[]
   if opened:goals.append('nose_open')
   if removed:goals.append('fastener_clear')
   if in_tray:goals.append('fastener_in_tray')
   if retained and in_tray:goals.append('door_and_bail_secured')
   score=.25 if opened or removed else 0.
   if in_tray:score=.75 if retained else .5
   clearance=frame.get('robot_clearance');ready=in_tray and retained and clearance is not None and math.isfinite(clearance) and clearance>=.020
   if not ready:self.window.clear()
   else:
    self.window.append((now,self.witnesses(bodies)))
    while len(self.window)>1 and self.window[1][0]<=now-self.spec['hold_seconds']:self.window.popleft()
    samples=np.asarray([x[1] for x in self.window]);drift=float(np.linalg.norm(samples[:,None]-samples[None,:],axis=-1).max())
    if drift>.0005:
     self.window.clear();self.window.append((now,self.witnesses(bodies)))
    elif now-self.window[0][0]>=self.spec['hold_seconds']-1e-8:score=1.;goals.append('released_stable_hold')
   self.result=Result(score=score,success=score==1.,completed=goals);return self.result
  except (KeyError,TypeError,ValueError,IndexError) as exc:return self.fail('Malformed physical observation: '+str(exc))
