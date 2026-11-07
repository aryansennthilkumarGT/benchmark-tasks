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
        for b in assembly['bodies']:
            body_path = '/Asset/' + b['name']
            body = UsdGeom.Xform.Define(stage, body_path)
            body.AddTranslateOp().Set(Gf.Vec3d(*(v-o for v, o in zip(b['pos'], origin))))
            q = b['quat']
            body.AddOrientOp().Set(Gf.Quatf(q[3], Gf.Vec3f(*q[:3])))
            UsdPhysics.RigidBodyAPI.Apply(body.GetPrim())
            UsdPhysics.MassAPI.Apply(body.GetPrim()).CreateMassAttr(b['mass'])
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
                    UsdShade.MaterialBindingAPI.Apply(shape.GetPrim()).Bind(material, materialPurpose='physics')
            if b.get('anchor'):
                fixed = UsdPhysics.FixedJoint.Define(stage, '/Asset/fix_' + b['name'])
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
            joint.CreateCollisionEnabledAttr(False)
            if unit is not None:
                joint.CreateAxisAttr(j['axis'])
                joint.CreateLowerLimitAttr(j['lower'] * unit)
                joint.CreateUpperLimitAttr(j['upper'] * unit)
                drive = UsdPhysics.DriveAPI.Apply(joint.GetPrim(), drive_type)
                drive.CreateTypeAttr('force')
                drive.CreateTargetPositionAttr(j.get('rest', 0.0) * unit)
                drive.CreateStiffnessAttr(j.get('stiffness', 0.0))
                drive.CreateDampingAttr(j.get('damping', 0.02))
        if assembly.get('joints') or any(b.get('anchor') for b in assembly['bodies']):
            UsdPhysics.ArticulationRootAPI.Apply(root.GetPrim())
        stage.GetRootLayer().Save()


if __name__ == '__main__':
    here = Path(__file__).resolve().parent
    compile_assets(json.loads((here/'scene.json').read_text()), here/'assets')
