"""Regenerate complete fixture parameter/provenance tables from the scene."""
from pathlib import Path
import json,csv
p=Path(__file__).resolve().parent
s=json.loads((p/'scene.json').read_text())
rows=[]
for k,v in s['parameters'].items():
 rows.append((k,v,'kg' if k.endswith('_mass') else 'm','Benchmark-authored approximation' if not k.startswith('flywheel_thread') else 'Manufacturer-documented available family; benchmark-selected application','fixture-profile.json / dimensions.py'))
extra=[('stud_count',3,'count','Manufacturer-documented','LuK section 10.6 p28'),('stud_angular_spacing',120,'degree','Manufacturer-documented','LuK section 10.6 p28'),('upper_thread_segments_per_turn',64,'count','Benchmark-authored approximation','generate_scene.helix'),('upper_thread_flank_relief',.0002,'m','Benchmark-authored approximation','generate_scene.helix'),('upper_thread_root_radial_clearance',.0002,'m','Derived from other explicitly stated geometry','female inner 4.9 mm - male root 4.7 mm'),('upper_thread_shell_radial_clearance',.00035,'m','Derived from other explicitly stated geometry','female shell bore 6.35 mm - male crest 6 mm'),('slot_diametral_clearance',.002,'m','Derived from other explicitly stated geometry','14 mm slot - 12 mm upper stud'),('spindle_mandrel_diametral_clearance',.004,'m','Derived from other explicitly stated geometry','19 mm bore - 15 mm mandrel'),('carrier_mandrel_diametral_clearance',.005,'m','Derived from other explicitly stated geometry','20 mm carrier bore - 15 mm mandrel'),('fixture_mass',5.,'kg','Benchmark-authored approximation','generate_scene.py'),('carrier_tray_mass',1.,'kg','Benchmark-authored approximation','generate_scene.py'),('retainer_tray_mass',1.,'kg','Benchmark-authored approximation','generate_scene.py')]
for k,v in s['material'].items():extra.append((k,v,'SI','Benchmark-authored approximation','scene.json material / build_assets.py / arena_runtime.py'))
extra.extend([('gravity',s['gravity'],'m/s^2','Benchmark-authored approximation','standard station choice'),('physics_dt',s['physics_dt'],'s','Benchmark-authored approximation','native integration setting'),('control_hz',20,'Hz','Benchmark-authored approximation','YAM policy interface'),('run_limit',42000,'actions','Benchmark-authored approximation','pending native timing'),('table_top',s['table_top'],'m','Benchmark-authored approximation','pinned station table convention')])
for k,v in s['score_spec'].items():
 if isinstance(v,(int,float)):extra.append(('scoring.'+k,v,'SI','Benchmark-authored approximation','score_spec; numerical benchmark acceptance tolerance'))
rows+=extra
# All exported local primitives, positions, bounds and inertia are enumerated so
# there is no undocumented dimension hidden in a generated USD file.
for a in s['assemblies']:
 b=a['bodies'][0]
 for k in ('pos','quat','bounds_min','bounds_max','center_of_mass','diagonal_inertia'):
  rows.append((b['name']+'.'+k,b[k],'SI (quat unitless)','Derived from other explicitly stated geometry' if k.startswith(('bounds','center_of_mass','diagonal')) else 'Benchmark-authored approximation','scene.json; inertia is mass-matched bounding-box approximation'))
 for i,t in enumerate(b['shapes']):
  for k in ('pos','quat','size','radius','height'):
   if k in t:rows.append((b['name']+'.shape_'+str(i)+'.'+k,t[k],'SI (quat unitless)','Derived from other explicitly stated geometry','generate_scene.py original construction recipe'))
with (p/'parameters.csv').open('w',newline='') as stream:
 w=csv.writer(stream);w.writerow(['parameter','value','unit','classification','reference_or_derivation']);w.writerows(rows)
text='# Fixture parameters and provenance\n\nGeometry mode: **BENCHMARK_AUTHORED**. None of the component geometry or material parameters in this fixture is independently measured LuK hardware. No measurement evidence is claimed. `uncertainty=0` denotes exact authored numerical input, not zero physical uncertainty. Target manufacturing tolerance is ±0.05 mm on mating dimensions, ±5 g on authored masses; assembly clearances and scorer tolerances are independent.\n\nThe three-stud count and 120° spacing are manufacturer-documented. Manufacturer kit data supports the availability of flywheel-side thread families; choosing an M8×1.25 prepared lower interface is authored, and does not determine the separate custom upper thread. No undocumented value is silently inferred from a kit label or photograph.\n\n| Parameter | Value | Unit | Classification / basis |\n|---|---|---|---|\n'
for k,v,u,c,r in rows[:len(s['parameters'])+len(extra)]:text+=f'| {k} | {v} | {u} | {c}; {r} |\n'
text+='\n`parameters.csv` additionally enumerates every body initial pose, quaternion, bounding extent, inertia and local collider dimension/pose, all generated from the stated construction recipe. `scene.json` contains exact machine-readable complete bodies. `generate_scene.py` is the manufacturing geometry source; `assets/*.usda` is its collision/visual export. No hidden simplified solid bore, grasp joint, attractive magnet or success-triggered drive is present.\n'
(p/'PARAMETER_TABLE.md').write_text(text)
