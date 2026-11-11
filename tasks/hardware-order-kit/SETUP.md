# Fit and pin a hinged collar around a captive shaft — physical setup

Bimanual YAM station; x forward, y left, z up; metres/kg/radians; XYZW quaternions. Tabletop z=0.7475 m. Fixed layout, seed 0, no object jitter. 

Geometry is original primitive construction. All movable components use friction 0.65 static / 0.5 dynamic and restitution 0. Joint damping, spring constants and contact pairs are specified below and in `scene.json`. Explicit inertias/centers of mass override shape-derived values where present. Extended handling tabs are part of the bench fixture, not a claim of commercial-product fidelity.

| Body | Material/type | Mass kg | Envelope m | World origin m | XYZW | Constraint |
|---|---|---:|---|---|---|---|
| `captive_shaft` | rigid fixture material | 1.2 | (0.052, 0.25, 0.101) | (0.33, 0, 0.8225) | (0, 0, 0, 1) | anchored |
| `lower_collar` | rigid fixture material | 0.12 | (0.12, 0.208, 0.0481299) | (0.185, 0, 0.7717) | (0, 0, 0, 1) | passive dynamic |
| `upper_collar` | rigid fixture material | 0.1 | (0.16, 0.208, 0.074) | (0.185, 0, 0.7717) | (0, 0, 0, 1) | passive dynamic |
| `collar_key` | rigid fixture material | 0.025 | (0.022, 0.093, 0.022) | (0.36, -0.24, 0.7587) | (0, 0, 0, 1) | passive dynamic |

The shaft has a 2.4 mm wide, 180 mm long locating rib on top. The groove between the upper collar arc segments mates with this rib to constrain rotation around the shaft after closure.

## Passive joints

- `collar_hinge`: revolute Y, `lower_collar` to `upper_collar`; limits [-1.35, 0]; stiffness 0, damping 0.002. Full joint frames are in `scene.json`.

## Mass distribution overrides



The rectangular retaining-key bores are 10 mm wide and 9.6 mm high around the 8 mm square key. The key fit is measured in the lower collar frame, with collar position and angle measured against the shaft.

The upper handling tab is centered at local (0.07, -0.16, 0.025) m. Its support is a 16 by 160 by 12 mm bar centered at (0.07, -0.08, 0.018) m. The orange tab measures 18 by 28 by 24 mm.


The lower and upper grip centres are now90mm from the collar midplane along opposite shaft-axis directions. Lower handle stem length is93mm and upper stem length is90mm. Body masses remain120g and100g. This reduces off-axis load moments during unsupported bimanual transfer. The offline open/close wrist samples now match the actual1rad opening command. Fresh native closure and load-retention checks remain required.
