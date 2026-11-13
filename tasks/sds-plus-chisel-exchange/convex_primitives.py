"""Original convex extrusions, with explicit faces and conservative bounds."""
from motion import rotate


def hull2(points):
 points=sorted(set((float(x),float(y)) for x,y in points))
 def cross(o,a,b):return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
 lower=[];upper=[]
 for p in points:
  while len(lower)>1 and cross(lower[-2],lower[-1],p)<=0:lower.pop()
  lower.append(p)
 for p in reversed(points):
  while len(upper)>1 and cross(upper[-2],upper[-1],p)<=0:upper.pop()
  upper.append(p)
 return lower[:-1]+upper[:-1]


def prism_x(points,width,pos=(0,0,0),q=(0,0,0,1),color=(.48,.5,.52)):
 polygon=hull2(points);n=len(polygon)
 if n<3 or width<=0:raise ValueError('Nondegenerate convex prism required')
 ys=[p[0] for p in polygon];zs=[p[1] for p in polygon];center=[0,(min(ys)+max(ys))/2,(min(zs)+max(zs))/2]
 vertices=[[x,y-center[1],z-center[2]] for x in (-width/2,width/2) for y,z in polygon]
 # Polygon ordering is CCW in YZ, hence +X is its outward normal.
 faces=[list(reversed(range(n))),list(range(n,2*n))]+[[i,(i+1)%n,(i+1)%n+n,i+n] for i in range(n)]
 worldcenter=rotate(q,center)+pos
 return dict(kind='convex',pos=worldcenter.tolist(),quat=list(q),vertices=vertices,faces=faces,
             size=[width,max(ys)-min(ys),max(zs)-min(zs)],color=list(color))
