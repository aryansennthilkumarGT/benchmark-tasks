# Feedback controller

The privileged scripted expert reads measured bodies, joints and robot proprioception. Dream receives the unmodified official cameras and robot joint observations. Both send the same 14 absolute joint/gripper targets at 20 Hz. No controller code writes body transforms, attaches objects or changes score state.

Each action uses measured-joint warm-start IK, <=3 mm Cartesian increments, <=0.045 rad per joint step and <=0.10 gripper increments. Approach completes before finger closure. Jaw width, body-relative grasp slip, lift or displacement, joint progress, and insertion stall checks control phase transitions. Holds follow measured parent frames where specified. Threading uses 45-degree turns with opening, wrist unwind and regrasp, checking measured pitch advancement. Minor body misalignment is corrected incrementally; a 2 s stalled insertion or failed grasp aborts rather than applying unbounded force or retries.

Offline nominal path checks sample actual URDF convex collision pieces for table and opposite-arm intersections every ten ideal controls, plus phase endpoints; critical grasp and first/last thread sweep checks include task fixtures. Full robot-to-fixture trajectories and deformable cable dynamics still require native validation. Sampling is not continuous collision certification.

| Phase | Arm | Operation | Measured completion |
|---:|---|---|---|
| 0 | left | move | Approach lid handle |
| 1 | left | grasp | Grasp raised lid handle |
| 2 | left | joint | Open and support the gravity lid |
| 3 | right | move | Approach drive handle |
| 4 | right | grasp | Grasp drive by its raised handle |
| 5 | right | carry | Lift and verify the drive grasp |
| 6 | right | carry | Move ahead of guide entrances |
| 7 | right | carry | Align with horizontal guide channels |
| 8 | right | insert | Advance drive along capped channels |
| 9 | right | release | Release seated drive |
| 10 | right | move | Clear the drive entrance |
| 11 | right | move | Approach retaining bar |
| 12 | right | grasp | Grasp retaining bar across its narrow dimension |
| 13 | right | carry | Lift and verify retaining bar |
| 14 | right | carry | Align retaining bar above both pockets |
| 15 | right | insert | Lower retaining bar into pockets |
| 16 | right | release | Release bar into supporting pockets |
| 17 | right | move | Lift clear of retainer pockets |
| 18 | right | move | Clear the closing lid |
| 19 | left | joint | Close lid to capture retaining bar |
| 20 | left | release | Release lid handle |
| 21 | left | move | Withdraw left arm |
| 22 | left | hold | Verify released mechanism is stable |

The trajectory audit checks the official convex robot meshes against anchored fixture bodies, the table and the other arm every ten controls and at segment endpoints. It does not certify moving fixture, payload, flexible cable or inter-sample collision clearance. Grasp and thread sweeps separately check task geometry at specified samples. All are ideal kinematic checks, not physical execution.

After the motion plan, the expert holds the released pose while the actual scorer establishes full-score stability. It stops only on measured success or fails after a bounded five-second terminal grace period (or hold time plus two seconds, if longer). A finished phase list is not a success signal.

The left arm uses a 0.12 rad bounded tracking-error window while supporting the gravity lid. Its IK reference advances by at most 0.02 rad per control. The lid-following lead is 0.035 rad, and native failure records include reference joints and applied actuator torques.

The measured chassis failure at lid angle 0.419 rad had about 0.895 rad wrist/body orientation drift and approached the wrist joint limit. The revolute controller now derives its bounded lead from the measured body pose and captured grasp transform. A stationary mechanism therefore produces the same desired wrist pose on repeated controls. This targeted correction requires native retesting.

The measured-body correction removed the wrist-limit failure, but both native repeats stalled near 0.018 rad under the lid load. The next candidate uses gain 8 on measured hinge error with a bounded 0.08-rad body-angle lead. This increases the finite lifting reference while retaining the original joint-rate, collision, grip and timeout guards. Native validation remains pending.

Gain 8 reached 0.84362 rad of the 0.85-rad opening target, leaving 0.00638 rad residual against the 0.006-rad phase completion tolerance. Gain 12 is the next bounded control candidate, with the same 0.08-rad lead cap and measured completion predicate. Native retesting is pending.

Gain 12 held the lid between 0.84285 and 0.84966 rad late in the native opening attempt. The 6-mrad arrival band persisted for only three consecutive 20-Hz frames, preventing the 0.15-second phase hold. The opening controller now uses a 0.01-rad arrival band about 0.85 rad, within the native 0.82–0.88-rad opening assertion. The measured support and complete-task demonstrations remain required.

Two native drive-lift probes timed out with the drive sliding on the table. Measured right-arm reference gaps stayed below 0.025 rad at failure, and the largest arm torque was approximately 5.71 Nm. Drive carrying now uses measured TCP translation with body-error gain 8 and a 20-mm lead cap. The right-arm tracking window is 0.08 rad. Native retesting is pending.

Measured-TCP carrying lifted the drive approximately 83 mm in the first native repeat, reaching within 1.36 mm of its waypoint at timeout. Millimetre-scale motion prevented the 1.5-mm arrival band from staying satisfied for 0.15 seconds. Free-space drive carries now use a 4-mm arrival band. The independent native lift assertion remains 60–110 mm. Insertion and objective scoring use their declared conditions. Native retesting is pending.

The revised drive lift passed both native control repeats. The full expert reached insertion, then lost height and drifted laterally before entering the rails. Guided insertion now aligns transverse position and body orientation before positive-X motion. The elliptical gate has 0.6-mm lateral and 1.5-mm vertical radii, with a 0.01-rad orientation limit. Measured corrections use lateral gain 8, a 20-mm lateral lead cap, 4-mm axial lead and bounded 0.04-rad wrist correction. Axial and transverse progress retain independent best measurements. A new robot probe tests seating, release and withdrawal against the actual carrier_seated score predicate. Native validation is pending.

Guided channel insertion uses unit-gain measured lateral and angular correction at 20 Hz, with 2 mm lateral and 1 mm axial lead caps. The previous gain-eight experiment oscillated across the lateral entry gate and failed its bounded stall detector. Alignment gates and stall checks remain active in this candidate. Native retesting is required.

Guided insertion now uses the measured-pose reference feedback already validated on the twelve-cell grasp probe and switch catch-release probe. Gain 2 per second integrates actual TCP error into the rate-limited IK reference and preserves its loaded tracking bias. The two purely proportional alignment experiments failed through oscillation or loss of vertical support. Native channel insertion remains pending for this candidate.

The measured insertion stop at carrier root x≈0.170 m matched the first upright face at x=0.220 m minus the 50 mm flange-front offset. An aligned geometric probe confirmed flange/upright interference. The revised uprights provide a physical flange underpass and the caps provide finite lateral body clearance. A strict aligned-path regression checks all chassis/carrier box pairs through the full insertion path. Native mechanism, retention and robot insertion tests are required for this geometry revision.

The 7 mm cap experiment failed the vertical-shortcut height assertion while the carrier remained tilted. The revised candidate restores 3 mm flange capture overlap and creates lateral clearance by using a 74 mm main carrier body. The flange underpass remains part of the geometry. Guided entry requires transverse error within 0.25 mm horizontally and 1 mm vertically, with orientation error at most 0.008 radians. Both the strict clear-path regression and native shortcut/retention tests must pass.

Loaded carries also use measured-pose reference feedback to compensate the known YAM tracking offset. Retainer insertion aligns horizontally before descending through the guide uprights, with independent transverse/axial progress tracking and the existing bounded stall guard. Native validation is required.


The horizontal guide waypoint is z=0.764 m. The floor top is0.7555 m and the drive half-height is8 mm, giving a passive resting centre of0.7635 m. The waypoint leaves0.5 mm nominal floor clearance and stays within the unchanged3 mm scoring radius. Guided transverse feedback gain is2 with2 mm lead. The75-second insertion timeout remains bounded by measured-progress checks and the180-second trial limit.


The insertion gate projects the actual rotated110 by74 by16mm core into world y. Its centre offset plus projected half-width must fit within the38mm inner half-width with0.1mm margin. This couples yaw and lateral alignment. The0.03rad attitude bound and1.5mm vertical gate keep the flanges below the770.5mm underpass. Fresh native insertion tests must verify the resulting controller.


The loaded right-arm reference window is0.16rad. Its maximum reference increment is0.02rad per action. A10N·m/rad wrist stiffness produces a1.6N·m proportional component at the window threshold, within the7N·m native wrist effort limit. The earlier0.08rad window approached saturation while the actual carrier stayed tilted against the floor. Native insertion and command/proprioception traces must verify load compensation.

Guide entry uses body-centre z 0.766 m. At the existing 0.03 rad pitch bound, the 110 by 74 by 16 mm core stays at least 0.85 mm above the 0.7555 m floor leading edge. The prior 0.764 m waypoint allowed the tilted leading corner to catch the floor lip. Angular improvement now contributes to bounded insertion progress while axial motion waits for alignment. Final scoring poses and tolerances are unchanged.

The right drive grasp tilts25degrees toward the fixture while preserving the Y-axis jaw closure. Native GPU contact tensors measured right robot link4 pressing the supported lid, with a peak force about6.8N, near drive x0.243m. All measured external right-arm contacts involved the lid. The tilt moves the wrist/forearm away from the lid without changing the fixture, closure geometry, guide clearance or scoring. Critical TCP audits now match the actual0.766m insertion waypoint.

After releasing the drive, the right hand lifts vertically with its25degree grasp orientation. It changes orientation at the following high-clearance bar approach. The earlier simultaneous lift/unwind path intersected a keeper post by2.28mm in the offline mesh audit.

Retainer transport first moves longitudinally at the source y=-0.23 m to x=0.235 m, then moves transversely toward the supporting pockets. Actual native GPU contacts measured approximately17 N between the right fingertip and the supported lid on the prior diagonal path. The new segmented route clears the leading lid edge before crossing its side plane. Physical clearances require fresh native confirmation.

Retainer grip pitches the wrist25degrees away from the supported lid, while preserving the opposing jaw grip. Offline convex-mesh checks found the former vertical wrist collides with the lid at both final insertion height and the diagonal path. The pitched grip clears the complete sampled height range and uses the same numeric seating goals. Fresh native contacts and cold experts remain required.

The pitched retainer grasp uses a16mm centre-to-TCP offset and20to30mm measured jaw interval, accounting for the projected18by16mm bar section. Actual jaw closure and retention are validated in the native expert.

The cold expert reached the retaining-bar grasp with a real19.08mm occupied jaw width. The20mm lower bound prevented completion. The measured interval is now16to28mm, with the same physical contact, slip and verified-lift requirements. Objective seating and retention tolerances are unchanged.

The retainer candidate rolls the wrist outward 25 degrees about the world X jaw-closing axis, rather than pitching that axis out of the bar-face normal. The closing normal remains horizontal and parallel to the narrow bar faces. This is an offline grasp-stability hypothesis and needs native qualification. Mechanism geometry and all objective predicates remain unchanged.

The parallel-jaw rolled grasp uses measured TCP feedback gain 2/s during the bar grasp. Native suffix testing left the bar stationary but settled TCP 1.78 mm from the target, outside the unchanged 1.5 mm pre-close gate; feedback corrects this actuator bias instead of opening the precision tolerance.
