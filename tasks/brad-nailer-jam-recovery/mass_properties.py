"""Authored density-weighted compound approximation, not measured hardware.

Primitive overlaps are counted; a common scale matches the separately authored
body mass. This is not a CAD boolean-union integral or manufacturer mass tensor.
Convex profiles use signed tetrahedral volume/moment integration.
"""
import math
import numpy as np
from motion import rotate


def primitive(shape):
 kind=shape['kind']
 if kind=='box':
  size=np.asarray(shape['size'],dtype=float);volume=float(np.prod(size));center=np.zeros(3);cov=np.diag(size*size/12)
 elif kind=='cylinder':
  r,h=shape['radius'],shape['height'];volume=math.pi*r*r*h;center=np.zeros(3);cov=np.diag([r*r/4,r*r/4,h*h/12])
 elif kind=='convex':
  vertices=np.asarray(shape['vertices'],dtype=float);volume=0.;first=np.zeros(3);second=np.zeros((3,3))
  for face in shape['faces']:
   for j in range(1,len(face)-1):
    a,b,c=vertices[[face[0],face[j],face[j+1]]];v=float(np.dot(a,np.cross(b,c)))/6
    total=a+b+c;volume+=v;first+=v*total/4
    second+=v*(np.outer(a,a)+np.outer(b,b)+np.outer(c,c)+np.outer(total,total))/20
  if abs(volume)<1e-15:raise ValueError('Degenerate closed convex profile')
  center=first/volume;cov=second/volume-np.outer(center,center);volume=abs(volume)
 else:raise ValueError('Unsupported mass geometry: '+kind)
 if not volume>0 or np.linalg.eigvalsh(cov).min()<-1e-12:raise ValueError('Invalid volume moments')
 rotation=np.column_stack([rotate(shape.get('quat',[0,0,0,1]),v) for v in np.eye(3)])
 return volume,np.asarray(shape['pos'])+rotation@center,rotation@cov@rotation.T


def compound(shapes,total_mass):
 from yam_arena.ik import matrix_to_quat_xyzw
 if not math.isfinite(total_mass) or total_mass<=0:raise ValueError('Positive authored mass required')
 parts=[]
 for shape in shapes:
  density=shape.get('mass_density')
  if not isinstance(density,(int,float)) or not math.isfinite(density) or density<=0:raise ValueError('Explicit authored density required')
  volume,center,cov=primitive(shape);parts.append((density*volume,center,cov))
 raw=sum(m for m,_,_ in parts);center=sum(m*c for m,c,_ in parts)/raw
 covariance=sum(m*(cov+np.outer(c-center,c-center)) for m,c,cov in parts)/raw
 tensor=total_mass*(np.trace(covariance)*np.eye(3)-covariance)
 diagonal,axes=np.linalg.eigh(tensor)
 if diagonal.min()<=0 or diagonal.max()>diagonal.sum()-diagonal.max()+1e-10:raise ValueError('Nonphysical inertia tensor')
 if np.linalg.det(axes)<0:axes[:,0]*=-1
 q=matrix_to_quat_xyzw(axes)
 if q[3]<0:q=-q
 clean=lambda v:[float(round(float(x),14)) for x in v]
 return dict(center_of_mass=clean(center),diagonal_inertia=clean(diagonal),principal_axes=clean(q),
             nominal_component_mass_kg=float(raw),density_normalization=float(total_mass/raw),
             inertia_model='Authored density-weighted compound volumes with overlaps counted; normalized to authored total mass; not measured hardware or exact boolean CAD.')
