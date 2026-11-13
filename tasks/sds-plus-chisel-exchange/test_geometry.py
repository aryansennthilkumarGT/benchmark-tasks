"""Actual USD/solid/interface/provenance contracts rather than score-only mocks."""
import json,math,hashlib,tempfile
from pathlib import Path
import numpy as np,pytest
from pxr import Usd,UsdPhysics
from audit_geometry import initial,geometry_module
from build_assets import compile_assets
from mechanism_cpu import export
from mass_properties import primitive
import dimensions as D
HERE=Path(__file__).resolve().parent
SPEC=json.loads((HERE/'scene.json').read_text())
def test_unfiltered_initial_solids_include_every_fixed_and_adjacent_pair():assert initial(HERE)['passed']
def test_every_contact_pair_remains_physical_and_ball_is_free():
 assert not SPEC['collision_exclusions'];j=SPEC['assemblies'][0]['joints'];assert len(j)==1 and j[0]['collision_enabled'];assert j[0]['name']=='sleeve_retraction'
 assert not next(a for a in SPEC['assemblies'] if a['bodies'][0]['name']=='locking_ball')['joints']
 xml=export(SPEC);assert 'filterparent="disable"' in xml and '<exclude' not in xml and 'locking_ball_free' in xml

def test_original_usd_assets_rebuild_exactly_and_preserve_material_units_and_drive(tmp_path):
 compile_assets(SPEC,tmp_path)
 for f in (HERE/'assets').glob('*.usda'):assert f.read_bytes()==(tmp_path/f.name).read_bytes()
 a=SPEC['assemblies'][0];stage=Usd.Stage.Open(str(HERE/'assets'/('sds_holder_asset.usda')));j=UsdPhysics.PrismaticJoint(stage.GetPrimAtPath('/Asset/sleeve_retraction'));assert j.GetCollisionEnabledAttr().Get() is True;d=UsdPhysics.DriveAPI(j.GetPrim(),'linear');assert np.isclose(d.GetStiffnessAttr().Get(),2000) and np.isclose(d.GetDampingAttr().Get(),5) and np.isclose(d.GetTargetPositionAttr().Get(),-.001)

def test_all_convex_parts_have_positive_volume_and_consistent_face_winding():
 for a in SPEC['assemblies']:
  for b in a['bodies']:
   for s in b['shapes']:
    volume,center,cov=primitive(s);assert volume>0 and np.linalg.eigvalsh(cov).min()>=-1e-12

def test_manufacturer_ball_dimension_is_not_a_claim_of_other_measured_geometry():
 assert D.MODE==D.GeometryMode.BENCHMARK_AUTHORED and D.validate()
 assert D.PARAMETERS['BALL_DIAMETER']['classification']=='Manufacturer-documented' and D.BALL_DIAMETER==.007
 assert D.PARAMETERS['SHAFT_RADIUS']['classification']=='Benchmark-authored approximation'
 with pytest.raises(ValueError):D.validate(D.GeometryMode.MEASURED_HARDWARE)

def test_integer_identity_quaternions_are_supported_by_real_sat():
 g=geometry_module(HERE);a=g.box(dict(pos=[0,0,0],quat=[0,0,0,1]),dict(kind='box',pos=[0,0,0],quat=[0,0,0,1],size=[1,1,1]));b=g.box(dict(pos=[.9,0,0],quat=[0,0,0,1]),dict(kind='box',pos=[0,0,0],quat=[0,0,0,1],size=[1,1,1]));assert np.isclose(g.box_pair_penetrations([a],[b])[0],.1)


def test_exact_manufacturer_ball_is_sphere_in_both_exports_and_correct_inertia():
 from pxr import UsdGeom
 import mujoco
 ball=next(b for a in SPEC['assemblies'] for b in a['bodies'] if b['name']=='locking_ball');assert len(ball['shapes'])==1 and ball['shapes'][0]['kind']=='sphere'
 stage=Usd.Stage.Open(str(HERE/'assets/locking_ball_asset.usda'));assert np.isclose(UsdGeom.Sphere(stage.GetPrimAtPath('/Asset/locking_ball/shape_0')).GetRadiusAttr().Get(),.0035)
 m=mujoco.MjModel.from_xml_string(export(SPEC));i=mujoco.mj_name2id(m,mujoco.mjtObj.mjOBJ_GEOM,'locking_ball_0');assert m.geom_type[i]==mujoco.mjtGeom.mjGEOM_SPHERE and np.isclose(m.geom_size[i,0],.0035)
 assert np.allclose(ball['diagonal_inertia'],np.ones(3)*2/5*ball['mass']*.0035**2,atol=1e-13)


def test_sphere_contact_faces_edges_corners_and_convex_backend_match_analytic_geometry():
 from cad import convex
 g=geometry_module(HERE);sphere=dict(kind='sphere',pos=[0.,0.,0.],quat=[0.,0.,0.,1.],radius=.0035);cube=dict(kind='box',pos=[0.,0.,0.],quat=[0.,0.,0.,1.],size=[.02,.02,.02]);origin=dict(pos=[0.,0.,0.],quat=[0.,0.,0.,1.]);hull=convex([[x,y,z] for x in (-.01,.01) for y in (-.01,.01) for z in (-.01,.01)])
 for offsets in [(0.0034,0.,0.),(.0023,.0023,0.),(.0019,.0019,.0019)]:
  center=[.01+v if v else 0. for v in offsets];body=dict(pos=center,quat=[0.,0.,0.,1.]);expected=max(0.,sphere['radius']-np.linalg.norm(offsets));a=g.sphere_pair_depth(body,sphere,origin,cube);b=g.sphere_pair_depth(body,sphere,origin,hull);assert np.isclose(a,expected,atol=1e-10) and np.isclose(b,expected,atol=1e-7),(offsets,a,b,expected)
 assert np.isclose(g.sphere_pair_depth(origin,sphere,origin,cube),.0135)


def test_sphere_robot_qa_hull_conservatively_contains_exact_sphere():
 from scipy.spatial import ConvexHull
 g=geometry_module(HERE);v,_,_=g.sphere_qa_polyhedron(.0035);h=ConvexHull(v);assert np.min(-h.equations[:,3])>=.0035-1e-12
 assert np.max(np.linalg.norm(v,axis=1))-.0035<.00006


def test_actual_usd_materials_match_scene_and_clear_windows_keep_collisions():
 from pxr import UsdShade,UsdGeom
 count=0
 for a in SPEC['assemblies']:
  stage=Usd.Stage.Open(str(HERE/'assets'/(a['name']+'.usda')))
  for b in a['bodies']:
   for i,s in enumerate(b['shapes']):
    prim=stage.GetPrimAtPath('/Asset/'+b['name']+'/shape_'+str(i));mat=UsdShade.MaterialBindingAPI(prim).ComputeBoundMaterial(materialPurpose='physics')[0];api=UsdPhysics.MaterialAPI(mat.GetPrim());values=SPEC.get('materials',{}).get(s.get('material'),SPEC['material'])
    assert np.isclose(api.GetStaticFrictionAttr().Get(),values['static_friction']) and np.isclose(api.GetDynamicFrictionAttr().Get(),values['dynamic_friction'])
    if s.get('opacity',1.)<1.:
     assert prim.HasAPI(UsdPhysics.CollisionAPI);visual=UsdShade.MaterialBindingAPI(prim).ComputeBoundMaterial()[0];shader=visual.ComputeSurfaceSource()[0];assert np.isclose(shader.GetInput('opacity').Get(),s['opacity']);count+=1
 assert count>60


def test_physical_inspection_inserts_provide_macro_centerline_access():
 from audit_visibility import audit
 assert audit()['passed']


def test_cached_mujoco_observations_match_a_fresh_forward_after_step():
 import mujoco
 from mechanism_cpu import initialize,observe
 m=mujoco.MjModel.from_xml_string(export(SPEC));d=mujoco.MjData(m);initialize(m,d,SPEC);mujoco.mj_step(m,d);mujoco.mj_forward(m,d);cached=observe(m,d,SPEC,refresh=False);fresh=observe(m,d,SPEC)
 for n in cached['bodies']:
  for k in ['pos','quat','linear','angular']:assert np.allclose(cached['bodies'][n][k],fresh['bodies'][n][k],atol=1e-12)


def test_cached_convex_sphere_distances_follow_current_rigid_pose():
 from cad import convex
 from motion import axis_quat,rotate
 g=geometry_module(HERE);cube=convex([[x,y,z] for x in (-.01,.01) for y in (-.01,.01) for z in (-.01,.01)]);sphere=dict(kind='sphere',pos=[0.,0.,0.],quat=[0.,0.,0.,1.],radius=.0035)
 for angle in [0.,.4,-1.1,.8]:
  q=axis_quat([0,0,1],angle);body=dict(pos=[.2,.1,.8],quat=q);point=np.array(body['pos'])+rotate(q,[.0134,0,0]);ball=dict(pos=point,quat=[0.,0.,0.,1.]);assert np.isclose(g.sphere_pair_depth(ball,sphere,body,cube),.0001,atol=1e-10)


def test_full_insertion_backstop_state_is_physically_noninterfering():
 from test_scoring import goal
 g=geometry_module(HERE);f=goal();f['bodies']['replacement_flat_chisel']['pos'][0]=SPEC['parameters']['holder_mouth'][0]+.0448
 assert g.maximum_penetration(SPEC,f['bodies'])<=SPEC['penetration_limit']
