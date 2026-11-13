"""Guard and dry-run contracts; no fake qualification artifacts are emitted."""
import json
from pathlib import Path
import pytest
from run import command,feasible
from run_ledger import Incomplete
from task_runner import main
from prepare_submission import prepare
from validate_rollout import public_text,inspect_log
HERE=Path(__file__).resolve().parent


def test_future_pipeline_preview_does_not_create_output_or_launch_services(tmp_path,capsys):
 output=tmp_path/'future'
 assert main(['--output',str(output),'--model'])==0
 report=json.loads(capsys.readouterr().out)
 assert report['kind']=='DRY_RUN' and report['run_limit']==5000 and not output.exists()
 assert report['stages'][-1]=='MEDIA_RENDERED'


def test_real_rollout_commands_keep_model_separate_from_privileged_expert(tmp_path):
 for mode,policy in [('expert','rc_expert'),('dream','dream')]:
  c=command(mode,tmp_path,'a'*40)
  assert c[c.index('--policy')+1]==policy and c[c.index('--max-steps')+1]=='5000'
  assert '--store-frames' in c and 'task_score' in c
  assert ('model=dreamlabs/dream-1-beta' in c)==(mode=='dream')


def test_missing_native_and_visual_evidence_cannot_prepare_submission(tmp_path):
 with pytest.raises(Incomplete,match='native/expert'):prepare(tmp_path,tmp_path/'review.json',tmp_path/HERE.name)
 with pytest.raises((Incomplete,FileNotFoundError)):feasible(tmp_path/'missing.json','a'*40)
 with pytest.raises(Incomplete,match='finalized'):inspect_log(tmp_path,'expert',5000,'a'*40,HERE)
 assert public_text(HERE)['required_fields']=='PASS'
