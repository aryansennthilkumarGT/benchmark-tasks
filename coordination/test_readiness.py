import copy
import unittest
from verify_readiness import problems


class ReadinessTests(unittest.TestCase):
    def valid(self):
        return {'tasks':[dict(slug=str(i),branch='submission/'+str(i),status='READY',ready=True,
                 novelty='CLEARED',physics='PASS',expert_trials=[dict(score=1.0,verified=True)]*2,
                 dream=dict(score=0.0,completed=True),media_id='M-TEST00',media_verified=True,
                 remote_verified=True) for i in range(8)]}
    def test_dream_zero_is_valid(self):self.assertEqual(problems(self.valid()),[])
    def test_draft_blocks(self):
        m=self.valid();m['tasks'][0]['status']='OFFLINE_DRAFT_NOT_READY'
        self.assertTrue(problems(m))
    def test_missing_native_trials_blocks(self):
        m=self.valid();m['tasks'][0]['expert_trials']=[]
        self.assertTrue(problems(m))
    def test_missing_media_blocks(self):
        m=self.valid();m['tasks'][0]['media_verified']=False
        self.assertTrue(problems(m))
    def test_incomplete_dream_blocks(self):
        m=self.valid();m['tasks'][0]['dream']['completed']=False
        self.assertTrue(problems(m))
    def test_duplicate_branch_blocks(self):
        m=self.valid();m['tasks'][1]['branch']=m['tasks'][0]['branch']
        self.assertTrue(problems(m))


if __name__=='__main__':unittest.main()
