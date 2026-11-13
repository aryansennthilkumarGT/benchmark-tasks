"""Prove hull reduction preserves the collision set and numeric SAT checks."""
import xml.etree.ElementTree as ET
import numpy as np
from scipy.spatial import ConvexHull
from yam_arena import YAM_URDF
from robot_geometry import stl_triangles,convex_collision_mesh,directions,local_hulls
from audit_geometry import geometry_module
from pathlib import Path
HERE=Path(__file__).resolve().parent

def test_every_robot_piece_hull_contains_all_original_vertices_without_added_vertices():
 count=0
 for mesh in ET.parse(YAM_URDF).getroot().findall('.//collision/geometry/mesh'):
  triangles=stl_triangles((YAM_URDF.parent/mesh.get('filename')).resolve());points=np.unique(np.round(triangles.reshape(-1,3),9),axis=0);h=ConvexHull(points);reduced=convex_collision_mesh(triangles)
  assert np.max(points@h.equations[:,:3].T+h.equations[:,3])<2e-8
  assert {tuple(v) for v in reduced['vertices']}<={tuple(v) for v in points}
  assert np.allclose(np.min(points,axis=0),np.min(reduced['vertices'],axis=0))
  assert np.allclose(np.max(points,axis=0),np.max(reduced['vertices'],axis=0));count+=1
 assert count==len(local_hulls()) and count>100

def test_reduced_and_original_sat_agree_on_separation_and_penetration():
 mesh=ET.parse(YAM_URDF).getroot().find('.//collision/geometry/mesh');tri=stl_triangles((YAM_URDF.parent/mesh.get('filename')).resolve());h=convex_collision_mesh(tri)
 dense=(np.unique(np.round(tri.reshape(-1,3),9),axis=0),directions(np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0])),directions(np.concatenate([tri[:,1]-tri[:,0],tri[:,2]-tri[:,1],tri[:,0]-tri[:,2]])))
 sparse=tuple(h[k] for k in ('vertices','normals','edges'));g=geometry_module(HERE)
 for delta in [[1,0,0],[.0003,.0002,.0001],[0,0,0]]:
  dense_b=(dense[0]+delta,*dense[1:]);sparse_b=(sparse[0]+delta,*sparse[1:])
  # Request the complete SAT maximum, not its separation early-exit estimate.
  assert abs(g.convex_separation(dense,dense_b,stop_at=float('inf'))-g.convex_separation(sparse,sparse_b,stop_at=float('inf')))<1e-7

def test_fcl_penetration_matches_analytic_boxes_and_complete_sat():
 import fcl
 from robot_geometry import fcl_depth
 for shift,depth in [(1.2,0.),(1.,0.),(.999,.001),(.8,.2),(.2,.8)]:
  a=fcl.CollisionObject(fcl.Box(1.,1.,1.));b=fcl.CollisionObject(fcl.Box(1.,1.,1.),fcl.Transform(np.array([shift,0.,0.])))
  assert abs(fcl_depth(a,b)-depth)<3e-6
 rng=np.random.default_rng(417);points=rng.normal(size=(18,3))*.01;hull=ConvexHull(points);tri=points[hull.simplices];h=convex_collision_mesh(tri);g=geometry_module(HERE)
 for shift in [[0,0,0],[.002,.003,.004],[.02,0,0],[.08,0,0]]:
  delta=np.asarray(shift);a=fcl.CollisionObject(h['fcl_geometry']);b=fcl.CollisionObject(h['fcl_geometry'],fcl.Transform(delta))
  poly=tuple(h[k] for k in ('vertices','normals','edges'));other=(poly[0]+delta,*poly[1:]);expected=max(0.,-g.convex_separation(poly,other,stop_at=float('inf')))
  assert abs(fcl_depth(a,b,g,(poly,other))-expected)<3e-6
