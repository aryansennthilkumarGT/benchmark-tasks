"""Real local process/Git-independent durability tests; no synthetic GPU claims."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from engine import Budget, Incomplete, Ledger, atomic, execute, exclusive, read


class EngineTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)
    def tearDown(self):self.temp.cleanup()
    def action(self,out):
        (out/'real-output.txt').write_text('test evidence, not physics')
        return {'test':True}
    def test_resume_reuses_success_without_invoking_action(self):
        Ledger(self.root).stage('a','unit',{'commit':'a'},self.action)
        def forbidden(out):raise AssertionError('Expensive stage repeated')
        result=Ledger(self.root,resume=True).stage('a','unit',{'commit':'a'},forbidden)
        self.assertEqual(result['status'],'PASS')
    def test_changed_artifact_rejects_resume(self):
        r=Ledger(self.root).stage('a','unit',{},self.action)
        (self.root/r['receipt']).parent.joinpath('real-output.txt').write_text('tampered')
        with self.assertRaisesRegex(Incomplete,'changed'):
            Ledger(self.root,resume=True).stage('a','unit',{},self.action)
    def test_missing_artifact_rejects_resume(self):
        r=Ledger(self.root).stage('a','unit',{},self.action)
        (self.root/r['receipt']).parent.joinpath('real-output.txt').unlink()
        with self.assertRaises(Incomplete):Ledger(self.root,resume=True).stage('a','unit',{},self.action)
    def test_failure_preserves_previous_task(self):
        ledger=Ledger(self.root)
        ledger.stage('a','unit',{},self.action)
        def fail(out):
            (out/'failure.log').write_text('diagnostic preserved')
            raise Incomplete('controlled failure')
        with self.assertRaises(Incomplete):ledger.stage('b','unit',{},fail)
        data=read(self.root/'ledger.json')
        self.assertEqual(data['tasks']['a']['unit'][0]['status'],'PASS')
        self.assertEqual(data['tasks']['b']['unit'][0]['status'],'FAILED')
        self.assertTrue(list(self.root.glob('b/unit/*/failure.log')))
    def test_unchanged_failure_is_not_automatically_repeated(self):
        def fail(out):raise Incomplete('bad physics configuration')
        with self.assertRaises(Incomplete):Ledger(self.root).stage('a','gpu',{},fail)
        with self.assertRaisesRegex(Incomplete,'unchanged'):
            Ledger(self.root,resume=True).stage('a','gpu',{},self.action)
    def test_one_reasoned_retry_then_hard_stop(self):
        def fail(out):raise Incomplete('bad')
        for reason in (None,'investigating driver startup'):
            with self.assertRaises(Incomplete):Ledger(self.root,retry_reason=reason).stage('a','gpu',{},fail)
        with self.assertRaisesRegex(Incomplete,'unchanged'):
            Ledger(self.root,retry_reason='again').stage('a','gpu',{},self.action)
    def test_changed_configuration_is_new_attempt(self):
        def fail(out):raise Incomplete('bad')
        with self.assertRaises(Incomplete):Ledger(self.root).stage('a','gpu',{'commit':'old'},fail)
        result=Ledger(self.root).stage('a','gpu',{'commit':'fixed'},self.action)
        self.assertEqual(result['status'],'PASS')
    def test_empty_evidence_cannot_pass(self):
        with self.assertRaisesRegex(Incomplete,'No stage evidence'):
            Ledger(self.root).stage('a','gpu',{},lambda out:{'score':1})
    def test_real_process_nonzero_is_recorded_not_accepted(self):
        with self.assertRaisesRegex(Incomplete,'exited 7'):
            execute([sys.executable,'-c','print("failure diagnostic");raise SystemExit(7)'],self.root,self.root/'log',5)
        self.assertIn('failure diagnostic',(self.root/'log').read_text())
    def test_real_process_timeout(self):
        with self.assertRaisesRegex(Incomplete,'timed out'):
            execute([sys.executable,'-c','import time;time.sleep(30)'],self.root,self.root/'log',0.2)
    def test_atomic_replacement_is_valid_json(self):
        atomic(self.root/'x.json',{'first':1});atomic(self.root/'x.json',{'second':2})
        self.assertEqual(read(self.root/'x.json'),{'second':2})
        self.assertEqual(list(self.root.glob('*.tmp')),[])
    def test_budget_counts_idle_time_and_reserve(self):
        data={'hourly_usd':2,'balance_usd':200,'spent_before_start_usd':0,'instance_started_unix':1000,
              'instance_id':'test','gpu_uuid':'test','provider_evidence':'unit-test-fixture'}
        atomic(self.root/'budget.json',data)
        budget=Budget(self.root/'budget.json',clock=lambda:1000+84*3600)
        self.assertEqual(budget.check()['estimated_instance_charge_usd'],168)
        with self.assertRaises(Incomplete):budget.check(3601)
    def test_zero_credit_cannot_start(self):
        atomic(self.root/'budget.json',{'hourly_usd':1.77,'balance_usd':0,'spent_before_start_usd':0,
               'instance_started_unix':1000,'instance_id':'test','gpu_uuid':'test','provider_evidence':'unit-test-fixture'})
        with self.assertRaises(Incomplete):Budget(self.root/'budget.json',clock=lambda:1000).check(1)
    def test_lock_prevents_second_process(self):
        command='from engine import exclusive;from pathlib import Path\nwith exclusive(Path(__import__("sys").argv[1])):pass'
        with exclusive(self.root/'lock'):
            proc=subprocess.run([sys.executable,'-c',command,str(self.root/'lock')],cwd=Path(__file__).parent,capture_output=True)
        self.assertNotEqual(proc.returncode,0)


if __name__=='__main__':unittest.main()
