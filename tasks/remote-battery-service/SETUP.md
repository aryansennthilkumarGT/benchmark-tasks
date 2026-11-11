# Replace opposed-polarity cells under a spring-return service cover — physical setup

Bimanual YAM station; x forward, y left, z up; metres/kg/radians; XYZW quaternions. Tabletop z=0.7475 m. Fixed layout, seed 0, no object jitter. 

Geometry is original primitive construction. All movable components use friction 0.65 static / 0.5 dynamic and restitution 0. Joint damping, spring constants and contact pairs are specified below and in `scene.json`. Explicit inertias/centers of mass override shape-derived values where present. Extended handling tabs are part of the bench fixture, not a claim of commercial-product fidelity.

| Body | Material/type | Mass kg | Envelope m | World origin m | XYZW | Constraint |
|---|---|---:|---|---|---|---|
| `controller` | rigid engineering plastic | 0.18 | (0.13, 0.132, 0.032) | (0.29, 0, 0.7475) | (0, 0, 0, 1) | anchored |
| `cover` | rigid engineering plastic | 0.06 | (0.126, 0.307, 0.0285) | (0.29, 0, 0.7815) | (0, 0, 0, 1) | passive dynamic |
| `contact_0` | rigid engineering plastic | 0.002 | (0.002, 0.014, 0.013) | (0.2645, -0.033, 0.76275) | (0, 0, 0, 1) | passive dynamic |
| `contact_1` | rigid engineering plastic | 0.002 | (0.002, 0.014, 0.013) | (0.3155, 0.033, 0.76275) | (0, 0, 0, 1) | passive dynamic |
| `used_cell_tray` | rigid engineering plastic | 0.5 | (0.144, 0.104, 0.04) | (0.39, -0.24, 0.7475) | (0, 0, 0, 1) | anchored |
| `old_cell_0` | rigid AA cell surrogate; no electrical or chemical simulation | 0.024 | (0.0518, 0.0145, 0.0145) | (0.29, -0.033, 0.76275) | (0, 0, 0, 1) | passive dynamic |
| `new_cell_0` | rigid AA cell surrogate; no electrical or chemical simulation | 0.024 | (0.0518, 0.0145, 0.0145) | (0.16, -0.24, 0.75495) | (0, 0, 0, 1) | passive dynamic |
| `old_cell_1` | rigid AA cell surrogate; no electrical or chemical simulation | 0.024 | (0.0518, 0.0145, 0.0145) | (0.29, 0.033, 0.76275) | (0, 0, 1, 6.12323e-17) | passive dynamic |
| `new_cell_1` | rigid AA cell surrogate; no electrical or chemical simulation | 0.024 | (0.0518, 0.0145, 0.0145) | (0.24, -0.24, 0.75495) | (0, 0, 1, 6.12323e-17) | passive dynamic |

| `new_cell_staging_rails` | rigid engineering plastic | 0.08 | (0.138, 0.032, 0.006) | (0.2, -0.24, 0.7475) | (0, 0, 0, 1) | anchored |

## Passive joints

- `cover_slide`: prismatic X, `controller` to `cover`; limits [0, 0.11]; stiffness 2.5, damping 0.1. Full joint frames are in `scene.json`.
- `spring_0`: prismatic X, `controller` to `contact_0`; limits [-0.002, 0]; stiffness 200, damping 0.4. Full joint frames are in `scene.json`.
- `spring_1`: prismatic X, `controller` to `contact_1`; limits [0, 0.002]; stiffness 200, damping 0.4. Full joint frames are in `scene.json`.

## Mass distribution overrides



Four 6 mm-high staging rails bound lateral rolling of the two fresh cells. The central 24 mm opening provides gripper clearance.
