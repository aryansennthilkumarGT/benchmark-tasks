"""Analytic mass-moment checks, independent of native physics evidence."""
import math
import numpy as np,pytest
from mass_properties import primitive,compound
from primitives import box,cylinder,quat
from convex_primitives import prism_x
from motion import rotate


def rotation(q):return np.column_stack([rotate(q,v) for v in np.eye(3)])


def tensor(props):
 r=rotation(props['principal_axes']);return r@np.diag(props['diagonal_inertia'])@r.T


def test_rotated_translated_box_matches_analytic_centroid_and_inertia():
 shape=box([.02,-.01,.03],[.02,.04,.06],q=quat([0,0,1],.3));shape['mass_density']=2700.
 p=compound([shape],.12);assert np.allclose(p['center_of_mass'],shape['pos'],atol=1e-13)
 R=rotation(shape['quat']);expected=R@np.diag([.12*(.04**2+.06**2)/12,.12*(.02**2+.06**2)/12,.12*(.02**2+.04**2)/12])@R.T
 assert np.allclose(tensor(p),expected,atol=1e-13)


def test_cylinder_has_correct_axial_and_transverse_moments():
 shape=cylinder([0,0,0],.005,.02);shape['mass_density']=7850.;p=compound([shape],.1)
 expected=np.diag([.1*(3*.005**2+.02**2)/12]*2+[.1*.005**2/2])
 assert np.allclose(tensor(p),expected,atol=1e-13)


def test_closed_convex_tetrahedral_integral_matches_rectangular_prism():
 shape=prism_x([[-.01,-.02],[.01,-.02],[.01,.02],[-.01,.02]],.03)
 volume,center,cov=primitive(shape)
 assert abs(volume-.03*.02*.04)<1e-14
 assert np.allclose(center,0.,atol=1e-14)
 assert np.allclose(cov,np.diag(np.array([.03,.02,.04])**2/12),atol=1e-14)


def test_density_weighted_components_and_parallel_axis_moment():
 a=box([-.03,0,0],[.01,.02,.03]);a['mass_density']=1000.
 b=box([.03,0,0],[.01,.02,.03]);b['mass_density']=3000.
 p=compound([a,b],.4);assert np.allclose(p['center_of_mass'],[.015,0,0],atol=1e-13)
 expected=np.diag([.4*(.02**2+.03**2)/12,.4*(.01**2+.03**2)/12,.4*(.01**2+.02**2)/12])
 expected+=np.diag([0.,.1*.045**2+.3*.015**2,.1*.045**2+.3*.015**2])
 assert np.allclose(tensor(p),expected,atol=1e-13)


def test_invalid_density_or_unsupported_geometry_cannot_fall_back_to_bbox():
 shape=box([0,0,0],[.01,.01,.01])
 with pytest.raises(ValueError,match='density'):compound([shape],.1)
 shape['mass_density']=float('nan')
 with pytest.raises(ValueError,match='density'):compound([shape],.1)
 with pytest.raises(ValueError,match='Unsupported'):primitive(dict(kind='sphere'))
