"""Resolve the least-overlapping static case of the same YUBI screen with OCCT.
Not another task prototype. Uses actual source solids and actual YAM convex hulls.
"""
import argparse,json,hashlib,sys
from pathlib import Path
import numpy as np
import cadquery as cq
from scipy.spatial import ConvexHull
from OCP.STEPCAFControl import STEPCAFControl_Reader
from OCP.TDocStd import TDocStd_Document
from OCP.TCollection import TCollection_ExtendedString
from OCP.TDF import TDF_LabelSequence,TDF_Label
from OCP.XCAFDoc import XCAFDoc_DocumentTool,XCAFDoc_ShapeTool
from OCP.TopLoc import TopLoc_Location
from OCP.gp import gp_Trsf
D=Path(__file__).resolve().parent
sys.path.insert(0,str(D.parent.parent/'robocurve-acceptance/preflight'))
from access_core import Robot
parser=argparse.ArgumentParser();parser.add_argument('--source',type=Path,default=D.parent/'agents/robot_build/evidence/yubi/STEP/glove/YUBI Glove Assy_ver2_R.STEP');source=parser.parse_args().source
x=json.loads((D/'YUBI_ENVELOPE_RESULT.json').read_text())
assert hashlib.sha256(source.read_bytes()).hexdigest()==x['source_assembly_sha256']
reader=STEPCAFControl_Reader();assert reader.ReadFile(str(source))==1
doc=TDocStd_Document(TCollection_ExtendedString('MDTV-XCAF'));assert reader.Transfer(doc)
tool=XCAFDoc_DocumentTool.ShapeTool_s(doc.Main());free=TDF_LabelSequence();tool.GetFreeShapes(free)
shapes=[]
def walk(label,parent=TopLoc_Location()):
 world=parent.Multiplied(XCAFDoc_ShapeTool.GetLocation_s(label));ref=label
 if XCAFDoc_ShapeTool.IsReference_s(label):
  ref=TDF_Label();assert XCAFDoc_ShapeTool.GetReferredShape_s(label,ref)
 children=TDF_LabelSequence()
 if XCAFDoc_ShapeTool.IsAssembly_s(ref) and XCAFDoc_ShapeTool.GetComponents_s(ref,children):
  for i in range(1,children.Length()+1):walk(children.Value(i),world)
 else:
  s=XCAFDoc_ShapeTool.GetShape_s(ref)
  if not s.IsNull():shapes.append(cq.Shape.cast(s.Moved(world)))
for i in range(1,free.Length()+1):walk(free.Value(i))
assert len(shapes)==46
case=min(x['cases'],key=lambda z:z['overlapping_envelope_pairs'])
assert len(case['first_pairs'])==case['overlapping_envelope_pairs'],'Narrow phase must not silently truncate overlaps'
M=np.array(case['source_to_world']);pose=gp_Trsf();pose.SetValues(*[float(M[i,j]) for i in range(3) for j in range(4)]);robot=Robot();q=x['joint_coordinates_each_arm'];hulls=robot.world_hulls(q,'left')
byname={h['name']:h for h in hulls}
def solid(v):
 h=ConvexHull(v);faces=[]
 for tri,eq in zip(h.simplices,h.equations):
  a=v[tri].copy()
  if np.dot(np.cross(a[1]-a[0],a[2]-a[0]),eq[:3])<0:a=a[[0,2,1]]
  w=cq.Wire.makePolygon([cq.Vector(*z) for z in a],close=True)
  faces.append(cq.Face.makeFromWires(w))
 out=cq.Solid.makeSolid(cq.Shell.makeShell(faces))
 assert out.isValid() and out.Volume()>0
 return out
rows=[]
for part,link,name in case['first_pairs']:
 s=shapes[part].scale(.001).moved(cq.Location(pose))
 h=solid(byname[name]['world']);common=s.intersect(h)
 vol=abs(common.Volume()) if common.Solids() else 0.0
 dist=s.distance(h)
 rows.append({'source_occurrence':part,'robot_link':link,'robot_hull':name,'source_solid_valid':s.isValid(),'hull_solid_valid':h.isValid(),'common_volume_mm3':vol*1e9,'minimum_surface_distance_mm':dist*1000,'interpretation':'actual source-solid overlap' if vol>1e-12 else ('separated in exact model' if dist>1e-6 else 'touching/numerically unresolved')})
result={'kind':'OCCT narrow phase of best static case from same bounded screen','case':{'yaw_deg':case['yaw_deg'],'hook_ahead_of_tcp_mm':case['hook_ahead_of_tcp_mm']},'source_parts':len(shapes),'pairs':rows,'scope':'Only resolves the source-envelope overlaps in this one pose. Does not certify any grasp, path, band routing, actual material or force.'}
(D/'YUBI_NARROWPHASE_RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
