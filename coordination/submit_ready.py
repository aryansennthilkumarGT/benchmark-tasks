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
from engine import Incomplete, atomic, read, verified_receipt, within, fingerprint
from evidence import require
from environment import capture

OFFICIAL='robocurve/benchmark-tasks'
FORK='aryansennthilkumarGT/benchmark-tasks'


def validate_metadata(metadata):
    # Limits directly observed in official intake responses on PR1733.
    for field, maximum in (('setup', 4000), ('fidelity', 500)):
        value = metadata.get(field)
        require(isinstance(value, str) and 0 < len(value) <= maximum,
                f'Official {field} metadata must contain 1–{maximum} characters')


def validated_metadata(task, handoff_path):
    """Bind handoff claims to one receipt chain and its publication repository."""
    root = Path(handoff_path).resolve().parent
    stages = ('MECHANICS_COMPLETE','STATIC_TESTS_PASSED','NATIVE_PHYSICS_PASSED','ROBOT_CONTROL_PASSED',
              'EXPERT_DEMO_1_PASSED','EXPERT_DEMO_2_PASSED','CLEAN_CHECKOUT_EXPERT_PASSED',
              'MODEL_EVALUATED','MEDIA_RENDERED','MEDIA_VERIFIED','MEDIA_UPLOADED','EXACT_COMMIT_VERIFIED')
    require(set(task.get('evidence', {})) == set(stages), 'Required validation receipts missing')
    records = {}; keys = {}; evaluated = task.get('evaluated_commit')
    require(isinstance(evaluated, str) and len(evaluated) == 40, 'Exact evaluated source missing')
    for stage in stages:
        ref = task['evidence'][stage]
        receipt = within(root, root / ref['receipt'])
        require(receipt.parent.parent.parent == root / task['slug']
                and receipt.parent.parent.name == stage, 'Receipt belongs to a different task/stage')
        require(verified_receipt(receipt, ref['key']), 'Changed or missing validation evidence')
        data = read(receipt); inputs = data['inputs']
        require(fingerprint(inputs) == ref['key'] and inputs.get('commit') == evaluated,
                'Receipt describes a different evaluated source')
        require(inputs.get('prerequisites') == keys, 'Validation receipt chain mismatch')
        records[stage] = data; keys[stage] = ref['key']
    for stage in ('EXPERT_DEMO_1_PASSED','EXPERT_DEMO_2_PASSED','CLEAN_CHECKOUT_EXPERT_PASSED'):
        result = records[stage]['result']
        require(result.get('commit') == evaluated and result.get('mode') == 'expert'
                and result.get('score') == 1., 'Expert receipt disagrees with handoff')
    require(task['expert_scores'] == [records[s]['result']['score'] for s in
                ('EXPERT_DEMO_1_PASSED','EXPERT_DEMO_2_PASSED')], 'Expert scores disagree with receipts')
    model = records['MODEL_EVALUATED']['result']
    require(model.get('commit') == evaluated and model.get('mode') == 'dream'
            and model.get('score') == task['dream_score'], 'Model receipt disagrees with handoff')
    require(records['MEDIA_UPLOADED']['result'].get('media_id') == task['media_id'],
            'Uploaded media disagrees with handoff')
    publication = records['EXACT_COMMIT_VERIFIED']['result']
    require(publication.get('verified') is True and publication.get('commit') == task.get('commit')
            and publication.get('evaluated_commit') == evaluated and publication.get('branch') == task['branch'],
            'Publication receipt disagrees with handoff')
    # This worktree holds the metadata-only publication commit. It is not in
    # the coordinator caller's object database, and no mutable ref is fetched.
    receipt = root / task['evidence']['EXACT_COMMIT_VERIFIED']['receipt']
    repository = within(root, receipt.parent / 'publication')
    require(repository.is_dir(), 'Verified publication checkout unavailable')
    require(capture(['git', 'rev-parse', 'HEAD'], repository) == task['commit'],
            'Publication checkout changed')
    metadata = json.loads(capture(['git', 'show',
        f'{task["commit"]}:tasks/{task["slug"]}/task.json'], repository))
    require(isinstance(metadata, dict), 'Invalid task metadata')
    model_name = records['MODEL_EVALUATED']['inputs']['stack']['model']
    require(metadata.get('media') == task['media_id'] and metadata.get('scores') ==
            f'Dream-1 ({model_name}): {task["dream_score"]}; expert demos: 1.0, 1.0',
            'Published scores/media disagree with validated evidence')
    validate_metadata(metadata)
    return metadata


def audit_official_pr(task, number):
    """Read back the actual official PR; never edits an existing submission."""
    info = json.loads(capture(['gh','api',f'repos/{OFFICIAL}/pulls/{number}']))
    require(info['head']['sha'] == task['commit'] and info['head']['ref'] == task['branch']
            and info['head']['repo']['full_name'] == FORK and info['base']['ref'] == 'main',
            'Official PR head/base differs from verified publication')
    pages = json.loads(capture(['gh','api','--paginate','--slurp',
                               f'repos/{OFFICIAL}/pulls/{number}/files']))
    files = [row for page in pages for row in page]; prefix = 'tasks/' + task['slug'] + '/'
    require(files and all(row['filename'].startswith(prefix)
            and (not row.get('previous_filename') or row['previous_filename'].startswith(prefix))
            for row in files), 'Official PR changes more than its one task folder')
    names = {row['filename'][len(prefix):] for row in files if row['status'] != 'removed'}
    require({'task.json','task.py','README.md'} <= names and any(n.endswith(('.usd','.usda','.usdc')) for n in names),
            'Official PR is missing metadata, task entry, setup documentation or USD assets')
    return {'status':'PASS','number':info['number'],'url':info['html_url'],
            'head':info['head']['sha'],'state':info['state'],'file_count':len(files),
            'one_task_folder':True,'metadata_receipts_validated':True,
            'visual_anonymity':'BOUND_TO_PREVIOUS_REAL_MEDIA_REVIEW_NOT_REVIEWED_AGAIN'}


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
        validated_metadata(task, args.handoff)
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
            row={'slug':task['slug'],'action':'ALREADY_EXISTS',**existing[0]}
            row['audit']=audit_official_pr(task,existing[0]['number']);result.append(row)
            atomic(args.handoff.resolve().parent/'submission-status.json',{'tasks':result});continue
        with tempfile.TemporaryDirectory(prefix='robocurve-pr-') as temporary:
            body_file=Path(temporary)/'body.txt';body_file.write_text(body,encoding='utf-8')
            url=capture(['gh','pr','create','--repo',OFFICIAL,'--base','main','--head',head,'--title',title,
                         '--body-file',str(body_file)])
        row={'slug':task['slug'],'action':'CREATED','url':url,'audit_status':'PENDING_READ_BACK'}
        result.append(row)
        # Persist creation before read-back: API failure must not hide a real PR.
        status_path=args.handoff.resolve().parent/'submission-status.json'
        atomic(status_path,{'tasks':result})
        try:
            row['audit']=audit_official_pr(task,int(url.rstrip('/').split('/')[-1]));row['audit_status']='PASS'
        except (Incomplete,ValueError,KeyError,OSError,subprocess.CalledProcessError) as exc:
            row['audit_status']='READ_BACK_FAILED';row['audit_error']=str(exc)
            atomic(status_path,{'tasks':result})
            raise Incomplete(f'Official PR was created at {url}; read-back failed: {exc}') from exc
        atomic(status_path,{'tasks':result})
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
