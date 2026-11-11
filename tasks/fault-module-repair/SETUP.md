# Balance and lock a counterweighted service arm — physical setup

Bimanual YAM station; x forward, y left, z up; metres/kg/radians; XYZW quaternions. Tabletop z=0.7475 m. Fixed layout, seed 0, no object jitter. 

Geometry is original primitive construction. All movable components use friction 0.65 static / 0.5 dynamic and restitution 0. Joint damping, spring constants and contact pairs are specified below and in `scene.json`. Explicit inertias/centers of mass override shape-derived values where present. Extended handling tabs are part of the bench fixture, not a claim of commercial-product fidelity.

| Body | Material/type | Mass kg | Envelope m | Authored zero-joint origin m | Authored XYZW | Constraint |
|---|---|---:|---|---|---|---|
| `pedestal` | rigid fixture material | 1.2 | (0.13, 0.12, 0.104) | (0.285, 0, 0.7475) | (0, 0, 0, 1) | anchored |
| `service_arm` | rigid fixture material | 0.36 | (0.29, 0.246, 0.063) | (0.285, 0, 0.8475) | (0, 0, 0, 1) | passive dynamic |
| `counterweight` | rigid fixture material | 0.3 | (0.044, 0.098, 0.0855) | (0.25, 0, 0.8675) | (0, 0, 0, 1) | passive dynamic |
| `locking_pin` | rigid fixture material | 0.025 | (0.022, 0.022, 0.064) | (0.32, -0.24, 0.7757) | (0, 0, 0, 1) | passive dynamic |
| `pin_stand` | rigid fixture material | 0.12 | (0.022, 0.022, 0.014) | (0.32, -0.24, 0.7475) | (0, 0, 0, 1) | anchored |

The lower pin receiver has an 18 mm-deep, 10 mm square bearing section and a 4 mm chamfered entry, 22 mm total depth. Its entry opens to 14 mm. The upper receiver has a 4 mm-deep 10 by 11.4 mm bearing and a 4 mm chamfered entry opening to 14 by 15.4 mm. The chamfers use inclined rigid collision faces. The pin has a 9.4 mm square shaft and an 8 mm square lead.

## Starting configuration

The body table lists authored zero-joint link frames. Native reset sets `arm_pivot` to +0.3 rad and `weight_slide` to 0 m, then settles the free pin on its stand. The observed first frame places the service-arm origin at (0.285000, 0, 0.847500) m with XYZW (0, 0.149438, 0, 0.988771), and the counterweight origin at (0.257474, 0, 0.876950) m with the same orientation. The pin settles near (0.320001, -0.240002, 0.775500) m. Numerical settling variation is checked within 3 mm across resets. The setup screenshot must show this tilted starting configuration.

The material is a rigid-contact surrogate with the stated friction, restitution, mass and explicit inertia. These coefficients specify the simulated material. Commercial alloy composition and compliant contact behavior are outside the modeled fidelity.

## Passive joints

- `arm_pivot`: revolute Y, `pedestal` to `service_arm`; limits [-0.3, 0.3]; stiffness 0, damping 0.004. Full joint frames are in `scene.json`.
- `weight_slide`: prismatic X, `service_arm` to `counterweight`; limits [-0.075, 0]; stiffness 0, damping 0.02, static sliding resistance 0.24 N and dynamic resistance 0.12 N in PhysX. Full joint frames are in `scene.json`.

## Mass distribution overrides

- `service_arm`: center of mass [0.0595833333333333, 0, -0.006]; diagonal inertia [0.0008, 0.0024, 0.0025].
- `counterweight`: center of mass [0, 0, -0.046]; diagonal inertia [0.00022, 0.00016, 0.00018].

Material names describe rigid mechanical surrogates. Explicit lumped masses, centres of mass and inertias define their dynamics. The common contact coefficients are static friction 0.65, dynamic friction 0.5 and restitution 0.
