"""Publish validated tasks through the registered submitting account. Preview by default.

Authenticate gh as the team's registered submitting account. Closed prior PRs
require inspection of official review comments before further action.
"""
import argparse
import json
import math
from pathlib import Path
import subprocess
import tempfile
from engine import Incomplete, atomic, read, verified_receipt, within
from evidence import require
from environment import capture

OFFICIAL='robocurve/benchmark-tasks'
FORK='aryansennthilkumarGT/benchmark-tasks'


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('handoff',type=Path)
    p.add_argument('--execute',action='store_true',help='Publish fully verified tasks as official pull requests')
    p.add_argument('--registered-account',help='Required exact registered GitHub login when executing')
    args=p.parse_args(argv);handoff=read(args.handoff)
    tasks=handoff['tasks'];require(tasks,'No submission-ready tasks; nothing to submit')
    require(len(tasks)<=8 and len({t['slug'] for t in tasks})==len(tasks),'Duplicate/invalid handoff')
    require(len({t['branch'] for t in tasks})==len(tasks),'Duplicate task branch')
    for task in tasks:
        require(task.get('ready') is True and task.get('status')=='READY_FOR_PR','Unfinished task in handoff')
        require(task.get('media_id') and task.get('expert_scores')==[1.0,1.0] and task.get('dream_score') is not None,
                'Mandatory evidence missing')
        require(isinstance(task['dream_score'],(int,float)) and not isinstance(task['dream_score'],bool)
                and math.isfinite(task['dream_score']) and 0<=task['dream_score']<=1,'Invalid model score')
        required={'MECHANICS_COMPLETE','STATIC_TESTS_PASSED','NATIVE_PHYSICS_PASSED','ROBOT_CONTROL_PASSED',
                  'EXPERT_DEMO_1_PASSED','EXPERT_DEMO_2_PASSED','MODEL_EVALUATED','MEDIA_RENDERED','MEDIA_VERIFIED','MEDIA_UPLOADED','EXACT_COMMIT_VERIFIED'}
        require(set(task.get('evidence',{}))==required,'Required validation receipts missing')
        for record in task['evidence'].values():
            receipt=within(args.handoff.resolve().parent,args.handoff.resolve().parent/record['receipt'])
            require(verified_receipt(receipt,record['key']),'Changed or missing validation evidence')
    if args.execute:
        require(args.registered_account,'--registered-account is required for execution')
        actual=capture(['gh','api','user','--jq','.login'])
        require(actual==args.registered_account,'Authenticated GitHub account differs from registered submitting account')
    result=[]
    for task in tasks:
        head=f'aryansennthilkumarGT:{task["branch"]}'
        title=task.get('suggested_pr_title') or task['title']
        body=task.get('suggested_pr_body') or (f'{task["title"]}. Reproducible task package in `tasks/{task["slug"]}`.\n\n'
            f'Validation: two expert demonstrations scored 1.0; Dream-1 scored {task["dream_score"]}. '
            f'Media: {task["media_id"]}. Exact verified commit: `{task["commit"]}`. '
            'See the task README for setup, fidelity limitations, numeric scoring, and reproduction commands.\n')
        if not args.execute:
            result.append({'slug':task['slug'],'title':title,'body':body,'head':head,'action':'PREVIEW_ONLY'})
            continue
        branch_sha=capture(['gh','api',f'repos/{FORK}/git/ref/heads/{task["branch"]}','--jq','.object.sha'])
        require(branch_sha==task['commit'],'Remote branch changed since validation')
        existing=json.loads(capture(['gh','pr','list','--repo',OFFICIAL,'--head',head,'--state','all',
                                    '--json','number,url,state']))
        if existing:
            require(len(existing)==1,'Multiple prior PRs require review')
            require(existing[0]['state'] in ('OPEN','MERGED'),'Prior closed PR: inspect review before any resubmission')
            result.append({'slug':task['slug'],'action':'ALREADY_EXISTS',**existing[0]});continue
        with tempfile.TemporaryDirectory(prefix='robocurve-pr-') as temporary:
            body_file=Path(temporary)/'body.txt';body_file.write_text(body,encoding='utf-8')
            url=capture(['gh','pr','create','--repo',OFFICIAL,'--base','main','--head',head,'--title',title,
                         '--body-file',str(body_file)])
        result.append({'slug':task['slug'],'action':'CREATED','url':url})
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
