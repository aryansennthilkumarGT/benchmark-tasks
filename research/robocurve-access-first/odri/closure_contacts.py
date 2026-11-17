"""Find first geometric contact while closing the real stock fingers.
No penetration is used to claim a loaded grip; contact events are geometry only.
"""
from pathlib import Path
import json,sys
sys.path.insert(0,'/workspace/robocurve-cpu-deps')
from support_gate import A,scene,evaluate
import numpy as np
D=Path(__file__).resolve().parent
rows=[]
for c in json.loads((D/'results/SUPPORT_GATE.json').read_text())['cases']:
 if c['first_blocking_stage'] is not None:continue
 origin=np.array(c['origin_m']);q=np.array(c['support_q']);obstacles=scene(origin);last=.035;event=None
 def check(gap):
  qq=q.copy();qq[6:]=-gap/2
  return evaluate(A.qready,qq,obstacles,origin,False)
 for gap in np.linspace(.035,.025,21):
  e=check(gap)
  if e['robot_source_pairs'] or e['arm_arm_pair'] or e['self_collision_pairs']:
   hi,lo=last,float(gap)
   for _ in range(12):
    mid=(lo+hi)/2;test=check(mid)
    if test['robot_source_pairs'] or test['arm_arm_pair'] or test['self_collision_pairs']:lo=mid;e=test
    else:hi=mid
   event=dict(last_clear_gap_mm=hi*1000,first_collision_gap_mm=lo*1000,contacts=e)
   break
  last=float(gap)
 rows.append(dict(origin_m=c['origin_m'],axial_shift_mm=c['axial_shift_mm'],roll_deg=c['roll_deg'],first_contact=event,
  physical_purchase='NOT PROVEN; actual tire/contact compliance/friction absent',source_scope='Registered bare SLA foot and original base, not complete tire-contact hardware'))
 print(c['origin_m'],c['axial_shift_mm'],event,flush=True)
(D/'results/CLOSURE_CONTACTS.json').write_text(json.dumps(rows,indent=2)+'\n')
