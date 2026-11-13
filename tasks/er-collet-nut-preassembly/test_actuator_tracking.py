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
 target=json.loads((HERE/'controller.json').read_text())['phases'][4]['target']
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
