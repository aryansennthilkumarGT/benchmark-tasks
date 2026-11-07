"""Read-only handoff gate. Never creates PRs or uploads media."""
import argparse
import json
from pathlib import Path


def problems(manifest):
    errors=[]
    tasks=manifest.get('tasks',[])
    if len(tasks)!=8:errors.append('Exactly eight task records are required.')
    if len({t.get('branch') for t in tasks})!=len(tasks):errors.append('Branches must be unique.')
    for task in tasks:
        slug=task.get('slug','<missing>')
        if task.get('status')!='READY' or task.get('ready') is not True:
            errors.append(slug+': not READY')
        if task.get('novelty')!='CLEARED':errors.append(slug+': novelty review unresolved')
        if task.get('physics')!='PASS':errors.append(slug+': native physics unverified')
        demos=task.get('expert_trials',[])
        if len(demos)<2 or any(d.get('score')!=1.0 or not d.get('verified') for d in demos[:2]):
            errors.append(slug+': two verified full-score expert trials required')
        dream=task.get('dream')
        if not isinstance(dream,dict) or not dream.get('completed') or dream.get('score') is None:
            errors.append(slug+': actual completed Dream evaluation required')
        if not task.get('media_id') or not task.get('media_verified'):
            errors.append(slug+': verified media upload required')
        if not task.get('remote_verified'):errors.append(slug+': exact remote branch not verified')
    return errors


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('manifest',nargs='?',type=Path,default=Path(__file__).with_name('draft-manifest.json'))
    args=parser.parse_args()
    result=problems(json.loads(args.manifest.read_text(encoding='utf-8')))
    print(json.dumps({'ready':not result,'issues':result,'opens_prs':False},indent=2))
    return 2 if result else 0


if __name__=='__main__':raise SystemExit(main())
