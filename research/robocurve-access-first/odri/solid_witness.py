"""A strict analytic-solid intrusion witness, beyond triangle-contact depth."""
from pathlib import Path
import sys,json
sys.path.insert(0,'/workspace/robocurve-cpu-deps')
D=Path(__file__).resolve().parent;R=D.parents[2]
sys.path.insert(0,str(R/'research/robocurve-next-prototype/odri'))
from sections import S
import cadquery as cq
s=cq.importers.importStep(str(S/'lower_leg_structure_base.STEP')).val().translate((0,0,160))
boundary=cq.Compound.makeCompound(s.Faces())
x=json.loads((D/'results/ROOT_CAUSE.json').read_text());out=[]
for h in x['cases'][0]['base_collisions']:
 points=h['source_base_contains_robot_hull_vertices_mm'];witness=None
 for p in points[:20]:
  distance=boundary.distance(cq.Vertex.makeVertex(*p))
  if distance>.001 and s.isInside(cq.Vector(*p),1e-7):witness=dict(point_mm=p,distance_to_any_STEP_boundary_mm=distance);break
 out.append(dict(hull=h['hull'],link=h['link'],strict_inside_witness=witness));print(out[-1],flush=True)
assert out and all(r['strict_inside_witness'] for r in out)
(D/'results/STRICT_SOLID_WITNESSES.json').write_text(json.dumps(out,indent=2)+'\n')
