"""Observable mechanical interfaces, shared by expert feedback and scorer.

No reward, expert phase, desired action or task-state mutation is exposed.
"""
import numpy as np
try:
 from .motion import rotate,conjugate
except ImportError:
 from motion import rotate,conjugate


def pin_captured(spec,bodies):
 root=bodies['nose_body'];pin=bodies['bail_crosspin'];center=rotate(conjugate(root['quat']),np.asarray(pin['pos'])-root['pos'])
 axis=rotate(conjugate(root['quat']),rotate(pin['quat'],[0,0,1]));definition=next(b for a in spec['assemblies'] for b in a['bodies'] if b['name']=='bail_crosspin')['shapes'][0]
 if abs(axis[2])<.98:return False
 arms=spec['parameters']['hook_arms']
 for z in arms['z_planes']:
  t=(z-center[2])/axis[2]
  if abs(t)>definition['height']/2-.001:return False
  point=center+t*axis;radius=definition['radius'];rear=point[0]-radius-arms['rear_inner_x'];underside=arms['lip_under_y']-(point[1]+radius);depth=arms['front_edge_x']-(point[0]+radius)
  if not (-.0001<=rear<=.0006 and -.0001<=underside<=.0006 and depth>=.001):return False
 return True
