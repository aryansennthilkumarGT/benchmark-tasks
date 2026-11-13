"""Reproducibility/provenance/native-case integration, not native execution."""
import copy,hashlib,json
from pathlib import Path
import pytest
from generate_scene import make_scene
from provenance import validate
HERE=Path(__file__).resolve().parent


def test_scene_is_exactly_reproducible_and_parameters_are_classified():
 assert make_scene()==json.loads((HERE/'scene.json').read_text())
 r=validate(HERE);assert r['passed'] and r['numeric_values']>17000
 assert r['counts']['INDEPENDENTLY_MEASURED']==0


def test_measured_claims_cannot_silently_inherit_authored_geometry(tmp_path):
 for name in ['scene.json','parameter-provenance.json']:(tmp_path/name).write_bytes((HERE/name).read_bytes())
 p=tmp_path/'parameter-provenance.json';data=json.loads(p.read_text())
 data['entries'][0]['category']='INDEPENDENTLY_MEASURED';p.write_text(json.dumps(data))
 with pytest.raises(ValueError,match='measurement evidence'):validate(tmp_path)
 data['entries'][0]['category']='DERIVED';p.write_text(json.dumps(data))
 with pytest.raises(ValueError,match='Derivation'):validate(tmp_path)


def test_native_cases_bind_existing_joints_bodies_and_exact_controller_phases():
 s=json.loads((HERE/'scene.json').read_text());plan=json.loads((HERE/'controller.json').read_text());cases=json.loads((HERE/'native-cases.json').read_text())
 assemblies={a['name']:a for a in s['assemblies']};names=[]
 for mode in ['physics','control']:
  for c in cases[mode]:
   names.append(c['name']);assert c['assertions']
   if mode=='control':
    assert c['through_label']==plan['phases'][c['through_phase']]['label']
    assert not c.get('initialize_joints') and not c.get('initialize_bodies') and not c.get('forces')
   for init in c.get('initialize_joints',[]):assert init['joint'] in {j['name'] for j in assemblies[init['assembly']]['joints']}
   for force in c.get('forces',[]):assert force['body'] in {b['name'] for b in assemblies[force['assembly']]['bodies']}
 assert len(names)==len(set(names)) and len(cases['physics'])==5 and len(cases['control'])==3


def test_assets_match_scene_masses_colliders_and_materials():
 from pxr import Usd,UsdPhysics,UsdShade
 s=json.loads((HERE/'scene.json').read_text())
 for a in s['assemblies']:
  stage=Usd.Stage.Open(str(HERE/'assets'/(a['name']+'.usda')))
  for b in a['bodies']:
   prim=stage.GetPrimAtPath('/Asset/'+b['name'])
   assert abs(UsdPhysics.MassAPI(prim).GetMassAttr().Get()-b['mass'])<1e-6
   for i,shape in enumerate(b['shapes']):
    if shape.get('material')!='cam':continue
    # Material binding is inspected on actual composed colliders.
    colliders=[p for p in Usd.PrimRange(prim) if p.HasAPI(UsdPhysics.CollisionAPI)]
    material=UsdShade.MaterialBindingAPI(colliders[i]).ComputeBoundMaterial(materialPurpose='physics')[0]
    assert material and abs(UsdPhysics.MaterialAPI(material.GetPrim()).GetDynamicFrictionAttr().Get()-.08)<1e-6


def test_metadata_remains_honest_and_goal_does_not_require_relaxed_handle_angle():
 s=json.loads((HERE/'task.json').read_text());v=json.loads((HERE/'validation.json').read_text())
 assert len(s['setup'])<=4000 and len(s['fidelity'])<=500 and s['media']==''
 assert 'not run' in s['scores'].lower() and not v['ready']
 assert v['expert_runs']==v['model_runs']==v['media_uploads']==0
