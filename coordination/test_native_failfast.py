import unittest
from pathlib import Path
from unittest.mock import patch
from watch_native_failures import owned_native_groups


class OwnershipTests(unittest.TestCase):
    def setUp(self):
        self.root = Path('/unit-owned-producer')

    @patch('watch_native_failures.command', return_value=['bash', '/some-other-producer.sh'])
    def test_unrelated_producer_is_never_followed(self, _):
        self.assertEqual(owned_native_groups(10, self.root), [])

    def groups(self, output, pgid):
        argv = {10: ['bash', str(self.root/'producer.sh')],
                20: ['timeout', '500', 'python', 'diagnostic.py', '--output', output]}
        with patch('watch_native_failures.command', side_effect=lambda p: argv.get(p, [])), \
             patch('watch_native_failures.children', side_effect=lambda p: [20] if p == 10 else []), \
             patch('watch_native_failures.os.getpgid', return_value=pgid), \
             patch('watch_native_failures.os.getpgrp', return_value=99):
            return owned_native_groups(10, self.root)

    def test_matches_exact_owned_native_output(self):
        self.assertEqual(self.groups(str(self.root/'selected-control'), 20), [20])

    def test_similarly_named_unowned_output_is_rejected(self):
        self.assertEqual(self.groups(str(self.root)+'-other/selected-control', 20), [])

    def test_shared_process_group_is_not_killed(self):
        self.assertEqual(self.groups(str(self.root/'final-control'), 99), [])


if __name__ == '__main__':
    unittest.main()
