"""Mechanics invariants and falsification controls (CPU, standard unittest)."""
import csv
from dataclasses import replace
import hashlib
import json
from pathlib import Path
import unittest
from unittest.mock import patch
import numpy as np
from mechanism import Coupon, Parameters, plastic_spring

ROOT = Path(__file__).resolve().parent

class MechanicsTests(unittest.TestCase):
    def test_contact_energy_gradient(self):
        # Finite-difference energy checks catch incorrect load-path derivatives.
        model = Coupon()
        previous = np.array([.7,.4,.1,.1])
        for x in [np.array([1.2,.85,.22,.25]), np.array([2.3,1.9,.4,.3])]:
            energy, force = model.objective(x,.26,previous,np.zeros(3),8.)
            numerical=[]
            for j in range(4):
                delta=np.zeros(4);delta[j]=1e-6
                hi=model.objective(x+delta,.26,previous,np.zeros(3),8.)[0]
                lo=model.objective(x-delta,.26,previous,np.zeros(3),8.)[0]
                numerical.append((hi-lo)/2e-6)
            np.testing.assert_allclose(force,numerical,atol=1e-5,rtol=1e-5)

    def test_radial_contact_has_positive_energy_and_restoring_load(self):
        m=Coupon()
        energy, axial, bending, normal, overlap=m.hole(.6,[.1,.1])
        self.assertGreater(energy,0); self.assertGreater(axial,0)
        self.assertTrue(np.all(bending<0)); self.assertGreater(normal,0)
        self.assertGreater(overlap,0)
        # At equal axial position, inward leg deformation reduces wall energy.
        self.assertLess(m.hole(.6,[.5,.5])[0],energy)

    def test_unilateral_tool_and_carrier(self):
        m=Coupon(offset=20.)
        self.assertIsNone(m.nose(.45)[0])
        # Upper-face contact cannot command upward clip extraction.
        d=Coupon(pose='upper').objective(np.zeros(4),.45,np.zeros(4),np.zeros(3),0.,True)
        self.assertGreater(d['tool_force_N'],0);self.assertEqual(d['head_force_N'],0)
        # No head traction before its clearance closes.
        d=Coupon().objective(np.array([.1,0.,0.,0.]),0.,np.zeros(4),np.zeros(3),0.,True)
        self.assertEqual(d['head_force_N'],0)

    def test_plasticity_is_irreversible_and_not_a_release_switch(self):
        _,force,a=plastic_spring(3.,0.,10.,1.,.05)
        self.assertGreater(a,0);self.assertGreater(force,10.)
        _,_,unloaded=plastic_spring(a,a,10.,1.,.05)
        self.assertEqual(a,unloaded)
        model=Coupon()
        state=np.array([4.,4.,0.,0.])
        self.assertTrue(model.audit(state,np.zeros(3))['valid_nondestructive_release'])
        self.assertFalse(model.audit(state,np.array([.1,0.,0.]))['valid_nondestructive_release'])

    def test_release_is_not_a_common_extraction_depth(self):
        x=np.array([3.4,3.2,0.,0.])
        a=np.zeros(3)
        self.assertTrue(Coupon().audit(x,a)['retention_released'])
        # Same extraction, different actual shoulder profile -> still captured.
        self.assertFalse(Coupon(replace(Parameters(),peak_radius=6.5)).audit(x,a)['retention_released'])
        self.assertFalse(Coupon().audit(np.array([6.,0.,0.,0.]),a)['retention_released'])

    def test_no_audit_latch_controls_dynamics(self):
        p=replace(Parameters(),steps=24)
        physical=Coupon(p)
        a,_=physical.run(.45)
        audit=physical.audit(np.zeros(4),np.zeros(3))
        # Lie about every release diagnostic; forces and trajectories stay equal.
        with patch.object(Coupon,'audit',return_value={**audit,'retention_released':True,'valid_nondestructive_release':True}):
            b,_=Coupon(p).run(.45)
        for first,second in zip(a,b):
            np.testing.assert_allclose([first[k] for k in ['panel_mm','clip_mm','left_deflection_mm','tool_force_N']],
                                       [second[k] for k in ['panel_mm','clip_mm','left_deflection_mm','tool_force_N']],atol=1e-10)

class RecordedExperimentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.s=json.loads((ROOT/'results/summary.json').read_text())

    def test_archived_results_match_executed_code(self):
        manifest=json.loads((ROOT/'results/RUN_MANIFEST.json').read_text())
        for filename,digest in manifest['code_sha256'].items():
            self.assertEqual(hashlib.sha256((ROOT/filename).read_bytes()).hexdigest(),digest)

    def test_positive_and_all_required_negative_controls(self):
        self.assertTrue(self.s['correct']['valid_success'])
        for name in ['nearby_not_engaged','wrong_upper_surface','partial_extraction',
                     'panel_moves_clip_captured','excessive_panel_load','yielding_legs','no_initial_retention']:
            self.assertFalse(self.s[name]['valid_success'],name)
        self.assertEqual(self.s['nearby_not_engaged']['peak_tool_force_N'],0.)
        self.assertGreater(self.s['partial_extraction']['final']['clip_mm'],0.)
        self.assertTrue(self.s['partial_extraction']['final']['oversized_retaining_material_below_seat'])
        s=self.s['panel_moves_clip_captured']['final']
        self.assertGreater(s['panel_mm'],3.);self.assertLess(s['clip_mm'],.5)
        self.assertTrue(s['oversized_retaining_material_below_seat'])
        self.assertTrue(self.s['excessive_panel_load']['final']['modeled_plastic_damage'])
        self.assertTrue(self.s['yielding_legs']['final']['modeled_plastic_damage'])
        self.assertFalse(self.s['no_initial_retention']['initial']['oversized_retaining_material_below_seat'])

    def test_scalar_solver_stationarity_and_leg_symmetry(self):
        for name,s in self.s.items():
            self.assertTrue(s['numerically_resolved'],name)
            with (ROOT/'results/traces'/f'{name}.csv').open() as f:
                for r in csv.DictReader(f):
                    self.assertAlmostEqual(float(r['left_deflection_mm']),float(r['right_deflection_mm']),places=6)
                    self.assertGreaterEqual(float(r['hole_normal_N']),0.)

    def test_local_panel_force_balance_and_recovery(self):
        p=Parameters()
        with (ROOT/'results/traces/correct.csv').open() as f:
            rows=list(csv.DictReader(f))
        for r in rows:
            balance=float(r['tool_force_N'])-float(r['head_force_N'])-p.panel_stiffness*float(r['panel_mm'])
            self.assertLess(abs(balance),.01)
        self.assertGreater(max(float(r['left_deflection_mm']) for r in rows),.5)
        self.assertLess(float(rows[-1]['left_deflection_mm']),.02)
        self.assertFalse(self.s['correct']['final']['fully_withdrawn'])

    def test_numerical_refinement_preserves_release_not_force_calibration(self):
        for name,s in self.s.items():
            if s['kind']=='numerical':self.assertTrue(s['valid_success'],name)
        nominal=self.s['correct']['final']['clip_mm']
        for s in self.s.values():
            if s['kind']=='numerical':
                self.assertLess(abs(s['final']['clip_mm']-nominal),.001)

    def test_out_of_domain_contact_is_never_valid_success(self):
        for name in ['wrong_upper_surface','peak_radius_5.8','combined_large_barb_small_hole']:
            self.assertFalse(self.s[name]['contact_domain_ok'],name)
            self.assertFalse(self.s[name]['valid_success'],name)
        self.assertGreater(self.s['wrong_upper_surface']['peak_tool_overclosure_mm'],3.)
        self.assertLess(self.s['peak_radius_5.8']['minimum_deformed_radius_mm'],0.)

if __name__=='__main__':
    unittest.main(verbosity=2)
