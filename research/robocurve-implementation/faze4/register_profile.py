"""Actual J4 CAD profiles and fit falsification, never a scripted ratio joint."""
from pathlib import Path
import sys,json,hashlib
sys.path.insert(0,'/workspace/robocurve-cpu-deps')
import numpy as np,trimesh
from shapely.geometry import Polygon,Point
from shapely import affinity
from scipy.optimize import differential_evolution,minimize
D=Path(__file__).resolve().parent;R=D.parents[2]
S=R/'research/robocurve-final-discovery/agents/robot_build/evidence/faze4/STL_V2/STL_V2/STL/Elbow/J4 cyclo'
meshes={n:trimesh.load_mesh(S/n,process=True) for n in ['11_1 cyclo disc.STL','Joint 4 motor case.STL','Joint 4 Output shaft.STL','Eccentric shaft J4.STL','Joint 4 top cover.STL']}
profiles={}
for name,m in meshes.items():
 slices=[]
 for z in np.linspace(m.bounds[0,2]+.1,m.bounds[1,2]-.1,8):
  sec=m.section(plane_origin=[0,0,z],plane_normal=[0,0,1])
  if sec is None:continue
  loops=sec.discrete
  polys=[]
  for loop in loops:
   p=Polygon(loop[:,:2]);polys.append({'area_mm2':p.area,'center_mm':list(p.centroid.coords)[0],'bounds_mm':p.bounds,'points_mm':loop[:,:2].tolist()})
  slices.append(dict(z_mm=z,loops=sorted(polys,key=lambda p:-p['area_mm2'])))
 profiles[name]=slices
(D/'results/SOURCE_SECTIONS.json').write_text(json.dumps(profiles,indent=2)+'\n')
print('Actual section counts',{k:[len(z['loops']) for z in v] for k,v in profiles.items()})
# Start from actual STEP/STL bearing centre and exact mesh outer profile.
p0=np.array([29.6014582285,28.7667403992]);disk=Polygon(profiles['11_1 cyclo disc.STL'][0]['loops'][0]['points_mm']);disk=affinity.translate(disk,-p0[0],-p0[1])
# Derive ring screw centres from section loops, rather than assuming a circle from a picture.
for sl in profiles['Joint 4 motor case.STL']:
 small=[x for x in sl['loops'][1:] if 2<x['area_mm2']<20];print('case z',sl['z_mm'],'small',[(round(x['area_mm2'],2),np.round(x['center_mm'],3).tolist()) for x in small])
