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

def test_no_qualified_candidate_blocks_without_launching(tmp_path):
 p=tmp_path/'m.json';atomic(p,dict(schema_version=3,tasks=[task(0),task(1)]))
 with pytest.raises(Incomplete,match='No candidate'),patch.object(marathon.pipeline,'main',side_effect=AssertionError('Paid work executed')):
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


def test_nested_manifest_resolves_declared_evidence_root_without_network(tmp_path):
 from test_offline_gate import fixture
 from engine import read
 t,d,bundle=fixture(tmp_path)
 t.update(branch='repair/fixture',task_folder='tasks/fixture',offline_state='OFFLINE READY',priority=1)
 nested=tmp_path/'nested'/'recovery';nested.mkdir(parents=True)
 path=nested/'manifest.json';m=dict(schema_version=3,offline_evidence_root='../..',tasks=[t]);atomic(path,m)
 with patch.object(marathon.pipeline,'main',side_effect=AssertionError('Preview executed paid work')),contextlib.redirect_stdout(io.StringIO()) as out:
  assert marathon.main(['--manifest',str(path),'--run-root',str(tmp_path/'runs'),'--verify-offline'])==0
 result=json.loads(out.getvalue());assert result['verified_offline_bundles'][0]['published_commit']==t['commit']
 assert not (tmp_path/'runs').exists()


def test_preview_verification_fails_on_changed_real_bundle_before_any_runtime(tmp_path):
 from test_offline_gate import fixture
 t,d,bundle=fixture(tmp_path);t.update(branch='repair/fixture',task_folder='tasks/fixture',offline_state='OFFLINE READY',priority=1)
 path=tmp_path/'manifest.json';atomic(path,dict(schema_version=3,tasks=[t]));bundle.write_text('{}')
 with pytest.raises(Incomplete,match='bundle changed'),patch.object(marathon.pipeline,'main',side_effect=AssertionError('Paid work executed')):
  marathon.main(['--manifest',str(path),'--run-root',str(tmp_path/'runs'),'--verify-offline'])
 assert not (tmp_path/'runs').exists()


def test_relocated_runtime_manifest_keeps_absolute_evidence_root(tmp_path):
 original=tmp_path/'nested'/'recovery';original.mkdir(parents=True)
 p=original/'manifest.json';tasks=[task(i,'OFFLINE READY') for i in range(3)]
 atomic(p,dict(schema_version=3,offline_evidence_root='../..',tasks=tasks))
 run=tmp_path/'other'/'runs'
 def inspect_runtime(args):
  from engine import read
  manifest=read(run/'ranked-source-manifest.json')
  assert manifest['offline_evidence_root']==str(tmp_path.resolve())
  assert len(manifest['tasks'])==3
  return 0
 with patch.object(marathon,'verify_ready',return_value=[]),patch.object(marathon,'open_sprint',return_value={'deadline_unix':12345}),patch.object(marathon.pipeline,'main',side_effect=inspect_runtime):
  assert marathon.main(['--execute','--manifest',str(p),'--run-root',str(run),'--budget-file','unused','--launchable-root','unused'])==0


def test_one_qualified_task_can_begin_and_submit_without_waiting_for_three(tmp_path):
 p=tmp_path/'m.json';atomic(p,dict(schema_version=3,tasks=[task(0,'OFFLINE READY'),task(1)]))
 def inspect(args):
  assert '--submit' in args and args[args.index('--deadline-unix')+1]=='12345'
  m=json.loads((tmp_path/'runs/ranked-source-manifest.json').read_text());assert len(m['tasks'])==1
  return 2  # Labelled orchestration fixture remains incomplete, no GPU claim.
 with patch.object(marathon,'verify_ready',return_value=[]),patch.object(marathon,'open_sprint',return_value={'deadline_unix':12345}),patch.object(marathon.pipeline,'main',side_effect=inspect):
  assert marathon.main(['--execute','--submit','--registered-account','fixture-account','--manifest',str(p),'--run-root',str(tmp_path/'runs'),'--budget-file','unused','--launchable-root','unused'])==2
