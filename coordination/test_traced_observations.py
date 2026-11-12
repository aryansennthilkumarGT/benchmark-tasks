"""Actual-observation serialization contracts; no simulator is executed."""
import types
import unittest
import numpy as np
from run_traced import observed_joints


class ObservationTraceTests(unittest.TestCase):
    def test_copies_measured_joint_values_without_using_action_targets(self):
        measured = np.linspace(-.5, .5, 14)
        observation = types.SimpleNamespace(state={'joint_pos': measured}, state_time=.15)
        result = observed_joints(observation)
        measured[0] = 99
        self.assertEqual(result['time'], .15)
        self.assertEqual(result['joint_pos'][0], -.5)
        self.assertEqual(len(result['joint_pos']), 14)

    def test_missing_or_nonfinite_measured_joints_fail_closed(self):
        for joints in [np.zeros(13), np.full(14, np.nan)]:
            with self.assertRaises(ValueError):
                observed_joints(types.SimpleNamespace(state={'joint_pos': joints}, state_time=0))
