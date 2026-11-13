"""Audit every normally filtered task-joint pair as real independent solids.

Joint adjacency is a native solver convention, never evidence that geometry
could actually be manufactured. Intended guide/bearing clearance must survive
unfiltered checks. No moving-part pair in this inspection is silently ignored.
"""
import json,hashlib
from pathlib import Path
from audit_geometry import geometry_module


def audit(folder):
 s=json.loads((folder/'scene.json').read_text());ref=json.loads((folder/'cam-reference.json').read_text())
 if ref['scene_sha256']!=hashlib.sha256((folder/'scene.json').read_bytes()).hexdigest():raise ValueError('Interface audit needs current scene reference')
 defs={b['name']:b for a in s['assemblies'] for b in a['bodies']};g=geometry_module(folder)
 pairs={j['name']:(j['parent'],j['child']) for a in s['assemblies'] for j in a['joints']}
 probes={n:dict(assemblies=[dict(bodies=[defs[a],defs[b]],joints=[])],collision_exclusions=[]) for n,(a,b) in pairs.items()}
 samples=[('CPU reference '+str(i),r['bodies']) for i,r in enumerate(ref['checks'])]
 samples += [('Controller '+str(i),p['nominal_bodies']) for i,p in enumerate(json.loads((folder/'controller.json').read_text())['phases'])]
 checks=[]
 for label,states in samples:
  for name,probe in probes.items():
   depth=float(g.maximum_penetration(probe,states));checks.append(dict(sample=label,joint=name,overlap_m=depth,passed=depth<=.00005))
 result=dict(kind='OFFLINE_UNFILTERED_ADJACENT_INTERFACE_CLEARANCE',physics_executed=False,joint_collision_filter_used=False,
             max_allowed_numerical_overlap_m=.00005,checks=checks,passed=all(r['passed'] for r in checks))
 print(json.dumps(result,indent=2));return 0 if result['passed'] else 1
if __name__=='__main__':raise SystemExit(audit(Path(__file__).resolve().parent))
