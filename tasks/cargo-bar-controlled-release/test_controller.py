"""Real pinned YAM IK/FK and feedback contracts, not contact demonstrations."""
import copy,json,math
from pathlib import Path
import numpy as np,pytest
from yam_arena import ik,station
from yam_arena.constants import READY
from feedback import Controller,ControlFailure,rotate,multiply,conjugate,axis_quat
from kinematics import reconstruct
HERE=Path(__file__).resolve().parent
SPEC=json.loads((HERE/'scene.json').read_text());PLAN=json.loads((HERE/'controller.json').read_text())


def fixture():
 root=next(b for a in SPEC['assemblies'] for b in a['bodies'] if b['name']=='outer_tube')
 js=SPEC['initial_joint_values'].copy()
 return root,dict(time=0.,joints=js,bodies=reconstruct(SPEC,root,js))


def test_handle_path_stays_on_captured_circle_with_bounded_real_joint_steps():
 c=Controller(PLAN,SPEC);c.index=8;p=c.phases[8];root,f=fixture();q=np.tile(np.r_[READY,1.],2)
 initial=PLAN['phases'][7]['target'];arm,pe,re=ik.solve(initial['pos'],initial['quat'],base_pos=station.BASES['right'],q_init=q[7:13],iters=500,tol=1e-5)
 assert pe<2e-5 and re<1e-4;q[7:13]=arm
 initial_tcp,initial_r=ik.tcp_pose(arm,station.BASES['right']);h=f['bodies']['handle']
 offset=rotate(conjugate(h['quat']),initial_tcp-np.array(h['pos']));tool=multiply(conjugate(h['quat']),ik.matrix_to_quat_xyzw(initial_r))
 for _ in range(500):
  action,_,_=c.arc_action(p,f,q);assert np.max(np.abs(action[:6]-q[7:13]))<=.020001
  q[7:]=action;tcp,r=ik.tcp_pose(q[7:13],station.BASES['right']);rotation=multiply(ik.matrix_to_quat_xyzw(r),conjugate(tool))
  local=multiply(conjugate(root['quat']),rotation);angle=2*math.atan2(local[0],local[3]);f['joints']['handle_rotation']=angle
  f['bodies'].update(reconstruct(SPEC,root,f['joints']));h=f['bodies']['handle']
  expected=np.array(h['pos'])+rotate(h['quat'],offset)
  assert np.linalg.norm(tcp-expected)<3e-5
  if abs(angle-2.6)<1e-4:break
 else:pytest.fail('No circular-path progress')


def test_missing_stale_feedback_and_non_grasp_stall_fail_closed():
 c=Controller(PLAN,SPEC);root,f=fixture();q=np.tile(np.r_[READY,1.],2)
 for b in f['bodies'].values():b.update(linear=[0,0,0],angular=[0,0,0])
 c.step(q,f)
 with pytest.raises(ControlFailure,match='Stale'):c.step(q,f)
 c.reset();c.step(q,f);f['time']=10.
 with pytest.raises(ControlFailure,match='stall'):c.step(q,f)
 c.reset()
 with pytest.raises(ControlFailure,match='missing'):c.step(q,dict(time=0.))


def test_grasp_recovery_is_bounded_and_reset_clears_failure():
 c=Controller(PLAN,SPEC);c.index=3;p=c.phases[3]
 c.begin_recovery(p,0.);assert c.recovery and c.recovery['phase']['grasp_width']==0.
 c.begin_recovery(p,1.);assert c.attempts[3]==2
 with pytest.raises(ControlFailure,match='exhausted'):c.begin_recovery(p,2.)
 c.reset();assert not c.failed and not c.attempts and not c.arc_grasps
