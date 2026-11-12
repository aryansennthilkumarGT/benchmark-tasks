# Fixed-action robot demonstration

The expert executes `expert_joint_trajectory.json` using only observed robot joints, action index and elapsed control time. It does not import the feedback controller or read task object poses, native mechanism joints or scorer state. Official SDK bounds and delta guards remain active, including0.05 per-step normalized jaw limiting. Both independent whole cold episodes scored1.0; one used a fresh HTTPS checkout. Authored checkpoints are action indices, not measured task success.

The feedback controller is a separate development tool. Controlled fixture initialization is excluded from demonstration evidence.
