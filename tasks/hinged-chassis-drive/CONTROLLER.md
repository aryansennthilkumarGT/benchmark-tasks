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
