"""Rigid source-profile registration with unilateral roller/hole clearance tests."""
from pathlib import Path
import sys,json
sys.path.insert(0,'/workspace/robocurve-cpu-deps')
import numpy as np
from scipy.optimize import differential_evolution,minimize
from shapely.geometry import Polygon,Point
from shapely import affinity
D=Path(__file__).resolve().parent
S=json.loads((D/'results/SOURCE_SECTIONS.json').read_text())
P=np.array([29.6014582285,28.7667403992])
base=np.array(S['11_1 cyclo disc.STL'][0]['loops'][0]['points_mm'])-P
casecenter=np.array([38.5,38.5])
# Source through-holes on32mm pitch circle; filter actual case holes by that radius.
ring=np.array([x['center_mm'] for x in S['Joint 4 motor case.STL'][0]['loops'][1:] if abs(np.linalg.norm(np.array(x['center_mm'])-casecenter)-32)<.03])-casecenter
assert len(ring)==12
h=np.array([[-18.0700738096079,7.37435222645733],[-11.167919793557,-13.86829355979066],[11.167919793557,-13.86829355979066],[18.0700738096079,7.37435222645733],[0,20.503029333333348]])-np.array([0,1.503029333333335])
# Carrier centres extracted directly from actual top section, radius19 from its realaxis.
carrier=np.array([x['center_mm'] for x in S['Joint 4 Output shaft.STL'][-1]['loops'][1:] if abs(np.linalg.norm(np.array(x['center_mm'])-[23,23])-19)<.03])-[23,23]
assert len(carrier)==5
hole_room=5.50302933333333-4
casecavity=Polygon(S['Joint 4 motor case.STL'][4]['loops'][1]['points_mm']);casecavity=affinity.translate(casecavity,-38.5,-38.5)
def rot(a):return np.array([[np.cos(a),-np.sin(a)],[np.sin(a),np.cos(a)]])
def gaps(q,theta,flip):
 R0=rot(q[0]);R1=rot(q[1]);cp=carrier@rot(q[2]).T;vec=rot(theta)@np.array([0,1.499962]);centers=[-vec,vec];out=[]
 for j,R in enumerate([R0,R1]):
  F=np.diag([flip if j else 1,1]);poly=Polygon(base@F@R.T+centers[j]);holes=h@F@R.T+centers[j]
  rr=np.array([poly.distance(Point(c))-4 for c in ring]);hh=hole_room-np.linalg.norm(cp[:,None,:]-holes[None,:,:],axis=2).min(1)
  # Case outside area is a diagnostic, not an invented locking constraint.
  out.extend(rr);out.extend(hh)
 return np.array(out)
fits=[]
for flip in [1,-1]:
 def cost(q):
  g=gaps(q,0,flip);bad=np.minimum(g,0);return float(np.dot(bad,bad))
 opt=differential_evolution(cost,[(-np.pi,np.pi)]*3,popsize=12,maxiter=220,seed=7,tol=1e-8,polish=True)
 gs=gaps(opt.x,0,flip);fits.append(dict(upper_mirror_x=flip,angles_rad=opt.x.tolist(),penalty_mm2=float(opt.fun),worst_gap_mm=float(gs.min()),negative_constraints=int(sum(gs<-.01))))
 print('fit',fits[-1],flush=True)
best=min(fits,key=lambda f:f['penalty_mm2']);q=np.array(best['angles_rad']);flip=best['upper_mirror_x'];sweep=[]
# Do not constrain output to a ratio. At each input angle, solve contact feasibility
# using only actual ring/hole geometry and continuity regularization.
for theta in np.linspace(0,2*np.pi,73):
 prior=q.copy()
 def cost(x):
  g=gaps(x,theta,flip);bad=np.minimum(g,0);return float(bad@bad+1e-8*np.sum((x-prior)**2))
 opt=minimize(cost,q,method='Powell',bounds=[(v-.15,v+.15) for v in q],options={'maxiter':80,'xtol':1e-8,'ftol':1e-12});q=opt.x;gs=gaps(q,theta,flip)
 sweep.append(dict(input_deg=float(np.rad2deg(theta)),angles_rad=q.tolist(),minimum_clearance_mm=float(gs.min())))
print('sweep min',min(x['minimum_clearance_mm'] for x in sweep),'derived output deg',np.rad2deg(q[2]-best['angles_rad'][2]),flush=True)
controls=[]
q0=np.array(best['angles_rad'])
for name,delta in [('nominal',0),('wrong_upper_phase_5deg',np.deg2rad(5)),('wrong_upper_phase_20deg',np.deg2rad(20))]:
 qq=q0.copy();qq[1]+=delta;gs=gaps(qq,0,flip);controls.append(dict(case=name,minimum_gap_mm=float(gs.min()),interfering_constraints=int(sum(gs<-.01))))
result=dict(source='Exact published STL section profiles; bearing/hole centres from originalSTEP and actualcase/carrier loop extraction',ring_centres_mm=ring.tolist(),carrier_centres_mm=carrier.tolist(),eccentricity_mm=1.499962,output_bearing_radius_mm=4,hole_radius_mm=5.50302933333333,fits=fits,best=best,sweep=sweep,negative_controls=controls,limitations=['Nominal 2D contact feasibility only, not material-force/3Dclosure/YAM proof','No forced gear-ratio joint; measured output follows optimization, not a prescribedratio','A failed nominal closure is not repaired by enlargingholes or deletingrollers'])
(D/'results/CLOSURE_GATE.json').write_text(json.dumps(result,indent=2)+'\n')
