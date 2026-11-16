"""Bounded source-BRep audit of two candidate articulated configurations.
Not all509 bodies, not exhaustive IK branches, not a path/load test.
"""
import sys,json,numpy as np,multiprocessing as mp,time,argparse,itertools
from pathlib import Path
HERE=Path(__file__).resolve().parent
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--source-dir',type=Path,required=True)
parser.add_argument('--results',type=Path,default=HERE/'results/articulation')
parser.add_argument('--max-pairs',type=int,default=80)
parser.add_argument('--timeout',type=float,default=3)
parser.add_argument('--adjacent-only',action='store_true')
args=parser.parse_args()
import RECONSTRUCT_KER as rec
from KER_CAD import load
from OCP.gp import gp_Trsf
import cadquery as cq
out=args.results;g=json.load(open(out/'ARTICULATED_AXES.json'));fits=json.load(open(out/'ARTICULATED_REGISTRATION.json'));features=json.load(__import__('gzip').open(HERE/'results/occurrence_features.json.gz'));_,M=rec.graph(features)
S=load(args.source_dir,'OpenArm KER.STEP');J=load(args.source_dir,'OpenArm KER JIG BASE.STEP')[0]['shape'];print('loaded',flush=True)
context=mp.get_context('fork')
# Conservative transformed source AABBs, not repeated expensive BRep meshing.
jf=json.load(__import__('gzip').open(HERE/'results/jig_faces.json.gz'))
jb=np.array([f['bounds_mm'] for f in jf]);jbox=(jb[:,:3].min(0),jb[:,3:].max(0))
boxes={}
def measure(a,b,timeout=args.timeout):
 parent,child=context.Pipe(False)
 def calc():
  try:child.send(dict(volume_mm3=a.intersect(b).Volume()))
  except Exception as e:child.send(dict(error=type(e).__name__+': '+str(e)))
 proc=context.Process(target=calc);proc.start()
 if parent.poll(timeout):r=parent.recv();proc.join();return r
 proc.terminate();proc.join();return dict(timeout_seconds=timeout)
def bboxoverlap(a,b):
 return bool(np.all(a[0]<b[1]-1e-7) and np.all(b[0]<a[1]-1e-7))
results=[];selected={};allbodies=[]
for side in [-1,1]:
 f=next(f for f in fits if f['side']==side and f['crossed'] and f['sign']==side)
 # smallest total absolute angle branch, no claim these are physical limits
 sol=min(f['solutions'],key=lambda s:sum(abs(x) for x in s['q_rad']));selected[side]=sol
 ts=rec.fk(sol['q_rad'],np.array(g[str(side)]['centers']),np.array(g[str(side)]['axes']));bodies=[]
 for link,ids in enumerate(M[side]):
  for i in ids:
   lo,hi=rec.bounds(features[i]);corners=np.array(list(itertools.product(*zip(lo,hi))))
   v=corners@ts[link][:3,:3].T+ts[link][:3,3];boxes[i]=(v.min(0),v.max(0))
   tr=gp_Trsf();tr.SetValues(*ts[link][:3].flatten().tolist());a=S[i]['shape'].moved(cq.Location(tr));bodies.append((i,side,link,a))
 allbodies+=bodies
 for i,side,link,a in bodies:
  if not args.adjacent_only and bboxoverlap(boxes[i],jbox):
   r=measure(a,J);results.append(dict(kind='jig',i=i,side=side,link=link,**r));rec.write(out/('ADJACENT_INTERFERENCE.json' if args.adjacent_only else 'BOUNDED_INTERFERENCE.json'),results)
 print('jig',side,flush=True)
# Cross-arm and nonadjacent links first; actual subset, neither all-parts nor exhaustive branch audit.
pairs=[]
for n,(i,side,l,a) in enumerate(allbodies):
 for j,s2,k,b in allbodies[n+1:]:
  eligible=(side==s2 and abs(l-k)==1) if args.adjacent_only else (side!=s2 or abs(l-k)>1)
  if not eligible or not bboxoverlap(boxes[i],boxes[j]):continue
  pairs.append((i,j,side,s2,l,k,a,b))
pairs.sort(key=lambda r:(r[2]==r[3],-abs(r[4]-r[5])))
print('adjacent candidate pairs' if args.adjacent_only else 'nonadjacent candidate pairs',len(pairs),flush=True)
for n,(i,j,side,s2,l,k,a,b) in enumerate(pairs[:args.max_pairs]):
 r=measure(a,b);baseline=measure(S[i]['shape'],S[j]['shape']) if r.get('volume_mm3',0)>1e-4 else None
 results.append(dict(kind='cross_link',i=i,j=j,sides=[side,s2],links=[l,k],baseline=baseline,**r));rec.write(out/('ADJACENT_INTERFERENCE.json' if args.adjacent_only else 'BOUNDED_INTERFERENCE.json'),results)
 print('pair',n,i,j,r,flush=True)
# Body datums evaluated independently on source shapes, no inferred flex/retention.
contact=[]
for part,face,jface in [(135,100,45),(136,45,42)]:
 a=S[part]['shape'].Faces()[face];b=J.Faces()[jface]
 contact.append(dict(part=part,face=face,jig_face=jface,distance_mm=a.distance(b),shared_area_mm2=a.intersect(b).Area()))
rec.write(out/'REGISTERED_BODY_CONTACTS.json',contact)
rec.write(out/('ADJACENT_AUDIT_RUN.json' if args.adjacent_only else 'BOUNDED_AUDIT_RUN.json'),dict(selected=selected,candidate_pairs=len(pairs),audited_pairs=min(len(pairs),args.max_pairs),adjacent_only=args.adjacent_only,per_boolean_timeout_seconds=args.timeout,adjacent_link_collisions='bounded adjacent audit' if args.adjacent_only else 'separate ADJACENT_AUDIT_RUN.json',unassigned_occurrences=396,all509_validation=False))
print('finished',flush=True)
