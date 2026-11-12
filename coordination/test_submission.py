"""Fail-closed preview checks; no external PR, simulator or model calls."""
import copy,json,tempfile,unittest
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

if __name__=='__main__':unittest.main()
