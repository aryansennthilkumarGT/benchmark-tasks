"""Reject raw coordinate use when source part occurrences are not an assembly.
This cannot establish a physical sag result; it deliberately emits no invented torque.
"""
from pathlib import Path
import json, sys
sys.path.insert(0, '/workspace/robocurve-cpu-deps')
import cadquery as cq
D=Path(__file__).resolve().parent;S=D.parent/'sources/cello/step'
parts={n:cq.importers.importStep(str(S/(n+'.step'))).val() for n in ['L1','L2','L3','L4','L5','L6']}
pairs=[]
for a,b in [('L2','L3'),('L2','L4'),('L3','L4'),('L4','L6')]:
 volume=parts[a].intersect(parts[b]).Volume()
 pairs.append(dict(parts=[a,b],raw_frame_overlap_mm3=volume));print(a,b,volume,flush=True)
x=dict(raw_coordinates_are_assembled=False,overlap_tests=pairs,
 physical_gravity_torque_Nm=None,loose_sag_deg=None,friction_window_Nm=None,
 decision='STOP_CELLO_SOURCE_REGISTRATION_GATE',
 reason='No installed occurrence transforms/BOM mass map established. Raw source coordinates substantially overlap; print layouts are not assembly transforms. Do not assign a fictitious gravity load.',
 not_a_claim='Not evidence that the actual designer arm cannot hold/backdrive; physical baseline and nine mechanism controls NOT RUN.')
assert all(p['raw_frame_overlap_mm3']>1000 for p in pairs)
(D/'results/LOAD_GATE.json').write_text(json.dumps(x,indent=2)+'\n')
