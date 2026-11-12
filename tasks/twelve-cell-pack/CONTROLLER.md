# Fixed-action expert

The submitted expert reads robot joint observations and emits the fixed14-dimensional command sequence in `expert_joint_trajectory.json`. It does not query runtime task object poses, mechanism joints, evaluator state or score. Authored action checkpoints describe program indices, not observed task completion.

The separate feedback controller is a development tool used to author the program; it is not imported by the demonstration policy. Two whole cold simulator episodes independently verified full score with the fixed program, including a fresh HTTPS checkout. Native actuation, collisions and scoring remain active throughout.
