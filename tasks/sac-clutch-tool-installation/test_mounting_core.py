"""Synthetic numerical fixtures only; no real SAC geometry or physics claim."""
import copy
import math
import unittest
from dimensions import REQUIRED,MissingMeasurements,validated
from mounting_score import Scorer


def spec():
    radius=.05
    sites=[[radius*math.cos(a),radius*math.sin(a)] for a in [0,2*math.pi/3,4*math.pi/3]]
    return dict(studs=[dict(axis_xy=v,tip_z=.820,engagement_min_z=.814,engagement_max_z=.827,minimum_turns=7.8) for v in sites],
        retainers=['nut0','nut1','nut2'],carrier_slot_centres=[[*v,0] for v in sites],
        carrier_seat_z=.800,retainer_top_offset=.005,pitch=.00125,lateral_tolerance=.0003,
        axial_tolerance=.0002,tilt_tolerance=.025,hold_seconds=2.,penetration_limit=.001,
        fixture_tolerance=.001,control_hz=20,speed_limit=.01,spin_limit=.2,release_clearance=.02,loss_plane=.70,
        anchors={'fixture':dict(pos=[0,0,.75],quat=[0,0,0,1])})


def body(pos,quat=None):
    return dict(pos=list(pos),quat=quat or [0,0,0,1],linear=[0,0,0],angular=[0,0,0])


def frame(s,t=0,carrier_x=0):
    bodies={'carrier':body([carrier_x,0,.8]),'fixture':body([0,0,.75])}
    for i,name in enumerate(s['retainers']):bodies[name]=body([*s['studs'][i]['axis_xy'],.825])
    return dict(schema=1,time=t,bodies=bodies,robot_clearance=.03,max_penetration=0.)


def turn_sequence(s,scorer,*,spin_only=False,all_one_site=False,tilt=0.):
    f=frame(s)
    for k in range(129):
        turns=8*k/128;f['time']=k*.05
        for i,name in enumerate(s['retainers']):
            site=s['studs'][0 if all_one_site else i]
            theta=-turns*math.pi
            # yaw followed by a deliberate X tilt for adversarial cases
            q=[math.cos(theta)*math.sin(tilt/2),math.sin(theta)*math.sin(tilt/2),
               math.sin(theta)*math.cos(tilt/2),math.cos(theta)*math.cos(tilt/2)]
            f['bodies'][name]=body([*site['axis_xy'],.825-(0 if spin_only else turns*s['pitch'])],q)
        result=scorer.update(copy.deepcopy(f))
    return f,result


class ScorerTests(unittest.TestCase):
    def test_initial_tray_has_no_credit(self):
        s=spec();self.assertEqual(Scorer(s).update(frame(s,carrier_x=.2)).score,0.)

    def test_three_independent_correct_threads_and_release_hold(self):
        s=spec();c=Scorer(s);f,r=turn_sequence(s,c)
        self.assertEqual(r.secured_studs,(0,1,2));self.assertEqual(r.score,.95);self.assertFalse(r.success)
        for _ in range(41):f['time']+=.05;r=c.update(copy.deepcopy(f))
        self.assertTrue(r.success);self.assertEqual(r.score,1.)

    def test_c3_carrier_rotation_is_equivalent(self):
        s=spec();f=frame(s);f['bodies']['carrier']['quat']=[0,0,math.sin(math.pi/3),math.cos(math.pi/3)]
        self.assertTrue(Scorer(s).update(f).seated_carrier)

    def test_non_c3_rotation_and_translation_do_not_fit_studs(self):
        for q,x in [([0,0,math.sin(.1),math.cos(.1)],0),([0,0,0,1],.002)]:
            s=spec();f=frame(s,carrier_x=x);f['bodies']['carrier']['quat']=q
            self.assertFalse(Scorer(s).update(f).seated_carrier)

    def test_just_placing_retainers_flush_has_no_thread_credit(self):
        s=spec();c=Scorer(s);f=frame(s)
        for b in s['retainers']:f['bodies'][b]['pos'][2]=.815
        for k in range(50):f['time']=k*.05;r=c.update(copy.deepcopy(f))
        self.assertEqual(r.secured_studs,());self.assertEqual(r.score,.25)

    def test_free_spinning_and_tilted_pins_do_not_accumulate_credit(self):
        for spin,tilt in [(True,0),(False,.2)]:
            s=spec();c=Scorer(s);_,r=turn_sequence(s,c,spin_only=spin,tilt=tilt)
            self.assertFalse(r.secured_studs);self.assertFalse(r.success)

    def test_three_retainers_on_one_site_do_not_close_three_sites(self):
        s=spec();c=Scorer(s);_,r=turn_sequence(s,c,all_one_site=True)
        self.assertEqual(r.secured_studs,(0,));self.assertLess(r.score,1.)

    def test_backing_out_one_retainer_removes_credit(self):
        s=spec();c=Scorer(s);f,_=turn_sequence(s,c)
        f['time']+=.05;f['bodies']['nut1']['pos'][2]+=.002
        self.assertNotIn(1,c.update(f).secured_studs)

    def test_fixture_tamper_and_invalid_state_latch_failure(self):
        for change in [lambda f:f['bodies']['fixture']['pos'].__setitem__(0,.01),
                       lambda f:f.update(max_penetration=.01),
                       lambda f:f['bodies']['nut0']['pos'].__setitem__(0,float('nan'))]:
            s=spec();c=Scorer(s);f=frame(s);change(f);r=c.update(f)
            self.assertEqual(r.score,0.);self.assertIsNotNone(r.failure)
            _,r=turn_sequence(s,c);self.assertEqual(r.score,0.)

    def test_missing_part_and_conflicting_timestamp_fail(self):
        s=spec();f=frame(s);del f['bodies']['nut0']
        self.assertIsNotNone(Scorer(s).update(f).failure)
        c=Scorer(s);f=frame(s);r=c.update(f);self.assertEqual(c.update(copy.deepcopy(f)),r)
        f['robot_clearance']=0.;self.assertIsNotNone(c.update(f).failure)

    def test_lost_retainer_invalidates_other_partial_credit(self):
        s=spec();c=Scorer(s);f=frame(s);f['bodies']['nut2']['pos'][2]=.6
        r=c.update(f);self.assertEqual(r.score,0.);self.assertIn('part_lost',r.failure)

    def test_hands_and_observation_gap_reset_stability(self):
        s=spec();c=Scorer(s);f,_=turn_sequence(s,c)
        for i in range(20):f['time']+=.05;c.update(copy.deepcopy(f))
        f['time']+=.05;f['robot_clearance']=0.;self.assertFalse(c.update(copy.deepcopy(f)).success)
        f['time']+=1.;f['robot_clearance']=.03;self.assertFalse(c.update(f).success)

    def test_site_change_does_not_transfer_turn_history(self):
        s=spec();c=Scorer(s);f,_=turn_sequence(s,c)
        f['time']+=.05;f['bodies']['nut0']['pos'][:2]=s['studs'][1]['axis_xy']
        r=c.update(f);self.assertNotIn(0,r.secured_studs)

    def test_free_spin_then_drop_cannot_recover_old_turn_credit(self):
        s=spec();c=Scorer(s);f,_=turn_sequence(s,c,spin_only=True)
        f['time']+=.05
        for name in s['retainers']:f['bodies'][name]['pos'][2]=.815
        r=c.update(f)
        self.assertEqual(r.secured_studs,());self.assertFalse(r.success)

    def test_malformed_body_state_fails_closed(self):
        s=spec();f=frame(s);f['bodies']['carrier']=None
        r=Scorer(s).update(f)
        self.assertEqual(r.score,0.);self.assertEqual(r.failure,'invalid_body_state')


class DimensionTests(unittest.TestCase):
    def fixture(self):
        # Deliberately synthetic numbers exercise consistency checks. They are
        # not exported to scene.json and are NOT measurements of the LuK tool.
        values=dict(stud_circle_radius=.05,stud_tip_height=.08,stud_thread_length=.02,
            carrier_thickness=.004,carrier_slot_inner_radius=.04,carrier_slot_outer_radius=.06,
            carrier_slot_width=.009,carrier_centre_bore=.025,retracted_spindle_inner_bore=.020,
            centring_tool_outer_diameter=.015,carrier_mass=.6,retainer_diameter=.02,
            retainer_height=.006,retainer_thread_length=.005,retainer_mass=.02,
            retainer_thread_major=.008,retainer_thread_pitch=.00125)
        return dict(thread_family='M8',application_thread_verified=True,measurements={
            k:dict(value=v,uncertainty=0.,kind='synthetic_unit_fixture',reference='UNIT TEST ONLY',
                   unit='kg' if k.endswith('_mass') else 'm') for k,v in values.items()})

    def test_missing_measurements_never_gain_defaults(self):
        with self.assertRaises(MissingMeasurements):validated({'measurements':{}})

    def test_synthetic_geometry_cannot_be_used_as_measured_hardware(self):
        with self.assertRaisesRegex(ValueError,'provenance'):validated(self.fixture())
        self.assertEqual(validated(self.fixture(),synthetic_test=True)['flywheel_thread_pitch'],.00125)

    def test_invalid_or_incompatible_dimensions_are_rejected(self):
        for key,value in [('carrier_slot_width',.007),('carrier_centre_bore',.01),
                          ('stud_circle_radius',.09),('retainer_thread_length',.01)]:
            f=self.fixture();f['measurements'][key]['value']=value
            with self.assertRaises(ValueError):validated(f,synthetic_test=True)

    def test_kit_family_does_not_prove_vehicle_compatibility(self):
        f=self.fixture();f['application_thread_verified']=False
        with self.assertRaisesRegex(ValueError,'flywheel'):validated(f,synthetic_test=True)

    def test_upper_retainer_thread_is_not_inferred_from_flywheel_thread(self):
        f=self.fixture();del f['measurements']['retainer_thread_pitch']
        with self.assertRaises(MissingMeasurements):validated(f,synthetic_test=True)

    def test_units_are_explicit_and_converted(self):
        f=self.fixture();r=f['measurements']['carrier_thickness'];r.update(value=4.,unit='mm')
        self.assertAlmostEqual(validated(f,synthetic_test=True)['carrier_thickness'],.004)
        r['unit']='inferred'
        with self.assertRaisesRegex(ValueError,'unit'):validated(f,synthetic_test=True)


if __name__=='__main__':unittest.main()
