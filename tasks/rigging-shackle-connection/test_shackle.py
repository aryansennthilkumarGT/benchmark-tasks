"""Deterministic synthetic scorer/contract tests, not native physics evidence."""
import ast
import copy
import importlib
import json
import math
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import patch
import numpy as np

from scoring import Scorer
from feedback import Controller, ControlFailure
from generate_scene import CENTER, PITCH, SEAT, TURNS, make_scene

HERE=Path(__file__).resolve().parent
SPEC=json.loads((HERE/'scene.json').read_text())
PLAN=json.loads((HERE/'controller.json').read_text())


def frame(time=0.):
    return dict(schema=1,time=time,bodies={b['name']:dict(pos=list(b['pos']),quat=list(b['quat']),
        linear=[0,0,0],angular=[0,0,0]) for a in SPEC['assemblies'] for b in a['bodies']},
        joints={},robot_clearance=.04,max_penetration=0.)


def helical(scorer, spinning_only=False, lateral=.0):
    f=frame();f['bodies']['shackle']['pos']=CENTER.copy()
    start=CENTER[2]+SEAT+TURNS*PITCH
    for i in range(481):
        turns=TURNS*i/480
        f['time']=i*.05
        f['bodies']['pin'].update(pos=[CENTER[0]+lateral,0,start-(0 if spinning_only else turns*PITCH)],
            quat=[0,0,math.sin(-math.pi*turns),math.cos(-math.pi*turns)])
        result=scorer.update(copy.deepcopy(f))
    return f,result


class ScoringTests(unittest.TestCase):
    def test_initial_score_zero(self):
        self.assertEqual(Scorer(SPEC).update(frame()).score,0.)

    def test_pitch_coupled_connection_requires_stability_and_release(self):
        s=Scorer(SPEC);f,r=helical(s)
        self.assertFalse(r.success);self.assertLess(r.score,1.)
        for _ in range(41):f['time']+=.05;r=s.update(copy.deepcopy(f))
        self.assertTrue(r.success);self.assertEqual(r.score,1.)
        f['time']+=.05;f['robot_clearance']=.001
        self.assertFalse(s.update(f).success)

    def test_free_spin_and_wrong_axis_cannot_earn_thread_credit(self):
        for spin,offset in ((True,0.),(False,.004)):
            s=Scorer(SPEC);_,r=helical(s,spin,offset)
            self.assertNotIn('collar_seated',r.completed);self.assertLessEqual(r.score,.2)

    def test_teleported_final_pose_cannot_replace_turn_history(self):
        s=Scorer(SPEC);f=frame();f['bodies']['shackle']['pos']=CENTER.copy()
        f['bodies']['pin']['pos']=[CENTER[0],0,CENTER[2]+SEAT]
        for i in range(50):f['time']=i*.05;r=s.update(copy.deepcopy(f))
        self.assertFalse(r.success);self.assertNotIn('pin_through_lug',r.completed)

    def test_tampered_fixtures_nan_and_contact_violation_latch_zero(self):
        mutations=[lambda f:f['bodies']['lifting_lug']['pos'].__setitem__(0,CENTER[0]+.01),
                   lambda f:f['bodies']['pin']['pos'].__setitem__(0,float('nan')),
                   lambda f:f.update(max_penetration=.002)]
        for change in mutations:
            s=Scorer(SPEC);f=frame();change(f);r=s.update(f)
            self.assertEqual(r.score,0.);self.assertIsNotNone(r.failure)
            _,r=helical(s);self.assertEqual(r.score,0.)

    def test_missing_body_and_undersampled_rotation_are_rejected(self):
        f=frame();del f['bodies']['pin']
        self.assertIsNotNone(Scorer(SPEC).update(f).failure)
        s=Scorer(SPEC);f=frame();f['bodies']['shackle']['pos']=CENTER.copy()
        f['bodies']['pin']['pos']=[CENTER[0],0,CENTER[2]+SEAT+TURNS*PITCH]
        s.update(copy.deepcopy(f));f['time']=.05;f['bodies']['pin']['quat']=[0,0,1.,0]
        self.assertIn('undersampled',s.update(f).failure)

    def test_duplicate_frame_is_idempotent_but_conflict_invalid(self):
        s=Scorer(SPEC);f=frame();r=s.update(f)
        self.assertEqual(s.update(copy.deepcopy(f)),r)
        f['robot_clearance']=.03
        self.assertIsNotNone(s.update(f).failure)

    def test_backing_pin_out_loses_seating_credit(self):
        s=Scorer(SPEC);f,r=helical(s)
        f['time']+=.05;f['bodies']['pin']['pos'][2]+=.005
        r=s.update(f);self.assertNotIn('collar_seated',r.completed)


class Contracts(unittest.TestCase):
    def test_media_verifier_decodes_real_fixture_and_rejects_frame_mismatch(self):
        import tempfile,subprocess,shutil
        from render_media import video_check
        from run_ledger import Incomplete
        executable=shutil.which('ffmpeg')
        self.assertIsNotNone(executable,'FFmpeg is required for offline media verification')
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);video=root/'synthetic-codec-fixture.mp4'
            subprocess.run([executable,'-v','error','-f','lavfi','-i','testsrc2=size=32x32:rate=20',
                '-frames:v','3','-c:v','libx264','-pix_fmt','yuv420p',str(video)],check=True)
            self.assertEqual(video_check(executable,video,3,root)['decoded_frames'],3)
            with self.assertRaisesRegex(Incomplete,'frame count'):
                video_check(executable,video,4,root)

    def test_official_loader_and_expert_binding_are_self_contained(self):
        from yam_arena import task_file
        task=task_file.load(HERE/'task.py')
        task_file.register('shackle-offline-contract',task)
        module=importlib.import_module(task.module._name+'.expert')
        expert=module.policy();expert.bind(types.SimpleNamespace(environment_id='shackle-offline-contract'))
        expert.reset(None)
        self.assertEqual(expert.info.action_space.shape,(14,))
        self.assertEqual(len(expert.controller.phases),len(PLAN['phases']))
        self.assertFalse(task.success({}));self.assertEqual(task.score({}),0.)

    def test_pin_bore_has_no_hidden_obstruction_at_entry_or_seating(self):
        from audit_geometry import geometry_module
        g=geometry_module(HERE)
        states={b['name']:copy.deepcopy(b) for a in SPEC['assemblies'] for b in a['bodies']}
        states['shackle']['pos']=CENTER.copy()
        for h in [SEAT,SEAT+TURNS*PITCH]:
            states['pin']['pos']=[CENTER[0],0,CENTER[2]+h]
            self.assertLess(g.maximum_penetration(SPEC,states),.00003)

    def test_submission_preparation_refuses_unexecuted_qualification(self):
        import tempfile
        from prepare_submission import prepare
        from run_ledger import Incomplete
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)
            with self.assertRaisesRegex(Incomplete,'qualification required'):
                prepare(p,p/'review.json',p/HERE.name)
            self.assertFalse((p/HERE.name).exists())

    def test_source_dimensions_and_mass_match_published_nominal_envelope(self):
        g=SPEC['geometry_parameters']
        self.assertAlmostEqual(g['pitch'],.0254/10)
        self.assertEqual(g['inside_gap'],.027);self.assertEqual(g['eye_diameter'],.040)
        masses={b['name']:b['mass'] for a in SPEC['assemblies'] for b in a['bodies']}
        self.assertAlmostEqual(masses['pin']+masses['shackle'],.63)
        self.assertEqual(make_scene(),SPEC)

    def test_all_bodies_have_positive_inertia_and_no_hidden_attachments(self):
        for a in SPEC['assemblies']:
            self.assertFalse(a['joints'])
            for b in a['bodies']:
                self.assertGreater(b['mass'],0)
                self.assertTrue(all(x>0 for x in b['diagonal_inertia']))
        self.assertFalse(SPEC['collision_exclusions'])

    def test_metadata_limits_and_blind_review(self):
        task=json.loads((HERE/'task.json').read_text())
        self.assertLessEqual(len(task['fidelity']),500);self.assertLessEqual(len(task['setup']),4000)
        text=json.dumps(task).lower()
        for identity in ['doubling time','t-06','aryansennthilkumar','/workspace','/data/']:
            self.assertNotIn(identity,text)

    def test_usd_geometry_and_collision_bores_exist(self):
        from pxr import Usd,UsdPhysics
        for a in SPEC['assemblies']:
            stage=Usd.Stage.Open(str(HERE/'assets'/(a['name']+'.usda')))
            self.assertIsNotNone(stage)
            b=a['bodies'][0]
            self.assertTrue(stage.GetPrimAtPath('/Asset/'+b['name']).HasAPI(UsdPhysics.RigidBodyAPI))
            self.assertEqual(sum(p.HasAPI(UsdPhysics.CollisionAPI) for p in stage.Traverse()),len(b['shapes']))

    def test_native_cases_nonempty_and_control_prefixes_current(self):
        cases=json.loads((HERE/'native-cases.json').read_text())
        for mode in ['physics','control']:
            self.assertGreaterEqual(len(cases[mode]),2)
            self.assertEqual(len(cases[mode]),len({x['name'] for x in cases[mode]}))
            for c in cases[mode]:self.assertTrue(c['assertions'])
        for c in cases['control']:
            self.assertEqual(PLAN['phases'][c['through_phase']]['label'],c['through_label'])

    def test_expert_does_not_read_native_object_state_or_scorer(self):
        for file in ['expert.py','feedback.py']:
            tree=ast.parse((HERE/file).read_text())
            names={n.attr for n in ast.walk(tree) if isinstance(n,ast.Attribute)}
            for forbidden in ['LATEST','EVALUATOR','write_root_pose_to_sim_index','write_joint_position_to_sim_index']:
                self.assertNotIn(forbidden,names)


class ControllerTests(unittest.TestCase):
    def test_invalid_or_stale_proprioception_fails(self):
        c=Controller(PLAN,SPEC)
        with self.assertRaises(ControlFailure):c.step([float('nan')]*14,{'time':0.})
        q=np.tile([0.,1.,1.,-.6,0.,0.,1.],2)
        c.step(q,{'time':0.})
        with self.assertRaises(ControlFailure):c.step(q,{'time':0.})

    def test_all_authored_phases_run_to_completion_under_tracking_fixture(self):
        # This tests sequencing and bounds only. It explicitly supplies ideal
        # kinematic tracking/contact apertures; it is not a grasp/physics test.
        class IdealMotion:
            reference=None
            def target(self,q,pos,quat,opening,**kwargs):return np.r_[q[:6],opening],0.,0.
        c=Controller(PLAN,SPEC);c.motion={s:IdealMotion() for s in ('left','right')}
        q=np.zeros(14);t=0.
        for _ in range(16000):
            if c.done:break
            for side,p in c.targets.items():q[(0 if side=='left' else 7)+6]=p['opening']+(.02 if p['opening']<.3 else 0.)
            c.step(q,{'time':t});t+=.05
        self.assertTrue(c.done)
        self.assertEqual(sum(e['event']=='PROPRIOCEPTIVE_PHASE_COMPLETE' for e in c.events),len(PLAN['phases']))

    def test_no_grasp_and_stall_have_bounded_failures(self):
        p=copy.deepcopy(PLAN['phases'][2]);p['timeout']=.2
        c=Controller({'phases':[p]},SPEC)
        class AtTarget:
            reference=None
            def target(self,q,pos,quat,opening,**kwargs):return q,0.,0.
        c.motion={s:AtTarget() for s in ('left','right')}
        q=np.zeros(14);q[6]=p['opening'] # fully closed in air, not contact
        c.step(q,{'time':0.})
        with self.assertRaisesRegex(ControlFailure,'timeout'):c.step(q,{'time':.25})


if __name__=='__main__':unittest.main()
