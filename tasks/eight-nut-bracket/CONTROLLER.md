# Expert controller

The expert submits14-dimensional absolute joint and jaw targets at20Hz through the official YAM embodiment. It reads actual robot joints, task body poses and passive joint positions. Object state changes occur through native robot contacts.

The left arm compresses and levels the spring-loaded plate. The right arm carries each nut to its stud, aligns the lead-in, then advances through3.45real turns using90-degree grips. Measured nut rotation must produce matching4mm-pitch axial movement. Open-jaw unwind recentres over the current nut at its original grasp height before reclosing. A1.5mm TCP gate and nonempty jaw width are required. Loaded joint tracking uses gain2.

The three clamp positions enclose the plate centre and retain control about both passive tilt axes. The final arm withdrawal and two-second native stability hold establish load transfer. Any missing grip, stalled insertion, joint-limit violation or inconsistent pitch advance aborts the expert.

| Phase | Arm | Operation | Instruction |
| --- | --- | --- | --- |
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
| 19 | right | move | Approach right stabilizing handle |
| 20 | right | grasp | Take plate support with right hand |
| 21 | left | release | Release left support after handover |
| 22 | left | move | Approach nut_2 |
| 23 | left | grasp | Grasp nut_2 |
| 24 | left | carry | Lift nut_2 |
| 25 | left | carry | Align nut_2 above stud |
| 26 | left | insert | Find thread lead for nut_2 |
| 27 | left | thread | Rotate and regrasp nut_2 |
| 28 | left | release | Release seated nut_2 |
| 29 | left | move | Withdraw from nut_2 |
| 30 | left | move | Clear fasteners with left hand |
| 31 | right | release | Release right plate support |
| 32 | right | move | Withdraw right arm |
| 33 | left | hold | Observe released threaded assembly |

Full targets, gains and timeout values are in controller.json. Exact IK paths, full robot meshes and intended grasp contacts are checked offline. Physical feasibility requires separate native trials.

The passive offset-drop probe is a negative control for engagement. The conical guide assists active alignment, and the first full nut-threading control probe must establish the actual positive case. The predecessor probe incorrectly assumed passive self-centring from an offset drop and failed. Its evidence remains in the engineering checkpoint.
