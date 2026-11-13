"""Complete original fixture parameter and classification table."""
import json,csv
from pathlib import Path
p=Path(__file__).resolve().parent;s=json.loads((p/'scene.json').read_text());rows=[]
documented={'collet_D1','collet_D2','collet_D3','collet_length','collet_groove_width','collet_nose_length','collet_bore','taper_angle','nose_angle'}
for k,v in s['parameters'].items():rows.append((k,v,'SI','Manufacturer-documented' if k in documented else 'Benchmark-authored approximation','REGO-FIX Drawing4, selected 8 mm bore' if k in documented else 'Original benchmark design, not measured nut hardware'))
for k,v in s['material'].items():rows.append(('material.'+k,v,'SI','Benchmark-authored approximation','Uniform contact assumption'))
for a in s['assemblies']:
 for b in a['bodies']:
  for k in ('pos','quat','mass','center_of_mass','diagonal_inertia','bounds_min','bounds_max'):
   rows.append((b['name']+'.'+k,b[k],'SI','Derived from other explicitly stated geometry' if k in ('center_of_mass','diagonal_inertia','bounds_min','bounds_max') else 'Benchmark-authored approximation','scene.json / bounding-box mass model'))
  for i,t in enumerate(b['shapes']):
   for k in ('pos','quat','size','radius','height'):
    if k in t:rows.append((b['name']+'.shape_'+str(i)+'.'+k,t[k],'SI','Derived from other explicitly stated geometry','generate_scene.py construction from classified dimensions'))
for k,v in s['score_spec'].items():rows.append(('scoring.'+k,v,'SI','Benchmark-authored approximation','Geometric acceptance criterion / declared initial state'))
with (p/'parameters.csv').open('w',newline='') as f:
 w=csv.writer(f,lineterminator="\n");w.writerow(['parameter','value','unit','classification','source_or_derivation']);w.writerows(rows)
md='# Parameter table and provenance\n\nNo independently measured data are claimed. Manufacturer collet dimensions are distinguished from the original nut/cam and physical parameters. Every local collider/body/scoring field is enumerated in parameters.csv; scene.json is the complete exact construction. Lengths in m, masses kg, angles radians, inertia kg·m².\n\n| Parameter | Value (SI) | Classification / source |\n|---|---|---|\n'
for k,v,u,c,r in rows[:len(s['parameters'])+len(s['material'])]:md+=f'| {k} | {v} | {c}; {r} |\n'
md+='\nDerived main-cone length=40−3.6−5.5=30.9 mm; groove z=±1.8 mm, nose end −7.3 mm, body end +32.7 mm; cam minimum radial edge=18.5−2.9=15.6 mm. Radial groove clearance at that edge=15.6−14.6=1 mm. Cam axial clearance at upright groove=3.6−0.6=3 mm. Published L1 is a holder-plane reference and is not silently reused as a nut/cam dimension. Faceted and sliced profiles approximate continuous surfaces; source recipe lists all approximants. Physical reproduction needs actual tolerance/mass/friction measurement before comparison.\n';(p/'PARAMETERS.md').write_text(md)
