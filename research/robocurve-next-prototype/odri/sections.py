"""Actual CAD section geometry in registered source foot-centre frame, millimetres."""
from pathlib import Path
import sys,json
sys.path.insert(0,'/workspace/robocurve-cpu-deps')
import numpy as np,trimesh
import cadquery as cq
from shapely.geometry import Polygon
from shapely.ops import unary_union
from functools import lru_cache
D=Path(__file__).resolve().parent
S=D.parent/'sources/odri/step_files'

@lru_cache(maxsize=None)
def source_mesh(name):
 shape=cq.importers.importStep(str(S/(Path(name).stem+'.STEP'))).val()
 v,f=shape.tessellate(.015,.05)
 m=trimesh.Trimesh(vertices=np.array([p.toTuple() for p in v]),faces=f,process=True)
 if name=='foot_structure.STL':
  # Actual pin axis +Y must point up the source leg +Z; preserve X optical axis.
  v=m.vertices.copy();m.vertices[:,1]=-v[:,2];m.vertices[:,2]=v[:,1]
 else:m.vertices[:,2]+=160
 return m

def section(name,x):
 m=source_mesh(name)
 sec=m.section(plane_origin=[x,0,0],plane_normal=[1,0,0])
 if sec is None:return Polygon()
 loops=[Polygon(v[:,1:3]) for v in sec.discrete if len(v)>3 and np.isfinite(v).all()]
 # XOR nesting preserves through holes and does not fill the original cavities.
 p=Polygon()
 for q in loops:
  if q.area<1e-8:continue
  if not q.is_valid:raise ValueError(f"Invalid source contour at {name} X={x}; do not fill or silently repair")
  p=p.symmetric_difference(q)
 return p

if __name__=='__main__':
 import matplotlib;matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 from shapely.geometry import mapping
 fig,axs=plt.subplots(2,4,figsize=(16,8));rows=[]
 for ax,x in zip(axs.ravel(),[-5.123,-4.123,-3.123,-2.123,1.123,2.123,3.123,5.123]):
  try:
   a=section('foot_structure.STL',x);b=section('lower_leg_structure_base.STL',x);c=section('lower_leg_structure_fork.STL',x)
  except ValueError as error:
   ax.set_title(str(error)[-65:]);rows.append(dict(x_mm=x,error=str(error)));continue
  for p,color in [(a,'red'),(b,'blue'),(c,'green')]:
   geoms=p.geoms if hasattr(p,'geoms') else [p]
   for q in geoms:
    if q.is_empty:continue
    ax.fill(*q.exterior.xy,alpha=.35,color=color)
    for hole in q.interiors:ax.fill(*hole.xy,color='white')
  ax.set_xlim(-16,16);ax.set_ylim(-16,16);ax.set_aspect('equal');ax.set_title(f'X={x}mm overlap={a.intersection(b.union(c)).area:.5f}')
  rows.append(dict(x_mm=x,foot=mapping(a),fixed=mapping(b.union(c)),intersection_area_mm2=a.intersection(b.union(c)).area))
 fig.tight_layout();fig.savefig(D/'results/REGISTERED_SECTIONS.png')
 (D/'results/SECTIONS.json').write_text(json.dumps(rows,indent=2)+'\n')
 print([(r['x_mm'],r.get('intersection_area_mm2',r.get('error'))) for r in rows])
