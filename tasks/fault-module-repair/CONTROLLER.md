# Feedback controller

The privileged scripted expert reads measured bodies, joints and robot proprioception. Dream receives the unmodified official cameras and robot joint observations. Both send the same 14 absolute joint/gripper targets at 20 Hz. No controller code writes body transforms, attaches objects or changes score state.

Each action uses measured-joint warm-start IK, <=3 mm Cartesian increments, <=0.045 rad per joint step and <=0.10 gripper increments. Approach completes before finger closure. Jaw width, body-relative grasp slip, lift or displacement, joint progress, and insertion stall checks control phase transitions. Holds follow measured parent frames where specified. Threading uses 45-degree turns with opening, wrist unwind and regrasp, checking measured pitch advancement. Minor body misalignment is corrected incrementally; a 2 s stalled insertion or failed grasp aborts rather than applying unbounded force or retries.

Offline nominal path checks sample actual URDF convex collision pieces for table and opposite-arm intersections every ten ideal controls, plus phase endpoints; critical grasp and first/last thread sweep checks include task fixtures. Full robot-to-fixture trajectories and deformable cable dynamics still require native validation. Sampling is not continuous collision certification.

| Phase | Arm | Operation | Measured completion |
|---:|---|---|---|
| 0 | left | move | Approach moving arm handle |
| 1 | left | grasp | Grasp arm support handle |
| 2 | left | joint | Support the arm level |
| 3 | right | move | Orient right hand outside the mechanism |
| 4 | right | move | Approach counterweight handle |
| 5 | right | grasp | Grasp counterweight slider |
| 6 | right | joint | Slide counterweight to the pin index |
| 7 | right | release | Release aligned counterweight |
| 8 | right | move | Clear counterweight |
| 9 | right | move | Approach locking pin |
| 10 | right | grasp | Grasp locking pin head |
| 11 | right | carry | Lift locking pin from its stand |
| 12 | right | carry | Route pin around the counterweight handle |
| 13 | right | carry | Align pin above both holes |
| 14 | right | insert | Insert pin through counterweight and arm |
| 15 | right | release | Release seated locking pin |
| 16 | right | move | Clear the pin and slider |
| 17 | left | release | Remove support from the balanced arm |
| 18 | left | move | Withdraw from service arm |
| 19 | left | hold | Observe three-second passive balance |

The trajectory audit checks the official convex robot meshes against anchored fixture bodies, the table and the other arm every ten controls and at segment endpoints. It does not certify moving fixture, payload, flexible cable or inter-sample collision clearance. Grasp and thread sweeps separately check task geometry at specified samples. All are ideal kinematic checks, not physical execution.

After the motion plan, the expert holds the released pose while the actual scorer establishes full-score stability. It stops only on measured success or fails after a bounded five-second terminal grace period (or hold time plus two seconds, if longer). A finished phase list is not a success signal.

During pin insertion the controller holds the wrist orientation derived from the verified grasp. Measured pin position drives the Cartesian correction, and measured pin angle gates completion. The bounded translation and stall guards apply throughout insertion.

The pin lift and routing targets include 12 mm extra vertical clearance after the measured approach dipped near the receiver face. The final hover adds 2 mm within the measured IK workspace. The critical TCP audit waypoints follow the current phase targets and nominal grasp offsets.

The fitted pin aligns to 0.15 mm lateral error before further axial motion. Lateral correction uses gain 8 with a 3 mm command lead bound. The stall metric weights lateral progress while the Cartesian speed and phase time limits bound the attempt.

The pin insertion phase permits 60 simulated seconds. The first chamfered-guide replay advanced the pin to world Z 0.8717 m, about 22 mm beyond the previous jam, with the slider retained at −31.14 mm. It was still progressing when the earlier 25-second phase limit expired. The overall 4,800-action limit and insertion pose, alignment, penetration and joint guard conditions are unchanged.
