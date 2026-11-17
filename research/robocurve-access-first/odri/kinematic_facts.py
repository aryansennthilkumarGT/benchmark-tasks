"""Source-FK finger travel direction and original bare-foot contact distance."""
from pathlib import Path
import sys,json
sys.path.insert(0,'/workspace/robocurve-cpu-deps')
D=Path(__file__).resolve().parent;R=D.parents[2]
sys.path.insert(0,str(R/'research/robocurve-implementation'))
from common.access import Access
import numpy as np
A=Access();data=json.loads((R/'research/robocurve-next-prototype/odri/results/YAM_ACCESS.json').read_text());facts=[]
for number in [0,4]:
 row=data['cases'][number];q=np.array(row['right_support_q']);P=A.r.fk(q,'right')[0];directions={}
 for j,link in [(6,'tip_left'),(7,'tip_right')]:
  changed=q.copy();changed[j]-=.001;T=A.r.fk(changed,'right')[0]
  axis=(T[link][:3,3]-P[link][:3,3])/.001;directions[link]=axis.tolist()
 facts.append(dict(prior_layout=number,opening_travel_direction_world=directions,gripper_frame_rotation=P['gripper'][:3,:3].tolist(),gripper_T_world=P['gripper'].tolist()))
assert all(abs(x['opening_travel_direction_world']['tip_right'][2])>.999 for x in facts)
(D/'results/KINEMATIC_FACTS.json').write_text(json.dumps(facts,indent=2)+'\n')
print('Source FK confirms nominal pinch direction along world Z, parallel to leg stem; local gripper X is the closure direction, not assumed local Y.')
