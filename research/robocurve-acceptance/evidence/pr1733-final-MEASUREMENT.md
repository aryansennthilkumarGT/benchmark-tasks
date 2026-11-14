# Noncontact measurement of all twelve terminal springs

This specifies physical judging access for a real-world build. It is a build and measurement design, not a claim that a physical fixture or photograph was tested. The native simulation and its recorded trials retain the original solid, opaque wall geometry. The judging-only optical details below are omitted from the rendering; no native transparent-wall execution is claimed.

## Physical build details

Use the holder coordinate system in `scene.json`: Z=0 is the tabletop/base underside; the base plate is 6 mm thick. Contact discs are 12 mm diameter and 2 mm thick. At the defined zero-travel stop, each disc centre is Z=8.000 mm. Each disc moves only along Z. In the physical base, provide a12.4 mm diameter,1.2 mm deep blind clearance recess under each disc, without cutting through the6 mm base. Its floor is Z=4.8 mm, leaving0.2 mm clearance even at the full2 mm travel stop. The native prismatic joint filters parent/disc collisions to approximate this internal clearance; the blind recess is omitted from its parent collision mesh.

There are two rows, Y=-28 and +28 mm. In each row, the six contact X coordinates are -125,-75,-25,25,75,125 mm. Contacts0–5 are the negative-Y row; contacts6–11 are the positive-Y row. Judge each row from its nearest outer side.

Provide a flush, optically clear 16 mm wide by6 mm high patch at each contact X, extending from Z=6 to12 mm, in BOTH walls between that contact and its nearest outer side:

| Wall | Centre Y | Thickness |
| --- | --- | --- |
| Outer holder wall | -57 or +57 mm | 6 mm |
| Outer wall of the individual cell guide | -37.7 or +37.7 mm | 4 mm |

Use a rigid, bonded transparent insert or a locally transparent wall of the same thickness. Preserve the wall's original inner and outer surfaces. These are solid windows, not holes: do not remove a cell seat, guide surface, base or rail, and do not create a new route for a finger or cell. The rest of the guide remains opaque. Window optical properties are a physical judging provision; simulator contact/friction properties remain an approximation, as disclosed in `task.json`.

Put a thin circumferential witness line at the exact midheight of each orange contact disc's cylindrical side. Specify a0.05 mm line width; use the line centre for readings. It adds no moving part or contact load. A middle line is used because the cell covers the disc's top face. At the maximum accepted compression the line is at Z=6.2 mm, above the6 mm base; it remains below the cell's bottom edge.

For each disc, rigidly mount a0.5 mm wide reference-scale strip to the holder, not to the spring or cell. Its X centre is7 mm to the positive-X side of the contact centre. Put its marked face in the same viewing plane as the disc's nearest cylindrical tangent: Y=-34 mm for the negative row, +34 mm for the positive row. Mark heights6–10 mm with0.1 mm divisions and labelled8.000 mm zero-travel datum. This strip lies beside the disc and outside the cell's circular footprint. It must not touch the cell, plate, disc or spring. Mark the two acceptance heights6.20 and7.65 mm explicitly. Use neutral contact numbers, not identifying text.

Before loading the fixed starting layout, use the contact's defined zero-travel mechanical stop to calibrate the8.000 mm witness datum and photograph each scale. Do not define zero from an arbitrary gravity-deflected unloaded equilibrium. Remove any calibration restraint before loading; no calibration restraint is present during the trial. Then reproduce the fully loaded starting layout in `SETUP.md`.

## Readings after the robot releases the assembly

Leave the holder fixed to the table and leave the plate, key and all cells untouched. Take twelve macro photographs through the clear patches, one per terminal. Move only the external camera or inspection mirror. If a camera cannot sit at the low witness height, use a20 mm inspection mirror on an independent stand outside the holder to turn a horizontal view upward to the camera. No mirror or tool enters the holder or contacts a task object.

The optical ray through the windows must be horizontal and normal to their faces. The witness and reference scale are coplanar, so both appear at the same image scale. Calibrate pixels per millimetre from that terminal's reference strip in the same photograph; do not use a ruler taped to the outer wall at a different depth. Require at least50 image pixels per millimetre, resolve the witness-line centre to0.05 mm or better, and retain the original images and pixel readings. Photograph at greater magnification if focus, glare, a cell edge or a reflection obscures a line. Do not infer a compression from the plate height, cell height or a neighbouring spring.

For contact i, let h_i be the photographed witness height above the base datum, in millimetres. Its compression is

    c_i = 8.000 - h_i

Thus the existing inclusive compression requirement0.35≤c_i≤1.80 mm is exactly6.20≤h_i≤7.65 mm. No scoring threshold changes. A compression of0.50 mm, for example, has a witness height7.50 mm. Record all twelve values independently; the twelve0.04 groups still require their other pose and stability conditions.

Do not round an out-of-range value into the interval. If the measurement uncertainty crosses a threshold, take a sharper, more magnified photograph of the unchanged assembly before awarding that group. The numerical rule remains the same; uncertain photographs do not widen it. Capture the required one-second hands-clear/stable interval on video as before. Still photographs assess displacement, not the temporal stability condition.

`MEASUREMENT_GEOMETRY.json` records the twelve coordinate checks against all69 original holder boxes. It identifies both required optical patches per sightline and reports no other fixed-holder obstruction at the accepted extreme heights and zero datum. This is an analytical access check, not physical photograph validation or a new simulation rollout.
