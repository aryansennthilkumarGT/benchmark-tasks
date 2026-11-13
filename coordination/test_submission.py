"""Fail-closed preview checks; no external PR, simulator or model calls."""
import copy,json,tempfile,unittest,os,subprocess
from unittest.mock import patch
from engine import Ledger, atomic, read
from submit_ready import validated_metadata, audit_official_pr
from pathlib import Path
from engine import Incomplete
from submit_ready import main, validate_metadata

class SubmissionTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.path=Path(self.tmp.name)/'handoff.json'
        self.task=dict(slug='fixture',branch='draft/fixture',ready=True,status='READY_FOR_PR',
                       expert_scores=[1.,1.],dream_score=0.,media_id='FORMAT-FIXTURE',evidence={})
    def tearDown(self):self.tmp.cleanup()
    def check(self,tasks,pattern):
        self.path.write_text(json.dumps({'tasks':tasks}),encoding='utf8')
        with self.assertRaisesRegex(Incomplete,pattern):main([str(self.path)])
    def test_empty_handoff_blocked(self):self.check([],'No submission-ready')
    def test_unfinished_task_blocked(self):
        self.task['ready']=False;self.check([self.task],'Unfinished')
    def test_missing_receipts_blocked(self):self.check([self.task],'receipts missing')
    def test_nonfinite_score_blocked(self):
        self.task['dream_score']=float('nan');self.check([self.task],'Invalid model score')
    def test_duplicate_branch_blocked(self):
        other=copy.deepcopy(self.task);other['slug']='fixture-two';self.check([self.task,other],'Duplicate task branch')
    def test_missing_second_demo_blocked(self):
        self.task['expert_scores']=[1.];self.check([self.task],'Mandatory evidence')
    def test_official_metadata_limits(self):
        validate_metadata({'setup':'s'*4000,'fidelity':'f'*500})
        for field,maximum in [('setup',4000),('fidelity',500)]:
            metadata={'setup':'valid','fidelity':'valid'}
            metadata[field]='x'*(maximum+1)
            with self.assertRaisesRegex(Incomplete,field):validate_metadata(metadata)
            metadata[field]=''
            with self.assertRaisesRegex(Incomplete,field):validate_metadata(metadata)


class ReceiptBindingTests(unittest.TestCase):
    """Temporary Git/receipt format fixture, never simulator/model evidence."""
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
        self.source='a'*40;self.slug='fixture';self.branch='draft/fixture'
        ledger=Ledger(self.root);rows={}
        stages=('MECHANICS_COMPLETE','STATIC_TESTS_PASSED','NATIVE_PHYSICS_PASSED','ROBOT_CONTROL_PASSED',
                'EXPERT_DEMO_1_PASSED','EXPERT_DEMO_2_PASSED','CLEAN_CHECKOUT_EXPERT_PASSED',
                'MODEL_EVALUATED','MEDIA_RENDERED','MEDIA_VERIFIED','MEDIA_UPLOADED','EXACT_COMMIT_VERIFIED')
        for stage in stages:
            def action(out,stage=stage):
                atomic(out/'format-fixture.json',{'not_physics':True})
                result={'commit':self.source,'mode':'expert','score':1.}
                if stage=='MODEL_EVALUATED':result.update(mode='dream',score=0.)
                if stage=='MEDIA_UPLOADED':result={'media_id':'M-FIXTURE'}
                if stage=='EXACT_COMMIT_VERIFIED':
                    repo=out/'publication';repo.mkdir()
                    def git(*args):return subprocess.check_output(['git',*args],cwd=repo,text=True).strip()
                    git('init','-q');git('config','user.name','Format fixture');git('config','user.email','fixture@example.invalid')
                    folder=repo/'tasks'/self.slug;folder.mkdir(parents=True)
                    atomic(folder/'task.json',{'setup':'Format fixture','fidelity':'Not physics','media':'M-FIXTURE',
                          'scores':'Dream-1 (FORMAT-MODEL): 0.0; expert demos: 1.0, 1.0'})
                    git('add','.');git('commit','-qm','Format fixture only');self.commit=git('rev-parse','HEAD')
                    result={'commit':self.commit,'evaluated_commit':self.source,'branch':self.branch,'verified':True}
                return result
            rows[stage]=ledger.stage(self.slug,stage,{'commit':self.source,'stack':{'model':'FORMAT-MODEL'},
                       'prerequisites':{k:r['key'] for k,r in rows.items()}},action)
        self.task={'slug':self.slug,'branch':self.branch,'commit':self.commit,'evaluated_commit':self.source,
                   'expert_scores':[1.,1.],'dream_score':0.,'media_id':'M-FIXTURE',
                   'evidence':{k:{'key':r['key'],'receipt':r['receipt']} for k,r in rows.items()}}
    def tearDown(self):self.tmp.cleanup()
    def test_publication_object_is_resolved_outside_callers_git_database(self):
        previous=Path.cwd()
        try:
            os.chdir('/tmp')
            self.assertEqual(validated_metadata(self.task,self.root/'handoff.json')['media'],'M-FIXTURE')
        finally:os.chdir(previous)
    def test_handoff_claims_cannot_reuse_another_runs_receipts(self):
        for field,value in [('slug','other-task'),('evaluated_commit','b'*40),('commit','c'*40),
                            ('branch','draft/other'),('dream_score',.5),('media_id','M-OTHER'),('expert_scores',[.5,1.])]:
            task=copy.deepcopy(self.task);task[field]=value
            with self.subTest(field=field),self.assertRaises(Incomplete):validated_metadata(task,self.root/'handoff.json')
    def test_intact_but_disconnected_receipt_chain_is_rejected(self):
        ref=self.task['evidence']['MEDIA_VERIFIED'];path=self.root/ref['receipt'];data=read(path)
        data['inputs']['prerequisites']={}
        from engine import fingerprint
        data['key']=fingerprint(data['inputs']);ref['key']=data['key'];atomic(path,data)
        with self.assertRaisesRegex(Incomplete,'chain mismatch'):validated_metadata(self.task,self.root/'handoff.json')


class OfficialReadBackTests(unittest.TestCase):
    """Labelled API-shape fixtures only: never contact or create a real PR."""
    def task_and_responses(self):
        task={'slug':'fixture','commit':'a'*40,'branch':'draft/fixture'}
        info={'number':1,'html_url':'https://example.invalid/fixture','state':'open',
              'head':{'sha':task['commit'],'ref':task['branch'],'repo':{'full_name':'aryansennthilkumarGT/benchmark-tasks'}},'base':{'ref':'main'}}
        files=[[{'filename':'tasks/fixture/'+n,'status':'added'} for n in ['task.json','task.py','README.md','assets/original.usda']]]
        return task,info,files
    def test_actual_head_and_complete_one_folder_are_checked(self):
        task,info,files=self.task_and_responses()
        with patch('submit_ready.capture',side_effect=[json.dumps(info),json.dumps(files)]):
            self.assertEqual(audit_official_pr(task,1)['status'],'PASS')
    def test_changed_head_cross_folder_and_missing_asset_fail(self):
        for failure in ['head','folder','asset','renamed']:
            task,info,files=self.task_and_responses()
            if failure=='head':info['head']['sha']='b'*40
            elif failure=='folder':files[0].append({'filename':'README.md','status':'modified'})
            elif failure=='asset':files[0].pop()
            else:files[0][0]['previous_filename']='tasks/other/task.json'
            with self.subTest(failure=failure),patch('submit_ready.capture',side_effect=[json.dumps(info),json.dumps(files)]),self.assertRaises(Incomplete):audit_official_pr(task,1)

if __name__=='__main__':unittest.main()

