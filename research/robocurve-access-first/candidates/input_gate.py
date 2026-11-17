"""Cheap source/scale gate before inventing a hardware access scene.
Researcher assets are inspected, but never silently treated as manufacturer CAD.
No Isaac/Omni imports from supplied asset scripts are executed.
"""
from pathlib import Path
import sys,json,gzip,hashlib,io
sys.path.insert(0,'/workspace/robocurve-cpu-deps')
D=Path(__file__).resolve().parent;R=D.parents[2]
sys.path.insert(0,str(R/'research/robocurve-implementation'))
import numpy as np,trimesh
from common.access import Access
A=Access()
S=D.parent/'sources'
requirements={
 '055':dict(name='Hamilton Beach loaded rotisserie',manufacturer_dimensions=dict(loaded_mass_kg=1.4,food_to_heater_clearance_m=.025),missing=['matched donor/SKU','spit length and pointed/square end sections','drive socket/cradle depth and registration','loaded roast envelope','matched cavity/door/heater geometry']),
 '091':dict(name='Ninja BL61030 locking lid',manufacturer_dimensions=dict(pitcher_capacity_L=2.1),missing=['manufacturer-calibrated pitcher/lid dimensions','handle section, hinge and motion','handle-to-catch linkage and under-tab sections','original blade-to-lid clearance'])}
rows=[]
for ident,config in requirements.items():
 raw=gzip.decompress((S/ident/'asset.obj.gz').read_bytes());model=trimesh.load(io.BytesIO(raw),file_type='obj',force='scene',process=False)
 geometry=[dict(name=name,vertices=len(m.vertices),faces=len(m.faces),bounds_asset_coordinates=m.bounds.tolist(),watertight=bool(m.is_watertight)) for name,m in model.geometry.items()]
 labels=json.loads((S/ident/'parts.json').read_text());code=(S/ident/'utils.py').read_text();text=(S/ident/'manufacturer_manual.txt').read_text()
 if ident=='055':assert 'rotisserie' in text.lower() and 'square' in text.lower()
 else:assert 'BL610' in text and 'handle' in text.lower() and 'tab' in text.lower()
 row=dict(id=ident,**config,asset_sha256=hashlib.sha256(raw).hexdigest(),asset_geometry=geometry,provided_part_labels=labels,
   audited_model_code_has_handle_linkage_identifier=any(x in code.lower() for x in ['latch','locking handle','retaining cuff']),
   real_scale_manufacturer_calibration=False,
   source_gate='REJECT FROM IMPLEMENTATION SELECTION',
   access_stages=dict(acquisition='NOT RUN: cannot bind real contact region/scale',manipulation='NOT RUN: essential matching interface geometry unsupported',release='NOT RUN',continuous_certificate='NOT RUN',physical_purchase='NOT PROVEN'),
   source_scope='Input package audit; absence of labels is not proof that no mesh contains a visual feature. No identified, dimensioned, articulated matching interface was recovered. No unsupported asset was rescaled into a passing scene.',
   robot_reference=dict(hulls_per_arm=len(A.r.hulls),total_hulls=2*len(A.r.hulls),nominal_opening_m=A.r.describe()['nominal_aperture_m'],necessary_TCP_radius_m=A.r.necessary_tcp_radius()),complete_access=False)
 rows.append(row);print(ident,config['name'],'material geometry groups',len(geometry),'BLOCKED before a source-scale robot scene',config['missing'],flush=True)
(D/'results/SOURCE_SCALE_GATES.json').write_text(json.dumps(rows,indent=2)+'\n')
