"""Offline reachability and scene-camera audit against the official URDF/calibration.

This does not prove physical grasp success, collisions, or contact dynamics.
"""
import json
import math
from pathlib import Path
import numpy as np
from yam_arena import ik,station
from yam_arena.constants import READY
from feedback import multiply,rotate,conjugate,axis_quat


def camera_coverage(spec,body_states=None):
    camera=station.top_camera();lens=camera.lens
    result={}
    for assembly in spec['assemblies']:
        for body in assembly['bodies']:
            if body.get('inspection_hidden'):continue
            state=(body_states or {}).get(body['name'],body)
            points=[]
            for x in (body['bounds_min'][0],body['bounds_max'][0]):
                for y in (body['bounds_min'][1],body['bounds_max'][1]):
                    for z in (body['bounds_min'][2],body['bounds_max'][2]):
                        world=np.asarray(state['pos'])+rotate(state['quat'],[x,y,z])
                        local=rotate(conjugate(camera.rot_xyzw),world-np.asarray(camera.pos))
                        depth=-local[2]
                        if depth<=0:raise ValueError('Geometry behind overhead camera')
                        points.append([lens.fx*local[0]/depth+lens.cx,lens.cy-lens.fy*local[1]/depth])
            lower=np.min(points,axis=0);upper=np.max(points,axis=0)
            result[body['name']]={'pixels_min':lower.tolist(),'pixels_max':upper.tolist(),
                                 'visible':bool(np.all(lower>=2) and upper[0]<lens.width-2 and upper[1]<lens.height-2)}
    return result


def audit(folder):
    spec=json.loads((folder/'scene.json').read_text());plan=json.loads((folder/'controller.json').read_text())
    checks=[];seeds={s:np.asarray(READY) for s in ('left','right')}
    for i,p in enumerate(plan['phases']):
        side=p['side'];target=p['target']
        q,pe,re=ik.solve(target['pos'],target['quat'],q_init=seeds[side],base_pos=station.BASES[side],iters=700,damping=.015,tol=1e-5)
        seeds[side]=q
        checks.append(dict(phase=i,label=p['label'],side=side,position_error_m=float(pe),rotation_error_rad=float(re),passed=bool(pe<.00035 and re<.025 and np.all(q>ik.LOWER+1e-5) and np.all(q<ik.UPPER-1e-5)),joints=q.tolist()))
    coverage=camera_coverage(spec)
    result=dict(kind='OFFLINE_IK_WAYPOINTS_ONLY',physics_executed=False,checks=checks,camera_coverage=coverage,
                passed=all(r['passed'] for r in checks) and all(r['visible'] for r in coverage.values()))
    print(json.dumps(result,indent=2));return 0 if result['passed'] else 1

if __name__=='__main__':raise SystemExit(audit(Path(__file__).resolve().parent))
