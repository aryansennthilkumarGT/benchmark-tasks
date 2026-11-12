import json
from pathlib import Path
import tempfile
import unittest
from stage_gate import verify


class CompletionGuards(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root/'producer-exit.txt').write_text('0\n')

    def test_interrupted_zero_exit_is_not_completion(self):
        (self.root/'intentional-wait-stop.json').write_text('{}')
        with self.assertRaisesRegex(ValueError, 'interrupted'):
            verify(self.root, [])

    def test_missing_real_stage_exit_is_not_completion(self):
        with self.assertRaises(FileNotFoundError):
            verify(self.root, ['process-exit.txt'])

    def test_zero_exits_without_actual_record_are_not_completion(self):
        (self.root/'process-exit.txt').write_text('0\n')
        with self.assertRaises(FileNotFoundError):
            verify(self.root, ['process-exit.txt'], 'validated-rollout.json', 'sha', 'dream')

    def test_nonzero_real_stage_is_rejected(self):
        (self.root/'process-exit.txt').write_text('143\n')
        with self.assertRaisesRegex(ValueError, 'nonzero'):
            verify(self.root, ['process-exit.txt'])


if __name__ == '__main__':
    unittest.main()
