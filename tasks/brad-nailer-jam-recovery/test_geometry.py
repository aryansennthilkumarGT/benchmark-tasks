"""Real authored interface/asset contracts; no native or hardware claims."""
import copy,json,math
from pathlib import Path
import numpy as np,pytest
from pxr import Usd,UsdPhysics
import dimensions as D
from generate_scene import make_scene
from audit_geometry import initial,geometry_module
from motion import rotate
HERE=Path(__file__).resolve().parent
SPEC=json.loads((HERE/'scene.json').read_text())


def test_authored_fixture_is_exactly_reproducible_without_false_measured_modes():
 assert make_scene()==SPEC
 assert D.validate_mode()['manufacturer_dimensions_claimed'] is False
 for mode in ['INDEPENDENTLY_MEASURED','MANUFACTURER_DOCUMENTED','UNKNOWN']:
  with pytest.raises(ValueError):D.validate_mode(mode)


def test_all_initial_solids_and_joint_pairs_are_checked_without_ghost_adjacency():
 r=initial(HERE);assert r['passed'] and not r['fixed_pairs_skipped'] and not r['adjacency_filtered']
 assert geometry_module(HERE).compiled_shapes(SPEC)['excluded']==set()
 assert all(j['collision_enabled'] is True for a in SPEC['assemblies'] for j in a['joints'])


def test_three_original_usds_preserve_mass_frames_and_every_joint_contact():
 for assembly in SPEC['assemblies']:
  stage=Usd.Stage.Open(str(HERE/'assets'/(assembly['name']+'.usda')));assert stage
  for b in assembly['bodies']:
   mass=UsdPhysics.MassAPI(stage.GetPrimAtPath('/Asset/'+b['name']))
   assert np.isclose(mass.GetMassAttr().Get(),b['mass'])
   assert np.allclose(mass.GetCenterOfMassAttr().Get(),b['center_of_mass'],atol=2e-8)
   q=mass.GetPrincipalAxesAttr().Get();actual=[*q.GetImaginary(),q.GetReal()]
   def tensor(quaternion,values):
    r=np.column_stack([rotate(quaternion,v) for v in np.eye(3)]);return r@np.diag(values)@r.T
   assert np.allclose(tensor(actual,mass.GetDiagonalInertiaAttr().Get()),tensor(b['principal_axes'],b['diagonal_inertia']),atol=2e-8,rtol=2e-6)
  for j in assembly['joints']:assert UsdPhysics.Joint(stage.GetPrimAtPath('/Asset/'+j['name'])).GetCollisionEnabledAttr().Get()


def test_draw_has_actual_overcenter_energy_barrier_not_only_a_named_latch():
 lengths=[]
 for phi in np.linspace(0,-.7,71):
  eccentric=np.asarray(D.HINGE_POINT)+rotate([0,0,math.sin(phi/2),math.cos(phi/2)],D.ECCENTRIC)
  lengths.append(float(np.linalg.norm(eccentric-D.PIN_CLOSED)))
 assert max(lengths)-lengths[0]>.00015
 assert 0<np.argmax(lengths)<len(lengths)-1
 assert abs(lengths[0]-D.DRAW_REST-D.END_PRELOAD)<1e-12
 assert D.INITIAL_CONTACT_DEFLECTION<.00005


def test_normal_straight_shank_fits_but_bent_head_cannot_roll_through_muzzle():
 from scoring import Scorer
 judge=Scorer(SPEC);nail=judge.defs['bent_brad'];shape=nail['shapes'][0]
 assert shape['size'][1]<.0035 and shape['size'][2]<.0026
 vertices=judge.nail_vertices(nail);root=judge.defs['nose_body']
 local=np.array([judge.local(root,p) for p in vertices]);widths=np.ptp(local[:,1:],axis=0)
 assert max(widths)>math.hypot(.0035,.0026)
 # This is a necessary axial-roll caging condition, not an exhaustive6D proof.
 # Contact protocols separately test real blocked pulls and opened extraction.

def test_original_usd_assets_rebuild_byte_for_byte(tmp_path):
 from build_assets import compile_assets
 compile_assets(SPEC,tmp_path)
 for a in SPEC['assemblies']:
  name=a['name']+'.usda';assert (tmp_path/name).read_bytes()==(HERE/'assets'/name).read_bytes()

def test_scoring_hook_planes_match_actual_capture_solids():
 arms=SPEC['parameters']['hook_arms'];root=SPEC['assemblies'][0]['bodies'][0]
 for z in arms['z_planes']:
  shapes=[s for s in root['shapes'] if s['kind']=='box' and s['pos'][2]==z and s['size'][2]==.003]
  lip=next(s for s in shapes if s['size'][0]==.0065);rear=next(s for s in shapes if s['size'][0]==.002)
  assert np.isclose(lip['pos'][1]-lip['size'][1]/2,arms['lip_under_y'])
  assert np.isclose(lip['pos'][0]+lip['size'][0]/2,arms['front_edge_x'])
  assert np.isclose(rear['pos'][0]+rear['size'][0]/2,arms['rear_inner_x'])
 assert np.isclose(arms['lip_under_y']-.0011-.005-.0011,.001)

def test_usd_joint_frames_limits_and_drive_units_match_declared_si_parameters():
 from motion import conjugate,multiply,axis_quat,qangle
 defs={b['name']:b for a in SPEC['assemblies'] for b in a['bodies']}
 for a in SPEC['assemblies']:
  stage=Usd.Stage.Open(str(HERE/'assets'/(a['name']+'.usda')))
  for j in a['joints']:
   prim=stage.GetPrimAtPath('/Asset/'+j['name']);joint=UsdPhysics.Joint(prim);parent=defs[j['parent']];child=defs[j['child']]
   assert np.allclose(joint.GetLocalPos0Attr().Get(),j['pivot_parent'],atol=1e-8)
   assert np.allclose(joint.GetLocalPos1Attr().Get(),j['pivot_child'],atol=1e-8)
   first=np.asarray(parent['pos'])+rotate(parent['quat'],joint.GetLocalPos0Attr().Get());second=np.asarray(child['pos'])+rotate(child['quat'],joint.GetLocalPos1Attr().Get());axis={'X':[1,0,0],'Y':[0,1,0],'Z':[0,0,1]}[j['axis']]
   expected=rotate(parent['quat'],np.asarray(axis)*j['initial']) if j['kind']=='prismatic' else np.zeros(3)
   assert np.allclose(second-first,expected,atol=2e-8)
   unit=180/math.pi if j['kind']=='revolute' else 1.;kind='angular' if j['kind']=='revolute' else 'linear';drive=UsdPhysics.DriveAPI(prim,kind)
   assert np.isclose(drive.GetStiffnessAttr().Get()*unit,j['stiffness'],rtol=1e-6,atol=1e-10)
   assert np.isclose(drive.GetDampingAttr().Get()*unit,j['damping'],rtol=1e-6,atol=1e-10)
   assert np.isclose(drive.GetTargetPositionAttr().Get()/unit,j['rest'],atol=1e-9)
   limit=UsdPhysics.RevoluteJoint(prim) if j['kind']=='revolute' else UsdPhysics.PrismaticJoint(prim)
   assert np.isclose(limit.GetLowerLimitAttr().Get()/unit,j['lower'],atol=2e-7)
   assert np.isclose(limit.GetUpperLimitAttr().Get()/unit,j['upper'],atol=2e-7)
