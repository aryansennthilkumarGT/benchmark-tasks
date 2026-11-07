"""Independent official YAM rollout launcher. Default prints the command only.

Supports official L40S and RTX workstation execution. This script never uploads
media, changes task bodies, or creates pull requests. Dream requires two separately
recorded, validated full-score expert runs of the same source revision.
"""
import argparse
import hashlib
import importlib
import importlib.util
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
sys.dont_write_bytecode=True

HERE=Path(__file__).resolve().parent


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def feasible(path,commit):
    data=json.loads(path.read_text())
    if data['commit']!=commit:raise ValueError('Feasibility revision differs')
    records=[data['physics'],data['control'],*data['experts']]
    if len(records)!=4:raise ValueError('Two separate expert demonstrations required')
    ids=[]
    for record in records:
        if record['status']!='PASS' or record['inputs']['commit']!=commit:raise ValueError('Failed/mismatched prerequisite')
        # Receipts use paths relative to the run root, which feasibility.json lives below.
        root=path.parent.parent
        receipt=(root/record['receipt']).resolve()
        directory=receipt.parent
        if not directory.is_relative_to(root.resolve()):raise ValueError('Evidence path escapes run root')
        if json.loads(receipt.read_text())!=record:raise ValueError('Feasibility record differs from its immutable receipt')
        actual={p.relative_to(directory).as_posix():sha(p) for p in directory.rglob('*')
                if p.is_file() and p.name!='receipt.json'}
        if actual!=record['artifacts']:raise ValueError('Prerequisite evidence missing or changed')
    for record in data['experts']:
        result=record['result']
        if result['score']!=1 or result['mode']!='expert':raise ValueError('Full-score experts required')
        ids.append(result['record_id'])
    if len(set(ids))!=2:raise ValueError('Expert trial reused')
    for mode in ('physics','control'):
        result=data[mode]['result']
        if result.get('kind')!='NATIVE_PHYSX_TESTS' or result.get('mode')!=mode or result.get('commit')!=commit:
            raise ValueError('Native prerequisite provenance mismatch')
        if result.get('failed')!=0 or result.get('passed',0)<2:raise ValueError('Native prerequisites did not pass')
        cases=json.loads((HERE/'native-cases.json').read_text())[mode]
        expected={(case['name'],repeat) for case in cases for repeat in (0,1)}
        actual={(case['name'],case['repeat']) for case in result['cases'] if case['status']=='PASS'}
        if actual!=expected or len(result['cases'])!=len(expected) or result.get('reset_count')!=len(expected):
            raise ValueError('Native prerequisites have incomplete case/repeat coverage')


def command(mode,output,commit,seed=0):
    spec=json.loads((HERE/'scene.json').read_text())
    return ['run','--embodiment','yam_arena','-E',f'task={HERE/"task.py"}',
            '-E','object_jitter=0','-E','control_hz=20','-E','cam_width=320','-E','cam_height=176',
            '--instruction',spec['instruction'],'--scorer','task_score','--max-steps',str(spec['run_limit']),
            '--seed',str(seed),'--store-frames','--log-dir',str(output),'--environment-revision',commit,
            '--policy','rc_expert' if mode=='expert' else 'dream']+([] if mode=='expert' else ['-P','model=dreamlabs/dream-1-beta'])


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--mode',choices=['expert','dream'],required=True)
    parser.add_argument('--output',type=Path,required=True);parser.add_argument('--commit')
    parser.add_argument('--seed',type=int,default=0);parser.add_argument('--execute',action='store_true')
    parser.add_argument('--evidence',type=Path)
    args=parser.parse_args()
    revision=subprocess.run(['git','rev-parse','HEAD'],cwd=HERE,text=True,capture_output=True,check=True).stdout.strip()
    if args.commit and args.commit!=revision:raise SystemExit('Commit does not match checkout HEAD')
    commit=args.commit or revision
    cmd=command(args.mode,args.output.resolve(),commit,args.seed)
    print(shlex.join(['inspect-robots']+cmd))
    if not args.execute:
        print('DRY RUN: no simulator or model request launched.');return 0
    if sys.platform!='linux':raise SystemExit('Native execution requires Linux with the official Arena stack')
    if subprocess.run(['git','status','--porcelain'],cwd=HERE,text=True,capture_output=True,check=True).stdout.strip():
        raise SystemExit('Task checkout must be clean before execution')
    if args.mode=='dream':
        if args.evidence is None:raise SystemExit('Dream requires --evidence <verified feasibility.json>')
        feasible(args.evidence.resolve(),commit)
    gpu=subprocess.run(['nvidia-smi','--query-gpu=name,uuid,memory.free','--format=csv,noheader'],
                       capture_output=True,text=True,check=True)
    if not any(name in gpu.stdout for name in ('L40S','RTX 4090','RTX 5090')):
        raise SystemExit('No supported ray-tracing GPU profile detected')
    args.output.mkdir(parents=True,exist_ok=False)
    os.environ['ROBOCURVE_TRACE']=str(args.output.resolve()/'native_frames.jsonl')
    os.environ['ROBOCURVE_EXPERT_EVENTS']=str(args.output.resolve()/'expert-events.jsonl')
    if args.mode=='expert':
        # Load exactly the task folder's self-contained expert; registered only for this process.
        loader=importlib.util.spec_from_file_location('robocurve_expert_task',HERE/'task.py')
        module=importlib.util.module_from_spec(loader);loader.loader.exec_module(module)
        factory=importlib.import_module(module._name+'.expert').policy
        from inspect_robots.registry import policy
        policy('rc_expert')(factory)
    from inspect_robots.cli import main as official_cli
    return official_cli(cmd)


if __name__=='__main__':raise SystemExit(main())
