# Actuated CPU repair, not native qualification

Original1263eb9658f67ddc0e632ee8b22d8621cbd625f5 is preserved. A fresh clean-HTTPS actual YAM/MuJoCo trial349actions/17.45s fails Lift collet from cradle, score0, no solver warnings. The collet is genuinely grasped/lifted, but robot-only gravity compensation leaves a loaded TCP error2.780mm at a0.25mm controller target. Original stock SDK gripper speed is exceeded by1.5357times. The full failed report/model/trace is retained on the recovery branch.

This successor retains all geometry, task masses, joints, contacts and scoring. Loaded phases use Cartesian measured-position integral feedback at3/s, capped to6mm reference lead. SDK force limits remain unchanged. Joint tracking allowance0.08rad is compatible with the SDK wrist D/K0.15s and0.4rad/s reference motion; it does not enlarge task success tolerances. Gripper reference slew is0.05normalized per50ms instead of0.10. A recorded-state regression exercises loaded correction and bounded windup, explicitly without claiming plant/task success. Full actual CPU and native tests are still required; readiness remains held.


## Actual lift repair passes; object orientation requires feedback

Clean c17e600 passes lift/transfer and the SDK velocity gate (maximum0.7687), then stops phase7/612actions/30.6s, score0, no solver warnings. At the preceding nominally completed tilt, actual collet pitch is about+0.052rad against desired−0.250rad. Wrist-only completion hides this actual part slip. The stock gripping normal aligns with that rotation axis in the former grasp; the supplemental point-friction contacts have no authored torsional-friction patch. This is an actual diagnostic limitation/risk, not proof that native PhysX or physical hardware behaves identically.

The successor rotates the initial gripper yaw90degrees so the required pitch is across the opposed jaws, and resolves loaded targets through measured TCP-to-collet pose on each observation. It requires actual part position/orientation to complete loaded phases. Native feedback is explicitly privileged scripted-expert telemetry; model observations are unchanged. Missing/stale/invalid part poses fail closed. Release opens at measured TCP before withdrawing. All original mechanical/scoring geometry and parameters are unchanged. New full robot physics, source-bound ideal/FK and native validation remain required.
