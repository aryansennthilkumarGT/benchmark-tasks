# Physical scoring specification

This protocol grades the **representative contact coupon**, not an official RoboCurve task. All tolerances below are authored experimental criteria, not Toshiba specifications. [scoring.py](toshiba/scoring.py) accepts only externally meaningful measurements; it receives no case name, installed flag, command count or target joint value.

Initial state: carrier already in the source-role recess, tray free and unengaged 30 mm above the nominal seat; input drive at rest. The coupon isolates the final landing and functioning assembly, not a complete robot policy. Incorrect controls change actual initial pose, components or support geometry. No post-initialization state assignment places the tray into its final seat.

Before the drive-only test, measure:

- Tray centre height within 0.4 mm of the authored 14.5 mm nominal, offset under 2 mm and tilt under 1 degree.
- Correct face up, all three actual wheel contacts supporting the tray, and no external support contact.

Then mechanically turn the **input shaft** at low speed through slightly more than a complete revolution, without touching the tray. Full score 1.0 additionally requires:

- Tray turns more than 2π radians; its accumulated angle differs from the input by less than 0.25 rad, accommodating the authored coupling backlash.
- Tray remains seated within 0.5 mm/1.2 degrees, with all three supports and no external prop.
- Each wheel's relative marker moves by more than 0.05 rad, so a tray sliding on jammed wheels cannot masquerade as rolling support.

Partial 0.25 is available for three-wheel, right-way-up, released support without complete transmission/rolling. Wrong-face, externally supported, missing-support or proud unstable configurations earn 0. Cracked/damaged real hardware is invalid regardless of pose; the current rigid simulation cannot validate damage thresholds.

## Measurement without hidden simulator flags

Use a ruler/depth gauge and three perimeter height measurements; side photographs/feeler slips confirm wheel contact. Paint marks on tray, input shaft and wheel faces plus video give rotation and relative wheel motion. A level/fiducial gives tilt. Observe hands/support withdrawal. Normal-force logs are diagnostic only; a physical trial need not reproduce an internal contact index.

On an authored open bench coupon the input shaft can be turned mechanically while isolated from electricity. **Do not assume the original microwave motor is low voltage or energize an appliance.** Access for these observations/drive isolation on the actual Toshiba donor remains unverified and is a prerequisite to any donor-specific task.

Seat/support is checked **before** the drive test: the source requires correct installation before use, and a test motor must not repair an initially proud assembly and hide that error. Rotation alone is insufficient—both wrong-phase and missing-carrier controls can transmit rotation in this model while failing the actual support/seat outcome.

## YUBI and Faze4

No completed physical scorer is claimed for either failed candidate. YUBI's eight required band-installation controls were not executed because Stage1 did not pass. Faze4's geometric diagnostics inspect actual profile clearance, component counts and hole-centre engagement, but nominal closure failed; no full physical assembly score is asserted. Neither an 11:1-like numerical angle nor a near-target pose rescues those failures.
