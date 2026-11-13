"""Real durable local checkpoints with synthetic clocks/API formats; no paid calls."""
import json
from unittest.mock import patch
import pytest
from engine import Incomplete,atomic,read
from session_budget import session
from sprint_state import open_sprint,record_repair,record_submission
from pipeline import submit_individual


def receipt(path,now=1000,cap=10.):
    atomic(path,dict(hourly_usd=2.,balance_usd=100.,balance_observed_unix=now,
                    spent_before_start_usd=0.,instance_started_unix=1000,
                    instance_id='NO_GPU_FORMAT_FIXTURE',gpu_uuid='NO_GPU',provider_evidence='SYNTHETIC',
                    authorized_session_spend_usd=cap,authorization_reference='TEST_ONLY_NOT_REAL_APPROVAL'))


def test_resume_preserves_deadline_and_cannot_reset_cap(tmp_path):
    p=tmp_path/'cost.json';receipt(p);root=tmp_path/'runs'
    state=open_sprint(root,p,clock=lambda:1000);assert state['deadline_unix']==22600
    receipt(p,now=1100);resumed=open_sprint(root,p,resume=True,clock=lambda:1100)
    assert resumed['deadline_unix']==22600 and len(resumed['provider_observations'])==2
    receipt(p,now=1100,cap=20.)
    with pytest.raises(Incomplete,match='cap changed'):open_sprint(root,p,resume=True,clock=lambda:1100)


def test_explicit_cap_includes_idle_and_projected_work(tmp_path):
    p=tmp_path/'cost.json';receipt(p,cap=1.)
    b=session(p,clock=lambda:1000)
    assert b.check(1700)['projected_charge_usd']<1.
    assert b.check()['shutdown_headroom_usd']>0.
    with pytest.raises(Incomplete,match='approved session'):b.check(1801)


def test_missing_authorization_never_creates_session_directory(tmp_path):
    p=tmp_path/'cost.json';receipt(p);r=read(p);r.pop('authorization_reference');atomic(p,r)
    with pytest.raises(Incomplete,match='authorization'):open_sprint(tmp_path/'runs',p,clock=lambda:1000)
    assert not (tmp_path/'runs').exists()


def test_two_repairs_per_precise_blocker_and_changed_source_required(tmp_path):
    p=tmp_path/'cost.json';receipt(p);root=tmp_path/'runs';open_sprint(root,p,clock=lambda:1000)
    for old,new in [('a'*40,'b'*40),('b'*40,'c'*40)]:record_repair(root,'fixture','phase30-pin',old,new,'Actual code change, fixture record only','d'*64)
    with pytest.raises(Incomplete,match='Two repair'):record_repair(root,'fixture','phase30-pin','c'*40,'e'*40,'Third approach','f'*64)


def test_created_pending_readback_is_durable_and_old_prs_do_not_count(tmp_path):
    p=tmp_path/'cost.json';receipt(p);root=tmp_path/'runs';open_sprint(root,p,clock=lambda:1000)
    record_submission(root,dict(action='ALREADY_EXISTS',url='https://example.invalid/old',audit={'status':'PASS'}))
    assert read(root/'sprint-session.json')['new_pr_count']==0
    for n in range(4):
        record_submission(root,dict(action='CREATED',slug=str(n),url=f'https://example.invalid/{n}',audit_status='PASS'))
    s=read(root/'sprint-session.json');assert s['new_pr_count']==4 and s['target_reached'] and not s['stop_after_target']


def test_each_submission_and_readback_failure_persist_before_next_candidate(tmp_path):
    p=tmp_path/'cost.json';receipt(p);root=tmp_path/'runs';open_sprint(root,p,clock=lambda:1000)
    task={'slug':'fixture','branch':'draft/fixture','commit':'a'*40}
    def successful(argv):
        assert read(root/'individual-ready-handoff.json')['tasks']==[task]
        atomic(root/'submission-status.json',{'tasks':[dict(slug='fixture',action='CREATED',url='https://example.invalid/1',audit_status='PASS')]})
    with patch('submit_ready.main',side_effect=successful):submit_individual(task,root,'fixture-account')
    second=dict(task,slug='second')
    def failed(argv):
        atomic(root/'submission-status.json',{'tasks':[dict(slug='second',action='CREATED',url='https://example.invalid/2',audit_status='READ_BACK_FAILED')]})
        raise Incomplete('FORMAT_FIXTURE_READBACK_FAILURE')
    with patch('submit_ready.main',side_effect=failed),pytest.raises(Incomplete):submit_individual(second,root,'fixture-account')
    assert read(root/'submissions/fixture.json')['tasks'][0]['url'].endswith('/1')
    assert read(root/'submissions/second.json')['tasks'][0]['url'].endswith('/2')
    s=read(root/'sprint-session.json');assert s['new_pr_count']==1 and len(s['created_prs'])==2


def test_diagnostic_preview_does_not_probe_gpu_credentials_or_provider(tmp_path):
    import sprint_diagnostic
    folder=tmp_path/'fixture';folder.mkdir()
    atomic(folder/'scene.json',{'slug':'fixture','physics_dt':1/960})
    atomic(folder/'native-cases.json',{'control':[{'name':'declared-case'}]})
    with patch.object(sprint_diagnostic,'hardware',side_effect=AssertionError('Preview probed GPU')),patch.object(sprint_diagnostic,'open_sprint',side_effect=AssertionError('Preview opened a paid session')):
        assert sprint_diagnostic.main(['--task-folder',str(folder),'--commit','a'*40,'--case','declared-case','--run-root',str(tmp_path/'run')])==0
    assert not (tmp_path/'run').exists()
