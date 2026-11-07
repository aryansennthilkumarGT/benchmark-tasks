"""Bind an actual visual review to the exact rendered media. Never simulates review."""
import argparse
from pathlib import Path
from engine import Incomplete,atomic,digest,read,utc,verified_receipt,within

FILES=('setup.png','model.mp4','demo.mp4','demo-repeat.mp4')
CHECKS=('correct_initial_configuration','mechanisms_and_robot_visible','videos_show_real_actions','no_identifying_text_or_overlays','claimed_outcomes_match_views')

def verify_review(path,commit,media):
    if not path.is_file():raise Incomplete('Rendered media awaits visual review. Inspect setup, three videos and contact sheets; record review with coordination/review_media.py, then --resume.')
    review=read(path)
    if review.get('commit')!=commit or review.get('files')!={n:digest(media/n) for n in FILES}:
        raise Incomplete('Visual review refers to different media or source')
    if review.get('checks')!={name:True for name in CHECKS}:raise Incomplete('Visual review is incomplete')
    return review

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('run_root',type=Path);p.add_argument('--task',required=True)
    p.add_argument('--confirm-reviewed',action='store_true',help='Assert you have actually inspected all listed media and checks')
    args=p.parse_args(argv);root=args.run_root.resolve();ledger=read(root/'ledger.json')
    rows=ledger['tasks'][args.task]['MEDIA_RENDERED'];row=next((r for r in reversed(rows) if r['status']=='PASS'),None)
    if not row:raise Incomplete('No successfully rendered media')
    receipt=within(root,root/row['receipt'])
    if not verified_receipt(receipt,row['key']):raise Incomplete('Rendered evidence changed')
    data=read(receipt);media=Path(data['result']['path']);commit=data['inputs']['commit']
    print('Inspect: '+str(media));print('Checks: '+', '.join(CHECKS))
    if not args.confirm_reviewed:return 0
    atomic(root/'reviews'/(args.task+'.json'),{'commit':commit,'files':{n:digest(media/n) for n in FILES},
                                           'checks':{n:True for n in CHECKS},'reviewed_at':utc()})
    return 0
if __name__=='__main__':raise SystemExit(main())
