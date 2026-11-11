# Exchange two internal modules and close out an enclosure — physical setup

Bimanual YAM station; x forward, y left, z up; metres/kg/radians; XYZW quaternions. Tabletop z=0.7475 m. Fixed layout, seed 0, no object jitter. 

Geometry is original primitive construction. All movable components use friction 0.65 static / 0.5 dynamic and restitution 0. Joint damping, spring constants and contact pairs are specified below and in `scene.json`. Explicit inertias/centers of mass override shape-derived values where present. Extended handling tabs are part of the bench fixture, not a claim of commercial-product fidelity.

| Body | Material/type | Mass kg | Envelope m | World origin m | XYZW | Constraint |
|---|---|---:|---|---|---|---|
| `chassis` | aluminium | 0.9 | (0.22, 0.18, 0.06) | (0.3, 0, 0.7475) | (0, 0, 0, 1) | anchored |
| `lid` | rigid engineering plastic | 0.18 | (0.208, 0.174, 0.045) | (0.4, 0, 0.8265) | (0, 0, 0, 1) | passive dynamic |
| `old_storage` | rigid engineering plastic | 0.12 | (0.152, 0.05, 0.053) | (0.3, 0, 0.7655) | (0, 0, 0, 1) | passive dynamic |
| `old_cooler` | rigid engineering plastic | 0.22 | (0.138, 0.124, 0.045) | (0.3, 0, 0.7955) | (0, 0, 0, 1) | passive dynamic |
| `new_storage` | rigid engineering plastic | 0.12 | (0.152, 0.05, 0.053) | (0.24, -0.28, 0.7977) | (0, 0, 0, 1) | passive dynamic |
| `new_cooler` | rigid engineering plastic | 0.22 | (0.138, 0.124, 0.045) | (0.25, -0.17, 0.7707) | (0, 0, 0, 1) | passive dynamic |
| `removed_parts` | rigid engineering plastic | 0.5 | (0.186, 0.214, 0.04) | (0.4, -0.225, 0.7475) | (0, 0, 0, 1) | anchored |
| `storage_source_stand` | rigid fixture material | 0.18 | (0.12, 0.07, 0.042) | (0.24, -0.28, 0.7475) | (0, 0, 0, 1) | anchored |

A 24 by 44 by 4 mm lid pad sits above the cooler handle with 2 mm nominal clearance.

## Passive joints

- `lid_hinge`: revolute Y, `chassis` to `lid`; limits [0.0, 1.35]; stiffness 0.0, damping 0.003. Full joint frames are in `scene.json`.

## Mass distribution overrides



A second 24 by 64 by 13 mm pad spans the far cooler fins with 3 mm nominal clearance. The two pads restrict upward translation and pitching of a seated cooler.


Both storage sleds have a connected raised pull grip centred90 mm forward and35 mm above the sled origin. The grip is14 by28 by20 mm. A45 by18 by12 mm horizontal neck and14 by18 by35 mm upright connect it to the sled. This clears the measured angled gripper/floor interference. The taller grips require fresh dependent-removal, lid-clearance, scoring and robot-control validation.


Each storage sled retains the original14 by28 by20mm low lug centred at local(-65,0,12)mm. That lug engages the cooling-shroud lip and blocks premature withdrawal. The new raised pull grip provides robot access while preserving this physical dependent-removal constraint. The prior raised-grip revision failed both shroud-blocking force probes, and that failure remains in the execution evidence.
