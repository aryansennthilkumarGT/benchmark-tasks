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

Material clarification: bracket, studs and nuts are steel rigid surrogates; the pressure plate is an aluminium rigid surrogate. Masses and friction coefficients are estimates, not calibrated material data. plate_carrier and plate_gimbal are1g noncolliding inertia/coordinate links representing the spring guide and two tilt axes, not additional manipulated1mm workpieces. Their visualization bounds must not be interpreted as physical collision envelopes.


### Custom mating thread dimensions

These are enlarged custom square-profile threads, without an ISO metric designation. Stud core radius7.70mm, external thread nominal crest radius9.05mm, nut internal thread crest radius8.15mm and nut-body inscribed bore radius9.40mm give0.90mm nominal radial flank overlap. The8.05mm guide radius clears the internal crest by0.10mm; the stud core clears it by0.45mm. Both mating helices advance4.00mm per turn, using16rigid sectors per turn with1.70mm axial teeth and0.60mm nominal axial backlash. External rectangular sector corners reach about9.208mm radius, still within the9.40mm nut root. Thus bore clearance does not substitute for thread engagement. Thread flanks are collision facets, not a virtual helical attachment or score-triggered snap; contact fidelity and manufacturing tolerances remain approximate.
