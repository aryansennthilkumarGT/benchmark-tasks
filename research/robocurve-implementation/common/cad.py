"""Immutable-source CAD/mesh extraction for CPU experiments; SI mesh output."""
from pathlib import Path
import hashlib,json
import numpy as np
import cadquery as cq
from OCP.STEPCAFControl import STEPCAFControl_Reader
from OCP.TDocStd import TDocStd_Document
from OCP.TCollection import TCollection_ExtendedString
from OCP.TDF import TDF_LabelSequence,TDF_Label
from OCP.XCAFDoc import XCAFDoc_DocumentTool,XCAFDoc_ShapeTool
from OCP.TopLoc import TopLoc_Location
ROOT=Path(__file__).resolve().parents[3]
YUBI_PIN='dd8bd13d2fd8e5003057243576f88be333d95fc5'
YUBI_SHA='7cffdf898a1cf54b897e95c116aa9dea6ac4307c06964d551001ecf938f321dd'
def source_path():
 paths=[Path('/tmp/yubi-pinned-source/STEP/glove/YUBI Glove Assy_ver2_R.STEP'),ROOT/'research/robocurve-final-discovery/agents/robot_build/evidence/yubi/STEP/glove/YUBI Glove Assy_ver2_R.STEP']
 return next((p for p in paths if p.exists()),paths[0])
def yubi_shapes(path=None):
 p=Path(path or source_path());assert hashlib.sha256(p.read_bytes()).hexdigest()==YUBI_SHA
 reader=STEPCAFControl_Reader();assert reader.ReadFile(str(p))==1
 doc=TDocStd_Document(TCollection_ExtendedString('MDTV-XCAF'));assert reader.Transfer(doc)
 tool=XCAFDoc_DocumentTool.ShapeTool_s(doc.Main());free=TDF_LabelSequence();tool.GetFreeShapes(free);out=[]
 def walk(label,parent=TopLoc_Location()):
  world=parent.Multiplied(XCAFDoc_ShapeTool.GetLocation_s(label));ref=label
  if XCAFDoc_ShapeTool.IsReference_s(label):ref=TDF_Label();assert XCAFDoc_ShapeTool.GetReferredShape_s(label,ref)
  children=TDF_LabelSequence()
  if XCAFDoc_ShapeTool.IsAssembly_s(ref) and XCAFDoc_ShapeTool.GetComponents_s(ref,children):
   for i in range(1,children.Length()+1):walk(children.Value(i),world)
  else:
   s=XCAFDoc_ShapeTool.GetShape_s(ref)
   if not s.IsNull():out.append(cq.Shape.cast(s.Moved(world)))
 for i in range(1,free.Length()+1):walk(free.Value(i))
 assert len(out)==46
 return out

def triangulate(shape,deflection_mm=.08):
 vs,fs=shape.tessellate(deflection_mm,.10)
 return np.array([p.toTuple() for p in vs],float)*.001,np.asarray(fs,np.int32)
