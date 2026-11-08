"""Real temporary Git/process integration, using labelled nonphysics fixture tasks."""
import contextlib
import copy
import io
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import pipeline
from engine import Incomplete,atomic,read
from review_media import FILES,CHECKS,verify_review

class PipelineIntegration(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name);self.repo=self.root/'fixture-source';self.repo.mkdir()
        self.git('init');self.git('config','user.name','Fixture');self.git('config','user.email','fixture@example.invalid')
        (self.repo/'baseline.txt').write_text('Orchestrator fixture. Not a simulation.\n');self.git('add','.');self.git('commit','-m','Fixture baseline')
        self.base=self.git('rev-parse','HEAD');self.tasks=[]
        for n in range(8):
            slug=f'fixture-{n}';self.git('checkout','--detach',self.base);self.git('checkout','-b','draft/'+slug)
            f=self.repo/'tasks'/slug;f.mkdir(parents=True)
            for name in ['task.py','scoring.py','run.py','expert.py','native_tests.py','test_scoring.py','test_control.py']:
                (f/name).write_text('"""Nonphysics orchestration fixture."""\n')
            for name in ['verify_assets.py','audit_control.py','audit_geometry.py','audit_grasps.py','audit_motion.py','audit_threads.py']:
                (f/name).write_text('print("ORCHESTRATION_FIXTURE_NOT_PHYSICS")\n')
            (f/'test_scoring.py').write_text('import unittest\nclass Fixture(unittest.TestCase):\n def test_labelled_fixture(self):self.assertTrue(True) # subprocess orchestration only\n')
            if n==2:(f/'test_control.py').write_text('import unittest\nclass Failure(unittest.TestCase):\n def test_intentional_failure(self):self.fail("intentional task 3 fixture failure")\n')
            for name in ['scene.json','controller.json']:atomic(f/name,{})
            atomic(f/'source_manifest.json',{'files':{'task.py':__import__('hashlib').sha256((f/'task.py').read_bytes().replace(b'\r\n',b'\n')).hexdigest()}})
            atomic(f/'mechanics-review.json',{'implementation_review':'COMPLETE','unimplemented_mechanics':[],'physical_validation':'PENDING_NATIVE_TESTS'})
            atomic(f/'task.json',dict(title='Nonphysics fixture',category='Other',instruction='Fixture only',setup='No physical scene',scoring='Fixture only',run_limit='0',fidelity='No simulation',scores='NOT RUN',media=''))
            (f/'README.md').write_text('This fixture tests orchestration only.')
            self.git('add','.');self.git('commit','-m',slug)
            self.tasks.append(dict(slug=slug,branch='draft/'+slug,task_folder='tasks/'+slug,commit=self.git('rev-parse','HEAD')))
        self.manifest=self.root/'manifest.json';atomic(self.manifest,{'tasks':self.tasks});self.runs=self.root/'runs'
    def tearDown(self):self.tmp.cleanup()
    def git(self,*args):
        return subprocess.run(['git',*args],cwd=self.repo,capture_output=True,text=True,check=True).stdout.strip()
    def run_pipeline(self,*extra):
        with patch.object(pipeline,'FORK',str(self.repo)),patch.object(pipeline,'BASELINE',self.base),contextlib.redirect_stdout(io.StringIO()):
            return pipeline.main(['--offline','--manifest',str(self.manifest),'--run-root',str(self.runs),*extra])
    def test_real_checkout_failure_preservation_resume_and_fixed_revision(self):
        self.assertEqual(self.run_pipeline('--all'),2)
        report=read(self.runs/'report.json');self.assertEqual(sum(t['status']=='STATIC_TESTS_PASSED' for t in report['tasks']),7)
        self.assertFalse(report['complete']);self.assertEqual(read(self.runs/'ready-handoff.json')['tasks'],[])
        before=read(self.runs/'ledger.json')['tasks']['fixture-0']
        self.assertEqual(self.run_pipeline('--all','--resume'),2)
        self.assertEqual(before,read(self.runs/'ledger.json')['tasks']['fixture-0'])
        self.git('checkout','draft/fixture-2');(self.repo/'tasks/fixture-2/test_control.py').write_text('"""Fixed orchestration fixture; no physics."""\n')
        self.git('add','.');self.git('commit','-m','Fix intentional fixture failure')
        self.tasks[2]['commit']=self.git('rev-parse','HEAD');atomic(self.manifest,{'tasks':self.tasks})
        self.assertEqual(self.run_pipeline('--all','--resume'),0)
        self.assertTrue(read(self.runs/'report.json')['offline_checks_passed'])
        self.assertFalse(read(self.runs/'report.json')['complete'])
    def test_dirty_worktree_is_rejected(self):
        self.assertEqual(self.run_pipeline('--task','fixture-0'),0)
        tree=self.runs/'worktrees/fixture-0'/self.tasks[0]['commit'];(tree/'tasks/fixture-0/task.py').write_text('# changed\n')
        self.assertEqual(self.run_pipeline('--task','fixture-0','--resume'),2)
        self.assertIn('dirty',read(self.runs/'report.json')['tasks'][0]['error'])

class NativeCoverageTests(unittest.TestCase):
    def test_publication_replaces_pending_fields_without_private_paths(self):
        old=dict(native_physics='NOT_RUN',robot_control='NOT_RUN',physics_runs=0,expert_runs=0,model_runs=0,media_uploads=0,media_verified=False)
        run=dict(score=1.,mode='expert',record_id='FORMAT-FIXTURE',log='/private/source/log.json',frames='/private/frames')
        value=pipeline.publication_record(old,{'experts':[run,run],'dream':dict(run,score=0.,mode='dream')},
             {'NATIVE_PHYSICS_PASSED':{'result':{'reset_count':8}},'ROBOT_CONTROL_PASSED':{'result':{'reset_count':4}}},'FORMAT-ONLY')
        self.assertEqual((value['physics_runs'],value['expert_runs'],value['model_runs'],value['media_uploads']),(12,2,1,1))
        self.assertEqual(value['native_physics'],'PASS');self.assertEqual(value['robot_control'],'PASS')
        self.assertTrue(value['media_verified']);self.assertFalse(value['ready'])
        self.assertNotIn('/private/',json.dumps(value));self.assertEqual(old['expert_runs'],0)
    def test_missing_or_duplicate_native_case_cannot_pass(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);atomic(root/'native-cases.json',{'physics':[{'name':'a','steps':1},{'name':'b','steps':1}]})
            output=root/'out';(output/'native').mkdir(parents=True)
            report={'kind':'NATIVE_PHYSX_TESTS','commit':'a'*40,'mode':'physics','passed':2,'failed':0,'reset_count':4,'cases':[{'name':'a','repeat':r,'status':'PASS'} for r in [0,1,0,1]]}
            atomic(output/'native/results.json',report)
            with patch.object(pipeline,'execute'),self.assertRaisesRegex(Incomplete,'coverage'):
                pipeline.native('unused',root,output,'physics','a'*40,None)
    def test_visual_review_bound_to_exact_bytes(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);review=root/'review.json'
            for name in FILES:(root/name).write_text('format fixture; not real media')
            with self.assertRaises(Incomplete):verify_review(review,'a'*40,root)
            from engine import digest
            atomic(review,{'commit':'a'*40,'files':{n:digest(root/n) for n in FILES},'checks':{n:True for n in CHECKS}})
            verify_review(review,'a'*40,root)
            (root/FILES[0]).write_text('changed')
            with self.assertRaises(Incomplete):verify_review(review,'a'*40,root)

if __name__=='__main__':unittest.main()
