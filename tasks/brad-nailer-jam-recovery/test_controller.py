"""Failure guards and physical arc contracts, not ideal or native success."""
import copy,json
from pathlib import Path
import numpy as np,pytest
from yam_arena.constants import READY
from feedback import Controller,ControlFailure
from ideal_fixture import IdealFixture
from provenance import validate
HERE=Path(__file__).resolve().parent

def fixture():
 f=IdealFixture(HERE);return f,Controller(f.plan,f.spec)

def test_invalid_and_stale_feedback_fail_closed():
 f,c=fixture();frame=f.frame();c.step(f.q,frame)
 with pytest.raises(ControlFailure,match='Stale'):c.step(f.q,frame)
 f,c=fixture()
 with pytest.raises(ControlFailure,match='Invalid'):c.step(np.zeros(13),f.frame())

def test_missing_native_body_fails_without_advancing_phase():
 f,c=fixture();i=next(i for i,p in enumerate(c.phases) if p['label']=='Grip latch lever');c.index=i;frame=f.frame();del frame['bodies']['latch_lever']
 with pytest.raises((ControlFailure,KeyError)):c.step(f.q,frame)
 assert c.index==i and not c.done

def test_empty_jaw_cannot_satisfy_acquisition_and_recovery_is_bounded():
 f,c=fixture();p=next(p for p in c.phases if p['label']=='Grip latch lever');c.index=c.phases.index(p);c.targets['right']=copy.deepcopy(p)
 c.start_recovery(p,0.,f.q);assert c.recovery['target']['opening']==.55
 c.recovery=None;c.start_recovery(p,1.,f.q);c.recovery=None
 with pytest.raises(ControlFailure,match='exhausted'):c.start_recovery(p,2.,f.q)
 assert c.attempts[c.index]==2

def test_phase_sequence_uses_physical_circles_and_two_distinct_pin_grasps():
 f,c=fixture();labels=[p['label'] for p in c.phases]
 assert len(labels)==len(set(labels))+labels.count('Park left arm')+labels.count('Park right arm')-2
 for label in ['Lift jam-clear lever','Open nose door','Close door while carrying pin clear','Guide pin around front of both arms','Insert pin through open hook mouth','Draw latch past center with both pin ends captured']:
  p=next(p for p in c.phases if p['label']==label);assert 'arc' in p and p['grasp_width']>0
 assert next(p for p in c.phases if p['label']=='Close door while carrying pin clear')['coupled']=='rigid'
 assert next(p for p in c.phases if p['label'].startswith('Draw latch'))['coupled']=='hook'
 assert labels.index('Regrasp crosspin top end')<labels.index('Release crosspin center')<labels.index('Regrasp open lever')

def test_every_numeric_parameter_is_classified_and_bound_to_source():
 r=validate(HERE);assert r['passed'] and r['numeric_values']>4000 and r['counts']['INDEPENDENTLY_MEASURED']==0

def test_coupled_arc_does_not_overwrite_follower_with_earlier_world_hold():
 from yam_arena import ik,station
 from yam_arena.demo import DOWN_GRIP
 from motion import rotate,multiply,conjugate,axis_quat
 f,c=fixture();phase=next(p for p in c.phases if p['label']=='Close door while carrying pin clear');index=c.phases.index(phase)
 js=c.phases[index-1]['nominal_joints'];bodies=c.phases[index-1]['nominal_bodies'];frame=dict(time=0.,bodies=bodies,joints=js)
 for side,name,local,tool in [('left','nose_door',[.025,0,-.022],multiply(bodies['nose_door']['quat'],multiply(conjugate(f.root['quat']),DOWN_GRIP))),('right','bail_crosspin',None,multiply(bodies['nose_door']['quat'],multiply(conjugate(f.root['quat']),axis_quat([1,0,0],-(np.pi/2+.5)))) )]:
  b=bodies[name];position=np.array(b['pos'])+(rotate(b['quat'],local) if local is not None else rotate(tool,[0,0,-.011]))
  solved,pe,re=ik.solve(position,tool,q_init=READY,base_pos=station.BASES[side],iters=500,tol=1e-5);assert pe<.00003 and re<.0001
  offset=0 if side=='left' else 7;f.q[offset:offset+6]=solved
 c.index=index;c.targets['right']=copy.deepcopy(c.phases[index-1])
 def wrong_hold(*a,**kw):raise AssertionError('Earlier follower world hold must not execute during coupled phase')
 c.motion['right'].target=wrong_hold
 output=c.step(f.q,frame);assert output.shape==(14,) and np.isfinite(output).all()
 assert all(c.motion[side].reference is not None for side in ('left','right'))

def test_passive_opening_model_uses_the_complete_source_bound_door_trace():
 f,c=fixture();assert f.door_opening[0]['joints']['door_rotation']<.01
 assert f.door_opening[-1]['joints']['door_rotation']>1.85
 assert f.door_opening[-1]['joints']['bail_rotation']-f.door_opening[0]['joints']['bail_rotation']>.3
