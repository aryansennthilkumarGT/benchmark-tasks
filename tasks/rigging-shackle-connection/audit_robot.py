"""Conservative all-endpoint robot/fixture collision checks using pinned URDF hulls.

Checks every authored endpoint, including all thread/regrasp cycles. This is sampled geometry, not swept-volume or native proof.
"""
import json
from pathlib import Path
import numpy as np
from yam_arena import ik,station
from yam_arena.constants import READY
from audit_geometry import geometry_module
from robot_geometry import arm_hulls,task_collisions,table_intersections,inter_arm_intersections
from feedback import rotate


def audit(folder):
    spec=json.loads((folder/'scene.json').read_text());plan=json.loads((folder/'controller.json').read_text())
    g=geometry_module(folder);q={side:np.r_[READY,1.] for side in ('left','right')}
    held={};checks=[]
    for index,p in enumerate(plan['phases']):
        label=p['label'];side=p['side']
        target=p['target']
        solved,pe,re=ik.solve(target['pos'],target['quat'],q_init=q[side][:6],base_pos=station.BASES[side],iters=500,damping=.015,tol=1e-5)
        aperture=p['opening']
        if aperture<.3:
            if p['contact_body']=='shackle':width=.016
            else:
                bodyq=p['nominal_bodies']['pin']['quat']
                jaw=rotate(target['quat'],[1,0,0])
                width=sum(abs(float(np.dot(jaw,rotate(bodyq,axis))))*length
                    for axis,length in [([1,0,0],.024),([0,1,0],.012)])
            # Position-controlled close commands stop at the solid part. Audit
            # measured contact aperture, not jaws intersecting a rigid solid.
            aperture=(width+.0003)/.0939
        q[side]=np.r_[solved,aperture]
        held[side]=p['contact_body']
        hulls={s:arm_hulls(s,q[s]) for s in q}
        contacts=[];table=[]
        for s in hulls:
            collisions=task_collisions(g,hulls[s],spec,p['nominal_bodies'],threshold=.0015)
            for c in collisions:
                if c['body']==held.get(s) and c['link'] in ('tip_left','tip_right') and c['penetration_m']<=.003:
                    continue # declared compliant pad/part contact, never palm contact
                contacts.append(dict(side=s,**c))
            table += [dict(side=s,**r) for r in table_intersections(hulls[s],spec['table_top'])]
        crossing=inter_arm_intersections(g,hulls['left'],hulls['right'])
        row=dict(phase=index,label=label,position_error_m=float(pe),rotation_error_rad=float(re),
            contacts=contacts,table=table,inter_arm=crossing,
            passed=pe<.00035 and re<.025 and not contacts and not table and not crossing)
        checks.append(row)
    report=dict(kind='OFFLINE_ALL_ENDPOINT_COLLISION_SAMPLES',physics_executed=False,
                swept_volume_validated=False,checks=checks,passed=all(r['passed'] for r in checks))
    print(json.dumps(report,indent=2));return 0 if report['passed'] else 1


if __name__=='__main__':raise SystemExit(audit(Path(__file__).resolve().parent))
