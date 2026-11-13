"""Actual controller FK vs nut/cam geometry with synthetic jaw contact only."""
import copy,json
from pathlib import Path
import numpy as np
from yam_arena import ik,station
from yam_arena.constants import READY
from yam_arena.demo import DOWN_GRIP
from motion import multiply,conjugate,rotate
from feedback import Controller,ControlFailure
from audit_geometry import geometry_module


def audit(folder):
 s=json.loads((folder/'scene.json').read_text());plan=json.loads((folder/'controller.json').read_text());c=Controller(plan,s)
 q=np.tile(np.r_[READY,1.],2);g=geometry_module(folder);checks=[];error=None
 for step in range(s['run_limit']):
  index=c.index
  try:q=c.step(q,{'time':step/20}).copy()
  except ControlFailure as exc:error=str(exc);break
  for side,p in c.targets.items():
   if p.get('grasp_width',0.):q[(0 if side=='left' else 7)+6]=max(q[(0 if side=='left' else 7)+6],p['grasp_width']/.0939)
  p=c.phases[index]
  if p['label'].startswith(('Lower tilted','Engage groove','Rock groove')):
   tcp,r=ik.tcp_pose(q[7:13],station.BASES['right']);tool=ik.matrix_to_quat_xyzw(r);bq=multiply(tool,conjugate(DOWN_GRIP))
   pos=tcp-rotate(bq,[0,0,.033]);states=copy.deepcopy(p['nominal_bodies']);states['collet']=dict(pos=pos.tolist(),quat=bq.tolist())
   depth=float(g.maximum_penetration(s,states));checks.append(dict(step=step,phase=index,max_penetration_m=depth,passed=depth<=s['penetration_limit']))
  if c.done:break
 result=dict(kind='OFFLINE_ACTUAL_FK_CAM_PATH_SYNTHETIC_CONTACT',physics_executed=False,grasps_validated=False,checks=checks,error=error,
   passed=bool(checks) and error is None and c.done and all(x['passed'] for x in checks))
 print(json.dumps(result,indent=2));return 0 if result['passed'] else 1
if __name__=='__main__':raise SystemExit(audit(Path(__file__).resolve().parent))
