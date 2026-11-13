"""Numerical/geometry/contracts only; never native grasp or holding evidence."""
import ast,copy,importlib,json,math,tempfile,types,unittest
from pathlib import Path
import numpy as np
from generate_scene import make_scene,make_plan,hook_pose
from scoring import Scorer
from feedback import Controller,ControlFailure
HERE=Path(__file__).resolve().parent
SPEC=json.loads((HERE/'scene.json').read_text());PLAN=json.loads((HERE/'controller.json').read_text())

def frame(states=None,t=0.):
 states=states or {b['name']:b for a in SPEC['assemblies'] for b in a['bodies']}
 return dict(schema=1,time=t,bodies={n:dict(pos=list(b['pos']),quat=list(b['quat']),linear=[0,0,0],angular=[0,0,0]) for n,b in states.items()},joints={},max_penetration=0.,robot_clearance=.025)

def completed(s):
 for i,p in enumerate(PLAN['phases']):f=frame(p['nominal_bodies'],i*1.);r=s.update(f)
 for _ in range(41):f['time']+=.05;r=s.update(copy.deepcopy(f))
 return f,r

class Tests(unittest.TestCase):
 def test_generated_scene_and_plan_are_current(self):self.assertEqual(make_scene(),SPEC);self.assertEqual(make_plan(SPEC),PLAN)
 def test_primary_collet_dimensions(self):
  p=SPEC['parameters'];self.assertEqual([p[n] for n in ('collet_D1','collet_D2','collet_D3','collet_length','collet_groove_width','collet_nose_length')],[.033,.032,.0292,.04,.0036,.0055])
 def test_initial_zero_then_hook_pivot_release_full(self):
  s=Scorer(SPEC);self.assertEqual(s.update(frame()).score,0.);s.reset();_,r=completed(s);self.assertTrue(r.success);self.assertEqual(r.score,1.)
 def test_direct_final_pose_without_hook_has_no_credit(self):
  f=frame(PLAN['phases'][-1]['nominal_bodies']);self.assertEqual(Scorer(SPEC).update(f).score,0.)
 def test_wrong_cam_side_does_not_establish_engagement(self):
  p,q=hook_pose();f=frame();f['bodies']['collet'].update(pos=[.48-p[0],p[1],p[2]],quat=[0,-q[1],0,q[3]])
  self.assertEqual(Scorer(SPEC).update(f).score,0.)
 def test_partial_hook_and_out_of_zone_reset(self):
  p,q=hook_pose();f=frame();f['bodies']['collet'].update(pos=p,quat=q);s=Scorer(SPEC);s.update(frame());f['time']=1.;self.assertEqual(s.update(f).score,.25)
  f['time']=1.05;f['bodies']['collet']['pos'][2]+=.01;self.assertEqual(s.update(f).score,0.)
 def test_missing_or_extra_body_nonfinite_and_quaternion_fail(self):
  for change in [lambda f:f['bodies'].pop('collet'),lambda f:f['bodies'].update(fake=f['bodies']['collet']),lambda f:f.update(time=float('nan')),lambda f:f['bodies']['collet'].update(quat=[0,0,0,2])]:
   f=frame();change(f);r=Scorer(SPEC).update(f);self.assertEqual(r.score,0.);self.assertIsNotNone(r.failure)
 def test_fixture_motion_penetration_loss_latch_failure(self):
  for change in [lambda f:f['bodies']['bench_nut']['pos'].__setitem__(0,.25),lambda f:f.update(max_penetration=.001),lambda f:f['bodies']['collet']['pos'].__setitem__(2,.1)]:
   f=frame();change(f);s=Scorer(SPEC);self.assertIsNotNone(s.update(f).failure);_,r=completed(s);self.assertEqual(r.score,0.)
 def test_release_stillness_and_gaps_are_required(self):
  for change in [lambda f:f.update(robot_clearance=0.),lambda f:f['bodies']['collet']['pos'].__setitem__(0,.2405),lambda f:f['bodies']['collet'].update(quat=[math.sin(.01),0,0,math.cos(.01)])]:
   s=Scorer(SPEC);f,_=completed(s);f['time']+=.05;change(f);self.assertFalse(s.update(f).success)
  s=Scorer(SPEC);f,_=completed(s);f['time']+=1.;self.assertFalse(s.update(f).success)
 def test_micron_contact_chatter_does_not_defeat_observable_stability(self):
  s=Scorer(SPEC);f,_=completed(s)
  for i in range(50):
   f['time']+=.05;f['bodies']['collet']['pos'][2]=.8055+(i%2)*.00003
   f['bodies']['collet']['linear']=[0,0,.019 if i%2 else -.019]
   r=s.update(copy.deepcopy(f))
  self.assertTrue(r.success)
 def test_subtolerance_motion_over_the_hold_window_prevents_success(self):
  s=Scorer(SPEC);f,_=completed(s)
  for i in range(60):
   f['time']+=.05;f['bodies']['collet']['pos'][0]=.24+(.00025 if i%2 else -.00025)
   r=s.update(copy.deepcopy(f))
   if i>=1:self.assertFalse(r.success)
 def test_displacement_removes_supported_credit(self):
  s=Scorer(SPEC);f,_=completed(s);f['time']+=.05;f['bodies']['collet']['pos'][0]+=.002;self.assertNotIn('supported_preassembly',s.update(f).completed)
 def test_collet_yaw_is_irrelevant_to_axisymmetric_groove(self):
  s=Scorer(SPEC);f,_=completed(s);f['time']+=.05;f['bodies']['collet']['quat']=[0,0,math.sin(.5),math.cos(.5)];self.assertTrue(s.update(f).success)
 def test_reset_and_duplicate_timestamp_contract(self):
  s=Scorer(SPEC);completed(s);s.reset();f=frame();r=s.update(f);self.assertEqual(r.score,0.);self.assertEqual(s.update(copy.deepcopy(f)),r);f['robot_clearance']=0.;self.assertIsNotNone(s.update(f).failure)
 def test_straight_axial_entry_has_actual_interference(self):
  from audit_geometry import geometry_module
  g=geometry_module(HERE);f=frame()['bodies'];f['collet']['pos']=[.24,0,.8075]
  self.assertGreater(g.maximum_penetration(SPEC,f),SPEC['penetration_limit'])
 def test_offset_upright_entry_is_rejected_across_scoring_envelope(self):
  from audit_geometry import geometry_module
  g=geometry_module(HERE);target=SPEC['score_spec']['target'];states=frame()['bodies']
  # At this unavoidable section of an upright descent, check the accepted
  # lateral disk, including the previously accepted +.599mm negative control.
  offsets=[(.000599,0.)]+[(r*math.cos(a),r*math.sin(a)) for r in (0.,.0003,.0006) for a in np.linspace(0,2*math.pi,17)[:-1]]
  for x,y in offsets:
   states['collet'].update(pos=[target[0]+x,target[1]+y,.8075],quat=[0,0,0,1])
   depth=g.maximum_penetration(SPEC,states)
   self.assertGreater(depth,SPEC['penetration_limit'],(x,y,depth))
  from audit_upright_entry import audit
  self.assertTrue(audit(HERE)['passed'])
  # Real replay boundary: even the most permissive observed former shortcut
  # overlap must fail, without reading controller phases or insertion history.
  judge=Scorer(SPEC);judge.update(frame());f=frame(t=1.)
  f['bodies']['collet'].update(pos=[target[0]+.000599,target[1],.8075],quat=[0,0,0,1])
  f['max_penetration']=g.maximum_penetration(SPEC,f['bodies'])
  self.assertEqual(judge.update(f).failure,'penetration')
 def test_blocked_gripper_reaches_closing_reference_with_bounded_slew(self):
  from motion import Motion
  m=Motion('right');previous=.3
  for _ in range(12):
   command=m.gripper_target(.3,.22)
   self.assertLessEqual(abs(command-previous),.050001);previous=command
  self.assertAlmostEqual(command,.22)
  for _ in range(12):
   command=m.gripper_target(.3,.65)
   self.assertLessEqual(abs(command-previous),.050001);previous=command
  self.assertAlmostEqual(command,.65)
 def test_intended_rock_path_has_no_nominal_intersections(self):
  from audit_geometry import geometry_module
  g=geometry_module(HERE)
  for p in PLAN['phases']:self.assertLess(g.maximum_penetration(SPEC,p['nominal_bodies']),.00001)
 def test_supported_setup_does_not_claim_unsupported_cam_retention(self):
  text=(HERE/'FIDELITY.md').read_text().lower();self.assertIn('not guaranteed',text);self.assertIn('unsupported',text)
  self.assertTrue(SPEC['assemblies'][0]['fixed']);self.assertFalse(SPEC['assemblies'][1]['joints'])
 def test_alternate_valid_entry_angle_is_not_rejected_by_expert_history(self):
  from audit_geometry import geometry_module
  g=geometry_module(HERE);s=Scorer(SPEC);s.update(frame())
  for i,a in enumerate(np.linspace(-.15,0,21)):
   pos,q=hook_pose(float(a));f=frame(t=1.+i*.05);f['bodies']['collet'].update(pos=pos,quat=q)
   self.assertLess(g.maximum_penetration(SPEC,f['bodies']),.00001)
   r=s.update(copy.deepcopy(f))
  for _ in range(41):f['time']+=.05;r=s.update(copy.deepcopy(f))
  self.assertTrue(r.success)
 def test_impossible_single_frame_pose_jump_is_rejected(self):
  s=Scorer(SPEC);s.update(frame());f=frame(PLAN['phases'][-1]['nominal_bodies'],.05)
  self.assertEqual(s.update(f).failure,'unobserved_state_jump')
 def test_composed_usd_mass_and_real_bores(self):
  from verify_assets import verify
  self.assertTrue(verify(HERE)['passed'])
  for a in SPEC['assemblies']:
   for b in a['bodies']:
    self.assertGreater(b['mass'],0);self.assertTrue(all(v>0 for v in b['diagonal_inertia']))
  self.assertFalse(SPEC['collision_exclusions'])
 def test_official_loader_and_expert_binding(self):
  from yam_arena import task_file
  t=task_file.load(HERE/'task.py');task_file.register('er-cpu-contract',t);x=importlib.import_module(t.module._name+'.expert').policy();x.bind(types.SimpleNamespace(environment_id='er-cpu-contract'));
  from unittest.mock import patch
  with tempfile.TemporaryDirectory() as tmp,patch.dict('os.environ',{'ROBOCURVE_TRACE':str(Path(tmp)/'native.jsonl')}):x.reset(None)
  self.assertEqual(x.info.action_space.shape,(14,))
 def test_no_score_reads_or_task_state_writes_in_policy(self):
  for n in ['expert.py','motion.py','feedback.py']:
   attrs={x.attr for x in ast.walk(ast.parse((HERE/n).read_text())) if isinstance(x,ast.Attribute)}
   for forbidden in ['LATEST','EVALUATOR','write_root_pose_to_sim_index','write_joint_position_to_sim_index']:self.assertNotIn(forbidden,attrs)
 def test_native_cases_and_control_prefixes(self):
  d=json.loads((HERE/'native-cases.json').read_text())
  for mode in ('physics','control'):
   self.assertGreaterEqual(len(d[mode]),2)
   for c in d[mode]:self.assertTrue(c['assertions'])
  for c in d['control']:self.assertEqual(PLAN['phases'][c['through_phase']]['label'],c['through_label'])
 def test_unqualified_submission_and_honest_metadata(self):
  from prepare_submission import prepare
  from run_ledger import Incomplete
  with tempfile.TemporaryDirectory() as tmp:
   p=Path(tmp)
   with self.assertRaises(Incomplete):prepare(p,p/'review.json',p/HERE.name)
  d=json.loads((HERE/'task.json').read_text());self.assertLessEqual(len(d['fidelity']),500)
  self.assertEqual(json.loads((HERE/'validation.json').read_text())['native_physics'],'NOT_RUN')
  for t in ['aryansennthilkumar','t-06','/workspace']:self.assertNotIn(t,json.dumps(d).lower())
 def test_bounded_grasp_recovery_and_stale_observation(self):
  p=copy.deepcopy(next(x for x in PLAN['phases'] if x['label']=='Grip collet tapered body'));p['timeout']=.1;c=Controller(dict(phases=[p]),SPEC)
  class Ideal:
   reference=None
   def target(self,q,pos,quat,opening,**kw):return q,0.,0.
  c.motion={s:Ideal() for s in ('left','right')};q=np.zeros(14);q[13]=p['opening'];c.step(q,frame(t=0.));c.step(q,frame(t=.2));self.assertIsNotNone(c.recovery)
  with self.assertRaises(ControlFailure):c.step(q,frame(t=13.))
 def test_actual_media_decode_and_frame_count(self):
  import shutil,subprocess
  from render_media import video_check
  from run_ledger import Incomplete
  ff=shutil.which('ffmpeg');self.assertIsNotNone(ff)
  with tempfile.TemporaryDirectory() as tmp:
   p=Path(tmp);f=p/'synthetic.mp4';subprocess.run([ff,'-v','error','-f','lavfi','-i','testsrc2=size=32x32:rate=20','-frames:v','3','-c:v','libx264','-pix_fmt','yuv420p',str(f)],check=True)
   self.assertEqual(video_check(ff,f,3,p)['decoded_frames'],3)
   with self.assertRaises(Incomplete):video_check(ff,f,4,p)
if __name__=='__main__':unittest.main()
