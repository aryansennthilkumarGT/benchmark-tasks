"""Adversarial scoring with independent MuJoCo FK fixtures, never robot evidence."""
import copy,json,math
from pathlib import Path
import mujoco,numpy as np,pytest
from mechanism_cpu import export,initialize,observe
from scoring import Scorer
HERE=Path(__file__).resolve().parent
SPEC=json.loads((HERE/'scene.json').read_text())
MODEL=mujoco.MjModel.from_xml_string(export(SPEC,False,False))


def frame(t=0.,finished=False,root_offset=(0,0,0),extension=.003,handle_angle=2.6):
 d=mujoco.MjData(MODEL);initialize(MODEL,d,SPEC)
 if finished:
  root=SPEC['parameters']['authored_cradle_root'];d.qpos[:3]=np.array(root)+root_offset
  values=dict(telescope=extension,pinion_rotation=-extension/SPEC['parameters']['authored_pinion_pitch_radius'],
              left_compliance=0.,right_compliance=0.,handle_rotation=handle_angle,trigger_pull=0.,holding_pawl_rotation=.36,driving_pawl_rotation=.245)
  for n,v in values.items():
   j=mujoco.mj_name2id(MODEL,mujoco.mjtObj.mjOBJ_JOINT,n);d.qpos[MODEL.jnt_qposadr[j]]=v
 row=observe(MODEL,d,SPEC)
 for b in row['bodies'].values():b.update(linear=[0,0,0],angular=[0,0,0])
 return dict(schema=1,time=t,bodies=row['bodies'],joints=row['joints'],max_penetration=0.,robot_clearance=.04)


def finish(judge,root_offset=(0,0,0),extension=.003):
 judge.update(frame());end=frame(finished=True,root_offset=root_offset,extension=extension)
 # Dense synthetic interpolation of physical FK states, not a physics rollout.
 for i in range(1,51):
  f=copy.deepcopy(end);f['time']=i*.05;r=judge.update(f)
 return end,r

def test_initial_is_zero_and_complete_geometric_fixture_scores():
 s=Scorer(SPEC);assert s.update(frame()).score==0.
 s.reset();_,r=finish(s);assert r.success and r.score==1.

def test_valid_alternate_final_geometry_is_not_expert_path_gated():
 _,r=finish(Scorer(SPEC),(.001,0,0),.0045);assert r.success

def test_final_pose_substitution_cannot_start_a_trial():
 r=Scorer(SPEC).update(frame(finished=True));assert r.score==0 and r.failure=='initial_layout'

def test_joint_body_disconnection_or_skip_latches_zero():
 for change in [lambda f:f['bodies']['inner_tube']['pos'].__setitem__(0,.28),
                lambda f:f['joints'].__setitem__('pinion_rotation',0.)]:
  s=Scorer(SPEC);f=frame();change(f);assert s.update(f).failure
  _,r=finish(s);assert r.score==0

def test_frame_movement_loss_and_interpenetration_fail():
 for change in [lambda f:f['bodies']['wall_frame']['pos'].__setitem__(0,.242),
                lambda f:f.update(max_penetration=.001)]:
  f=frame();change(f);assert Scorer(SPEC).update(f).score==0 and Scorer(SPEC).update(f).failure
 s=Scorer(SPEC);s.update(frame());f=frame(.05,True,root_offset=(0,0,-.06));r=s.update(f)
 assert r.score==0 and r.failure

def test_hands_near_or_disturbed_bar_cannot_sustain_success():
 s=Scorer(SPEC);f,r=finish(s);assert r.success
 f['time']=2.55;f['robot_clearance']=0.;assert not s.update(f).success
 f['time']=2.60;f['bodies']['inner_tube']['linear']=[.02,0,0];assert not s.update(f).success

def test_missing_nan_bad_norm_and_conflicting_frames_fail():
 for change in [lambda f:f['bodies'].pop('handle'),lambda f:f['joints'].__setitem__('telescope',float('nan')),
                lambda f:f['bodies']['handle'].__setitem__('quat',[0,0,0,2])]:
  f=frame();change(f);assert Scorer(SPEC).update(f).failure
 s=Scorer(SPEC);f=frame();r=s.update(f);assert s.update(copy.deepcopy(f))==r
 f['robot_clearance']=0.;assert s.update(f).failure

def test_reset_clears_history_and_failure():
 s=Scorer(SPEC);s.update(frame(finished=True));s.reset();assert s.update(frame()).failure is None and s.result.score==0.


def test_passive_handle_relaxation_after_unloading_is_a_valid_alternate_state():
 s=Scorer(SPEC);s.update(frame())
 for i in range(1,51):r=s.update(frame(i*.05,True,handle_angle=2.24))
 assert r.success and r.score==1.
