"""Full original fixture geometry and physical parameter/provenance export."""
import csv,json
from pathlib import Path
p=Path(__file__).resolve().parent;s=json.loads((p/'scene.json').read_text());rows=[]
manufacturer={'drive_length','drive_width','drive_height'}
for k,v in s['parameters'].items():rows.append((k,v,'SI','Manufacturer-documented' if k in manufacturer else 'Benchmark-authored approximation','Samsung 870 EVO datasheet' if k in manufacturer else 'Original fixture design'))
for k,v in s['material'].items():rows.append(('material.'+k,v,'SI','Benchmark-authored approximation','Native contact model; not measured Dell/Samsung data'))
for a in s['assemblies']:
 for b in a['bodies']:
  for k in ('pos','quat','mass','center_of_mass','diagonal_inertia','bounds_min','bounds_max'):
   rows.append((b['name']+'.'+k,b[k],'SI (quaternion unitless)','Derived from other explicitly stated geometry' if k in ('center_of_mass','diagonal_inertia','bounds_min','bounds_max') else 'Benchmark-authored approximation','Bounding-box mass model / original scene'))
  for i,shape in enumerate(b['shapes']):
   for k in ('pos','quat','size','radius','height'):
    if k in shape:rows.append((b['name']+'.shape_'+str(i)+'.'+k,shape[k],'SI','Derived from other explicitly stated geometry','generate_scene.py construction from stated dimensions'))
 for j in a['joints']:
  for k,v in j.items():rows.append(('joint.'+j['name']+'.'+k,v,'SI','Benchmark-authored approximation','Lumped compliant rail, not manufacturer data'))
for k,v in s['score_spec'].items():rows.append(('scoring.'+k,v,'SI','Benchmark-authored approximation','Numerical benchmark acceptance criterion / stated initial geometry'))
with (p/'parameters.csv').open('w',newline='') as stream:
 w=csv.writer(stream);w.writerow(['parameter','value','units','classification','source_or_derivation']);w.writerows(rows)
md='# Parameters and provenance\n\nOnly the drive external envelope is manufacturer-documented. No independently measured hardware is claimed. All mounting bores, pin dimensions/positions, spring/damping/limits, masses, support/handle dimensions, materials/contact properties and numerical tolerances are benchmark-authored approximations. COM/inertia are derived mass-matched bounding-box approximations, not measured tensors.\n\n| Parameter | Value (SI) | Classification |\n|---|---|---|\n'
for k,v,unit,kind,ref in rows[:len(s['parameters'])+len(s['material'])]:md+=f'| {k} | {v} | {kind}; {ref} |\n'
md+='\n`parameters.csv` includes every exported collider dimension/pose, body mass/initial pose/COM/inertia, joint and scoring parameter. `scene.json` is the full reproducible machine-readable construction. Boreshole radial clearance is 2.4−1.5=0.9 mm; pin penetration is 2.925 mm; normal release 6 mm leaves ~3.075 mm side clearance. Nominal outward force at 6 mm is derived as 180×0.006=1.08 N, a benchmark design value, never a manufacturer force. Contacts use static/dynamic friction 0.65/0.5 and 30 µm offset, restitution zero.\n'
(p/'PARAMETERS.md').write_text(md)
