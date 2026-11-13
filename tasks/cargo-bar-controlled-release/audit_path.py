"""Sample the executed controller's pinned-URDF FK hulls, not nominal waypoints.

Task-body observations use the explicitly synthetic IdealFixture. No native
contact, grasp or swept-volume guarantee is implied. Test every fifth action
(4 Hz), all phase transitions and the final action; report all unexpected hits.
"""
import json,hashlib
from pathlib import Path
from feedback import Controller,ControlFailure
from ideal_fixture import IdealFixture
from robot_geometry import arm_hulls,task_collisions,table_intersections,inter_arm_intersections


def audit(folder):
 files=list(folder.glob('*.py'))+list(folder.glob('*.json'))+list((folder/'assets').glob('*.usda'))+list((folder/'test_fixtures').glob('*.json'))
 identity=lambda:{p.relative_to(folder).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files) if p.name!='source_manifest.json'}
 source=identity()
 f=IdealFixture(folder);c=Controller(f.plan,f.spec);rows=[];previous=-1;error=None
 for step in range(f.spec['run_limit']):
  frame=f.frame(geometric_metrics=False);index=c.index
  if step%5==0 or index!=previous or c.done:
   hulls={s:arm_hulls(s,f.q[(0 if s=='left' else 7):(7 if s=='left' else 14)]) for s in ('left','right')}
   collisions=[];table=[]
   for side in hulls:
    allowed=c.targets.get(side,{}).get('contact_bodies',[])
    for hit in task_collisions(f.g,hulls[side],f.spec,frame['bodies'],threshold=.00005):
     if hit['body'] in allowed and hit['link'] in ('tip_left','tip_right') and hit['penetration_m']<=.0008:continue
     collisions.append(dict(side=side,**hit))
    table.extend(dict(side=side,**hit) for hit in table_intersections(hulls[side],f.spec['table_top'],threshold=.00005))
   crossing=inter_arm_intersections(f.g,hulls['left'],hulls['right'],threshold=.00005)
   rows.append(dict(step=step,time=f.time,phase=index,label=c.phases[min(index,len(c.phases)-1)]['label'],contacts=collisions,
                    table=table,inter_arm=crossing,passed=not collisions and not table and not crossing))
  if c.done:break
  try:action=c.step(f.q,frame)
  except (ControlFailure,ValueError,KeyError) as exc:error=str(exc);break
  previous=index;f.advance(c,action,index)
 result=dict(kind='OFFLINE_ACTUAL_CONTROLLER_FK_PATH',physics_executed=False,synthetic_task_feedback=True,grasps_validated=False,
             swept_volume_validated=False,unintentional_contact_bound_m=.00005,intended_finger_contact_bound_m=.0008,runtime_inputs_sha256=source,source_bound=identity()==source,sample_stride_actions=5,samples=len(rows),actions=step,checks=rows,error=error,
             passed=bool(identity()==source and c.done and error is None and all(r['passed'] for r in rows)))
 print(json.dumps(result,indent=2));return 0 if result['passed'] else 1
if __name__=='__main__':raise SystemExit(audit(Path(__file__).resolve().parent))
