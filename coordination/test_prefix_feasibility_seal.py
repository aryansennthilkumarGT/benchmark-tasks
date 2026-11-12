"""Failure guards use temporary unit inputs, never simulation evidence."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from seal_expert_prefix_feasibility import seal


class SealGuardTests(unittest.TestCase):
    def config(self, directory):
        root = Path(directory)
        exit_file = root/'unit-exit.txt'
        exit_file.write_text('0\n')
        return {'root': str(root), 'folder': str(root), 'commit': 'unit-revision',
                'exit_files': {k: str(exit_file) for k in ['qualification', 'first',
                    'first_validation', 'second', 'second_validation', 'physics', 'control']},
                'gpu_inventories': []}

    @patch('seal_expert_prefix_feasibility.subprocess.check_output', return_value='unit-revision')
    def test_missing_exit_fields_cannot_be_sealed(self, _):
        with tempfile.TemporaryDirectory() as directory:
            config = self.config(directory)
            del config['exit_files']['physics']
            with self.assertRaisesRegex(ValueError, 'Missing execution'):
                seal(config)
            self.assertFalse((Path(directory)/'evidence').exists())

    @patch('seal_expert_prefix_feasibility.subprocess.check_output', return_value='unit-revision')
    def test_nonzero_actual_exit_is_not_a_pass(self, _):
        with tempfile.TemporaryDirectory() as directory:
            config = self.config(directory)
            Path(config['exit_files']['qualification']).write_text('124\n')
            with self.assertRaisesRegex(ValueError, 'Nonzero or incomplete'):
                seal(config)
            self.assertFalse(list(Path(directory).rglob('receipt.json')))

    @patch('seal_expert_prefix_feasibility.subprocess.check_output', return_value='unit-revision')
    def test_missing_exit_file_is_not_a_pass(self, _):
        with tempfile.TemporaryDirectory() as directory:
            config = self.config(directory)
            Path(config['exit_files']['qualification']).unlink()
            with self.assertRaises(FileNotFoundError):
                seal(config)
            self.assertFalse((Path(directory)/'evidence').exists())

    @patch('seal_expert_prefix_feasibility.subprocess.check_output', return_value='unit-revision')
    def test_driver_evidence_cannot_be_fabricated_by_omission(self, _):
        with tempfile.TemporaryDirectory() as directory:
            config = self.config(directory)
            with self.assertRaisesRegex(ValueError, 'GPU inventories'):
                seal(config)
            inventory = Path(directory)/'invalid-unit-inventory.csv'
            inventory.write_text('Unit fixture: L40S on a different driver580\n')
            config['gpu_inventories'] = [str(inventory)]
            with self.assertRaisesRegex(ValueError, 'fixed-driver'):
                seal(config)
            self.assertFalse(list(Path(directory).rglob('receipt.json')))


if __name__ == '__main__':
    unittest.main()
