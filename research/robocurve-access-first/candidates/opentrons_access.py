"""Manufacturer-dimensioned roof-region reach survey, NOT socket/grasp poses.
The lamp/socket/clip dimensions and registered positions remain unavailable, so
this test cannot instantiate an accepted complete hardware manipulation scene.
"""
from pathlib import Path
import sys,json
sys.path.insert(0,'/workspace/robocurve-cpu-deps')
D=Path(__file__).resolve().parent;R=D.parents[2]
sys.path.insert(0,str(R/'research/robocurve-implementation'))
import numpy as np,fcl
from scipy.spatial.transform import Rotation
from common.access import Access
sys.path.insert(0,str(D.parent/"odri"))
from support_gate import evaluate,ob
A=Access();S=D.parent/'sources/opentrons'
text=(S/'flex-specs.md').read_text();installation=(S/'hepa-installation.md').read_text();spec=(S/'hepa-product-specs.md').read_text()
assert '87 × 69 × 84 cm' in text and '87 cm L x 64 cm W x 14 cm H' in spec
assert 'underside' in installation and 'gantry' in installation
# A same-bench front-facing workcell is an authored placement; device dimensions
# and installed-on-Flex sequence are manufacturer facts. No low detached bay.
table=[('table',ob(fcl.Box(1.1,1.3,.06),np.eye(3),[.36,0,.7175]))]
RT=np.array([[0,0,1],[0,-1,0],[1,0,0]],float)
rotations=[('horizontal-front',RT),('horizontal-side',Rotation.from_euler('z',np.pi/2).as_matrix()@RT),('upward',np.eye(3))]
rows=[]
for bench in [.7475,.90]:
 roof=bench+.84
 # Optimistic14cm band BELOW the roof, broader than a located lamp interface.
 # This is a bounded region survey, not a fabricated socket location.
 for x in [.20,.545,.89]:
  for y in [-.30,0,.30]:
   for z in [roof-.14,roof]:
    point=np.array([x,y,z])
    for side in ['left','right']:
     distance=float(np.linalg.norm(point-A.r.base_poses[side][:3,3]))
     for label,rot in rotations:
      if distance>A.r.necessary_tcp_radius():
       row=dict(bench_m=bench,point_m=point.tolist(),side=side,orientation=label,status='OUTSIDE NECESSARY TCP SPHERE',distance_m=distance)
      else:
       q,e=A.ik(point,rot,side=side,gap=.04)
       collision=evaluate(q,A.qready,table,np.zeros(3)) if side=='left' else evaluate(A.qready,q,table,np.zeros(3))
       row=dict(bench_m=bench,point_m=point.tolist(),side=side,orientation=label,status='IK SOLVED' if e['valid'] else 'IK UNRESOLVED',IK=e,known_geometry_collision_check=collision,q=q.tolist())
      rows.append(row)
 summary={k:sum(r['status']==k for r in rows) for k in ['OUTSIDE NECESSARY TCP SPHERE','IK SOLVED','IK UNRESOLVED']}
 out=dict(name='Opentrons Flex HEPA/UV two-interface lamp installation',source_dimensions=dict(Flex_m=[.87,.69,.84],module_m=[.87,.64,.14]),roof_on_standard_bench_m=.7475+.84,
  scope='Optimistic free-space point region below a source-sized installed roof; not manufacturer socket anchors. Both stock arms, their interaction and nonadjacent self pairs are checked against the known table; full enclosure/gantry, lamp, socket and clip geometry are not supplied.',
  survey_summary=summary,cases=rows,hulls_per_arm=len(A.r.hulls),
  missing=['matched bulb/base geometry','four pin/socket channel sections and insertion direction/location','remote clip throat and retention geometry','registered full Flex/gantry/lamp-bay corridor'],
  access_gate='REJECT FROM IMPLEMENTATION SELECTION: no complete source geometry/purchase/path',complete_access=False,physical_purchase='NOT PROVEN',continuous_certificate='NOT RUN')
 (D/'results/OPENTRONS_ACCESS.json').write_text(json.dumps(out,indent=2,default=lambda v:v.item() if isinstance(v,np.generic) else str(v))+'\n')
 print(bench,summary,flush=True)
