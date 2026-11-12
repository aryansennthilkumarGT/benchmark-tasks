"""Synthetic contact serialization regressions, with no simulation evidence."""
import types
import unittest
from unittest.mock import Mock

import numpy as np

from replay_native import measured_contacts


class ContactSerializationTests(unittest.TestCase):
    def test_uses_actual_physics_dt_and_preserves_force_vector(self):
        matrix = np.array([[[0.02, -0.03, 0.04]]])
        view = Mock()
        view.get_contact_force_matrix.return_value = types.SimpleNamespace(numpy=lambda: matrix)
        result = measured_contacts(view, ['robot'], ['collar'], 1/480)
        view.get_contact_force_matrix.assert_called_once_with(dt=1/480)
        self.assertEqual(result, [{'sensor': 'robot', 'other': 'collar', 'force_N': [0.02, -0.03, 0.04]}])

    def test_filters_only_small_force_samples(self):
        matrix = np.array([[[0., 0., 0.], [0.001, 0., 0.], [0., 0., 0.1]]])
        view = Mock()
        view.get_contact_force_matrix.return_value = types.SimpleNamespace(numpy=lambda: matrix)
        result = measured_contacts(view, ['robot'], ['floor', 'guide', 'collar'], 1/240)
        self.assertEqual([row['other'] for row in result], ['collar'])

    def test_mismatched_body_dimensions_fail_instead_of_truncating(self):
        view = Mock()
        view.get_contact_force_matrix.return_value = types.SimpleNamespace(numpy=lambda: np.zeros((1, 1, 3)))
        with self.assertRaisesRegex(ValueError, 'dimensions'):
            measured_contacts(view, ['robot', 'collar'], ['floor'], 1/480)

class ControllerSnapshotTests(unittest.TestCase):
    def test_nested_thread_state_is_serializable_and_cannot_change_after_recording(self):
        from diagnostic_native import diagnostic_controller_state
        controller=types.SimpleNamespace(index=0,phases=[{'label':'Thread'}],
            thread={'mode':'lift','tcp0':np.array([.1,.2,.3])})
        result=diagnostic_controller_state(controller)
        controller.thread['tcp0'][0]=99
        controller.thread['mode']='turn'
        self.assertEqual(result['thread_state'],{'mode':'lift','tcp0':[.1,.2,.3]})
