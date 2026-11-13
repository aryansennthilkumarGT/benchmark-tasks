"""Rank and dry-run a six-hour qualification/submission window; preview by default.

No provisioning, instance connection, media upload or official PR occurs in a
preview. Execute only in a newly authorized runtime with freshly observed billing
facts. Candidate failures preserve receipts and advance; success at three never
stops the loop. Media awaits genuine visual review, then --resume continues.
"""
import argparse,json,sys,time
from pathlib import Path
from engine import Incomplete,atomic,read
from sprint_state import open_sprint
import pipeline


def ranked(manifest):
    tasks=pipeline.selected(manifest,None)
    # Quality gate outranks speed. Seconds are offline planning assumptions until
    # replaced by actual receipt timings; they are never reported as measured.
    return sorted(tasks,key=lambda t:(t.get('offline_state')!='OFFLINE READY',t.get('priority',99),
                                      t.get('estimated_qualification_seconds',7200)))


def verify_ready(tasks, manifest, manifest_path):
    """Resolve evidence from an explicit manifest-relative root, never cwd."""
    from offline_gate import verify
    root=(Path(manifest_path).resolve().parent / manifest.get('offline_evidence_root','.')).resolve()
    return [verify(task,root) for task in tasks if task.get('offline_state')=='OFFLINE READY']


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--manifest',type=Path,required=True);p.add_argument('--run-root',type=Path,required=True)
    p.add_argument('--verify-offline',action='store_true',help='Read and verify source-bound bundles during the pure preview')
    p.add_argument('--execute',action='store_true');p.add_argument('--resume',action='store_true')
    p.add_argument('--retry-failed',metavar='REASON',help='One ledger-bounded retry after a substantive external repair')
    p.add_argument('--budget-file',type=Path);p.add_argument('--launchable-root',type=Path)
    p.add_argument('--registered-account');p.add_argument('--submit',action='store_true')
    a=p.parse_args(argv);m=read(a.manifest);tasks=ranked(m)
    plan=pipeline.plan(tasks,a.run_root,read(pipeline.HERE/'stack-lock.json'))
    plan.update(maximum_session_seconds=21600,stop_after_three=False,target_new_prs=3,submit_each_ready_task_immediately=True,
      minimum_qualified_candidates_to_begin=1,first_action='Bounded cargo diagnostic after actual start/spend authorization',automatic_provisioning=False,
      billing_shutdown='Workload termination does not stop billing. Authorized operator must stop the existing instance.',
      ranking=[dict(slug=t['slug'],priority=t.get('priority'),offline_state=t.get('offline_state'),
                    timing_basis=t.get('timing_basis','OFFLINE_ASSUMPTION')) for t in tasks],
      blocked=[t['slug'] for t in tasks if t.get('offline_state')!='OFFLINE READY'])
    if not a.execute:
        if a.verify_offline:
            bundles=verify_ready(tasks,m,a.manifest)
            plan['verified_offline_bundles']=[dict(slug=b['slug'],published_commit=b['published_commit'],tested_source_commit=b['tested_source_commit']) for b in bundles]
        print(json.dumps(plan,indent=2));return 0
    if not a.budget_file or not a.launchable_root:raise Incomplete('Fresh provider receipt and installed runtime are required')
    ready=[t for t in tasks if t.get('offline_state')=='OFFLINE READY']
    if not ready:raise Incomplete('No candidate meets the per-task qualification gate; run the authorized bounded diagnostic/repair loop first')
    verify_ready(ready,m,a.manifest)
    if a.submit and not a.registered_account:raise Incomplete('Registered account required before paid sprint submission')
    state=open_sprint(a.run_root,a.budget_file,resume=a.resume)
    # Never rerun evaluations for heads already created during this sprint.
    created={row['slug'] for row in state.get('created_prs',{}).values()}
    ready=[task for task in ready if task['slug'] not in created]
    if not ready:
        print('No unsubmitted qualified candidates; continue targeted repairs/real visual review within the original session budget.')
        return 2
    a.run_root.mkdir(parents=True,exist_ok=True)
    runtime_manifest=a.run_root/'ranked-source-manifest.json'
    evidence_root=(a.manifest.resolve().parent / m.get('offline_evidence_root','.')).resolve()
    atomic(runtime_manifest,dict(m,tasks=ready,offline_evidence_root=str(evidence_root)))
    args=['--all','--manifest',str(runtime_manifest),'--run-root',str(a.run_root),
          '--budget-file',str(a.budget_file),'--launchable-root',str(a.launchable_root),
          '--deadline-unix',str(state['deadline_unix'])]
    if a.resume:args+=['--resume']
    if a.retry_failed:args+=['--retry-failed',a.retry_failed]
    if a.submit:args+=['--submit','--registered-account',a.registered_account]
    code=pipeline.main(args)
    return code

if __name__=='__main__':
    try:raise SystemExit(main())
    except (Incomplete,ValueError,OSError,KeyError) as exc:print('BLOCKED: '+str(exc),file=sys.stderr);raise SystemExit(3)
