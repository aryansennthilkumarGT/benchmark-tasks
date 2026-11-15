"""Inspect official KER STEP in native mm and run static CAD diagnostics on real surfaces.
CPU only. No pose is declared calibration-ready; no dynamics or latch model.
"""
from pathlib import Path
import json,time,hashlib
from OCP.STEPCAFControl import STEPCAFControl_Reader
from OCP.STEPControl import STEPControl_Reader
from OCP.TDocStd import TDocStd_Document
from OCP.TCollection import TCollection_ExtendedString
from OCP.TDF import TDF_LabelSequence,TDF_Label
from OCP.TDataStd import TDataStd_Name
from OCP.XCAFDoc import XCAFDoc_DocumentTool,XCAFDoc_ShapeTool
from OCP.TopLoc import TopLoc_Location
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_SOLID,TopAbs_FACE
from OCP.GProp import GProp_GProps
from OCP.BRepGProp import BRepGProp
from OCP.TColStd import TColStd_SequenceOfAsciiString
import argparse, gzip, numpy as np, cadquery as cq
parser=argparse.ArgumentParser()
parser.add_argument('--source-dir',type=Path,required=True)
parser.add_argument('--output-dir',type=Path,default=Path(__file__).resolve().parent/'results')
args=parser.parse_args()
root=args.source_dir;out=args.output_dir;out.mkdir(parents=True,exist_ok=True)
EXPECTED={'OpenArm KER.STEP': 'f9fdb476bb460ca396511bdde9d528ea7bc9d15a145963cfa0e4816240dcd17a', 'OpenArm KER JIG BASE.STEP': '7912bc827c20e01e45b97ee4eaa68ad9e2399aac88b28baf002d254af77ee3b1'}
rows=[];loaded={}
def bbox(shape):
 b=Bnd_Box();BRepBndLib.AddOptimal_s(shape,b,False,False);v=b.Get();return dict(min=list(v[:3]),max=list(v[3:]),size=[v[i+3]-v[i] for i in range(3)])
def name(l):
 a=TDataStd_Name();return a.Get().ToExtString() if l.FindAttribute(TDataStd_Name.GetID_s(),a) else ''
def mat(loc):
 t=loc.Transformation();return [[t.Value(i,j) for j in range(1,5)] for i in range(1,4)]+[[0.,0.,0.,1.]]
for file in ['OpenArm KER.STEP','OpenArm KER JIG BASE.STEP']:
 p=root/'OpenArm KER'/file
 assert hashlib.sha256(p.read_bytes()).hexdigest()==EXPECTED[file], 'Refuse unpinned CAD geometry'
 start=time.perf_counter();reader=STEPCAFControl_Reader();reader.SetNameMode(True)
 status=reader.ReadFile(str(p));print('read',file,status,flush=True)
 units=[TColStd_SequenceOfAsciiString() for _ in range(3)];reader.Reader().FileUnits(*units)
 assert units[0].Length()==1 and units[0].Value(1).ToCString()=='millimetre'
 doc=TDocStd_Document(TCollection_ExtendedString('MDTV-XCAF'));assert reader.Transfer(doc)
 tool=XCAFDoc_DocumentTool.ShapeTool_s(doc.Main());free=TDF_LabelSequence();tool.GetFreeShapes(free)
 items=[];shapes=[]
 def walk(label,parentloc=TopLoc_Location(),trail=()):
  local=XCAFDoc_ShapeTool.GetLocation_s(label);world=parentloc.Multiplied(local);target=TDF_Label()
  definition=label
  if XCAFDoc_ShapeTool.IsReference_s(label):
   assert XCAFDoc_ShapeTool.GetReferredShape_s(label,target);definition=target
  path=trail+(name(label) or name(definition) or '?',)
  children=TDF_LabelSequence()
  if XCAFDoc_ShapeTool.IsAssembly_s(definition) and XCAFDoc_ShapeTool.GetComponents_s(definition,children):
   for i in range(1,children.Length()+1):walk(children.Value(i),world,path)
  else:
   shape=XCAFDoc_ShapeTool.GetShape_s(definition)
   if shape.IsNull():return
   located=shape.Moved(world);shapes.append(located)
   solids=TopExp_Explorer(located,TopAbs_SOLID);nsol=0
   while solids.More():nsol+=1;solids.Next()
   g=GProp_GProps();BRepGProp.VolumeProperties_s(located,g)
   items.append(dict(index=len(items),path=list(path),name=name(definition),local_transform=mat(local),world_transform=mat(world),bbox_mm=bbox(located),solid_count=nsol,volume_mm3=g.Mass()))
 for i in range(1,free.Length()+1):walk(free.Value(i))
 whole=[bbox(XCAFDoc_ShapeTool.GetShape_s(free.Value(i))) for i in range(1,free.Length()+1)]
 row=dict(file=file,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),source_units=[[v.Value(i).ToCString() for i in range(1,v.Length()+1)] for v in units],free_roots=free.Length(),root_bounds_mm=whole,leaf_occurrences=len(items),leaves=items,seconds=time.perf_counter()-start)
 lo=np.min([x['bbox_mm']['min'] for x in items],axis=0);hi=np.max([x['bbox_mm']['max'] for x in items],axis=0)
 error=max(np.max(abs(lo-whole[0]['min'])),np.max(abs(hi-whole[0]['max'])))
 assert error < 1e-5, 'Occurrence transforms do not reproduce imported assembly bounds'
 row['occurrence_union_bound_error_mm']=float(error)
 rows.append(row);loaded[file]=shapes
 print(file,'roots',free.Length(),'leaves',len(items),'bounds',whole,flush=True)
 for item in items:
  if len(items)<30 or any(x in item['name'].lower() for x in ['base','jig','p1','j8','trg','grip','pipe']):print(item['index'],item['name'],item['bbox_mm'],flush=True)

with gzip.GzipFile(filename=str(out/'cad_inventory.json.gz'),mode='wb',mtime=0) as f:
    f.write((json.dumps(rows,indent=2)+'\n').encode())
# Selected surfaces are analytic source STEP faces; no proxy fixture geometry.
from OCP.BRepAdaptor import BRepAdaptor_Surface
from OCP.GeomAbs import GeomAbs_Cylinder,GeomAbs_Plane
from OCP.BRepAlgoAPI import BRepAlgoAPI_Common
from OCP.BRepExtrema import BRepExtrema_DistShapeShape
jig=cq.Shape.cast(loaded['OpenArm KER JIG BASE.STEP'][0]);faces=[]
for i,face in enumerate(jig.Faces()):
    a=BRepAdaptor_Surface(face.wrapped,True);b=face.BoundingBox();r=dict(face=i,type=str(a.GetType()),area_mm2=face.Area(),center_mm=list(face.Center().toTuple()),bounds_mm=[b.xmin,b.ymin,b.zmin,b.xmax,b.ymax,b.zmax])
    if a.GetType()==GeomAbs_Cylinder:
        g=a.Cylinder();r.update(radius_mm=g.Radius(),axis=[g.Axis().Direction().X(),g.Axis().Direction().Y(),g.Axis().Direction().Z()],axis_origin_mm=[g.Location().X(),g.Location().Y(),g.Location().Z()])
    if a.GetType()==GeomAbs_Plane:
        g=a.Plane();r['normal']=[g.Axis().Direction().X(),g.Axis().Direction().Y(),g.Axis().Direction().Z()]
    faces.append(r)
with gzip.GzipFile(filename=str(out/'jig_faces.json.gz'),mode='wb',mtime=0) as f:f.write((json.dumps(faces,indent=2)+'\n').encode())
seats=[r for r in faces if 'radius_mm' in r and abs(r['radius_mm']-7.5)<1e-6]
assert len(seats)==2
seat=next(r for r in seats if r['axis_origin_mm'][0]<0)
seat_face=jig.Faces()[seat['face']]
# Occurrence0 is source PIPE_15_100, selected by source name and actual geometry.
assert rows[0]['leaves'][0]['name']=='PIPE_15_100'
pipe=cq.Shape.cast(loaded['OpenArm KER.STEP'][0]);outer=[]
for f in pipe.Faces():
    a=BRepAdaptor_Surface(f.wrapped,True)
    if a.GetType()==GeomAbs_Cylinder and abs(a.Cylinder().Radius()-7.5)<1e-6:outer.append(f)
assert len(outer)>=1
controls=[]
for name,delta in [('as_exported_nominal',(0,0,0)),('hover_1mm',(0,0,1)),('lateral_interference_1mm',(1,0,0)),('partial_axial_shift_60mm',(0,60,0)),('off_seat_shift_120mm',(0,120,0))]:
    moved=pipe.translate(delta)
    distance=BRepExtrema_DistShapeShape(moved.wrapped,jig.wrapped);distance.Perform();assert distance.IsDone()
    common=BRepAlgoAPI_Common(moved.wrapped,jig.wrapped);common.Build();assert common.IsDone()
    g=GProp_GProps();BRepGProp.VolumeProperties_s(common.Shape(),g)
    shared_area=0.
    for source_face in outer:
        mf=source_face.translate(delta)
        patch=BRepAlgoAPI_Common(mf.wrapped,seat_face.wrapped);patch.Build();assert patch.IsDone()
        area=GProp_GProps();BRepGProp.SurfaceProperties_s(patch.Shape(),area);shared_area+=area.Mass()
    controls.append(dict(name=name,diagnostic_translation_mm=delta,minimum_BRep_distance_mm=distance.Value(),interference_volume_mm3=abs(g.Mass()),shared_seat_surface_area_mm2=shared_area,force_or_retention_or_task_success_assessed=False))
right=next(r for r in seats if r['axis_origin_mm'][0]>0)
angle=float(np.degrees(np.arccos(np.clip(abs(np.dot(right['axis'],[0.,1.,0.])),-1,1))))
result=dict(scope='Static source-CAD Boolean/distance diagnostics, NOT dynamics, snap-fit or a release simulation',units='mm, mm2, mm3',source_outer_cylinder_face_count=len(outer),seat_faces=seats,right_seat_axis_angle_to_exported_Y_axis_deg=angle,controls=controls,calibration_ready_KER_joint_registration='NOT_ESTABLISHED',force_model='NONE',global_joint_path='NONE')
(out/'CAD_CONTACT_DIAGNOSTICS.json').write_text(json.dumps(result,indent=2)+'\n')
assert controls[0]['interference_volume_mm3'] < 1e-3
assert abs(controls[0]['shared_seat_surface_area_mm2']-seat['area_mm2'])<1e-5
assert controls[1]['shared_seat_surface_area_mm2'] < 1e-3
assert controls[2]['interference_volume_mm3'] > 1
assert controls[3]['shared_seat_surface_area_mm2'] < controls[0]['shared_seat_surface_area_mm2']
summary=dict(files=[dict(file=r['file'],sha256=r['sha256'],source_units=r['source_units'],free_roots=r['free_roots'],leaf_occurrences=r['leaf_occurrences'],solids=sum(x['solid_count'] for x in r['leaves']),root_bounds_mm=r['root_bounds_mm'],occurrence_union_bound_error_mm=r['occurrence_union_bound_error_mm']) for r in rows],CAD_diagnostic_assertions_passed=True,commercial_geometry_warning='Release KER README says commercial parts are simplified; exact purchased details may be omitted',mechanism_or_robot_feasibility_claim=False)
(out/'CAD_SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(result,indent=2))
