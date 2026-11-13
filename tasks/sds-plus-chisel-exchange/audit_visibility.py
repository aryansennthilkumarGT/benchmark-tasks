"""CPU geometric macro-view access through physical inspection inserts.

This checks geometry/transparency declarations, not actual rendering or optics.
All transparent components remain physical colliders; the locking roof is opaque.
"""
import copy,json,math
from pathlib import Path
import numpy as np
from scipy.spatial import ConvexHull
from audit_geometry import geometry_module
from kinematics import reconstruct
HERE=Path(__file__).resolve().parent

def ray_segment(g,body,shape,start,end):
 center,half,axes=g.box(body,shape);a=axes@(np.asarray(start)-center);b=axes@(np.asarray(end)-center);delta=b-a
 if shape['kind']=='sphere':return False
 if shape['kind']=='box':normals=np.concatenate([np.eye(3),-np.eye(3)]);offset=-np.r_[half,half]
 else:
  vertices=g.polyhedron(dict(pos=[0.,0.,0.],quat=[0.,0.,0.,1.]),dict(shape,pos=[0.,0.,0.],quat=[0.,0.,0.,1.]))[0];h=ConvexHull(vertices);normals=h.equations[:,:3];offset=h.equations[:,3]
 lower,upper=0.,1.
 for n,d in zip(normals,offset):
  p=float(n@a+d);v=float(n@delta)
  if abs(v)<1e-12:
   if p>1e-10:return False
  elif v>0:upper=min(upper,-p/v)
  else:lower=max(lower,-p/v)
 return lower<=upper and upper>=0 and lower<=1

def audit(folder=HERE):
 s=json.loads((folder/'scene.json').read_text());g=geometry_module(folder);bs={b['name']:b for a in s['assemblies'] for b in a['bodies']};root=bs['tool_holder'];rows=[]
 for q,x in [(0.,.020),(.008,.020),(0.,.0245)]:
  poses={n:copy.deepcopy(b) for n,b in bs.items()};poses.update(reconstruct(s,root,{'sleeve_retraction':q}));point=np.asarray(root['pos'])+[x,0,.008];camera=point+[0,.10,0];blocked=[];clear=[]
  for n,definition in bs.items():
   if n=='locking_ball':continue
   for i,shape in enumerate(definition['shapes']):
    if not ray_segment(g,poses[n],shape,camera,point):continue
    row=dict(body=n,shape=i,opacity=shape.get('opacity',1.))
    (clear if shape.get('opacity',1.)<.2 else blocked).append(row)
  rows.append(dict(sleeve_retraction=q,ball_race_x=x,opaque_blockers=blocked,physical_clear_insert_hits=clear,passed=not blocked and bool(clear)))
 return dict(kind='OFFLINE_MACRO_VIEW_RAY_GEOMETRY_ONLY',native_rendering_executed=False,hardware_optics_verified=False,checks=rows,passed=all(r['passed'] for r in rows))
if __name__=='__main__':r=audit();print(json.dumps(r,indent=2));raise SystemExit(0 if r['passed'] else 1)
