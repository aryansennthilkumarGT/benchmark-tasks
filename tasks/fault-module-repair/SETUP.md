# Balance and lock a counterweighted service arm — physical setup

Bimanual YAM station; x forward, y left, z up; metres/kg/radians; XYZW quaternions. Tabletop z=0.7475 m. Fixed layout, seed 0, no object jitter. 

Geometry is original primitive construction. All movable components use friction 0.65 static / 0.5 dynamic and restitution 0. Joint damping, spring constants and contact pairs are specified below and in `scene.json`. Explicit inertias/centers of mass override shape-derived values where present. Extended handling tabs are part of the bench fixture, not a claim of commercial-product fidelity.

| Body | Material/type | Mass kg | Envelope m | World origin m | XYZW | Constraint |
|---|---|---:|---|---|---|---|
| `pedestal` | rigid fixture material | 1.2 | (0.13, 0.12, 0.104) | (0.285, 0, 0.7475) | (0, 0, 0, 1) | anchored |
| `service_arm` | rigid fixture material | 0.36 | (0.29, 0.246, 0.047) | (0.285, 0, 0.8475) | (0, 0, 0, 1) | passive dynamic |
| `counterweight` | rigid fixture material | 0.3 | (0.044, 0.098, 0.0855) | (0.25, 0, 0.8675) | (0, 0, 0, 1) | passive dynamic |
| `locking_pin` | rigid fixture material | 0.025 | (0.022, 0.022, 0.064) | (0.32, -0.24, 0.7757) | (0, 0, 0, 1) | passive dynamic |
| `pin_stand` | rigid fixture material | 0.12 | (0.022, 0.022, 0.014) | (0.32, -0.24, 0.7475) | (0, 0, 0, 1) | anchored |

## Passive joints

- `arm_pivot`: revolute Y, `pedestal` to `service_arm`; limits [-0.3, 0.3]; stiffness 0, damping 0.004. Full joint frames are in `scene.json`.
- `weight_slide`: prismatic X, `service_arm` to `counterweight`; limits [-0.075, 0]; stiffness 0, damping 0.02. Full joint frames are in `scene.json`.

## Mass distribution overrides

- `service_arm`: center of mass [0.0595833333333333, 0, -0.006]; diagonal inertia [0.0008, 0.0024, 0.0025].
- `counterweight`: center of mass [0, 0, -0.03]; diagonal inertia [0.00022, 0.00016, 0.00018].
