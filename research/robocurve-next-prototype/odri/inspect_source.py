from pathlib import Path
import json,sys
sys.path.insert(0,'/workspace/robocurve-cpu-deps')
import cadquery as cq
from OCP.BRepAdaptor import BRepAdaptor_Surface
from OCP.GeomAbs import GeomAbs_Cylinder
D=Path(__file__).resolve().parent
S=D.parent/'sources/odri/step_files'
rows=[]
for p in S.glob('*.STEP'):
 s=cq.importers.importStep(str(p)).val();b=s.BoundingBox();cs=[]
 for i,f in enumerate(s.Faces()):
  a=BRepAdaptor_Surface(f.wrapped)
  if a.GetType()==GeomAbs_Cylinder:
   c=a.Cylinder();cs.append(dict(face=i,radius_mm=c.Radius(),point_mm=list(c.Location().Coord()),axis=list(c.Axis().Direction().Coord())))
 row=dict(file=p.name,solids=len(s.Solids()),bounds_mm=[b.xmin,b.ymin,b.zmin,b.xmax,b.ymax,b.zmax],cylinders=cs);rows.append(row)
 print(p.name,row['bounds_mm']);print([(c['face'],round(c['radius_mm'],4),[round(x,4) for x in c['point_mm']],c['axis']) for c in cs])
(D/'results/GEOMETRY.json').write_text(json.dumps(rows,indent=2)+'\n')
