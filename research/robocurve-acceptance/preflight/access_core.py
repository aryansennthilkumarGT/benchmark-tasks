"""CPU-only source-bound FK, convex geometry and conservative swept-access checks.

No simulator, IK policy, task actions, object state changes or empirical task claim.
A clear sweep is certified only when conservative motion envelopes separate.
Intersecting envelopes are INCONCLUSIVE unless endpoint model intersection exists.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
from functools import lru_cache
from pathlib import Path

import numpy as np
from scipy.spatial import ConvexHull

ROOT = Path(__file__).resolve().parent
JOINT_NAMES = [f'joint{i}' for i in range(1, 9)]
GUARD_M = 1e-8  # Numerical design guard, not an OEM tolerance or measured clearance.


def rpy_matrix(v):
    r, p, y = v
    cr, sr, cp, sp, cy, sy = np.cos(r), np.sin(r), np.cos(p), np.sin(p), np.cos(y), np.sin(y)
    return np.array([[cy*cp, cy*sp*sr-sy*cr, cy*sp*cr+sy*sr],
                     [sy*cp, sy*sp*sr+cy*cr, sy*sp*cr-cy*sr], [-sp, cp*sr, cp*cr]])


def transform(xyz=(0., 0., 0.), rpy=(0., 0., 0.)):
    m = np.eye(4)
    m[:3, :3], m[:3, 3] = rpy_matrix(rpy), xyz
    return m


def axis_rotation(axis, angle):
    a = np.asarray(axis, float)
    a /= np.linalg.norm(a)
    k = np.array([[0., -a[2], a[1]], [a[2], 0., -a[0]], [-a[1], a[0], 0.]])
    return np.eye(3) + np.sin(angle)*k + (1-np.cos(angle))*(k@k)


def points_at(vertices, pose):
    return np.asarray(vertices) @ pose[:3, :3].T + pose[:3, 3]


def aabb(vertices):
    p = np.asarray(vertices)
    return p.min(axis=0), p.max(axis=0)


def aabb_separated(a, b, inflate_a=0., inflate_b=0.):
    alo, ahi = a
    blo, bhi = b
    return bool(np.any(ahi + inflate_a + GUARD_M < blo - inflate_b) or
                np.any(bhi + inflate_b + GUARD_M < alo - inflate_a))


def convex_intersects(a, b):
    """Convex SAT, incl. face and cross-edge axes. Contact within guard is intersection.

    Result applies to supplied collision hulls, not a certification of real hardware.
    """
    a, b = np.asarray(a, float), np.asarray(b, float)
    if aabb_separated(aabb(a), aabb(b)):
        return False
    ha, hb = ConvexHull(a), ConvexHull(b)
    axes = [*ha.equations[:, :3], *hb.equations[:, :3]]

    def edges(p, hull):
        out = []
        for tri in hull.simplices:
            for i, j in [(0, 1), (1, 2), (2, 0)]:
                v = p[tri[j]] - p[tri[i]]
                if np.linalg.norm(v) > 1e-12:
                    out.append(v / np.linalg.norm(v))
        return np.unique(np.round(out, 10), axis=0)
    ea, eb = edges(a, ha), edges(b, hb)
    if len(ea) and len(eb):
        axes.extend(np.cross(ea[:, None, :], eb[None, :, :]).reshape(-1, 3))
    axes = np.asarray(axes)
    norms = np.linalg.norm(axes, axis=1)
    axes = axes[norms > 1e-10] / norms[norms > 1e-10, None]
    # Process in blocks rather than allocate unbounded projections.
    for start in range(0, len(axes), 256):
        ax = axes[start:start+256]
        pa, pb = a @ ax.T, b @ ax.T
        if np.any(pa.max(axis=0) + GUARD_M < pb.min(axis=0)) or np.any(pb.max(axis=0) + GUARD_M < pa.min(axis=0)):
            return False
    return True


class Robot:
    def __init__(self, path=ROOT / 'assets/YAM_REFERENCE.json.gz'):
        path = Path(path)
        self.bundle_sha256 = hashlib.sha256(path.read_bytes()).hexdigest()
        with gzip.open(path, 'rt') as f:
            self.data = json.load(f)
        self.joints = self.data['joints']
        self.by_name = {x['name']: x for x in self.joints}
        self.by_child = {x['child']: x for x in self.joints}
        self.hulls = []
        for name, link in self.data['links'].items():
            for h in link['hulls']:
                self.hulls.append({'name': h['name'], 'link': name,
                                   'vertices': np.asarray(h['vertices_link_m'], float)})
        self.chain = {}
        for name in self.data['links']:
            anc, child = [], name
            while child in self.by_child:
                j = self.by_child[child]
                anc.append(j)
                child = j['parent']
            self.chain[name] = list(reversed(anc))
        self.base_poses = {s: transform(p) for s, p in self.data['station_bases_m'].items()}

    def validate_q(self, q):
        if len(q) != 8 or not np.all(np.isfinite(q)):
            raise ValueError('Each arm needs eight finite actual joint coordinates (six rad, two m).')
        for name, value in zip(JOINT_NAMES, q):
            j = self.by_name[name]
            if not j['lower'] - 1e-12 <= value <= j['upper'] + 1e-12:
                raise ValueError(f'{name}={value} outside pinned URDF limits')

    def fk(self, q, side='left'):
        self.validate_q(q)
        return self._fk_cached(tuple(float(x) for x in q), side)

    @lru_cache(maxsize=1024)
    def _fk_cached(self, q, side):
        values = dict(zip(JOINT_NAMES, q))
        poses, joint_frames = {'base': self.base_poses[side]}, {}
        for j in self.joints:
            o = poses[j['parent']] @ transform(j['xyz_m'], j['rpy_rad'])
            joint_frames[j['name']] = o
            motion = np.eye(4)
            if j['type'] == 'revolute':
                motion[:3, :3] = axis_rotation(j['axis'], values[j['name']])
            elif j['type'] == 'prismatic':
                motion[:3, 3] = np.asarray(j['axis']) * values[j['name']]
            poses[j['child']] = o @ motion
        return poses, joint_frames

    def tcp(self, q, side='left'):
        poses, _ = self.fk(q, side)
        return (poses['gripper'] @ np.r_[self.data['tcp_offset_m'], 1.])[:3]

    def world_hulls(self, q, side):
        poses, _ = self.fk(q, side)
        return [{**h, 'world': points_at(h['vertices'], poses[h['link']])} for h in self.hulls]

    def movement_bound(self, link, vertices_link, q0, q1):
        """Upper bound on displacement of EVERY hull point over linear joint interpolation.

        For each upstream revolute joint use |dq| times a configuration-independent
        downstream lever bound (sum of origin lengths, prismatic range, local radius).
        Sum triangle inequality over all joints. No endpoint-only sweep claim.
        """
        chain = self.chain[link]
        local_radius = float(np.linalg.norm(vertices_link, axis=1).max())
        dq = dict(zip(JOINT_NAMES, np.abs(np.asarray(q1) - q0)))
        bound = 0.
        for k, j in enumerate(chain):
            if j['type'] == 'prismatic':
                bound += dq[j['name']]
                continue
            lever = local_radius
            for downstream in chain[k+1:]:
                lever += np.linalg.norm(downstream['xyz_m'])
                if downstream['type'] == 'prismatic':
                    lever += max(abs(downstream['lower']), abs(downstream['upper']))
            bound += lever * dq[j['name']]
        return float(bound)

    def necessary_tcp_radius(self):
        return float(sum(np.linalg.norm(j['xyz_m']) for j in self.chain['gripper']) +
                     np.linalg.norm(self.data['tcp_offset_m']))

    def jacobian_and_gravity(self, q, side='left'):
        poses, frames = self.fk(q, side)
        tcp = self.tcp(q, side)
        jac = np.zeros((6, 6))
        gravity_load = np.zeros(6)
        for k in range(6):
            j = self.by_name[f'joint{k+1}']
            axis = frames[j['name']][:3, :3] @ np.asarray(j['axis'])
            pivot = frames[j['name']][:3, 3]
            jac[:3, k] = np.cross(axis, tcp - pivot)
            jac[3:, k] = axis
            for link, info in self.data['links'].items():
                if j not in self.chain[link]:
                    continue
                com = (poses[link] @ np.r_[info['com_m'], 1.])[:3]
                fg = np.array([0., 0., -9.80665 * info['mass_kg']])
                gravity_load[k] += np.dot(axis, np.cross(com - pivot, fg))
        return jac, gravity_load

    def static_force_ceiling(self, q, direction, side='left'):
        """Optimistic configured static TCP point-force ceiling, no tool/grip/dynamics.

        This is NOT achievable task force or impulse. Required task load is unknown.
        """
        jac, gravity = self.jacobian_and_gravity(q, side)
        direction = np.asarray(direction, float)
        direction /= np.linalg.norm(direction)
        coefficients = jac[:3].T @ direction
        low, high = 0., float('inf')
        active = None
        for k, (a, g) in enumerate(zip(coefficients, gravity)):
            lim = self.data['actuator_effort_configuration'][f'joint{k+1}']
            if abs(a) < 1e-12:
                if abs(g) > lim:
                    return {'feasible_static_interval_N': None, 'reason': 'Model gravity alone exceeds effort configuration.'}
                continue
            l, h = sorted(((-lim-g)/a, (lim-g)/a))
            low = max(low, l)
            if h < high:
                high, active = h, f'joint{k+1}'
        return {'direction_world': direction.tolist(),
                'direction_semantics': 'External force on robot TCP; force applied by robot to object has opposite direction.',
                'feasible_static_interval_N': [float(low), float(high)] if high >= low else None,
                'limiting_configured_joint': active,
                'scope': 'Optimistic static TCP point-force screening at this q, model gravity only; no payload/grip/contact/dynamics/impact or hardware certification.'}

    def describe(self):
        q = self.data['ready_joint_radians'] + [-.04695, -.04695]
        jac, gravity = self.jacobian_and_gravity(q)
        shape_bounds = {}
        poses, _ = self.fk(q)
        for name in ['tip_left', 'tip_right', 'gripper', 'link5', 'link4']:
            pts = np.concatenate([h['vertices'] for h in self.hulls if h['link'] == name])
            shape_bounds[name] = {'collision_hulls': sum(h['link'] == name for h in self.hulls),
                                  'local_axis_extents_m': np.ptp(pts, axis=0).tolist()}
        return {'pin': self.data['pin'], 'asset_source_commit': self.data['asset_source_commit'],
                'bundle_sha256': self.bundle_sha256,
                'collision_hulls_per_arm': len(self.hulls),
                'collision_hulls_per_link': {k: len(v['hulls']) for k, v in self.data['links'].items()},
                'station_bases_m': self.data['station_bases_m'],
                'nominal_aperture_m': .0939,
                'necessary_only_TCP_radius_about_base_m': self.necessary_tcp_radius(),
                'ready_joint_coordinates': q,
                'ready_TCP_left_m': self.tcp(q, 'left').tolist(),
                'ready_TCP_right_m': self.tcp(q, 'right').tolist(),
                'ready_Jacobian_linear_then_angular': jac.tolist(),
                'analysis_gravity_m_s2': 9.80665,
                'ready_gravity_joint_load_Nm_no_tool': gravity.tolist(),
                'ready_static_force_ceiling_up': self.static_force_ceiling(q, [0., 0., 1.]),
                'ready_static_force_ceiling_down': self.static_force_ceiling(q, [0., 0., -1.]),
                'local_collision_shape_bounds': shape_bounds,
                'limits': ['Necessary reach sphere is NOT a reachable workspace/IK result.',
                           'Gravity/Jacobian are static source-model calculations, not impact/actuator certification.',
                           'Cameras, task geometry, grasp loads and actual work poses remain separate inputs.']}


def interpolate(a, b, t):
    return {s: (np.asarray(a[s])*(1-t) + np.asarray(b[s])*t).tolist() for s in ['left', 'right']}


def certify_static_obstacle_interval(robot, arm, hull, q0, q1, obstacle, depth=0, max_depth=8):
    """Adaptive conservative sweep vs a source-bound FIXED convex obstacle.

    Returns CLEAR only when all subinterval enclosures separate. If max depth is
    reached with overlapping enclosures: INCONCLUSIVE, never an endpoint-based pass.
    """
    start_poses, _ = robot.fk(q0, arm)
    end_poses, _ = robot.fk(q1, arm)
    a = points_at(hull['vertices'], start_poses[hull['link']])
    b = points_at(hull['vertices'], end_poses[hull['link']])
    if convex_intersects(a, obstacle) or convex_intersects(b, obstacle):
        return 'COLLISION_MODEL_INTERSECTION'
    rho = robot.movement_bound(hull['link'], hull['vertices'], np.asarray(q0), q1)
    if aabb_separated(aabb(a), aabb(obstacle), rho):
        return 'CLEAR_CONSERVATIVE_ENCLOSURE'
    if depth >= max_depth:
        return 'INCONCLUSIVE_SWEEP_BOUND'
    mid = ((np.asarray(q0) + q1)/2).tolist()
    results = [certify_static_obstacle_interval(robot, arm, hull, q0, mid, obstacle, depth+1, max_depth),
               certify_static_obstacle_interval(robot, arm, hull, mid, q1, obstacle, depth+1, max_depth)]
    if 'COLLISION_MODEL_INTERSECTION' in results:
        return 'COLLISION_MODEL_INTERSECTION'
    return 'CLEAR_CONSERVATIVE_ENCLOSURE' if all(r == 'CLEAR_CONSERVATIVE_ENCLOSURE' for r in results) else 'INCONCLUSIVE_SWEEP_BOUND'


def certify_interarm_interval(robot, ha, hb, a0, a1, depth=0, max_depth=8, side_a='left', side_b='right'):
    pa0, _ = robot.fk(a0[side_a], side_a)
    pb0, _ = robot.fk(a0[side_b], side_b)
    pa1, _ = robot.fk(a1[side_a], side_a)
    pb1, _ = robot.fk(a1[side_b], side_b)
    va, vb = points_at(ha['vertices'], pa0[ha['link']]), points_at(hb['vertices'], pb0[hb['link']])
    va1, vb1 = points_at(ha['vertices'], pa1[ha['link']]), points_at(hb['vertices'], pb1[hb['link']])
    if convex_intersects(va, vb) or convex_intersects(va1, vb1):
        return 'COLLISION_MODEL_INTERSECTION'
    ra = robot.movement_bound(ha['link'], ha['vertices'], np.asarray(a0[side_a]), a1[side_a])
    rb = robot.movement_bound(hb['link'], hb['vertices'], np.asarray(a0[side_b]), a1[side_b])
    if aabb_separated(aabb(va), aabb(vb), ra, rb):
        return 'CLEAR_CONSERVATIVE_ENCLOSURE'
    if depth >= max_depth:
        return 'INCONCLUSIVE_SWEEP_BOUND'
    mid = interpolate(a0, a1, .5)
    rs = [certify_interarm_interval(robot, ha, hb, a0, mid, depth+1, max_depth, side_a, side_b),
          certify_interarm_interval(robot, ha, hb, mid, a1, depth+1, max_depth, side_a, side_b)]
    if 'COLLISION_MODEL_INTERSECTION' in rs:
        return 'COLLISION_MODEL_INTERSECTION'
    return 'CLEAR_CONSERVATIVE_ENCLOSURE' if all(r == 'CLEAR_CONSERVATIVE_ENCLOSURE' for r in rs) else 'INCONCLUSIVE_SWEEP_BOUND'


def audit_inputs(data):
    """Missing/untrusted dimensions stay missing; descriptive part IDs are not dimensions."""
    missing = []
    for name in data['required_geometry']:
        v = data.get('geometry_inputs', {}).get(name)
        if not isinstance(v, dict) or v.get('value') is None:
            missing.append({'input': name, 'reason': 'No numeric geometry/shape supplied.'})
        elif v.get('status') not in ['source_bound', 'measured'] or not v.get('source_ref'):
            missing.append({'input': name, 'reason': 'Assumed/unsourced input is not trusted candidate geometry.'})
    if not data.get('path'):
        missing.append({'input': 'two_arm_joint_path', 'reason': 'No complete full-scale essential procedure path.'})
    if not data.get('static_obstacles'):
        missing.append({'input': 'full_surroundings_collision_geometry', 'reason': 'Door/cowl/block/tool surroundings not supplied.'})
    for obstacle in (data.get('static_obstacles') or []):
        if obstacle.get('status') not in ['source_bound', 'measured'] or not obstacle.get('source_ref') or not obstacle.get('vertices_world_m'):
            missing.append({'input': obstacle.get('name', 'obstacle'), 'reason': 'Untrusted/incomplete obstacle hull.'})
    if not data.get('moving_body_sweep_envelopes'):
        missing.append({'input': 'tools_panel_or_payload_swept_envelopes', 'reason': 'Moving tool/panel/payload clearance is not a point-TCP check.'})
    else:
        for obstacle in data['moving_body_sweep_envelopes']:
            if obstacle.get('status') not in ['source_bound', 'measured'] or not obstacle.get('source_ref') or not obstacle.get('vertices_world_m'):
                missing.append({'input': obstacle.get('name', 'payload'), 'reason': 'Payload full swept envelope untrusted/incomplete.'})
    path = data.get('path') or []
    phases = {x.get('phase') for x in path}
    for phase in data['essential_phases']:
        if phase not in phases:
            missing.append({'input': phase, 'reason': 'Essential procedure phase not covered by joint path.'})
    sites = set(data.get('required_sites') or [])
    covered = {x.get('site') for x in path}
    if data.get('requires_site_inventory') and not sites:
        missing.append({'input': 'actual_site_inventory', 'reason': 'Clip/branch/attachment site count and positions are unbound.'})
    for site in sorted(sites - covered):
        missing.append({'input': site, 'reason': 'Required site absent from complete path.'})
    return missing


def evaluate(data, robot):
    missing = audit_inputs(data)
    result = {'candidate': data['candidate'], 'input_status': 'BLOCKED_MISSING_INPUTS' if missing else 'COMPLETE_PROVENANCE_DECLARED',
              'access_decision': 'NOT_CLEARED', 'empirical_candidate_test': False,
              'physical_task_or_simulation_executed': False,
              'input_sha256': hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest(),
              'robot_reference': robot.describe(), 'missing_inputs': missing,
              'force_inputs_missing': [k for k in data.get('required_force_inputs', [])
                                       if data.get('force_inputs', {}).get(k, {}).get('value') is None],
              'reach': 'NOT_ASSESSED_WITHOUT_SOURCE_BOUND_TARGETS',
              'swept_access': 'NOT_ASSESSED_WITHOUT_COMPLETE_GEOMETRY_AND_PATH',
              'not_tested': ['Grasp stability/friction, dynamic torque/impulse and compliant mechanism response.',
                             'Current ownership/importance, physical scoring and end-state mechanism correctness.',
                             'Sensor/fixture geometry not in the pinned asset and unvalidated expected contacts.',
                             'Declared expected tool contacts are not contact-force proofs.',
                             'Whole adjacent-link pairs and intentional finger-carriage overlap are exempt; unintended adjacent-link contact is not certified.']}
    if missing:
        return result
    # No object-specific guessed dimensions or fabricated paths are synthesized here.
    path = data['path']
    for frame in path:
        for side in ['left', 'right']:
            robot.validate_q(frame[side])
    necessary = []
    for target in data.get('targets', []):
        if not target.get('source_ref') or target.get('status') not in ['source_bound', 'measured']:
            raise ValueError('Reach target needs trustworthy geometry provenance.')
        d = float(np.linalg.norm(np.asarray(target['xyz_m']) - robot.data['station_bases_m'][target['arm']]))
        necessary.append({'name': target['name'], 'distance_from_base_m': d,
                          'outside_necessary_sphere': d > robot.necessary_tcp_radius()+GUARD_M})
    result['reach'] = necessary or 'NO_TARGET_POSE_COMPARISON_SUPPLIED'
    if not necessary:
        result['input_status'] = 'BLOCKED_MISSING_TARGET_POSES'
        return result
    # TCP orientation/position demands must match FK of the actual supplied path.
    errors = []
    for target in data['targets']:
        frame = path[target['frame_index']]
        poses, _ = robot.fk(frame[target['arm']], target['arm'])
        pos_error = float(np.linalg.norm(robot.tcp(frame[target['arm']], target['arm']) - target['xyz_m']))
        rot = poses['gripper'][:3, :3].T @ rpy_matrix(target['rpy_rad'])
        angle = float(np.arccos(np.clip((np.trace(rot)-1)/2, -1., 1.)))
        errors.append({'name': target['name'], 'position_error_m': pos_error, 'orientation_error_rad': angle,
                       'within_declared_tolerances': pos_error <= target['position_tolerance_m'] and angle <= target['angle_tolerance_rad']})
    result['target_pose_errors'] = errors
    checks = []
    obstacles = data['static_obstacles'] + data['moving_body_sweep_envelopes']
    # Conservative whole-workpiece swept envelopes are treated as forbidden occupied
    # volume to certify robot non-contact access; expected contact links are excluded
    # explicitly and remain unverified interactions, never counted as force passes.
    excluded = {(x['arm'], x['link'], x['object']) for x in data.get('declared_contact_interfaces', [])}
    if any(link not in ['tip_left', 'tip_right'] for _, link, _ in excluded):
        raise ValueError('Expected contacts cannot mask the full palm/wrist/arm. Use explicit fingertip interfaces only.')
    if len(path) < 2:
        raise ValueError('At least two actual two-arm path frames are required.')
    for payload in data['moving_body_sweep_envelopes']:
        for obj in data['static_obstacles']:
            if convex_intersects(np.asarray(payload['vertices_world_m']), np.asarray(obj['vertices_world_m'])):
                checks.append({'payload': payload['name'], 'object': obj['name'],
                               'outcome': 'PAYLOAD_SWEEP_ENVELOPE_OVERLAP_REQUIRES_POSEWISE_CONTACT_CHECK'})
    for i, (f0, f1) in enumerate(zip(path, path[1:])):
        for side in ['left', 'right']:
            for hull in robot.hulls:
                for obj in obstacles:
                    if (side, hull['link'], obj['name']) in excluded:
                        continue
                    outcome = certify_static_obstacle_interval(robot, side, hull, f0[side], f1[side], np.asarray(obj['vertices_world_m']))
                    if outcome != 'CLEAR_CONSERVATIVE_ENCLOSURE':
                        checks.append({'segment': i, 'arm': side, 'link': hull['link'], 'hull': hull['name'], 'object': obj['name'], 'outcome': outcome})
        for ha in robot.hulls:
            for hb in robot.hulls:
                outcome = certify_interarm_interval(robot, ha, hb, f0, f1)
                if outcome != 'CLEAR_CONSERVATIVE_ENCLOSURE':
                    checks.append({'segment': i, 'pair': [ha['name'], hb['name']], 'outcome': outcome})
        # Nonadjacent same-arm checks; adjacent designed joints and the documented
        # overlapping finger carriages are explicit geometric exemptions, not
        # permission to ignore a wrist or the second arm in task surroundings.
        adjacent = {frozenset((j['parent'], j['child'])) for j in robot.joints}
        adjacent.add(frozenset(('tip_left', 'tip_right')))
        for side in ['left', 'right']:
            for k, ha in enumerate(robot.hulls):
                for hb in robot.hulls[k+1:]:
                    if ha['link'] == hb['link'] or frozenset((ha['link'], hb['link'])) in adjacent:
                        continue
                    outcome = certify_interarm_interval(robot, ha, hb, f0, f1, side_a=side, side_b=side)
                    if outcome != 'CLEAR_CONSERVATIVE_ENCLOSURE':
                        checks.append({'segment': i, 'arm': side, 'self_pair': [ha['name'], hb['name']], 'outcome': outcome})
    result['nonclear_sweep_checks'] = checks
    result['declared_contact_interfaces_not_force_validated'] = data.get('declared_contact_interfaces', [])
    good = (len(path) >= 2 and all(x['within_declared_tolerances'] for x in errors)
            and not any(x['outside_necessary_sphere'] for x in necessary) and not checks)
    result['swept_access'] = 'CLEAR_FOR_SUPPLIED_MODEL_AND_PATH_ONLY' if good else 'COLLISION_OR_UNRESOLVED_MODEL_PATH'
    # No full feasibility PASS even with a geometric certificate: self/contact/force
    # and actual mechanism execution remain outside this evaluator.
    result['access_decision'] = 'PARTIAL_GEOMETRIC_CERTIFICATE_ONLY' if good else 'NOT_CLEARED'
    return result


def main(candidate):
    p = argparse.ArgumentParser(description='CPU source-bound full collision geometry access preflight; missing data never passes.')
    p.add_argument('--input', type=Path, default=ROOT / 'inputs' / f'{candidate}.json')
    p.add_argument('--output', type=Path, default=ROOT / 'results' / f'{candidate}_ACCESS_RESULT.json')
    a = p.parse_args()
    data = json.loads(a.input.read_text())
    if data.get('candidate') != candidate:
        p.error('Candidate/input mismatch')
    result = evaluate(data, Robot())
    result['input_file_sha256'] = hashlib.sha256(a.input.read_bytes()).hexdigest()
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(result, indent=2, allow_nan=False) + '\n')
    print(json.dumps({'candidate': candidate, 'input_status': result['input_status'],
                      'access_decision': result['access_decision'], 'missing_inputs': len(result['missing_inputs']),
                      'robot_hulls_per_arm': result['robot_reference']['collision_hulls_per_arm'],
                      'output': str(a.output)}, indent=2))
    return 0 if not result['missing_inputs'] and result['access_decision'] == 'PARTIAL_GEOMETRIC_CERTIFICATE_ONLY' else 2
