"""Conservative collision bounds for QA, never a replacement physics engine."""
import itertools
import math
from .scoring import add, sub, rotate, multiply


def box(body, shape):
    q = multiply(body['quat'], shape.get('quat', [0, 0, 0, 1]))
    centre = add(body['pos'], rotate(body['quat'], shape['pos']))
    half = ([v/2 for v in shape['size']] if shape['kind'] == 'box'
            else [shape['radius'], shape['radius'], shape['height']/2])
    axes = [rotate(q, axis) for axis in [(1, 0, 0), (0, 1, 0), (0, 0, 1)]]
    return centre, half, axes


def penetration(a, b):
    """OBB separating-axis test; cylinder bounding boxes are conservative."""
    c, h, A = a
    d, k, B = b
    delta = sub(d, c)
    axes = A+B
    for u, v in itertools.product(A, B):
        cross = (u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0])
        size = math.sqrt(sum(x*x for x in cross))
        if size > 1e-8:
            axes.append(tuple(x/size for x in cross))
    overlap = math.inf
    for axis in axes:
        ra = sum(hi*abs(sum(x*y for x, y in zip(ai, axis))) for hi, ai in zip(h, A))
        rb = sum(hi*abs(sum(x*y for x, y in zip(ai, axis))) for hi, ai in zip(k, B))
        gap = ra+rb-abs(sum(x*y for x, y in zip(delta, axis)))
        if gap <= 0:
            return 0.0
        overlap = min(overlap, gap)
    return overlap


def maximum_penetration(spec, bodies):
    body_specs = {b['name']: b for a in spec['assemblies'] for b in a['bodies']}
    excluded = {frozenset((j['parent'], j['child'])) for a in spec['assemblies'] for j in a.get('joints', [])}
    excluded.update(frozenset(p) for p in spec.get('collision_exclusions', []))
    maximum = 0.0
    bounds = {}
    for name, bs in body_specs.items():
        bounds[name] = [box(bodies[name], s) for s in bs['shapes'] if s.get('collision', True)]
    for left, right in itertools.combinations(body_specs, 2):
        if frozenset((left, right)) in excluded:
            continue
        l, r = body_specs[left], body_specs[right]
        if l.get('anchor') and r.get('anchor'):
            continue
        # Rotation-independent broad phase, followed by actual primitive bounds.
        radius = math.sqrt(sum(x*x for x in l['half_extent'])) + math.sqrt(sum(x*x for x in r['half_extent']))
        if sum(x*x for x in sub(bodies[left]['pos'], bodies[right]['pos'])) > radius*radius:
            continue
        for a, b in itertools.product(bounds[left], bounds[right]):
            maximum = max(maximum, penetration(a, b))
    return maximum
