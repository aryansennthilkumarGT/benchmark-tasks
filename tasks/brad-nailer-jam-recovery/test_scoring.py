"""Synthetic scorer unit cases only; no native demonstration evidence."""
import copy,json
from pathlib import Path
import numpy as np,pytest
from scoring import Scorer
from kinematics import reconstruct
HERE=Path(__file__).resolve().parent
SPEC=json.loads((HERE/'scene.json').read_text())


def initial():
 return dict(time=0.,bodies={b['name']:dict(pos=b['pos'].copy(),quat=b['quat'].copy(),linear=[0,0,0],angular=[0,0,0]) for a in SPEC['assemblies'] for b in a['bodies']},joints=SPEC['initial_joint_values'].copy(),max_penetration=.00001,robot_clearance=.05)


def goal(t=1.):
 f=initial();f['time']=t;tray=f['bodies']['parts_tray']['pos'];f['bodies']['bent_brad'].update(pos=[tray[0],tray[1],SPEC['table_top']+.0045],quat=[2**-.5,0,0,2**-.5]);return f


def complete(judge,frame):
 for i in range(42):
  current=copy.deepcopy(frame);current['time']=frame['time']+i/20;r=judge.update(current)
 return r


def test_completed_substitution_cannot_initialize_episode():
 j=Scorer(SPEC);r=j.update(goal());assert r.score==0 and 'initial' in r.failure


def test_real_two_arm_pin_capture_and_past_center_are_required_for_full_score():
 j=Scorer(SPEC);f=initial();assert j.update(f).score==0
 g=goal();assert j.captured(g['bodies']) and j.past_center(g['bodies'],g['joints'])
 assert j.update(g).score==.75
 assert complete(j,goal(1.05)).success
 j.reset();j.update(initial());f=goal();f['joints']['bail_rotation']+=.35
 poses=reconstruct(SPEC,f['bodies']['nose_body'],f['joints'])
 for name,p in poses.items():f['bodies'][name].update(p)
 assert not j.captured(f['bodies']);r=j.update(f);assert r.score==.5 and not r.success and r.failure is None


def test_clearance_and_continuous_observation_are_needed_for_hold():
 j=Scorer(SPEC);j.update(initial());f=goal();f['robot_clearance']=None
 assert complete(j,f).score==.75
 j.reset();j.update(initial());j.update(goal(1.));assert not j.update(goal(3.)).success
 assert complete(j,goal(3.05)).success


def test_pose_window_rejects_peak_to_peak_motion_even_when_each_side_is_near_first():
 j=Scorer(SPEC);j.update(initial());f=goal();j.update(f)
 f=goal(1.05);f['bodies']['bent_brad']['pos'][0]+=.0004;j.update(f)
 f=goal(1.10);f['bodies']['bent_brad']['pos'][0]-=.0004;j.update(f)
 # Fewer than two seconds since the oscillation must never qualify.
 for k in range(1,38):f=goal(1.10+k/20);assert not j.update(f).success


@pytest.mark.parametrize('mutation,reason',[
 ('disconnect','Disconnected'),('stop','mechanical stop'),('penetration','interference'),('fixture','fixture moved'),('lost','lost'),('missing','Missing'),('nonfinite','Nonfinite')])
def test_invalid_strategies_latch_zero_through_later_good_states(mutation,reason):
 j=Scorer(SPEC);j.update(initial());f=goal()
 if mutation=='disconnect':f['bodies']['bail_crosspin']['pos'][2]+=.005
 elif mutation=='stop':f['joints']['bail_extension']=.01
 elif mutation=='penetration':f['max_penetration']=.001
 elif mutation=='fixture':f['bodies']['nose_body']['pos'][0]+=.003
 elif mutation=='lost':f['bodies']['bent_brad']['pos'][2]=SPEC['table_top']-.02
 elif mutation=='missing':del f['bodies']['draw_bail']
 else:f['bodies']['bent_brad']['linear'][0]=float('nan')
 r=j.update(f);assert r.score==0 and reason.lower() in r.failure.lower()
 assert complete(j,goal(2.)).score==0


def test_pin_axis_must_cover_both_capture_arms_and_unobserved_fastener_is_not_removed():
 j=Scorer(SPEC);f=initial();assert j.captured(f['bodies'])
 f['bodies']['bail_crosspin']['quat']=[0,0,0,1]  # root is flipped but axis sign remains valid
 assert j.captured(f['bodies'])
 f['bodies']['bail_crosspin']['quat']=[2**-.5,0,0,2**-.5]
 assert not j.captured(f['bodies'])
 j.reset();assert j.update(initial()).score==0
