"""Guard clearance QA independent of native joint-adjacency collision filtering.

Moving-part pairs are excluded solely in this inspection so every housing/part
pair is checked, even if PhysX would normally filter the parent-child pair.
Includes physical cam observations, nominal controller poses and full rack range.
"""
import copy,itertools,json,hashlib
from pathlib import Path
import numpy as np
from audit_geometry import geometry_module
from kinematics import reconstruct


def audit(folder):
 s=json.loads((folder/'scene.json').read_text());ref=json.loads((folder/'cam-reference.json').read_text())
 if ref['scene_sha256']!=hashlib.sha256((folder/'scene.json').read_bytes()).hexdigest():raise ValueError('Housing audit needs a current physical cam reference')
 defs={b['name']:b for a in s['assemblies'] for b in a['bodies']};outer=defs['outer_tube']
 housing=[shape for shape in outer['shapes'] if shape.get('role')=='protective_housing']
 assert housing
 moving=['inner_tube','gear_set','handle','release_trigger','holding_pawl','driving_pawl']
 guard=dict(name='housing',anchor=True,shapes=housing)
 probe=dict(assemblies=[dict(bodies=[guard]+[defs[n] for n in moving],joints=[])],
            collision_exclusions=[list(pair) for pair in itertools.combinations(moving,2)])
 g=geometry_module(folder);samples=[]
 for i,row in enumerate(ref['checks']):samples.append(('CPU cam reference '+str(i),row['bodies']))
 for i,p in enumerate(json.loads((folder/'controller.json').read_text())['phases']):samples.append(('Controller endpoint '+str(i),p['nominal_bodies']))
 for q in np.linspace(0,.05,11):
  js=ref['checks'][-1]['joints'].copy();js['telescope']=float(q);js['pinion_rotation']=-float(q)/s['parameters']['authored_pinion_pitch_radius']
  samples.append(('Full rack travel '+str(float(q)),reconstruct(s,outer,js)))
 rows=[]
 for label,states in samples:
  states=dict(states,housing=states['outer_tube'])
  depth=float(g.maximum_penetration(probe,states));rows.append(dict(label=label,housing_overlap_m=depth,passed=depth<=.00005))
 result=dict(kind='OFFLINE_HOUSING_MOVING_PART_CLEARANCE',physics_executed=False,joint_adjacency_filter_used=False,
             inspected_housing_shapes=len(housing),checks=rows,passed=all(r['passed'] for r in rows))
 print(json.dumps(result,indent=2));return 0 if result['passed'] else 1
if __name__=='__main__':raise SystemExit(audit(Path(__file__).resolve().parent))
