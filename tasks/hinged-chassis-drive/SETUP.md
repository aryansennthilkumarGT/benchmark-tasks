# Install and retain a drive under a gravity-closing lid — physical setup

Bimanual YAM station; x forward, y left, z up; metres/kg/radians; XYZW quaternions. Tabletop z=0.7475 m. Fixed layout, seed 0, no object jitter. 

Geometry is original primitive construction. All movable components use friction 0.65 static / 0.5 dynamic and restitution 0. Joint damping, spring constants and contact pairs are specified below and in `scene.json`. Explicit inertias/centers of mass override shape-derived values where present. Extended handling tabs are part of the bench fixture, not a claim of commercial-product fidelity.

| Body | Material/type | Mass kg | Envelope m | World origin m | XYZW | Constraint |
|---|---|---:|---|---|---|---|
| `chassis` | aluminium | 0.9 | (0.22, 0.18, 0.06) | (0.3, 0, 0.7475) | (0, 0, 0, 1) | anchored |
| `lid` | rigid aluminium proxy | 0.67 | (0.208, 0.247, 0.067) | (0.4, 0, 0.8115) | (0, 0, 0, 1) | passive dynamic |
| `drive` | aluminium carrier with plastic handle | 0.22 | (0.11, 0.082, 0.037) | (0.22, -0.24, 0.7557) | (0, 0, 0, 1) | passive dynamic |
| `retainer` | rigid engineering plastic | 0.06 | (0.018, 0.095, 0.016) | (0.36, -0.23, 0.7557) | (0, 0, 0, 1) | passive dynamic |

The lid includes two 18 by 16 by 26 mm underside ribs over the seated retainer. Each leaves 2 mm nominal vertical clearance before engaging under upward load.

## Passive joints

- `lid_hinge`: revolute Y, `chassis` to `lid`; limits [0.0, 1.35]; stiffness 0.0, damping 0.003. Full joint frames are in `scene.json`.

## Mass distribution overrides



## Guide and upright clearance

The two rail caps have local centres (18, ±43, 26) mm and size 144×7×4 mm. Their inner edges provide 1.5 mm lateral clearance per side for the 76 mm carrier body and overlap each carrier flange by 1.5 mm. Four retaining-bar guide uprights have local centres (-78, ±47, 36.5) mm and (-52, ±47, 36.5) mm, each sized 4×15×27 mm. Their bottoms are 23 mm above the chassis origin, providing 3 mm vertical clearance above the travelling carrier flanges at the nominal 18 mm carrier-centre height. The original fixed chassis frame and scene coordinates define these local measurements.
