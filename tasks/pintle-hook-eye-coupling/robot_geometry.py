"""Offline collision inspection using the official YAM URDF convex pieces.

No simulator is loaded. These checks inspect nominal kinematic poses and cannot
certify contact forces, grasps, actuator tracking, or dynamic collision avoidance.
"""
from functools import lru_cache
from pathlib import Path
import struct
import xml.etree.ElementTree as ET
import numpy as np
from yam_arena import YAM_URDF,station
from yam_arena.constants import ARM_JOINTS,FINGER_JOINTS,FINGER_OPEN
from yam_arena.urdf import forward_kinematics,rpy_matrix


def directions(values):
    lengths=np.linalg.norm(values,axis=1);values=values[lengths>1e-10]/lengths[lengths>1e-10,None]
    largest=np.argmax(np.abs(values),axis=1);sign=np.sign(values[np.arange(len(values)),largest]);values*=sign[:,None]
    return np.unique(np.round(values,7),axis=0)


def stl_triangles(path):
    data=Path(path).read_bytes()
    count=struct.unpack_from('<I',data,80)[0] if len(data)>=84 else -1
    if len(data)==84+50*count:
        dtype=np.dtype([('normal','<f4',(3,)),('vertices','<f4',(3,3)),('attribute','<u2')])
        return np.frombuffer(data,dtype=dtype,count=count,offset=84)['vertices'].astype(float)
    points=[]
    for line in data.decode('ascii').splitlines():
        words=line.split()
        if words and words[0]=='vertex':points.append([float(v) for v in words[1:]])
    return np.asarray(points).reshape(-1,3,3)


def convex_collision_mesh(triangles):
    """Same convex point set, without internal/concave STL tessellation edges.

    SAT already treats each URDF piece as a convex vertex cloud. Computing its
    hull changes neither that set nor its support function. Qhull errors fail
    closed; no jitter, bounding-box substitution or mesh decimation is used.
    """
    from scipy.spatial import ConvexHull
    points=np.unique(np.round(np.asarray(triangles).reshape(-1,3),9),axis=0)
    hull=ConvexHull(points);faces=points[hull.simplices]
    edges=np.concatenate([faces[:,1]-faces[:,0],faces[:,2]-faces[:,1],faces[:,0]-faces[:,2]])
    vertices=points[hull.vertices]
    if np.max(points@hull.equations[:,:3].T+hull.equations[:,3])>2e-8:
        raise ValueError('Hull does not contain original collision vertices')
    # FCL needs outward face winding and compact vertex indices.
    import fcl
    remap={int(old):new for new,old in enumerate(hull.vertices)};encoded=[]
    for simplex,plane in zip(hull.simplices,hull.equations):
        face=list(map(int,simplex));v=points[face]
        if np.dot(np.cross(v[1]-v[0],v[2]-v[0]),plane[:3])<0:face[1],face[2]=face[2],face[1]
        encoded.extend([3,*[remap[i] for i in face]])
    return dict(vertices=vertices,normals=directions(hull.equations[:,:3]),edges=directions(edges),fcl_geometry=fcl.Convex(vertices,len(hull.simplices),encoded))


@lru_cache(maxsize=1)
def local_hulls():
    rows=[]
    for link in ET.parse(YAM_URDF).getroot().findall('link'):
        for i,collision in enumerate(link.findall('collision')):
            origin=collision.find('origin');xyz=np.zeros(3);rpy=np.zeros(3)
            if origin is not None:
                xyz=np.array([float(v) for v in origin.get('xyz','0 0 0').split()])
                rpy=np.array([float(v) for v in origin.get('rpy','0 0 0').split()])
            mesh=collision.find('geometry/mesh')
            if mesh is None:raise ValueError('Unexpected non-mesh YAM collider; review pinned URDF')
            path=(YAM_URDF.parent/mesh.get('filename')).resolve()
            scale=np.array([float(v) for v in mesh.get('scale','1 1 1').split()])
            triangles=(stl_triangles(path)*scale)@rpy_matrix(rpy).T+xyz
            rows.append(dict(link=link.get('name'),piece=i,**convex_collision_mesh(triangles)))
    if not rows:raise ValueError('Pinned URDF has no collision geometry')
    return rows


def arm_hulls(side,joints):
    import fcl
    joints=np.asarray(joints);configuration={name:float(value) for name,value in zip(ARM_JOINTS,joints[:6])}
    configuration.update({name:float(joints[6]*FINGER_OPEN) for name in FINGER_JOINTS})
    poses=forward_kinematics(YAM_URDF,configuration);base=np.array(station.BASES[side]);rows=[]
    for hull in local_hulls():
        pose=poses[hull['link']];r=pose[:3,:3];p=pose[:3,3]+base
        vertices=hull['vertices']@r.T+p
        rows.append(dict(link=hull['link'],piece=hull['piece'],polyhedron=(vertices,hull['normals']@r.T,hull['edges']@r.T),
                         fcl_object=fcl.CollisionObject(hull['fcl_geometry'],fcl.Transform(r,p)),lower=vertices.min(axis=0),upper=vertices.max(axis=0)))
    return rows


def task_collisions(geometry,hulls,spec,states,threshold=.002):
    compiled=geometry.compiled_shapes(spec);boxes,bounds=geometry.world_boxes(compiled,states)
    rows=[];cache={}
    for body,shapes in compiled['shapes'].items():
        lo,hi=bounds[body]
        for hull in hulls:
            indices=np.flatnonzero(np.all(hi>hull['lower'],axis=1)&np.all(lo<hull['upper'],axis=1))
            for i in indices:
                key=(body,int(i))
                if key not in cache:cache[key]=geometry.polyhedron(states[body],shapes[i])
                depth=max(0.,-geometry.convex_separation(hull['polyhedron'],cache[key],stop_at=-threshold))
                if depth>threshold:rows.append(dict(link=hull['link'],piece=hull['piece'],body=body,shape=int(i),penetration_m=depth))
    return sorted(rows,key=lambda row:-row['penetration_m'])


def table_intersections(hulls,top,threshold=.001):
    return [dict(link=h['link'],piece=h['piece'],depth_m=top-float(h['lower'][2])) for h in hulls if h['lower'][2]<top-threshold]


def inter_arm_intersections(geometry,left,right,threshold=.002):
    lower=np.array([h['lower'] for h in right]);upper=np.array([h['upper'] for h in right]);rows=[]
    for a in left:
        candidates=np.flatnonzero(np.all(upper>a['lower']+threshold,axis=1)&np.all(lower<a['upper']-threshold,axis=1))
        for i in candidates:
            b=right[i];depth=fcl_depth(a['fcl_object'],b['fcl_object'],geometry,(a['polyhedron'],b['polyhedron']))
            if depth>threshold:rows.append(dict(left=a['link'],right=b['link'],depth_m=depth))
    return rows


def fcl_depth(a,b,geometry=None,polyhedra=None):
    """CPU libFCL convex GJK/EPA, cross-checked against complete SAT in tests."""
    import fcl
    # libccd EPA can return an arbitrary separating direction for exactly
    # coincident convex transforms. Preserve complete SAT for that degeneracy.
    if polyhedra is not None and np.linalg.norm(a.getTranslation()-b.getTranslation())<1e-6:
        return max(0.,-geometry.convex_separation(*polyhedra,stop_at=float('inf')))
    result=fcl.CollisionResult();fcl.collide(a,b,fcl.CollisionRequest(enable_contact=True,num_max_contacts=1),result)
    if not result.is_collision:return 0.
    if not result.contacts:raise ValueError('FCL collision has no penetration result')
    depths=[float(c.penetration_depth) for c in result.contacts]
    if not np.isfinite(depths).all() or min(depths)<-1e-7:raise ValueError('Invalid FCL penetration result')
    return max(0.,max(depths))
