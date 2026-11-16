"""Full source YAM FK/IK and CPU FCL collision checks; no ideal point hands."""
from pathlib import Path
import sys
sys.path.insert(0,'/workspace/robocurve-cpu-deps')
import numpy as np
import fcl
from scipy.spatial import ConvexHull
from scipy.optimize import least_squares
from scipy.spatial.transform import Rotation
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'research/robocurve-acceptance/preflight'))
from access_core import Robot,points_at,transform

def convex(v):
 h=ConvexHull(v);f=h.simplices.copy()
 for k,t in enumerate(f):
  if np.dot(np.cross(v[t[1]]-v[t[0]],v[t[2]]-v[t[0]]),h.equations[k,:3])<0:f[k]=t[[0,2,1]]
 return fcl.Convex(np.asarray(v,float),len(f),np.c_[np.full(len(f),3),f].astype(np.int32).ravel())
def mesh(v,f):
 m=fcl.BVHModel();m.beginModel(len(v),len(f));m.addSubModel(v,f);m.endModel();return m
class Access:
 def __init__(self):
  self.r=Robot();self.geoms=[convex(h['vertices']) for h in self.r.hulls]
  self.qready=np.array(self.r.data['ready_joint_radians']+[-.04695,-.04695]);self.objs=[];self.names={}
 def set_obstacles(self,entries):
  self.objs=[];self.names={};self.labels=[]
  for name,geom,R,t in entries:
   o=fcl.CollisionObject(geom,fcl.Transform(R,t));self.objs.append(o);self.labels.append(name);self.names[id(geom)]=name
  self.manager=fcl.DynamicAABBTreeCollisionManager();self.manager.registerObjects(self.objs);self.manager.setup()
 def ik(self,pos,rot,side='left',seed=None,gap=.008):
  lo=np.array([self.r.by_name['joint'+str(i)]['lower'] for i in range(1,7)]);hi=np.array([self.r.by_name['joint'+str(i)]['upper'] for i in range(1,7)])
  seeds=[np.clip(np.array(seed if seed is not None else self.qready)[:6],lo+1e-8,hi-1e-8),np.array([0,1.4,1.8,-1.2,0,0]),np.array([-.5,1.,1.5,-.8,.5,.5])]
  best=None
  for x in seeds:
   def err(z):
    q=np.r_[z,-gap/2,-gap/2];P=self.r.fk(q,side)[0]['gripper'];p=(P@np.array([0,0,.134,1]))[:3]
    return np.r_[(p-pos)*5,Rotation.from_matrix(rot@P[:3,:3].T).as_rotvec()]
   fit=least_squares(err,np.clip(x,lo+1e-8,hi-1e-8),bounds=(lo,hi),max_nfev=100,ftol=1e-8,xtol=1e-8,gtol=1e-8)
   e=err(fit.x);rank=np.linalg.norm(e)
   if best is None or rank<best[0]:best=(rank,np.r_[fit.x,-gap/2,-gap/2],float(np.linalg.norm(e[:3])/5),float(np.linalg.norm(e[3:])))
   if best[2]<.001 and best[3]<.02:break
  return best[1],dict(position_error_mm=1000*best[2],orientation_error_deg=np.rad2deg(best[3]),valid=best[2]<.001 and best[3]<.02)
 def collision(self,left,right=None,tool=None):
  hits=[]
  for side,q in [('left',left),('right',self.qready if right is None else right)]:
   poses=self.r.fk(q,side)[0]
   for h,g in zip(self.r.hulls,self.geoms):
    P=poses[h['link']];o=fcl.CollisionObject(g,fcl.Transform(P[:3,:3],P[:3,3]));data=fcl.CollisionData(request=fcl.CollisionRequest(num_max_contacts=1,enable_contact=True))
    self.manager.collide(o,data,fcl.defaultCollisionCallback)
    if data.result.is_collision:
     contact=data.result.contacts[0];other=contact.o1 if contact.o1 is not g else contact.o2
     label='unresolved'
     for label,obs in zip(self.labels,self.objs):
      rr=fcl.CollisionResult()
      if fcl.collide(o,obs,fcl.CollisionRequest(),rr):break
     hits.append({'side':side,'link':h['link'],'hull':h['name'],'obstacle':label,'penetration_mm':float(contact.penetration_depth*1000)})
     return hits
  if tool:
   poses=self.r.fk(left,'left')[0];G=poses['gripper']
   for name,geom,local in tool:
    T=G@local;o=fcl.CollisionObject(geom,fcl.Transform(T[:3,:3],T[:3,3]));data=fcl.CollisionData(request=fcl.CollisionRequest(num_max_contacts=1,enable_contact=True));self.manager.collide(o,data,fcl.defaultCollisionCallback)
    if data.result.is_collision:return [{'side':'tool','link':name,'obstacle':'source-or-fixture'}]
  return []
 def sample_path(self,keys,tool=None):
  count=0
  for k in range(len(keys)-1):
   a,b=keys[k],keys[k+1]
   for u in np.linspace(0,1,13):
    q=(1-u)*a+u*b;count+=1;hits=self.collision(q,tool=tool)
    if hits:return dict(clear=False,segment=k,fraction=float(u),sampled_poses=count,first_collision=hits[0])
  return dict(clear=True,sampled_poses=count,scope='Sampled path only; no swept or contact/grasp certificate')
