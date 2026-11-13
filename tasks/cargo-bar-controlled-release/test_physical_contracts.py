"""Cross-export contracts for real contacts and compound inertial frames."""
import json
from pathlib import Path
import xml.etree.ElementTree as ET
import numpy as np
import mujoco
from pxr import Usd, UsdPhysics, UsdShade
from mechanism_cpu import export
from motion import rotate
from audit_geometry import geometry_module

HERE = Path(__file__).resolve().parent


def scene():
    return json.loads((HERE/'scene.json').read_text())


def matrix(q):
    return np.column_stack([rotate(q, v) for v in np.eye(3)])


def test_every_joint_pair_has_real_contact_in_both_exports_and_scoring_geometry():
    spec = scene()
    tree = ET.fromstring(export(spec))
    assert tree.find('option/flag').get('filterparent') == 'disable'
    assert not tree.findall('contact/exclude')
    assert not spec['collision_exclusions']
    excluded = geometry_module(HERE).compiled_shapes(spec)['excluded']
    count = 0
    for assembly in spec['assemblies']:
        stage = Usd.Stage.Open(str(HERE/'assets'/(assembly['name']+'.usda')))
        for joint in assembly['joints']:
            assert joint['collision_enabled'] is True
            assert frozenset((joint['parent'], joint['child'])) not in excluded
            usd = UsdPhysics.Joint(stage.GetPrimAtPath('/Asset/'+joint['name']))
            assert usd.GetCollisionEnabledAttr().Get() is True
            count += 1
    assert count == 8


def test_usd_and_cpu_preserve_compound_mass_centroid_and_full_tensor():
    spec = scene()
    model = mujoco.MjModel.from_xml_string(export(spec))
    for assembly in spec['assemblies']:
        stage = Usd.Stage.Open(str(HERE/'assets'/(assembly['name']+'.usda')))
        for body in assembly['bodies']:
            api = UsdPhysics.MassAPI(stage.GetPrimAtPath('/Asset/'+body['name']))
            assert np.allclose(api.GetCenterOfMassAttr().Get(), body['center_of_mass'], atol=2e-8)
            q = api.GetPrincipalAxesAttr().Get()
            usd_rotation = matrix([*q.GetImaginary(), q.GetReal()])
            expected_rotation = matrix(body['principal_axes'])
            expected = expected_rotation @ np.diag(body['diagonal_inertia']) @ expected_rotation.T
            actual = usd_rotation @ np.diag(api.GetDiagonalInertiaAttr().Get()) @ usd_rotation.T
            assert np.allclose(actual, expected, atol=2e-8, rtol=2e-6)
            if body.get('anchor'):
                continue  # MuJoCo's static body has no dynamic inertial frame.
            index = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, body['name'])
            assert np.isclose(model.body_mass[index], body['mass'])
            assert np.allclose(model.body_ipos[index], body['center_of_mass'], atol=1e-12)
            q = model.body_iquat[index]
            rotation = matrix([*q[1:], q[0]])
            actual = rotation @ np.diag(model.body_inertia[index]) @ rotation.T
            assert np.allclose(actual, expected, atol=1e-11)


def test_pad_material_pair_uses_declared_dynamic_mean_without_static_substitution():
    spec = scene()
    values = spec['materials']['pad']
    expected = (values['dynamic_friction'] + spec['material']['dynamic_friction'])/2
    assert np.isclose(values['cpu_dynamic_against_default'], expected)
    model = mujoco.MjModel.from_xml_string(export(spec))
    assembly = next(a for a in spec['assemblies'] if a['name']=='cargo_bar_asset')
    stage = Usd.Stage.Open(str(HERE/'assets/cargo_bar_asset.usda'))
    for name in ('left_pad', 'right_pad'):
        body = next(b for b in assembly['bodies'] if b['name']==name)
        assert body['shapes'][0]['material'] == 'pad'
        prim = stage.GetPrimAtPath('/Asset/'+name+'/shape_0')
        material = UsdShade.MaterialBindingAPI(prim).ComputeBoundMaterial(materialPurpose='physics')[0]
        api = UsdPhysics.MaterialAPI(material.GetPrim())
        assert np.isclose(api.GetDynamicFrictionAttr().Get(), values['dynamic_friction'])
        assert np.isclose(api.GetStaticFrictionAttr().Get(), values['static_friction'])
        index = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_GEOM, name+'0')
        assert np.isclose(model.geom_friction[index, 0], expected)


def test_diagnostic_velocities_use_the_same_link_origin_as_scored_positions():
    from mechanism_cpu import initialize
    from cpu_native_cases import frame
    spec = scene()
    model = mujoco.MjModel.from_xml_string(export(spec))
    data = mujoco.MjData(model)
    initialize(model, data, spec)
    data.qvel[:] = np.linspace(-.2, .3, model.nv)
    mujoco.mj_forward(model, data)
    result = frame(model, data, spec)
    for name, body in result['bodies'].items():
        index = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, name)
        linear = np.zeros((3, model.nv))
        angular = np.zeros((3, model.nv))
        mujoco.mj_jacBody(model, data, linear, angular, index)
        assert np.allclose(body['linear'], linear @ data.qvel, atol=1e-12)
        assert np.allclose(body['angular'], angular @ data.qvel, atol=1e-12)


def test_detection_margin_is_separate_from_rest_offset_and_reference_binds_export():
    import copy,hashlib,pytest
    from plan_controller import make_plan
    spec=scene();tree=ET.fromstring(export(spec));geom=tree.find('default/geom')
    assert float(geom.get('margin'))==spec['material']['contact_offset']
    assert float(geom.get('margin'))-float(geom.get('gap'))==spec['material']['rest_offset']==0.
    assert tree.find('option').get('cone')=='elliptic'
    reference=json.loads((HERE/'cam-reference.json').read_text())
    assert reference['contact_export_sha256']==hashlib.sha256(export(spec,True,True).encode()).hexdigest()
    stale=copy.deepcopy(reference);stale['contact_export_sha256']='0'*64
    with pytest.raises(ValueError,match='physical export'):make_plan(spec,stale)


def test_usd_drive_coefficients_convert_si_radians_to_usd_degrees():
    """USD DriveAPI angular coefficients are per degree; native cfg stays SI."""
    from math import pi
    spec = scene()
    observed = []
    for assembly in spec['assemblies']:
        stage = Usd.Stage.Open(str(HERE/'assets'/(assembly['name']+'.usda')))
        for j in assembly['joints']:
            angular = j['kind'] == 'revolute'
            scale = 180 / pi if angular else 1.
            prim = stage.GetPrimAtPath('/Asset/'+j['name'])
            joint = UsdPhysics.RevoluteJoint(prim) if angular else UsdPhysics.PrismaticJoint(prim)
            assert np.isclose(joint.GetLowerLimitAttr().Get(), j['lower'] * scale)
            assert np.isclose(joint.GetUpperLimitAttr().Get(), j['upper'] * scale)
            drive = UsdPhysics.DriveAPI(prim, 'angular' if angular else 'linear')
            assert np.isclose(drive.GetTargetPositionAttr().Get(), j.get('rest', 0.) * scale)
            assert np.isclose(drive.GetStiffnessAttr().Get(), j.get('stiffness', 0.) / scale, atol=1e-10)
            assert np.isclose(drive.GetDampingAttr().Get(), j.get('damping', .02) / scale, atol=1e-10)
            if angular: observed.append(j['name'])
    assert set(observed) == {'pinion_rotation','handle_rotation','holding_pawl_rotation','driving_pawl_rotation'}
