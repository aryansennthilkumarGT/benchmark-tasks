# Fixture parameters

SI units, XYZW quaternions. Every numeric scene field has longest-prefix provenance in parameter-provenance.json bound to the scene SHA. A=benchmark-authored approximation; D=derived. No manufacturer numerical dimension or independently measured value is used. The 18GA product class and procedure are manufacturer statements; this original pre-bent brad is not represented as a standard gauge conversion.

| Interface | Specification | Class |
|---|---|---|
| Nose / service orientation | root(0.25,0.06,0.805)m; Rx180deg; firing+X, service−Y | A |
| Table | z0.7475m | A |
| Rear trough / muzzle | x10–85 /85–100mm; inner half widths6 /1.3mm | A |
| Closed service gap | floor y−1.5mm to door y2mm:3.5mm | A / D |
| Door | rear81×3×26mm; front15×3×18mm; rear side overhang5mm over narrowed16mm backplate | A / D |
| Door hinge | R2mm shaft /R2.2mm bore;0.2mm radial gap; axisZ | A |
| Lever pivot | door(55,5.2,0)mm; R1.6 shaft /R1.8 bore | A |
| Lever |51×2×17mm plate; stop x7–13mm; eccentric(−5,−1.15,0)mm | A |
| Draw bail | arms z±18mm; ring inner/outer1.05/1.8mm; eccentric R0.9mm | A |
| Axial draw guide | rod R1.0mm /bore R1.1mm;0.1mm radial gap | A |
| Crosspin | R1.1mm ×52mm; ends exposed for stock YAM fingers | A, not OEM projection |
| Capture arms | z±12mm; rear inner face x93.5mm; lip underside y7.4mm; mouth front x98mm | A |
| Closed pin center |(94.6,6.3,0)mm nominal;5um initial elastic contact deflection | A; numerical deflection not machining interference |
| Draw spring |20kN/m,1N·s/m,0.5mm preload=10N | A / D; effective wire compliance, not measured OEM force |
| Brad |45×1×1.2mm stem; pre-bent head5.6mm transverse span;0.5g | A |
| Tray |80×90mm outer;76×86mm inner;20mm walls; world(0.24,−0.28,0.7495)m | A / D |
| Contact | static0.65,dynamic0.50,restitution0; contact offset20um/rest0 | A |
| Integrity | maximum penetration0.20mm; native1920Hz/control20Hz | A numerical tolerances |

All four parent-child pairs collide. There are no broad adjacency exclusions. Original workholding has a260×360×12mm plate at unchanged world base height,4.5/31.5mm supports, two bridges and93.5mm clamp rods. These heights derive from the authored service-origin z0.805m and the actual case/magazine envelopes. Every solid position, dimension, color, role and density appears in scene.json. Densities steel7850, aluminium2700, polymer1200kg/m³ are reasonable authored material assumptions; authored target masses normalize the computed moments. Density scales are not real measured material densities.

| Body | Mass kg(A) | Local COM m(D) | Principal inertia kg·m²(D) | Density scale(D) |
|---|---:|---|---|---:|
| nose_body | 3.5 | 0.0034745679, -0.09312499, 0.035417194 | 0.021243467, 0.035526226, 0.051963894 | 0.7863163 |
| nose_door | 0.075 | 0.046358945, 0.00036687332, 0 | 4.3096844e-06, 5.9502114e-05, 6.3436789e-05 | 1.170812 |
| latch_lever | 0.025 | -0.024736868, 0.0016543048, 0 | 8.846974e-07, 6.7615718e-06, 7.5926364e-06 | 1.568731 |
| draw_bail | 0.012 | 0.021210532, 0, -0 | 2.0571976e-06, 3.8999967e-06, 5.944452e-06 | 3.926616 |
| bail_crosspin | 0.003 | -0.0010009886, 0, 0 | 1.658996e-08, 7.428821e-07, 7.5772713e-07 | 1.503301 |
| bent_brad | 0.0005 | -0.00096804511, 0, -0.00044360902 | 6.7715e-10, 1.0461208e-07, 1.052059e-07 | 0.9977172 |
| parts_tray | 0.2 | 0, 0, 0.0032075472 | 0.0001468983, 0.00017975491, 0.00031329937 | 1.74703 |

| Joint | Limits | Stiffness / damping / rest | Initial |
|---|---|---|---|
| door_rotation | 0.0 to 2.05 | 0.0 / 0.001 / 0.0 | 0 |
| lever_rotation | -2.15 to 0.0 | 0.0 / 0.0004 / 0.0 | 0 |
| bail_rotation | -3.141592653589793 to 3.141592653589793 | 0.0 / 5e-05 / 0.0 | -0.02802271075 |
| bail_extension | -0.0003 to 0.0015 | 20000.0 / 1.0 / 0.0 | 0.0005 |

Slide units N/m,N·s/m,m; hinge units N·m/rad,N·m·s/rad,rad. Pivot frames and all joint limits are authored. Draw length/rest and prepared initial angle are derived. Supplemental capped diagnostic wrenches/torques are test inputs, never manufacturer forces or robot capacity estimates.
