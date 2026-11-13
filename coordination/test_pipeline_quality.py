"""Paid boundary tests; no simulator/provider/setup work is executed."""
import json
from pathlib import Path
from unittest.mock import patch
import pytest
import pipeline
from engine import atomic, Incomplete


def candidate(state):
 return dict(slug='fixture',branch='repair/fixture',task_folder='tasks/fixture',commit='a'*40,offline_state=state)


@pytest.mark.parametrize('state', ['NOVELTY_HOLD','REPLACE',None])
def test_quality_hold_blocks_before_hardware_or_run_directory(tmp_path,state):
 m=tmp_path/'manifest.json';atomic(m,dict(schema_version=3,tasks=[candidate(state)]))
 with patch.object(pipeline,'hardware',side_effect=AssertionError('Hardware queried before qualification')):
  assert pipeline.main(['--manifest',str(m),'--run-root',str(tmp_path/'runs')])==3
 assert not (tmp_path/'runs').exists()


def test_label_without_evidence_blocks_before_hardware(tmp_path):
 m=tmp_path/'manifest.json';atomic(m,dict(schema_version=3,tasks=[candidate('OFFLINE READY')]))
 with patch.object(pipeline,'hardware',side_effect=AssertionError('Hardware queried before qualification')):
  assert pipeline.main(['--manifest',str(m),'--run-root',str(tmp_path/'runs')])==3
 assert not (tmp_path/'runs').exists()


def test_real_nested_bundle_resolution_and_mutation(tmp_path):
 from test_offline_gate import fixture
 t,d,bundle=fixture(tmp_path);t['offline_state']='OFFLINE READY'
 nested=tmp_path/'nested'/'recovery';nested.mkdir(parents=True)
 m=dict(offline_evidence_root='../..')
 pipeline.verify_paid_candidates([t],m,nested/'manifest.json')
 bundle.write_text('{}')
 with pytest.raises(Incomplete,match='bundle changed'):
  pipeline.verify_paid_candidates([t],m,nested/'manifest.json')


def test_official_smoke_uses_coordinator_validator_without_task_context(tmp_path):
 command=pipeline.smoke_validation_command('python',tmp_path/'smoke','b'*40)
 assert command==['python',str(pipeline.HERE/'evidence.py'),'--directory',str(tmp_path/'smoke'),'--mode','smoke','--limit','600','--commit','b'*40]
 assert Path(command[1]).is_file()
