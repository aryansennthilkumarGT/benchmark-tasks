"""Replay the exact IK step limiter with ideal joint tracking, without physics.

This proves continuity/rate/limit checks for the prescribed Cartesian targets.
It does not establish actuator tracking, object manipulation, or physical success.
"""
import json
import copy
import re
from pathlib import Path
import numpy as np
from yam_arena import ik,station
from yam_arena.constants import READY
from feedback import Motion,ControlFailure,qangle
from audit_geometry import geometry_module
from robot_geometry import arm_hulls,table_intersections,inter_arm_intersections,task_collisions


def audit(folder):
    plan=json.loads((folder/'controller.json').read_text());spec=json.loads((folder/'scene.json').read_text())
    joints={side:np.r_[READY,1.] for side in ('left','right')};motions={side:Motion(side) for side in joints}
    groups=[]
    for target in plan['audit_tcp_targets']:
        if target['label'].endswith(' concurrent support') and groups:groups[-1].append(target)
        else:groups.append([target])
    checks=[];total=0;mesh_samples=0;geometry=geometry_module(folder)
    fixed=copy.deepcopy(spec)
    for assembly in fixed['assemblies']:
        assembly['bodies']=[b for b in assembly['bodies'] if b.get('anchor')]
    initial={b['name']:b for a in fixed['assemblies'] for b in a['bodies']}
    for group in groups:
        label=group[0]['label'];row=dict(label=label,passed=False,steps=0)
        try:
            for step in range(1000):
                completed=True
                for target in group:
                    side=target['side'];p,r=ik.tcp_pose(joints[side][:6],station.BASES[side]);q=ik.matrix_to_quat_xyzw(r)
                    pe=float(np.linalg.norm(p-target['pos']));re=qangle(q,target['quat'])
                    if pe>.0015 or re>.035 or abs(joints[side][6]-target.get('opening',joints[side][6]))>.001:
                        completed=False
                        action,_,_=motions[side].target(joints[side],target['pos'],target['quat'],target.get('opening',joints[side][6]))
                        if np.max(np.abs(action[:6]-joints[side][:6]))>.04500001:raise ControlFailure('Joint-rate violation')
                        joints[side]=action
                row['steps']=step;total+=1
                positions=[ik.tcp_pose(joints[side][:6],station.BASES[side])[0] for side in ('left','right')]
                if np.linalg.norm(positions[0]-positions[1])<.055:raise ControlFailure('TCP separation below 55 mm')
                if min(p[2] for p in positions)<spec['table_top']+.004:raise ControlFailure('TCP entered table guard')
                if step%10==0 or completed:
                    hulls={side:arm_hulls(side,joints[side]) for side in ('left','right')};mesh_samples+=1
                    table=[dict(side=side,**v) for side in hulls for v in table_intersections(hulls[side],spec['table_top'])]
                    if table:raise ControlFailure('Robot mesh/table intersection: '+str(table[:3]))
                    crossing=inter_arm_intersections(geometry,hulls['left'],hulls['right'])
                    if crossing:raise ControlFailure('Inter-arm mesh intersection: '+str(crossing[:3]))
                    contacts=[dict(side=side,**v) for side in hulls for v in task_collisions(geometry,hulls[side],fixed,initial)]
                    if contacts:raise ControlFailure('Robot mesh/fixed fixture intersection: '+str(contacts[:3]))
                if completed:row['passed']=True;break
            else:raise ControlFailure('Ideal tracking did not reach target within 1,000 controls')
        except Exception as exc:
            row['error']=str(exc);row['joints']={s:v.tolist() for s,v in joints.items()};row['targets']=group;checks.append(row);break
        checks.append(row)
    report=dict(kind='OFFLINE_IDEAL_JOINT_TRACKING',physics_executed=False,control_period_s=.05,
                checked_groups=len(checks),planned_groups=len(groups),ideal_control_steps=total,
                mesh_samples=mesh_samples,mesh_sampling_period_controls=10,
                robot_mesh_checks=['table','opposite arm','anchored fixture bodies'],fixture_motion_collisions_checked='STATIC_ANCHORS_ONLY',
                checks=checks,passed=len(checks)==len(groups) and all(c['passed'] for c in checks))
    print(json.dumps(report,indent=2));return 0 if report['passed'] else 1


if __name__=='__main__':raise SystemExit(audit(Path(__file__).resolve().parent))
