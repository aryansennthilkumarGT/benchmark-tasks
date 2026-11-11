"""Exercise the fixed-driver preflight policy without simulating GPU execution."""
import unittest
from unittest.mock import patch

from environment import hardware


class DriverPreflightTests(unittest.TestCase):
    def hardware_for(self, name, driver):
        line = f'{name}, GPU-fixture, {driver}, 46068, 46067, 0'
        with patch('environment.shutil.which', return_value='/usr/bin/nvidia-smi'):
            with patch('environment.capture', return_value=line):
                return hardware()

    def test_fixed_l40s_requires_smoke_with_warning(self):
        result = self.hardware_for('NVIDIA L40S', '565.57.01')
        self.assertEqual(result['driver_status'], 'fixed_driver_smoke_required')
        self.assertEqual(result['selected_gpu']['driver'], '565.57.01')
        self.assertTrue(any('recommendation' in warning for warning in result['warnings']))
        self.assertFalse(any('Driver' in problem for problem in result['problems']))

    def test_other_unvalidated_driver_profiles_remain_blocked(self):
        for name, driver in (('NVIDIA L40S', '565.57.02'), ('NVIDIA GeForce RTX 4090', '565.57.01')):
            with self.subTest(name=name, driver=driver):
                result = self.hardware_for(name, driver)
                self.assertEqual(result['driver_status'], 'below_recommendation_unvalidated')
                self.assertTrue(any('compatibility-test profile' in problem for problem in result['problems']))

    def test_recommended_driver_has_no_driver_warning(self):
        result = self.hardware_for('NVIDIA L40S', '580.95.05')
        self.assertEqual(result['driver_status'], 'meets_recommendation')
        self.assertFalse(result['warnings'])


if __name__ == '__main__':
    unittest.main()
