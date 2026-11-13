"""Durable continuous-session control. No simulator, provider or PR operations.

An authorization reference records actual user approval; it is not independent
proof of that approval. Provider receipts are factual observations, not tokens.
"""
import argparse,json,math,time,re
from functools import wraps
from pathlib import Path
from engine import Incomplete,atomic,read,exclusive
from session_budget import session


def serialized(function):
    @wraps(function)
    def locked(root,*args,**kwargs):
        with exclusive(Path(root)/'sprint-state.lock'):
            return function(root,*args,**kwargs)
    return locked


def open_sprint(root,budget_file,resume=False,clock=time.time):
    root=Path(root);path=root/'sprint-session.json'
    # Reject missing authorization before filesystem mutation. No execution occurs if funds are invalid.
    receipt=read(budget_file)
    cap=receipt.get('authorized_session_spend_usd')
    if isinstance(cap,bool) or not isinstance(cap,(int,float)) or not math.isfinite(cap) or cap<=0 or not receipt.get('authorization_reference'):
        raise Incomplete('Continuous sprint requires actual start/spend authorization and an explicit cap')
    identity={k:receipt[k] for k in ('instance_id','gpu_uuid','instance_started_unix','hourly_usd','spent_before_start_usd','authorization_reference','authorized_session_spend_usd')}
    with exclusive(root/'sprint-state.lock'):
        if path.exists():
            if not resume:raise Incomplete('Sprint already exists; resume its original deadline and records')
            state=read(path)
            if state['identity']!=identity:raise Incomplete('Sprint identity or authorized cap changed; do not reset spending history')
            deadline=state['deadline_unix']
        else:
            # Six-hour ceiling is anchored to actual instance start, not each retry.
            deadline=receipt['instance_started_unix']+21600
            state={'schema':1,'identity':identity,'deadline_unix':deadline,'target_new_prs':3,
                   'stop_after_target':False,'submissions':{},'repairs':{},'billing_stopped':False}
        budget=session(budget_file,deadline=deadline,clock=clock)
        state['last_cost_check']=budget.check()
        observation={k:receipt[k] for k in ('balance_usd','balance_observed_unix','hourly_usd','provider_evidence')}
        history=state.setdefault('provider_observations',[])
        if observation not in history:history.append(observation)
        atomic(path,state)
        return state


@serialized
def record_repair(root,slug,blocker,old_commit,new_commit,reason,diff_sha256):
    path=Path(root)/'sprint-session.json';state=read(path)
    if (not blocker or not reason or not re.fullmatch('[0-9a-f]{64}',diff_sha256)
            or not all(re.fullmatch('[0-9a-f]{40}',commit) for commit in (old_commit,new_commit))
            or old_commit==new_commit):
        raise Incomplete('A repair requires a precise blocker, changed source, diff hash and substantive reason')
    key=slug+'|'+blocker;rows=state['repairs'].setdefault(key,[])
    if any(r['new_commit']==new_commit for r in rows):raise Incomplete('This repair source is already recorded; reuse its evidence')
    if len(rows)>=2:raise Incomplete('Two repair approaches exhausted at this blocker; switch candidate or preserve a bounded diagnostic')
    rows.append(dict(old_commit=old_commit,new_commit=new_commit,reason=reason,diff_sha256=diff_sha256))
    atomic(path,state)
    return rows[-1]


@serialized
def record_submission(root,row):
    path=Path(root)/'sprint-session.json'
    if not path.exists():return
    state=read(path)
    created=state.setdefault('created_prs',{})
    if row.get('action')=='CREATED' or row.get('url') in created:
        created[row['url']]=row
        if row.get('audit_status')=='PASS' or row.get('audit',{}).get('status')=='PASS':
            state['submissions'][row['url']]=row
    state['new_pr_count']=len(state['submissions'])
    state['target_reached']=state['new_pr_count']>=state['target_new_prs']
    atomic(path,state)


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--run-root',type=Path,required=True)
    p.add_argument('--task',required=True);p.add_argument('--blocker',required=True)
    p.add_argument('--old-commit',required=True);p.add_argument('--new-commit',required=True)
    p.add_argument('--reason',required=True);p.add_argument('--diff-sha256',required=True)
    a=p.parse_args(argv)
    print(json.dumps(record_repair(a.run_root,a.task,a.blocker,a.old_commit,a.new_commit,a.reason,a.diff_sha256),indent=2))
if __name__=='__main__':main()
