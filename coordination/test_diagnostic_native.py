import json
from pathlib import Path
import tempfile
import unittest

from diagnostic_native import completed_report


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
