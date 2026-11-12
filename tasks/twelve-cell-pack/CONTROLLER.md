# Measured-state pressure-plate closure expert

The 22 phases begin with twelve cells already loaded. The left hand grasps the loose pressure plate with a -10-degree jaw yaw, lifts and aligns it, and compresses all twelve terminal springs. Completion checks every contact travel, cell position and polarity before proceeding. The right hand grasps the separate cross-key and inserts it through the retaining channels while the pressure hand maintains the measured loaded reference.

Load transfer keeps the key held while the pressure hand opens, lifts vertically with its grasp yaw preserved, moves outward and withdraws. After observing the transferred load, the key hand opens, lifts vertically and withdraws. The final phase observes the released assembly. Full score requires the independent scorer's contact, pose, key-retention, robot-clearance and stability conditions; reaching a controller phase never assigns a score.

The controller reads native body poses, passive-joint state and robot proprioception. Loaded carries use bounded measured-position feedback and rate-limited IK. Compression has a 5 mm command lead and 10 mm/s motion limit. Insertion checks transverse alignment and tracks axial and transverse progress separately, with a bounded stall failure. Native actuator, joint and collision constraints remain active. The expert writes only fourteen robot joint/gripper commands, never object poses or score state.

Two independently recorded full-score cold experts of the evaluated revision each used 1,677 actions. Current measurements and exact source provenance are in validation.json. The controller's top-level status annotation is metadata; all 22 evaluated phase objects are preserved unchanged in the publication.
