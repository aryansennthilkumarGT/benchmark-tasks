# Measured expert controller

The controller commands the real bimanual YAM14-dimensional joint/jaw interface at20Hz. The left hand first compresses and levels the spring plate while the right hand threads nuts0 and1. Support is handed to the right arm before the left arm threads nut2. After all fasteners are seated, both hands withdraw and the assembly must retain preload and level attitude.

Nut advance occurs through physical contact with4mm-pitch helical facets. Measured rotation must agree with axial advance; free spin, missed grasps, joint limits or stalled motion abort. Quarter-turn segments alternate with open/lift/unwind/lower/regrasp motions. The actual52mm jaw opening and12mm raised unwind trajectory preserve fixture clearance. Measured TCP corrections use gain2/s; turning corrects radial/axial helix error by at most0.5mm per action. An early regrasp starts at wrist reference1.90rad, preserving margin to the unchanged2.0944rad hardware limit.

Controller targets are3.45turns for nuts0/1 and3.50turns for nut2, with objective full-score requirement3.45measured turns for every nut. The third target includes seating margin; it does not change the scorer or bypass real helical advance. Pose, pitch, nonempty-grip and bounded regrasp guards remain active. All parameters are authoritative in controller.json.

| Phase | Arm | Operation | Goal |
|---|---|---|---|
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

Offline unit/geometry checks do not prove feasibility. Initialized recorded-state replays are diagnostics only. Two complete cold-reset full-score demonstrations, actual native mechanism tests and a fresh HTTPS reproduction are required before publication.
