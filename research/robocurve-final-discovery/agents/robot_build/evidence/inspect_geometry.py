"""CPU-only source geometry inspection; no robot reach/contact pass is claimed."""
from pathlib import Path
import json, struct
import numpy as np
import cadquery as cq
from OCP.BRepAdaptor import BRepAdaptor_Surface
D=Path(__file__).resolve().parent
out={"method":"Binary STL vertex bounds and OCCT analytic surface inspection; millimetres", "stl":[], "step":[]}
for p in sorted(D.rglob('*')):
    if p.suffix.lower()=='.stl':
        b=p.read_bytes()
        try:
            n=struct.unpack('<I',b[80:84])[0]
            dt=np.dtype([('normal','<f4',(3,)),('v','<f4',(3,3)),('attribute','<u2')])
            a=np.frombuffer(b[84:],dtype=dt,count=n)['v'].reshape(-1,3)
            out['stl'].append({"path":str(p.relative_to(D)),"triangles":n,"bounds_mm":[a.min(0).tolist(),a.max(0).tolist()],"size_mm":(a.max(0)-a.min(0)).tolist()})
        except (ValueError,struct.error):
            pass
    if p.suffix.lower()=='.step':
        a=cq.importers.importStep(str(p));bbox=a.val().BoundingBox();cyl=[]
        for f in a.faces().vals():
            if f.geomType()=='CYLINDER':
                c=BRepAdaptor_Surface(f.wrapped).Cylinder();cyl.append({"radius_mm":c.Radius(),"axis_point_mm":c.Location().Coord(),"axis_direction":c.Axis().Direction().Coord()})
        out['step'].append({"path":str(p.relative_to(D)),"solids":len(a.solids().vals()),"size_mm":[bbox.xlen,bbox.ylen,bbox.zlen],"cylinders":cyl})
(D/'geometry-reproduced.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({"stl_count":len(out['stl']),"step_count":len(out['step']),"output":"geometry-reproduced.json"}))
