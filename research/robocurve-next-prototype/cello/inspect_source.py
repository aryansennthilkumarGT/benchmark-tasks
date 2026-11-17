"""Inspect unmodified CELLO solids; do not infer assembly transforms from print layouts."""
from pathlib import Path
import json, hashlib, sys
sys.path.insert(0, '/workspace/robocurve-cpu-deps')
import cadquery as cq
from OCP.BRepAdaptor import BRepAdaptor_Surface
from OCP.GeomAbs import GeomAbs_Cylinder
D = Path(__file__).resolve().parent
S = D.parent/'sources/cello/step'
rows = []
for p in sorted(S.glob('*.step')):
    parts = []
    for s in cq.importers.importStep(str(p)).solids().vals():
        b = s.BoundingBox()
        cylinders = []
        for face in s.Faces():
            a = BRepAdaptor_Surface(face.wrapped)
            if a.GetType() == GeomAbs_Cylinder:
                c = a.Cylinder(); loc = c.Location(); axis = c.Axis().Direction()
                item = dict(radius_mm=c.Radius(), axis=list(axis.Coord()), point_mm=list(loc.Coord()))
                if item not in cylinders: cylinders.append(item)
        parts.append(dict(volume_mm3=s.Volume(), centroid_mm=list(s.Center().toTuple()),
                          bounds_mm=[b.xmin,b.ymin,b.zmin,b.xmax,b.ymax,b.zmax], cylinders=cylinders))
    rows.append(dict(file=p.name, sha256=hashlib.sha256(p.read_bytes()).hexdigest(), solids=parts))
(D/'results/SOURCE_INSPECTION.json').write_text(json.dumps(rows, indent=2)+'\n')
for row in rows:
    print(row['file'], 'solids',len(row['solids']))
    for s in row['solids']:
        print('  volume', round(s['volume_mm3'],2),'COM', [round(x,3) for x in s['centroid_mm']])
        if row['file'] in ['L1.step','L2.step','L3.step']:
            print('  cylinders',[(round(c['radius_mm'],3),[round(x,3) for x in c['point_mm']], [round(x,2) for x in c['axis']]) for c in s['cylinders'] if c['radius_mm']>5])
