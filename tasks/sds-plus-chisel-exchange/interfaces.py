"""Observable physical interface checks; no controller phases or reward access."""
import numpy as np
try:
 from .motion import rotate,conjugate
except ImportError:
 from motion import rotate,conjugate

def local(body,point):return rotate(conjugate(body['quat']),np.asarray(point)-body['pos'])

def retained(spec,bodies,joints,name='replacement_flat_chisel'):
 h=bodies['tool_holder'];b=bodies[name];p=spec['parameters'];leading=local(h,b['pos']);axis=rotate(conjugate(h['quat']),rotate(b['quat'],[1,0,0]));key=rotate(conjugate(h['quat']),rotate(b['quat'],[0,1,0]));ball=local(b,bodies['locking_ball']['pos']);ball_h=local(h,bodies['locking_ball']['pos'])
 return bool(.031<=leading[0]<=.044 and np.linalg.norm(leading[1:])<=.00035 and axis[0]>=np.cos(.02) and abs(key[2])<=np.sin(.12) and joints['sleeve_retraction']<=.00035 and p['closed_slot_rear']+.0002<=ball[0]<=p['closed_slot_front']-.0002 and abs(ball[1])<=.0005 and abs(ball[2])>=.007 and abs(ball[2])-.0035<=p['shank_radius']-.00025 and p['authored_ball_race_x_min']<=ball_h[0]<=p['authored_locked_ball_x_max'])
