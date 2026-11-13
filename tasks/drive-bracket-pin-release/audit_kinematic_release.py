"""Actual feedback FK path vs retaining geometry, with synthetic jaw contact.

This is a kinematic fixture, not contact simulation or a physical demonstration.
Only the critical tilt/withdraw/lift prefix is geometrically sampled.
"""
import copy,json
from pathlib import Path
import numpy as np
from yam_arena import ik,station
from yam_arena.constants import READY
from feedback import Controller,ControlFailure
from motion import multiply,conjugate,rotate
from yam_arena.demo import DOWN_GRIP
from audit_geometry import geometry_module


def audit(folder):
 spec=json.loads((folder/'scene.json').read_text());plan=json.loads((folder/'controller.json').read_text())
 c=Controller(plan,spec);q=np.tile(np.r_[READY,1.],2);g=geometry_module(folder);rows=[];error=None
 for step in range(spec['run_limit']):
  index=c.index
  try:q=c.step(q,{'time':step/20}).copy()
  except ControlFailure as exc:error=str(exc);break
  for side,p in c.targets.items():
   if p.get('grasp_width',0.):q[(0 if side=='left' else 7)+6]=max(q[(0 if side=='left' else 7)+6],p['grasp_width']/.0939)
  phase=c.phases[index]
  if phase['label'].startswith(('Tilt','Slide away','Lift drive')):
   tcp,r=ik.tcp_pose(q[7:13],station.BASES['right']);tool=ik.matrix_to_quat_xyzw(r)
   bodyq=multiply(tool,conjugate(DOWN_GRIP));bodypos=tcp-rotate(bodyq,[-.047,0,.014])
   states=copy.deepcopy(phase['nominal_bodies']);states['drive']=dict(pos=bodypos.tolist(),quat=bodyq.tolist())
   depth=float(g.maximum_penetration(spec,states))
   rows.append(dict(step=step,phase=index,max_penetration_m=depth,passed=depth<=spec['penetration_limit']))
  if c.done:break
 report=dict(kind='OFFLINE_ACTUAL_FK_RELEASE_PATH_SYNTHETIC_CONTACT',physics_executed=False,grasps_validated=False,
     checks=rows,controller_error=error,passed=bool(rows) and error is None and all(x['passed'] for x in rows))
 print(json.dumps(report,indent=2));return 0 if report['passed'] else 1
if __name__=='__main__':raise SystemExit(audit(Path(__file__).resolve().parent))
