# Feedback controller

The privileged scripted expert reads measured bodies, joints and robot proprioception. Dream receives the unmodified official cameras and robot joint observations. Both send the same 14 absolute joint/gripper targets at 20 Hz. No controller code writes body transforms, attaches objects or changes score state.

Each action uses measured-joint warm-start IK, <=3 mm Cartesian increments, <=0.045 rad per joint step and <=0.10 gripper increments. Approach completes before finger closure. Jaw width, body-relative grasp slip, lift or displacement, joint progress, and insertion stall checks control phase transitions. Holds follow measured parent frames where specified. Threading uses 45-degree turns with opening, wrist unwind and regrasp, checking measured pitch advancement. Minor body misalignment is corrected incrementally; a 2 s stalled insertion or failed grasp aborts rather than applying unbounded force or retries.

Offline nominal path checks sample actual URDF convex collision pieces for table and opposite-arm intersections every ten ideal controls, plus phase endpoints; critical grasp and first/last thread sweep checks include task fixtures. Full robot-to-fixture trajectories and deformable cable dynamics still require native validation. Sampling is not continuous collision certification.

| Phase | Arm | Operation | Measured completion |
|---:|---|---|---|
| 0 | left | move | Approach plate stabilizing handle |
| 1 | left | grasp | Stabilize the spring-loaded plate |
| 2 | left | joint | Compress and level the access plate |
| 3 | right | move | Approach nut_0 |
| 4 | right | grasp | Grasp nut_0 |
| 5 | right | carry | Lift nut_0 |
| 6 | right | carry | Align nut_0 above stud |
| 7 | right | insert | Find thread lead for nut_0 |
| 8 | right | thread | Rotate and regrasp nut_0 |
| 9 | right | release | Release seated nut_0 |
| 10 | right | move | Withdraw from nut_0 |
| 11 | right | move | Approach nut_1 |
| 12 | right | grasp | Grasp nut_1 |
| 13 | right | carry | Lift nut_1 |
| 14 | right | carry | Align nut_1 above stud |
| 15 | right | insert | Find thread lead for nut_1 |
| 16 | right | thread | Rotate and regrasp nut_1 |
| 17 | right | release | Release seated nut_1 |
| 18 | right | move | Withdraw from nut_1 |
| 19 | right | move | Approach nut_2 |
| 20 | right | grasp | Grasp nut_2 |
| 21 | right | carry | Lift nut_2 |
| 22 | right | carry | Align nut_2 above stud |
| 23 | right | insert | Find thread lead for nut_2 |
| 24 | right | thread | Rotate and regrasp nut_2 |
| 25 | right | release | Release seated nut_2 |
| 26 | right | move | Withdraw from nut_2 |
| 27 | right | move | Approach nut_3 |
| 28 | right | grasp | Grasp nut_3 |
| 29 | right | carry | Lift nut_3 |
| 30 | right | carry | Align nut_3 above stud |
| 31 | right | insert | Find thread lead for nut_3 |
| 32 | right | thread | Rotate and regrasp nut_3 |
| 33 | right | release | Release seated nut_3 |
| 34 | right | move | Withdraw from nut_3 |
| 35 | right | move | Approach right stabilizing handle |
| 36 | right | grasp | Take plate support with right hand |
| 37 | left | release | Release left support after handover |
| 38 | left | move | Approach nut_4 |
| 39 | left | grasp | Grasp nut_4 |
| 40 | left | carry | Lift nut_4 |
| 41 | left | carry | Align nut_4 above stud |
| 42 | left | insert | Find thread lead for nut_4 |
| 43 | left | thread | Rotate and regrasp nut_4 |
| 44 | left | release | Release seated nut_4 |
| 45 | left | move | Withdraw from nut_4 |
| 46 | left | move | Approach nut_5 |
| 47 | left | grasp | Grasp nut_5 |
| 48 | left | carry | Lift nut_5 |
| 49 | left | carry | Align nut_5 above stud |
| 50 | left | insert | Find thread lead for nut_5 |
| 51 | left | thread | Rotate and regrasp nut_5 |
| 52 | left | release | Release seated nut_5 |
| 53 | left | move | Withdraw from nut_5 |
| 54 | left | move | Approach nut_6 |
| 55 | left | grasp | Grasp nut_6 |
| 56 | left | carry | Lift nut_6 |
| 57 | left | carry | Align nut_6 above stud |
| 58 | left | insert | Find thread lead for nut_6 |
| 59 | left | thread | Rotate and regrasp nut_6 |
| 60 | left | release | Release seated nut_6 |
| 61 | left | move | Withdraw from nut_6 |
| 62 | left | move | Approach nut_7 |
| 63 | left | grasp | Grasp nut_7 |
| 64 | left | carry | Lift nut_7 |
| 65 | left | carry | Align nut_7 above stud |
| 66 | left | insert | Find thread lead for nut_7 |
| 67 | left | thread | Rotate and regrasp nut_7 |
| 68 | left | release | Release seated nut_7 |
| 69 | left | move | Withdraw from nut_7 |
| 70 | left | move | Clear fasteners with left hand |
| 71 | right | release | Release right plate support |
| 72 | right | move | Withdraw right arm |
| 73 | left | hold | Observe released threaded assembly |

The trajectory audit checks the official convex robot meshes against anchored fixture bodies, the table and the other arm every ten controls and at segment endpoints. It does not certify moving fixture, payload, flexible cable or inter-sample collision clearance. Grasp and thread sweeps separately check task geometry at specified samples. All are ideal kinematic checks, not physical execution.

After the motion plan, the expert holds the released pose while the actual scorer establishes full-score stability. It stops only on measured success or fails after a bounded five-second terminal grace period (or hold time plus two seconds, if longer). A finished phase list is not a success signal.

The square-thread approximation uses 4 mm lead, 1.70 mm axial ridge thickness and 16 contact sectors per turn. Nominal mating backlash is 0.60 mm. Female crest radius is 8.15 mm around a 7.70 mm stud core, with 0.90 mm male/female radial engagement. Internal thread clocking is -67.5 degrees with a +0.05 mm axial offset, matching the authored entry and loaded fixture phases. The previous 1-mm flanks allowed 2-mm nominal axial backlash, and 0.5-mm radial engagement was smaller than the 0.85-mm core clearance. This candidate needs full native validation.

The corrected profile passed 7/8 native physics cases, with both passive retention repetitions passing. The second upward-load repetition reported deep penetration involving the last initialized nut. The next fixture test synchronizes native FK after all initialization writes and records measured post-initialization coordinates before loading. This synchronization belongs to physics probes. Expert actions remain robot controls. Native retesting is pending.

The first native robot probe compressed the pressure plate 3.38 mm against a 12-mm target and developed approximately 0.083-rad pitch. Its shared prerequisite timed out. The press now integrates measured joint error into the existing rate-limited robot reference and targets a level plate orientation. The left reference tracking window is 0.08 rad, with the 0.5-mm per-step Cartesian increment. Native retesting is pending. Failure receipts include measured references and actuator torques.

Thread-lead approach integrates measured nut-position error into the rate-limited robot reference, with gain 0.1 and a 0.5 mm per-action lead cap. The previous nominal 0.5 mm body target descended only about 0.4 mm/s and drifted laterally before timing out. Grasp checks, joint limits, and bounded stall detection remain active. Native thread entry is still unverified for this candidate.

The threading arm uses the 0.08-radian loaded joint-tracking window already configured for the preload arm. A native trace showed only 0.0147 radians of net yaw change and 0.184 mm of height change over 53.1 simulated seconds. That incomplete experiment was intentionally stopped. Rotation now requires at least 0.005 radians of additional directed progress within two seconds, including a fresh progress interval after each regrasp. Failure diagnostics include actual joints, references, grasp transforms and thread state. Native retesting must determine whether the tracking window resolves the stall.
