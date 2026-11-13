"""Sample every original latch/handle arc, then the full-size ring insertion path."""
import copy,json,math
from pathlib import Path
import numpy as np
from audit_geometry import geometry_module
from kinematics import reconstruct
HERE=Path(__file__).resolve().parent

def audit(spec):
 g=geometry_module(HERE);root=spec['assemblies'][0]['bodies'][0];base={b['name']:dict(pos=b['pos'],quat=b['quat']) for a in spec['assemblies'] for b in a['bodies']};rows=[]
 def check(label,joints,eye=None):
  states=copy.deepcopy(base);states.update(reconstruct(spec,root,joints))
  if eye is not None:states['drawbar_eye']['pos']=eye
  d=float(g.maximum_penetration(spec,states));rows.append(dict(label=label,joints=joints.copy(),eye=eye,depth_m=d,passed=d<=.00005))
  if d>.00005:rows[-1]['contacts']=g.intersection_details(spec,states,.00005)
 for v in np.linspace(0.,-.65,31):check('unlock',dict(latch_rotation=0.,lock_rotation=float(v)))
 for v in np.linspace(0.,-1.5,81):check('open',dict(latch_rotation=float(v),lock_rotation=-.65))
 goal=np.asarray(spec['assemblies'][0]['origin'])+spec['parameters']['eye_goal_local']
 for dz in np.linspace(.11,0,41):check('insert_eye',dict(latch_rotation=-1.5,lock_rotation=-.65),(goal+[0.,0.,dz]).tolist())
 for v in np.linspace(-1.5,0.,81):check('close_over_eye',dict(latch_rotation=float(v),lock_rotation=-.65),goal.tolist())
 for v in np.linspace(-.65,0.,31):check('lock_over_eye',dict(latch_rotation=0.,lock_rotation=float(v)),goal.tolist())
 return dict(kind='OFFLINE_ORIGINAL_INTERFACE_PATH',native_physics=False,swept_volume_guarantee=False,samples=len(rows),checks=rows,passed=all(r['passed'] for r in rows))
if __name__=='__main__':
 r=audit(json.loads((HERE/'scene.json').read_text()));print(json.dumps(r,indent=2));raise SystemExit(0 if r['passed'] else 1)
