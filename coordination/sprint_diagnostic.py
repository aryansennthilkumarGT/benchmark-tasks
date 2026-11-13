"""Budgeted native prefix inside the same continuous sprint. Preview by default.

No provisioning or provider connection. --execute is for the already authorized
existing Launchable, with genuine provider facts, credentials and installed SDK.
A passed prefix never qualifies a full task or authorizes Dream/submission.
"""
import argparse,json,sys
from pathlib import Path
from engine import Incomplete,Ledger,atomic,digest,execute,read,exclusive
from environment import hardware,launchable_runtime,capture
from sprint_state import open_sprint
from session_budget import session

HERE=Path(__file__).resolve().parent


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--task-folder',type=Path,required=True);p.add_argument('--commit',required=True)
    p.add_argument('--case',required=True);p.add_argument('--run-root',type=Path,required=True)
    p.add_argument('--budget-file',type=Path);p.add_argument('--launchable-root',type=Path,default=Path('/data'))
    p.add_argument('--registered-account');p.add_argument('--execute',action='store_true');p.add_argument('--resume',action='store_true')
    p.add_argument('--timeout-seconds',type=int,default=1200)
    a=p.parse_args(argv)
    if not 1<=a.timeout_seconds<=1200:raise Incomplete('Native diagnostic must be bounded to at most20minutes')
    folder=a.task_folder.resolve();spec=read(folder/'scene.json')
    cases=[row for row in read(folder/'native-cases.json')['control'] if row['name']==a.case]
    if len(cases)!=1:raise Incomplete('Choose an actual declared native control case')
    frequency=round(1/spec['physics_dt'])
    def command(python,out):
        return [python,str(HERE/'diagnostic_native.py'),'--folder',str(folder),'--mode','control',
                '--case',a.case,'--commit',a.commit,'--output',str(out/'native'),
                '--expected-physics-hz',str(frequency),'--render-every','1','--sdk-limits','--fail-fast']
    if not a.execute:
        print(json.dumps({'kind':'DRY_RUN_NO_PAID_WORK','stage':'BOUNDED_NATIVE_PREFIX_NOT_QUALIFICATION',
            'command':command('/data/IsaacLab-Arena/.venv/bin/python',a.run_root/'diagnostic-preview'),
            'timeout_seconds':a.timeout_seconds,'required_authorization':'Actual user start approval and explicit cap'},indent=2));return 0
    if not a.budget_file or not a.registered_account:raise Incomplete('Actual provider receipt and registered account required')
    root=a.run_root.resolve();state=open_sprint(root,a.budget_file,resume=a.resume)
    budget=session(a.budget_file,deadline=state['deadline_unix'])
    observed=hardware()
    if observed['problems']:raise Incomplete('; '.join(observed['problems']))
    if observed['selected_gpu']['uuid']!=budget.receipt['gpu_uuid']:raise Incomplete('Provider receipt names a different GPU')
    if not all(observed['credentials_present'].get(k) for k in ('dream','robocurve','github_cli')):
        raise Incomplete('Configure existing session credentials securely before paid work; no token values are recorded')
    if capture(['gh','api','user','--jq','.login'])!=a.registered_account:raise Incomplete('Wrong registered GitHub account')
    installed=launchable_runtime(a.launchable_root,read(HERE/'stack-lock.json'))
    if capture(['git','rev-parse','HEAD'],folder)!=a.commit or capture(['git','status','--porcelain'],folder):
        raise Incomplete('Native diagnostic requires the exact clean task source')
    ledger=Ledger(root,resume=a.resume)
    def action(out):
        atomic(out/'preflight.json',{'hardware':observed,'runtime':installed,'not_credentials':True})
        execute(command(installed['python'],out),folder,out/'process.log',a.timeout_seconds,budget=budget)
        report=read(out/'native/results.json')
        coverage={(row['name'],row['repeat']) for row in report['cases'] if row['status']=='PASS'}
        if (report.get('status')!='PASS' or report.get('commit')!=a.commit or report.get('failed')!=0
                or coverage!={(a.case,0),(a.case,1)} or len(report['cases'])!=2):
            raise Incomplete('Native prefix reset/repeat evidence incomplete')
        return {'kind':'BOUNDED_NATIVE_PREFIX','commit':a.commit,'passed':True,
                'case':a.case,'full_task_qualified':False,'native_report':'native/results.json'}
    with exclusive(root/'pipeline.lock'):
        ledger.stage(spec['slug'],'BOUNDED_NATIVE_DIAGNOSTIC',{'commit':a.commit,'case':a.case,
                     'wrapper':digest(HERE/'diagnostic_native.py'),'native_script':digest(folder/'native_tests.py'),
                     'gpu':observed['selected_gpu'],'timeout_seconds':a.timeout_seconds},action)
    return 0
if __name__=='__main__':
    try:raise SystemExit(main())
    except (Incomplete,OSError,ValueError,KeyError) as exc:print('BLOCKED: '+str(exc),file=sys.stderr);raise SystemExit(2)
