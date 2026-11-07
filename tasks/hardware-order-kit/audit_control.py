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
    bodies={b['name']:b for a in spec['assemblies'] for b in a['bodies']}
    checks=[];seeds={s:np.asarray(READY) for s in ('left','right')}
    # Explicit reachable critical TCP poses include hinge arcs and regrasp endpoints.
    for waypoint in plan['audit_tcp_targets']:
        side=waypoint['side'];p=waypoint['pos'];q=waypoint['quat']
        solved,pe,re=ik.solve(p,q,q_init=seeds[side],base_pos=station.BASES[side],iters=500,damping=0.015,tol=1e-5)
        seeds[side]=solved
        checks.append({'label':waypoint['label'],'side':side,'position_error_m':pe,'rotation_error_rad':re,
                       'pass':bool(pe<=0.0015 and re<=0.035 and np.all(solved>ik.LOWER+1e-5) and np.all(solved<ik.UPPER-1e-5))})
    if not checks:raise ValueError('No critical TCP targets were provided')
    coverage=camera_coverage(spec)
    result={'kind':'OFFLINE_URDF_KINEMATICS_AND_CAMERA_PROJECTION','physics_executed':False,'checks':checks,
            'camera_coverage':coverage,'passed':all(c['pass'] for c in checks) and all(c['visible'] for c in coverage.values())}
    print(json.dumps(result,indent=2))
    return 0 if result['passed'] else 1


if __name__=='__main__':raise SystemExit(audit(Path(__file__).resolve().parent))
