"""Deliberately regenerate the authored fixture's exhaustive provenance/table.

Run only after reviewing intentional geometry/physical edits. This records
provenance; it cannot produce validation or measured-hardware evidence.
"""
import hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
HF='https://manuals.harborfreight.com/manuals/96000-96999/96811-792363968119.pdf'
HF_SHA='a486b18f2445e9a74fd1230a538f6bbf602ac46e1e3eb6f7d9c165c0ecf14489'
USCC='https://www.uscargocontrol.com/products/round-tube-cargo-load-bars-w-2x4-pads-4-pack.json'
USCC_SHA='fe11382d0fa409e6c85e7a7b7532f7af771df8a4fa991b68d8b0e77dd314a96b'


def write(folder=HERE):
 s=json.loads((folder/'scene.json').read_text())
 entries=[dict(pointer='',category='BENCHMARK_AUTHORED',basis='Original fully specified benchmark fixture, material assumptions and test configuration. No OEM dimensions, force, friction, mass or torque measurement is claimed. Covers numeric fields unless an explicitly derived/source entry overrides it.')]
 def derived(pointer,basis,formula,**kw):entries.append(dict(pointer=pointer,category='DERIVED',basis=basis,derivation=formula,**kw))
 for name,value in [('reference_minimum_length',40),('reference_maximum_length',70)]:
  derived('/parameters/'+name,'Documented reference operating span, converted to SI.',f'{value} inch * 0.0254 m/inch',source_url=HF,source_sha256=HF_SHA,quote='40 to 70 inch range, manual page2')
 for ai,a in enumerate(s['assemblies']):
  for bi,b in enumerate(a['bodies']):
   base=f'/assemblies/{ai}/bodies/{bi}'
   for name in ['bounds_min','bounds_max']:
    derived(base+'/'+name,'Enclosing bounds computed from authored oriented primitive envelopes.','primitives.body: extrema of transformed enclosing primitive-box corners; not a mass model.')
   for name in ['diagonal_inertia','center_of_mass','principal_axes','nominal_component_mass_kg','density_normalization']:
    derived(base+'/'+name,'Density-weighted compound primitive moments, normalized to separately authored total mass. Overlapping pieces counted; not measured hardware or exact boolean CAD.', 'mass_properties.py: mi=rhoi*Vi; C=sum(mi*Ci)/sum(mi); covariance=sum(mi*(Qi+(Ci-C)(Ci-C)^T))/sum(mi); I=M*(trace(Q)*identity-Q); principal axes/eigenvalues=eigh(I); density scale=M/sum(mi). Boxes/cylinders analytic, convex closed surfaces signed tetrahedra.')
   if b['name'] in ('left_pad','right_pad'):
    for j,inch in [(0,2.5),(2,4)]:
     derived(base+f'/shapes/0/size/{j}','Separate commercial US Cargo Control pad envelope; never attributed to HF96811.',f'{inch} inch * 0.0254 m/inch',source_url=USCC,source_sha256=USCC_SHA,quote='2.5 inch x 4 inch pads')
 for n,formula in [('authored_pinion_pitch_radius','R=pitch*20/(2*pi)'),('authored_initial_extension','extension=7*(2*pi/24)*R'),('authored_initial_pad_compression','compression=(extension-0.020m)/2')]:
  derived('/parameters/'+n,'Exact authored gearing/prepared layout.',formula)
 derived('/initial_joint_values','Prepared contact-compatible layout.','generate_scene.py: seven ratchet pitches, symmetric foot compression, pinion=-extension/R; other coordinates zero.')
 derived('/materials/pad/cpu_dynamic_against_default','Supplemental single-coefficient approximation to a dynamic pad/metal pair; not measured static friction.','(materials.pad.dynamic_friction + material.dynamic_friction)/2')
 data=dict(schema=1,mode='BENCHMARK_AUTHORED',scene_sha256=hashlib.sha256((folder/'scene.json').read_bytes()).hexdigest(),entries=entries,independently_measured_hardware=False)
 (folder/'parameter-provenance.json').write_text(json.dumps(data,indent=2)+'\n')
 p=s['parameters'];compression=p['authored_initial_pad_compression'];normal=p['authored_pad_stiffness']*compression
 lines=['# Parameters and provenance','','SI units and XYZW quaternions. M = manufacturer-documented, D = derived, A = benchmark-authored approximation. No independently measured value exists. The complete machine-readable solid/joint/material/pose table is scene.json; every numeric field is classified by longest JSON-pointer prefix in parameter-provenance.json and bound to its SHA256. Neither inherited A provenance nor regeneration permits a claim of genuine measurement.','','| Parameter | Value | Class / basis |','|---|---|---|',
 '| Reference operating range | 40–70in / 1.016–1.778m | M inches / D conversion; HF96811 manual p2 |',
 '| Separate commercial pad face | 2.5×4in / 63.5×101.6mm | M inches / D conversion; USCC LB200-4PK, not HF |',
 '| Pad thickness / rod | 12mm / R4.8×24mm | A; guided compliant cartridge |',
 '| Wall inner spacing / wall height | 1200 / 140mm | A |',
 '| Outer tube | 740mm, OD36/ID28mm | A; 510mm rear closed guide, 180mm service opening, 50mm forward closed guide |',
 '| Inner tube | 600mm, OD25/ID18mm | A; 1.5mm radial tube clearance; about176.7mm initial axial overlap |',
 '| Rack / side guides | 100mm rack, 4mm pitch, 0.3mm side clearance | A; explicit rack mounts and connected guides |',
 '| Pinion | 20 teeth, 20deg pressure angle, R12.732395447mm pitch | A teeth/profile; D radius=20×4/(2π)mm |',
 '| Rack/pinion radial design clearance | 50µm | A, not manufacturer tolerance |',
 '| Ratchet | 24 teeth, R17–20mm, width14mm, phase0.029rad | A |',
 '| Shaft / bearing bores | R4.8 / R6.7mm | A; 1.9mm nominal radial clearance |',
 '| Handle hub | boreR5.4/outerR6.2mm | A; 0.6mm shaft radial clearance |',
 '| Guard | authored1–1.5mm panels, PC density1200kg/m³ | A; full panels/annular ports specified in scene |',
 '| Guard ports | outerR18.75 / innerR13.25 / hubR8mm | A; nominal radial gaps0.75 / 0.75 / 1.8mm |',
 '| Handle / trigger operating bars | 12×12×10 / 12×6×10mm | A; independent sliding trigger, actual slot and keeper |',
 '| Trigger travel / commanded pull | 0–9 / 8.3mm | A |',
 '| Full-forward handle stop | 2.60rad | A; manufacturer specifies full-forward, not this angle |',
 f'| Foot stiffness / nominal normal force | {p["authored_pad_stiffness"]:g}N/m / {normal:.6g}N each | A stiffness; D stiffness×compression |',
 f'| Initial extension / pad compression | {p["authored_initial_extension"]*1000:.9g} / {compression*1000:.9g}mm | D: seven ratchet pitches and symmetric preload |',
 '| Contact integrity bound | 0.35mm | A numerical integrity tolerance, not permitted real damage |',
 f'| Native physics / control | {1/s["physics_dt"]:g} / {s["control_hz"]:g}Hz | A; supplemental-engine settings separately disclosed |','',
 'All eight joint pairs have collisions enabled. No adjacency or broad object-pair exclusions conceal interference. Contact-bearing tubes, rods, bearings, rack guides and trigger have actual hollow/clearance geometry.','','Body properties: all target masses A. COM, principal axes, principal inertia and normalization D from the stated compound formula. Full tensors are preserved in USD and MuJoCo. Overlaps count twice; density scaling represents lumped fasteners/hollows/ballast, not real weighing.','','| Body | Mass kg | Local COM m | Principal inertia kg·m² | Density scale |','|---|---:|---|---|---:|']
 for a in s['assemblies']:
  for b in a['bodies']:lines.append('| '+b['name']+' | '+str(b['mass'])+' | '+', '.join(f'{v:.8g}' for v in b['center_of_mass'])+' | '+', '.join(f'{v:.8g}' for v in b['diagonal_inertia'])+' | '+f'{b["density_normalization"]:.7g}'+' |')
 lines+=['','Authored nominal densities: aluminium2700kg/m³ for the frame, tube and support pieces; steel7850 for gears, pawls, trigger/handle and tagged rack/cam/guide members; PC1200 for protective housing; effective homogenized pad-face580 with steel rod7850. The580 value approximates a hollow lightweight foot carrier/elastomer envelope, not solid rubber density. Actual reproduction must engineer that internal mass distribution or report deviations. Every individual shape density, normalized mass scale and principal quaternion appears in scene.json.','','| Contact material | Static / dynamic | Class |','|---|---|---|',f'| Default | {s["material"]["static_friction"]} / {s["material"]["dynamic_friction"]} | A |']
 for name,m in s['materials'].items():lines.append(f'| {name} | {m["static_friction"]} / {m["dynamic_friction"]} | A |')
 lines+=['','Restitution is zero. MuJoCo has one Coulomb coefficient; the pad uses the declared dynamic mean0.575 against default metal, not the larger static mean. Native PhysX keeps its separately declared static/dynamic coefficients. Cam materials and other supplemental contact differences require exact-source native checks.','','| Joint | Type/axis | Parent → child | Limits | Spring / damping / rest | Initial |','|---|---|---|---|---|---|']
 for a in s['assemblies']:
  for j in a['joints']:lines.append(f'| {j["name"]} | {j["kind"]}/{j["axis"]} | {j["parent"]} → {j["child"]} | {j["lower"]}, {j["upper"]} | {j["stiffness"]} / {j["damping"]} / {j["rest"]} | {j["initial"]:.10g} |')
 lines+=['','Joint stiffness/damping units are N/m and N·s/m for slides, N·m/rad and N·m·s/rad for hinges. All coefficients/limits/pivots are A; initial coordinates D. The original cam surfaces generate physical pawl lift; no virtual clearance angle or gear equality switches contact off.','',f'The free articulated bar target mass is {sum(b["mass"] for a in s["assemblies"] for b in a["bodies"] if not b.get("anchor")):.3f}kg. A nominal symmetric translational friction bound is 2×{normal:.6g}×0.575={2*normal*.575:.6g}N, before moment distribution, solver effects and gripper loading. This bound is not a static-hold proof, measured force, cargo rating or robot capability. All normal-load/grasp/native-contact claims require their actual tests.']
 (folder/'PARAMETERS.md').write_text('\n'.join(lines)+'\n')

if __name__=='__main__':write()
