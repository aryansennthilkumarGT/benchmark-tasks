# Parameters and provenance

SI units and XYZW quaternions throughout. Every original solid, convex vertex/face, transform, mass, COM, inertia, contact value and joint is specified in `scene.json`. `parameter-provenance.json` classifies every numeric value by longest JSON-pointer prefix and binds the exact scene hash. `provenance.py` checks coverage. No parameter is independently measured.

M = manufacturer-documented; D = derived from stated geometry or source; A = benchmark-authored approximation. A source dimension from one product is never attributed to the other product.

| Parameter | Value | Class / basis |
|---|---|---|
| Reference product operating span | 40–70 in (1.016–1.778 m) | M inches, D conversion; HF96811 manual p2 |
| Separate commercial pad envelope | 2.5 × 4 in (63.5 × 101.6 mm) | M inches, D conversion; USCC LB200-4PK |
| Pad thickness | 12 mm | A |
| Wall inner spacing | 1200 mm | A; inside reference span |
| Outer tube | 600 mm; OD36 / ID28 mm | A; 510 mm closed guide plus 90 mm service window |
| Inner tube | 600 mm; OD25 / ID18 mm | A; 1.5 mm radial guide clearance |
| Rack | 100 mm long, 4 mm pitch | A |
| Pinion | 20 teeth; 20° pressure angle | A |
| Pinion pitch radius | 12.732395447 mm | D = 20×4/(2π) mm |
| Rack radial clearance | 50 µm | A; not a manufacturer tolerance |
| Ratchet | 24 teeth; root17 / tip20 mm radius; 14 mm width | A |
| Ratchet phase | 0.029 rad | A; original tooth-contact alignment |
| Shaft / bearing bores | R4.8 / R6.7 mm | A; 1.9 mm nominal radial gap |
| Handle hub bore | R5.4 mm | A; 0.6 mm shaft radial clearance |
| Trigger stroke / operating pull | 0–9 / 8.3 mm | A |
| Handle stop | 2.60 rad | A; manufacturer states full-forward, not this angle |
| Foot springs | 12,000 N/m; travel4 mm; damping2 N·s/m | A; compliant cartridge surrogate |
| Initial extension | 23.333333 mm | D = seven ratchet pitches |
| Initial per-pad compression | 1.666667 mm | D = (extension−20 mm)/2 |
| Initial pad normal load | 20 N each | D = spring stiffness×compression, not measured force |
| Contact coefficients | main static0.65 / dynamic0.5; cams0.12 / 0.08; restitution0 | A; steel/aluminium/rubber and greased contact approximations |
| Physics / control | 960 / 20 Hz | A |
| Penetration rejection | 0.35 mm | A numerical integrity tolerance, not allowable hardware deformation |

Body properties (all masses A; COM/inertia D bounding-box equivalents, not CAD integration or real mass tensors):

| Body | Mass kg | Local COM m | Diagonal inertia kg·m² |
|---|---:|---|---|
| wall_frame | 5.0 | 0, 0, 0.07 | 0.73416667, 0.028333333, 0.74616667 |
| outer_tube | 0.85 | 0.021, -0.26975, -0.028003461 | 0.026142141, 0.0012524236, 0.026195318 |
| inner_tube | 0.48 | 8.6736174e-19, 0.265, -0.003995422 | 0.014927536, 6.8535832e-05, 0.014909 |
| left_pad | 0.06 | 0, 0, 0 | 5.23328e-05, 7.177405e-05, 2.088125e-05 |
| right_pad | 0.06 | 0, 0, 0 | 5.23328e-05, 7.177405e-05, 2.088125e-05 |
| gear_set | 0.16 | 0, 0, 0 | 4.3014766e-05, 7.9587383e-05, 7.9587383e-05 |
| handle | 0.07 | 0.048, 0.0349, -0.014379617 | 4.9297048e-05, 2.3322148e-05, 5.28549e-05 |
| release_trigger | 0.012 | 0.054, 0.02, 0.00025 | 3.24625e-06, 8.9425e-07, 3.92e-06 |
| holding_pawl | 0.008 | 0.01275, 0.010948801, 0.0055773651 | 4.7454469e-07, 6.9889749e-07, 9.3598054e-07 |
| driving_pawl | 0.008 | 0.0145, 0.0081469261, 0.009625 | 5.2936e-07, 1.0270417e-06, 9.5431834e-07 |

Joint properties (all A except initial coordinates D; rad, m, N/m or N·m/rad and corresponding damping):

| Joint | Type/axis | Parent → child | Limits | Spring / damping / rest | Initial |
|---|---|---|---|---|---|
| telescope | prismatic/Y | outer_tube → inner_tube | 0, 0.05 | 0.0 / 0.05 / 0.0 | 0.02333333333 |
| left_compliance | prismatic/Y | outer_tube → left_pad | 0, 0.004 | 12000.0 / 2.0 / 0.0 | 0.001666666667 |
| right_compliance | prismatic/Y | inner_tube → right_pad | -0.004, 0 | 12000.0 / 2.0 / 0.0 | -0.001666666667 |
| pinion_rotation | revolute/X | outer_tube → gear_set | -8, 8 | 0.0 / 5e-05 / 0.0 | -1.832595715 |
| handle_rotation | revolute/X | outer_tube → handle | 0, 2.6 | 0.0 / 0.002 / 0.0 | 0 |
| trigger_pull | prismatic/Y | handle → release_trigger | 0, 0.009 | 80.0 / 0.2 / 0.0 | 0 |
| holding_pawl_rotation | revolute/X | outer_tube → holding_pawl | -0.02, 0.8 | 0.02 / 0.0004 / 0.0 | 0 |
| driving_pawl_rotation | revolute/X | handle → driving_pawl | -0.02, 0.8 | 0.02 / 0.0004 / 0.0 | 0 |

Every joint pivot is listed as `pivot_parent` / `pivot_child` in the canonical table `scene.json`. Every body shape is ordered there with local position, orientation, size/radius/height or complete convex vertices/faces. This machine-readable solid table is the complete manufacturing profile; none of its unlisted-in-this-summary dimensions is an OEM measurement. `generate_scene.py`, `gearing.py` and `convex_primitives.py` reproduce the exact shapes.

Material assumptions: lightweight aluminium tube/housing/handle members, steel rack, shaft, ratchet/pinion and pawls, elastomer-faced passive foot cartridges. Outer0.85kg leaves mass for its housing/bearings beyond about0.65kg for a full uncut aluminium tube; inner0.48kg covers about0.38kg aluminium tube plus rack/fittings. Gear set0.16kg permits a steel shaft and webbed wheel. These are authored lumped properties; physical construction must weigh and trim noncontact ballast, then report genuine measurements separately. No material density, surface treatment, force or rating was measured. The mechanism totals 1.708 kg. Initial friction design bound is 2×20×0.5=20 N versus weight about16.8 N; actual contacts/grasp margins require native validation.

The authored cam release produces conservative nose-clearance bounds from the actual nose colliders in `mechanism_cpu.py`; no virtual hinge threshold disengages contacts. The native controller checks ≥0.8mm conservative clearance before retracting. Full-forward handle position is required to operate release, not to remain latched after unloading.
