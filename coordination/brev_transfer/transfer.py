"""Source-pinned transfer and native-only preflight. Never controls Brev billing."""
from __future__ import annotations
import argparse,datetime,hashlib,json,os,re,shutil,subprocess,sys,tempfile,uuid
from pathlib import Path

HERE=Path(__file__).resolve().parent
OPS=HERE.parents[1]
sys.path.insert(0,str(OPS/'coordination'))
from engine import Incomplete,atomic,digest,read,Budget,exclusive
from brev_policy import POLICY_ID,INSTANCE,AUTHORIZATION_REFERENCE,STOP_COMMAND


def data_root():
    if os.environ.get('ROBOCURVE_TRANSFER_TEST_MODE')=='1':
        return Path(os.environ['ROBOCURVE_TRANSFER_TEST_ROOT']).resolve()
    return Path('/data')


def paths(root=None):
    root=root or data_root()
    return {'ops':root/'robocurve-ops','cargo':root/'robocurve-task-cargo','sprint':root/'robocurve-sprint'}


def active_run():
    p=paths();state=read(p['sprint']/'handoff-state.json')
    return p['sprint']/'sessions'/state['authorization_session_id']


def run(command,cwd=None,timeout=60):
    result=subprocess.run([str(v) for v in command],cwd=cwd,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=timeout)
    if result.returncode:raise Incomplete('Command failed: '+str(command[0])+'. Check local availability/access; source and evidence were preserved.')
    return result.stdout.strip()


def remote_identity(value):
    if value.startswith('git@github.com:'):value='https://github.com/'+value.split(':',1)[1]
    return value.removesuffix('.git').rstrip('/')


def verify_checkout(folder,commit,repository):
    if folder.is_symlink():raise Incomplete('Refusing a symlink at a managed checkout path')
    if run(['git','rev-parse','--show-toplevel'],folder)!=str(folder.resolve()):raise Incomplete('Managed path is not its own Git repository')
    if remote_identity(run(['git','remote','get-url','origin'],folder))!=remote_identity(repository):raise Incomplete('Existing repository identity differs; no replacement attempted')
    if run(['git','status','--porcelain','--untracked-files=all'],folder):raise Incomplete('Existing checkout is dirty; do not delete/reset it')
    if run(['git','rev-parse','HEAD'],folder)!=commit:raise Incomplete('Existing checkout differs from exact handoff SHA; no reset attempted')


def writable(folder):
    if not folder.resolve().is_relative_to(data_root().resolve()):raise Incomplete('Output path escapes the dedicated data root')
    folder.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryFile(dir=folder) as stream:stream.write(b'local permission probe')


def source_manifest(folder):
    manifest=read(folder/'source_manifest.json')
    for name,expected in manifest['files'].items():
        file=(folder/name).resolve()
        if not file.is_relative_to(folder.resolve()) or not file.is_file():raise Incomplete('Missing/escaping task manifest file')
        if hashlib.sha256(file.read_bytes().replace(b'\r\n',b'\n')).hexdigest()!=expected:raise Incomplete('Task source manifest changed: '+name)


def manifest():return read(HERE/'HANDOFF_MANIFEST.json')


def bootstrap(ops_ref):
    m=manifest();p=paths();repository=m['repository_url']
    if os.environ.get('ROBOCURVE_TRANSFER_TEST_MODE')=='1':repository=os.environ['ROBOCURVE_TRANSFER_TEST_REPO']
    verify_checkout(p['ops'],ops_ref,repository)
    candidate=m['candidates']['cargo'];cargo=p['cargo']
    if cargo.exists():verify_checkout(cargo,candidate['commit'],repository)
    else:
        pending=Path(tempfile.mkdtemp(prefix='robocurve-cargo-transfer-',dir=data_root()))
        run(['git','-c','credential.helper=','-c','credential.helper=!gh auth git-credential','clone','--filter=blob:none','--no-checkout','--single-branch','--branch',candidate['branch'],repository,str(pending)],timeout=180)
        run(['git','config','core.autocrlf','false'],pending)
        run(['git','sparse-checkout','init','--cone'],pending)
        run(['git','sparse-checkout','set',candidate['task_folder'],'tools'],pending)
        run(['git','checkout','--detach',candidate['commit']],pending);verify_checkout(pending,candidate['commit'],repository)
        os.rename(pending,cargo)
    a=(p['ops']/run(['git','rev-parse','--git-common-dir'],p['ops'])).resolve()
    b=(cargo/run(['git','rev-parse','--git-common-dir'],cargo)).resolve()
    if a==b:raise Incomplete('Coordinator and cargo must have independent Git object stores')
    source_manifest(cargo/candidate['task_folder'])
    writable(p['sprint']);state_path=p['sprint']/'handoff-state.json'
    baseline={'coordinator_commit':ops_ref,'cargo_commit':candidate['commit'],'manifest_sha256':digest(HERE/'HANDOFF_MANIFEST.json'),'spending_policy_id':POLICY_ID}
    with exclusive(p['sprint']/'transfer-bootstrap.lock'):
        if state_path.exists():
            state=read(state_path)
            if any(state.get(k)!=v for k,v in baseline.items()):raise Incomplete('Existing handoff session identity differs; preserve it instead of replacing it')
        else:
            state=dict(baseline,authorization_session_id=str(uuid.uuid4()))
            atomic(state_path,state)
    print('BOOTSTRAP COMPLETE: independent exact sources; no GPU/provider calls or environment installation.')
    print('Next: bash '+str(p['ops']/'coordination/brev_transfer/preflight.sh')+' --free')


def required_command(name):
    value=shutil.which(name)
    if not value:raise Incomplete('Missing '+name+'; resolve before native execution. No installer is run.')
    return value


def free_checks():
    m=manifest();p=paths();state=read(p['sprint']/'handoff-state.json')
    repository=m['repository_url']
    if os.environ.get('ROBOCURVE_TRANSFER_TEST_MODE')=='1':repository=os.environ['ROBOCURVE_TRANSFER_TEST_REPO']
    verify_checkout(p['ops'],state['coordinator_commit'],repository)
    verify_checkout(p['cargo'],m['candidates']['cargo']['commit'],repository)
    if state['manifest_sha256']!=digest(HERE/'HANDOFF_MANIFEST.json'):raise Incomplete('Transfer manifest differs from saved handoff')
    if not m.get('source_files_sha256'):raise Incomplete('Transfer source-lock inventory is empty')
    for name,expected in m['source_files_sha256'].items():
        file=(p['ops']/name).resolve()
        if not file.is_relative_to(p['ops'].resolve()) or digest(file)!=expected:raise Incomplete('Transfer tooling source hash differs: '+name)
    a=(p['ops']/run(['git','rev-parse','--git-common-dir'],p['ops'])).resolve()
    b=(p['cargo']/run(['git','rev-parse','--git-common-dir'],p['cargo'])).resolve()
    if a==b:raise Incomplete('Coordinator/task Git stores are not independent')
    source_manifest(p['cargo']/m['candidates']['cargo']['task_folder'])
    inventory=read(p['ops']/'coordination/recovery/diagnostic-sources.json')['tasks']
    for candidate in m['candidates'].values():
        if not any(t['commit']==candidate['commit'] and t['branch']==candidate['branch'] and t.get('diagnostic_only') for t in inventory):raise Incomplete('Candidate differs from source-bound diagnostic inventory')
    proof=read(p['ops']/'coordination/recovery/source-verification/cargo-4740eba/summary.json')
    if proof.get('source_commit')!=m['candidates']['cargo']['commit'] or proof.get('passed') is not True:raise Incomplete('Missing source-bound Cargo offline evidence')
    for name in ('git','python3','gh','tmux','codex'):required_command(name)
    if run(['gh','api','user','--jq','.login'])!=m['registered_github_account']:raise Incomplete('GitHub login differs from registered account')
    # Discard all authentication-status output: never print/store secret material.
    auth=subprocess.run([required_command('codex'),'login','status'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=30)
    if auth.returncode:raise Incomplete('Codex CLI is not authenticated. Authenticate securely on this machine, never in chat/Git.')
    for path in (p['sprint'],p['sprint']/'provider-observations',active_run()):writable(path)
    return {'kind':'FREE_TRANSFER_PREFLIGHT','passed':True,'coordinator_commit':state['coordinator_commit'],
            'cargo_commit':state['cargo_commit'],'session_run_root':str(active_run()),'codex_path':required_command('codex'),
            'native_executed':False,'provider_queried':False,'credentials_printed':False}


def budget_path():
    path=paths()['sprint']/'active-provider-receipt.json'
    pointer=read(path);receipt=Path(pointer['receipt']).resolve()
    if receipt.parent!=(paths()['sprint']/'provider-observations').resolve():raise Incomplete('Budget pointer escapes provider observation directory')
    return receipt


def check_diagnostic_history(sprint):
    ledger=sprint/'ledger.json'
    if not ledger.exists():return
    history=read(ledger).get('tasks',{}).get('cargo-bar-controlled-release',{}).get('BOUNDED_NATIVE_DIAGNOSTIC',[])
    if any(row['status']=='PASS' for row in history):raise Incomplete('Cargo diagnostic already passed: preserve/reuse evidence; do not repeat it')
    if history:raise Incomplete('Prior failed/interrupted diagnostic exists: inspect it and make a supported repair; no automatic retry')


def gpu_checks(stage='diagnostic'):
    p=paths()
    if os.environ.get('ROBOCURVE_TRANSFER_TEST_MODE'):raise Incomplete('Test mode can never execute GPU checks')
    if stage=='diagnostic':check_diagnostic_history(active_run())
    receipt=budget_path();cost=Budget(receipt);cost.check(180)
    from session_budget import session
    state_path=active_run()/'sprint-session.json'
    if state_path.exists():
        state=read(state_path)
        if state['identity']['instance_started_unix']!=cost.receipt['instance_started_unix'] or state['identity'].get('authorization_session_id')!=cost.receipt['authorization_session_id']:
            raise Incomplete('Resume cannot reset start time/session identity')
        session(receipt,deadline=state['deadline_unix'],resume_state=state)
    else:session(receipt)
    result=free_checks()
    env=data_root()/'IsaacLab-Arena/yam.env';python=data_root()/'IsaacLab-Arena/.venv/bin/python'
    if not env.is_file() or not python.is_file():raise Incomplete('Existing yam.env or pinned Python missing; do not reinstall Isaac/driver')
    probe=[str(python),str(HERE/'runtime_probe.py'),'--root',str(data_root()),'--stage',stage]
    native=json.loads(run(probe))
    if native['gpu_uuid']!=cost.receipt['gpu_uuid']:raise Incomplete('Observed GPU differs from provider receipt')
    return dict(result,kind='GPU_TRANSFER_PREFLIGHT',runtime=native,budget=cost.check(),stage=stage)


def record_provider():
    if os.environ.get('ROBOCURVE_TRANSFER_TEST_MODE'):raise Incomplete('Test mode cannot record real provider evidence')
    p=paths();state=read(p['sprint']/'handoff-state.json')
    def prompt(label):
        value=input(label+': ').strip()
        if not value:raise Incomplete('Required provider fact was empty')
        return value
    print('Enter ONLY fresh provider facts, never credentials/tokens. Start/observation times must be provider-observed.')
    rate=float(prompt('Observed GPU hourly USD rate'))
    balance=float(prompt('Observed remaining Brev credits in USD'))
    def timestamp(label):
        value=datetime.datetime.fromisoformat(prompt(label).replace('Z','+00:00'))
        if value.tzinfo is None:raise Incomplete('Use a timezone, for example +00:00 or -05:00')
        return value.timestamp()
    started=timestamp('Actual current instance billing START time (ISO8601 with timezone)')
    observed=timestamp('Time provider BALANCE was observed (ISO8601 with timezone)')
    provider_id=prompt('Actual existing provider instance ID/name')
    gpu_uuid=prompt('Actual GPU UUID from nvidia-smi --query-gpu=uuid --format=csv,noheader')
    evidence=prompt('Provider evidence reference (console observation timestamp/screenshot path, not a token)')
    if prompt('Confirm laptop shutdown command is available; type CONFIRMED ('+STOP_COMMAND+')')!='CONFIRMED':raise Incomplete('Provider stop method must be confirmed before workloads')
    if prompt('Confirm you have started/authorized THIS existing instance; type STARTED')!='STARTED':raise Incomplete('Instance start has not been confirmed')
    from brev_policy import ROOT
    if p['sprint']!=ROOT:raise Incomplete('Scoped policy root differs')
    data={'hourly_usd':rate,'balance_usd':balance,'instance_started_unix':started,'balance_observed_unix':observed,
          'instance_id':provider_id,'instance_name':INSTANCE,'gpu_uuid':gpu_uuid,'provider_evidence':evidence,
          'spent_before_start_usd':0.,'spending_accounting_scope':'NEW_SESSION_ONLY_NOT_HISTORICAL_TOTAL',
          'spending_policy_id':POLICY_ID,'authorization_reference':AUTHORIZATION_REFERENCE,
          'authorization_session_id':state['authorization_session_id'],'authorized_session_spend_usd':15.,
          'estimated_shutdown_trigger_usd':13.5,'provider_stop_command':STOP_COMMAND,'shutdown_method_confirmed':True}
    old=p['sprint']/'active-provider-receipt.json'
    if old.exists():
        previous=read(Path(read(old)['receipt']))
        fixed=('instance_id','gpu_uuid','instance_started_unix','hourly_usd','authorization_session_id')
        if any(previous[k]!=data[k] for k in fixed):raise Incomplete('Provider refresh cannot change instance/start/rate identity or reset spending')
    folder=p['sprint']/'provider-observations';writable(folder)
    target=folder/(datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S')+'-'+uuid.uuid4().hex[:8]+'.json')
    # Only a newly created receipt is written; earlier observations are immutable.
    atomic(target,data)
    try:
        from session_budget import session
        session(target)
    except Exception:
        print('Provider observation preserved, but rejected; do not run native work. Check funds/time or stop the instance.',file=sys.stderr)
        raise
    atomic(old,{'receipt':str(target)})
    from sprint_state import open_sprint
    open_sprint(active_run(),target,resume=(active_run()/'sprint-session.json').exists())
    print('Fresh observation validated; $15 hard cap, $13.50 conservative trigger, six-hour outer deadline. No provider stop was performed.')


def diagnostic(execute=False):
    p=paths();candidate=manifest()['candidates']['cargo']
    command=[str(data_root()/'IsaacLab-Arena/.venv/bin/python'),str(p['ops']/'coordination/sprint_diagnostic.py'),
        '--task-folder',str(p['cargo']/candidate['task_folder']),'--commit',candidate['commit'],
        '--case',candidate['case'],'--run-root',str(active_run() if (p['sprint']/'handoff-state.json').exists() else p['sprint']/'sessions/PERSISTED_SESSION_ID'),'--launchable-root',str(data_root()),
        '--registered-account',manifest()['registered_github_account'],'--timeout-seconds','1200']
    if not execute:
        print(json.dumps({'kind':'DRY_RUN_NO_GPU_OR_PROVIDER_CALLS','command':command,'policy':{'hard_cap_usd':15,'estimated_shutdown_trigger_usd':13.5},'no_auto_dream_media_or_pr':True},indent=2));return
    result=gpu_checks('diagnostic');atomic(active_run()/'first-diagnostic-preflight.json',result)
    command+=['--budget-file',str(budget_path()),'--execute']
    if (active_run()/'sprint-session.json').exists():command+=['--resume']
    # No shell, no pipeline after failure, no implicit provision/start/stop call.
    os.execv(command[0],command)


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='command',required=True)
    p=sub.add_parser('bootstrap');p.add_argument('--ops-ref',required=True)
    p=sub.add_parser('preflight');group=p.add_mutually_exclusive_group(required=True);group.add_argument('--free',action='store_true');group.add_argument('--gpu',action='store_true');group.add_argument('--record-provider-facts',action='store_true');p.add_argument('--stage',choices=('diagnostic','qualification'),default='diagnostic')
    p=sub.add_parser('diagnostic');p.add_argument('--execute',action='store_true');p.add_argument('--dry-run',action='store_true')
    sub.add_parser('launch-codex')
    sub.add_parser('session-path')
    a=parser.parse_args(argv)
    if a.command=='session-path':print(active_run())
    elif a.command=='launch-codex':
        result=free_checks();p=paths();cache=p['sprint']/'cache';writable(cache)
        os.environ.update(PYTHONDONTWRITEBYTECODE='1',XDG_CACHE_HOME=str(cache),CUDA_CACHE_PATH=str(cache/'cuda'))
        command=[result['codex_path'],'--sandbox','workspace-write','--config','sandbox_workspace_write.network_access=true',
                 '--add-dir',str(p['cargo']),'--add-dir',str(p['sprint']),
                 'Read coordination/brev_transfer/START_HERE.md and GPU_RESUME_PLAN.md. Continue the source-pinned continuous RoboCurve sprint, respecting the scoped $15 hard cap/$13.50 trigger. Verify actual preflight/provider facts; no fabricated native evidence or automatic billing-stop claims.']
        os.chdir(p['ops']);os.execv(command[0],command)
    elif a.command=='bootstrap':bootstrap(a.ops_ref)
    elif a.command=='diagnostic':
        if a.execute and a.dry_run:raise Incomplete('Choose dry-run or execute, never both')
        diagnostic(a.execute)
    elif a.record_provider_facts:record_provider()
    else:
        value=gpu_checks(a.stage) if a.gpu else free_checks()
        target=paths()['sprint']
        stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S')+'-'+uuid.uuid4().hex[:8]
        atomic(target/'preflight-observations'/(stamp+'.json'),value)
        atomic(target/('preflight-gpu.json' if a.gpu else 'preflight-free.json'),value)
        print(json.dumps(value,indent=2))
if __name__=='__main__':
    try:main()
    except (Incomplete,OSError,ValueError,KeyError,TypeError,subprocess.TimeoutExpired) as exc:
        print('PREFLIGHT BLOCKED: '+str(exc),file=sys.stderr);sys.exit(2)
