"""Recorded physical failure response, not synthetic/native task success."""
import json
from pathlib import Path
import numpy as np
from motion import Motion
HERE=Path(__file__).resolve().parent


def test_load_feedback_corrects_actual_recorded_static_tcp_error_and_is_bounded():
 d=json.loads((HERE/'test_fixtures/loaded-lift-stall.json').read_text());assert d['not_isaac'] and d['not_success']
 row=d['keyframe'];q=np.array(row['robot_q'][7:]);m=Motion('right',tracking_error_limit=.08)
 m.reference=np.array(row['action'][7:13]);old=m.reference.copy()
 target=d['target']
 oldpos,_=m.ik.tcp_pose(old,m.base);actual,_=m.ik.tcp_pose(q[:6],m.base);goal=np.array(target['pos']);previous_grip=q[6]
 assert np.linalg.norm(actual-goal)>.0025
 # Replaying a frozen measurement tests controller response/windup only.
 for _ in range(100):
  cmd,_,_=m.target(q,goal,target['quat'],.22,feedback_gain=3.)
  pos,_=m.ik.tcp_pose(cmd[:6],m.base)
  assert np.linalg.norm(pos-actual)<.0061
  assert np.max(np.abs(cmd[:6]-old))<=.020001
  assert abs(cmd[6]-previous_grip)<=.050001;previous_grip=cmd[6]
  old=cmd[:6].copy()
 assert np.dot(pos-oldpos,goal-actual)>1e-6
 assert abs(cmd[6]-.22)<1e-12


def test_real_part_orientation_error_blocks_descent_despite_near_target_wrist():
 from feedback import Controller,ControlFailure
 import pytest
 row=json.loads((HERE/'test_fixtures/tilt-slip-keyframe.json').read_text())['keyframe']
 plan=json.loads((HERE/'controller.json').read_text());spec=json.loads((HERE/'scene.json').read_text());c=Controller(plan,spec)
 target,errors=c.target_for_part(plan['phases'][6],row['frame'],np.array(row['robot_q']))
 assert errors[1]>.25 and errors[1]>plan['phases'][6]['angle_tolerance']
 # A physical part observation is mandatory; no fallback to nominal poses.
 with pytest.raises(ControlFailure,match='collet pose required'):
  c.target_for_part(plan['phases'][6],{'time':0.},np.array(row['robot_q']))
 assert np.isfinite(target['pos']).all() and np.isfinite(target['quat']).all()


def test_measured_angular_feedback_limits_static_windup_and_joint_rate():
 from feedback import Controller
 from motion import qangle
 row=json.loads((HERE/'test_fixtures/tilt-slip-keyframe.json').read_text())['keyframe'];q=np.array(row['robot_q'][7:])
 plan=json.loads((HERE/'controller.json').read_text());spec=json.loads((HERE/'scene.json').read_text());c=Controller(plan,spec)
 target,errors=c.target_for_part(plan['phases'][6],row['frame'],np.array(row['robot_q']))
 m=Motion('right');m.reference=q[:6].copy();_,r=m.ik.tcp_pose(q[:6],m.base);measured=m.ik.matrix_to_quat_xyzw(r);old=m.reference.copy()
 for _ in range(30):
  output,_,_=m.target(q,target['pos'],target['quat'],.22,feedback_gain=3.,angular_feedback_gain=1.5)
  _,r=m.ik.tcp_pose(output[:6],m.base)
  assert qangle(measured,m.ik.matrix_to_quat_xyzw(r))<.0805
  assert np.max(np.abs(output[:6]-old))<=.020001
  old=output[:6].copy()


def test_acquired_empty_jaw_terminates_before_chasing_a_lost_part():
 import copy,pytest
 from feedback import Controller,ControlFailure
 row=json.loads((HERE/'test_fixtures/loaded-lift-stall.json').read_text())['keyframe']
 c=Controller(json.loads((HERE/'controller.json').read_text()),json.loads((HERE/'scene.json').read_text()));c.index=4;c.acquired['right']=True
 # Isolate the independent loss guard from IK. The recorded valid body state
 # and an explicitly empty jaw must not silently keep pursuing a moving goal.
 c.motion['right'].target=lambda q,*a,**kw:(q.copy(),0.,0.)
 q=np.array(row['robot_q']);q[13]=.22
 for tick in (0.,.1):
  frame=copy.deepcopy(row['frame']);frame['time']=tick;c.step(q,frame)
 frame=copy.deepcopy(row['frame']);frame['time']=.3
 with pytest.raises(ControlFailure,match='grip lost'):c.step(q,frame)


def test_part_servo_ignores_axial_yaw_without_relaxing_entry_axis_tolerance():
 import copy
 from feedback import Controller
 from motion import qangle
 row=json.loads((HERE/'test_fixtures/loaded-lift-stall.json').read_text())['keyframe']
 plan=json.loads((HERE/'controller.json').read_text());c=Controller(plan,json.loads((HERE/'scene.json').read_text()))
 frame=copy.deepcopy(row['frame']);frame['bodies']['collet']['quat']=[0,0,np.sin(.7),np.cos(.7)]
 target,errors=c.target_for_part(plan['phases'][4],frame,np.array(row['robot_q']))
 _,r=c.motion['right'].ik.tcp_pose(np.array(row['robot_q'][7:13]),c.motion['right'].base)
 measured=c.motion['right'].ik.matrix_to_quat_xyzw(r)
 assert errors[1]<1e-7 and qangle(target['quat'],measured)<1e-7
 assert plan['phases'][6]['angle_tolerance']==.02
 assert plan['phases'][7]['angle_tolerance']==.02
