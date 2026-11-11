# Feedback expert

The privileged expert reads actual body poses, passive joints and robot proprioception. It sends the same 14 joint/gripper targets available to the model at 20 Hz. Every interaction is executed through robot actions. The unmodified official cameras and robot observations are supplied to Dream.

Measured-joint warm-start IK uses bounded Cartesian and joint reference changes. Grasp completion checks jaw opening, relative pose and physical motion. Insertion uses filtered measured orientation correction, bounded lateral and axial command leads, and a 60-second phase timeout. The pin is guided to 10 mm above its final seat, released after engagement with both receivers, and allowed to seat under gravity after vertical finger withdrawal. The final passive balance requires three seconds of measured stability with robot clearance of at least 20 mm.

| Phase | Arm | Operation | Completion objective |
|---|---|---|---|
| 0 | left | move | Approach moving arm handle |
| 1 | left | grasp | Grasp arm support handle |
| 2 | left | joint | Support the arm level |
| 3 | right | move | Orient right hand outside the mechanism |
| 4 | right | move | Approach counterweight handle |
| 5 | right | grasp | Grasp counterweight slider |
| 6 | right | joint | Slide counterweight to the pin index |
| 7 | right | release | Release aligned counterweight |
| 8 | right | move | Lift above the counterweight after release |
| 9 | right | move | Clear the slider lane above the fixture |
| 10 | right | move | Approach locking pin |
| 11 | right | grasp | Grasp locking pin head |
| 12 | right | carry | Lift locking pin from its stand |
| 13 | right | carry | Route pin around the counterweight handle |
| 14 | right | carry | Align pin above both holes |
| 15 | right | insert | Guide pin into both bearing sections |
| 16 | right | release | Release guided pin to seat under gravity |
| 17 | right | move | Lift fingers vertically clear of the pin receiver |
| 18 | right | hold | Allow the guided pin to settle under gravity |
| 19 | right | move | Clear the pin and slider |
| 20 | left | release | Remove support from the balanced arm |
| 21 | left | move | Withdraw from service arm |
| 22 | left | hold | Observe three-second passive balance |

Two independent native expert episodes at implementation commit `46bf1008e01546b266b5ba973d31e75e64bf8f89` each reached score 1.0 in 1899 actions. All 8 physics cases and 4 robot-control cases passed at that implementation. Each recording was fully decoded and visually sampled across the complete trial. The evaluated source and sealed raw evidence remain separately preserved. Dream evaluation and official media upload are pending.

Offline IK and convex-clearance audits check sampled nominal configurations. Native runtime checks read measured robot links and collision geometry owned by each rigid link. Nested descendant robot colliders are excluded from parent-link bounds. Objective scoring recomputes all goals and invalid conditions from measured native state.
