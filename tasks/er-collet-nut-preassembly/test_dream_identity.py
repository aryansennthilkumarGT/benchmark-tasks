import copy
import unittest
from dream_identity import verify_identity


class DreamIdentity(unittest.TestCase):
    def setUp(self):
        self.spec = {'policy_config': {'action_horizon': 1}}
        self.policy = {'name': 'dream', 'checkpoint': 'dreamlabs/dream-1-beta'}
        self.transcripts = [{'model': 'dreamlabs/dream-1-beta', 'dry_run': False,
            'requests': [{'rows': 48, 'session_id': 'synthetic-test-only', 'infer_ms': 2., 'rtt_s': .1}]}]

    def test_recorded_checkpoint_and_requests_support_omitted_generic_model_field(self):
        self.assertEqual(verify_identity(self.spec,self.policy,self.transcripts)['provider_requests'],1)

    def test_dry_run_missing_or_true_fails(self):
        for value in (None, True):
            self.transcripts[0]['dry_run']=value
            with self.assertRaises(ValueError):verify_identity(self.spec,self.policy,self.transcripts)

    def test_conflicting_model_fails(self):
        self.spec['policy_config']['model']='another-model'
        with self.assertRaises(ValueError):verify_identity(self.spec,self.policy,self.transcripts)

    def test_no_provider_requests_fails(self):
        self.transcripts[0]['requests']=[]
        with self.assertRaises(ValueError):verify_identity(self.spec,self.policy,self.transcripts)


if __name__=='__main__':unittest.main()
