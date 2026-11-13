"""Public physical predicates: complete eye capture and visible flush latch."""
import math
import numpy as np
try:
 from .motion import rotate,conjugate
except ImportError:
 from motion import rotate,conjugate

def local(root,point):return rotate(conjugate(root['quat']),np.asarray(point)-root['pos'])
def seated(spec,bodies):
 p=local(bodies['hook_body'],bodies['drawbar_eye']['pos']);goal=np.asarray(spec['parameters']['eye_goal_local']);axis=rotate(conjugate(bodies['hook_body']['quat']),rotate(bodies['drawbar_eye']['quat'],[0,0,1]))
 return bool(np.linalg.norm(p[:2]-goal[:2])<=.004 and abs(p[2]-goal[2])<=.0015 and abs(axis[2])>=math.cos(.08))
def latched(spec,bodies,joints):
 return seated(spec,bodies) and abs(joints['latch_rotation'])<=.025 and abs(joints['lock_rotation'])<=.035
