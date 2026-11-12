"""Offline grasp-clearance checks against every official convex robot piece.

The jaw width is a nominal value inside the specified contact interval. Actual
closure, force and object retention are separate native robot-control tests.
"""
import json
from pathlib import Path
import numpy as np
from yam_arena import ik,station
from yam_arena.constants import READY
from audit_geometry import frames,geometry_module
from robot_geometry import arm_hulls,task_collisions,table_intersections
from feedback import rotate,multiply


def audit(folder):
    spec=json.loads((folder/'scene.json').read_text());plan=json.loads((folder/'controller.json').read_text())
    geometry=geometry_module(folder);seeds={side:np.array(READY) for side in ('left','right')};solutions={}
    for item in plan['audit_tcp_targets']:
        side=item['side'];q,pe,re=ik.solve(item['pos'],item['quat'],q_init=seeds[side],base_pos=station.BASES[side],iters=500,damping=.015,tol=1e-5)
        if pe>.0015 or re>.035:raise ValueError('Critical pose failed before grasp clearance: '+item['label'])
        seeds[side]=q;solutions.setdefault(item['label'],[]).append(q)
    checks=[]
    for label,states in frames(spec,plan,linear_step=.02,include_phase_starts=True):
        if not label.startswith('PHASE '):continue
        index=int(label.split(':',1)[0].split()[1]);phase=plan['phases'][index]
        if phase['kind']!='grasp':continue
        q=solutions[phase['label']].pop(0);opening=sum(phase['width'])/2/.0939
        hulls=arm_hulls(phase['side'],np.r_[q,opening])
        # Bendable cable paths during motion cannot be inferred without PhysX.
        inspect_spec=spec
        if spec.get('offline_deformable_bodies') and index>0:
            import copy
            inspect_spec=copy.deepcopy(spec);excluded=set(spec['offline_deformable_bodies'])
            for assembly in inspect_spec['assemblies']:assembly['bodies']=[b for b in assembly['bodies'] if b['name'] not in excluded]
        contacts=task_collisions(geometry,hulls,inspect_spec,states)
        forbidden=[c for c in contacts if c['body']!=phase['body'] or c['link'] not in ('tip_left','tip_right')]
        # Even intended fingertip contacts must not require deep geometric overlap.
        forbidden += [c for c in contacts if c['body']==phase['body'] and c['link'] in ('tip_left','tip_right') and c['penetration_m']>.004]
        table=table_intersections(hulls,spec['table_top'])
        checks.append(dict(phase=index,label=phase['label'],nominal_jaw_width_m=opening*.0939,
                           forbidden_intersections=forbidden,table_intersections=table,passed=not forbidden and not table))
    result=dict(kind='OFFLINE_URDF_GRASP_GEOMETRY',physics_executed=False,actual_grasp_verified=False,
                flexible_cable_path_excluded=bool(spec.get('offline_deformable_bodies')),checks=checks,
                passed=bool(checks) and all(row['passed'] for row in checks))
    print(json.dumps(result,indent=2));return 0 if result['passed'] else 1


if __name__=='__main__':raise SystemExit(audit(Path(__file__).resolve().parent))
