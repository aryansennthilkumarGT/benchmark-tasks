"""Independent original-STEP registration and numerical beam/SDF checks."""
from pathlib import Path
import sys,json,hashlib
sys.path.insert(0,'/workspace/robocurve-cpu-deps')
import numpy as np,cadquery as cq,shapely
from OCP.BRepAdaptor import BRepAdaptor_Surface
from OCP.GeomAbs import GeomAbs_Cylinder
from shapely.geometry import shape
from elastic_ring import Ring,Field
from sections import S
D=Path(__file__).resolve().parent
foot=cq.importers.importStep(str(S/'foot_structure.STEP')).val().rotate((0,0,0),(1,0,0),90).translate((0,0,-160))
guide=[]
for name in ['foot_structure.STEP','lower_leg_structure_base.STEP','lower_leg_structure_fork.STEP']:
 original=cq.importers.importStep(str(S/name)).val()
 for i,face in enumerate(original.Faces()):
  surface=BRepAdaptor_Surface(face.wrapped)
  if surface.GetType()!=GeomAbs_Cylinder:continue
  c=surface.Cylinder();radius=c.Radius()
  if abs(radius-.85)<1e-5 or name=='foot_structure.STEP' and abs(radius-.775)<1e-5:
   b=face.BoundingBox();guide.append(dict(file=name,face=i,radius_mm=radius,point_mm=list(c.Location().Coord()),axis=list(c.Axis().Direction().Coord()),bounds_mm=[b.xmin,b.ymin,b.zmin,b.xmax,b.ymax,b.zmax]))
(D/'results/GUIDE_GEOMETRY.json').write_text(json.dumps(guide,indent=2)+'\n')
clearance=abs(guide[2]['point_mm'][1])+guide[2]['radius_mm']-.75
assert abs(clearance-.4)<1e-6
rows=[]
for n in ['lower_leg_structure_base.STEP','lower_leg_structure_fork.STEP']:
 s=cq.importers.importStep(str(S/n)).val();v=foot.intersect(s).Volume()
 rows.append(dict(file=n,intersection_volume_mm3=v));print(n,v,flush=True)
# Do not silently use wrong source registration.
assert max(r['intersection_volume_mm3'] for r in rows)<.01,'Source assembly intersection; STOP before interpreting contact'
ring=Ring();q=ring.circle([9.5,0]);q[3]+=[.07,-.1];E,g=ring.energy(q)
errors=[]
for i,j in [(3,0),(3,1),(4,0),(2,1)]:
 z=q.copy();z[i,j]+=1e-6;a=ring.energy(z)[0];z[i,j]-=2e-6;b=ring.energy(z)[0];errors.append(abs((a-b)/2e-6-g[i,j]))
# A free ring has no hidden centering spring to world/foot.
translated=ring.energy(q+[12.,-8.])[0]
rot=np.array([[.6,-.8],[.8,.6]]);rotated=ring.energy(q@rot.T)[0]
assert max(errors)<1e-5 and abs(translated-E)<1e-10 and abs(rotated-E)<1e-10
sections=json.loads((D/'results/SECTIONS.json').read_text());sdf=[]
rng=np.random.default_rng(7)
for x in [2.123,-2.123]:
 row=next(r for r in sections if r['x_mm']==x)
 for key in ['foot','fixed']:
  polygon=shape(row[key]);f=Field(polygon);points=rng.uniform(-14,14,(3000,2))
  actual=shapely.distance(shapely.points(points),polygon.boundary)
  actual[shapely.contains_xy(polygon,points[:,0],points[:,1])]*=-1
  error=np.abs(actual-f.at(points)[0]);sdf.append(dict(x_mm=x,body=key,max_error_mm=float(error.max()),p99_error_mm=float(np.quantile(error,.99))))
assert max(a['max_error_mm'] for a in sdf)<.03
out=dict(guide_pin_lateral_clearance_mm=clearance,guide_channel_z_relative_foot_mm=[16,18],pin_embed_depth_not_measured_mm=[0,3.6],source_STEP_overlap_tests=rows,registration=dict(foot_rotation_about_X_deg=90,foot_translation_mm=[0,0,-160],basis='Foot pin +Y aligned with leg +Z and coincident optical X axes; zero-overlap alone is not full hardware assembly validation'),beam_gradient_max_error_N=max(errors),energy_translation_error_Nmm=abs(translated-E),energy_rotation_error_Nmm=abs(rotated-E),SDF_checks=sdf,material_calibrated=False)
(D/'results/SOURCE_AUDIT.json').write_text(json.dumps(out,indent=2)+'\n');print(out,flush=True)
