"""Synthetic CPU contracts/negative controls; no native evidence."""
import ast,copy,importlib,json,math,tempfile,types,unittest
from pathlib import Path
import numpy as np
from generate_scene import make_scene,make_plan
from scoring import Scorer
from feedback import Controller,ControlFailure
HERE=Path(__file__).resolve().parent
SPEC=json.loads((HERE/'scene.json').read_text());PLAN=json.loads((HERE/'controller.json').read_text())

def frame(states=None,t=0.):
 states=states or {b['name']:b for a in SPEC['assemblies'] for b in a['bodies']}
 bodies={n:dict(pos=list(b['pos']),quat=list(b['quat']),linear=[0,0,0],angular=[0,0,0]) for n,b in states.items()}
 q=bodies['release_rail']['pos'][1]-SPEC['score_spec']['rail_origin'][1]
 return dict(schema=1,time=t,bodies=bodies,joints={'rail_flexure':q},max_penetration=0.,robot_clearance=.025)

def completed(s):
 for i,p in enumerate(PLAN['phases']):f=frame(p['nominal_bodies'],i*.2);r=s.update(f)
 for _ in range(41):f['time']+=.05;r=s.update(copy.deepcopy(f))
 return f,r

class Tests(unittest.TestCase):
 def test_generated_scene_plan_are_current(self):self.assertEqual(make_scene(),SPEC);self.assertEqual(make_plan(SPEC),PLAN)
 def test_actual_external_dimensions_are_documented(self):
  self.assertEqual([SPEC['parameters'][n] for n in ['drive_length','drive_width','drive_height']],[.100,.06985,.0068])
 def test_initial_zero_and_real_sequence_fixture_full(self):
  s=Scorer(SPEC);self.assertEqual(s.update(frame()).score,0.);s.reset();_,r=completed(s);self.assertTrue(r.success)
 def test_teleport_to_tray_without_release_has_zero(self):
  f=frame(PLAN['phases'][-1]['nominal_bodies']);self.assertEqual(Scorer(SPEC).update(f).score,0.)
 def test_release_only_does_not_earn_removal(self):
  p=next(x for x in PLAN['phases'] if x['label']=='Pull rail to release two pins');s=Scorer(SPEC);s.update(frame());r=s.update(frame(p['nominal_bodies'],.05));self.assertEqual(r.score,.25);self.assertFalse(r.success)
 def test_alternate_continuous_physical_path_is_not_expert_event_gated(self):
  # The separate geometry tests establish why closed pins obstruct lift. Here
  # the scorer must accept a valid path even when sampled phase boundaries omit
  # the expert's particular 12 mm tilt and 2.5 mm translation events.
  s=Scorer(SPEC);s.update(frame());states=copy.deepcopy(PLAN['phases'][-1]['nominal_bodies'])
  start=np.array(SPEC['score_spec']['initial_drive']);end=np.array(states['drive']['pos'])
  for i in range(1,101):
   f=frame(states,i*.05);f['bodies']['drive']['pos']=(start+(end-start)*i/100).tolist();s.update(f)
  for i in range(42):f['time']+=.05;r=s.update(copy.deepcopy(f))
  self.assertTrue(r.success)
 def test_unobserved_position_replacement_is_rejected(self):
  s=Scorer(SPEC);s.update(frame());f=frame(PLAN['phases'][-1]['nominal_bodies'],.05)
  self.assertEqual(s.update(f).failure,'unobserved_state_jump')
 def test_held_rail_and_robot_contact_prevent_full(self):
  s=Scorer(SPEC);f,r=completed(s);f['time']+=.05;f['joints']['rail_flexure']=.006;f['bodies']['release_rail']['pos'][1]=.006
  self.assertLess(s.update(copy.deepcopy(f)).score,1.)
  s=Scorer(SPEC);f,_=completed(s);f['time']+=.05;f['robot_clearance']=0.;self.assertFalse(s.update(f).success)
 def test_disturbing_staged_drive_removes_score(self):
  s=Scorer(SPEC);f,_=completed(s);f['time']+=.05;f['bodies']['drive']['pos'][0]+=.01
  self.assertNotIn('drive_staged',s.update(f).completed)
 def test_tamper_loss_penetration_bad_quat_latch_zero(self):
  for change in [lambda f:f['bodies']['bracket']['pos'].__setitem__(0,.3),lambda f:f['bodies']['drive']['pos'].__setitem__(2,.1),lambda f:f.update(max_penetration=.001),lambda f:f['bodies']['drive'].update(quat=[0,0,0,2])]:
   s=Scorer(SPEC);f=frame();change(f);self.assertIsNotNone(s.update(f).failure);_,r=completed(s);self.assertEqual(r.score,0.)
 def test_joint_mismatch_and_overlimit_fail(self):
  for value in (.006,.010):
   f=frame();f['joints']['rail_flexure']=value;self.assertIsNotNone(Scorer(SPEC).update(f).failure)
 def test_missing_extra_nan_and_stale_frames_fail(self):
  for change in [lambda f:f['bodies'].pop('drive'),lambda f:f.update(time=float('nan')),lambda f:f['joints'].update(fake=0)]:
   f=frame();change(f);self.assertIsNotNone(Scorer(SPEC).update(f).failure)
  s=Scorer(SPEC);f=frame();r=s.update(f);self.assertEqual(s.update(copy.deepcopy(f)),r);f['robot_clearance']=0.;self.assertIsNotNone(s.update(f).failure)
 def test_reset_clears_physical_history(self):
  s=Scorer(SPEC);completed(s);s.reset();self.assertEqual(s.update(frame()).score,0.);self.assertFalse(s.withdrawn)
 def test_usd_assets_actual_joints_and_mass(self):
  from verify_assets import verify
  from pxr import Usd,UsdPhysics
  self.assertTrue(verify(HERE)['passed']);st=Usd.Stage.Open(str(HERE/'assets/bracket_asset.usda'));j=UsdPhysics.PrismaticJoint(st.GetPrimAtPath('/Asset/rail_flexure'))
  self.assertAlmostEqual(j.GetUpperLimitAttr().Get(),.007);self.assertEqual(j.GetAxisAttr().Get(),'Y')
 def test_retaining_pins_block_straight_lift_without_rail_release(self):
  from audit_geometry import geometry_module
  g=geometry_module(HERE);f=frame()['bodies'];f['drive']['pos'][2]+=.002
  self.assertGreater(g.maximum_penetration(SPEC,f),SPEC['penetration_limit'])
 def test_nominal_removal_phases_have_no_hidden_intersection(self):
  from audit_geometry import geometry_module
  g=geometry_module(HERE)
  for p in PLAN['phases']:self.assertLessEqual(g.maximum_penetration(SPEC,p['nominal_bodies']),SPEC['penetration_limit'])
 def test_all_body_masses_inertia_positive_and_drive_never_attached(self):
  for a in SPEC['assemblies']:
   for b in a['bodies']:
    self.assertGreater(b['mass'],0);self.assertTrue(all(v>0 for v in b['diagonal_inertia']))
   for j in a['joints']:self.assertNotIn('drive',(j['parent'],j['child']))
  self.assertFalse(SPEC['collision_exclusions'])
 def test_official_task_loader_and_expert_bind(self):
  from yam_arena import task_file
  t=task_file.load(HERE/'task.py');task_file.register('drive-offline-contract',t)
  x=importlib.import_module(t.module._name+'.expert').policy();x.bind(types.SimpleNamespace(environment_id='drive-offline-contract'));x.reset(None)
  self.assertEqual(x.info.action_space.shape,(14,))
 def test_policy_no_native_object_reads_or_state_writes(self):
  for name in ('expert.py','feedback.py','motion.py'):
   attrs={x.attr for x in ast.walk(ast.parse((HERE/name).read_text())) if isinstance(x,ast.Attribute)}
   for forbidden in ('LATEST','EVALUATOR','write_root_pose_to_sim_index','write_joint_position_to_sim_index'):self.assertNotIn(forbidden,attrs)
 def test_native_cases_assertions_and_control_prefixes(self):
  d=json.loads((HERE/'native-cases.json').read_text())
  for mode in ('physics','control'):
   self.assertGreaterEqual(len(d[mode]),2)
   for c in d[mode]:self.assertTrue(c['assertions'])
  for c in d['control']:self.assertEqual(PLAN['phases'][c['through_phase']]['label'],c['through_label'])
 def test_submission_guard_rejects_unrun_native_qualification(self):
  from prepare_submission import prepare
  from run_ledger import Incomplete
  with tempfile.TemporaryDirectory() as tmp:
   p=Path(tmp)
   with self.assertRaises(Incomplete):prepare(p,p/'review.json',p/HERE.name)
 def test_honest_blind_metadata(self):
  t=json.loads((HERE/'task.json').read_text());self.assertLessEqual(len(t['fidelity']),500)
  for term in ('aryansennthilkumar','t-06','/workspace'):self.assertNotIn(term,json.dumps(t).lower())
  self.assertEqual(json.loads((HERE/'validation.json').read_text())['native_physics'],'NOT_RUN')
 def test_controller_stale_and_air_grasp_recovery(self):
  p=next(x for x in PLAN['phases'] if x['label']=='Grip drive case across its width');p=copy.deepcopy(p);p['timeout']=.1
  c=Controller(dict(phases=[p]),SPEC)
  class Ideal:
   reference=None
   def target(self,q,pos,quat,opening,**kw):return q,0.,0.
  c.motion={s:Ideal() for s in ('left','right')};q=np.zeros(14);q[13]=p['opening'];c.step(q,{'time':0.});c.step(q,{'time':.2});self.assertIsNotNone(c.recovery);self.assertGreater(c.recovery['phase']['opening'],SPEC['parameters']['drive_width']/.0939)
  with self.assertRaises(ControlFailure):c.step(q,{'time':13.})
 def test_wide_grasp_recovery_opens_then_can_reacquire(self):
  p=copy.deepcopy(next(x for x in PLAN['phases'] if x['label']=='Grip drive case across its width'));p['timeout']=.1
  c=Controller(dict(phases=[p]),SPEC)
  class Ideal:
   reference=None
   def target(self,q,pos,quat,opening,**kw):return q,0.,0.
  c.motion={s:Ideal() for s in ('left','right')};q=np.zeros(14);q[13]=p['opening']
  c.step(q,{'time':0.});c.step(q,{'time':.2});q[13]=c.recovery['phase']['opening']
  for i in range(8):c.step(q,{'time':.25+i*.05})
  self.assertIsNone(c.recovery)
  p['timeout']=2. # restore an acquisition timeout longer than its dwell
  q[13]=p['grasp_width']/.0939
  for i in range(15):
   c.step(q,{'time':.65+i*.05})
   if c.done:break
  self.assertTrue(c.done)
 def test_media_fixture_codec_and_frame_count(self):
  import shutil,subprocess
  from render_media import video_check
  from run_ledger import Incomplete
  ff=shutil.which('ffmpeg');self.assertIsNotNone(ff)
  with tempfile.TemporaryDirectory() as tmp:
   p=Path(tmp);f=p/'synthetic.mp4';subprocess.run([ff,'-v','error','-f','lavfi','-i','testsrc2=size=32x32:rate=20','-frames:v','3','-c:v','libx264','-pix_fmt','yuv420p',str(f)],check=True)
   self.assertEqual(video_check(ff,f,3,p)['decoded_frames'],3)
   with self.assertRaises(Incomplete):video_check(ff,f,4,p)
if __name__=='__main__':unittest.main()
