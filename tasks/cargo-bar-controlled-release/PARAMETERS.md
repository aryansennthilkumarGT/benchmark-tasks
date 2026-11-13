# Parameters and provenance

SI units and XYZW quaternions. M = manufacturer-documented, D = derived, A = benchmark-authored approximation. No independently measured value exists. The complete machine-readable solid/joint/material/pose table is scene.json; every numeric field is classified by longest JSON-pointer prefix in parameter-provenance.json and bound to its SHA256. Neither inherited A provenance nor regeneration permits a claim of genuine measurement.

| Parameter | Value | Class / basis |
|---|---|---|
| Reference operating range | 40–70in / 1.016–1.778m | M inches / D conversion; HF96811 manual p2 |
| Separate commercial pad face | 2.5×4in / 63.5×101.6mm | M inches / D conversion; USCC LB200-4PK, not HF |
| Pad thickness / rod | 12mm / R4.8×24mm | A; guided compliant cartridge |
| Wall inner spacing / wall height | 1200 / 140mm | A |
| Outer tube | 740mm, OD36/ID28mm | A; 510mm rear closed guide, 180mm service opening, 50mm forward closed guide |
| Inner tube | 600mm, OD25/ID18mm | A; 1.5mm radial tube clearance; about176.7mm initial axial overlap |
| Rack / side guides | 100mm rack, 4mm pitch, 0.3mm side clearance | A; explicit rack mounts and connected guides |
| Pinion | 20 teeth, 20deg pressure angle, R12.732395447mm pitch | A teeth/profile; D radius=20×4/(2π)mm |
| Rack/pinion radial design clearance | 50µm | A, not manufacturer tolerance |
| Ratchet | 24 teeth, R17–20mm, width14mm, phase0.029rad | A |
| Shaft / bearing bores | R4.8 / R6.7mm | A; 1.9mm nominal radial clearance |
| Handle hub | boreR5.4/outerR6.2mm | A; 0.6mm shaft radial clearance |
| Guard | authored1–1.5mm panels, PC density1200kg/m³ | A; full panels/annular ports specified in scene |
| Guard ports | outerR18.75 / innerR13.25 / hubR8mm | A; nominal radial gaps0.75 / 0.75 / 1.8mm |
| Handle / trigger operating bars | 12×12×10 / 12×6×10mm | A; independent sliding trigger, actual slot and keeper |
| Trigger travel / commanded pull | 0–9 / 8.3mm | A |
| Full-forward handle stop | 2.60rad | A; manufacturer specifies full-forward, not this angle |
| Foot stiffness / nominal normal force | 12000N/m / 20N each | A stiffness; D stiffness×compression |
| Initial extension / pad compression | 23.3333333 / 1.66666667mm | D: seven ratchet pitches and symmetric preload |
| Contact integrity bound | 0.35mm | A numerical integrity tolerance, not permitted real damage |
| Native physics / control | 960 / 20Hz | A; supplemental-engine settings separately disclosed |

All eight joint pairs have collisions enabled. No adjacency or broad object-pair exclusions conceal interference. Contact-bearing tubes, rods, bearings, rack guides and trigger have actual hollow/clearance geometry.

Body properties: all target masses A. COM, principal axes, principal inertia and normalization D from the stated compound formula. Full tensors are preserved in USD and MuJoCo. Overlaps count twice; density scaling represents lumped fasteners/hollows/ballast, not real weighing.

| Body | Mass kg | Local COM m | Principal inertia kg·m² | Density scale |
|---|---:|---|---|---:|
| wall_frame | 11.0 | 0, 0.0005705817, 0.021541898 | 0.050711515, 2.1974168, 2.2221117 | 1.006317 |
| outer_tube | 1.05 | 0.0031063331, -0.17620357, -0.0090217152 | 0.0012197298, 0.048781738, 0.049153592 | 0.9714133 |
| inner_tube | 0.48 | 0, 0.24122335, -0.0019693312 | 6.090989e-05, 0.016491145, 0.016501104 | 0.9368227 |
| left_pad | 0.06 | 0, 0.0027953878, 0 | 1.8312212e-05, 4.2437155e-05, 5.5215372e-05 | 1.024941 |
| right_pad | 0.06 | 0, -0.0027953878, 0 | 1.8312212e-05, 4.2437155e-05, 5.5215372e-05 | 1.024941 |
| gear_set | 0.16 | 0.0088011818, -0, -0 | 1.8231942e-05, 3.2079195e-05, 3.2079195e-05 | 0.7855576 |
| handle | 0.07 | 0.049626469, 0.029175479, -0.0056061116 | 1.0195001e-05, 5.248984e-05, 5.8256967e-05 | 1.064993 |
| release_trigger | 0.012 | 0.059038363, 0.033560102, 0.00039897698 | 2.1703283e-07, 1.9481312e-06, 2.0468526e-06 | 0.9774056 |
| holding_pawl | 0.008 | 0.0069755211, 0.014650977, 0.0075226332 | 2.3442098e-07, 1.0045994e-06, 1.1824475e-06 | 1.334049 |
| driving_pawl | 0.008 | 0.0076432993, 0.00853593, 0.012668329 | 2.9885845e-07, 1.1848607e-06, 1.2792985e-06 | 1.331513 |

Authored nominal densities: aluminium2700kg/m³ for the frame, tube and support pieces; steel7850 for gears, pawls, trigger/handle and tagged rack/cam/guide members; PC1200 for protective housing; effective homogenized pad-face580 with steel rod7850. The580 value approximates a hollow lightweight foot carrier/elastomer envelope, not solid rubber density. Actual reproduction must engineer that internal mass distribution or report deviations. Every individual shape density, normalized mass scale and principal quaternion appears in scene.json.

| Contact material | Static / dynamic | Class |
|---|---|---|
| Default | 0.65 / 0.5 | A |
| cam | 0.12 / 0.08 | A |
| pad | 0.8 / 0.65 | A |

Restitution is zero. MuJoCo has one Coulomb coefficient; the pad uses the declared dynamic mean0.575 against default metal, not the larger static mean. Native PhysX keeps its separately declared static/dynamic coefficients. Cam materials and other supplemental contact differences require exact-source native checks.

| Joint | Type/axis | Parent → child | Limits | Spring / damping / rest | Initial |
|---|---|---|---|---|---|
| telescope | prismatic/Y | outer_tube → inner_tube | 0, 0.05 | 0.0 / 0.05 / 0.0 | 0.02333333333 |
| left_compliance | prismatic/Y | outer_tube → left_pad | 0, 0.004 | 12000.0 / 12.0 / 0.0 | 0.001666666667 |
| right_compliance | prismatic/Y | inner_tube → right_pad | -0.004, 0 | 12000.0 / 12.0 / 0.0 | -0.001666666667 |
| pinion_rotation | revolute/X | outer_tube → gear_set | -8, 8 | 0.0 / 5e-05 / 0.0 | -1.832595715 |
| handle_rotation | revolute/X | outer_tube → handle | 0, 2.6 | 0.0 / 0.002 / 0.0 | 0 |
| trigger_pull | prismatic/Y | handle → release_trigger | 0, 0.009 | 80.0 / 0.2 / 0.0 | 0 |
| holding_pawl_rotation | revolute/X | outer_tube → holding_pawl | -0.02, 0.8 | 0.02 / 0.0004 / 0.0 | 0 |
| driving_pawl_rotation | revolute/X | handle → driving_pawl | -0.02, 0.8 | 0.02 / 0.0004 / 0.0 | 0 |

Joint stiffness/damping units are N/m and N·s/m for slides, N·m/rad and N·m·s/rad for hinges. All coefficients/limits/pivots are A; initial coordinates D. The original cam surfaces generate physical pawl lift; no virtual clearance angle or gear equality switches contact off.

The free articulated bar target mass is 1.908kg. A nominal symmetric translational friction bound is 2×20×0.575=23N, before moment distribution, solver effects and gripper loading. This bound is not a static-hold proof, measured force, cargo rating or robot capability. All normal-load/grasp/native-contact claims require their actual tests.
