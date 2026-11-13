"""Every-control cam geometry using actual FK and explicitly ideal rigid grasps.

Shares the audited synthetic fixture with the full FK replay. No missing native
pose feedback is replaced by nominal phase poses. No native grasp is implied.
"""
import json
from pathlib import Path
from audit_full_fk_path import audit as simulate
from audit_geometry import geometry_module


def audit(folder):
 spec=json.loads((folder/'scene.json').read_text());plan=json.loads((folder/'controller.json').read_text());g=geometry_module(folder);checks=[]
 def sample(step,index,states):
  if plan['phases'][index]['label'].startswith(('Lower tilted','Engage groove','Rock groove')):
   depth=float(g.maximum_penetration(spec,states))
   checks.append(dict(step=step,phase=index,max_penetration_m=depth,passed=depth<=spec['penetration_limit']))
 trace=simulate(folder,collision_checks=False,on_step=sample,emit=False)
 result=dict(kind='OFFLINE_ACTUAL_FK_CAM_PATH_SYNTHETIC_CONTACT',physics_executed=False,grasps_validated=False,
  source_bound=trace['source_bound'],runtime_inputs_sha256=trace['runtime_inputs_sha256'],checks=checks,error=trace['error'],
  passed=bool(checks) and trace['passed'] and all(row['passed'] for row in checks))
 print(json.dumps(result,indent=2));return 0 if result['passed'] else 1
if __name__=='__main__':raise SystemExit(audit(Path(__file__).resolve().parent))
