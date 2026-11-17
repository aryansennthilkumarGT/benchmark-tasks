"""Independent full STEP solid audit of canonical coupon foot positions.
The standard pin is a source-sized cylinder; a small loaded interference is the
explicit penalty-contact regularization, not a claim of hard-solid penetration.
"""
from pathlib import Path
import sys,json
sys.path.insert(0,'/workspace/robocurve-cpu-deps')
import cadquery as cq
from sections import S
D=Path(__file__).resolve().parent
control=json.loads((D/'results/CONTROLS.json').read_text())[0]
foot=cq.importers.importStep(str(S/'foot_structure.STEP')).val().rotate((0,0,0),(1,0,0),90).translate((0,0,-160))
fixed=[(n,cq.importers.importStep(str(S/n)).val()) for n in ['lower_leg_structure_base.STEP','lower_leg_structure_fork.STEP']]
rows=[]
for observation in control['observations']:
 y,z=observation['foot_shift_mm'];body=foot.translate((0,y,z))
 # Pin bottomed in the source3.6mm-deep bore:9.9..21.9mm above foot center.
 # Any source-compatible seating depth0..3.6mm overlaps the16..18mm guide.
 pin=cq.Solid.makeCylinder(.75,12,cq.Vector(0,y,-150.1+z),cq.Vector(0,0,1))
 row=dict(foot_shift_mm=[y,z],foot_print_overlap_mm3={},pin_print_overlap_mm3={})
 for n,s in fixed:
  row['foot_print_overlap_mm3'][n]=body.intersect(s).Volume()
  row['pin_print_overlap_mm3'][n]=pin.intersect(s).Volume()
 print(row,flush=True);rows.append(row)
assert max(v for row in rows for v in row['foot_print_overlap_mm3'].values())<.01
assert max(rows[0]['pin_print_overlap_mm3'].values())<.001
(D/'results/POSE_AUDIT.json').write_text(json.dumps(rows,indent=2)+'\n')
