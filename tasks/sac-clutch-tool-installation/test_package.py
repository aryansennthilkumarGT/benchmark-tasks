"""Package contracts and adversarial fixtures; no native physics claims."""
import ast
import copy
import importlib
import json
import math
from pathlib import Path
import tempfile
import types
import unittest
import numpy as np
from dimensions import validated
from feedback import Controller,ControlFailure
from generate_scene import make_scene,make_plan
from mounting_score import Scorer

HERE=Path(__file__).resolve().parent
SPEC=json.loads((HERE/'scene.json').read_text());PLAN=json.loads((HERE/'controller.json').read_text())


def initial_frame():
    return dict(schema=1,time=0.,bodies={b['name']:dict(pos=b['pos'].copy(),quat=b['quat'].copy(),linear=[0.,0.,0.],angular=[0.,0.,0.]) for a in SPEC['assemblies'] for b in a['bodies']},robot_clearance=.025,max_penetration=0.)


def complete(scorer):
    f=initial_frame();ss=SPEC['score_spec'];f['bodies']['carrier']['pos']=[.24,0,ss['carrier_seat_z']]
    for i,name in enumerate(ss['retainers']):
        for k in range(129):
            turns=4*k/128;a=-2*math.pi*turns
            f['time']+=.05
            f['bodies'][name].update(pos=[*ss['studs'][i]['axis_xy'],ss['studs'][i]['tip_z']+.006-turns*ss['pitch']],quat=[0,0,math.sin(a/2),math.cos(a/2)])
            r=scorer.update(copy.deepcopy(f))
    for _ in range(41):f['time']+=.05;r=scorer.update(copy.deepcopy(f))
    return f,r


class PackageTests(unittest.TestCase):
    def test_reproducible_scene_and_plan(self):
        self.assertEqual(make_scene(),SPEC);self.assertEqual(make_plan(SPEC),PLAN)

    def test_authored_profile_is_explicit_and_strict(self):
        profile=json.loads((HERE/'fixture-profile.json').read_text())
        self.assertEqual(profile['geometry_mode'],'BENCHMARK_AUTHORED')
        self.assertEqual(validated(profile),SPEC['parameters'])
        for kind in ['physical_measurement','manufacturer_dimensioned_document']:
            # Merely changing the mode must not relabel authored data as real.
            wrong=copy.deepcopy(profile);wrong['geometry_mode']='MEASURED_HARDWARE'
            with self.assertRaises(ValueError):validated(wrong)
        wrong=copy.deepcopy(profile);del wrong['authorship_disclosure']
        with self.assertRaises(ValueError):validated(wrong)
        wrong=copy.deepcopy(profile);wrong['measurements']['retainer_mass'].update(kind='physical_measurement')
        with self.assertRaisesRegex(ValueError,'evidence'):validated(wrong)

    def test_upper_and_flywheel_thread_specifications_are_independent(self):
        self.assertEqual(SPEC['parameters']['flywheel_thread_pitch'],.00125)
        self.assertEqual(SPEC['parameters']['retainer_thread_pitch'],.003)
        self.assertEqual(SPEC['parameters']['retainer_thread_major'],.012)

    def test_positive_physical_bodies_no_hidden_joints_or_exclusions(self):
        self.assertEqual(len(SPEC['assemblies']),7);self.assertFalse(SPEC['collision_exclusions'])
        for a in SPEC['assemblies']:
            self.assertFalse(a['joints'])
            for b in a['bodies']:
                self.assertGreater(b['mass'],0);self.assertTrue(all(v>0 for v in b['diagonal_inertia']))
        self.assertEqual({b['name'] for a in SPEC['assemblies'] for b in a['bodies'] if not b['anchor']},{'carrier','nut0','nut1','nut2'})

    def test_three_slots_and_mandrel_have_positive_design_clearance(self):
        d=SPEC['parameters']
        self.assertGreater(d['carrier_slot_width']-d['retainer_thread_major'],.001)
        self.assertGreater(d['retracted_spindle_inner_bore']-d['centring_tool_outer_diameter'],.003)
        self.assertEqual(SPEC['score_spec']['retainer_top_offset'],d['retainer_height']/2)

    def test_mismatched_thread_phase_has_actual_collision(self):
        from audit_geometry import geometry_module
        g=geometry_module(HERE);f=initial_frame()['bodies'];ss=SPEC['score_spec']
        f['carrier']['pos']=[.24,0,ss['carrier_seat_z']]
        f['nut0']['pos']=[*ss['studs'][0]['axis_xy'],ss['studs'][0]['tip_z']-.006+ss['pitch']/2]
        self.assertGreater(g.maximum_penetration(SPEC,f),SPEC['penetration_limit'])

    def test_inconsistent_absolute_thread_phase_cannot_earn_credit(self):
        ss=copy.deepcopy(SPEC['score_spec'])
        for stud in ss['studs']:stud['entry_yaw']=math.pi
        _,result=complete(Scorer(ss))
        self.assertEqual(result.secured_studs,());self.assertFalse(result.success)

    def test_initial_score_zero_and_sequential_retention_full(self):
        s=Scorer(SPEC['score_spec']);self.assertEqual(s.update(initial_frame()).score,0.)
        s.reset();f,r=complete(s);self.assertTrue(r.success);self.assertEqual(r.score,1.)
        self.assertEqual(r.secured_studs,(0,1,2))

    def test_reset_erases_credit_and_latched_failure(self):
        s=Scorer(SPEC['score_spec']);_,r=complete(s);self.assertTrue(r.success)
        s.reset();self.assertEqual(s.update(initial_frame()).score,0.)
        f=initial_frame();f['time']=.05;f['max_penetration']=.1;self.assertIsNotNone(s.update(f).failure)
        s.reset();self.assertIsNone(s.update(initial_frame()).failure)

    def test_rotated_fixture_cannot_earn_partial_credit(self):
        f=initial_frame();f['bodies']['fixture']['quat']=[0,0,math.sin(.05),math.cos(.05)]
        self.assertEqual(Scorer(SPEC['score_spec']).update(f).score,0.)

    def test_overspeed_and_hand_contact_prevent_full_score(self):
        for field in ('linear','angular'):
            s=Scorer(SPEC['score_spec']);f,_=complete(s);f['time']+=.05;f['bodies']['carrier'][field]=[1.,0.,0.]
            self.assertFalse(s.update(f).success)
        s=Scorer(SPEC['score_spec']);f,_=complete(s);f['time']+=.05;f['robot_clearance']=0.
        self.assertFalse(s.update(f).success)

    def test_nonfinite_quaternion_and_time_fail_closed(self):
        for mutation in [lambda f:f.update(time=float('inf')),lambda f:f['bodies']['nut0'].update(quat=[0,0,0,2])]:
            f=initial_frame();mutation(f);self.assertEqual(Scorer(SPEC['score_spec']).update(f).score,0.)

    def test_all_assets_compose_and_have_expected_colliders(self):
        from verify_assets import verify
        self.assertTrue(verify(HERE)['passed'])

    def test_official_loader_and_expert_bind_without_isaac(self):
        from yam_arena import task_file
        task=task_file.load(HERE/'task.py');task_file.register('sac-offline-contract',task)
        expert=importlib.import_module(task.module._name+'.expert').policy()
        expert.bind(types.SimpleNamespace(environment_id='sac-offline-contract'));expert.reset(None)
        self.assertEqual(expert.info.action_space.shape,(14,));self.assertEqual(len(expert.controller.phases),len(PLAN['phases']))
        self.assertEqual(task.score({}),0.)

    def test_native_prefixes_and_diagnostics_have_assertions(self):
        cases=json.loads((HERE/'native-cases.json').read_text())
        for mode in ('physics','control'):
            self.assertGreaterEqual(len(cases[mode]),2)
            self.assertEqual(len({x['name'] for x in cases[mode]}),len(cases[mode]))
            for c in cases[mode]:self.assertTrue(c['assertions'])
        for c in cases['control']:self.assertEqual(PLAN['phases'][c['through_phase']]['label'],c['through_label'])

    def test_policy_has_no_object_reads_or_state_write_paths(self):
        for name in ('expert.py','feedback.py','motion.py'):
            tree=ast.parse((HERE/name).read_text());attrs={x.attr for x in ast.walk(tree) if isinstance(x,ast.Attribute)}
            for forbidden in ('LATEST','EVALUATOR','write_root_pose_to_sim_index','write_joint_position_to_sim_index','set_world_pose'):
                self.assertNotIn(forbidden,attrs)

    def test_unqualified_submission_is_rejected(self):
        from prepare_submission import prepare
        from run_ledger import Incomplete
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)
            with self.assertRaisesRegex(Incomplete,'qualification required'):prepare(p,p/'review.json',p/HERE.name)
            self.assertFalse((p/HERE.name).exists())

    def test_blind_metadata_and_honest_validation(self):
        t=json.loads((HERE/'task.json').read_text());v=json.loads((HERE/'validation.json').read_text())
        self.assertLessEqual(len(t['fidelity']),500);self.assertLessEqual(len(t['setup']),4000)
        for term in ('aryansennthilkumar','t-06','/workspace','/data/'):
            self.assertNotIn(term,json.dumps(t).lower())
        self.assertEqual(v['native_physics'],'NOT_RUN');self.assertEqual(v['dream_1'],'NOT_RUN')
        self.assertIn('not run',t['scores'].lower())

    def test_real_ffmpeg_decode_and_bad_frame_count_rejection(self):
        import shutil,subprocess
        from render_media import video_check
        from run_ledger import Incomplete
        executable=shutil.which('ffmpeg');self.assertIsNotNone(executable)
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);video=p/'synthetic-codec-fixture.mp4'
            subprocess.run([executable,'-v','error','-f','lavfi','-i','testsrc2=size=32x32:rate=20','-frames:v','3','-c:v','libx264','-pix_fmt','yuv420p',str(video)],check=True)
            self.assertEqual(video_check(executable,video,3,p)['decoded_frames'],3)
            with self.assertRaises(Incomplete):video_check(executable,video,4,p)


class ControllerTests(unittest.TestCase):
    class Ideal:
        reference=None
        def target(self,q,pos,quat,opening,**kwargs):return np.r_[q[:6],opening],0.,0.

    def test_sequence_exhausts_all_sac_phases_with_synthetic_feedback(self):
        c=Controller(PLAN,SPEC);c.motion={s:self.Ideal() for s in ('left','right')};q=np.zeros(14)
        for step in range(12000):
            for side,p in c.targets.items():q[(0 if side=='left' else 7)+6]=p['grasp_width']/.0939 if p['opening']<.3 else p['opening']
            c.step(q,{'time':step*.05})
            if c.done:break
        self.assertTrue(c.done);self.assertEqual(len([e for e in c.events if e['event']=='PROPRIOCEPTIVE_PHASE_COMPLETE']),len(PLAN['phases']))

    def test_air_grasp_recovery_is_bounded_and_explicit(self):
        phase=copy.deepcopy(PLAN['phases'][2]);phase['timeout']=.10
        c=Controller(dict(phases=[phase]),SPEC);c.motion={s:self.Ideal() for s in ('left','right')};q=np.zeros(14);q[6]=phase['opening']
        c.step(q,{'time':0.});c.step(q,{'time':.2})
        self.assertEqual(c.recovery['kind'],'REOPEN_AND_REACQUIRE')
        with self.assertRaisesRegex(ControlFailure,'Recovery timeout'):c.step(q,{'time':13.})

    def test_thread_recovery_reverses_exactly_one_increment(self):
        p=next(p for p in PLAN['phases'] if p['label'].startswith('Thread'))
        c=Controller(dict(phases=[p]),SPEC);c.last_time=0.;c.begin_recovery(p,0.)
        self.assertAlmostEqual(c.recovery['phase']['target']['pos'][2]-p['target']['pos'][2],.003/8)
        c.begin_recovery(p,1.)
        with self.assertRaisesRegex(ControlFailure,'exhausted'):c.begin_recovery(p,2.)

    def test_invalid_and_stale_robot_observations_fail(self):
        c=Controller(PLAN,SPEC)
        with self.assertRaises(ControlFailure):c.step([float('nan')]*14,{'time':0.})
        c.motion={s:self.Ideal() for s in ('left','right')};c.step(np.ones(14),{'time':0.})
        with self.assertRaises(ControlFailure):c.step(np.ones(14),{'time':0.})


if __name__=='__main__':unittest.main()
