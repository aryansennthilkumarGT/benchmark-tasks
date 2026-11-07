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
