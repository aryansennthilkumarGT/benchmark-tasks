"""CPU transfer integration: real local Git fixtures, no GPU/provider/model calls."""
import importlib.util,json,os,shutil,subprocess,sys,hashlib
from pathlib import Path
import pytest
from engine import Budget,Incomplete,atomic,read
import brev_policy
from session_budget import session
from sprint_state import open_sprint

HERE=Path(__file__).resolve().parent/'brev_transfer'
spec=importlib.util.spec_from_file_location('transfer_fixture_module',HERE/'transfer.py')
transfer=importlib.util.module_from_spec(spec);spec.loader.exec_module(transfer)


def git(root,*args):return subprocess.check_output(['git',*args],cwd=root,text=True,stderr=subprocess.DEVNULL).strip()


@pytest.fixture
def scoped(tmp_path,monkeypatch):
    root=tmp_path/'session';root.mkdir();monkeypatch.setattr(brev_policy,'ROOT',root)
    atomic(root/'handoff-state.json',{'authorization_session_id':'FORMAT_FIXTURE_NOT_REAL_AUTH'})
    folder=root/'provider-observations';folder.mkdir();path=folder/'facts.json'
    value=dict(hourly_usd=2.,balance_usd=20.,spent_before_start_usd=999.,instance_started_unix=1000.,
        balance_observed_unix=1000.,instance_id='NO_GPU_TEST',gpu_uuid='NO_GPU_TEST',instance_name=brev_policy.INSTANCE,
        provider_evidence='SYNTHETIC_NOT_PROVIDER_DATA',spending_policy_id=brev_policy.POLICY_ID,
        authorization_reference=brev_policy.AUTHORIZATION_REFERENCE,authorization_session_id='FORMAT_FIXTURE_NOT_REAL_AUTH',
        authorized_session_spend_usd=15.,estimated_shutdown_trigger_usd=13.5,
        provider_stop_command=brev_policy.STOP_COMMAND,shutdown_method_confirmed=True)
    atomic(path,value)
    return root,path,value


def test_scoped_15_approval_works_below_legacy_30_reserve_without_faking_past_cost(scoped):
    root,path,value=scoped;budget=Budget(path,clock=lambda:1000)
    result=budget.check(1200)
    assert result['cap_usd']==15. and result['reserve_usd']==0. and result['estimated_shutdown_trigger_usd']==13.5
    assert read(path)['spent_before_start_usd']==999.  # Historical facts were not zeroed/mutated.


def test_1350_trigger_and_insufficient_actual_credit_block_before_work(scoped):
    root,path,value=scoped
    with pytest.raises(Incomplete,match='13.50'):Budget(path,clock=lambda:1000+13.5*1800).check()
    value['balance_usd']=.01;atomic(path,value)
    with pytest.raises(Incomplete,match='reserve'):Budget(path,clock=lambda:1000).check(1200)


@pytest.mark.parametrize('field,value',[('spending_policy_id','other'),('instance_name','other-instance'),
    ('authorization_reference','not-this-approval'),('authorization_session_id','other-session'),
    ('authorized_session_spend_usd',16.),('estimated_shutdown_trigger_usd',15.),('shutdown_method_confirmed',False)])
def test_other_sessions_cannot_silently_bypass_limits(scoped,field,value):
    root,path,data=scoped;data[field]=value;atomic(path,data)
    with pytest.raises(Incomplete):Budget(path,clock=lambda:1000)


def test_legacy_receipt_still_has_30_reserve(scoped):
    root,path,value=scoped;value.pop('spending_policy_id');value['spent_before_start_usd']=0.;atomic(path,value)
    with pytest.raises(Incomplete,match='reserve'):Budget(path,clock=lambda:1000).check()


def test_scoped_receipt_cannot_be_moved_to_another_run_root(scoped,tmp_path):
    root,path,value=scoped;other=tmp_path/'other.json';atomic(other,value)
    with pytest.raises(Incomplete,match='dedicated'):Budget(other,clock=lambda:1000)


def test_resume_cannot_reset_six_hour_clock_or_reuse_scope_as_new_start(scoped):
    root,path,value=scoped
    state=open_sprint(root,path,clock=lambda:1000);assert state['deadline_unix']==22600
    value['balance_observed_unix']=1100.;atomic(path,value)
    assert open_sprint(root,path,resume=True,clock=lambda:1100)['deadline_unix']==22600
    value['instance_started_unix']=1100.;atomic(path,value)
    with pytest.raises(Incomplete,match='identity'):open_sprint(root,path,resume=True,clock=lambda:1100)


@pytest.fixture
def local_repo(tmp_path):
    repo=tmp_path/'repo';repo.mkdir();git(repo,'init','-b','optimization/cargo-actuator-tracking');git(repo,'config','user.name','CPU fixture');git(repo,'config','user.email','fixture@example.invalid')
    folder=repo/'tasks/cargo-bar-controlled-release';folder.mkdir(parents=True)
    atomic(folder/'scene.json',{'slug':'cargo-bar-controlled-release','physics_dt':1/960,'not_physics':True})
    atomic(folder/'native-cases.json',{'control':[{'name':'retract_controlled_inner_tube'}]})
    hashes={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in folder.iterdir()}
    atomic(folder/'source_manifest.json',{'files':hashes});git(repo,'add','.');git(repo,'commit','-m','CPU fixture, not a simulation')
    cargo=git(repo,'rev-parse','HEAD');git(repo,'checkout','-b','recovery/cloud-cpu-engineering')
    coor=repo/'coordination';coor.mkdir();shutil.copytree(HERE,coor/'brev_transfer')
    for name in ['engine.py','brev_policy.py','session_budget.py','sprint_state.py']:shutil.copyfile(HERE.parent/name,coor/name)
    m=read(coor/'brev_transfer/HANDOFF_MANIFEST.json');m['candidates']['cargo']['commit']=cargo
    m['source_files_sha256']={'coordination/engine.py':hashlib.sha256((coor/'engine.py').read_bytes()).hexdigest()}
    atomic(coor/'brev_transfer/HANDOFF_MANIFEST.json',m)
    inventory=[dict(c,diagnostic_only=True) for c in m['candidates'].values()]
    atomic(coor/'recovery/diagnostic-sources.json',{'tasks':inventory})
    atomic(coor/'recovery/source-verification/cargo-4740eba/summary.json',{'source_commit':cargo,'passed':True,'not_physics':True})
    git(repo,'add','.');git(repo,'commit','-m','CPU transfer fixture');ops=git(repo,'rev-parse','HEAD')
    root=tmp_path/'data';root.mkdir();protected=root/'benchmark-tasks';protected.mkdir();(protected/'raw-evidence').write_text('MUST PRESERVE')
    env=dict(os.environ,ROBOCURVE_TRANSFER_TEST_MODE='1',ROBOCURVE_TRANSFER_TEST_ROOT=str(root),ROBOCURVE_TRANSFER_TEST_REPO=str(repo),PYTHONDONTWRITEBYTECODE='1')
    return repo,ops,cargo,root,env


def bootstrap(local_repo):
    repo,ops,cargo,root,env=local_repo
    return subprocess.run(['/bin/bash',str(HERE/'bootstrap.sh'),'--ops-ref',ops],env=env,text=True,capture_output=True)


def test_actual_bootstrap_is_repeatable_independent_and_preserves_work(local_repo):
    repo,ops,cargo,root,env=local_repo
    first=bootstrap(local_repo);assert first.returncode==0,first.stderr
    state=read(root/'robocurve-sprint/handoff-state.json')
    second=bootstrap(local_repo);assert second.returncode==0,second.stderr
    assert read(root/'robocurve-sprint/handoff-state.json')==state
    assert git(root/'robocurve-ops','rev-parse','HEAD')==ops and git(root/'robocurve-task-cargo','rev-parse','HEAD')==cargo
    assert (root/'benchmark-tasks/raw-evidence').read_text()=='MUST PRESERVE'
    assert not git(root/'robocurve-ops','status','--porcelain') and not git(root/'robocurve-task-cargo','status','--porcelain')


def test_dirty_or_unrelated_existing_folder_is_never_replaced(local_repo):
    repo,ops,cargo,root,env=local_repo;assert bootstrap(local_repo).returncode==0
    marker=root/'robocurve-ops/UNTRACKED_WORK';marker.write_text('preserve')
    result=bootstrap(local_repo);assert result.returncode!=0 and marker.read_text()=='preserve'
    marker.unlink();git(root/'robocurve-ops','remote','set-url','origin','https://example.invalid/unrelated.git')
    assert bootstrap(local_repo).returncode!=0
    assert git(root/'robocurve-ops','remote','get-url','origin')=='https://example.invalid/unrelated.git'


def test_existing_nonrepository_is_never_overwritten(local_repo):
    repo,ops,cargo,root,env=local_repo;(root/'robocurve-ops').mkdir();marker=root/'robocurve-ops/private-work';marker.write_text('keep')
    assert bootstrap(local_repo).returncode!=0 and marker.read_text()=='keep'


def test_dry_scripts_cannot_call_provider_gpu_or_authentication(tmp_path):
    stub=tmp_path/'bin';stub.mkdir();log=tmp_path/'FORBIDDEN'
    for name in ('brev','nvidia-smi','gh','codex','tmux','ssh','git'):
        file=stub/name;file.write_text('#!/bin/sh\necho forbidden >> "$FORBIDDEN_LOG"\nexit 93\n');file.chmod(0o755)
    env=dict(os.environ,PATH=str(stub)+':'+os.environ['PATH'],FORBIDDEN_LOG=str(log),PYTHONDONTWRITEBYTECODE='1')
    for command in [ ['/bin/bash',str(HERE/'bootstrap.sh'),'--dry-run','--ops-ref','a'*40],
                     ['/bin/bash',str(HERE/'run_first_diagnostic.sh'),'--dry-run'] ]:
        result=subprocess.run(command,env=env,text=True,capture_output=True);assert result.returncode==0,result.stderr
    assert not log.exists()


def test_completed_failed_or_running_diagnostics_are_not_repeated(tmp_path):
    for status in ('PASS','FAILED','RUNNING'):
        atomic(tmp_path/'ledger.json',{'tasks':{'cargo-bar-controlled-release':{'BOUNDED_NATIVE_DIAGNOSTIC':[{'status':status}]}}})
        with pytest.raises(Incomplete):transfer.check_diagnostic_history(tmp_path)


def test_only_verified_same_scoped_session_can_continue_with_aged_observation(scoped):
    root,path,value=scoped;state=open_sprint(root,path,clock=lambda:1000)
    assert open_sprint(root,path,resume=True,clock=lambda:2000)['deadline_unix']==22600
    assert read(path)['balance_observed_unix']==1000  # No invented fresh provider fact.
    bad=dict(state,identity=dict(state['identity'],gpu_uuid='different'))
    with pytest.raises(Incomplete,match='five minutes'):session(path,deadline=22600,clock=lambda:2000,resume_state=bad)
    with pytest.raises(Incomplete,match='six hours'):session(path,deadline=23600,clock=lambda:2000,resume_state=state)


def test_free_preflight_checks_remote_cli_auth_without_printing_auth_output(local_repo,tmp_path):
    repo,ops,cargo,root,env=local_repo;assert bootstrap(local_repo).returncode==0
    shim=tmp_path/'shim';shim.mkdir()
    for name,body in {'gh':'printf aryansennthilkumarGT','codex':'echo FORMAT_FIXTURE_SECRET_MUST_NOT_LEAK; echo FORMAT_FIXTURE_SECRET_MUST_NOT_LEAK >&2; exit 0','tmux':'exit 0'}.items():
        file=shim/name;file.write_text('#!/bin/sh\n'+body+'\n');file.chmod(0o755)
    active=dict(env,PATH=str(shim)+':'+env['PATH'])
    script=root/'robocurve-ops/coordination/brev_transfer/preflight.sh'
    result=subprocess.run(['/bin/bash',str(script),'--free'],env=active,text=True,capture_output=True)
    assert result.returncode==0,result.stderr
    assert 'SECRET_MUST_NOT_LEAK' not in result.stdout+result.stderr
    data=json.loads(result.stdout);assert data['passed'] and not data['native_executed'] and not data['provider_queried']
    state=read(root/'robocurve-sprint/handoff-state.json')
    assert data['session_run_root']==str(root/'robocurve-sprint/sessions'/state['authorization_session_id'])
    (shim/'codex').write_text('#!/bin/sh\nexit 1\n')
    denied=subprocess.run(['/bin/bash',str(script),'--free'],env=active,text=True,capture_output=True)
    assert denied.returncode==2 and 'not authenticated' in denied.stderr


def test_clean_but_different_task_commit_is_never_reset(local_repo):
    repo,ops,cargo,root,env=local_repo;assert bootstrap(local_repo).returncode==0
    task=root/'robocurve-task-cargo';git(task,'config','user.name','CPU fixture');git(task,'config','user.email','fixture@example.invalid')
    (task/'WORK_TO_PRESERVE').write_text('Committed user work')
    git(task,'add','.');git(task,'commit','-m','CPU fixture user work');changed=git(task,'rev-parse','HEAD')
    result=bootstrap(local_repo);assert result.returncode!=0
    assert git(task,'rev-parse','HEAD')==changed and (task/'WORK_TO_PRESERVE').read_text()=='Committed user work'


def test_native_only_runtime_probe_does_not_require_dream_or_upload_auth(monkeypatch,tmp_path):
    module_spec=importlib.util.spec_from_file_location('runtime_probe_fixture',HERE/'runtime_probe.py')
    probe=importlib.util.module_from_spec(module_spec);module_spec.loader.exec_module(probe)
    monkeypatch.setattr(probe,'hardware',lambda:{'problems':[],'selected_gpu':{'uuid':'NO_GPU_TEST','name':'L40S','driver':'565.57.01'},'credentials_present':{'dream':False,'robocurve':False}})
    calls=[]
    def installed(root,lock,require_dream=True):calls.append(require_dream);return {'not_native_evidence':True}
    monkeypatch.setattr(probe,'launchable_runtime',installed)
    assert probe.probe(tmp_path,'diagnostic')['dream_auth_required'] is False and calls==[False]
    with pytest.raises(Incomplete,match='Qualification needs'):probe.probe(tmp_path,'qualification')
    assert calls[-1] is True


def test_six_hour_deadline_cannot_be_extended_when_money_remains(scoped):
    root,path,value=scoped;open_sprint(root,path,clock=lambda:1000)
    with pytest.raises(Incomplete,match='six hours'):open_sprint(root,path,resume=True,clock=lambda:22601)


def test_provider_wizard_preserves_observations_and_cannot_reset_start(scoped,monkeypatch):
    import session_budget,sprint_state
    root,path,value=scoped
    monkeypatch.setattr(transfer,'paths',lambda:{'sprint':root})
    monkeypatch.setattr(transfer,'data_root',lambda:root.parent)
    original_session=session_budget.session;original_open=sprint_state.open_sprint
    def checked_session(*args,**kwargs):kwargs['clock']=lambda:1000;return original_session(*args,**kwargs)
    def checked_open(*args,**kwargs):kwargs['clock']=lambda:1000;return original_open(*args,**kwargs)
    monkeypatch.setattr(session_budget,'session',checked_session);monkeypatch.setattr(sprint_state,'open_sprint',checked_open)
    facts=iter(['2','20','1970-01-01T00:16:40+00:00','1970-01-01T00:16:40+00:00','NO_GPU_TEST','NO_GPU_TEST','SYNTHETIC_NOT_PROVIDER_DATA','CONFIRMED','STARTED'])
    monkeypatch.setattr('builtins.input',lambda prompt:next(facts))
    transfer.record_provider()
    pointer=root/'active-provider-receipt.json';before=pointer.read_bytes();receipt=read(Path(read(pointer)['receipt']))
    assert receipt['authorized_session_spend_usd']==15. and receipt['estimated_shutdown_trigger_usd']==13.5
    assert read(transfer.active_run()/'sprint-session.json')['deadline_unix']==22600
    changed=iter(['2','20','1970-01-01T00:16:50+00:00','1970-01-01T00:16:50+00:00','NO_GPU_TEST','NO_GPU_TEST','SYNTHETIC_NOT_PROVIDER_DATA','CONFIRMED','STARTED'])
    monkeypatch.setattr('builtins.input',lambda prompt:next(changed))
    with pytest.raises(Incomplete,match='reset spending'):transfer.record_provider()
    assert pointer.read_bytes()==before
