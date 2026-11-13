import json
from pathlib import Path
import tempfile
import unittest

from diagnostic_native import completed_report, observed_cadence, sdk_sample, diagnostic_controller_state
from types import SimpleNamespace


class DiagnosticReportTests(unittest.TestCase):
    def test_missing_results_are_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            self.assertFalse(completed_report(Path(directory) / 'results.json', 'physics', 'abc'))

    def test_running_or_failed_report_cannot_pass(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'results.json'
            for status, failed in [('RUNNING', 0), ('FAIL', 1)]:
                path.write_text(json.dumps(dict(status=status, mode='physics', commit='abc',
                                                passed=2, failed=failed)))
                self.assertFalse(completed_report(path, 'physics', 'abc'))

    def test_completed_probe_requires_matching_source_and_mode(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'results.json'
            path.write_text(json.dumps(dict(status='PASS', mode='physics', commit='abc', passed=2, failed=0)))
            self.assertTrue(completed_report(path, 'physics', 'abc'))
            self.assertFalse(completed_report(path, 'control', 'abc'))
            self.assertFalse(completed_report(path, 'physics', 'different'))


class CameraCadenceTests(unittest.TestCase):
    def test_short_release_probe_can_finish_before_first_camera_period(self):
        record = dict(control_steps_completed=2, camera_samples=[],
                      camera_frame_start=dict(front=4), camera_frame_end=dict(front=4))
        self.assertTrue(observed_cadence(dict(resets=[record], render_every_control_steps=4)))

    def test_long_probe_still_requires_observed_camera_samples(self):
        record = dict(control_steps_completed=20, camera_samples=[],
                      camera_frame_start=dict(front=4), camera_frame_end=dict(front=4))
        self.assertFalse(observed_cadence(dict(resets=[record], render_every_control_steps=4)))

    def test_short_probe_requires_real_final_counters(self):
        record = dict(control_steps_completed=2, camera_samples=[], camera_frame_start=dict(front=4))
        self.assertFalse(observed_cadence(dict(resets=[record], render_every_control_steps=4)))

    def test_short_probe_rejects_counter_regression_or_excess_updates(self):
        for final in (3, 10):
            record = dict(control_steps_completed=2, camera_samples=[],
                          camera_frame_start=dict(front=4), camera_frame_end=dict(front=final))
            self.assertFalse(observed_cadence(dict(resets=[record], render_every_control_steps=4)))


class NativeSDKTelemetryTests(unittest.TestCase):
    def test_named_limits_keep_linear_finger_units_and_joint_order(self):
        settings={'wrist':{'velocity':20.,'effort':7.},'finger':{'velocity':.146,'effort':50.}}
        sample=sdk_sample(['finger','wrist'],[.1,10.],[30.,5.],settings)
        self.assertTrue(sample['passed']);self.assertAlmostEqual(sample['maximum_velocity_ratio'],.1/.146)
        self.assertAlmostEqual(sample['maximum_effort_ratio'],5./7.)
    def test_violation_nonfinite_and_unknown_joints_are_not_hidden(self):
        settings={'joint':{'velocity':2.,'effort':7.}}
        for speed,effort in [(2.1,1.),(1.,7.1)]:self.assertFalse(sdk_sample(['joint'],[speed],[effort],settings)['passed'])
        for names,vel,effort in [(['wrong'],[0.],[0.]),(['joint'],[float('nan')],[0.]),(['joint'],[0.],[])]:
            with self.assertRaises(ValueError):sdk_sample(names,vel,effort,settings)
    def test_cargo_and_nailer_do_not_require_er_thread_state(self):
        c=SimpleNamespace(index=1,phases=[{'label':'a'},{'label':'b'}],context={'arc_reference':.3})
        result=diagnostic_controller_state(c);self.assertIsNone(result['thread_state'])
        self.assertEqual(result['context']['arc_reference'],.3);self.assertEqual(result['phase_label'],'b')
