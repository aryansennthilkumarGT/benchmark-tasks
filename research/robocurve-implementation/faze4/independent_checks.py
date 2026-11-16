"""Independent one-dimensional ring fits and physically inspectable negative states."""
from pathlib import Path
import sys,json,hashlib
sys.path.insert(0,'/workspace/robocurve-cpu-deps')
import numpy as np
from scipy.optimize import minimize_scalar,differential_evolution
from shapely.geometry import Polygon,Point
D=Path(__file__).resolve().parent;x=json.loads((D/'results/CLOSURE_GATE.json').read_text());sections=json.loads((D/'results/SOURCE_SECTIONS.json').read_text())
v=np.array(sections['11_1 cyclo disc.STL'][0]['loops'][0]['points_mm'])-[29.6014582285,28.7667403992]
ring=np.array(x['ring_centres_mm']);cp=np.array(x['carrier_centres_mm']);hole=np.array([[-18.0700738096079,5.871322893124],[-11.167919793557,-15.371322893124],[11.167919793557,-15.371322893124],[18.0700738096079,5.871322893124],[0,19.]])
def R(a):return np.array([[np.cos(a),-np.sin(a)],[np.sin(a),np.cos(a)]])
fits=[]
for side in [-1,1]:
 c=np.array([0,side*x['eccentricity_mm']])
 def gap(a):
  p=Polygon(v@R(a).T+c);return np.array([p.distance(Point(k))-4 for k in ring])
 grid=np.linspace(-np.pi,np.pi,2201);cost=np.array([np.minimum(gap(a),0)@np.minimum(gap(a),0) for a in grid]);local=[i for i in range(len(grid)-1) if cost[i]<=cost[(i-1)%(len(grid)-1)] and cost[i]<=cost[(i+1)%(len(grid)-1)]]
 f=[]
 for i in local:
  o=minimize_scalar(lambda a:float(np.minimum(gap(a),0)@np.minimum(gap(a),0)),bounds=(grid[i]-(grid[1]-grid[0]),grid[i]+(grid[1]-grid[0])),method='bounded',options={'xatol':1e-12});f.append(dict(angle_rad=float(o.x),worst_ring_gap_mm=float(gap(o.x).min()),penalty_mm2=float(o.fun)))
 fits.append(dict(eccentric_side=side,ring_only_minima=f))
# All combinations of independently ring-fitted orientations. Find best shared
# carrier angle without imposing an output ratio or forcing hole engagement.
allfits=[]
for a in fits[0]['ring_only_minima']:
 for b in fits[1]['ring_only_minima']:
  hh=[hole@R(a['angle_rad']).T+[0,-x['eccentricity_mm']],hole@R(b['angle_rad']).T+[0,x['eccentricity_mm']]]
  def minimum(phi):
   p=cp@R(phi).T
   return min(float((5.50302933333333-4-np.linalg.norm(p[:,None,:]-h[None,:,:],axis=2).min(1)).min()) for h in hh)
  # whole output range over one fivefold repeat, then locally refine max clearance
  grid=np.linspace(-np.pi/5,np.pi/5,1441);vals=np.array([minimum(z) for z in grid]);i=int(np.argmax(vals));lo=grid[max(0,i-1)];hi=grid[min(len(grid)-1,i+1)]
  z=minimize_scalar(lambda q:-minimum(q),bounds=(lo,hi),method='bounded',options={'xatol':1e-12})
  allfits.append(dict(lower_angle_rad=a['angle_rad'],upper_angle_rad=b['angle_rad'],carrier_angle_rad=float(z.x),minimum_hole_clearance_mm=float(-z.fun)))
best=max(allfits,key=lambda a:a['minimum_hole_clearance_mm'])
# Actual source mesh case/cover check; aligned central axes, no invented slots.
import trimesh,fcl
sys.path.insert(0,str(D.parents[0]));from common.access import mesh
S=D.parents[2]/'research/robocurve-final-discovery/agents/robot_build/evidence/faze4/STL_V2/STL_V2/STL/Elbow/J4 cyclo'
case=trimesh.load_mesh(S/'Joint 4 motor case.STL');cover=trimesh.load_mesh(S/'Joint 4 top cover.STL');casegeom=mesh(case.vertices*.001,case.faces);covergeom=mesh(cover.vertices*.001,cover.faces)
coverchecks=[]
for z in [25.,24.]:
 a=fcl.CollisionObject(casegeom);b=fcl.CollisionObject(covergeom,fcl.Transform(np.eye(3),np.array([38.5-45.005,38.5-40.001,z])*.001));res=fcl.CollisionResult();fcl.collide(a,b,fcl.CollisionRequest(num_max_contacts=100,enable_contact=True),res)
 coverchecks.append(dict(cover_lower_face_z_mm=z,triangle_contact_count=len(res.contacts),maximum_contact_depth_mm=max([c.penetration_depth*1000 for c in res.contacts],default=0),interior_z_overlap_mm=max(0.,25-z),fcl_depth_warning='Triangle contact depth at coplanar mesh faces is NOT solid penetration; nominalz25 has disjointinteriors byZ bounds',source_axis_registration='central mesh axes only; screw-axis compatibility not yet proved'))
# Negative states are actual point/profile sets, not preassigned engaged flags.
neg=[]
base0=np.array(x['best']['angles_rad']);F=x['best']['upper_mirror_x']
for name in ['nominal','missing_disk','missing_roller_pair','carrier_one_plane_only','wrong_upper_phase_5deg']:
 angles=base0[:2].copy()
 if name=='wrong_upper_phase_5deg':angles[1]+=np.deg2rad(5)
 active=[0] if name=='missing_disk' else [0,1]
 points=cp[:4] if name=='missing_roller_pair' else cp
 points=points@R(base0[2]).T
 if name=='carrier_one_plane_only':points=hole@R(angles[0]).T+[0,-x['eccentricity_mm']]
 observed=[];allgaps=[]
 for j in active:
  mir=np.diag([1 if j==0 else F,1]);center=np.array([0,(-1 if j==0 else 1)*x['eccentricity_mm']]);poly=Polygon(v@mir@R(angles[j]).T+center);hh=hole@mir@R(angles[j]).T+center
  hg=5.50302933333333-4-np.linalg.norm(points[:,None,:]-hh[None,:,:],axis=2).min(1)
  rg=np.array([poly.distance(Point(k))-4 for k in ring]);allgaps.extend(hg);allgaps.extend(rg)
  observed.append(dict(disk_index=j,output_centres_inside_holes=int(sum(hg>=-.00001)),minimum_hole_gap_mm=float(hg.min()),minimum_ring_gap_mm=float(rg.min())))
 mingap=min(allgaps);inventory=len(active)==2 and len(points)==5;contact=mingap>=-.05
 neg.append(dict(case=name,visible_disk_count=len(active),visible_output_pair_count=len(points),measured_layers=observed,minimum_clearance_mm=float(mingap),physical_inventory_gate=inventory,contact_gate_pass=contact,full_planar_gate=inventory and contact,proposed_mesh_guard_mm=.05))
out=dict(independent_ring_fits=fits,number_of_ring_phase_pairs=len(allfits),best_shared_carrier_at_ring_fits=best,cover_checks=coverchecks,negative_states=neg,phase_controls=x['negative_controls'],decision='STOP FAZE4: no demonstrated nominal source closure; numerical11:1-like motion under penalty penetration does not validate assembly',scope='Finite mesh/analytic registration screen; not a global theorem or material-deflection model',not_executed=['ActualYAMinsertion: nominalsourceclosurefailed first','Dynamicbearing/force validation','Completeaxialstackandcoverfastenerregistration'])
(D/'results/INDEPENDENT_CHECKS.json').write_text(json.dumps(out,indent=2,default=lambda v:v.item() if isinstance(v,np.generic) else str(v))+'\n');print(json.dumps(dict(best_carrier_gap_mm=best['minimum_hole_clearance_mm'],phase_pairs=len(allfits),cover=coverchecks),indent=2))
