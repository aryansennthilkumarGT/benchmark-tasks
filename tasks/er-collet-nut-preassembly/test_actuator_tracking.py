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
 oldpos,_=m.ik.tcp_pose(old,m.base);actual,_=m.ik.tcp_pose(q[:6],m.base);goal=np.array(target['pos'])
 assert np.linalg.norm(actual-goal)>.0025
 # Replaying a frozen measurement tests controller response/windup only.
 for _ in range(100):
  cmd,_,_=m.target(q,goal,target['quat'],.22,feedback_gain=3.)
  pos,_=m.ik.tcp_pose(cmd[:6],m.base)
  assert np.linalg.norm(pos-actual)<.0061
  assert np.max(np.abs(cmd[:6]-old))<=.020001
  old=cmd[:6].copy()
 assert np.dot(pos-oldpos,goal-actual)>1e-6
 assert abs(cmd[6]-q[6])<=.050001


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
