"""Timing and scope guards; synthetic event dictionaries are unit data only."""
import unittest
from pathlib import Path
import subprocess
import sys
import tempfile

from verify_expert_control_prefixes import completion_tick


class CompletionTests(unittest.TestCase):
    def setUp(self):
        self.case = dict(name='probe', through_phase=0, through_label='Seat', max_steps=21,
                         assertions=[])
        self.phases = [dict(label='Seat')]
        self.events = [dict(event='MEASURED_PHASE_COMPLETE', phase=0, label='Seat', time=1.)]

    def test_checks_post_action_frame_instead_of_pre_action_event(self):
        self.assertEqual(completion_tick(self.case, self.phases, self.events), 21)

    def test_rejects_prefix_that_exceeds_case_action_budget(self):
        self.case['max_steps'] = 20
        with self.assertRaisesRegex(ValueError, 'limit'):
            completion_tick(self.case, self.phases, self.events)

    def test_fixture_initialization_cannot_reuse_default_expert_reset(self):
        self.case['initialize_joints'] = []
        with self.assertRaisesRegex(ValueError, 'fixture'):
            completion_tick(self.case, self.phases, self.events)

    def test_missing_or_duplicate_phase_event_is_not_success(self):
        for events in [[], self.events*2]:
            with self.subTest(events=events), self.assertRaisesRegex(ValueError, 'ambiguous'):
                completion_tick(self.case, self.phases, events)

    def test_phase_label_mismatch_is_not_success(self):
        self.case['through_label'] = 'Another phase'
        with self.assertRaisesRegex(ValueError, 'label mismatch'):
            completion_tick(self.case, self.phases, self.events)

    def test_off_timeline_event_is_rejected(self):
        self.events[0]['time'] = 1.023
        with self.assertRaisesRegex(ValueError, 'timeline'):
            completion_tick(self.case, self.phases, self.events)

    def test_optimized_python_cannot_disable_native_assertions(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)/'must-not-exist'
            command = [sys.executable, '-O', str(Path(__file__).with_name(
                'verify_expert_control_prefixes.py')), '--folder', directory,
                '--trial', directory, '--trial', directory, '--commit', 'unit-input',
                '--output', str(output)]
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('without optimization', result.stderr)
            self.assertFalse(output.exists())


if __name__ == '__main__':
    unittest.main()
