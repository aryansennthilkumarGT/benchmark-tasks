# RoboCurve eight-task checkpoint

Status: **AWAITING_COMPUTE_ENDPOINT**. No task is selected, implemented, evaluated, uploaded or ready.

This coordination branch is separate from task submissions. Read `mission-checkpoint.json` for evidence and next actions, and `candidate-matrix.json` for preliminary overlap risks. Run `lab_preflight.py --expected-host <actual-confirmed-hostname>` only after connecting to the authorized RTX 4090 workstation. It is read-only and reports credential presence without values; its JSON includes private host details, so keep its output outside this public branch.

The official guide requires Isaac Lab-Arena, Inspect Robots and genuine Dream-1 evaluation for bimanual parallel-gripper tasks. Hardware and installed versions remain unverified. Complete a real official-example smoke test before building the eight tasks.

No official upstream PR may be opened by the agent. The teammate submission script and final manifest are not prepared yet because no validated task branches exist.
