"""Structural USD and scene checks. Does not start a simulator."""
from pathlib import Path
import json
import math


def verify(here):
    from pxr import Usd, UsdPhysics
    spec=json.loads((here/'scene.json').read_text(encoding='utf-8'))
    body_count=joint_count=0
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
    return dict(kind='USD_STRUCTURE_ONLY_NOT_PHYSICS',assemblies=len(spec['assemblies']),bodies=body_count,joints=joint_count)


if __name__=='__main__':print(json.dumps(verify(Path(__file__).resolve().parent)))
