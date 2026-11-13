"""Actual official FK/IK screw-lead regression, without native contact claims."""
import math
import unittest
import numpy as np
from yam_arena import ik,station
from yam_arena.constants import READY
from yam_arena.demo import DOWN_GRIP
from motion import Motion,multiply,axis_quat

class CoupledMotion(unittest.TestCase):
 def test_thread_descent_stays_coupled_to_rotation_between_endpoints(self):
  side='right';start=np.array([.24,0.,.85]);target=start+np.array([0,0,-.003/8])
  q0,pe,re=ik.solve(start,DOWN_GRIP,q_init=np.array(READY),base_pos=station.BASES[side],iters=700,damping=.015,tol=1e-6)
  self.assertLess(pe,1e-5);self.assertLess(re,1e-5)
  measured=np.r_[q0,.30];motion=Motion(side);rotated=multiply(axis_quat([0,0,1],-math.pi/4),DOWN_GRIP)
  maximum=0.
  initial_p,initial_r=ik.tcp_pose(q0,station.BASES[side]);initial_yaw=math.atan2(initial_r[1,0],initial_r[0,0])
  for _ in range(180):
   measured,pe,re=motion.target(measured,target,rotated,.20,speed=.004,angular_speed=.5)
   p,r=ik.tcp_pose(measured[:6],station.BASES[side]);yaw=math.atan2(r[1,0],r[0,0]);delta=(yaw-initial_yaw+math.pi)%(2*math.pi)-math.pi
   maximum=max(maximum,abs(p[2]-initial_p[2]-.003*delta/(2*math.pi)))
   if pe<.00002 and re<.0002:break
  self.assertLess(maximum,.00008)
  self.assertLess(pe,.00002);self.assertLess(re,.0002)
if __name__=='__main__':unittest.main()
