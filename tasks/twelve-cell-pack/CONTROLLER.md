# Feedback controller

The privileged scripted expert reads measured bodies, joints and robot proprioception. Dream receives the unmodified official cameras and robot joint observations. Both send the same 14 absolute joint/gripper targets at 20 Hz. No controller code writes body transforms, attaches objects or changes score state.

Each action uses measured-joint warm-start IK, <=3 mm Cartesian increments, <=0.045 rad per joint step and <=0.10 gripper increments. Approach completes before finger closure. Jaw width, body-relative grasp slip, lift or displacement, joint progress, and insertion stall checks control phase transitions. Holds follow measured parent frames where specified. Threading uses 45-degree turns with opening, wrist unwind and regrasp, checking measured pitch advancement. Minor body misalignment is corrected incrementally; a 2 s stalled insertion or failed grasp aborts rather than applying unbounded force or retries.

Offline nominal path checks sample actual URDF convex collision pieces for table and opposite-arm intersections every ten ideal controls, plus phase endpoints; critical grasp and first/last thread sweep checks include task fixtures. Full robot-to-fixture trajectories and deformable cable dynamics still require native validation. Sampling is not continuous collision certification.

| Phase | Arm | Operation | Measured completion |
|---:|---|---|---|
| 0 | right | move | Approach cell_0 |
| 1 | right | grasp | Grasp cell_0 |
| 2 | right | carry | Verify lift of cell_0 |
| 3 | right | carry | Move outside retaining channel cell_0 |
| 4 | right | carry | Pass around retaining channel cell_0 |
| 5 | right | carry | Transport cell_0 |
| 6 | right | insert | Seat cell_0 |
| 7 | right | release | Release cell_0 |
| 8 | right | move | Withdraw from cell_0 |
| 9 | right | move | Approach cell_1 |
| 10 | right | grasp | Grasp cell_1 |
| 11 | right | carry | Verify lift of cell_1 |
| 12 | right | carry | Move outside retaining channel cell_1 |
| 13 | right | carry | Pass around retaining channel cell_1 |
| 14 | right | carry | Transport cell_1 |
| 15 | right | insert | Seat cell_1 |
| 16 | right | release | Release cell_1 |
| 17 | right | move | Withdraw from cell_1 |
| 18 | right | move | Approach cell_2 |
| 19 | right | grasp | Grasp cell_2 |
| 20 | right | carry | Verify lift of cell_2 |
| 21 | right | carry | Move outside retaining channel cell_2 |
| 22 | right | carry | Pass around retaining channel cell_2 |
| 23 | right | carry | Transport cell_2 |
| 24 | right | insert | Seat cell_2 |
| 25 | right | release | Release cell_2 |
| 26 | right | move | Withdraw from cell_2 |
| 27 | right | move | Approach cell_3 |
| 28 | right | grasp | Grasp cell_3 |
| 29 | right | carry | Verify lift of cell_3 |
| 30 | right | carry | Move outside retaining channel cell_3 |
| 31 | right | carry | Pass around retaining channel cell_3 |
| 32 | right | carry | Transport cell_3 |
| 33 | right | insert | Seat cell_3 |
| 34 | right | release | Release cell_3 |
| 35 | right | move | Withdraw from cell_3 |
| 36 | right | move | Approach cell_4 |
| 37 | right | grasp | Grasp cell_4 |
| 38 | right | carry | Verify lift of cell_4 |
| 39 | right | carry | Move outside retaining channel cell_4 |
| 40 | right | carry | Pass around retaining channel cell_4 |
| 41 | right | carry | Transport cell_4 |
| 42 | right | insert | Seat cell_4 |
| 43 | right | release | Release cell_4 |
| 44 | right | move | Withdraw from cell_4 |
| 45 | right | move | Approach cell_5 |
| 46 | right | grasp | Grasp cell_5 |
| 47 | right | carry | Verify lift of cell_5 |
| 48 | right | carry | Move outside retaining channel cell_5 |
| 49 | right | carry | Pass around retaining channel cell_5 |
| 50 | right | carry | Transport cell_5 |
| 51 | right | insert | Seat cell_5 |
| 52 | right | release | Release cell_5 |
| 53 | right | move | Withdraw from cell_5 |
| 54 | right | move | Park right arm before working on the rear row |
| 55 | left | move | Approach cell_6 |
| 56 | left | grasp | Grasp cell_6 |
| 57 | left | carry | Verify lift of cell_6 |
| 58 | left | carry | Move outside retaining channel cell_6 |
| 59 | left | carry | Pass around retaining channel cell_6 |
| 60 | left | carry | Transport cell_6 |
| 61 | left | insert | Seat cell_6 |
| 62 | right | release | Release cell_6 |
| 63 | left | move | Withdraw from cell_6 |
| 64 | left | move | Approach cell_7 |
| 65 | left | grasp | Grasp cell_7 |
| 66 | left | carry | Verify lift of cell_7 |
| 67 | left | carry | Move outside retaining channel cell_7 |
| 68 | left | carry | Pass around retaining channel cell_7 |
| 69 | left | carry | Transport cell_7 |
| 70 | left | insert | Seat cell_7 |
| 71 | right | release | Release cell_7 |
| 72 | left | move | Withdraw from cell_7 |
| 73 | left | move | Approach cell_8 |
| 74 | left | grasp | Grasp cell_8 |
| 75 | left | carry | Verify lift of cell_8 |
| 76 | left | carry | Move outside retaining channel cell_8 |
| 77 | left | carry | Pass around retaining channel cell_8 |
| 78 | left | carry | Transport cell_8 |
| 79 | left | insert | Seat cell_8 |
| 80 | right | release | Release cell_8 |
| 81 | left | move | Withdraw from cell_8 |
| 82 | left | move | Approach cell_9 |
| 83 | left | grasp | Grasp cell_9 |
| 84 | left | carry | Verify lift of cell_9 |
| 85 | left | carry | Move outside retaining channel cell_9 |
| 86 | left | carry | Pass around retaining channel cell_9 |
| 87 | left | carry | Transport cell_9 |
| 88 | left | insert | Seat cell_9 |
| 89 | right | release | Release cell_9 |
| 90 | left | move | Withdraw from cell_9 |
| 91 | left | move | Approach cell_10 |
| 92 | left | grasp | Grasp cell_10 |
| 93 | left | carry | Verify lift of cell_10 |
| 94 | left | carry | Move outside retaining channel cell_10 |
| 95 | left | carry | Pass around retaining channel cell_10 |
| 96 | left | carry | Transport cell_10 |
| 97 | left | insert | Seat cell_10 |
| 98 | right | release | Release cell_10 |
| 99 | left | move | Withdraw from cell_10 |
| 100 | left | move | Approach cell_11 |
| 101 | left | grasp | Grasp cell_11 |
| 102 | left | carry | Verify lift of cell_11 |
| 103 | left | carry | Move outside retaining channel cell_11 |
| 104 | left | carry | Pass around retaining channel cell_11 |
| 105 | left | carry | Transport cell_11 |
| 106 | left | insert | Seat cell_11 |
| 107 | right | release | Release cell_11 |
| 108 | left | move | Withdraw from cell_11 |
| 109 | right | move | Clear completed cells |
| 110 | left | move | Approach pressure-plate handle |
| 111 | left | grasp | Grasp pressure plate |
| 112 | left | carry | Lift pressure plate |
| 113 | left | carry | Align plate contact pads |
| 114 | left | insert | Compress all twelve terminal springs |
| 115 | right | move | Approach capture key |
| 116 | right | grasp | Grasp capture key |
| 117 | right | carry | Lift capture key |
| 118 | right | carry | Align key ahead of retaining channels |
| 119 | right | carry | Lower key to channel height |
| 120 | right | insert | Capture pressure plate with cross-key |
| 121 | right | release | Release seated key |
| 122 | right | move | Clear retaining key |
| 123 | left | release | Release captured preload |
| 124 | right | move | Withdraw right arm |
| 125 | left | move | Withdraw left arm |
| 126 | left | hold | Observe released terminal stability |

The trajectory audit checks the official convex robot meshes against anchored fixture bodies, the table and the other arm every ten controls and at segment endpoints. It does not certify moving fixture, payload, flexible cable or inter-sample collision clearance. Grasp and thread sweeps separately check task geometry at specified samples. All are ideal kinematic checks, not physical execution.

After the motion plan, the expert holds the released pose while the actual scorer establishes full-score stability. It stops only on measured success or fails after a bounded five-second terminal grace period (or hold time plus two seconds, if longer). A finished phase list is not a success signal.

The first native cell grasp/lift passed both resets. Seating stalled above the channel with about 0.85 mm lateral error. The candidate cell insertion aligns within 0.4 mm before vertical advance, using bounded lateral gain 8 and a 4-mm lead. Its progress monitor weights measured lateral correction during alignment. The right-arm tracking window is bounded at 0.08 rad. Native seating validation is pending.

Cell carry/seating completion checks the measured longitudinal axis, matching the polarity goal for the cylindrical cells. Axial spin is free. The regression rejects tilt while accepting axial rotation.

The guided second-cell trial descended approximately 2 mm during its final two seconds, while the weighted lateral residual triggered a stall. Progress now uses measured three-dimensional distance to the physical target. A regression checks continuing descent with lateral jitter and a subsequent stationary jam. Native retesting is pending.
