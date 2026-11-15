"""Logic/source-geometry regression tests. Synthetic probes are NOT candidate geometry."""
import copy
import json
import unittest
from pathlib import Path

import numpy as np

from access_core import (ROOT, Robot, aabb, aabb_separated, audit_inputs, convex_intersects,
                         certify_static_obstacle_interval, evaluate, points_at, rpy_matrix)


def box(centre, half):
    # Explicit mathematical test solid, not a door/clip/seal/hardware model.
    return np.asarray(centre) + np.array([[x, y, z] for x in [-half, half]
                                        for y in [-half, half] for z in [-half, half]])


class AccessCoreTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.robot = Robot()
        cls.q = cls.robot.data['ready_joint_radians'] + [-.04695, -.04695]

    def test_pinned_complete_collision_geometry(self):
        self.assertEqual(self.robot.data['pin'], '0059d02a1a91bc6834c1d0846022891df0c78730')
        self.assertEqual(len(self.robot.hulls), 315)
        for link, expected in [('gripper', 44), ('tip_left', 45), ('tip_right', 47), ('link5', 16)]:
            self.assertEqual(sum(h['link'] == link for h in self.robot.hulls), expected)

    def test_known_source_fk_ready_coordinates(self):
        # Independent prior pinned-reference FK values, not fitted to task targets.
        np.testing.assert_allclose(self.robot.tcp(self.q), [.3234096581812836, .3050041444307181, 1.008104160176804], atol=1e-11)

    def test_second_arm_station_offset(self):
        np.testing.assert_allclose(self.robot.tcp(self.q, 'left') - self.robot.tcp(self.q, 'right'), [0., .61, 0.], atol=1e-12)

    def test_actual_joint_limits_not_tcp_reach_alone(self):
        q = self.q.copy()
        q[0] = 10.
        with self.assertRaises(ValueError):
            self.robot.fk(q)

    def test_missing_arm_finger_coordinates_rejected(self):
        with self.assertRaises(ValueError):
            self.robot.fk(self.q[:6])

    def test_jacobian_against_actual_fk_finite_difference(self):
        jac, _ = self.robot.jacobian_and_gravity(self.q)
        eps = 1e-6
        for k in range(6):
            qa, qb = self.q.copy(), self.q.copy()
            qa[k] += eps
            qb[k] -= eps
            actual = (self.robot.tcp(qa)-self.robot.tcp(qb))/(2*eps)
            np.testing.assert_allclose(actual, jac[:3, k], atol=2e-8)

    def test_static_force_is_configuration_bound_not_hardware_rating(self):
        result = self.robot.static_force_ceiling(self.q, [0., 0., 1.])
        self.assertIsNotNone(result['feasible_static_interval_N'])
        self.assertGreater(result['feasible_static_interval_N'][1], 0.)
        self.assertIn('no payload/grip', result['scope'])

    def test_sat_separated_and_overlapping_math_solids(self):
        self.assertFalse(convex_intersects(box([0., 0., 0.], 1.), box([3., 0., 0.], 1.)))
        self.assertTrue(convex_intersects(box([0., 0., 0.], 1.), box([1.5, 0., 0.], 1.)))

    def test_sat_contact_is_not_positive_clearance(self):
        self.assertTrue(convex_intersects(box([0., 0., 0.], 1.), box([2., 0., 0.], 1.)))

    def test_actual_palm_collision_not_seen_by_point_tcp(self):
        poses, _ = self.robot.fk(self.q)
        h = next(h for h in self.robot.hulls if h['link'] == 'gripper')
        v = points_at(h['vertices'], poses['gripper'])
        centre = v.mean(axis=0)
        probe = box(centre, 1e-6)
        self.assertTrue(convex_intersects(v, probe))
        self.assertGreater(np.linalg.norm(centre-self.robot.tcp(self.q)), .01)

    def test_sweep_bound_encloses_real_hull_vertices(self):
        qa, qb = self.q.copy(), self.q.copy()
        qb[1] += .25
        qb[3] -= .2
        qb[6] = 0.
        for link in ['link2', 'gripper', 'tip_left', 'tip_right']:
            h = next(h for h in self.robot.hulls if h['link'] == link)
            a, _ = self.robot.fk(qa)
            original = points_at(h['vertices'], a[link])
            bound = self.robot.movement_bound(link, h['vertices'], np.asarray(qa), qb)
            for t in np.linspace(0., 1., 25):
                q = ((1-t)*np.asarray(qa)+t*np.asarray(qb)).tolist()
                p, _ = self.robot.fk(q)
                displacement = np.linalg.norm(points_at(h['vertices'], p[link])-original, axis=1).max()
                self.assertLessEqual(displacement, bound+1e-10)

    def test_zero_movement_bound(self):
        h = next(h for h in self.robot.hulls if h['link'] == 'tip_left')
        self.assertEqual(self.robot.movement_bound(h['link'], h['vertices'], np.asarray(self.q), self.q), 0.)

    def test_far_obstacle_conservative_interval_certificate(self):
        h = next(h for h in self.robot.hulls if h['link'] == 'gripper')
        q1 = self.q.copy()
        q1[3] += .1
        result = certify_static_obstacle_interval(self.robot, 'left', h, self.q, q1, box([50., 50., 50.], .01))
        self.assertEqual(result, 'CLEAR_CONSERVATIVE_ENCLOSURE')

    def test_endpoint_collision_cannot_be_sweep_clear(self):
        h = next(h for h in self.robot.hulls if h['link'] == 'gripper')
        poses, _ = self.robot.fk(self.q)
        centre = points_at(h['vertices'], poses['gripper']).mean(axis=0)
        result = certify_static_obstacle_interval(self.robot, 'left', h, self.q, self.q, box(centre, 1e-6))
        self.assertEqual(result, 'COLLISION_MODEL_INTERSECTION')

    def test_mid_swing_collision_is_not_hidden_by_clear_endpoints(self):
        h = next(h for h in self.robot.hulls if h['link'] == 'gripper')
        q1 = self.q.copy()
        q1[0] += .8
        mid = ((np.asarray(self.q)+q1)/2).tolist()
        pm, _ = self.robot.fk(mid)
        probe = box(points_at(h['vertices'], pm['gripper']).mean(axis=0), 1e-6)
        for q in [self.q, q1]:
            p, _ = self.robot.fk(q)
            self.assertFalse(convex_intersects(points_at(h['vertices'], p['gripper']), probe))
        coarse = certify_static_obstacle_interval(self.robot, 'left', h, self.q, q1, probe, max_depth=0)
        self.assertEqual(coarse, 'INCONCLUSIVE_SWEEP_BOUND')
        refined = certify_static_obstacle_interval(self.robot, 'left', h, self.q, q1, probe, max_depth=4)
        self.assertEqual(refined, 'COLLISION_MODEL_INTERSECTION')

    def test_null_input_regression_all_candidates_block(self):
        for name in ['N040', 'N044', 'N047', 'N022']:
            with self.subTest(candidate=name):
                d = json.loads((ROOT/'inputs'/f'{name}.json').read_text())
                out = evaluate(d, self.robot)
                self.assertEqual(out['access_decision'], 'NOT_CLEARED')
                self.assertEqual(out['input_status'], 'BLOCKED_MISSING_INPUTS')
                self.assertFalse(out['empirical_candidate_test'])

    def test_ordinary_part_id_not_numeric_geometry(self):
        d = json.loads((ROOT/'inputs/N044.json').read_text())
        self.assertIn('HYD214432E000', d['selected_equipment'])
        self.assertTrue(any(x['input']=='VIN_matched_seal_section_OD_ID_width_and_orientation' for x in audit_inputs(d)))

    def test_assumed_geometry_is_not_trusted(self):
        d = json.loads((ROOT/'inputs/N044.json').read_text())
        name = d['required_geometry'][0]
        d['geometry_inputs'][name] = {'value': [1., 2., 3.], 'status': 'assumed', 'source_ref': 'illustrative'}
        self.assertTrue(any(x['input']==name and 'unsourced' in x['reason'] for x in audit_inputs(d)))

    def test_package_length_not_selected_robot_span(self):
        d = json.loads((ROOT/'inputs/N022.json').read_text())
        self.assertIsNone(d['geometry_inputs']['selected_sleeve_pitch_ID_OD_section_and_cut_length']['value'])

    def test_known_travel_or_stem_does_not_clear_keeper(self):
        d = json.loads((ROOT/'inputs/N047.json').read_text())
        self.assertEqual(d['known_numeric_geometry']['max_retainer_depression_m']['value'], .012)
        self.assertIn('spring_force_displacement_and_installed_preload', evaluate(d, self.robot)['force_inputs_missing'])
        self.assertIsNone(d['geometry_inputs']['keeper_halves_OD_height_taper_and_stem_groove_dimensions']['value'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
