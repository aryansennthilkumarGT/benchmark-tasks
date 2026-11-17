"""Intermediate protocol only; canonical controls are in mechanism_tests.py."""
from pathlib import Path
import sys,json
sys.path.insert(0,'/workspace/robocurve-cpu-deps')
import numpy as np
from elastic_ring import Ring,Field,solve
from shapely.geometry import shape
from contact_coupon import initial
D=Path(__file__).resolve().parent
rows=json.loads((D/'results/SECTIONS.json').read_text());fields=[]
for x in [2.123,-2.123]:
 r=next(r for r in rows if r['x_mm']==x);fields.append((Field(shape(r['foot'])),Field(shape(r['fixed']))))
rings=[Ring() for _ in range(12)];q=np.r_[initial(rings[:6]),initial(rings[:6])];shift=[0,0];out=[]
for force in [(0,0),(0,1),(0,0),(1,0),(0,0),(-1,0),(0,0)]:
 q,o=solve(rings,q,[fields[0][0]]*6+[fields[1][0]]*6,[fields[0][1]]*6+[fields[1][1]]*6,shift=shift,free_foot=True,body_force=np.array(force)+[0,-.009*9.80665],node_force=[0,-.001*9.80665/(12*32)])
 shift=o['foot_shift_mm'];o['probe_force_N']=force;out.append(o);print(o,flush=True)
(D.parent/'debug/FREE_FOOT_TRIAL.json').write_text(json.dumps(out,indent=2)+'\n');np.save(D.parent/'debug/FREE_FOOT_NODES.npy',q)
