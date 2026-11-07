"""Independent one-task native verification; no handoff branch or private imports.

Default is a dry run. In the official pinned environment, --execute performs the
native probes and two separate expert episodes. --model adds Dream and media only
after both demonstrations have been independently verified. No uploads or PRs.
"""
import argparse
import json
from pathlib import Path
import subprocess
import sys
sys.dont_write_bytecode=True
from run_ledger import Incomplete,Ledger,atomic,execute,exclusive,fingerprint,read
from validate_rollout import inspect_log,require

HERE=Path(__file__).resolve().parent


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--execute',action='store_true')
    parser.add_argument('--model',action='store_true')
    parser.add_argument('--resume',action='store_true')
    parser.add_argument('--retry-failed',metavar='REASON')
    args=parser.parse_args(argv);root=args.output.resolve();spec=read(HERE/'scene.json')
    commit=subprocess.run(['git','rev-parse','HEAD'],cwd=HERE,text=True,capture_output=True,check=True).stdout.strip()
    stages=['NATIVE_PHYSICS_PASSED','ROBOT_CONTROL_PASSED','EXPERT_DEMO_1_PASSED','EXPERT_DEMO_2_PASSED']
    if args.model:stages+=['MODEL_EVALUATED','MEDIA_RENDERED']
    if not args.execute:
        print(json.dumps({'kind':'DRY_RUN','commit':commit,'stages':stages,'output':str(root),'run_limit':spec['run_limit']},indent=2));return 0
    require(sys.platform=='linux','Native execution requires the official Linux GPU environment')
    require(not subprocess.run(['git','status','--porcelain'],cwd=HERE,text=True,capture_output=True,check=True).stdout.strip(),'Checkout must be clean')
    require(not root.is_relative_to(HERE.parent.parent),'Keep evidence outside the Git checkout')
    python=sys.executable;slug=HERE.name;records={}
    with exclusive(root/'task.lock'):
        ledger=Ledger(root,args.resume,args.retry_failed)
        def stage(name,action):
            row=ledger.stage(slug,name,{'commit':commit,'prerequisites':{k:v['key'] for k,v in records.items()}},action)
            records[name]=row;return row
        def native(out,mode):
            cases=read(HERE/'native-cases.json')[mode]
            steps=sum(c.get('max_steps',c.get('steps',0)+c.get('settle_steps',20)) for c in cases)*2
            execute([python,str(HERE/'native_tests.py'),'--mode',mode,'--output',str(out/'native'),'--commit',commit],
                    HERE,out/'process.log',max(1800,steps//20*8))
            report=read(out/'native/results.json');expected={(c['name'],r) for c in cases for r in (0,1)}
            require(report['kind']=='NATIVE_PHYSX_TESTS' and report['commit']==commit and report['mode']==mode,'Native provenance mismatch')
            actual={(c['name'],c['repeat']) for c in report['cases'] if c['status']=='PASS'}
            require(actual==expected and len(report['cases'])==len(expected) and report['failed']==0 and report['reset_count']==len(expected),'Native suite incomplete')
            return report
        stage(stages[0],lambda out:native(out,'physics'))
        stage(stages[1],lambda out:native(out,'control'))
        proof=root/slug/'feasibility.json'
        def trial(out,mode):
            cmd=[python,str(HERE/'run.py'),'--mode',mode,'--output',str(out/'trial'),'--commit',commit,'--execute']
            if mode=='dream':cmd+=['--evidence',str(proof)]
            execute(cmd,HERE,out/'process.log',max(1800,spec['run_limit']//20*8))
            result=inspect_log(out/'trial',mode,spec['run_limit'],commit,HERE)
            atomic(out/'trial/validated-rollout.json',result);return result
        experts=[stage(name,lambda out:trial(out,'expert')) for name in stages[2:4]]
        require(len({row['result']['record_id'] for row in experts})==2,'Expert trial was reused')
        atomic(proof,{'commit':commit,'physics':records[stages[0]],'control':records[stages[1]],'experts':experts})
        report={'status':'EXPERT_DEMONSTRATIONS_VERIFIED','commit':commit,'expert_scores':[r['result']['score'] for r in experts],
                'ready_for_submission':False,'media_uploaded':False}
        if args.model:
            require(read(HERE/'mechanics-review.json')['novelty_review']['decision']=='CLEARED','Novelty review remains unresolved')
            dream=stage('MODEL_EVALUATED',lambda out:trial(out,'dream'))
            def media(out):
                atomic(out/'inputs.json',{'experts':[r['result'] for r in experts],'dream':dream['result'],
                                         'camera_coverage':records[stages[0]]['result']['camera_coverage']})
                execute([python,str(HERE/'render_media.py'),'--inputs',str(out/'inputs.json'),'--folder',str(HERE),
                         '--output',str(out/'media')],HERE,out/'process.log',1800)
                return read(out/'media/media-validation.json')
            stage('MEDIA_RENDERED',media)
            report.update(status='LOCAL_MEDIA_RENDERED_VISUAL_REVIEW_REQUIRED',dream_score=dream['result']['score'])
        atomic(root/'report.json',report);print(json.dumps(report,indent=2))
    return 0


if __name__=='__main__':
    try:raise SystemExit(main())
    except (Incomplete,OSError,ValueError,KeyError) as exc:
        print(str(exc),file=sys.stderr);raise SystemExit(2)
