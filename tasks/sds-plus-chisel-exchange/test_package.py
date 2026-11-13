"""Actual metadata and preview/receipt guards; never emits fake native evidence."""
import json
from pathlib import Path
import pytest,jsonschema
from task_runner import main
from run import command,feasible
from run_ledger import Incomplete
from prepare_submission import prepare
from validate_rollout import public_text
from provenance import validate
from audit_control import camera_coverage
HERE=Path(__file__).resolve().parent

def test_actual_schema_and_complete_provenance():
 jsonschema.Draft202012Validator(json.loads((HERE/'task-metadata.schema.json').read_text())).validate(json.loads((HERE/'task.json').read_text()));assert validate()['passed'];assert public_text(HERE)['required_fields']=='PASS'
def test_preview_never_launches_services_or_creates_output(tmp_path,capsys):
 output=tmp_path/'future';assert main(['--output',str(output),'--model'])==0;report=json.loads(capsys.readouterr().out);assert report['kind']=='DRY_RUN' and report['run_limit']==3200 and not output.exists()
def test_missing_native_receipts_cannot_prepare_submission(tmp_path):
 with pytest.raises(Incomplete):prepare(tmp_path,tmp_path/'review.json',tmp_path/HERE.name)
 with pytest.raises((Incomplete,FileNotFoundError)):feasible(tmp_path/'none','a'*40)
 for mode in ['expert','dream']:
  cmd=command(mode,tmp_path,'a'*40);assert cmd[cmd.index('--policy')+1]==('rc_expert' if mode=='expert' else 'dream');assert cmd[cmd.index('--max-steps')+1]=='3200'
def test_cpu_claims_do_not_become_native_scores():
 d=json.loads((HERE/'validation.json').read_text());assert not d['ready'] and d['native_physics']=='NOT_RUN' and d['robot_control']=='NOT_RUN' and not d['expert_scores'] and d['dream_score'] is None
def test_actual_initial_bounds_fit_calibrated_camera():assert all(x['visible'] for x in camera_coverage(json.loads((HERE/'scene.json').read_text())).values())
