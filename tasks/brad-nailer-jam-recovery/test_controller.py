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
 f,c=fixture();p=next(p for p in c.phases if p['label']=='Grip latch lever');c.index=c.phases.index(p);c.targets['right']=copy.deepcopy(p);f.q[13]=0.
 c.start_recovery(p,0.,f.q);assert np.isclose(c.recovery['target']['opening'],(.002+.002)/.0939)
 c.recovery=None;c.start_recovery(p,1.,f.q);c.recovery=None
 with pytest.raises(ControlFailure,match='exhausted'):c.start_recovery(p,2.,f.q)
 assert c.attempts[c.index]==2

def test_phase_sequence_uses_physical_circles_and_two_distinct_pin_grasps():
 f,c=fixture();labels=[p['label'] for p in c.phases]
 assert len(labels)==len(set(labels))+labels.count('Park left arm')+labels.count('Park right arm')-2
 for label in ['Lift jam-clear lever','Open nose door','Close door while carrying pin clear','Guide outboard pin toward hook mouth','Bring pin below both retaining lips','Seat crosspin while passive lever follows','Push lever shut with pin already captured']:
  p=next(p for p in c.phases if p['label']==label);assert 'arc' in p and p['grasp_width']>0
 assert next(p for p in c.phases if p['label']=='Close door while carrying pin clear')['coupled']=='rigid'
 assert next(p for p in c.phases if p['label']=='Seat crosspin while passive lever follows')['pin_drive'] is True
 assert 'coupled' not in next(p for p in c.phases if p['label'].startswith('Push lever'))
 assert labels.index('Seat crosspin while passive lever follows')<labels.index('Release engaged crosspin')<labels.index('Regrasp partially closed lever')

def test_every_numeric_parameter_is_classified_and_bound_to_source():
 r=validate(HERE);assert r['passed'] and r['numeric_values']>4000 and r['counts']['INDEPENDENTLY_MEASURED']==0

def test_coupled_arc_does_not_overwrite_follower_with_earlier_world_hold():
 from yam_arena import ik,station
 from yam_arena.demo import DOWN_GRIP
 from motion import rotate,multiply,conjugate,axis_quat
 f,c=fixture();phase=next(p for p in c.phases if p['label']=='Close door while carrying pin clear');index=c.phases.index(phase)
 js=c.phases[index-1]['nominal_joints'];bodies=c.phases[index-1]['nominal_bodies'];frame=dict(time=0.,bodies=bodies,joints=js)
 for side,name,local,tool in [('left','nose_door',[.025,0,-.022],multiply(bodies['nose_door']['quat'],multiply(conjugate(f.root['quat']),DOWN_GRIP))),('right','bail_crosspin',None,multiply(bodies['nose_door']['quat'],multiply(conjugate(f.root['quat']),axis_quat([1,0,0],-(np.pi/2+.5)))) )]:
  b=bodies[name];position=np.array(b['pos'])+rotate(b['quat'],local) if local is not None else np.array(c.bind(c.phases[index-1],frame,f.q)['target']['pos'])
  if side=='right':tool=c.bind(c.phases[index-1],frame,f.q)['target']['quat']
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

def test_wide_obstruction_stops_before_an_unsafe_reacquire():
 f,c=fixture();p=next(p for p in c.phases if p['label']=='Grip latch lever');c.index=c.phases.index(p);c.targets['right']=copy.deepcopy(p)
 with pytest.raises(ControlFailure,match='wide obstruction'):c.start_recovery(p,0.,f.q)
 assert c.recovery is None

def test_opening_reference_covers_full_requested_lever_stroke():
 f,c=fixture();requested=next(p for p in c.phases if p['label']=='Lift jam-clear lever')['arc']['angle'];angles=[r['joints']['lever_rotation'] for r in f.opening]
 assert min(angles)-.0001<=requested<=max(angles)+.0001

def test_stale_plan_cannot_control_changed_geometry():
 f=IdealFixture(HERE);modified=copy.deepcopy(f.spec);modified['parameters']['draw_rest']+=.001
 with pytest.raises(ControlFailure,match='different scene'):Controller(f.plan,modified)

def test_changed_physical_reference_cannot_be_reused_with_an_old_plan(tmp_path):
 for name in ['scene.json','controller.json','guided-cycle-reference.json']:(tmp_path/name).write_bytes((HERE/name).read_bytes())
 p=tmp_path/'guided-cycle-reference.json';data=json.loads(p.read_text());data['checks'][0]['joints']['lever_rotation']+=.5;p.write_text(json.dumps(data))
 with pytest.raises(ValueError,match='reference source mismatch'):IdealFixture(tmp_path)

def test_plan_generation_preserves_the_physical_reset_specification():
 from plan_controller import make_plan
 import hashlib
 spec=json.loads((HERE/'scene.json').read_text());before=copy.deepcopy(spec);plan=make_plan(spec)
 assert spec==before
 assert plan['scene_content_sha256']==hashlib.sha256(json.dumps(before,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()


def test_brad_acquisition_clears_the_real_case_bumper_with_stock_finger_meshes():
 from audit_geometry import geometry_module
 from robot_geometry import arm_hulls,task_collisions
 from yam_arena import ik,station
 f,c=fixture();phase=next(p for p in c.phases if p['label']=='Reach bent brad');g=geometry_module(HERE)
 target=phase['target'];q0=np.array([-.61,2.19,1.88,-1.26,0.,-.61])
 def hits(pos):
  q,pe,re=ik.solve(pos,target['quat'],q_init=q0,base_pos=station.BASES['left'],iters=300,tol=1e-6)
  assert pe<1e-5 and re<1e-4
  return [h for h in task_collisions(g,arm_hulls('left',np.r_[q,phase['opening']]),f.spec,phase['nominal_bodies'],threshold=.00005) if h['body']!='bent_brad']
 # The former goal permits409um of case penetration, which looked clean to
 # the old500um screen but physically blocks the fingers before acquisition.
 old=np.asarray(target['pos'])-np.array([.002,0.,0.]);bad=hits(old)
 assert any(h['body']=='nose_body' and h['penetration_m']>.0003 for h in bad)
 assert hits(target['pos'])==[]


def test_actual_closed_jaw_capture_allows_contact_deflection_but_not_empty_grip():
 # Recorded real MuJoCo frames, not a mocked physics-success experiment.
 data=json.loads((HERE/'test_fixtures/grip-contact-keyframes.json').read_text())
 rows=data['frames'];assert data['not_complete_expert'] and data['not_isaac']
 for empty in [False,True]:
  f,c=fixture();c.index=17
  for row in rows[1:]:
   q=np.array(row['robot_q']);frame=copy.deepcopy(row['frame'])
   if empty:q[6]=0.
   c.step(q,frame)
  assert (c.index==18) is (not empty)


def test_released_door_entry_clears_recorded_motion_before_jaw_closure():
 from audit_geometry import geometry_module
 from robot_geometry import arm_hulls,task_collisions
 from yam_arena import ik,station
 # True start/stall observations from the previous failed physical run. Test
 # static geometry at its measured door excursion, not an ideal success claim.
 data=json.loads((HERE/'test_fixtures/door-approach-keyframes.json').read_text())
 assert data['not_isaac'] and data['not_complete_expert']
 a,b=data['frames'];f,c=fixture();p=next(p for p in c.phases if p['label']=='Reach open door again')
 target=c.bind(p,a['frame'],np.array(a['robot_q']))['target']
 q,pe,re=ik.solve(target['pos'],target['quat'],q_init=np.array(a['robot_q'][:6]),base_pos=station.BASES['left'],iters=500,tol=1e-6)
 assert pe<1e-5 and re<1e-4
 g=geometry_module(HERE)
 def hits(opening):return task_collisions(g,arm_hulls('left',np.r_[q,opening]),f.spec,b['frame']['bodies'],threshold=.00005)
 assert any(h['body']=='nose_door' and h['penetration_m']>.002 for h in hits(.06))
 assert hits(p['opening'])==[]
 assert next(p for p in c.phases if p['label']=='Regrasp open nose door')['opening']==0.


def test_pin_capture_tracks_actual_free_pin_motion_and_preserves_empty_jaw_guard():
 data=json.loads((HERE/'test_fixtures/pin-capture-keyframes.json').read_text());assert data['not_success'] and data['not_isaac']
 f,c=fixture();c.index=30;p=c.phases[30];assert p['grasp_width']==.0022
 previous=None;previous_command=None;displacement=0.
 for row in data['frames']:
  q=np.array(row['robot_q']);frame=copy.deepcopy(row['frame']);action=c.step(q,frame)
  bound=np.array(c.targets['right']['target']['pos'])
  expected=c.bind(p,frame,q)['target']['pos'];assert np.allclose(bound,expected)
  if previous is not None:displacement+=float(np.linalg.norm(bound-previous))
  previous=bound
  if previous_command is not None:assert abs(action[13]-previous_command)<=.005001
  previous_command=float(action[13])
 assert displacement>p['position_tolerance'] and not c.done and c.index==30


def test_blocked_pin_grip_preserves_slow_command_slew_without_capping_final_force():
 from motion import Motion
 m=Motion('right');previous=.3
 for _ in range(30):
  command=m.gripper_target(.3,.22,.005)
  assert abs(command-previous)<=.005001;previous=command
 assert abs(command-.22)<1e-12
