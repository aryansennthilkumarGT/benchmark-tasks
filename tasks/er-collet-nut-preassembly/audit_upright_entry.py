"""Bound upright entry over the final lateral disk using rigid-geometry SAT.

This is not a physics or elastic-collet proof. At fixed identity orientation,
SAT overlap is 1-Lipschitz under translation: each normalized-axis projection
changes by at most the translation norm, as do min/max across axes and pairs.
A radial/angular covering therefore bounds unsampled translations in the disk.
"""
import copy,hashlib,json,math
from pathlib import Path
from audit_geometry import geometry_module


def audit(folder):
 spec=json.loads((folder/'scene.json').read_text());g=geometry_module(folder)
 states={b['name']:dict(pos=b['pos'].copy(),quat=b['quat'].copy()) for a in spec['assemblies'] for b in a['bodies']}
 target=spec['score_spec']['target'];radius=spec['score_spec']['lateral_tolerance'];rings=2;angles=16
 plane=target[2]+.002
 rows=[]
 for i in range(rings+1):
  for j in range(angles):
   r=radius*i/rings;a=2*math.pi*j/angles
   states['collet'].update(pos=[target[0]+r*math.cos(a),target[1]+r*math.sin(a),plane],quat=[0,0,0,1])
   rows.append(dict(offset=[r*math.cos(a),r*math.sin(a)],overlap_m=float(g.maximum_penetration(spec,states))))
 cover=math.sqrt((radius/(2*rings))**2+4*radius**2*math.sin(math.pi/(2*angles))**2)
 minimum=min(row['overlap_m'] for row in rows);lower=minimum-cover
 # All accepted upright final z values lie below this unavoidable entry plane.
 crossed=plane>target[2]+spec['score_spec']['axial_tolerance']
 result=dict(kind='OFFLINE_UPRIGHT_ENTRY_ENVELOPE_BOUND',physics_executed=False,
   elastic_entry_tested=False,continuous_time_monitoring=False,geometry_scene_sha256=hashlib.sha256((folder/'scene.json').read_bytes()).hexdigest(),
   probe_height_m=plane,lateral_disk_radius_m=radius,samples=rows,minimum_sampled_overlap_m=minimum,
   disk_cover_radius_m=cover,overlap_lower_bound_over_disk_m=lower,integrity_limit_m=spec['penetration_limit'],
   accepted_final_poses_below_probe=crossed,passed=bool(crossed and lower>spec['penetration_limit']))
 return result

if __name__=='__main__':
 report=audit(Path(__file__).resolve().parent);print(json.dumps(report,indent=2));raise SystemExit(0 if report['passed'] else 1)
