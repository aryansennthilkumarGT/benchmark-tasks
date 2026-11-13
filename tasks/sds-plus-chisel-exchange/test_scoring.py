"""Synthetic objective/adversarial cases, never demonstrations or physical evidence."""
import copy,json,math
from pathlib import Path
import numpy as np,pytest
from scoring import Scorer
from motion import axis_quat
from interfaces import retained
HERE=Path(__file__).resolve().parent
SPEC=json.loads((HERE/'scene.json').read_text())
def initial():return dict(time=0.,bodies={b['name']:dict(pos=b['pos'].copy(),quat=b['quat'].copy(),linear=[0,0,0],angular=[0,0,0]) for a in SPEC['assemblies'] for b in a['bodies']},joints=SPEC['initial_joint_values'].copy(),max_penetration=.00003,robot_clearance=.05)
def goal(t=1.):
 f=initial();f['time']=t;f['bodies']['used_point_chisel'].update(pos=[.37,-.30,SPEC['table_top']+.0102]);f['bodies']['replacement_flat_chisel'].update(pos=[.41,0,.86],quat=[0,0,0,1]);return f
def hold(j,f):
 for i in range(42):g=copy.deepcopy(f);g['time']=f['time']+i/20;r=j.update(g)
 return r

def test_goal_requires_fresh_initial_state_and_continuous_released_hold():
 j=Scorer(SPEC);assert j.update(goal()).score==0 and j.failed
 j.reset();assert j.update(initial()).score==0;assert j.update(goal()).score==.75;assert hold(j,goal(1.05)).success

def test_both_symmetric_groove_orientations_and_axial_play_are_valid():
 j=Scorer(SPEC);j.update(initial());f=goal();f['bodies']['replacement_flat_chisel']['quat']=axis_quat([1,0,0],math.pi).tolist();assert retained(SPEC,f['bodies'],f['joints']);assert hold(j,f).success
 j.reset();j.update(initial());f=goal();f['bodies']['replacement_flat_chisel']['pos'][0]+=.0018;assert hold(j,f).success

@pytest.mark.parametrize('mutation',['unreleased_sleeve','miskeyed','outside_closed_slot'])
def test_geometric_capture_not_plain_insertion_is_required(mutation):
 j=Scorer(SPEC);j.update(initial());f=goal()
 if mutation=='unreleased_sleeve':f['joints']['sleeve_retraction']=.008;f['bodies']['locking_sleeve']['pos'][0]+=.008
 elif mutation=='miskeyed':f['bodies']['replacement_flat_chisel']['quat']=axis_quat([1,0,0],math.pi/2).tolist()
 else:f['bodies']['replacement_flat_chisel']['pos'][0]+=.015
 assert not hold(j,f).success;assert j.result.score==.5

@pytest.mark.parametrize('mutation',['ball_escape','sleeve_disconnect','fixed_move','lost','missing','nonfinite','overlap','joint_stop'])
def test_invalid_strategies_permanently_invalidate(mutation):
 j=Scorer(SPEC);j.update(initial());f=goal()
 if mutation=='ball_escape':f['bodies']['locking_ball']['pos'][1]+=.003
 elif mutation=='sleeve_disconnect':f['bodies']['locking_sleeve']['pos'][0]+=.003
 elif mutation=='fixed_move':f['bodies']['tool_holder']['pos'][1]+=.003
 elif mutation=='lost':f['bodies']['used_point_chisel']['pos'][2]=.1
 elif mutation=='missing':del f['bodies']['locking_ball']
 elif mutation=='nonfinite':f['bodies']['replacement_flat_chisel']['linear'][1]=np.nan
 elif mutation=='overlap':f['max_penetration']=.001
 else:f['joints']['sleeve_retraction']=.02
 r=j.update(f);assert r.failure and r.score==0;assert hold(j,goal(2.)).score==0

def test_clearance_is_observed_and_time_gap_clears_witness_history():
 j=Scorer(SPEC);j.update(initial());f=goal();f['robot_clearance']=None;assert hold(j,f).score==.75
 j.reset();j.update(initial());j.update(goal(1.));assert not j.update(goal(3.)).success
 assert hold(j,goal(3.05)).success

def test_pairwise_witness_drift_rejects_opposed_small_excursions():
 j=Scorer(SPEC);j.update(initial());j.update(goal(1.))
 f=goal(1.05);f['bodies']['used_point_chisel']['pos'][0]+=.0004;j.update(f)
 f=goal(1.10);f['bodies']['used_point_chisel']['pos'][0]-=.0004;j.update(f)
 for i in range(1,38):assert not j.update(goal(1.10+i/20)).success


def test_ball_in_rear_insertion_relief_is_not_locked_even_with_closed_sleeve():
 j=Scorer(SPEC);j.update(initial());f=goal();f['bodies']['locking_ball']['pos'][0]+=.0045;f['bodies']['locking_ball']['pos'][2]+=.0005
 assert not retained(SPEC,f['bodies'],f['joints']);assert hold(j,f).score==.5


def test_intact_full_insertion_near_real_backstop_is_not_rejected_by_arbitrary_depth():
 j=Scorer(SPEC);j.update(initial());f=goal();f['bodies']['replacement_flat_chisel']['pos'][0]=SPEC['parameters']['holder_mouth'][0]+.0448;assert hold(j,f).success
