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
