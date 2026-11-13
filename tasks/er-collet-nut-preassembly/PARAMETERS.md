# Parameter table and provenance

No independently measured data are claimed. Manufacturer collet dimensions are distinguished from the original nut/cam and physical parameters. Every local collider/body/scoring field is enumerated in parameters.csv; scene.json is the complete exact construction. Lengths in m, masses kg, angles radians, inertia kg·m².

| Parameter | Value (SI) | Classification / source |
|---|---|---|
| grasp_offset_z | 0.036 | Benchmark-authored approximation; Original benchmark design, not measured nut hardware |
| collet_D1 | 0.033 | Manufacturer-documented; REGO-FIX Drawing4, selected 8 mm bore |
| collet_D2 | 0.032 | Manufacturer-documented; REGO-FIX Drawing4, selected 8 mm bore |
| collet_D3 | 0.0292 | Manufacturer-documented; REGO-FIX Drawing4, selected 8 mm bore |
| collet_length | 0.04 | Manufacturer-documented; REGO-FIX Drawing4, selected 8 mm bore |
| collet_groove_width | 0.0036 | Manufacturer-documented; REGO-FIX Drawing4, selected 8 mm bore |
| collet_nose_length | 0.0055 | Manufacturer-documented; REGO-FIX Drawing4, selected 8 mm bore |
| collet_bore | 0.008 | Manufacturer-documented; REGO-FIX Drawing4, selected 8 mm bore |
| taper_angle | 0.13962634015954636 | Manufacturer-documented; REGO-FIX Drawing4, selected 8 mm bore |
| nose_angle | 0.5235987755982988 | Manufacturer-documented; REGO-FIX Drawing4, selected 8 mm bore |
| cam_inner_radius | 0.0185 | Benchmark-authored approximation; Original benchmark design, not measured nut hardware |
| cam_eccentricity | 0.0029 | Benchmark-authored approximation; Original benchmark design, not measured nut hardware |
| cam_thickness | 0.0006 | Benchmark-authored approximation; Original benchmark design, not measured nut hardware |
| nut_front_bore_radius | 0.019 | Benchmark-authored approximation; Original benchmark design, not measured nut hardware |
| nut_upper_bore_radius | 0.0202 | Benchmark-authored approximation; Original benchmark design, not measured nut hardware |
| nut_outer_radius | 0.025 | Benchmark-authored approximation; Original benchmark design, not measured nut hardware |
| hook_angle | -0.25 | Benchmark-authored approximation; Original benchmark design, not measured nut hardware |
| collet_mass | 0.15 | Benchmark-authored approximation; Original benchmark design, not measured nut hardware |
| material.static_friction | 0.65 | Benchmark-authored approximation; Uniform contact assumption |
| material.dynamic_friction | 0.5 | Benchmark-authored approximation; Uniform contact assumption |
| material.restitution | 0.0 | Benchmark-authored approximation; Uniform contact assumption |
| material.contact_offset | 3e-05 | Benchmark-authored approximation; Uniform contact assumption |
| material.rest_offset | 0.0 | Benchmark-authored approximation; Uniform contact assumption |

Derived main-cone length=40−3.6−5.5=30.9 mm; groove z=±1.8 mm, nose end −7.3 mm, body end +32.7 mm; cam minimum radial edge=18.5−2.9=15.6 mm. Radial groove clearance at that edge=15.6−14.6=1 mm. Cam axial clearance at upright groove=3.6−0.6=3 mm. Published L1 is a holder-plane reference and is not silently reused as a nut/cam dimension. Faceted and sliced profiles approximate continuous surfaces; source recipe lists all approximants. Physical reproduction needs actual tolerance/mass/friction measurement before comparison.
