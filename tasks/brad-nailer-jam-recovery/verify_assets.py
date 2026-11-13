"""Verify actual composed USD attributes and unchanged dimensional source."""
import json
from pathlib import Path
from pxr import Usd,UsdGeom,UsdPhysics


def verify(folder):
    spec=json.loads((folder/'scene.json').read_text());checks=[]
    for a in spec['assemblies']:
        stage=Usd.Stage.Open(str(folder/'assets'/(a['name']+'.usda')))
        if stage is None:raise ValueError('Cannot compose '+a['name'])
        assert UsdGeom.GetStageUpAxis(stage)=='Z'
        assert UsdGeom.GetStageMetersPerUnit(stage)==1.
        assert stage.GetDefaultPrim().GetPath().pathString=='/Asset'
        for b in a['bodies']:
            prim=stage.GetPrimAtPath('/Asset/'+b['name'])
            assert prim.HasAPI(UsdPhysics.RigidBodyAPI)
            assert abs(UsdPhysics.MassAPI(prim).GetMassAttr().Get()-b['mass'])<1e-6
            shapes=[p for p in Usd.PrimRange(prim) if p.HasAPI(UsdPhysics.CollisionAPI)]
            assert len(shapes)==sum(s.get('collision',True) for s in b['shapes'])
            checks.append(dict(body=b['name'],colliders=len(shapes),mass_kg=b['mass']))
    result=dict(kind='OFFLINE_COMPOSED_USD',checks=checks,passed=True,physics_executed=False)
    print(json.dumps(result,indent=2));return result


if __name__=='__main__':verify(Path(__file__).resolve().parent)
