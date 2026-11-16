"""Preserve named YUBI source occurrence frames; not a reach or contact pass."""
from pathlib import Path
import json,hashlib
import cadquery as cq
from OCP.STEPCAFControl import STEPCAFControl_Reader
from OCP.TDocStd import TDocStd_Document
from OCP.TCollection import TCollection_ExtendedString
from OCP.TDF import TDF_LabelSequence,TDF_Label
from OCP.TDataStd import TDataStd_Name
from OCP.XCAFDoc import XCAFDoc_DocumentTool,XCAFDoc_ShapeTool
from OCP.TopLoc import TopLoc_Location
D=Path(__file__).resolve().parent/'yubi';p=D/'STEP/glove/YUBI Glove Assy_ver2_R.STEP'
r=STEPCAFControl_Reader();r.SetNameMode(True);r.ReadFile(str(p));doc=TDocStd_Document(TCollection_ExtendedString('MDTV-XCAF'));assert r.Transfer(doc);tool=XCAFDoc_DocumentTool.ShapeTool_s(doc.Main());free=TDF_LabelSequence();tool.GetFreeShapes(free)
def name(l):
 a=TDataStd_Name();return a.Get().ToExtString() if l.FindAttribute(TDataStd_Name.GetID_s(),a) else ''
def matrix(loc):
 t=loc.Transformation();return [[t.Value(i,j) for j in range(1,5)] for i in range(1,4)]+[[0.,0.,0.,1.]]
rows=[];out=D/'registered_parts';out.mkdir(exist_ok=True)
def walk(l,parent=TopLoc_Location(),trail=()):
 world=parent.Multiplied(XCAFDoc_ShapeTool.GetLocation_s(l));d=l
 if XCAFDoc_ShapeTool.IsReference_s(l):d=TDF_Label();assert XCAFDoc_ShapeTool.GetReferredShape_s(l,d)
 path=trail+(name(l) or name(d),);ch=TDF_LabelSequence()
 if XCAFDoc_ShapeTool.IsAssembly_s(d) and XCAFDoc_ShapeTool.GetComponents_s(d,ch):
  for i in range(1,ch.Length()+1):walk(ch.Value(i),world,path)
 else:
  s=XCAFDoc_ShapeTool.GetShape_s(d)
  if s.IsNull():return
  s=cq.Shape.cast(s.Moved(world));b=s.BoundingBox();row=dict(index=len(rows),name=name(d),path=path,world_transform=matrix(world),bounds_mm=[b.xmin,b.ymin,b.zmin,b.xmax,b.ymax,b.zmax],solid_count=len(s.Solids()))
  if any(k in row['name'] for k in ['HOLDER_Quest','FINGER with Gear','UNDER PLATE','UPPER PLATE','GRIP']):
   fp=out/(str(row['index'])+'.step');cq.exporters.export(s,str(fp));row['registered_step']=str(fp.relative_to(D));row['registered_sha256']=hashlib.sha256(fp.read_bytes()).hexdigest()
  rows.append(row)
for i in range(1,free.Length()+1):walk(free.Value(i))
manifest=dict(source_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),source='Toyota/yubi-hw@dd8bd13d2fd8e5003057243576f88be333d95fc5/STEP/glove/YUBI Glove Assy_ver2_R.STEP',units='mm',leaf_occurrences=rows)
(D/'assembly-occurrences.json').write_text(json.dumps(manifest,indent=2)+'\n')
for r in rows:
 if 'registered_step' in r:print(r['index'],r['name'],r['bounds_mm'],r['registered_step'])
print('total',len(rows),'No rubber band geometry is present; source hook geometry and frames only.')
