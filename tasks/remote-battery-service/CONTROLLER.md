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

Cell transport uses the verified grasp transform and measured cell-position correction. Vertical seating uses incremental TCP motion, lateral alignment and a 1.5 mm bounded axial lead with the verified grasp orientation.

Seating lateral alignment uses gain 8 and a 3 mm bounded lead. The stall guard measures lateral progress as well as axial progress.

Cell grasp offsets are vertical in the world frame. Rotation about a cylindrical cell’s longitudinal axis leaves its grasp geometry unchanged. Native staging showed a 38-degree roll, which incorrectly rotated the previous body-local 10 mm approach offset sideways by about 6 mm. The cover handle retains its body-local grasp offset. This correction awaits a recorded native rollout.

The fresh-cell approach permits 3 mm measured TCP position error before closing the jaws. Successful grasp still requires 10–18 mm measured jaw width, less than 4 mm TCP error, less than 0.06 rad orientation error and the subsequent physical lift/slip verification. A native replay reached its Cartesian reference within 0.02 mm while the original 1.5 mm closure gate remained unsatisfied. Failure events now preserve actual robot joints and motion references for diagnosing residual tracking or contact errors.

Carry and insertion phase completion for cylindrical cells checks their longitudinal X axis. Rotation about that axis is physically symmetric and already excluded from the objective scorer. The 61bab7c replay grasped and lifted the fresh cell by 113 mm, reaching its position within 1 mm, then waited because a stable 4.4-degree axial roll exceeded the controller’s full-quaternion threshold. Longitudinal tilt and polarity remain constrained, along with all existing scoring and contact checks.

The low-rail replay successfully released the used cell and grasped the fresh cell, but the fresh-cell lift drifted 63 mm while its longitudinal axis stayed within 0.021 rad. The controller was rotating the wrist to remove irrelevant axial roll from the source cell, invalidating its fixed grasp-offset translation model. Fresh-cell carry and insertion now preserve the measured wrist orientation captured at grasp. Fresh-cell carry uses measured TCP translation feedback with gain 4 and the existing hard 3 mm command lead. Longitudinal-axis completion, physical lift/slip checks, scoring and all used-cell motion remain active. This revision awaits native execution.

The 81dbcca replay completed the fresh-cell grasp, lift and transport. Insertion reached world Z 0.82724 m before its 0.65 mm lateral entry gate stalled at 1.06 mm error, above any bay contact. Fresh-cell insertion now allows 1.5 mm lateral entry error and 60 seconds to engage the physical guides and springs. The objective requires final placement within 1 mm, correct polarity, spring contact, stillness and cover closure.

The 9bb4e97 replay reached the first spring contact at cell Z 0.77512 m, compressing spring_0 by 0.374 mm. Actual measured robot geometry showed no fixture interference. The cell now enters negative-end-first with an 0.2 rad longitudinal tilt, presses its spring to 1.15 mm compression using bounded measured-joint feedback, lowers its free end, and centres before release. Spring feedback gain is 8 with a 3 mm command lead and 0.25 mm joint tolerance. The mirrored sequence serves the opposite-polarity bay. Native validation remains pending for this procedure.

The concurrent tilt/descent replay deflected the first cell axis to approximately −16.6 degrees while targeting +11.5 degrees. The revised sequence first orients the cell above fixture contact, then lowers the already tilted cell. This isolates free-air grasp orientation from contact-induced rotation in the next native experiment.

The next candidate uses a 0.3-rad tilt, a 2.6-mm offset away from the spring and a 0.7710-m body center during first contact entry. These dimensions are chosen to clear the cylindrical rim over the spring top and keep the opposite end above its fixed contact. Native validation is pending.

The 0.3-rad native trial completed free-space orientation, then made off-center contact with the spring edge and stalled. Measured convex checks found only intended fingertip/cell contact for robot geometry and a 0.078-mm cell/spring overlap. The next entry target adds 5 mm offset away from the spring and uses body height 0.774 m, providing nominal rim/end-wall clearance before horizontal spring compression. Physical validation is pending.

The wider entry also timed out after contact. Setting ROBOCURVE_PROPRIO_TRACE enables per-action measured robot joints for time-aligned contact diagnosis. This optional evidence stream preserves the controller actions and scoring behavior. The next diagnostic replays the same physical plan to locate the first contact before changing the entry path again.

Synchronized native poses and measured joints showed roughly 5 mm lateral cell drift before spring contact, with sampled robot/fixture geometry clear. Tilted entry now uses a world-vertical insertion axis, lateral gain 8 and an 8-mm lead cap, and permits descent only within 0.8 mm lateral alignment. The right-arm tracking window is bounded at 0.08 rad. Per-reference rate, physical collision and objective score guards remain active. Native validation is pending.

The guided descent passed native execution, then the spring-press phase lost the cell tilt and drifted sideways. The prismatic press now holds its measured starting transverse position and the captured wrist rotated to the entry tilt. The press uses a 3-mm axial lead, gain 8 and an eight-second timeout. Native validation is pending.

A sampled transverse/tilt hold frame showed approximately 0.49-mm compression. The completed trace later showed 0–2-mm oscillation and a failed dwell check. Measured-pose convex geometry found contact only with the intended spring face. The next bounded press uses gain 12 and a 6-mm axial TCP lead cap against the 200-N/m spring. Physical stroke remains 2 mm. Native validation is pending.

The larger axial-lead trial ended with a 0.052-mm compression sample. Its completed trace later showed 0–2-mm oscillation. Geometric inspection suggests contact high on the spring face while the cell is tilted. The next candidate lowers both tilted-entry body targets 3 mm to z=0.771 m. Offline IK at the synchronized measured entry pose converged below 1 micrometre, with no robot/fixture surface pair within 0.6 mm and no object-pair penetration above 0.3 mm. The physical native result remains pending.

Complete 162-frame press traces for all three attempts show repeated motion across the full 2-mm spring stroke. The original hold attempt had mean compression 1.067 mm and standard deviation 0.467 mm. No attempt sustained consecutive in-band samples for the required 0.15 seconds. The press now uses gain 1 and a 0.5-mm step cap. Entry returns to the previously executed z=0.774 m target. The press requires 1.15-mm compression within 0.25 mm for 0.15 seconds. Native validation is pending.

The free-end lowering candidate integrates bounded axial body error into the current robot reference while applying measured transverse correction. The 0.1 axial gain and 0.5 mm per-action cap address the observed loaded vertical tracking residual. Last-frame offline convex inspection found no robot-to-fixture penetration above 0.3 mm at the earlier stalled pose. This geometric diagnostic does not establish native contact forces. Native retesting is required.

Free-end lowering combines axial reference integration with lateral gain 8 and an 8 mm lateral lead cap. The unit-gain lateral experiment drifted approximately 10 mm in x while the wrist flattened the cell, preventing axial alignment. The earlier gain-eight trace retained lateral alignment. A geometric inspection of the failed unit-gain frame found intended cell/jaw contacts and no fixture surface within 0.6 mm of the right robot collision hulls. This inspection supplies geometric proximity evidence. Actual contact forces were not measured. Native retesting is required.

The second replacement cell descends unrotated to 0.79275 m before the 0.3 radian spring-entry tilt. Offline IK on the measured failed pose reaches the wrist lower stop at the former 0.80275 m tilt height. The lower waypoint provides wrist clearance. Measured-pose feedback with gain 2 retains the loaded translation reference during this descent and orientation. Native verification remains required.

The second spring-compression phase integrates its bounded 0.5 mm prismatic lead from the loaded robot reference along the contact axis. Measured spring travel determines completion. Transverse TCP coordinates stay at their phase-entry values. The previous measured-TCP-only lead stalled before contact with a 20 mrad wrist tracking bias. The correction affects only the second spring phase.
