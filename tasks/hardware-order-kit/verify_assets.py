"""Structural USD and scene checks. Does not start a simulator."""
from pathlib import Path
import json
import math


def verify(here):
    from pxr import Gf,Sdf,Usd,UsdGeom,UsdPhysics,Work
    # Validate deterministically in this offline process. The Windows usd-core
    # 25.11 parallel descriptor parser can crash on multi-assembly scenes.
    # This does not change any native simulator thread/physics configuration.
    Work.SetConcurrencyLimit(1)
    spec=json.loads((here/'scene.json').read_text(encoding='utf-8'))
    body_count=joint_count=0
    composed=Usd.Stage.CreateInMemory()
    for a in spec['assemblies']:
        stage=Usd.Stage.Open(str(here/'assets'/f'{a["name"]}.usda'))
        assert stage and stage.GetDefaultPrim(),a['name']
        names={b['name'] for b in a['bodies']}
        for b in a['bodies']:
            prim=stage.GetPrimAtPath('/Asset/'+b['name'])
            assert prim and prim.HasAPI(UsdPhysics.RigidBodyAPI),b['name']
            assert b['mass']>0 and all(math.isfinite(v) for v in b['pos'])
            assert abs(sum(v*v for v in b['quat'])-1)<1e-9
            body_count+=1
        for j in a.get('joints',[]):
            assert j['parent'] in names and j['child'] in names
            assert j['lower']<=0<=j['upper']
            prim=stage.GetPrimAtPath('/Asset/'+j['name'])
            assert prim and prim.IsA(UsdPhysics.Joint)
            for relationship in ('physics:body0','physics:body1'):
                targets=prim.GetRelationship(relationship).GetTargets()
                assert len(targets)==1 and stage.GetPrimAtPath(targets[0])
            joint_count+=1
        # Reference the asset at its real spawn transform before parsing. A USD
        # file can parse in isolation while its world anchor is authored wrongly.
        root=UsdGeom.Xform.Define(composed,'/World/'+a['name'])
        root.GetPrim().GetReferences().AddReference(str((here/'assets'/f'{a["name"]}.usda').resolve()))
        root.AddTranslateOp().Set(Gf.Vec3d(*a['origin']))
    # Parse the complete composed task once, as a consumer would. Keep the
    # returned descriptor vectors alive for the full validation scope.
    parsed=UsdPhysics.LoadUsdPhysicsFromRange(composed,[Sdf.Path('/World')])
    for paths,descriptions in parsed.values():
        assert all(descriptions[i].isValid for i in range(len(descriptions))),'Invalid parsed USD physics descriptor'
    fixed=parsed.get(UsdPhysics.ObjectType.FixedJoint,((),()))
    # Copy scalar values; do not retain references from Boost vector iterators.
    anchors={str(fixed[0][i]):(str(fixed[1][i].body0),tuple(fixed[1][i].localPose0Position)) for i in range(len(fixed[0]))}
    for a in spec['assemblies']:
        prefix='/World/'+a['name']+'/'
        for b in a['bodies']:
            actual=UsdGeom.Xformable(composed.GetPrimAtPath(prefix+b['name'])).ComputeLocalToWorldTransform(0).Transform(Gf.Vec3d(0))
            assert (actual-Gf.Vec3d(*b['pos'])).GetLength()<2e-6,b['name']
            if b.get('anchor'):
                anchor=anchors[prefix+'fix_'+b['name']]
                assert not anchor[0],'Anchor reference must be static'
                assert (Gf.Vec3d(*anchor[1])-actual).GetLength()<2e-6,'World anchor does not follow asset placement'
                assert composed.GetPrimAtPath(prefix+'fix_'+b['name']).HasAPI(UsdPhysics.ArticulationRootAPI)
        for j in a.get('joints',[]):
            prim=UsdPhysics.Joint(composed.GetPrimAtPath(prefix+j['name']))
            points=[]
            for i in (0,1):
                target=getattr(prim,'GetBody'+str(i)+'Rel')().GetTargets()[0]
                matrix=UsdGeom.Xformable(composed.GetPrimAtPath(target)).ComputeLocalToWorldTransform(0)
                points.append(matrix.Transform(Gf.Vec3d(getattr(prim,'GetLocalPos'+str(i)+'Attr')().Get())))
            assert (points[0]-points[1]).GetLength()<2e-6,('Initial joint frames do not meet',j['name'])
    return dict(kind='USD_STRUCTURE_AND_COMPOSED_PHYSICS_DESCRIPTORS_NOT_SIMULATION',assemblies=len(spec['assemblies']),bodies=body_count,joints=joint_count,spawn_transforms_and_anchors='PASS',initial_joint_frames='PASS')


if __name__=='__main__':print(json.dumps(verify(Path(__file__).resolve().parent)))
