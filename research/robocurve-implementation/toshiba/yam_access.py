"""Actual630-hull bimanual access to representative apparatus; NOT a grasp demo.
A prescribed held-tray relationship is a collision-planning hypothesis only.
"""
from pathlib import Path
import sys,json
sys.path.insert(0,'/workspace/robocurve-cpu-deps');sys.path.insert(0,str(Path(__file__).resolve().parents[1]));sys.path.insert(0,str(Path(__file__).resolve().parent))
import numpy as np,fcl,mujoco
from scipy.spatial.transform import Rotation
from common.access import Access,mesh,transform
from contact_coupon import build
D=Path(__file__).resolve().parent;A=Access();model=mujoco.MjModel.from_xml_string(build('correct'));data=mujoco.MjData(model)
for _ in range(3000):mujoco.mj_step(model,data)
origin=np.array([.50,0,.85]);static=[];traygeoms=[]
for i in range(model.ngeom):
 name=mujoco.mj_id2name(model,mujoco.mjtObj.mjOBJ_GEOM,i) or str(i);typ=model.geom_type[i];size=model.geom_size[i];R=data.geom_xmat[i].reshape(3,3);p=data.geom_xpos[i]+origin
 if name=='floor':continue
 is_tray=model.geom_bodyid[i]==mujoco.mj_name2id(model,mujoco.mjtObj.mjOBJ_BODY,'tray')
 if typ==mujoco.mjtGeom.mjGEOM_BOX:g=fcl.Box(*(2*size))
 elif typ==mujoco.mjtGeom.mjGEOM_CYLINDER:g=fcl.Cylinder(size[0],2*size[1])
 elif typ==mujoco.mjtGeom.mjGEOM_MESH:
  j=model.geom_dataid[i];v=model.mesh_vert[model.mesh_vertadr[j]:model.mesh_vertadr[j]+model.mesh_vertnum[j]];f=model.mesh_face[model.mesh_faceadr[j]:model.mesh_faceadr[j]+model.mesh_facenum[j]];g=mesh(np.array(v,float),np.array(f,np.int32))
 else:raise ValueError(typ)
 if is_tray:
  tid=mujoco.mj_name2id(model,mujoco.mjtObj.mjOBJ_BODY,'tray');Tb=data.xmat[tid].reshape(3,3);localp=Tb.T@(data.geom_xpos[i]-data.xpos[tid]);localR=Tb.T@R;traygeoms.append((name,g,localR,localp))
 else:static.append((name,g,R,p))
static += [('station-table',fcl.Box(1.1,1.3,.06),np.eye(3),np.array([.36,0,.7175])),('oven-bottom',fcl.Box(.4,.36,.03),np.eye(3),origin+np.array([0,0,-.015])),('oven-ceiling',fcl.Box(.4,.36,.01),np.eye(3),origin+np.array([0,0,.24]))]
# Two standard support rods and their posts; no special tray grasp handles.
for k,x in enumerate([.27,.33]):
 static += [(f'rack-rod{k}',fcl.Cylinder(.002,.20),Rotation.from_euler('x',np.pi/2).as_matrix(),np.array([x,0,.9255])),(f'rack-post{k}',fcl.Box(.008,.008,.178),np.eye(3),np.array([x,.11,.8365]))]
Rgrip=np.array([[0.,0.,1.],[0.,-1.,0.],[1.,0.,0.]])
# Five millimetre glass; actual distal pad inner faces derived from original hulls.
poses=[('acquire',np.array([.30,0,.93])),('lift',np.array([.30,0,1.01])),('insert',np.array([.50,0,1.01])),('lower',np.array([.50,0,.8645]))]
keys=[];ik=[];L=A.qready.copy();R=A.qready.copy()
for label,c in poses:
 pair=[]
 for side,y,seed in [('left',.075,L),('right',-.075,R)]:
  q,e=A.ik(c+np.array([-.11,y,0]),Rgrip,side=side,seed=seed,gap=.0049);pair.append(q);ik.append(dict(stage=label,side=side,**e))
 L,R=pair;keys.append((label,L,R,c))
# Release the5mm pinch and pull both hands out through the front.
Lopen=L.copy();Ropen=R.copy();Lopen[6:]=-.012;Ropen[6:]=-.012
keys.append(('release',Lopen,Ropen,poses[-1][1]))
for side,y,seed in [('left',.075,Lopen),('right',-.075,Ropen)]:
 q,e=A.ik(poses[-1][1]+[-.24,y,.025],Rgrip,side=side,seed=seed,gap=.024);ik.append(dict(stage='withdraw',side=side,**e))
 if side=='left':Le=q
 else:Re=q
keys.append(('withdraw',Le,Re,poses[-1][1]))
# Robot-arm link collision managers retain every original convex hull. Same-link
# and original URDF adjacent pairs are excluded as in existing validated preflight.
adj={frozenset([j['parent'],j['child']]) for j in A.r.joints};adj.add(frozenset(['tip_left','tip_right']))
def robotobjects(q,side):
 P=A.r.fk(q,side)[0];groups={};allobjs=[]
 for h,g in zip(A.r.hulls,A.geoms):
  T=P[h['link']];o=fcl.CollisionObject(g,fcl.Transform(T[:3,:3],T[:3,3]));groups.setdefault(h['link'],[]).append(o);allobjs.append(o)
 managers={}
 for link,obs in groups.items():
  m=fcl.DynamicAABBTreeCollisionManager();m.registerObjects(obs);m.setup();managers[link]=m
 full=fcl.DynamicAABBTreeCollisionManager();full.registerObjects(allobjs);full.setup()
 return groups,managers,full

def self_pair(left,right):
 la,lm,lf=robotobjects(left,'left');ra,rm,rf=robotobjects(right,'right')
 d=fcl.CollisionData();lf.collide(rf,d,fcl.defaultCollisionCallback)
 if d.result.is_collision:return 'arm-arm'
 for side,ms in [('left',lm),('right',rm)]:
  links=list(ms)
  for i,a in enumerate(links):
   for b in links[i+1:]:
    if frozenset([a,b]) in adj:continue
    d=fcl.CollisionData();ms[a].collide(ms[b],d,fcl.defaultCollisionCallback)
    if d.result.is_collision:return side+':'+a+'/'+b
 return None

def tray_check(left,right,c):
 # Actual glass body cylinder; underside keys are central and do not approach hands.
 # The geometry screen does NOT certify frictional grasp stability.
 glass=fcl.CollisionObject(fcl.Cylinder(.135,.005),fcl.Transform(np.eye(3),c));unintended=[];tipcontacts=0
 for side,q in [('left',left),('right',right)]:
  P=A.r.fk(q,side)[0]
  for h,g in zip(A.r.hulls,A.geoms):
   T=P[h['link']];o=fcl.CollisionObject(g,fcl.Transform(T[:3,:3],T[:3,3]));rr=fcl.CollisionResult();n=fcl.collide(o,glass,fcl.CollisionRequest(),rr)
   if n:
    if h['link'].startswith('tip'):tipcontacts+=1
    else:unintended.append([side,h['link'],h['name']])
 return unintended,tipcontacts

def run(angle):
 a=np.deg2rad(angle);hinge=origin+[-.20,.18,.12]
 # Original left-hinged door role preserved; donor angle/dimensions are unverified.
 doorR=Rotation.from_euler('z',-a).as_matrix();doorcenter=hinge+doorR@np.array([0,-.18,0])
 entries=static+[('open-door',fcl.Box(.01,.36,.24),doorR,doorcenter)]
 A.set_obstacles(entries);samples=[]
 # Initial acquisition is a posed pregrasp, not a verified contact pickup.
 for k in range(len(keys)-1):
  a0,L0,R0,c0=keys[k];a1,L1,R1,c1=keys[k+1]
  for u in np.linspace(0,1,13):
   l=L0*(1-u)+L1*u;r=R0*(1-u)+R1*u;c=c0*(1-u)+c1*u
   hits=A.collision(l,r);own=self_pair(l,r);bad,tips=tray_check(l,r,c)
   payload_hits=[]
   for name,g,rg,pg in traygeoms:
    ob=fcl.CollisionObject(g,fcl.Transform(rg,c+pg))
    for nn,gg,rr,pp in entries:
     if (nn.startswith('wheel') and name=='glass' or nn.startswith('drivekey') and name.startswith('glasslug')) and (k>=3 or k==2 and u>.99):continue
     result=fcl.CollisionResult()
     if fcl.collide(ob,fcl.CollisionObject(gg,fcl.Transform(rr,pp)),fcl.CollisionRequest(),result):payload_hits.append([name,nn]);break
   samples.append(dict(payload_obstacle_hits=payload_hits,segment=a0+'->'+a1,fraction=float(u),obstacle_collision=hits[0] if hits else None,self_collision=own,unintended_tray_collision=bad[:2],intended_tip_contact_hulls=tips))
 # Full-size tray/aperture negative control: a200mm-wide aperture cannot pass270mm tray.
 cylinder=fcl.CollisionObject(fcl.Cylinder(.135,.005),fcl.Transform(np.eye(3),origin+[0,0,.0145]));wall=fcl.CollisionObject(fcl.Box(.40,.01,.24),fcl.Transform(np.eye(3),origin+[0,.10,.12]));rr=fcl.CollisionResult();fcl.collide(cylinder,wall,fcl.CollisionRequest(),rr)
 return dict(door_angle_deg=angle,samples=samples,summary=dict(sampled_poses=len(samples),payload_collision_poses=sum(bool(z['payload_obstacle_hits']) for z in samples),obstacle_collision_poses=sum(z['obstacle_collision'] is not None for z in samples),self_collision_poses=sum(z['self_collision'] is not None for z in samples),unintended_tray_collision_poses=sum(bool(z['unintended_tray_collision']) for z in samples)),undersized_aperture_negative_detected=rr.is_collision)
results=[run(90),run(110)]
out=dict(scope='Actual stock YAM geometry on explicitly representative apparatus dimensions; sampled kinematic hypothesis only',robot_hulls_per_arm=len(A.r.hulls),total_hulls=2*len(A.r.hulls),ik=ik,keyframes=[dict(label=k,left=l.tolist(),right=r.tolist(),tray_center_m=c.tolist()) for k,l,r,c in keys],cases=results,not_demonstrated=['No dynamic acquisition or weight-bearing pinch proof','No actualToshiba scale/door geometry validated','No continuous collision certificate between samples','No complete ready-to-pregrasp motion','Held-tray relationship is a planning hypothesis, never a simulator weld'],source_body_pin=A.r.data['pin'])
(D/'results/YAM_ACCESS.json').write_text(json.dumps(out,indent=2,default=lambda v:v.item() if isinstance(v,np.generic) else str(v))+'\n')
print(json.dumps({'IK_unresolved':sum(not z['valid'] for z in ik),'cases':[z['summary'] for z in results]},indent=2))
