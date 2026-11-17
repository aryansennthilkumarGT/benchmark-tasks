"""Stage-specific necessary conditions after the bounded support screen.
No grasp joint, carried-object pose assignment, tool purchase claim or insertion
physics is created. A colliding required configuration suffices to reject a plan.
"""
from pathlib import Path
import sys,json
sys.path.insert(0,'/workspace/robocurve-cpu-deps')
D=Path(__file__).resolve().parent
from support_gate import A,RT,scene,evaluate,robot,ob,hit,tool_parts
import numpy as np,fcl
if __name__=='__main__':
 prior=json.loads((D/'results/SUPPORT_GATE.json').read_text());rows=[]
 for c in prior['cases']:
  if c['first_blocking_stage'] is not None:continue
  origin=np.array(c['origin_m']);qr=np.array(c['support_q']);obstacles=scene(origin)
  # Reposition the ordinary unheld tool cradle to the working arm's side. Two
  # end supports leave its original5mm handle exposed; no object is attached.
  obstacles=[x for x in obstacles if not x[0].startswith(('unheld-tweezer','tool-cradle'))]
  center=np.array([.24,.25,.87])
  for label,g,local in tool_parts():obstacles.append(('unheld-'+label,ob(g,RT,center+RT@local)))
  # Two stepped end rests straddle the approximate uniform-metal center of mass;
  # neither clamps the tool. Stability/contact remains unproved.
  for dx,top in [(-.020,center[2]-.0025),(.035,center[2]-.001)]:
   height=top-.7475;obstacles.append(('ordinary-tool-end-support',ob(fcl.Box(.004,.012,height),np.eye(3),[center[0]+dx,center[1],.7475+height/2])))
  down=RT
  acquisition=[];last=A.qready.copy()
  for stage,dz,gap in [('tool_pregrasp',.06,.020),('tool_contact',0,.005),('tool_release',.005,.020),('tool_withdraw',.06,.020)]:
   q,e=A.ik(center-dz*down[:,2],down,seed=last,gap=gap)
   check=evaluate(q,qr,obstacles,origin,True)
   # Contact with the tool is expected only for fingers at the contact stage;
   # record it, do not silently exempt obstacles in a passing certificate.
   acquisition.append(dict(stage=stage,IK=e,geometric_check=check));last=q
  placement=c['simultaneous_counterexample']
  blockers=placement['robot_source_pairs'];arm=placement['arm_arm_pair'];tools=placement['tool_pairs']
  first=next((dict(stage=x['stage'],reason='IK not solved' if not x['IK']['valid'] else 'observed collision',detail=x) for x in acquisition if not x['IK']['valid'] or x['geometric_check']['robot_source_pairs'] or x['geometric_check']['arm_arm_pair'] or x['geometric_check']['self_collision_pairs']),None)
  if first is None and (blockers or arm or tools or placement['self_collision_pairs']):first=dict(stage='annulus-placement_required_pose',reason='support/tool configuration collision',robot_source=blockers,arm_arm=arm,tool_pairs=tools)
  rows.append(dict(origin_m=c['origin_m'],axial_shift_mm=c['axial_shift_mm'],roll_deg=c['roll_deg'],support_sampled_clear=True,acquisition_endpoint_checks=acquisition,
   first_blocking_stage=first,placement_required_configuration=placement,
   physical_tool_purchase='NOT PROVEN',physical_annulus_installation='NOT RUN',release_and_withdrawal_of_installed_annulus='NOT RUN',
   continuous_motion_certificate='NONE: rejection precedes a free-path/grasp certificate',complete_manipulation=False))
  print(c['origin_m'],c['axial_shift_mm'],c['roll_deg'],'first',None if first is None else first['stage'],'arm pair',arm,'tool/support pairs',len(tools),flush=True)
 out=dict(cases=rows,source_scale_complete=False,missing_input='Matched bonded tread/contact profile, exact ordinary tool purchase response and actual source part retention during first bank assembly',decision='PARK ODRI; do not start another contact simulation')
 assert all(x['first_blocking_stage'] is not None for x in rows)
 (D/'results/ONE_ANNULUS_STAGE_GATE.json').write_text(json.dumps(out,indent=2,default=lambda v:v.item() if isinstance(v,np.generic) else str(v))+'\n')
