"""FORMAT fixtures only: these tests do not execute or prove a robot rollout."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
import numpy as np
from inspect_robots.frames import _frame_filename
from inspect_robots.rollout import derive_seed
from engine import atomic,Incomplete
from evidence import inspect_log,public_text


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)
        self.commit='a'*40;self.record=self.root/'records/run/fixture-e0';self.record.mkdir(parents=True)
        self.frames=self.root/'frames/run';self.frames.mkdir(parents=True)
        self.actions=self.root/'actions/run/fixture.jsonl';self.actions.parent.mkdir(parents=True)
        self.actions.write_text(json.dumps({'action_dim':14})+'\n'+json.dumps({'t':0,'action':[0]*14})+'\n')
        reset_seed = derive_seed(0, None, 0)
        atomic(self.record/'record.json', {
            'record_id': 'FORMAT-FIXTURE-NOT-A-ROLLOUT', 'steps': 1, 'seed': reset_seed, 'chunks': 1,
            'epoch': 0, 'configuration': {'seed': 0, 'trial_seed': reset_seed,
                                         'scene': {'id': 'fixture', 'init_seed': None}},
        })
        (self.record/'chunks.jsonl').write_text(json.dumps({'kind':'header'})+'\n'+json.dumps({'t':0,'actions':[[0]*14]})+'\n')
        for camera in ('top_cam','left_cam','right_cam'):
            for step in (0,1):np.save(self.frames/_frame_filename('fixture',camera,step),np.zeros((176,320,3),dtype=np.uint8))
        self.log={'version':3,'status':'success','eval':{'embodiment':'yam_arena','seed':0,'max_steps':10,
                  'environment_revision':self.commit,'policy':'dream','policy_config':{'model':'dreamlabs/dream-1-beta'}},
                  'results':{'total_trials':1,'total_scenes':1,'errored_trials':0},
                  'stats':{'total_steps':1,'frames_dir':'frames/run','duration_s':1},
                  'samples':[{'scene_id':'fixture','status':'success','epochs':[{'task_score':0}], 'termination_reasons':['max_steps'],
                              'record_ids':['FORMAT-FIXTURE-NOT-A-ROLLOUT'],'record_dirs':['records/run/fixture-e0']}]}
        self.write()
    def tearDown(self):self.temp.cleanup()
    def write(self):atomic(self.root/'fixture-log.json',self.log)
    def check(self):return inspect_log(self.root,'dream',10,self.commit)
    def test_schema_accepts_single_action_model_chunk(self):
        self.assertEqual(self.check()['steps'],1)
        self.assertEqual(self.check()['reset_seed'], derive_seed(0, None, 0))
    def test_raw_eval_seed_rejected_as_reset_seed(self):
        path = self.record/'record.json'
        record = json.loads(path.read_text())
        record['seed'] = 0
        atomic(path, record)
        with self.assertRaisesRegex(Incomplete, 'Derived reset seed mismatch'):
            self.check()
    def test_missing_camera_frame_rejected(self):
        (self.frames/_frame_filename('fixture','top_cam',1)).unlink()
        with self.assertRaisesRegex(Incomplete,'dropped'):self.check()
    def test_wrong_commit_rejected(self):
        self.log['eval']['environment_revision']='b'*40;self.write()
        with self.assertRaisesRegex(Incomplete,'revision'):self.check()
    def test_dream_dry_run_cannot_be_evidence(self):
        self.log['eval']['policy_config']['dry_run']=True;self.write()
        with self.assertRaisesRegex(Incomplete,'dry-run'):self.check()
    def test_error_is_not_a_zero_score(self):
        self.log['status']='error';self.write()
        with self.assertRaisesRegex(Incomplete,'finish successfully'):self.check()
    def test_expert_record_cannot_be_model_evidence(self):
        self.log['eval']['policy']='rc_expert';self.write()
        with self.assertRaisesRegex(Incomplete,'policy'):self.check()
    def test_action_gap_rejected(self):
        self.actions.write_text(json.dumps({'action_dim':14})+'\n'+json.dumps({'t':1,'action':[0]*14})+'\n')
        with self.assertRaisesRegex(Incomplete,'timeline'):self.check()
    def test_nonfinite_score_rejected(self):
        self.log['samples'][0]['epochs'][0]['task_score']='NaN';self.write()
        with self.assertRaisesRegex(Incomplete,'finite'):self.check()
    def test_path_escape_rejected(self):
        self.log['samples'][0]['record_dirs']=['../private'];self.write()
        with self.assertRaisesRegex(Incomplete,'escapes'):self.check()
    def test_native_telemetry_is_mandatory_for_task_validation(self):
        atomic(self.root/'scene.json',{})
        # A minimal scorer module is only a parser fixture, never native evidence.
        (self.root/'scoring.py').write_text('class Scorer:\n def __init__(self,spec):pass\n')
        with self.assertRaisesRegex(Incomplete,'telemetry missing'):
            inspect_log(self.root,'dream',10,self.commit,self.root)


if __name__=='__main__':unittest.main()
