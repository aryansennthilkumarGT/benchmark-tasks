"""Deadline enforcement for explicitly registered producer process trees only.

PID marker files are recovery hints, never proof of ownership or test success.
No cloud/instance power operation is performed.
"""
import datetime,json,os,signal,subprocess,time
from pathlib import Path

ROOT=Path('/data/robocurve-runs/resume-compat')

def process_table():
    raw=subprocess.check_output(['ps','-eo','pid=,ppid=,pgid='],text=True)
    rows=[]
    for line in raw.splitlines():
        pid,parent,group=map(int,line.split())
        try:args=[x.decode(errors='replace') for x in Path(f'/proc/{pid}/cmdline').read_bytes().split(b'\0') if x]
        except (FileNotFoundError,PermissionError,ProcessLookupError):continue
        rows.append((pid,parent,group,args))
    return rows

def owned_groups(root,table,own_group):
    expected=str(Path(root)/'producer.sh')
    producers={pid for pid,_,_,args in table if args and
               (args[0]==expected or (len(args)>1 and Path(args[0]).name in {'bash','sh','dash'}
                                     and args[1]==expected))}
    descendants=set(producers)
    while True:
        expanded=descendants|{pid for pid,parent,_,_ in table if parent in descendants}
        if expanded==descendants:break
        descendants=expanded
    groups={group for pid,_,group,_ in table if pid in descendants}
    if any(group<=1 or group==own_group for group in groups):
        raise RuntimeError('Refusing unowned/agent process group')
    return producers,groups

def main():
    plan_path=ROOT/'budget-workload-deadline.json'
    while True:
        plan=json.loads(plan_path.read_text())
        deadline=datetime.datetime.fromisoformat(plan['deadline'])
        remaining=(deadline-datetime.datetime.now(datetime.timezone.utc)).total_seconds()
        if remaining<=0:break
        time.sleep(min(60,remaining))
    table=process_table();events=[];seen=set()
    for root in plan['producer_roots']:
        producers,groups=owned_groups(root,table,os.getpgrp())
        for group in groups-seen:
            try:os.killpg(group,signal.SIGTERM)
            except ProcessLookupError:continue
            seen.add(group);events.append({'producer':root,'verified_producer_pids':sorted(producers),'process_group':group,'signal':'SIGTERM'})
    receipt={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'kind':'OWNED_WORKLOAD_BUDGET_DEADLINE_REACHED','events':events,'instance_power_operation':False,'warning':'Brev instances continue billing; workload cancellation does not stop instance charges.'}
    (ROOT/'budget-workload-deadline-result.json').write_text(json.dumps(receipt,indent=2)+'\n')

if __name__=='__main__':main()
