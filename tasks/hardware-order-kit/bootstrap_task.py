"""One-branch bootstrap using the official pinned installer. Preview by default."""
import argparse
import json
import sys
from pathlib import Path
sys.dont_write_bytecode=True
from run_ledger import Budget,Incomplete,Ledger,atomic,digest,execute,exclusive,read
from setup_environment import bootstrap,hardware,launchable_runtime,verify_runtime
HERE=Path(__file__).resolve().parent

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--budget-file',type=Path)
    p.add_argument('--launchable-root',type=Path,help='Verify and reuse an installed pinned Launchable')
    p.add_argument('--execute',action='store_true')
    p.add_argument('--model',action='store_true')
    p.add_argument('--resume',action='store_true')
    p.add_argument('--retry-failed')
    args=p.parse_args(argv);root=args.output.resolve();lock=read(HERE/'stack-lock.json')
    if not args.execute:
        print(json.dumps({'kind':'DRY_RUN','stack':lock,'stages':['bootstrap','official smoke','static checks','native probes','two experts']+(['Dream','media'] if args.model else []),'output':str(root)},indent=2));return 0
    if root.is_relative_to(HERE.parent.parent):raise Incomplete('Evidence directory must be outside the task Git checkout')
    check=hardware()
    if check['problems']:raise Incomplete('; '.join(check['problems']))
    if args.budget_file is None:raise Incomplete('Supply the actual provider cost receipt with --budget-file')
    budget=Budget(args.budget_file)
    if check['selected_gpu']['uuid']!=budget.receipt['gpu_uuid']:raise Incomplete('GPU differs from budget receipt')
    import os
    os.environ['CUDA_VISIBLE_DEVICES']=check['selected_gpu']['uuid']
    if not args.launchable_root and check['driver_status'] == 'fixed_driver_smoke_required':
        raise Incomplete('Fixed driver validation requires --launchable-root with the installed vendor stack')
    runtime_root = args.launchable_root.resolve() if args.launchable_root else root/'stack'
    installed = launchable_runtime(runtime_root, lock) if args.launchable_root else None
    implementation = {name: digest(HERE/name) for name in ('bootstrap_task.py', 'setup_environment.py')}
    with exclusive(root/'bootstrap.lock'):
        ledger=Ledger(root,args.resume,args.retry_failed)
        if installed is not None:
            def reuse(out):
                atomic(out/'installed-runtime.json', installed)
                return installed
            stack=ledger.stage('_environment','REUSE_LAUNCHABLE',
                               {'stack':lock,'runtime':installed,'implementation':implementation},reuse)
        else:
            stack=ledger.stage('_environment','BOOTSTRAP',
                               {'stack':lock,'implementation':implementation},
                               lambda out:bootstrap(runtime_root,lock,out,budget))
        python=stack['result']['python']
        verify_runtime(stack['result'],runtime_root,lock)
        def smoke(out):
            atomic(out/'hardware.json',check)
            trial=out/'trial';trial.mkdir()
            execute([str(Path(python).parent/'inspect-robots'),'run','--embodiment','yam_arena','--policy','yam_scripted','-E','scene=station','-E','object_jitter=0','-E','control_hz=20','-E','cam_width=320','-E','cam_height=176','--instruction','put apple into the bowl','--scorer','success_at_end','--max-steps','600','--store-frames','--seed','0','--environment-revision',lock['adapter']['commit'],'--log-dir',str(trial)],HERE,out/'smoke.log',1800,budget=budget)
            execute([python,str(HERE/'validate_rollout.py'),'--directory',str(trial),'--mode','smoke','--limit','600','--commit',lock['adapter']['commit']],HERE,out/'smoke-validation.log',600,budget=budget)
            return read(trial/'validated-rollout.json')
        gpu_identity = {name: check['selected_gpu'][name] for name in ('name','uuid','driver')}
        ledger.stage('_environment','OFFICIAL_SMOKE',
                     {'stack':lock,'gpu':gpu_identity,'bootstrap':stack['key']},smoke)
        revision=__import__('subprocess').run(['git','rev-parse','HEAD'],cwd=HERE,text=True,capture_output=True,check=True).stdout.strip()
        def static(out):
            execute([python,str(HERE/'static_check.py')],HERE,out/'checks.log',7200,budget=budget)
            return {'status':'PASS','kind':'OFFLINE_CHECKS','commit':revision}
        ledger.stage(HERE.name,'STATIC_TESTS_PASSED',{'commit':revision},static)
        command=[python,str(HERE/'task_runner.py'),'--output',str(root/'task-evidence'),'--execute']
        if args.model:command+=['--model']
        if args.resume:command+=['--resume']
        if args.retry_failed:command+=['--retry-failed',args.retry_failed]
        # The outer budget monitor covers all child subprocesses and kills the
        # owned group if the reserve is reached. It does not stop cloud billing.
        execute(command,HERE,root/'task-runner.log',24*3600,budget=budget)
    return 0
if __name__=='__main__':
    try:raise SystemExit(main())
    except (Incomplete,OSError,ValueError,KeyError) as exc:
        print(str(exc),file=sys.stderr);raise SystemExit(2)
