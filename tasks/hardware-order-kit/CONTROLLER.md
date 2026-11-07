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
