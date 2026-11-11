# Feedback controller

The privileged scripted expert reads measured bodies, joints and robot proprioception. Dream receives the unmodified official cameras and robot joint observations. Both send the same 14 absolute joint/gripper targets at 20 Hz. No controller code writes body transforms, attaches objects or changes score state.

Each action uses measured-joint warm-start IK, <=3 mm Cartesian increments, <=0.045 rad per joint step and <=0.10 gripper increments. Approach completes before finger closure. Jaw width, body-relative grasp slip, lift or displacement, joint progress, and insertion stall checks control phase transitions. Holds follow measured parent frames where specified. Threading uses 45-degree turns with opening, wrist unwind and regrasp, checking measured pitch advancement. Minor body misalignment is corrected incrementally; a 2 s stalled insertion or failed grasp aborts rather than applying unbounded force or retries.

Offline nominal path checks sample actual URDF convex collision pieces for table and opposite-arm intersections every ten ideal controls, plus phase endpoints; critical grasp and first/last thread sweep checks include task fixtures. Full robot-to-fixture trajectories and deformable cable dynamics still require native validation. Sampling is not continuous collision certification.

| Phase | Arm | Operation | Measured completion |
|---:|---|---|---|
| 0 | left | move | Approach inclined lid handle |
| 1 | left | grasp | Grasp lid handle |
| 2 | left | joint | Open and support service lid |
| 3 | right | move | Approach old_cooler |
| 4 | right | grasp | Grasp old_cooler |
| 5 | right | carry | Verify lift of old_cooler |
| 6 | right | carry | Draw cooling shroud clear of the lid |
| 7 | right | carry | Lift clear of enclosure |
| 8 | right | carry | Clear the lid before crossing toward the tray |
| 9 | right | carry | Transport old_cooler |
| 10 | right | insert | Seat old_cooler |
| 11 | right | release | Release old_cooler |
| 12 | right | move | Withdraw from old_cooler |
| 13 | right | move | Approach storage pull handle |
| 14 | right | grasp | Grasp storage pull handle |
| 15 | right | insert | Withdraw storage through guide mouths |
| 16 | right | carry | Verify extracted storage lift |
| 17 | right | carry | Transport removed storage |
| 18 | right | insert | Place removed storage in tray |
| 19 | right | release | Release old storage |
| 20 | right | move | Clear collection tray |
| 21 | right | move | Approach replacement storage |
| 22 | right | grasp | Grasp replacement storage |
| 23 | right | carry | Lift replacement storage |
| 24 | right | carry | Move ahead of storage rails |
| 25 | right | carry | Align with storage rails |
| 26 | right | insert | Insert storage beneath guide caps |
| 27 | right | release | Release new storage |
| 28 | right | move | Lift clear of storage rails |
| 29 | right | move | Clear storage handle |
| 30 | right | move | Approach new_cooler |
| 31 | right | grasp | Grasp new_cooler |
| 32 | right | carry | Verify lift of new_cooler |
| 33 | right | carry | Transport new_cooler |
| 34 | right | carry | Lower replacement ahead of open enclosure |
| 35 | right | carry | Move replacement under the supported lid |
| 36 | right | insert | Seat new_cooler |
| 37 | right | release | Release new_cooler |
| 38 | right | move | Withdraw from new_cooler |
| 39 | right | move | Clear service lid |
| 40 | left | joint | Close lid over keyed cooling module |
| 41 | left | release | Release closed lid |
| 42 | left | move | Withdraw inclined left grasp |
| 43 | left | hold | Observe released service assembly |

The trajectory audit checks the official convex robot meshes against anchored fixture bodies, the table and the other arm every ten controls and at segment endpoints. It does not certify moving fixture, payload, flexible cable or inter-sample collision clearance. Grasp and thread sweeps separately check task geometry at specified samples. All are ideal kinematic checks, not physical execution.

After the motion plan, the expert holds the released pose while the actual scorer establishes full-score stability. It stops only on measured success or fails after a bounded five-second terminal grace period (or hold time plus two seconds, if longer). A finished phase list is not a success signal.

The native cooler grasp stopped about 4.93 mm above its moving TCP target with a fingertip against the extension plate. A vertical wrist candidate intersected the supported lid in offline geometry and was rejected. The next candidate retains the inclined wrist and raises the grasp center by 6 mm within the existing 20-mm-high tab. Physical validation is pending.

The raised cooler grasp succeeded in native control, then lift stalled near its original height. The next right-arm payload profile uses a 0.10-rad tracking window and measured carry translation gain 8 with a 25-mm reference lead cap. Cartesian/joint reference rate limits and vendor actuator limits bound the physical actions. Completion requires measured body goals, lift, slip and scoring checks. Native payload validation is pending.

The telemetry probes lifted the cooling shroud approximately 26.4 mm and 31.2 mm, then missed the transient waypoint arrival band. The first repeat had approximately 0.123-rad pitch. The lift-verification phase now permits 10-mm target-position error and 0.15-rad tilt while requiring at least 25-mm measured vertical displacement. The native independent displacement assertion remains 25–50 mm. Later alignment and scoring are evaluated by their own numeric conditions. Native retesting is pending.

The full expert repeated the lift failure despite both native prefix passes. Its cooler tilted approximately 0.26 rad under the cantilevered grasp. Cooler carries now apply measured body-orientation feedback to the actual wrist, with gain 3 and a 0.08-rad angular lead cap. Vendor joint rate and torque limits constrain the resulting commands. Failure and optional per-action records now include synchronized measured joints. Native validation is pending.

Measured rotation feedback passed both lift probes and reduced full-expert cooler orientation error to about 0.016 rad. The next transit stopped with approximately 3.2-mm position error against its 1.5-mm band. Cooler transit waypoints now use 4-mm arrival tolerance. Insertion phases integrate body-position error into the rate-limited reference with per-step gain 0.1 and a 0.5-mm cap, and use measured rotation feedback through placement. The removed cooler is placed at 0.1-rad positive-Y tilt before release. Loaded-grasp IK converged below 1 micrometre with 0.246-rad minimum joint margin; offline convex checks found no robot/fixture surface within 0.6 mm or object penetration above 0.3 mm. A new real robot probe verifies collection before storage removal. Native validation is pending.

Cooler reorientation compensates the measured grasp lever about the body centroid, with unit angular gain and a 0.04-radian correction cap. This candidate addresses coupling between orientation correction and translation of the offset lifting tab. The previous cooler collection test passed its positional arrival band and failed orientation. Native collection is being retested.

Loaded cooler carries use measured-pose reference feedback at gain 2 per second, integrating actual TCP position and orientation error within existing motion-rate and joint-tracking caps. The native collar experiment retained a load-dependent angular residual after centroid compensation, motivating this reuse of the native-validated twelve-cell feedback. Node inserts continue using their explicit bounded body-error reference integration. Native validation of this carry candidate is required.
