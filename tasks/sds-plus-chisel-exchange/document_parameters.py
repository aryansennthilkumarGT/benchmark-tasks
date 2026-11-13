"""Expand explicit parameter provenance; no value is silently called measured."""
import json,math
from pathlib import Path
import dimensions as D
HERE=Path(__file__).resolve().parent
CLASSES={'Manufacturer-documented','Independently measured, with genuine measurement evidence','Benchmark-authored approximation','Derived from other explicitly stated geometry'}
def numbers(x,path=''):
 if isinstance(x,bool):return
 if isinstance(x,(int,float)):yield path,x
 elif isinstance(x,list):
  for i,v in enumerate(x):yield from numbers(v,path+'/'+str(i))
 elif isinstance(x,dict):
  for k,v in x.items():yield from numbers(v,path+'/'+k)
def provenance(s):
 rows=[]
 derived_mass_paths={f'/assemblies/{ai}/bodies/{bi}/mass' for ai,a in enumerate(s['assemblies']) for bi,b in enumerate(a['bodies']) if b['name'] in ('locking_ball','locking_sleeve','used_point_chisel','replacement_flat_chisel')}
 for path,value in numbers(s):
  if path=='/parameters/ball_diameter_manufacturer':kind='Manufacturer-documented';source='SOURCES.json manufacturer parts1903230013,DIN5401-Ø7MM-III-ST'
  elif path in derived_mass_paths:kind='Derived from other explicitly stated geometry';source='Specified original primitive volumes and authored material densities; sphere uses documented7mm diameter'
  elif any('/'+k+'/' in path or path.endswith('/'+k) for k in ['vertices','faces','center_of_mass','diagonal_inertia','principal_axes','density_normalization','nominal_component_mass_kg','bounds_min','bounds_max']):kind='Derived from other explicitly stated geometry';source='cad.py/generate_scene.py and mass_properties.py; declared authored solids/densities and documented7mm ball'
  else:kind='Benchmark-authored approximation';source='dimensions.py/generate_scene.py; explicit original fixture configuration, not measured OEM hardware'
  rows.append(dict(path=path,value=value,classification=kind,source=source))
 return dict(schema=1,geometry_mode=D.MODE.value,records=rows)
def write():
 s=json.loads((HERE/'scene.json').read_text());d=provenance(s);(HERE/'parameter-provenance.json').write_text(json.dumps(d,indent=2)+'\n');lines=['# Complete parameter and reproduction table','','M manufacturer-documented; A benchmark-authored; D derived. There are no independently measured values. Every expanded numeric scene value, including every solid vertex, appears in parameter-provenance.json. Raw primitive coordinates are canonical scene.json; original decomposition/formulas are in cad.py/generate_scene.py.','','| Source parameter | Value (SI unless stated) | Classification | Evidence |','|---|---|---|---|']
 for n,r in D.PARAMETERS.items():lines.append('|'+n+'|'+str(r['value'])+'|'+r['classification']+'|'+r['source']+'|')
 lines+=['','| Additional authored interface | Specification |','|---|---|','| Ball race | Front center19.95mm to rear24.55mm; forward locked range19.4–21.0mm |','| Inner retaining lips | transverse half-gap3.1mm; z=6.2mm+0.10(x−20mm) overx16.9–27.6mm |','| Outer guides | lateral half-gap3.55mm; free ball rotation; no slider/weld |',f'| Sleeve bore |{D.COLLAR_BORE_RELEASED*1000:.2f}mm radius throughx15mm; transition to{D.COLLAR_BORE_CLOSED*1000:.2f} at17; locking land17–22; rear relief to{D.COLLAR_BORE_RELEASED*1000:.2f} at24; rear end35mm |','| Sleeve spring |2000N/m,5N·s/m,rest−1mm; forward stop0,travel8mm;2N preload |','| Open drive interface | shank groove floor3.6mm; key inner radius3.8mm and1.4mm tangential width; starts5mm into holder |','| Running fit | nominal shankR5mm / holder boreR5.15mm;0.15mm radial authored clearance |','| Cage lateral clearance |7.1mm guide opening /7mm nominal ball;0.05mm nominal radial clearance; faceting affects actual contact |','| Materials | steel7850kg/m³; clear glass2500; clear polycarbonate1200; fixed-fixture default2700. Authored assumptions, not OEM measured properties |','| Friction | dry static0.65/dynamic0.45; lubricated0.18/0.12; restitution0 |','| Numerics |1920Hzphysics/20Hzcontrol;20um contact offset,zero rest;200um max overlap |','','The gravity-biased race and relieved locking sleeve are original engineered approximations of the documented external SDS operation, not claimed OEM hidden geometry. The manufacturer establishes the procedure and7mm ball; no forces/torques or other dimensions are invented as manufacturer specifications.','','| Body | Mass kg | COM m(D) | Principal inertia kg·m²(D) |','|---|---:|---|---|']
 for a in s['assemblies']:
  for b in a['bodies']:lines.append('|'+b['name']+'|'+str(b['mass'])+'|'+str(b['center_of_mass'])+'|'+str(b['diagonal_inertia'])+'|')
 lines+=['','Chisel/sleeve masses derive from explicit non-overlapping material volumes. Ball target mass derives from documented7mm diameter and authored7850kg/m³ density using4πr³/3. Fixed-fixture target masses are A. Compound overlaps count twice; normalized moments are not exact boolean CAD or measured hardware. Complete expanded numeric provenance: '+str(len(d['records']))+' values.']
 (HERE/'PARAMETERS.md').write_text('\n'.join(lines)+'\n')
if __name__=='__main__':write()
