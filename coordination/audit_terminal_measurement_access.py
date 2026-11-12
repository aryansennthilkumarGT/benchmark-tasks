"""Offline optical-access geometry checks; no simulator or physical photo claim."""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np


def rotation(q):
    q = np.asarray(q, dtype=float)
    if q.shape != (4,) or not np.isfinite(q).all() or np.linalg.norm(q) < 1e-12:
        raise ValueError('Invalid geometry quaternion')
    x, y, z, w = q / np.linalg.norm(q)
    return np.array([[1-2*(y*y+z*z), 2*(x*y-z*w), 2*(x*z+y*w)],
                     [2*(x*y+z*w), 1-2*(x*x+z*z), 2*(y*z-x*w)],
                     [2*(x*z-y*w), 2*(y*z+x*w), 1-2*(x*x+y*y)]])


def box_interval(origin, delta, half):
    low, high = 0., 1.
    for o, d, h in zip(origin, delta, half):
        if abs(d) < 1e-12:
            if abs(o) >= h-1e-10:
                return None
        else:
            a, b = sorted(((-h-o)/d, (h-o)/d))
            low, high = max(low, a), min(high, b)
    return (low, high) if high-low > 1e-9 else None


def cylinder_interval(origin, delta, radius, height):
    low, high = 0., 1.
    a, b = float(delta[:2]@delta[:2]), float(2*origin[:2]@delta[:2])
    c = float(origin[:2]@origin[:2]-radius*radius)
    if a < 1e-20:
        if c >= -1e-12:
            return None
    else:
        discriminant = b*b-4*a*c
        if discriminant <= 0:
            return None
        p, q = sorted(((-b-discriminant**.5)/(2*a), (-b+discriminant**.5)/(2*a)))
        low, high = max(low, p), min(high, q)
    if abs(delta[2]) < 1e-12:
        if abs(origin[2]) >= height/2-1e-10:
            return None
    else:
        p, q = sorted(((-height/2-origin[2])/delta[2], (height/2-origin[2])/delta[2]))
        low, high = max(low, p), min(high, q)
    return (low, high) if high-low > 1e-9 else None


def shape_hit(start, end, body, shape):
    rb, rs = rotation(body['quat']), rotation(shape.get('quat', [0, 0, 0, 1]))
    matrix = rb@rs
    centre = np.asarray(body['pos'])+rb@np.asarray(shape['pos'])
    origin, delta = matrix.T@(start-centre), matrix.T@(end-start)
    if shape['kind'] == 'box':
        return box_interval(origin, delta, np.asarray(shape['size'])/2)
    if shape['kind'] == 'cylinder':
        return cylinder_interval(origin, delta, shape['radius'], shape['height'])
    raise ValueError('Unsupported visible shape: '+shape['kind'])


def within_clear_patch(start, end, holder, nominal_contact, shape, interval):
    """Only explicitly dimensioned solid transparent patches transmit a ray."""
    local_contact = nominal_contact
    sign = 1 if local_contact[1] > 0 else -1
    y = shape['pos'][1]
    outer = abs(y-sign*.057) < 1e-8 and abs(shape['size'][1]-.006) < 1e-8
    guide = abs(y-(local_contact[1]+sign*.0097)) < 1e-8 and abs(shape['size'][1]-.004) < 1e-8
    if not (outer or guide):
        return False
    for t in interval:
        local = rotation(holder['quat']).T@(start+t*(end-start)-holder['pos'])
        if abs(local[0]-local_contact[0]) > .008 or not .006 <= local[2] <= .012:
            return False
    return True


def audit(spec, frame):
    geometry = {b['name']: b for a in spec['assemblies'] for b in a['bodies']}
    holder = frame['bodies']['holder']
    rh = rotation(holder['quat'])
    results = []
    for index in range(12):
        name = f'contact_{index}'
        cap = frame['bodies'][name]
        nominal = rotation(geometry['holder']['quat']).T@(
            np.asarray(geometry[name]['pos'])-geometry['holder']['pos'])
        local = rh.T@(np.asarray(cap['pos'])-holder['pos'])
        sign = 1 if local[1] > 0 else -1
        witness = np.asarray(cap['pos'])+rotation(cap['quat'])@np.array([0, sign*.006, 0])
        targets = [('witness', witness, name)]
        # Scale and witness use the same contact-front plane, not the outer wall.
        for height in (.0062, .008, .010):
            targets.append((f'scale_{height}', np.asarray(holder['pos'])+
                rh@np.array([nominal[0]+.007, nominal[1]+sign*.006, height]), None))
        checks = []
        for label, end, target_body in targets:
            end_local = rh.T@(end-holder['pos'])
            # A 20 x 8 mm rectangular mirror, 45 degrees, centre Y=+/-110mm,Z=8mm.
            mirror_local = np.array([nominal[0], sign*(.110+end_local[2]-.008), end_local[2]])
            start = np.asarray(holder['pos'])+rh@mirror_local
            blocked, transmitted = [], []
            if (abs(end_local[0]-nominal[0]) > .010
                    or abs(end_local[2]-.008)*2**.5 > .004):
                blocked.append(['proposed_mirror', 'outside_rectangular_aperture'])
            for body_name, body in frame['bodies'].items():
                if body_name == target_body:
                    continue
                # Include noncolliding visual labels: opacity is not a collision test.
                for number, shape in enumerate(geometry[body_name]['shapes']):
                    interval = shape_hit(start, end, body, shape)
                    if interval is None:
                        continue
                    if body_name == 'holder' and within_clear_patch(start, end, holder, nominal, shape, interval):
                        transmitted.append(number)
                    else:
                        blocked.append([body_name, number])
            checks.append({'target': label, 'opaque_intersections': blocked,
                           'transparent_holder_shapes': transmitted})
        results.append({'contact': name, 'witness_height_mm': float(local[2]*1000), 'rays': checks})
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--folder', type=Path, required=True)
    parser.add_argument('--trial', type=Path, action='append', required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    spec = json.loads((args.folder/'scene.json').read_text())
    trials = []
    for trial in args.trial:
        path = trial/'native_frames.jsonl'
        with path.open('rb') as stream:
            stream.seek(max(0, path.stat().st_size-50000))
            row = json.loads(stream.read().splitlines()[-1])
        if row['result']['score'] != 1:
            raise ValueError('Source posture is not an actual full-score final state')
        proof = json.loads((trial/'validated-rollout.json').read_text())
        if (proof['mode'] != 'expert' or proof['score'] != 1
                or abs(row['frame']['time']-proof['simulated_seconds']) > 1e-6
                or hashlib.sha256(Path(proof['log']).read_bytes()).hexdigest() != proof['log_sha256']):
            raise ValueError('Recorded posture/proof provenance differs')
        trials.append({'record_id': proof['record_id'], 'source_commit': proof['commit'],
                       'native_frame_file_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                       'contacts': audit(spec, row['frame'])})
    blocked = sum(len(ray['opaque_intersections']) for t in trials for c in t['contacts'] for ray in c['rays'])
    report = {'kind': 'OFFLINE_PROPOSED_PHYSICAL_OPTICAL_GEOMETRY_NOT_SIMULATION_OR_PHOTOGRAPH',
              'status': 'CALCULATED_ACCESS_CLEAR' if blocked == 0 else 'OCCLUSIONS_FOUND',
              'recorded_success_postures': len(trials), 'rays_checked': len(trials)*12*4,
              'opaque_intersections': blocked, 'trials': trials,
              'mirror_design': {'width_mm': 20, 'height_mm': 8, 'angle_degrees': 45,
                                'holder_relative_y_mm': [-110, 110], 'centre_z_mm': 8,
                                'lowest_z_mm': 8-4/2**.5},
              'limitations': ['Uses dimensioned proposed transparent patches; native walls remain opaque.',
                             'Checks two recorded successful postures, not every allowed state.',
                             'Robot, camera and stand geometry are not included in the task-part rays.',
                             'Does not validate refraction, lens distortion, physical construction or pixel accuracy.',
                             'No physics, robot demonstration or physical photograph was generated.']}
    args.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({k: report[k] for k in ('status', 'rays_checked', 'opaque_intersections')}))
    return 0 if blocked == 0 else 1


if __name__ == '__main__':
    raise SystemExit(main())
