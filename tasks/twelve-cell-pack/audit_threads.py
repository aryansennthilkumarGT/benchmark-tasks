"""Offline thread turning/open-wrist clearance envelope, not contact validation."""
import copy
import json
import math
from pathlib import Path
import numpy as np
from yam_arena import ik,station
from yam_arena.constants import READY
from audit_geometry import frames,geometry_module
from feedback import axis_quat,rotate,multiply,conjugate
from robot_geometry import arm_hulls,task_collisions,table_intersections


def audit(folder):
    spec=json.loads((folder/'scene.json').read_text());plan=json.loads((folder/'controller.json').read_text())
    geometry=geometry_module(folder);checks=[];grips={}
    for label,states in frames(spec,plan,linear_step=.02,include_phase_starts=True):
        if not label.startswith('PHASE '):continue
        index=int(label.split(':',1)[0].split()[1]);phase=plan['phases'][index];side=phase['side']
        if phase['kind']=='grasp':grips[side]=phase
        if phase['kind']!='thread':continue
        grasp=grips[side];body=states[phase['body']];reference=states[phase['reference']]
        axis=rotate(reference['quat'],[0,0,1]);start=np.array(body['pos']);initial_q=body['quat']
        q0=grasp['quat'];seed=np.array(READY);count=math.ceil(phase['turns']*8)
        for segment in (1,count):
            for fraction in (0.,.5,1.):
                total=segment-1+fraction;body_pos=start-axis*phase['pitch']*total/8
                body_q=multiply(axis_quat(axis,-total*math.pi/4),initial_q)
                pose=copy.deepcopy(states);pose[phase['body']].update(pos=body_pos.tolist(),quat=body_q.tolist())
                for opening in (sum(grasp['width'])/2,(phase.get('grasp_width_max',.04)+.012)):
                    # Gripper returns to q0 between segments. This samples both
                    # directions of its 45-degree sweep at both depth extremes.
                    tcp=body_pos+rotate(reference['quat'],grasp['offset'])
                    quat=multiply(axis_quat(axis,-fraction*math.pi/4),q0)
                    joints,pe,re=ik.solve(tcp,quat,q_init=seed,base_pos=station.BASES[side],iters=500,damping=.015,tol=1e-5);seed=joints
                    row=dict(body=phase['body'],segment=segment,fraction=fraction,jaw_width_m=opening)
                    hulls=arm_hulls(side,np.r_[joints,opening/.0939])
                    contacts=task_collisions(geometry,hulls,spec,pose)
                    forbidden=[c for c in contacts if c['body']!=phase['body'] or c['link'] not in ('tip_left','tip_right') or c['penetration_m']>.004]
                    table=table_intersections(hulls,spec['table_top'])
                    row.update(position_error_m=float(pe),rotation_error_rad=float(re),collisions=forbidden,table_intersections=table,
                               passed=pe<.0015 and re<.035 and not forbidden and not table)
                    checks.append(row)
    report=dict(kind='OFFLINE_THREAD_WRIST_ENVELOPE',physics_executed=False,checks=checks,applicable=bool(checks),
                passed=all(row['passed'] for row in checks))
    print(json.dumps(report,indent=2));return 0 if report['passed'] else 1


if __name__=='__main__':raise SystemExit(audit(Path(__file__).resolve().parent))
