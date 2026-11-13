"""Sample actual controller FK paths with explicitly ideal rigid grasps.

No physics: grasp acquisition/retention and released-part support are assumed.
This verifies sampled robot/fixture/inter-arm geometry between waypoints, not
native contacts, continuous swept volumes or demonstrated physical success.
"""
import copy,json,hashlib
from pathlib import Path
import numpy as np
from yam_arena import ik,station
from yam_arena.constants import READY
from feedback import Controller,ControlFailure
from motion import multiply,conjugate,rotate
from audit_geometry import geometry_module
from robot_geometry import arm_hulls,task_collisions,table_intersections,inter_arm_intersections


def audit(folder,collision_checks=True):
 s=json.loads((folder/'scene.json').read_text());plan=json.loads((folder/'controller.json').read_text())
 runtime_files=list(folder.glob('*.py'))+[folder/n for n in ('scene.json','controller.json','stack-lock.json')]+list((folder/'assets').glob('*.usda'))+list((folder/'test_fixtures').glob('*.json'))
 identity=lambda:{p.relative_to(folder).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(runtime_files)}
 sources=identity()
 c=Controller(plan,s);q=np.tile(np.r_[READY,1.],2);g=geometry_module(folder);held={};rows=[];error=None
 states={b['name']:dict(pos=b['pos'],quat=b['quat']) for a in s['assemblies'] for b in a['bodies']}
 def pose(side,q):
  off=0 if side=='left' else 7;p,r=ik.tcp_pose(q[off:off+6],station.BASES[side]);return p,ik.matrix_to_quat_xyzw(r)
 for step in range(s['run_limit']):
  index=c.index;p=c.phases[index];side=p['side'];name=p.get('contact_body');width=p.get('grasp_width',0.)
  if width and (side not in held or held[side]['body']!=name):
   tcp,tq=pose(side,q);b=states[name]
   held[side]=dict(body=name,offset=rotate(conjugate(tq),np.array(b['pos'])-tcp),quat=multiply(conjugate(tq),b['quat']))
  if not width:held.pop(side,None)
  try:q=c.step(q,{'time':step/20,'bodies':states,'joints':{}}).copy()
  except ControlFailure as exc:error=str(exc);break
  for arm,target in c.targets.items():
   if target.get('grasp_width',0.):q[(0 if arm=='left' else 7)+6]=max(q[(0 if arm=='left' else 7)+6],(target['grasp_width']+.0003)/.0939)
  for arm,h in held.items():
   tcp,tq=pose(arm,q);states[h['body']]=dict(pos=(tcp+rotate(tq,h['offset'])).tolist(),quat=multiply(tq,h['quat']).tolist())
  if collision_checks and (step%5==0 or c.index!=index or c.done):
   hulls={a:arm_hulls(a,q[(0 if a=='left' else 7):(7 if a=='left' else 14)]) for a in ('left','right')};contacts=[];table=[]
   for arm in hulls:
    for hit in task_collisions(g,hulls[arm],s,states,threshold=.00005):
     if held.get(arm,{}).get('body')==hit['body'] and hit['link'] in ('tip_left','tip_right') and hit['penetration_m']<=.0008:continue
     contacts.append(dict(side=arm,**hit))
    table += [dict(side=arm,**x) for x in table_intersections(hulls[arm],s['table_top'],threshold=.00005)]
   cross=inter_arm_intersections(g,hulls['left'],hulls['right'],threshold=.00005)
   rows.append(dict(step=step,phase=index,contacts=contacts,table=table,inter_arm=cross,passed=not contacts and not table and not cross))
  if c.done:break
 result=dict(kind='OFFLINE_ACTUAL_CONTROLLER_FK_PATH_IDEAL_GRASPS' if collision_checks else 'IDEAL_CONTROLLER_SYNTHETIC_PART_GRASPS',collision_checks_executed=collision_checks,physics_executed=False,grasps_validated=False,
   swept_volume_validated=False,sampling='20 Hz control, every fifth action plus every phase boundary',unintentional_contact_bound_m=.00005,intended_finger_contact_bound_m=.0008,runtime_inputs_sha256=sources,source_bound=identity()==sources,checks=rows,error=error,
   actions=step+1,passed=identity()==sources and (bool(rows) or not collision_checks) and error is None and c.done and all(x['passed'] for x in rows))
 print(json.dumps(result,indent=2));return 0 if result['passed'] else 1
if __name__=='__main__':raise SystemExit(audit(Path(__file__).resolve().parent))
