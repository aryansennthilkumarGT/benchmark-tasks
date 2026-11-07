"""Print a native run command, or explicitly execute it on the required workstation.

No evaluator credentials are read or printed. Run artifacts stay outside the task branch.
This launcher does not upload media and never opens a pull request.
"""
import argparse
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys


def command(mode,output,model):
    here=Path(__file__).resolve().parent
    spec=json.loads((here/'scene.json').read_text(encoding='utf-8'))
    cmd=['inspect-robots','run','--embodiment','yam_arena','-E',f'task={here/"task.py"}',
         '-E','object_jitter=0','-E','control_hz=20','-E','cam_width=320','-E','cam_height=176',
         '--instruction',spec['instruction'],'--scorer','task_score','--max-steps',str(spec['run_limit']),
         '--seed','0','--store-frames','--log-dir',str(output)]
    if mode=='expert':cmd+=['--policy','yam_scripted']
    else:cmd+=['--policy','dream','-P',f'model={model}']
    return cmd


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--mode',choices=['expert','dream'],required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--model',default='dreamlabs/dream-1-beta')
    parser.add_argument('--execute',action='store_true')
    args=parser.parse_args()
    cmd=command(args.mode,args.output.resolve(),args.model)
    print(shlex.join(cmd))
    if not args.execute:
        print('DRY RUN ONLY. Complete mechanism/controller/novelty gates and verify installed CLI compatibility first.')
        return 0
    if args.mode=='dream':
        validation=json.loads((Path(__file__).resolve().parent/'validation.json').read_text())
        trials=validation.get('expert_trials',[])
        if (validation.get('physics')!='PASS' or len(trials)<2
                or any(t.get('score')!=1.0 or not t.get('verified') for t in trials[:2])):
            raise SystemExit('Dream execution is blocked until native physics and two full-score expert trials are verified.')
    if sys.platform!='linux':raise SystemExit('Native execution requires the verified Linux RTX 4090 workstation.')
    gpu=subprocess.run(['nvidia-smi','--query-gpu=name,memory.free,utilization.gpu','--format=csv,noheader'],
                       check=True,capture_output=True,text=True)
    if not gpu.stdout.splitlines() or 'RTX 4090' not in gpu.stdout.splitlines()[0]:
        raise SystemExit('Required RTX 4090 is not CUDA device 0.')
    # No overwriting existing trials or silently appending to their evidence.
    args.output.mkdir(parents=True,exist_ok=False)
    env=os.environ.copy();env['ROBOCURVE_TRACE']=str(args.output.resolve()/'native_frames.jsonl')
    record={'status':'STARTED_NOT_COMPLETE','mode':args.mode,'model':args.model if args.mode=='dream' else None,
            'seed':0,'command':cmd,'gpu_diagnostic':gpu.stdout.strip()}
    (args.output/'run_status.json').write_text(json.dumps(record,indent=2)+'\n')
    result=subprocess.run(cmd,env=env)
    record['status']='PROCESS_EXITED_REQUIRES_EVIDENCE_REVIEW';record['returncode']=result.returncode
    (args.output/'run_status.json').write_text(json.dumps(record,indent=2)+'\n')
    return result.returncode


if __name__=='__main__':raise SystemExit(main())
