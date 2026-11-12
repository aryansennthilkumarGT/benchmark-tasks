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
from robot_geometry import arm_hulls,task_collisions,table_intersections,inter_arm_intersections


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
        q0=grasp['quat'];seed=np.array(READY)
        segment_angle = phase.get('segment_angle', math.pi/4)
        count = math.ceil(phase['turns'] * 2 * math.pi / segment_angle)
        for segment in (1,count):
            for fraction in (0.,.5,1.):
                total=segment-1+fraction;body_pos=start-axis*phase['pitch']*total*segment_angle/(2*math.pi)
                body_q=multiply(axis_quat(axis,-total*segment_angle),initial_q)
                pose=copy.deepcopy(states);pose[phase['body']].update(pos=body_pos.tolist(),quat=body_q.tolist())
                for opening, lift in [(sum(grasp['width'])/2, 0.), (phase.get('grasp_width_max',.04)+.012, 0.), (phase.get('grasp_width_max',.04)+.012, .012)]:
                    # Gripper returns to q0 between segments. This samples both
                    # directions of its declared sweep at both depth extremes.
                    tcp=body_pos+rotate(reference['quat'],grasp['offset'])+[0,0,lift]
                    quat=multiply(axis_quat(axis,-fraction*segment_angle),q0)
                    joints,pe,re=ik.solve(tcp,quat,q_init=seed,base_pos=station.BASES[side],iters=500,damping=.015,tol=1e-5);seed=joints
                    row=dict(body=phase['body'],segment=segment,fraction=fraction,jaw_width_m=opening,unwind_lift_m=lift)
                    hulls=arm_hulls(side,np.r_[joints,opening/.0939])
                    contacts=task_collisions(geometry,hulls,spec,pose)
                    forbidden=[c for c in contacts if c['body']!=phase['body'] or c['link'] not in ('tip_left','tip_right') or c['penetration_m']>.004]
                    table=table_intersections(hulls,spec['table_top'])
                    other_side = 'left' if side == 'right' else 'right'
                    crossing = []
                    if other_side in grips:
                        other_grasp = grips[other_side]
                        other_body = pose[other_grasp['body']]
                        other_tcp = np.asarray(other_body['pos']) + rotate(other_body['quat'], other_grasp['offset'])
                        other_q, other_pe, other_re = ik.solve(other_tcp, other_grasp['quat'],
                            base_pos=station.BASES[other_side], iters=500, damping=.015, tol=1e-5)
                        if other_pe>.0015 or other_re>.035:
                            raise ValueError('Supporting arm IK failed in thread audit')
                        other_hulls = arm_hulls(other_side, np.r_[other_q, sum(other_grasp['width'])/2/.0939])
                        left_hulls, right_hulls = (other_hulls, hulls) if side == 'right' else (hulls, other_hulls)
                        crossing = inter_arm_intersections(geometry, left_hulls, right_hulls)
                    row['inter_arm_collisions'] = crossing
                    row.update(position_error_m=float(pe),rotation_error_rad=float(re),collisions=forbidden,table_intersections=table,
                               passed=pe<.0015 and re<.035 and not forbidden and not table and not crossing)
                    checks.append(row)
    report=dict(kind='OFFLINE_THREAD_WRIST_ENVELOPE',physics_executed=False,checks=checks,applicable=bool(checks),
                passed=all(row['passed'] for row in checks))
    print(json.dumps(report,indent=2));return 0 if report['passed'] else 1


if __name__=='__main__':raise SystemExit(audit(Path(__file__).resolve().parent))
