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

The shaft-entry phase retains measured-body translation and centroid-compensated orientation feedback through insertion. The earlier rigid-grasp transform allowed the collar to tilt while changing from supported carry to insertion. Angular corrections are capped at 0.02 rad with gain 0.3, while loaded translational lead remains 2.5 mm. A separate assembled fixture checks passive full-score stability before further robot trials.

Custom collar/shaft/key assets use 64 position and 16 velocity solver iterations with a 0.005 sleep threshold at the unchanged 240 Hz physics rate. The prior assembled fixtures satisfied every pose/hinge condition but raw contact-induced angular motion repeatedly exceeded the unchanged 0.2 rad/s stillness bound. The stricter solver candidate requires native confirmation. Robot drive limits and scoring thresholds are unchanged.

All custom rigid links, including links inside articulated fixtures, receive0.1 linear and0.5 angular damping and a0.5m/s depenetration cap. Existing64/16solver iterations and raw0.01m/s,0.2rad/s scoring bounds remain. The next assembled fixture tests the complete coupled assembly again.

Before radial shaft entry the lower collar aligns within1mm position and0.01rad attitude. During upward entry axial progress requires at most1mm transverse error and0.015rad attitude error. Actual prior cold insertion drifted11mm horizontally and0.15rad in attitude. The5mm axial target lead gives at most0.5mm reference progress per20Hz command with the existing nested gain, respecting the10mm/s insertion speed. Objective fit, hinge and key limits remain unchanged.

Open the collar hinge to -1.30 rad before transport. At the earlier -1.0 rad command, actual native upper-half contact with the captive shaft prevented alignment; a recorded-root geometry sweep found only 0.283 mm clearance versus 4.006 mm at -1.30 rad. These are offline estimates. Fresh native robot-control validation is required; hinge limits and scoring remain unchanged.

The upper-handle grasp adds 10 degrees of world-Z yaw. Offline continuous IK at the open-collar lift changes wrist reference from 1.953 to 1.778 rad, preserving margin for the natively observed loaded-root tilt while retaining the -1.30 rad shaft-clearance opening. Full native validation is required; geometry and score thresholds are unchanged.

The open-collar phase allows 40 simulated seconds within the unchanged overall action limit. The measured loaded hinge advanced monotonically at about 0.0355 rad/s near the former 30-second deadline and was 0.1126 rad short of the unchanged -1.30 rad target. This bounded duration increase permits that observed motion; it does not relax joint position, contact, solver, preservation or scoring gates.

The upper-handle grasp uses 20 degrees of outward yaw, superseding the earlier 10-degree candidate. At the exact recorded loaded-lift failure target, the original right wrist clips at 2.0944 rad; the new orientation solves at 1.9263 rad with 0.1681 rad minimum margin. The captured-pose regression preserves the hardware limit and convergence gates. This numerical margin still requires cold native validation.


Supporting-arm tracking revision (2026-11-12): relative holds now retain an explicit measured-pose feedback gain. The upper-collar support uses gain 2 during lower-collar translation; carry speed is bounded to 12.5 mm/s. This corrects inactive-arm routing, without changing scene, joint stops or scoring. Offline controller tests pass; native validation remains required. Earlier native failure hit the hinge opening stop before lower-body tilt; shaft contact was not established by that evidence.


Deeper lower-handle grasp (2026-11-12): measured e083 traces lost the lower support at54.8 simulated seconds during lifting. Exact749-action reconstruction found the saved upper relative target differed by only0.183 mm and1.00 mrad at the handoff, so that target was not blamed without evidence. Actual-pose URDF mesh analysis found only7.5 mm of lower-handle vertical pad overlap. Lower TCP offset is now0 mm instead of+10 mm relative to the lower body, yielding16.65/17.48 mm pad overlap and19.10 mm minimum table clearance in offline IK/mesh checks. Native grip stability remains unproven until rerun. Separate opening-case expectation now matches the existing-1.30 rad controller goal (-1.33..-1.27); scene, torque limits and scoring are unchanged.


Cooperative carry correction (2026-11-12): source6d84833 retained deeper lower-pad contact but still failed Grasp slipped during lift. Exact801-action reconstruction of its first lift command showed19.34 mm and40.61 mrad relative command inconsistency: the active arm targeted an incremental future lower-collar pose while the upper support tracked the old measured lower pose. Coordinated lower-body carry now sends both grippers targets from the same planned incremental rigid-body transform, preserving the stored open-hinge relative grasp. Applied only to three lower-collar carry phases. Cartesian rate bounds, joint limits, torque limits, scoring, scene and measured-slip guards are unchanged. A recorded-state regression fails before the correction and verifies relative target invariance afterward, including no mutation of the physics frame. Native validation is still required.


Near-goal carry and insertion (2026-11-12): d38 completed the lift in1.4simseconds, then timed out at71.5sim while oscillating around the unchanged1mm carry goal. Last10seconds:200samples,38insidegoal,max2consecutiveinside (too short for0.15secondhold), errors0.445–2.063mm. Body command gain8 overshot a recorded0.952mm error to6.661mm in one proposed target. Carry gain is now1 so near-goal parent targets contract toward the goal; tolerances and time budgets unchanged. Coordinated relative holds also use the insertion branch's gated lateral/axial correction, preventing the support from advancing while axial alignment is blocked. Two regression tests fail the prior behavior and pass the correction. No physics, force, joint-limit or scoring changes. Native success remains to be established.
