"""Rank and dry-run a six-hour qualification/submission window; preview by default.

No provisioning, instance connection, media upload or official PR occurs in a
preview. Execute only in a newly authorized runtime with freshly observed billing
facts. Candidate failures preserve receipts and advance; success at three never
stops the loop. Media awaits genuine visual review, then --resume continues.
"""
import argparse,json,sys,time
from pathlib import Path
from engine import Incomplete,atomic,read
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
    p.add_argument('--budget-file',type=Path);p.add_argument('--launchable-root',type=Path)
    p.add_argument('--registered-account');p.add_argument('--submit',action='store_true')
    a=p.parse_args(argv);m=read(a.manifest);tasks=ranked(m)
    plan=pipeline.plan(tasks,a.run_root,read(pipeline.HERE/'stack-lock.json'))
    plan.update(maximum_session_seconds=21600,stop_after_three=False,automatic_provisioning=False,
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
    if len(ready)<3:raise Incomplete('Fewer than three candidates meet the offline gate; do not start paid qualification')
    verify_ready(ready,m,a.manifest)
    a.run_root.mkdir(parents=True,exist_ok=True)
    runtime_manifest=a.run_root/'ranked-source-manifest.json'
    evidence_root=(a.manifest.resolve().parent / m.get('offline_evidence_root','.')).resolve()
    atomic(runtime_manifest,dict(m,tasks=ready,offline_evidence_root=str(evidence_root)))
    args=['--all','--manifest',str(runtime_manifest),'--run-root',str(a.run_root),
          '--budget-file',str(a.budget_file),'--launchable-root',str(a.launchable_root),
          '--deadline-unix',str(time.time()+21600)]
    if a.resume:args+=['--resume']
    code=pipeline.main(args)
    # Submit genuinely ready tasks even when another candidate failed or awaits
    # review. Existing submit_ready verifies every immutable mandatory receipt.
    handoff=a.run_root/'ready-handoff.json'
    if a.submit and handoff.exists() and read(handoff)['tasks']:
        from submit_ready import main as submit
        submit_args=[str(handoff),'--execute']
        if a.registered_account:submit_args+=['--registered-account',a.registered_account]
        submit(submit_args)
    return code

if __name__=='__main__':
    try:raise SystemExit(main())
    except (Incomplete,ValueError,OSError,KeyError) as exc:print('BLOCKED: '+str(exc),file=sys.stderr);raise SystemExit(3)
