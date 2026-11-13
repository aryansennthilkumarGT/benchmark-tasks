"""Offline reachability and scene-camera audit against the official URDF/calibration.

This does not prove physical grasp success, collisions, or contact dynamics.
"""
import json
import math
from pathlib import Path
import numpy as np
from yam_arena import ik,station
from yam_arena.constants import READY
from motion import multiply,rotate,conjugate,axis_quat


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


if __name__=="__main__":
 s=json.loads(Path(__file__).with_name("scene.json").read_text());coverage=camera_coverage(s);print(json.dumps(dict(kind="OFFLINE_PINNED_CAMERA_FRUSTUM",native_executed=False,coverage=coverage,passed=all(v["visible"] for v in coverage.values())),indent=2));raise SystemExit(0 if all(v["visible"] for v in coverage.values()) else 1)
