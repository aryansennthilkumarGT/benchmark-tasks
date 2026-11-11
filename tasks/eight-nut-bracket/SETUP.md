# Fasten a spring-loaded access plate while maintaining its preload — physical setup

Bimanual YAM station; x forward, y left, z up; metres/kg/radians; XYZW quaternions. Tabletop z=0.7475 m. Fixed layout, seed 0, no object jitter. 

Geometry is original primitive construction. All movable components use friction 0.65 static / 0.5 dynamic and restitution 0. Joint damping, spring constants and contact pairs are specified below and in `scene.json`. Explicit inertias/centers of mass override shape-derived values where present. Extended handling tabs are part of the bench fixture, not a claim of commercial-product fidelity.

| Body | Material/type | Mass kg | Envelope m | World origin m | XYZW | Constraint |
|---|---|---:|---|---|---|---|
| `bracket` | steel plate and threaded studs | 0.6 | (0.25, 0.17, 0.0385) | (0.265, 0, 0.7515) | (0, 0, 0, 1) | anchored |
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

Each threaded stud has a 7.7 mm radius guide core over the lower 23 mm and a 7.0 mm radius lead-in over the upper 3 mm. The narrower lead-in helps center a nut at entry, and the larger core limits lateral travel when the plate loads a seated nut. The helical tooth geometry sets the pitch.

The stud thread flanks extend to a nominal radius of 9.05 mm. Nut shell panels retain the 17 mm outer radius and provide 9.4 mm internal clearance. The female thread flanks retain their original pitch and radial position.

The eight light nut bodies enable PhysX speculative continuous collision detection for the thin thread flanks. This contact-quality setting is recorded in each generated USD. [NVIDIA collision tuning guidance](https://github.com/NVIDIA-Omniverse/PhysX/blob/main/ovphysx/docs/guides/collision_tuning.md).

The square-thread approximation uses 4 mm lead, 1.70 mm axial ridge thickness and 16 contact sectors per turn. Nominal mating backlash is 0.60 mm. Female crest radius is 8.15 mm around a 7.70 mm stud core, with 0.90 mm male/female radial engagement. Internal thread clocking is -67.5 degrees with a -0.15 mm axial offset, matching the authored entry and loaded fixture phases. The previous 1-mm flanks allowed 2-mm nominal axial backlash, and 0.5-mm radial engagement was smaller than the 0.85-mm core clearance. This candidate needs full native validation.

Each stud has a cylindrical entry pilot of radius 7.95 mm extending from local z=27 to38.5 mm. The helical load-bearing flanks retain their 4 mm pitch and original geometry. The pilot has 0.20 mm nominal radial clearance to the female crest and supports the nut axis during early regrasping before a full thread turn is engaged. A native gravity probe starts from the predicted90degree pose derived from the measured45degree pose and4mm pitch and checks at most0.60mm axial settling and at most0.06rad tilt.


The female helical ridges are now0.20mm lower relative to the nut body. This reduces initial axial freeplay. The previous90degree gravity probe settled0.682mm, exceeding the unchanged0.60mm native retention bound and0.65mm scoring coupling slack. The thread has4mm pitch,1.70mm flanks and0.60mm nominal backlash. The native retention bound is0.60mm and scoring coupling slack is0.65mm. The revised geometry requires fresh native gravity and actual robot-threading validation.
