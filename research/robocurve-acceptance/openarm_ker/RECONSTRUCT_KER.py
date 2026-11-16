"""Bounded, CPU-only articulated hypothesis audit; never a simulation or path test.

Native STEP millimetres. All motions are products of rotations about source
bearing axes. Joint signs and q=0 refer only to the exported CAD, not encoders.
"""
import argparse
import gzip
import hashlib
import json
from pathlib import Path

import numpy as np
from scipy.optimize import least_squares
from scipy.spatial.transform import Rotation

HERE = Path(__file__).resolve().parent
BASES = {-1: list(range(2, 114, 14)), 1: list(range(183, 295, 14))}
COVERS = {-1: [None,114,None,115,None,116,117,118],
           1: [None,179,None,180,None,181,182,508]}
# Explicit graph hypothesis. Commercial bearings are indivisible simplified
# CAD envelopes: assigned to the stator for this audit, NOT both rings rigid.
# AUU3-15 spring envelopes (134/145) are frozen at exported q8=0 solely
# for interference diagnostics, NOT claimed to be rigid link members.
MEMBERS = {-1: [[135,136,137],[123],[0,119,120,124,125],[126],
                [1,121,122,127,128],[129],[130],[131,133,134],[132]],
            1: [[],[150],[155,148,153,149,147],[138],
                [154,151,152,141,144],[142],[140],[146,139,145],[143]]}
CONNECTORS = {-1: [[135],[123],[124,125],[126],[127,128],[129],[130],[131],[132]],
               1: [[135],[150],[149,147],[138],[141,144],[142],[140],[146],[143]]}


def write(path, obj):
    path.write_text(json.dumps(obj, indent=2) + '\n')


def bounds(row):
    b = np.array([f['bounds'] for f in row['faces']])
    return b[:,:3].min(0), b[:,3:].max(0)


def axis_feature(row, radius):
    return next(f for f in row['faces'] if abs(f.get('radius',-1)-radius)<1e-6)


def line_error(p, a, q, b):
    return float(np.linalg.norm(np.cross(np.array(p)-q, a))), float(1-abs(np.dot(a,b)))


def matching_holes(a, b):
    """Coaxial mounting-hole candidates; no finite mating or preload proof."""
    found=[]
    for f in a['faces']:
        if not .74 < f.get('radius',-1) < 1.31:
            continue
        for g in b['faces']:
            if not .74 < g.get('radius',-1) < 1.31:
                continue
            dist,parallel=line_error(f['origin'],f['axis'],np.array(g['origin']),g['axis'])
            if dist>1e-5 or parallel>1e-8:
                continue
            axis=np.array(f['axis']);p=np.array(f['origin']);p-=axis*np.dot(axis,p)
            if not any(np.linalg.norm(p-np.array(h['line_point']))<1e-5 for h in found):
                found.append(dict(faces=[f['face'],g['face']],line_point=p.tolist(),
                                  radii=[f['radius'],g['radius']],distance_mm=dist))
    return found


def fk(q, centers, axes):
    T=np.eye(4);out=[T.copy()]
    for angle,p,a in zip(q,centers,axes):
        R=Rotation.from_rotvec(a*angle).as_matrix()
        E=np.eye(4);E[:3,:3]=R;E[:3,3]=p-R@p
        T=T@E;out.append(T.copy())
    return out


def graph(rows):
    output={};members={s:[x.copy() for x in m] for s,m in MEMBERS.items()}
    for side,ids in BASES.items():
        centers=[];axes=[];joints=[]
        for k,b in enumerate(ids):
            lo,hi=bounds(rows[b]);center=(lo+hi)/2
            bearing=axis_feature(rows[b],7.5);a=np.array(bearing['axis'])
            if a[np.argmax(abs(a))]<0:a=-a
            housing=axis_feature(rows[b+1],7.5);shaft=axis_feature(rows[b+2],5)
            residuals={}
            for label,feature in [('housing',housing),('shaft',shaft)]:
                residuals[label]=line_error(center,a,np.array(feature['origin']),feature['axis'])
            # The original group has bearing, housing, horn, ten screws, spacer.
            # Do NOT silently fix all ten screws to the same side of the joint.
            members[side][k]+=[b,b+1,b+13]
            members[side][k+1]+=[b+2]
            if COVERS[side][k] is not None:members[side][k].append(COVERS[side][k])
            horn_connections=[];housing_connections=[]
            for i in CONNECTORS[side][k+1]:
                h=matching_holes(rows[b+2],rows[i])
                if h:horn_connections.append(dict(index=i,holes=h))
            for i in CONNECTORS[side][k]:
                h=matching_holes(rows[b+1],rows[i])
                if h:housing_connections.append(dict(index=i,holes=h))
            joints.append(dict(joint=k+1,bearing=b,housing=b+1,horn=b+2,
                bearing_envelope_midpoint_mm=center.tolist(),axis=a.tolist(),
                coaxial_errors=residuals,housing_mount=housing_connections,
                horn_mount=horn_connections,status='SOURCE-SUPPORTED HYPOTHESIS',
                limits='UNKNOWN',bearing_internal_rings='not separated in released CAD'))
            centers.append(center);axes.append(a)
        output[str(side)]=dict(joints=joints,centers=np.array(centers).tolist(),axes=np.array(axes).tolist())
    return output,members


def register(g, starts):
    results=[]
    targets={-1:np.array([-77.365220892,-110,48.3]),1:np.array([68.079022274,-110,-6.7])}
    for side in [-1,1]:
        p=np.array(g[str(side)]['centers']);axes=np.array(g[str(side)]['axes'])
        q1=0 if side==-1 else -np.arcsin(5/14)
        # Source ENC_HOUSING radial M2 drill pair, on the unused Z=-63 flat.
        point=np.array([side*100.05,-373.2,-63])
        for crossed in [False,True]:
            target=targets[-side if crossed else side]
            for sign in [-1,1]:
                Rtar=np.column_stack([[0,0,sign],[sign,0,0],[0,1,0]])
                def residual(x):
                    T=fk([q1,0,*x,0],p,axes)[7];R=T[:3,:3]
                    return np.r_[R@point+T[:3,3]-target,
                        50*Rotation.from_matrix(Rtar.T@R).as_rotvec()]
                solutions=[]
                for seed in range(starts):
                    x=np.random.default_rng(seed).uniform(-np.pi,np.pi,5)
                    r=least_squares(residual,x,max_nfev=180,ftol=1e-11,xtol=1e-11,gtol=1e-10)
                    q=np.r_[q1,0,(r.x+np.pi)%(2*np.pi)-np.pi,0]
                    if any(np.linalg.norm(q-np.array(s['q_rad']))<1e-4 for s in solutions):continue
                    T=fk(q,p,axes)[7];e=residual(q[2:7])
                    # An independent scalar reach invariant: distance from
                    # elbow-axis intersection to wrist-axis intersection.
                    wrist=np.array([side*106.75,-305.2,0.])
                    elbow=np.array([side*106.75,-154,0.])
                    T2=fk(q,p,axes)[2];elbow_target=T2[:3,:3]@elbow+T2[:3,3]
                    required_wrist=target+Rtar@(wrist-point)
                    invariant=float(np.linalg.norm(required_wrist-elbow_target)-151.2)
                    pipe=np.array([side*106.75,-66.,0.])
                    pdir=T2[:3,:3]@np.array([0,1.,0]);pos=T2[:3,:3]@pipe+T2[:3,3]
                    seat=np.array([0,1.,0]) if side==-1 else np.array([0,np.sqrt(171)/14,-5/14])
                    seat_origin=np.array([side*106.75,0,0])
                    pipe_err=line_error(pos,pdir,seat_origin,seat)
                    hole_errors=[]
                    for offset in [-3,3]:
                        h=point+np.array([0,offset,0])
                        expected=target+Rtar@np.array([0,offset,0])
                        actual=T[:3,:3]@h+T[:3,3]
                        hole_errors.append(dict(point_mm=actual.tolist(),target_mm=expected.tolist(),
                                               line_error_mm=float(np.linalg.norm((actual-expected)[[0,2]]))))
                    solutions.append(dict(q_rad=q.tolist(),q_deg=np.rad2deg(q).tolist(),
                        position_error_mm=float(np.linalg.norm(e[:3])),
                        orientation_error_deg=float(np.linalg.norm(e[3:])/50*180/np.pi),
                        reach_invariant_error_mm=invariant,pipe_line_errors=pipe_err,
                        screw_axis_points=hole_errors,T7=T.tolist(),
                        q8='0 is exported pose ONLY; spring/stop angle unverified'))
                solutions.sort(key=lambda s:s['position_error_mm']+s['orientation_error_deg'])
                results.append(dict(side=side,crossed=crossed,sign=sign,solutions=solutions))
    return results


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-dir',type=Path)
    parser.add_argument('--features',type=Path,default=HERE/'results/occurrence_features.json.gz')
    parser.add_argument('--extract',action='store_true')
    parser.add_argument('--starts',type=int,default=12)
    parser.add_argument('--output-dir',type=Path,required=True)
    args=parser.parse_args();args.output_dir.mkdir(parents=True,exist_ok=True)
    if args.extract:
        if args.source_dir is None:parser.error('--extract requires --source-dir')
        from KER_CAD import load,features
        shapes=load(args.source_dir,'OpenArm KER.STEP')
        rows=[dict(index=r['index'],name=r['name'],path=r['path'],faces=features(r['shape'])) for r in shapes]
        args.features.parent.mkdir(parents=True,exist_ok=True)
        with gzip.open(args.features,'wt') as f:json.dump(rows,f)
    else:
        rows=json.load(gzip.open(args.features))
    assert len(rows)==509 and all(r['index']==i for i,r in enumerate(rows))
    g,members=graph(rows)
    write(args.output_dir/'ARTICULATED_AXES.json',g)
    known={i:(side,k) for side,links in members.items() for k,ids in enumerate(links) for i in ids}
    assignment=[dict(index=r['index'],name=r['name'],assignment=known.get(r['index'],'UNKNOWN'),
                     status='SOURCE-SUPPORTED HYPOTHESIS' if r['index'] in known else 'UNKNOWN',
                     representation=('frozen spring collision envelope; NOT a rigid link member' if r['index'] in [134,145] else 'simplified bearing envelope on stator; internal rings unmodeled' if r['index'] in sum(BASES.values(),[]) else 'structural assignment hypothesis' if r['index'] in known else 'unassigned')) for r in rows]
    write(args.output_dir/'OCCURRENCE_LINK_ASSIGNMENT.json',assignment)
    fits=register(g,args.starts);write(args.output_dir/'ARTICULATED_REGISTRATION.json',fits)
    write(args.output_dir/'RECONSTRUCTION_RUN.json',dict(features_sha256=hashlib.sha256(args.features.read_bytes()).hexdigest(),
        starts_per_case=args.starts,occurrences=len(rows),structural_assignment_count=len(known),
        unknown_assignment_count=len(rows)-len(known),root_transform=np.eye(4).tolist(),
        hypotheses=['source housing radial pair and Z=-63 flat are jig J8 interface',
                    'root identity is constrained by source rear face, lock ledge and P1 seats',
                    'q2=0 pipe orientation branch; opposite pipe branch not exhaustively searched',
                    'no physical joint limits assumed; coordinate angles wrapped to [-pi,pi]',
                    'q8 exported zero, spring/stop response UNKNOWN'],
        collision_scope='explicit structural bodies only; NOT all509 or full carried assembly'))
    for f in fits:
        s=f['solutions'][0]
        print(f['side'],f['crossed'],f['sign'],s['position_error_mm'],s['orientation_error_deg'])

if __name__=='__main__':main()
