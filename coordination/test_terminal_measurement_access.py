"""Analytical geometry tests only; no physics or physical photography."""
import unittest
import numpy as np
from audit_terminal_measurement_access import box_interval, cylinder_interval, shape_hit, within_clear_patch


class MeasurementGeometry(unittest.TestCase):
    def test_box_hit_and_clear_miss(self):
        self.assertEqual(box_interval(np.array([-2.,0,0]),np.array([4.,0,0]),np.ones(3)),(.25,.75))
        self.assertIsNone(box_interval(np.array([-2.,0,2]),np.array([4.,0,0]),np.ones(3)))

    def test_cylinder_crossing_and_axis_and_tangent(self):
        self.assertEqual(cylinder_interval(np.array([-2.,0,0]),np.array([4.,0,0]),1,2),(.25,.75))
        self.assertEqual(cylinder_interval(np.array([0.,0,-2]),np.array([0.,0,4]),1,2),(.25,.75))
        self.assertIsNone(cylinder_interval(np.array([-2.,1,0]),np.array([4.,0,0]),1,2))

    def test_body_rotation_and_translation_are_applied(self):
        body={'pos':[3.,4.,5.],'quat':[0,0,2**-.5,2**-.5]}
        shape={'kind':'box','pos':[0,0,0],'size':[2,1,1]}
        actual=shape_hit(np.array([3.,2.,5.]),np.array([3.,6.,5.]),body,shape)
        np.testing.assert_allclose(actual,[.25,.75],atol=1e-12)

    def test_transparency_does_not_remove_whole_wall(self):
        holder={'pos':[0.,0.,0.],'quat':[0,0,0,1]}
        cap=np.array([-.125,-.028,.008])
        wall={'pos':[0,-.057,.025],'size':[.31,.006,.05]}
        end=np.array([-.125,-.034,.008]);start=np.array([-.125,-.11,.008])
        interval=shape_hit(start,end,holder,dict(wall,kind='box'))
        self.assertTrue(within_clear_patch(start,end,holder,cap,wall,interval))
        start[0]+=.0081;end[0]+=.0081
        self.assertFalse(within_clear_patch(start,end,holder,cap,wall,interval))
        start[0]-=.0081;end[0]-=.0081;start[2]=end[2]=.02
        self.assertFalse(within_clear_patch(start,end,holder,cap,wall,interval))


if __name__=='__main__':unittest.main()
