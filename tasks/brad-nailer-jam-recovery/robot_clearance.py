"""Conservative per-link robot boxes matching the native release-clearance rule."""
from functools import lru_cache
import numpy as np
from yam_arena import ik,station,YAM_URDF
from yam_arena.constants import ARM_JOINTS,FINGER_JOINTS,FINGER_OPEN
from yam_arena.urdf import forward_kinematics
from robot_geometry import local_hulls

@lru_cache(maxsize=1)
def bounds():
 groups={}
 for h in local_hulls():groups.setdefault(h['link'],[]).append(h['vertices'])
 result={}
 for name,parts in groups.items():
  v=np.concatenate(parts);result[name]=((v.min(axis=0)+v.max(axis=0))/2,(v.max(axis=0)-v.min(axis=0))/2)
 return result

def boxes(q,geometry):
 rows=[]
 for side in ('left','right'):
  i=0 if side=='left' else 7;conf={n:float(v) for n,v in zip(ARM_JOINTS,q[i:i+6])};conf.update({n:float(q[i+6]*FINGER_OPEN) for n in FINGER_JOINTS});transforms=forward_kinematics(YAM_URDF,conf)
  for name,(center,half) in bounds().items():
   m=transforms[name];body=dict(pos=(m[:3,3]+station.BASES[side]).tolist(),quat=ik.matrix_to_quat_xyzw(m[:3,:3]).tolist());rows.append(geometry.box(body,dict(kind='box',pos=center,size=2*half,quat=[0,0,0,1])))
 return rows
