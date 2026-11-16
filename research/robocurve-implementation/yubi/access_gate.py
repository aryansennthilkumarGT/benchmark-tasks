"""Bounded YUBI access attempt. Failing suite kills investment, not all possible poses."""
from pathlib import Path
import argparse,sys,json,hashlib
sys.path.insert(0,str(Path(__file__).resolve().parents[1]));sys.path.insert(0,'/workspace/robocurve-cpu-deps')
import numpy as np
import fcl
from scipy.spatial.transform import Rotation
from common.cad import ROOT,yubi_shapes,triangulate,YUBI_SHA
from common.access import Access,mesh,transform
D=Path(__file__).resolve().parent
parser=argparse.ArgumentParser();parser.add_argument('--variant',choices=['direct','raised-transit'],default='raised-transit');variant=parser.parse_args().variant
A=Access();shapes=yubi_shapes();manifest=[];geoms=[]
for i,s in enumerate(shapes):
 if i==34:continue
 v,f=triangulate(s);geoms.append((i,mesh(v,f)));manifest.append(dict(occurrence=i,vertices=len(v),triangles=len(f)))
H=np.array([-22.055430442,9.919948188,1035.])*.001
# Candidate feature at faces276--279, near groove253. Occupancy audit rejects
# this point as a free band centreline; no installed-band model is inferred.
S=np.array([-37.540496996,5.13831255,954.5])*.001
G=np.array([-37.540496996,-.080051812,980.])*.001
# The No16 section/free length are NOT independently read. This is a loose trial
# loop for access screening only, with unanchored nodes and unilateral floor contact.
r=.019;section=.00055;pts=np.array([[.19+r*np.cos(t),-.11+r*np.sin(t),.765] for t in np.linspace(0,2*np.pi,64,endpoint=False)])
vel=np.zeros_like(pts);L=np.linalg.norm(np.roll(pts,-1,axis=0)-pts,axis=1)
for _ in range(700):
 d=np.roll(pts,-1,axis=0)-pts;l=np.linalg.norm(d,axis=1);spring=3*(l-L)[:,None]*d/l[:,None];force=spring-np.roll(spring,1,axis=0);force[:,2]-=9.80665*.00001
 vel+=force/.00001*.0002;vel*=.995;pts+=vel*.0002
 below=pts[:,2]<.7475+section;pts[below,2]=.7475+section;vel[below,2]=np.maximum(0,vel[below,2])
np.save(D/'results/loose_band_nodes.npy',pts)
rows=[]
# Two ordinary fixture placements. Pivot vertical; module fixed through real GRIP.
for yaw in [-35,35]:
 C=np.array([[0.,0.,1.],[1.,0.,0.],[0.,1.,0.]]);R=Rotation.from_euler('z',yaw,degrees=True).as_matrix()@C;target=np.array([.35,.03,1.01]) if yaw<0 else np.array([.45,.10,1.07]);t=target-R@H
 entries=[('source-'+str(i),g,R,t) for i,g in geoms]
 entries += [('table',fcl.Box(1.1,1.3,.06),np.eye(3),np.array([.36,0,.7175]))]
 grip=shapes[8].BoundingBox();gc=R@(np.array([(grip.xmin+grip.xmax)/2,(grip.ymin+grip.ymax)/2,(grip.zmin+grip.zmax)/2])*.001)+t
 # Ordinary fixture support underneath actual grip. No hook or finger supported.
 height=max(.02,gc[2]-.7475-.012)
 entries += [('grip-support',fcl.Box(.04,.04,height),np.eye(3),np.array([gc[0],gc[1],.7475+height/2]))]
 A.set_obstacles(entries)
 for tooltype in ['stock-pads','ordinary-blunt-pick']:
  for spin in [0,90,180,270]:
   # One tabletop acquisition plus finite outward approach directions at real hook.
   for tilt in [25,65,105,145]:
    down=Rotation.from_euler('xyz',[180,0,spin],degrees=True).as_matrix();rot=Rotation.from_euler('xyz',[180-tilt,0,spin],degrees=True).as_matrix()
    pickup=pts[0]+np.array([0,0,.003 if variant=='direct' else (.014 if tooltype=='stock-pads' else .001)]);hook=target+R@np.array([-.001,0,.002]);saddle=R@S+t;groove=R@G+t
    offset=.147 if tooltype!='stock-pads' else 0.
    tool=[]
    if offset:
     # Normal9mm handle,2mm blunt shaft and1.6mm blunt tip; held by handle.
     for name,rad,length,z in [('handle',.0045,.080,.135),('shaft',.001,.10,.225),('blunt-tip',.0008,.006,.278)]:
      tool.append((name,fcl.Capsule(rad,length),transform((0,0,z))))
    points=([('transit-above-band',pickup+np.array([0,0,.20])-down[:,2]*offset,down)] if variant=='raised-transit' else [])+[('pickup',pickup-down[:,2]*offset,down),('lift',pickup+np.array([0,0,.10])-down[:,2]*offset,down),('first-hook',hook-rot[:,2]*offset,rot),('groove',groove-rot[:,2]*offset,rot),('second-hook',saddle+R@np.array([0,-.003,0])-rot[:,2]*offset,rot),('withdraw',hook+np.array([0,0,.10])-rot[:,2]*offset,rot)]
    key=[A.qready.copy()];errors=[];failed=None
    for label,p,rmat in points:
     q,e=A.ik(p,rmat,seed=key[-1],gap=.0011 if not offset else .009);errors.append(dict(stage=label,**e))
     if not e['valid']:failed=dict(clear=False,reason='IK endpoint not solved within1mm/1.15deg',stage=label);break
     key.append(q)
    prefix=A.sample_path(key,tool=tool) if len(key)>1 else dict(clear=False,sampled_poses=0,reason='No solved acquisition prefix')
    result=failed if failed else prefix
    result['valid_prefix_collision_check']=prefix
    rows.append(dict(fixture_yaw_deg=yaw,approach_yaw_deg=spin,approach_tilt_deg=tilt,method=tooltype,ik=errors,path=result,joint_keyframes=[q.tolist() for q in key]))
    print(yaw,tooltype,spin,tilt,result.get('reason',result.get('first_collision',{})),flush=True)
result=dict(variant=variant,source_sha256=YUBI_SHA,source_meshes=manifest,second_saddle=dict(center_mm=(S*1000).tolist(),faces=[276,277,278,279],groove_face=253,role='Unvalidated feature hypothesis; separate occupancy audit rejects this point as a free band centreline',geometry_measured=True,band_contact_point_offset='Not material-calibrated'),loose_band=dict(nodes=64,anchors=0,radius_mm=19,section_radius_mm=.55,dimensional_provenance='Explicit exploratory values; not verified No16 product specification',settled_lowest_z_m=float(pts[:,2].min()),free_node_velocity_max_m_s=float(np.linalg.norm(vel,axis=1).max())),robot_hulls_per_arm=315,approaches=rows,summary=dict(attempts=len(rows),sampled_clear_paths=sum(r['path']['clear'] for r in rows)),decision='STOP YUBI if no route; this bounded suite is not a universal impossibility proof',limitations=['No stable contact acquisition was established by a geometric path','No band autoattachment used; stage2 must not start on an invalid route','No all-pose impossibility claim; fixtures/tool choices explicitly bounded','No actual No16 dimensions or material calibration'])
(D/'results'/('ACCESS_'+variant.upper().replace('-','_')+'.json')).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result['summary']))
