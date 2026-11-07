# Fasten a spring-loaded access plate while maintaining its preload — physical setup

Bimanual YAM station; x forward, y left, z up; metres/kg/radians; XYZW quaternions. Tabletop z=0.7475 m. Fixed layout, seed 0, no object jitter. 

Geometry is original primitive construction. All movable components use friction 0.65 static / 0.5 dynamic and restitution 0. Joint damping, spring constants and contact pairs are specified below and in `scene.json`. Explicit inertias/centers of mass override shape-derived values where present. Extended handling tabs are part of the bench fixture, not a claim of commercial-product fidelity.

| Body | Material/type | Mass kg | Envelope m | World origin m | XYZW | Constraint |
|---|---|---:|---|---|---|---|
| `bracket` | steel plate and threaded studs | 0.6 | (0.25, 0.17, 0.034) | (0.265, 0, 0.7515) | (0, 0, 0, 1) | anchored |
| `plate_carrier` | rigid fixture material | 0.001 | (0.001, 0.001, 0.001) | (0.265, 0, 0.7735) | (0, 0, 0, 1) | passive dynamic |
| `plate_gimbal` | rigid fixture material | 0.001 | (0.001, 0.001, 0.001) | (0.265, 0, 0.7735) | (0, 0, 0, 1) | passive dynamic |
| `pressure_plate` | rigid fixture material | 0.12 | (0.25, 0.266, 0.032) | (0.265, 0, 0.7735) | (0, 0, 0, 1) | passive dynamic |
| `nut_0` | coarse threaded steel surrogate | 0.024 | (0.034, 0.034, 0.01) | (0.15, -0.18, 0.7527) | (0, 0, 0, 1) | passive dynamic |
| `nut_1` | coarse threaded steel surrogate | 0.024 | (0.034, 0.034, 0.01) | (0.22, -0.18, 0.7527) | (0, 0, 0, 1) | passive dynamic |
| `nut_2` | coarse threaded steel surrogate | 0.024 | (0.034, 0.034, 0.01) | (0.29, -0.18, 0.7527) | (0, 0, 0, 1) | passive dynamic |
| `nut_3` | coarse threaded steel surrogate | 0.024 | (0.034, 0.034, 0.01) | (0.36, -0.18, 0.7527) | (0, 0, 0, 1) | passive dynamic |
| `nut_4` | coarse threaded steel surrogate | 0.024 | (0.034, 0.034, 0.01) | (0.15, 0.23, 0.7527) | (0, 0, 0, 1) | passive dynamic |
| `nut_5` | coarse threaded steel surrogate | 0.024 | (0.034, 0.034, 0.01) | (0.22, 0.23, 0.7527) | (0, 0, 0, 1) | passive dynamic |
| `nut_6` | coarse threaded steel surrogate | 0.024 | (0.034, 0.034, 0.01) | (0.29, 0.23, 0.7527) | (0, 0, 0, 1) | passive dynamic |
| `nut_7` | coarse threaded steel surrogate | 0.024 | (0.034, 0.034, 0.01) | (0.36, 0.23, 0.7527) | (0, 0, 0, 1) | passive dynamic |

## Passive joints

- `plate_preload`: prismatic Z, `bracket` to `plate_carrier`; limits [-0.014, 0.002]; stiffness 400, damping 2. Full joint frames are in `scene.json`.
- `plate_tilt_x`: revolute X, `plate_carrier` to `plate_gimbal`; limits [-0.12, 0.12]; stiffness 0.2, damping 0.015. Full joint frames are in `scene.json`.
- `plate_tilt_y`: revolute Y, `plate_gimbal` to `pressure_plate`; limits [-0.12, 0.12]; stiffness 0.2, damping 0.015. Full joint frames are in `scene.json`.

## Mass distribution overrides

- `plate_carrier`: center of mass derived from geometry; diagonal inertia [1e-07, 1e-07, 1e-07].
- `plate_gimbal`: center of mass derived from geometry; diagonal inertia [1e-07, 1e-07, 1e-07].
