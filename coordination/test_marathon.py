"""Preview isolation and source-gate regression; no fake GPU successes."""
import contextlib,io,json
from pathlib import Path
from unittest.mock import patch
import pytest
import marathon
from engine import Incomplete,atomic


def task(n,state='REVISION REQUIRED'):
 return dict(slug=f'fixture-{n}',branch=f'repair/fixture-{n}',task_folder=f'tasks/fixture-{n}',commit='a'*40,
             offline_state=state,priority=n)

def test_dry_run_never_executes_network_or_paid_work(tmp_path):
 p=tmp_path/'m.json';atomic(p,dict(schema_version=3,tasks=[task(i) for i in range(4)]))
 with patch.object(marathon.pipeline,'main',side_effect=AssertionError('Preview executed')),contextlib.redirect_stdout(io.StringIO()) as out:
  assert marathon.main(['--manifest',str(p),'--run-root',str(tmp_path/'runs')])==0
 d=json.loads(out.getvalue());assert d['stop_after_three'] is False and len(d['tasks'])==4 and len(d['blocked'])==4
 assert not (tmp_path/'runs').exists()

def test_incomplete_first_three_block_before_execution(tmp_path):
 p=tmp_path/'m.json';atomic(p,dict(schema_version=3,tasks=[task(0,'OFFLINE READY'),task(1)]))
 with pytest.raises(Incomplete,match='Fewer than three'),patch.object(marathon.pipeline,'main',side_effect=AssertionError('Paid work executed')):
  marathon.main(['--execute','--manifest',str(p),'--run-root',str(tmp_path/'runs'),'--budget-file','unused','--launchable-root','unused'])

def test_offline_label_alone_does_not_authorize_pipeline(tmp_path):
 p=tmp_path/'m.json';atomic(p,dict(schema_version=3,tasks=[task(i,'OFFLINE READY') for i in range(3)]))
 with pytest.raises(Incomplete,match='evidence bundle missing'),patch.object(marathon.pipeline,'main',side_effect=AssertionError('Paid work executed')):
  marathon.main(['--execute','--manifest',str(p),'--run-root',str(tmp_path/'runs'),'--budget-file','unused','--launchable-root','unused'])

def test_quality_rank_precedes_speed():
 a=task(3,'OFFLINE READY');a['estimated_qualification_seconds']=9000;b=task(0);b['estimated_qualification_seconds']=5
 assert marathon.ranked(dict(schema_version=3,tasks=[b,a]))==[a,b]

def test_protected_pending_and_rejected_branches_cannot_be_selected():
 t=task(0);t['branch']='publication/twelve-cell-pack'
 with pytest.raises(Incomplete,match='Unexpected|Protected'):marathon.ranked(dict(schema_version=3,tasks=[t]))
