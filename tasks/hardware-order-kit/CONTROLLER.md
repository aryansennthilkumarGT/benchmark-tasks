# Feedback controller

The privileged scripted expert reads measured bodies, joints and robot proprioception. Dream receives the unmodified official cameras and robot joint observations. Both send the same 14 absolute joint/gripper targets at 20 Hz. No controller code writes body transforms, attaches objects or changes score state.

Each action uses measured-joint warm-start IK, <=3 mm Cartesian increments, <=0.045 rad per joint step and <=0.10 gripper increments. Approach completes before finger closure. Jaw width, body-relative grasp slip, lift or displacement, joint progress, and insertion stall checks control phase transitions. Holds follow measured parent frames where specified. Threading uses 45-degree turns with opening, wrist unwind and regrasp, checking measured pitch advancement. Minor body misalignment is corrected incrementally; a 2 s stalled insertion or failed grasp aborts rather than applying unbounded force or retries.

Offline nominal path checks sample actual URDF convex collision pieces for table and opposite-arm intersections every ten ideal controls, plus phase endpoints; critical grasp and first/last thread sweep checks include task fixtures. Full robot-to-fixture trajectories and deformable cable dynamics still require native validation. Sampling is not continuous collision certification.

| Phase | Arm | Operation | Measured completion |
|---:|---|---|---|
| 0 | left | move | Approach lower collar handle |
| 1 | left | grasp | Support lower collar |
| 2 | right | move | Approach upper collar handle |
| 3 | right | grasp | Grasp upper collar handle |
| 4 | right | joint | Open the split collar |
| 5 | left | carry | Lift the open collar |
| 6 | left | carry | Bring open collar beneath captive shaft |
| 7 | left | insert | Lift lower half around the shaft |
| 8 | right | joint | Close upper half over the shaft |
| 9 | right | release | Release closed upper collar |
| 10 | right | move | Clear upper handle |
| 11 | right | move | Approach transverse key head |
| 12 | right | grasp | Grasp transverse key head |
| 13 | right | carry | Lift transverse key |
| 14 | right | carry | Align key in front of the three lugs |
| 15 | right | insert | Pass key through interleaved lugs |
| 16 | right | release | Release seated transverse key |
| 17 | right | move | Lift above captive shaft |
| 18 | right | move | Retreat past shaft flange |
| 19 | right | move | Clear retained collar |
| 20 | left | release | Release lower collar support |
| 21 | right | move | Withdraw right arm |
| 22 | left | move | Withdraw left arm |
| 23 | left | hold | Observe released terminal stability |

The trajectory audit checks the official convex robot meshes against anchored fixture bodies, the table and the other arm every ten controls and at segment endpoints. It does not certify moving fixture, payload, flexible cable or inter-sample collision clearance. Grasp and thread sweeps separately check task geometry at specified samples. All are ideal kinematic checks, not physical execution.

After the motion plan, the expert holds the released pose while the actual scorer establishes full-score stability. It stops only on measured success or fails after a bounded five-second terminal grace period (or hold time plus two seconds, if longer). A finished phase list is not a success signal.

The first two native placement prefixes opened the collar, then timed out during lift. Measured lower-half pitch was about 0.16 rad while the nominal carry demanded a level body. The lift and transfer now use measured TCP translation feedback independently of the desired body orientation. Revolute commands also derive their bounded lead from measured child pose and the captured grasp. Regression checks cover both corrections. Native validation is pending.

A +30-degree pre-tilted upper grasp failed the full offline reach audit and was rejected. The original upper-handle path had minimum joint margin 0.00744 rad. A reach sweep with the handle 60 mm inward gave minimum margin 0.20247 rad across the same critical poses. The upper handling extension is shortened to y=-0.16 m, retaining the downward grasp and two-handed controller. Full static and native validation are required.

The shortened-handle scene passed 12/12 native physics cases. Placement telemetry repeated the lift joint-limit failure after the lower collar drifted approximately 27 mm sideways. Carry feedback now uses gain 8 and a 20-mm measured-TCP lead cap, with 0.08-rad tracking windows on both supporting arms. The first failed placement repeat was recorded; redundant repeats were deliberately stopped, exit 143. New native placement validation is pending.

The carry-gain probe lifted the collar approximately 25.3 mm and reached within 1.34 mm of its target in the first repeat. It timed out with approximately 0.28-rad body tilt. Lower-collar carrying now uses measured body-rotation feedback, gain 3 and a 0.08-rad angular lead cap, matching the cooler controller that achieved about 0.016-rad orientation error in native execution. Placement validation is pending.

Measured rotation correction also moves the offset grasp around the observed body centroid. This compensates the handle lever during reorientation. The previous fixed-TCP correction drove the supporting wrist into its joint limit. This candidate uses unit angular gain capped at 0.04 radians per target, with native retesting required. Joint-limit failures include the active arm base and solved joint values.

Loaded carries integrate actual TCP pose error into the rate-limited reference at gain 2 per second. The centroid-compensated native test avoided the earlier wrist limit and retained a 0.279-radian loaded angular residual at lift timeout. This candidate reuses measured-pose reference feedback validated by the twelve-cell control suite. Native collar validation remains required.


Loaded insertions use a2.5mm task-space lead and gain2 reference integration. This carries the actuator load compensation from transfer into shaft and key insertion. The earlier insertion switched to a0.5mm proportional target and lost the measured loaded pose. Fresh native insertion probes must validate this revision.
