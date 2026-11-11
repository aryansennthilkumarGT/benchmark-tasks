"""Deterministic, simulator-independent scorer. Synthetic test frames are NOT rollouts.

Units: metres, seconds, radians; quaternions XYZW. One observation per control
step. Only the native collector writes observations during an actual episode.
"""
from __future__ import annotations

from dataclasses import dataclass
import math


def finite(values, size):
    return len(values) == size and all(isinstance(x, (int, float)) and not isinstance(x, bool)
                                     and math.isfinite(x) for x in values)


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def norm(a):
    return math.sqrt(sum(x * x for x in a))


def multiply(a, b):
    x, y, z, w = a
    X, Y, Z, W = b
    return (w*X+x*W+y*Z-z*Y, w*Y-x*Z+y*W+z*X,
            w*Z+x*Y-y*X+z*W, w*W-x*X-y*Y-z*Z)


def conjugate(q):
    return (-q[0], -q[1], -q[2], q[3])


def rotate(q, v):
    return multiply(multiply(q, (*v, 0.0)), conjugate(q))[:3]


def angle(a, b):
    return 2 * math.acos(min(1.0, abs(sum(x*y for x, y in zip(a, b)))))


def relative(body, reference):
    qi = conjugate(reference['quat'])
    return rotate(qi, sub(body['pos'], reference['pos'])), multiply(qi, body['quat'])


@dataclass(frozen=True)
class Result:
    score: float
    success: bool
    completed: tuple[str, ...]
    failure: str | None
    first_completion: tuple[tuple[str, float], ...]
    recoveries: int
    simulated_seconds: float


class Scorer:
    def __init__(self, spec):
        self.spec = spec
        self.body_specs = {b['name']: b for a in spec['assemblies'] for b in a['bodies']}
        if len(self.body_specs) != sum(len(a['bodies']) for a in spec['assemblies']):
            raise ValueError('duplicate body name')
        if not spec['goals'] or len({g['name'] for g in spec['goals']}) != len(spec['goals']):
            raise ValueError('goal names must be nonempty and unique')
        if any(not finite([g['weight']],1) or not 0 < g['weight'] <= 1 for g in spec['goals']):
            raise ValueError('goal weights must be finite and positive')
        if abs(sum(g['weight'] for g in spec['goals']) - 1) > 1e-9:
            raise ValueError('goal weights must sum to one')
        self.joint_specs = {j['name']: j for a in spec['assemblies'] for j in a.get('joints', [])}
        for group in spec['goals'] + spec.get('invariants', []):
            for p in group['all']:
                if p['kind'] not in {'pose','region','still','axis','joint','turns'}:
                    raise ValueError('unknown predicate kind')
                if p['kind']=='pose' and 'position_axis' in p:
                    axis = p['position_axis']
                    if (not finite(axis, 3) or abs(norm(axis)-1) > 1e-9
                            or not finite([p.get('axial_tolerance')], 1) or p['axial_tolerance'] <= 0):
                        raise ValueError('Invalid radial or axial pose tolerance')
                if p['kind']=='joint':
                    if p['joint'] not in self.joint_specs:raise ValueError('unknown joint')
                elif p['body'] not in self.body_specs:raise ValueError('unknown body')
                if p.get('relative_to') and p['relative_to'] not in self.body_specs:
                    raise ValueError('unknown reference body')
        self.reset()

    def reset(self):
        self.last_time = None
        self.last_frame = None
        self.previous_observation = None
        self.failed = None
        self.hold_start = None
        self.first = {}
        self.previous = set()
        self.recoveries = 0
        self.lost = set()
        self.turns = {t['body']: 0.0 for t in self.spec.get('threads', [])}
        self.thread_previous = {}
        self.thread_origins = {}
        self.thread_angles = {}
        self.result = Result(0.0, False, (), None, (), 0, 0.0)

    def _validate(self, f):
        if not isinstance(f, dict) or f.get('schema') != 1:
            return 'invalid_frame_schema'
        if not finite([f.get('time')], 1) or f['time'] < 0:
            return 'invalid_time'
        if not isinstance(f.get('bodies'), dict) or set(f['bodies']) != set(self.body_specs):
            return 'missing_or_unexpected_body'
        if not finite([f.get('robot_clearance')], 1):
            return 'missing_robot_clearance'
        if not finite([f.get('max_penetration')], 1) or f['max_penetration'] < 0:
            return 'invalid_penetration'
        expected = {j['name'] for a in self.spec['assemblies'] for j in a.get('joints', [])}
        if not isinstance(f.get('joints'), dict) or set(f['joints']) != expected:
            return 'missing_or_unexpected_joint'
        if not finite(list(f['joints'].values()), len(expected)):
            return 'nonfinite_joint'
        for name, b in f['bodies'].items():
            if not isinstance(b,dict):return f'invalid_body:{name}'
            for field, count in [('pos', 3), ('quat', 4), ('linear', 3), ('angular', 3)]:
                if not isinstance(b.get(field), (list, tuple)) or not finite(b[field], count):
                    return f'invalid_{field}:{name}'
            if abs(norm(b['quat']) - 1) > 1e-5:
                return f'unnormalized_quaternion:{name}'
        return None

    def observed_motion(self, name, frame):
        """Rates measurable from adjacent control-rate poses, with raw fallback."""
        previous = self.previous_observation
        if previous is not None:
            elapsed = frame['time'] - previous['time']
            if 0 < elapsed <= 1.5 / self.spec['control_hz']:
                before = previous['bodies'][name]
                body = frame['bodies'][name]
                return (norm(sub(body['pos'], before['pos'])) / elapsed,
                        angle(body['quat'], before['quat']) / elapsed)
        body = frame['bodies'][name]
        return norm(body['linear']), norm(body['angular'])

    def predicate(self, p, f):
        kind = p['kind']
        if kind == 'turns':
            return self.turns[p['body']] + 1e-9 >= p['min']
        if kind == 'joint':
            return p['min'] - 1e-10 <= f['joints'][p['joint']] <= p['max'] + 1e-10
        b = f['bodies'][p['body']]
        pos, quat = b['pos'], b['quat']
        if p.get('relative_to'):
            pos, quat = relative(b, f['bodies'][p['relative_to']])
        if kind == 'pose':
            delta = sub(pos, p['pos'])
            positioned = norm(delta) <= p['tolerance'] + 1e-10
            if 'position_axis' in p:
                axial = sum(a*b for a, b in zip(delta, p['position_axis']))
                radial = sub(delta, tuple(axial*a for a in p['position_axis']))
                positioned = (norm(radial) <= p['tolerance'] + 1e-10
                              and abs(axial) <= p['axial_tolerance'] + 1e-10)
            return positioned and angle(quat, p.get('quat', [0, 0, 0, 1])) <= p['angle'] + 1e-10
        if kind == 'axis':
            actual = rotate(quat, p.get('local_axis', [0, 0, 1]))
            return sum(a*b for a, b in zip(actual, p['direction'])) >= math.cos(p['angle'])-1e-10
        if kind == 'region':
            # Entire oriented collision bound, not only the centre, must fit.
            bs = self.body_specs[p['body']]
            corners = [add(pos, rotate(quat, (x,y,z)))
                       for x in (bs['bounds_min'][0],bs['bounds_max'][0])
                       for y in (bs['bounds_min'][1],bs['bounds_max'][1])
                       for z in (bs['bounds_min'][2],bs['bounds_max'][2])]
            return all(all(lo-1e-10 <= v <= hi+1e-10 for v, lo, hi in zip(c, p['min'], p['max']))
                       for c in corners)
        if kind == 'still':
            speed, spin = self.observed_motion(p['body'], f)
            return speed <= p.get('speed', 0.01) and spin <= p.get('spin', 0.2)
        raise ValueError(f'unsupported predicate {kind}')

    def update(self, frame):
        error = self._validate(frame)
        now = frame.get('time', 0.0) if isinstance(frame, dict) else 0.0
        if error:
            self.failed = self.failed or error
            self.result = Result(0.0, False, (), self.failed, tuple(sorted(self.first.items())),
                                 self.recoveries, self.last_time or 0.0)
            return self.result
        if self.last_time is not None and now <= self.last_time:
            if now == self.last_time and frame == self.last_frame:
                return self.result  # success() + score() cannot double-count time.
            self.failed = self.failed or 'nonmonotonic_or_conflicting_frame'
        if self.last_time is not None and now - self.last_time > 1.5 / self.spec['control_hz']:
            self.hold_start = None  # an unobserved time gap cannot prove stability.
        previous_frame=self.last_frame
        self.previous_observation = previous_frame
        import copy
        self.last_time, self.last_frame = now, copy.deepcopy(frame)
        for name, bs in self.body_specs.items():
            b = frame['bodies'][name]
            # Check lowest corner, including rotation, against loss plane.
            bottom = min(add(b['pos'], rotate(b['quat'], (x,y,z)))[2]
                         for x in (bs['bounds_min'][0],bs['bounds_max'][0])
                         for y in (bs['bounds_min'][1],bs['bounds_max'][1])
                         for z in (bs['bounds_min'][2],bs['bounds_max'][2]))
            if bottom < self.spec['table_top'] - 0.025:
                self.failed = self.failed or f'off_table:{name}'
            if bs.get('anchor'):
                if (norm(sub(b['pos'], bs['pos'])) > 0.005
                        or angle(b['quat'], bs['quat']) > math.radians(3)):
                    self.failed = self.failed or f'fixture_moved:{name}'
        if frame['max_penetration'] > self.spec['penetration_limit']:
            self.failed = self.failed or 'interpenetration'
        for name,j in self.joint_specs.items():
            margin = 0.01 if j['kind']=='revolute' else 0.0005
            if not j['lower']-margin <= frame['joints'][name] <= j['upper']+margin:
                self.failed = self.failed or f'joint_limit_violation:{name}'
        for connection in self.spec.get('continuity',[]):
            joint=self.joint_specs[connection['joint']]
            parent=frame['bodies'][joint['parent']];child=frame['bodies'][joint['child']]
            left=add(parent['pos'],rotate(parent['quat'],joint['pivot_parent']))
            right=add(child['pos'],rotate(child['quat'],joint['pivot_child']))
            if norm(sub(left,right))>connection['tolerance']:
                self.failed=self.failed or 'broken_connection:'+connection['joint']
        if previous_frame is not None:
            for guard in self.spec.get('latch_release_guards',[]):
                body=guard['body'];name=guard['joint']
                for port in guard['ports']:
                    before,_=relative(previous_frame['bodies'][body],previous_frame['bodies'][port])
                    after,_=relative(frame['bodies'][body],frame['bodies'][port])
                    crosses=(abs(before[0])<.004 and abs(before[2])<.006
                             and -.004<=before[1]<=guard['catch_distance']<after[1])
                    if crosses and min(previous_frame['joints'][name],frame['joints'][name])>guard['release_below']:
                        self.failed=self.failed or 'catch_forced_without_release:'+body
        for guard in self.spec.get('invariants', []):
            if not all(self.predicate(p, frame) for p in guard['all']):
                self.failed = self.failed or guard['name']
        for forbidden in self.spec.get('forbidden_regions', []):
            bs=self.body_specs[forbidden['body']];b=frame['bodies'][forbidden['body']]
            corners=[add(b['pos'],rotate(b['quat'],(x,y,z)))
                     for x in (bs['bounds_min'][0],bs['bounds_max'][0])
                     for y in (bs['bounds_min'][1],bs['bounds_max'][1])
                     for z in (bs['bounds_min'][2],bs['bounds_max'][2])]
            if all(max(c[i] for c in corners)>forbidden['min'][i]
                   and min(c[i] for c in corners)<forbidden['max'][i] for i in range(3)):
                self.failed = self.failed or f'forbidden_part_in_kit:{forbidden["body"]}'
        for thread in self.spec.get('threads', []):
            name = thread['body']
            pos, quat = relative(frame['bodies'][name], frame['bodies'][thread['reference']])
            theta = 2 * math.atan2(quat[2], quat[3])
            engaged = (math.hypot(pos[0]-thread['xy'][0], pos[1]-thread['xy'][1]) <= thread['radial_tolerance']
                       and thread['z_min'] <= pos[2] <= thread['z_max'])
            previous = self.thread_previous.get(name)
            if not engaged:
                self.turns[name] = 0.0
                self.thread_origins.pop(name, None)
                self.thread_angles.pop(name, None)
            elif previous is None or not previous[2]:
                self.thread_origins[name] = pos[2]
                self.thread_angles[name] = 0.0
            if engaged and previous is not None and previous[2]:
                delta = (theta-previous[0]+math.pi) % (2*math.pi)-math.pi
                if abs(delta) > 0.75:
                    self.failed = self.failed or f'undersampled_thread_rotation:{name}'
                self.thread_angles[name] += delta
                # Coupling is cumulative, so many tiny in-place spins cannot exploit per-step slack.
                expected = thread['pitch'] * self.thread_angles[name] / (2*math.pi)
                error = abs(pos[2]-self.thread_origins[name]-expected)
                self.turns[name] = (max(0.0, -self.thread_angles[name]/(2*math.pi))
                                    if error <= thread['axial_slack'] else 0.0)
            self.thread_previous[name] = (theta, pos[2], engaged)
        active = {g['name'] for g in self.spec['goals']
                  if all(self.predicate(p, frame) for p in g['all'])}
        for name in active:
            self.first.setdefault(name, now)
            if name in self.lost:
                self.recoveries += 1
                self.lost.remove(name)
        self.lost.update(self.previous - active)
        self.previous = active
        all_done = len(active) == len(self.spec['goals']) and frame['robot_clearance'] >= 0.02
        all_still = all(speed <= 0.01 and spin <= 0.2
                        for speed, spin in (self.observed_motion(name, frame)
                                            for name in frame['bodies']))
        if all_done and all_still and not self.failed:
            if self.hold_start is None:
                self.hold_start = now
        else:
            self.hold_start = None
        success = self.hold_start is not None and now-self.hold_start+1e-10 >= self.spec['hold_seconds']
        credit = sum(g['weight'] for g in self.spec['goals'] if g['name'] in active)
        score = 0.0 if self.failed else (1.0 if success else min(0.95, credit))
        self.result = Result(score, bool(success), tuple(sorted(active)), self.failed,
                             tuple(sorted(self.first.items())), self.recoveries, now)
        return self.result
