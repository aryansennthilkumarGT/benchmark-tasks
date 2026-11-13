# Parameters and provenance

Only the drive external envelope is manufacturer-documented. No independently measured hardware is claimed. All mounting bores, pin dimensions/positions, spring/damping/limits, masses, support/handle dimensions, materials/contact properties and numerical tolerances are benchmark-authored approximations. COM/inertia are derived mass-matched bounding-box approximations, not measured tensors.

| Parameter | Value (SI) | Classification |
|---|---|---|
| drive_length | 0.1 | Manufacturer-documented; Samsung 870 EVO datasheet |
| drive_width | 0.06985 | Manufacturer-documented; Samsung 870 EVO datasheet |
| drive_height | 0.0068 | Manufacturer-documented; Samsung 870 EVO datasheet |
| drive_mass | 0.045 | Benchmark-authored approximation; Original fixture design |
| pin_radius | 0.0015 | Benchmark-authored approximation; Original fixture design |
| pin_length | 0.006 | Benchmark-authored approximation; Original fixture design |
| pin_x_spacing | 0.06 | Benchmark-authored approximation; Original fixture design |
| pin_centres_y | [-0.035, 0.035] | Benchmark-authored approximation; Original fixture design |
| bore_radius | 0.0024 | Benchmark-authored approximation; Original fixture design |
| bore_depth | 0.006 | Benchmark-authored approximation; Original fixture design |
| rail_travel | 0.006 | Benchmark-authored approximation; Original fixture design |
| rail_limit | 0.007 | Benchmark-authored approximation; Original fixture design |
| rail_stiffness | 180.0 | Benchmark-authored approximation; Original fixture design |
| rail_damping | 1.0 | Benchmark-authored approximation; Original fixture design |
| rail_mass | 0.016 | Benchmark-authored approximation; Original fixture design |
| tilt_angle | 0.25 | Benchmark-authored approximation; Original fixture design |
| opposite_pin_release_translation | 0.0045 | Benchmark-authored approximation; Original fixture design |
| material.static_friction | 0.65 | Benchmark-authored approximation; Native contact model; not measured Dell/Samsung data |
| material.dynamic_friction | 0.5 | Benchmark-authored approximation; Native contact model; not measured Dell/Samsung data |
| material.restitution | 0.0 | Benchmark-authored approximation; Native contact model; not measured Dell/Samsung data |
| material.contact_offset | 3e-05 | Benchmark-authored approximation; Native contact model; not measured Dell/Samsung data |
| material.rest_offset | 0.0 | Benchmark-authored approximation; Native contact model; not measured Dell/Samsung data |

`parameters.csv` includes every exported collider dimension/pose, body mass/initial pose/COM/inertia, joint and scoring parameter. `scene.json` is the full reproducible machine-readable construction. Boreshole radial clearance is 2.4−1.5=0.9 mm; pin penetration is 2.925 mm; normal release 6 mm leaves ~3.075 mm side clearance. Nominal outward force at 6 mm is derived as 180×0.006=1.08 N, a benchmark design value, never a manufacturer force. Contacts use static/dynamic friction 0.65/0.5 and 30 µm offset, restitution zero.
