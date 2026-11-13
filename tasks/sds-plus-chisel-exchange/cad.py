"""Original convex CAD; exact same authored solids go to USD, QA and MuJoCo."""
import math
import numpy as np
from scipy.spatial import ConvexHull
try:
 from .primitives import box,cylinder,body
except ImportError:
 from primitives import box,cylinder,body

STEEL=[.46,.49,.52]
def convex(points,color=STEEL,role='contact'):
 p=np.unique(np.round(points,12),axis=0);lo=p.min(0);hi=p.max(0);center=(lo+hi)/2;p=p-center;h=ConvexHull(p);faces=[]
 for f,n in zip(h.simplices,h.equations):
  f=list(map(int,f));v=p[f]
  if np.dot(np.cross(v[1]-v[0],v[2]-v[0]),n[:3])<0:f[1],f[2]=f[2],f[1]
  faces.append(f)
 return dict(kind='convex',pos=center.tolist(),quat=[0,0,0,1],vertices=p.tolist(),faces=faces,size=(hi-lo).tolist(),color=color,role=role)

def annular_slice(x0,x1,inner0,inner1,outer,count=64,skip=None,color=STEEL,role='sleeve'):
 shapes=[]
 for i in range(count):
  a=2*math.pi*i/count;b=2*math.pi*(i+1)/count;mid=(a+b)/2
  if skip and skip(mid):continue
  points=[]
  for x,inner in [(x0,inner0),(x1,inner1)]:
   # Circumscribed inner polygon guarantees stated minimum bore clearance.
   for r in [inner/math.cos(math.pi/count),outer]:
    for t in [a,b]:points.append([x,r*math.cos(t),r*math.sin(t)])
  shapes.append(convex(points,color,role))
 return shapes

def shank():
 import dimensions as D
 xs=[-.045,-.040,D.SLOT_REAR,D.SLOT_FLOOR_REAR,D.SLOT_FLOOR_FRONT,D.SLOT_FRONT,-.004,0.]
 count=64;shapes=[]
 def slot_r(x):
  if x<=D.SLOT_REAR or x>=D.SLOT_FRONT:return D.SHAFT_RADIUS
  if x<D.SLOT_FLOOR_REAR:return D.SHAFT_RADIUS+(D.SLOT_RADIUS-D.SHAFT_RADIUS)*(x-D.SLOT_REAR)/(D.SLOT_FLOOR_REAR-D.SLOT_REAR)
  if x>D.SLOT_FLOOR_FRONT:return D.SLOT_RADIUS+(D.SHAFT_RADIUS-D.SLOT_RADIUS)*(x-D.SLOT_FLOOR_FRONT)/(D.SLOT_FRONT-D.SLOT_FLOOR_FRONT)
  return D.SLOT_RADIUS
 for x0,x1 in zip(xs,xs[1:]):
  for i in range(count):
   a=2*math.pi*i/count;b=2*math.pi*(i+1)/count;mid=(a+b)/2
   drive=abs(math.sin(mid))<.232
   retention=abs(math.cos(mid))<.455
   def radius(x):
    r=D.SHAFT_RADIUS
    if drive and x>=-.040:r=D.OPEN_GROOVE_RADIUS
    if retention:r=min(r,slot_r(x))
    if x>-.004:r=min(r,D.SHAFT_RADIUS-.001*(x+.004)/.004)
    return r
   points=[]
   for x in [x0,x1]:
    r=radius(x);points.extend([[x,0,0],[x,r*math.cos(a),r*math.sin(a)],[x,r*math.cos(b),r*math.sin(b)]])
   shapes.append(convex(points,role='drive_groove' if drive else 'closed_retention_groove' if retention else 'shank'))
 return shapes

def faceted_ball(radius,subdivisions=2):
 t=(1+math.sqrt(5))/2;v=np.array([[-1,t,0],[1,t,0],[-1,-t,0],[1,-t,0],[0,-1,t],[0,1,t],[0,-1,-t],[0,1,-t],[t,0,-1],[t,0,1],[-t,0,-1],[-t,0,1]],float);v/=np.linalg.norm(v,axis=1)[:,None]
 for _ in range(subdivisions):
  h=ConvexHull(v);edges={tuple(sorted((int(f[i]),int(f[(i+1)%3])))) for f in h.simplices for i in range(3)};mid=np.array([v[i]+v[j] for i,j in sorted(edges)]);mid/=np.linalg.norm(mid,axis=1)[:,None];v=np.concatenate([v,mid])
 return convex(v*radius,[.68,.70,.72],'original_faceted_7mm_ball')
