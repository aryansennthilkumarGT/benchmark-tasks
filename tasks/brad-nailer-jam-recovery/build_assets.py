"""Build original primitive collision assets. USD authoring only; no physics run.

Requires usd-core for offline compilation, or pxr bundled with Isaac Sim.
Joint motion is passive: no success-triggered snapping, attachments or teleportation.
"""
from pathlib import Path
import json
import math


def compile_assets(spec, directory):
    from pxr import Gf, Sdf, Usd, UsdGeom, UsdPhysics, UsdShade
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    for assembly in spec['assemblies']:
        path = directory / (assembly['name'] + '.usda')
        stage = Usd.Stage.CreateNew(str(path))
        UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.z)
        UsdGeom.SetStageMetersPerUnit(stage, 1.0)
        root = UsdGeom.Xform.Define(stage, '/Asset')
        stage.SetDefaultPrim(root.GetPrim())
        origin = assembly['origin']
        material = UsdShade.Material.Define(stage, '/Asset/Material')
        physics = UsdPhysics.MaterialAPI.Apply(material.GetPrim())
        physics.CreateStaticFrictionAttr(0.65)
        physics.CreateDynamicFrictionAttr(0.5)
        physics.CreateRestitutionAttr(0.0)
        materials={'default':material}
        for name,values in spec.get('materials',{}).items():
            extra=UsdShade.Material.Define(stage,'/Asset/Material_'+name)
            properties=UsdPhysics.MaterialAPI.Apply(extra.GetPrim())
            properties.CreateStaticFrictionAttr(values['static_friction'])
            properties.CreateDynamicFrictionAttr(values['dynamic_friction'])
            properties.CreateRestitutionAttr(values.get('restitution',0.))
            materials[name]=extra
        for b in assembly['bodies']:
            body_path = '/Asset/' + b['name']
            body = UsdGeom.Xform.Define(stage, body_path)
            body.AddTranslateOp().Set(Gf.Vec3d(*(v-o for v, o in zip(b['pos'], origin))))
            q = b['quat']
            body.AddOrientOp().Set(Gf.Quatf(q[3], Gf.Vec3f(*q[:3])))
            UsdPhysics.RigidBodyAPI.Apply(body.GetPrim())
            if b.get('speculative_ccd'):
                body.GetPrim().AddAppliedSchema('PhysxRigidBodyAPI')
                body.GetPrim().CreateAttribute(
                    'physxRigidBody:enableSpeculativeCCD', Sdf.ValueTypeNames.Bool).Set(True)
            mass=UsdPhysics.MassAPI.Apply(body.GetPrim());mass.CreateMassAttr(b['mass'])
            if 'center_of_mass' in b:mass.CreateCenterOfMassAttr(Gf.Vec3f(*b['center_of_mass']))
            if 'diagonal_inertia' in b:mass.CreateDiagonalInertiaAttr(Gf.Vec3f(*b['diagonal_inertia']))
            q=b.get('principal_axes',[0,0,0,1]);mass.CreatePrincipalAxesAttr(Gf.Quatf(q[3],Gf.Vec3f(*q[:3])))
            for i, s in enumerate(b['shapes']):
                shape_path = body_path + f'/shape_{i}'
                if s['kind'] == 'box':
                    shape = UsdGeom.Cube.Define(stage, shape_path)
                    shape.CreateSizeAttr(1.0)
                    shape.AddScaleOp().Set(Gf.Vec3f(*s['size']))
                elif s['kind'] == 'cylinder':
                    shape = UsdGeom.Cylinder.Define(stage, shape_path)
                    shape.CreateRadiusAttr(s['radius'])
                    shape.CreateHeightAttr(s['height'])
                    shape.CreateAxisAttr('Z')
                elif s['kind'] == 'convex':
                    shape = UsdGeom.Mesh.Define(stage, shape_path)
                    shape.CreatePointsAttr([Gf.Vec3f(*v) for v in s['vertices']])
                    shape.CreateFaceVertexCountsAttr([len(f) for f in s['faces']])
                    shape.CreateFaceVertexIndicesAttr([i for f in s['faces'] for i in f])
                    shape.CreateSubdivisionSchemeAttr('none')
                    UsdPhysics.MeshCollisionAPI.Apply(shape.GetPrim()).CreateApproximationAttr('convexHull')
                elif s['kind'] == 'cone':
                    shape = UsdGeom.Cone.Define(stage, shape_path)
                    shape.CreateRadiusAttr(s['radius'])
                    shape.CreateHeightAttr(s['height'])
                    shape.CreateAxisAttr('Z')
                else:
                    raise ValueError(s['kind'])
                # Order transforms explicitly: translation then orientation then scale.
                scale = shape.GetOrderedXformOps()
                trans = shape.AddTranslateOp()
                trans.Set(Gf.Vec3d(*s['pos']))
                rot = shape.AddOrientOp()
                q = s.get('quat', [0, 0, 0, 1])
                rot.Set(Gf.Quatf(q[3], Gf.Vec3f(*q[:3])))
                shape.SetXformOpOrder([trans, rot] + scale)
                shape.CreateDisplayColorAttr([Gf.Vec3f(*s['color'])])
                if s.get('collision', True):
                    UsdPhysics.CollisionAPI.Apply(shape.GetPrim())
                    UsdShade.MaterialBindingAPI.Apply(shape.GetPrim()).Bind(materials[s.get('material','default')], materialPurpose='physics')
            if b.get('anchor'):
                fixed = UsdPhysics.FixedJoint.Define(stage, '/Asset/fix_' + b['name'])
                # Attach to the asset's static Xform, so reference/spawn transforms
                # move the anchor too. An absent body0 means the absolute world.
                fixed.CreateBody0Rel().SetTargets([Sdf.Path('/Asset')])
                fixed.CreateBody1Rel().SetTargets([Sdf.Path(body_path)])
                fixed.CreateLocalPos0Attr(Gf.Vec3f(*(v-o for v, o in zip(b['pos'], origin))))
                fixed.CreateLocalRot0Attr(Gf.Quatf(b['quat'][3], Gf.Vec3f(*b['quat'][:3])))
        for j in assembly.get('joints', []):
            path = '/Asset/' + j['name']
            if j['kind'] == 'revolute':
                joint = UsdPhysics.RevoluteJoint.Define(stage, path)
                unit = 180 / math.pi
                drive_type = 'angular'
            elif j['kind'] == 'prismatic':
                joint = UsdPhysics.PrismaticJoint.Define(stage, path)
                unit = 1
                drive_type = 'linear'
            elif j['kind'] == 'spherical':
                joint = UsdPhysics.SphericalJoint.Define(stage, path)
                unit = None
            else:
                raise ValueError(j['kind'])
            joint.CreateBody0Rel().SetTargets([Sdf.Path('/Asset/'+j['parent'])])
            joint.CreateBody1Rel().SetTargets([Sdf.Path('/Asset/'+j['child'])])
            joint.CreateLocalPos0Attr(Gf.Vec3f(*j['pivot_parent']))
            joint.CreateLocalPos1Attr(Gf.Vec3f(*j['pivot_child']))
            for index in (0,1):
                q=j.get('rotation_'+str(index),[0,0,0,1])
                getattr(joint,'CreateLocalRot'+str(index)+'Attr')(Gf.Quatf(q[3],Gf.Vec3f(*q[:3])))
            joint.CreateCollisionEnabledAttr(j.get('collision_enabled',False))
            if unit is not None:
                joint.CreateAxisAttr(j['axis'])
                joint.CreateLowerLimitAttr(j['lower'] * unit)
                joint.CreateUpperLimitAttr(j['upper'] * unit)
                drive = UsdPhysics.DriveAPI.Apply(joint.GetPrim(), drive_type)
                drive.CreateTypeAttr('force')
                drive.CreateTargetPositionAttr(j.get('rest', 0.0) * unit)
                # OpenUSD angular drive coefficients are per degree, while
                # scene.json and the native actuator API use SI per radian.
                drive.CreateStiffnessAttr(j.get('stiffness', 0.0) / unit)
                drive.CreateDampingAttr(j.get('damping', 0.02) / unit)
        # Only explicitly listed, physically adjacent cable links may overlap at
        # their common bend joint. Other cable/fixture/robot collisions stay on.
        names={b['name'] for b in assembly['bodies']}
        for first,second in spec.get('collision_exclusions',[]):
            if first in names and second in names:
                api=UsdPhysics.FilteredPairsAPI.Apply(stage.GetPrimAtPath('/Asset/'+first))
                api.CreateFilteredPairsRel().AddTarget(Sdf.Path('/Asset/'+second))
        anchors=[b for b in assembly['bodies'] if b.get('anchor')]
        if anchors:
            if len(anchors)!=1:raise ValueError('Each fixed articulation needs one explicit root anchor')
            # Fixed-base articulation root belongs to the world/root fixed joint.
            # Keep the static reference Xform outside the articulated subtree.
            UsdPhysics.ArticulationRootAPI.Apply(stage.GetPrimAtPath('/Asset/fix_'+anchors[0]['name']))
        elif assembly.get('joints'):
            UsdPhysics.ArticulationRootAPI.Apply(root.GetPrim())
        stage.GetRootLayer().Save()


if __name__ == '__main__':
    here = Path(__file__).resolve().parent
    compile_assets(json.loads((here/'scene.json').read_text()), here/'assets')
