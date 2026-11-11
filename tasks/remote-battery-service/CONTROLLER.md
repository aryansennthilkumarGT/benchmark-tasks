# Feedback controller

The privileged scripted expert reads measured bodies, joints and robot proprioception. Dream receives the unmodified official cameras and robot joint observations. Both send the same 14 absolute joint/gripper targets at 20 Hz. No controller code writes body transforms, attaches objects or changes score state.

Each action uses measured-joint warm-start IK, <=3 mm Cartesian increments, <=0.045 rad per joint step and <=0.10 gripper increments. Approach completes before finger closure. Jaw width, body-relative grasp slip, lift or displacement, joint progress, and insertion stall checks control phase transitions. Holds follow measured parent frames where specified. Threading uses 45-degree turns with opening, wrist unwind and regrasp, checking measured pitch advancement. Minor body misalignment is corrected incrementally; a 2 s stalled insertion or failed grasp aborts rather than applying unbounded force or retries.

Offline nominal path checks sample actual URDF convex collision pieces for table and opposite-arm intersections every ten ideal controls, plus phase endpoints; critical grasp and first/last thread sweep checks include task fixtures. Full robot-to-fixture trajectories and deformable cable dynamics still require native validation. Sampling is not continuous collision certification.

| Phase | Arm | Operation | Measured completion |
|---:|---|---|---|
| 0 | left | move | Approach cover handle |
| 1 | left | grasp | Grasp cover handle |
| 2 | left | joint | Slide cover open and support it |
| 3 | right | move | Approach old_cell_0 |
| 4 | right | grasp | Grasp old_cell_0 |
| 5 | right | carry | Verify lift of old_cell_0 |
| 6 | right | carry | Transport old_cell_0 |
| 7 | right | insert | Seat old_cell_0 |
| 8 | right | release | Release old_cell_0 |
| 9 | right | move | Withdraw from old_cell_0 |
| 10 | right | move | Approach new_cell_0 |
| 11 | right | grasp | Grasp new_cell_0 |
| 12 | right | carry | Verify lift of new_cell_0 |
| 13 | right | carry | Transport new_cell_0 |
| 14 | right | insert | Seat new_cell_0 |
| 15 | right | release | Release new_cell_0 |
| 16 | right | move | Withdraw from new_cell_0 |
| 17 | right | move | Approach old_cell_1 |
| 18 | right | grasp | Grasp old_cell_1 |
| 19 | right | carry | Verify lift of old_cell_1 |
| 20 | right | carry | Transport old_cell_1 |
| 21 | right | insert | Seat old_cell_1 |
| 22 | right | release | Release old_cell_1 |
| 23 | right | move | Withdraw from old_cell_1 |
| 24 | right | move | Approach new_cell_1 |
| 25 | right | grasp | Grasp new_cell_1 |
| 26 | right | carry | Verify lift of new_cell_1 |
| 27 | right | carry | Transport new_cell_1 |
| 28 | right | insert | Seat new_cell_1 |
| 29 | right | release | Release new_cell_1 |
| 30 | right | move | Withdraw from new_cell_1 |
| 31 | right | move | Clear cover travel |
| 32 | left | joint | Close the sliding cover |
| 33 | left | release | Release cover handle |
| 34 | right | move | Withdraw right arm |
| 35 | left | move | Withdraw left arm |
| 36 | left | hold | Observe released terminal stability |

The trajectory audit checks the official convex robot meshes against anchored fixture bodies, the table and the other arm every ten controls and at segment endpoints. It does not certify moving fixture, payload, flexible cable or inter-sample collision clearance. Grasp and thread sweeps separately check task geometry at specified samples. All are ideal kinematic checks, not physical execution.

After the motion plan, the expert holds the released pose while the actual scorer establishes full-score stability. It stops only on measured success or fails after a bounded five-second terminal grace period (or hold time plus two seconds, if longer). A finished phase list is not a success signal.

Overhead cell-approach waypoints use a 3 mm positional tolerance at 0.8675 m height. The grasp phase aligns to the measured cell and verifies jaw width and lift.

Cell transport uses measured cell error to command incremental TCP motion. Vertical seating aligns laterally before applying a 1.5 mm bounded axial lead, with the verified grasp orientation held during descent.
