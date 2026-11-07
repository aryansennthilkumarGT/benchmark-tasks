# Preload and retain a twelve-cell service pack — physical setup

Bimanual YAM station; x forward, y left, z up; metres/kg/radians; XYZW quaternions. Tabletop z=0.7475 m. Fixed layout, seed 0, no object jitter. 

Geometry is original primitive construction. All movable components use friction 0.65 static / 0.5 dynamic and restitution 0. Joint damping, spring constants and contact pairs are specified below and in `scene.json`. Explicit inertias/centers of mass override shape-derived values where present. Extended handling tabs are part of the bench fixture, not a claim of commercial-product fidelity.

| Body | Material/type | Mass kg | Envelope m | World origin m | XYZW | Constraint |
|---|---|---:|---|---|---|---|
| `holder` | rigid engineering plastic | 0.7 | (0.31, 0.166, 0.0845) | (0.225, 0, 0.7475) | (0, 0, 0, 1) | anchored |
| `contact_0` | rigid engineering plastic | 0.002 | (0.012, 0.012, 0.002) | (0.1, -0.028, 0.7555) | (0, 0, 0, 1) | passive dynamic |
| `contact_1` | rigid engineering plastic | 0.002 | (0.012, 0.012, 0.002) | (0.15, -0.028, 0.7555) | (0, 0, 0, 1) | passive dynamic |
| `contact_2` | rigid engineering plastic | 0.002 | (0.012, 0.012, 0.002) | (0.2, -0.028, 0.7555) | (0, 0, 0, 1) | passive dynamic |
| `contact_3` | rigid engineering plastic | 0.002 | (0.012, 0.012, 0.002) | (0.25, -0.028, 0.7555) | (0, 0, 0, 1) | passive dynamic |
| `contact_4` | rigid engineering plastic | 0.002 | (0.012, 0.012, 0.002) | (0.3, -0.028, 0.7555) | (0, 0, 0, 1) | passive dynamic |
| `contact_5` | rigid engineering plastic | 0.002 | (0.012, 0.012, 0.002) | (0.35, -0.028, 0.7555) | (0, 0, 0, 1) | passive dynamic |
| `contact_6` | rigid engineering plastic | 0.002 | (0.012, 0.012, 0.002) | (0.1, 0.028, 0.7555) | (0, 0, 0, 1) | passive dynamic |
| `contact_7` | rigid engineering plastic | 0.002 | (0.012, 0.012, 0.002) | (0.15, 0.028, 0.7555) | (0, 0, 0, 1) | passive dynamic |
| `contact_8` | rigid engineering plastic | 0.002 | (0.012, 0.012, 0.002) | (0.2, 0.028, 0.7555) | (0, 0, 0, 1) | passive dynamic |
| `contact_9` | rigid engineering plastic | 0.002 | (0.012, 0.012, 0.002) | (0.25, 0.028, 0.7555) | (0, 0, 0, 1) | passive dynamic |
| `contact_10` | rigid engineering plastic | 0.002 | (0.012, 0.012, 0.002) | (0.3, 0.028, 0.7555) | (0, 0, 0, 1) | passive dynamic |
| `contact_11` | rigid engineering plastic | 0.002 | (0.012, 0.012, 0.002) | (0.35, 0.028, 0.7555) | (0, 0, 0, 1) | passive dynamic |
| `cell_0` | rigid AA cell surrogate; no electrical or chemical simulation | 0.024 | (0.0145, 0.0145, 0.0518) | (0.16, -0.17, 0.77295) | (0, 0, 0, 1) | passive dynamic |
| `cell_1` | rigid AA cell surrogate; no electrical or chemical simulation | 0.024 | (0.0145, 0.0145, 0.0518) | (0.21, -0.17, 0.77425) | (1, 0, 0, 6.12323e-17) | passive dynamic |
| `cell_2` | rigid AA cell surrogate; no electrical or chemical simulation | 0.024 | (0.0145, 0.0145, 0.0518) | (0.26, -0.17, 0.77295) | (0, 0, 0, 1) | passive dynamic |
| `cell_3` | rigid AA cell surrogate; no electrical or chemical simulation | 0.024 | (0.0145, 0.0145, 0.0518) | (0.31, -0.17, 0.77425) | (1, 0, 0, 6.12323e-17) | passive dynamic |
| `cell_4` | rigid AA cell surrogate; no electrical or chemical simulation | 0.024 | (0.0145, 0.0145, 0.0518) | (0.36, -0.17, 0.77295) | (0, 0, 0, 1) | passive dynamic |
| `cell_5` | rigid AA cell surrogate; no electrical or chemical simulation | 0.024 | (0.0145, 0.0145, 0.0518) | (0.41, -0.17, 0.77425) | (1, 0, 0, 6.12323e-17) | passive dynamic |
| `cell_6` | rigid AA cell surrogate; no electrical or chemical simulation | 0.024 | (0.0145, 0.0145, 0.0518) | (0.16, 0.11, 0.77295) | (0, 0, 0, 1) | passive dynamic |
| `cell_7` | rigid AA cell surrogate; no electrical or chemical simulation | 0.024 | (0.0145, 0.0145, 0.0518) | (0.21, 0.11, 0.77425) | (1, 0, 0, 6.12323e-17) | passive dynamic |
| `cell_8` | rigid AA cell surrogate; no electrical or chemical simulation | 0.024 | (0.0145, 0.0145, 0.0518) | (0.26, 0.11, 0.77295) | (0, 0, 0, 1) | passive dynamic |
| `cell_9` | rigid AA cell surrogate; no electrical or chemical simulation | 0.024 | (0.0145, 0.0145, 0.0518) | (0.31, 0.11, 0.77425) | (1, 0, 0, 6.12323e-17) | passive dynamic |
| `cell_10` | rigid AA cell surrogate; no electrical or chemical simulation | 0.024 | (0.0145, 0.0145, 0.0518) | (0.36, 0.11, 0.77295) | (0, 0, 0, 1) | passive dynamic |
| `cell_11` | rigid AA cell surrogate; no electrical or chemical simulation | 0.024 | (0.0145, 0.0145, 0.0518) | (0.41, 0.11, 0.77425) | (1, 0, 0, 6.12323e-17) | passive dynamic |
| `retaining_plate` | rigid engineering plastic | 0.18 | (0.308, 0.114, 0.0487) | (0.285, 0.23, 0.7515) | (0, 0, 0, 1) | passive dynamic |
| `capture_key` | rigid fixture material | 0.08 | (0.014, 0.156, 0.014) | (0.385, -0.24, 0.7547) | (0, 0, 0, 1) | passive dynamic |

## Passive joints

- `contact_spring_0`: prismatic Z, `holder` to `contact_0`; limits [-0.002, 0]; stiffness 500, damping 0.5. Full joint frames are in `scene.json`.
- `contact_spring_1`: prismatic Z, `holder` to `contact_1`; limits [-0.002, 0]; stiffness 500, damping 0.5. Full joint frames are in `scene.json`.
- `contact_spring_2`: prismatic Z, `holder` to `contact_2`; limits [-0.002, 0]; stiffness 500, damping 0.5. Full joint frames are in `scene.json`.
- `contact_spring_3`: prismatic Z, `holder` to `contact_3`; limits [-0.002, 0]; stiffness 500, damping 0.5. Full joint frames are in `scene.json`.
- `contact_spring_4`: prismatic Z, `holder` to `contact_4`; limits [-0.002, 0]; stiffness 500, damping 0.5. Full joint frames are in `scene.json`.
- `contact_spring_5`: prismatic Z, `holder` to `contact_5`; limits [-0.002, 0]; stiffness 500, damping 0.5. Full joint frames are in `scene.json`.
- `contact_spring_6`: prismatic Z, `holder` to `contact_6`; limits [-0.002, 0]; stiffness 500, damping 0.5. Full joint frames are in `scene.json`.
- `contact_spring_7`: prismatic Z, `holder` to `contact_7`; limits [-0.002, 0]; stiffness 500, damping 0.5. Full joint frames are in `scene.json`.
- `contact_spring_8`: prismatic Z, `holder` to `contact_8`; limits [-0.002, 0]; stiffness 500, damping 0.5. Full joint frames are in `scene.json`.
- `contact_spring_9`: prismatic Z, `holder` to `contact_9`; limits [-0.002, 0]; stiffness 500, damping 0.5. Full joint frames are in `scene.json`.
- `contact_spring_10`: prismatic Z, `holder` to `contact_10`; limits [-0.002, 0]; stiffness 500, damping 0.5. Full joint frames are in `scene.json`.
- `contact_spring_11`: prismatic Z, `holder` to `contact_11`; limits [-0.002, 0]; stiffness 500, damping 0.5. Full joint frames are in `scene.json`.

## Mass distribution overrides


