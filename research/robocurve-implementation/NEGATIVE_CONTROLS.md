# Negative controls actually executed

## Passing representative contact coupon

The correct case earns 1.0. Every incorrect case below earns less than 1.0. Partial 0.25 means genuine released, right-way-up three-point support without the complete function; it is not a successful installation.

|Control|Observed physical result|Unit score|
|---|---|---:|
|wrong_phase|Rests proud on drive features; no three-wheel support before test, even though rotation transfers.|0.00|
|missing_carrier|Tray can rotate on the shaft but lacks the mandatory three-point carrier support.|0.00|
|missing_drive|Correct support height but virtually zero driven output.|0.25|
|missing_wheel|Only two wheel contacts and altered height/tilt.|0.00|
|inverted_tray|Wrong face and no keyed transmission; no invalid-orientation partial credit.|0.00|
|held_proud|Actual external support blocks contact the tray; released seating fails.|0.00|
|displaced_carrier|Incorrect support/height despite substantial driven rotation.|0.00|
|seized_wheels|Wheel bodies fixed to the carrier; no relative wheel motion and no full driven function.|0.25|

Additional falsifier: lowering the authored drive-arm top to 7 mm eliminates the required overlap; the result is 0.25 rather than false full credit. Nominal 9/10/11 mm arrangements work in this chosen section. These are not manufacturer ranges.

## Debugging that mattered

- A 9-second drive command initially stopped before an output revolution. The final protocol ends on actual input stroke, not on a prescribed output angle.
- An attempted high-friction wheel control did not actually lock its joints. It was replaced by physical fixed axles; relative wheel-marker motion is independently checked.
- An early partial-credit branch incorrectly admitted an upside-down tray. The final observation scorer explicitly requires the correct normal/tilt even for partial support credit.
- The first door rotation sign opened inward. Canonical access results use the corrected outward left-hinged door. Invalid captures are isolated under debug/ and are not passing evidence.

## Failed candidates are not passed negative-control suites

YUBI: source occupancy and bounded access failed; correct installation, missing band, one-hook capture, wrong groove, robot-held band, slack loop, jam and escape tests are **NOT RUN**, because fabricating an installed-band model would bypass Stage1.

Faze4: actual missing-profile/pair, one-layer carrier and phase perturbations were geometrically evaluated, but **nominal closure itself failed**. They are diagnostic rejected states, not a validated full assembly scorer or successful robot experiment. Cover/axial and robot gates remain unpassed.
