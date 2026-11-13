"""Executable metadata/native-case/reproduction contracts, no GPU claims."""
import json
from pathlib import Path
import jsonschema,pytest
from source_identity import runtime_hashes,require_same
HERE=Path(__file__).resolve().parent

def test_actual_metadata_matches_explicit_json_schema():
 jsonschema.Draft202012Validator(json.loads((HERE/'task-metadata.schema.json').read_text())).validate(json.loads((HERE/'task.json').read_text()))

def test_every_native_control_prefix_names_a_real_phase_and_asserts_integrity():
 plan=json.loads((HERE/'controller.json').read_text())['phases'];cases=json.loads((HERE/'native-cases.json').read_text());spec=json.loads((HERE/'scene.json').read_text())
 assert len(cases['physics'])>=5 and len(cases['control'])>=3
 for case in cases['control']:
  assert plan[case['through_phase']]['label']==case['through_label'] and case['max_steps']<=spec['run_limit']
 for mode in ('physics','control'):
  assert len({c['name'] for c in cases[mode]})==len(cases[mode])
  for case in cases[mode]:assert dict(kind='penetration',max=spec['penetration_limit']) in case['continuous_assertions']

def test_runtime_identity_rejects_changed_controller_code_and_assets(tmp_path):
 (tmp_path/'assets').mkdir()
 for name in ['scene.json','controller.json','guided-cycle-reference.json','stack-lock.json']:(tmp_path/name).write_text('{}')
 (tmp_path/'feedback.py').write_text('pass\n');(tmp_path/'assets'/'original.usda').write_text('#usda 1.0\n')
 identity=runtime_hashes(tmp_path);require_same(tmp_path,identity)
 (tmp_path/'feedback.py').write_text('raise RuntimeError\n')
 with pytest.raises(ValueError,match='stale'):require_same(tmp_path,identity)

def test_gpu_and_model_evidence_is_honestly_unexecuted():
 v=json.loads((HERE/'validation.json').read_text());assert v['ready'] is False and v['native_physics']=='NOT_RUN' and v['robot_control']=='NOT_RUN'
 assert not v['expert_scores'] and v['dream_score'] is None and v['media_uploads']==0
