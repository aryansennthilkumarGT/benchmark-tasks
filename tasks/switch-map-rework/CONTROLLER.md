# Feedback controller

The privileged scripted expert reads measured bodies, joints and robot proprioception. Dream receives the unmodified official cameras and robot joint observations. Both send the same 14 absolute joint/gripper targets at 20 Hz. No controller code writes body transforms, attaches objects or changes score state.

Each action uses measured-joint warm-start IK, <=3 mm Cartesian increments, <=0.045 rad per joint step and <=0.10 gripper increments. Approach completes before finger closure. Jaw width, body-relative grasp slip, lift or displacement, joint progress, and insertion stall checks control phase transitions. Holds follow measured parent frames where specified. Threading uses 45-degree turns with opening, wrist unwind and regrasp, checking measured pitch advancement. Minor body misalignment is corrected incrementally; a 2 s stalled insertion or failed grasp aborts rather than applying unbounded force or retries.

Offline nominal path checks sample actual URDF convex collision pieces for table and opposite-arm intersections every ten ideal controls, plus phase endpoints; critical grasp and first/last thread sweep checks include task fixtures. Full robot-to-fixture trajectories and deformable cable dynamics still require native validation. Sampling is not continuous collision certification.

| Phase | Arm | Operation | Measured completion |
|---:|---|---|---|
| 0 | right | move | Approach plug 0 |
| 1 | right | grasp | Grasp plug 0 |
| 2 | left | move | Approach release paddle 0 |
| 3 | left | grasp | Grasp release paddle 0 |
| 4 | left | joint | Depress catch 0 |
| 5 | right | insert | Withdraw blue plug past the catch |
| 6 | left | release | Release catch 0 |
| 7 | left | move | Clear catch 0 |
| 8 | right | carry | Lift blue plug toward parking cradle |
| 9 | right | carry | Move blue plug to parking cradle |
| 10 | right | insert | Lower blue plug onto parking cradle |
| 11 | right | release | Release parked blue plug |
| 12 | right | move | Clear parked blue plug |
| 13 | right | move | Approach plug 1 |
| 14 | right | grasp | Grasp plug 1 |
| 15 | left | move | Approach release paddle 1 |
| 16 | left | grasp | Grasp release paddle 1 |
| 17 | left | joint | Depress catch 1 |
| 18 | right | insert | Withdraw orange plug past the catch |
| 19 | right | carry | Lift orange lead with its catch supported |
| 20 | right | carry | Move orange lead to matching port |
| 21 | right | carry | Align orange plug at port mouth |
| 22 | right | insert | Insert orange plug beneath the catch lip |
| 23 | left | release | Release catch 1 |
| 24 | left | move | Clear catch 1 |
| 25 | right | release | Release correctly latched orange plug |
| 26 | right | move | Clear orange connector |
| 27 | right | move | Approach plug 0 |
| 28 | right | grasp | Grasp plug 0 |
| 29 | left | move | Approach release paddle 0 |
| 30 | left | grasp | Grasp release paddle 0 |
| 31 | left | joint | Depress catch 0 |
| 32 | right | carry | Lift parked blue plug |
| 33 | right | carry | Move blue plug to its matching port |
| 34 | right | carry | Align blue plug at port mouth |
| 35 | right | insert | Insert blue plug beneath catch lip |
| 36 | left | release | Release catch 0 |
| 37 | left | move | Clear catch 0 |
| 38 | right | release | Release correctly latched blue plug |
| 39 | right | move | Withdraw right arm |
| 40 | left | move | Withdraw left arm |
| 41 | left | hold | Observe released terminal stability |

The trajectory audit checks the official convex robot meshes against anchored fixture bodies, the table and the other arm every ten controls and at segment endpoints. It does not certify moving fixture, payload, flexible cable or inter-sample collision clearance. Grasp and thread sweeps separately check task geometry at specified samples. All are ideal kinematic checks, not physical execution.

After the motion plan, the expert holds the released pose while the actual scorer establishes full-score stability. It stops only on measured success or fails after a bounded five-second terminal grace period (or hold time plus two seconds, if longer). A finished phase list is not a success signal.

The prior three-axis interior gimbal model produced nonfinite cable state during reset after positive-inertia correction. A lower-complexity candidate coalesces coincident interior proxy masses and retains two bending axes per segment plus all three terminal connector axes. Contact geometry, cable length and total assembly mass are preserved. This is a changed torsion approximation with native validation pending.

Native approach stopped 2.391 mm from its clearance waypoint with wrist orientation error below 0.04 rad. Measured-pose convex geometry found no robot/task surfaces within 2 mm. The three plug clearance approaches use 3-mm arrival tolerance. Each following grasp uses its measured-body target and fingertip closure verification. Native retesting is pending.

Plug approach and grasp passed the next native control probe. The release-paddle clearance approach stopped 2.255 mm from its target, with measured convex geometry showing no task/robot surfaces within 2 mm. Those three paddle clearance approaches now use 3-mm arrival tolerance. The diagnostic was deliberately terminated after its first recorded failure, exit 143, to advance independent work. Its partial report establishes no successful full suite. Native retesting is pending.

Both approaches and grasps passed the next native trial, then the catch reached approximately 2.14 mm against its 5.5-mm target while the plug rotated under paddle load. Plug grasp phases lacked keep_hold, causing the inactive supporting arm to follow its measured pose. All three right-arm plug grasps now establish a fixed support target, and right-arm releases clear that hold. A redundant press repeat was stopped deliberately, exit 143. Synchronized failure joints, references and torques are recorded for the next native test.

The fixed-support catch trace reached 3.143-mm peak compression and averaged 2.696 mm, with no samples in the 5.5±0.35-mm target band. The capped run exited 124 after its first recorded failure. Catch pressing now integrates joint error into the reference with per-step gain 0.1 and a 0.25-mm cap. Absolute move/grasp targets use the measured-pose feedback validated by the fourth-cell native probe. Right-arm plug operations refresh measured world-pose holds, which use pose feedback during inactive support and clear on release. This prevents a later left-arm action from returning the plug to an earlier hold point. Native validation is pending.
