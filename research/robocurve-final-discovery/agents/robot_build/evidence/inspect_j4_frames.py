"""Inspect print-oriented source STL circle frames; no mating transform/fit pass."""
from pathlib import Path
import json, struct
import numpy as np
D=Path(__file__).resolve().parent/'faze4'
def points(p):
 b=p.read_bytes();n=struct.unpack('<I',b[80:84])[0];dt=np.dtype([('n','<f4',(3,)),('v','<f4',(3,3)),('a','<u2')]);return np.unique(np.frombuffer(b[84:],dtype=dt,count=n)['v'].reshape(-1,3),axis=0)
def circles(xy,r):
 rng=np.random.default_rng(17);found=[]
 for _ in range(10000):
  a,b=xy[rng.integers(len(xy),size=2)];v=b-a;l=np.linalg.norm(v)
  if l<r/2 or l>2*r:continue
  mid=(a+b)/2;perp=np.array([-v[1],v[0]])/l
  for center in [mid+perp*np.sqrt(max(0.0,r*r-l*l/4)),mid-perp*np.sqrt(max(0.0,r*r-l*l/4))]:
   ix=np.abs(np.linalg.norm(xy-center,axis=1)-r)<0.012
   if sum(ix)<12:continue
   # algebraic least squares gives actual STL radius, independent of nominated value
   q=xy[ix];m=np.c_[2*q[:,0],2*q[:,1],np.ones(len(q))];coef=np.linalg.lstsq(m,(q*q).sum(1),rcond=None)[0];cc=coef[:2];rr=np.sqrt(coef[2]+sum(cc*cc))
   if abs(rr-r)>.02 or any(np.linalg.norm(cc-np.array(c['center_xy_mm']))<.1 for c in found):continue
   found.append(dict(center_xy_mm=cc.tolist(),radius_mm=float(rr),inlier_vertices=int(sum(ix))))
 return sorted(found,key=lambda a:a['center_xy_mm'])
out=[]
for name,radii in [('Eccentric shaft J4.STL',[8.5]),('11_1 cyclo disc.STL',[5.503029333,11.54]),('Joint 4 Output shaft.STL',[1.5,1.6]),('Joint 4 motor case.STL',[1.5,1.6])]:
 p=next(x for x in (D/'STL_V2').rglob(name) if '/J4 cyclo/' in str(x));v=points(p);xy=np.unique(v[:,:2],axis=0)
 out.append(dict(path=str(p.relative_to(D)),vertices=len(v),z_levels=np.unique(np.round(v[:,2],4)).tolist(),circles=[dict(nominated_radius_mm=r,features=circles(xy,r)) for r in radii]))
(D/'print-frame-circles.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2)[:15000])
