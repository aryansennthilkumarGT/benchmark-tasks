"""Extract analytic surfaces on source-registered YUBI bodies; not a mechanism test."""
from pathlib import Path
import cadquery as cq,json,hashlib
from OCP.BRepAdaptor import BRepAdaptor_Surface
from OCP.GeomAbs import GeomAbs_Cylinder,GeomAbs_Plane
D=Path(__file__).resolve().parent/'yubi';out=[]
for idx in [0,1,2,3,8,16]:
 p=D/'registered_parts'/f'{idx}.step';s=cq.importers.importStep(str(p)).val();fs=[]
 for i,f in enumerate(s.Faces()):
  a=BRepAdaptor_Surface(f.wrapped,True);b=f.BoundingBox();row=dict(face=i,area_mm2=f.Area(),center_mm=f.Center().toTuple(),bounds_mm=[b.xmin,b.ymin,b.zmin,b.xmax,b.ymax,b.zmax],type=str(a.GetType()))
  if a.GetType()==GeomAbs_Cylinder:
   c=a.Cylinder();row.update(radius_mm=c.Radius(),axis_point_mm=c.Location().Coord(),axis_direction=c.Axis().Direction().Coord())
  if a.GetType()==GeomAbs_Plane:row['normal']=a.Plane().Axis().Direction().Coord()
  fs.append(row)
 out.append(dict(index=idx,path=str(p.relative_to(D)),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),faces=fs))
(D/'registered-features.json').write_text(json.dumps(out,indent=2)+'\n')
for o in out:
 if o['index'] in [2,3]:
  print(o['index'],[f for f in o['faces'] if f.get('radius_mm') and abs(f['radius_mm']-4)<.01])
