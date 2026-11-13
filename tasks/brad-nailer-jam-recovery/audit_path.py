"""Actual pinned-URDF FK replay from a source-bound synthetic controller trace.

Every fifth action and every phase transition are checked. No swept-volume,
physical grasp, native physics or actuator tracking guarantee is claimed.
"""
import argparse,hashlib,json,copy
from pathlib import Path
from audit_geometry import geometry_module
from robot_geometry import arm_hulls,task_collisions,inter_arm_intersections,table_intersections
from source_identity import require_same
from scoring import Scorer
from robot_clearance import boxes
HERE=Path(__file__).resolve().parent


def audit(trace,folder=HERE,diagnostic_stale=False):
 data=json.loads(trace.read_text());spec=json.loads((folder/'scene.json').read_text());plan=json.loads((folder/'controller.json').read_text());g=geometry_module(folder)
 hashes={'scene_sha256':'scene.json','controller_sha256':'controller.json'}
 bound=all(data[k]==hashlib.sha256((folder/v).read_bytes()).hexdigest() for k,v in hashes.items())
 try:require_same(folder,data.get('runtime_inputs_sha256'))
 except ValueError:bound=False
 if not bound and not diagnostic_stale:raise ValueError('Trace inputs changed; cannot qualify stale FK samples')
 rows=[];judge=Scorer(spec);scorer_failure=None
 for sample in data['samples']:
  index=sample['index'];targets={}
  for phase in plan['phases'][:index+1]:targets[phase['side']]=phase
  q=sample['q'];states=sample['frame']['bodies'];hulls={s:arm_hulls(s,q[(0 if s=='left' else 7):(7 if s=='left' else 14)]) for s in ('left','right')};bad=[];table=[]
  for side in hulls:
   allowed=targets.get(side,{}).get('contact_body')
   for hit in task_collisions(g,hulls[side],spec,states,threshold=.0005):
    if hit['body']==allowed and hit['link'] in ('tip_left','tip_right') and hit['penetration_m']<=.0008:continue
    bad.append(dict(side=side,**hit))
   table.extend(dict(side=side,**v) for v in table_intersections(hulls[side],spec['table_top'],threshold=.0005))
  crossing=inter_arm_intersections(g,hulls['left'],hulls['right'],threshold=.0005)
  frame=copy.deepcopy(sample['frame']);frame['max_penetration']=float(g.maximum_penetration(spec,states));frame['robot_clearance']=float(g.robot_clearance(boxes(q,g),spec,states));scored=judge.update(frame)
  if scored.failure and scorer_failure is None:scorer_failure=dict(index=index,time=frame['time'],reason=scored.failure)
  rows.append(dict(index=index,time=frame['time'],contacts=bad,table=table,inter_arm=crossing,task_penetration_m=frame['max_penetration'],release_clearance_m=frame['robot_clearance'],synthetic_score=scored.score,passed=not bad and not table and not crossing and not scored.failure))
 try:require_same(folder,data.get('runtime_inputs_sha256'))
 except ValueError:bound=False
 return dict(kind='OFFLINE_ACTUAL_CONTROLLER_FK_PATH',physics_executed=False,synthetic_task_feedback=True,grasps_validated=False,swept_volume_validated=False,
   source_bound=bound,trace_sha256=hashlib.sha256(trace.read_bytes()).hexdigest(),samples=len(rows),checks=rows,synthetic_score=judge.result.score,scorer_failure=scorer_failure,passed=bool(bound and data['passed'] and judge.result.success and all(r['passed'] for r in rows)))

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('trace',type=Path);p.add_argument('--diagnostic-stale',action='store_true');a=p.parse_args();r=audit(a.trace,diagnostic_stale=a.diagnostic_stale);print(json.dumps(r,indent=2));raise SystemExit(0 if r['passed'] else 1)
