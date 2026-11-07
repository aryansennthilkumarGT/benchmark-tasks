"""Conservative geometric QA, never a replacement physics engine.

Primitive AABBs reject distant shape pairs before separating-axis tests. Cylinders
use circumscribed 32-sided prisms for narrow-phase checks (radial excess below
0.5 percent). Native contacts remain authoritative for physical feasibility.
"""
import itertools
import numpy as np
from .scoring import add,sub,rotate,multiply

_compiled={}


def compiled_shapes(spec):
    key=id(spec)
    if key in _compiled and _compiled[key]['spec'] is spec:return _compiled[key]
    definitions={b['name']:b for a in spec['assemblies'] for b in a['bodies'] if any(s.get('collision',True) for s in b['shapes'])}
    shapes={n:[s for s in b['shapes'] if s.get('collision',True)] for n,b in definitions.items()}
    local={}
    for name,items in shapes.items():
        values=[box({'pos':[0,0,0],'quat':[0,0,0,1]},s) for s in items]
        local[name]=tuple(np.asarray([v[i] for v in values]) for i in range(3))
    excluded={frozenset((j['parent'],j['child'])) for a in spec['assemblies'] for j in a.get('joints',[])}
    excluded.update(frozenset(p) for p in spec.get('collision_exclusions',[]))
    result=dict(spec=spec,definitions=definitions,shapes=shapes,local=local,excluded=excluded,world={})
    _compiled[key]=result;return result


def world_boxes(compiled,bodies):
    boxes={};bounds={}
    for name,(centres,half,axes) in compiled['local'].items():
        body=bodies[name];key=(*body['pos'],*body['quat']);cached=compiled['world'].get(name)
        if cached is None or cached[0]!=key:
            rotation=np.array([rotate(body['quat'],a) for a in [(1,0,0),(0,1,0),(0,0,1)]])
            world_centres=centres@rotation+body['pos'];world_axes=axes@rotation
            extent=np.einsum('nj,njk->nk',half,np.abs(world_axes))
            cached=(key,list(zip(world_centres,half,world_axes)),(world_centres-extent,world_centres+extent))
            compiled['world'][name]=cached
        boxes[name]=cached[1];bounds[name]=cached[2]
    return boxes,bounds


def box(body,shape):
    q=multiply(body['quat'],shape.get('quat',[0,0,0,1]))
    centre=add(body['pos'],rotate(body['quat'],shape['pos']))
    half=([v/2 for v in shape['size']] if shape['kind']=='box' else [shape['radius'],shape['radius'],shape['height']/2])
    axes=[rotate(q,axis) for axis in [(1,0,0),(0,1,0),(0,0,1)]]
    return np.asarray(centre),np.asarray(half),np.asarray(axes)


def separation(a,b):
    """Signed SAT gap. Positive is a conservative separation, negative penetration."""
    c,h,A=map(np.asarray,a);d,k,B=map(np.asarray,b)
    cross=np.cross(A[:,None,:],B[None,:,:]).reshape(-1,3)
    lengths=np.linalg.norm(cross,axis=1);cross=cross[lengths>1e-8]/lengths[lengths>1e-8,None]
    axes=np.concatenate((A,B,cross))
    radius_a=(np.abs(axes@A.T)*h).sum(axis=1);radius_b=(np.abs(axes@B.T)*k).sum(axis=1)
    return float(np.max(np.abs(axes@(d-c))-radius_a-radius_b))


def penetration(a,b):return max(0.,-separation(a,b))


def polyhedron(body,shape):
    centre,half,axes=box(body,shape)
    if shape['kind']=='box':
        vertices=np.array(list(itertools.product(*[(-v,v) for v in half])))@axes+centre
        return vertices,axes,axes
    angles=np.arange(32)*2*np.pi/32
    radius=shape['radius']/np.cos(np.pi/32)
    ring=np.column_stack((radius*np.cos(angles),radius*np.sin(angles)))
    vertices=np.concatenate([np.column_stack((ring,np.full(32,z))) for z in (-half[2],half[2])])@axes+centre
    midpoint=angles+np.pi/32
    normals=np.vstack((np.column_stack((np.cos(midpoint),np.sin(midpoint),np.zeros(32))),[0,0,1]))@axes
    edges=np.vstack((np.column_stack((-np.sin(midpoint),np.cos(midpoint),np.zeros(32))),[0,0,1]))@axes
    return vertices,normals,edges


def convex_separation(a,b,stop_at=0.):
    vertices_a,normals_a,edges_a=a;vertices_b,normals_b,edges_b=b
    maximum=-float('inf')
    def project(axes):
        best=-float('inf')
        for start in range(0,len(axes),128):
            chunk=axes[start:start+128];pa=vertices_a@chunk.T;pb=vertices_b@chunk.T
            best=max(best,float(np.max(np.maximum(pb.min(axis=0)-pa.max(axis=0),pa.min(axis=0)-pb.max(axis=0)))))
            if best>=stop_at:break
        return best
    # Face normals often prove separation before any edge pairs are needed.
    maximum=max(maximum,project(np.concatenate((normals_a,normals_b))))
    if maximum>=stop_at:return maximum
    for start in range(0,len(edges_a),8):
        cross=np.cross(edges_a[start:start+8,None,:],edges_b[None,:,:]).reshape(-1,3)
        lengths=np.linalg.norm(cross,axis=1);cross=cross[lengths>1e-8]/lengths[lengths>1e-8,None]
        if len(cross):maximum=max(maximum,project(cross))
        if maximum>=stop_at:return maximum
    return maximum


def shape_bounds(boxes):
    if not boxes:return np.empty((0,3)),np.empty((0,3))
    centres=np.array([b[0] for b in boxes]);sizes=np.array([np.asarray(b[1])@np.abs(b[2]) for b in boxes])
    return centres-sizes,centres+sizes


def maximum_penetration(spec,bodies):
    compiled=compiled_shapes(spec);definitions=compiled['definitions'];excluded=compiled['excluded'];shapes=compiled['shapes']
    boxes,bounds=world_boxes(compiled,bodies)
    polygons={}
    def polygon(name,index):
        key=(name,index)
        if key not in polygons:polygons[key]=polyhedron(bodies[name],shapes[name][index])
        return polygons[key]
    maximum=0.
    names=list(definitions)
    if len(names)<2:return maximum
    body_lower=np.array([bounds[n][0].min(axis=0) for n in names]);body_upper=np.array([bounds[n][1].max(axis=0) for n in names])
    overlaps=np.triu(np.all(body_upper[:,None,:]>body_lower[None,:,:],axis=2)&
                     np.all(body_lower[:,None,:]<body_upper[None,:,:],axis=2),1)
    for left_index,right_index in zip(*np.nonzero(overlaps)):
        left,right=names[left_index],names[right_index]
        if frozenset((left,right)) in excluded:continue
        if definitions[left].get('anchor') and definitions[right].get('anchor'):continue
        lmin,lmax=bounds[left];rmin,rmax=bounds[right]
        if len(lmin)==0 or len(rmin)==0:continue
        if np.any(lmax.max(axis=0)<=rmin.min(axis=0)) or np.any(rmax.max(axis=0)<=lmin.min(axis=0)):continue
        left_candidates=np.flatnonzero(np.all(lmax>body_lower[right_index],axis=1)&np.all(lmin<body_upper[right_index],axis=1))
        pair_mask=(np.all(rmax[None,:,:]>lmin[left_candidates,None,:],axis=2)&
                   np.all(rmin[None,:,:]<lmax[left_candidates,None,:],axis=2))
        for row,j in zip(*np.nonzero(pair_mask)):
            index=left_candidates[row];depth=penetration(boxes[left][index],boxes[right][j])
            if depth<=maximum:continue
            if shapes[left][index]['kind']=='cylinder' or shapes[right][j]['kind']=='cylinder':
                depth=max(0.,-convex_separation(polygon(left,index),polygon(right,j)))
            maximum=max(maximum,depth)
    return maximum


def robot_clearance(robot_boxes,spec,bodies):
    candidates=[box(bodies[b['name']],s) for a in spec['assemblies'] for b in a['bodies']
                if not b.get('anchor') for s in b['shapes'] if s.get('collision',True)]
    if not robot_boxes or not candidates:raise ValueError('Cannot measure robot release clearance')
    # Clearance is capped at 25 mm because the scorer only needs proof of 20 mm.
    # Distant pairs use a world-axis lower bound; only nearby pairs need SAT.
    lower,upper=shape_bounds(candidates);clearance=.025
    for robot in robot_boxes:
        lo,hi=shape_bounds([robot]);gap=np.maximum(lower-hi[0],lo[0]-upper).max(axis=1)
        for index in np.flatnonzero(gap<clearance):
            clearance=min(clearance,separation(robot,candidates[index]))
    return clearance


def intersection_details(spec,bodies,threshold=.002):
    """Slow diagnostic used only for the first failing offline sample."""
    definitions={b['name']:b for a in spec['assemblies'] for b in a['bodies']}
    excluded={frozenset((j['parent'],j['child'])) for a in spec['assemblies'] for j in a.get('joints',[])}
    excluded.update(frozenset(p) for p in spec.get('collision_exclusions',[]))
    rows=[]
    for left,right in itertools.combinations(definitions,2):
        if frozenset((left,right)) in excluded:continue
        if definitions[left].get('anchor') and definitions[right].get('anchor'):continue
        for i,a in enumerate(definitions[left]['shapes']):
            if not a.get('collision',True):continue
            for j,b in enumerate(definitions[right]['shapes']):
                if not b.get('collision',True):continue
                depth=penetration(box(bodies[left],a),box(bodies[right],b))
                if depth>threshold and (a['kind']=='cylinder' or b['kind']=='cylinder'):
                    depth=max(0.,-convex_separation(polyhedron(bodies[left],a),polyhedron(bodies[right],b)))
                if depth>threshold:rows.append(dict(left=left,right=right,left_shape=i,right_shape=j,penetration_m=depth))
    return sorted(rows,key=lambda row:-row['penetration_m'])[:12]
