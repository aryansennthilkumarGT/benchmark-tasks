# Setup

Press the grey access plate level against its marked height while turning the three orange nuts down their studs. Keep the plate controlled as the nuts capture its spring load. Seat every nut against the plate, then withdraw both hands; the plate must remain level and compressed.

All dimensions use metres, masses use kg, and quaternions use XYZW. Tabletop z=0.7475. The station uses two YAM arms with parallel grippers. Fixed seed0 and zero jitter reproduce the layout.

| Body | Material | Mass | Envelope | Initial position | Quaternion |
| --- | --- | --- | --- | --- | --- |
| bracket | steel plate and threaded studs | 0.6 | (0.25, 0.17, 0.047) | (0.265, 0, 0.7515000000000001) | (0.0, 0.0, 0.0, 1.0) |
| plate_carrier | rigid material | 0.001 | (0.001, 0.001, 0.001) | (0.265, 0, 0.7735000000000001) | (0, 0, 0, 1) |
| plate_gimbal | rigid material | 0.001 | (0.001, 0.001, 0.001) | (0.265, 0, 0.7735000000000001) | (0, 0, 0, 1) |
| pressure_plate | rigid material | 0.12 | (0.25, 0.266, 0.032) | (0.265, 0, 0.7735000000000001) | (0, 0, 0, 1) |
| nut_0 | coarse threaded steel surrogate | 0.024 | (0.034, 0.034, 0.01) | (0.15, -0.18, 0.7527) | (0.0, 0.0, 0.0, 1.0) |
| nut_1 | coarse threaded steel surrogate | 0.024 | (0.034, 0.034, 0.01) | (0.36, -0.18, 0.7527) | (0.0, 0.0, 0.0, 1.0) |
| nut_2 | coarse threaded steel surrogate | 0.024 | (0.034, 0.034, 0.01) | (0.22, 0.23, 0.7527) | (0.0, 0.0, 0.0, 1.0) |

The fixed bracket retains three threaded studs at local x,y=(-0.09,-0.05),(0.09,-0.05),(-0.03,0.05). The guided plate has one vertical spring and two passive tilt joints. Unused holes in the plate remain part of its original geometry. Full shape dimensions, joint axes, stops, spring constants and materials are enumerated in scene.json.

Each stud has a4mm-pitch rigid square-profile thread with16contact sectors per turn and an8mm conical lead-in over an8.05mm-radius guide. The guide assists active alignment. A passive offset drop is a negative control for thread engagement.

Reset each nut to its declared source pose, restore the plate joints, and clear all accumulated thread history. No consumables are used. The expert and model move only through robot actions. Initialized mechanism fixtures are diagnostic tests.
