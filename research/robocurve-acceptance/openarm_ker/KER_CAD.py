"""Read the pinned KER CAD only; no previous static control experiments rerun."""
from pathlib import Path
import hashlib
import numpy as np
from OCP.STEPCAFControl import STEPCAFControl_Reader
from OCP.TDocStd import TDocStd_Document
from OCP.TCollection import TCollection_ExtendedString
from OCP.TDF import TDF_LabelSequence,TDF_Label
from OCP.TDataStd import TDataStd_Name
from OCP.XCAFDoc import XCAFDoc_DocumentTool,XCAFDoc_ShapeTool
from OCP.TopLoc import TopLoc_Location
from OCP.BRepAdaptor import BRepAdaptor_Surface
from OCP.GeomAbs import GeomAbs_Cylinder,GeomAbs_Plane
import cadquery as cq

EXPECTED={'OpenArm KER.STEP':'f9fdb476bb460ca396511bdde9d528ea7bc9d15a145963cfa0e4816240dcd17a','OpenArm KER JIG BASE.STEP':'7912bc827c20e01e45b97ee4eaa68ad9e2399aac88b28baf002d254af77ee3b1'}

def load(root,filename):
 p=Path(root)/'OpenArm KER'/filename
 assert hashlib.sha256(p.read_bytes()).hexdigest()==EXPECTED[filename]
 reader=STEPCAFControl_Reader();reader.SetNameMode(True);reader.ReadFile(str(p))
 doc=TDocStd_Document(TCollection_ExtendedString('MDTV-XCAF'));assert reader.Transfer(doc)
 tool=XCAFDoc_DocumentTool.ShapeTool_s(doc.Main());free=TDF_LabelSequence();tool.GetFreeShapes(free);result=[]
 def name(l):
  a=TDataStd_Name();return a.Get().ToExtString() if l.FindAttribute(TDataStd_Name.GetID_s(),a) else ''
 def walk(l,parent=TopLoc_Location(),path=()):
  world=parent.Multiplied(XCAFDoc_ShapeTool.GetLocation_s(l));d=l
  if XCAFDoc_ShapeTool.IsReference_s(l):
   d=TDF_Label();assert XCAFDoc_ShapeTool.GetReferredShape_s(l,d)
  path=path+(name(l) or name(d),);children=TDF_LabelSequence()
  if XCAFDoc_ShapeTool.IsAssembly_s(d) and XCAFDoc_ShapeTool.GetComponents_s(d,children):
   for i in range(1,children.Length()+1):walk(children.Value(i),world,path)
  else:
   s=XCAFDoc_ShapeTool.GetShape_s(d)
   if not s.IsNull():result.append(dict(index=len(result),name=name(d),path=path,shape=cq.Shape.cast(s.Moved(world))))
 for i in range(1,free.Length()+1):walk(free.Value(i))
 return result

def features(shape):
 result=[]
 for i,f in enumerate(shape.Faces()):
  a=BRepAdaptor_Surface(f.wrapped,True);b=f.BoundingBox();row=dict(face=i,type=str(a.GetType()).split('.')[-1],area=f.Area(),center=f.Center().toTuple(),bounds=[b.xmin,b.ymin,b.zmin,b.xmax,b.ymax,b.zmax])
  if a.GetType()==GeomAbs_Cylinder:
   g=a.Cylinder();d=g.Axis().Direction();o=g.Location();row.update(radius=g.Radius(),axis=(d.X(),d.Y(),d.Z()),origin=(o.X(),o.Y(),o.Z()))
  elif a.GetType()==GeomAbs_Plane:
   g=a.Plane();d=g.Axis().Direction();row.update(normal=(d.X(),d.Y(),d.Z()))
  result.append(row)
 return result
