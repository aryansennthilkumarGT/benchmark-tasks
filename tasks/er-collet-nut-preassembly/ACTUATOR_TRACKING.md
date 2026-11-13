# Actuated CPU repair, not native qualification

Original1263eb9658f67ddc0e632ee8b22d8621cbd625f5 is preserved. A fresh clean-HTTPS actual YAM/MuJoCo trial349actions/17.45s fails Lift collet from cradle, score0, no solver warnings. The collet is genuinely grasped/lifted, but robot-only gravity compensation leaves a loaded TCP error2.780mm at a0.25mm controller target. Original stock SDK gripper speed is exceeded by1.5357times. The full failed report/model/trace is retained on the recovery branch.

This successor retains all geometry, task masses, joints, contacts and scoring. Loaded phases use Cartesian measured-position integral feedback at3/s, capped to6mm reference lead. SDK force limits remain unchanged. Joint tracking allowance0.08rad is compatible with the SDK wrist D/K0.15s and0.4rad/s reference motion; it does not enlarge task success tolerances. Gripper reference slew is0.05normalized per50ms instead of0.10. A recorded-state regression exercises loaded correction and bounded windup, explicitly without claiming plant/task success. Full actual CPU and native tests are still required; readiness remains held.


## Actual lift repair passes; object orientation requires feedback

Clean c17e600 passes lift/transfer and the SDK velocity gate (maximum0.7687), then stops phase7/612actions/30.6s, score0, no solver warnings. At the preceding nominally completed tilt, actual collet pitch is about+0.052rad against desired−0.250rad. Wrist-only completion hides this actual part slip. The stock gripping normal aligns with that rotation axis in the former grasp; the supplemental point-friction contacts have no authored torsional-friction patch. This is an actual diagnostic limitation/risk, not proof that native PhysX or physical hardware behaves identically.

The successor rotates the initial gripper yaw90degrees so the required pitch is across the opposed jaws, and resolves loaded targets through measured TCP-to-collet pose on each observation. It requires actual part position/orientation to complete loaded phases. Native feedback is explicitly privileged scripted-expert telemetry; model observations are unchanged. Missing/stale/invalid part poses fail closed. Release opens at measured TCP before withdrawing. All original mechanical/scoring geometry and parameters are unchanged. New full robot physics, source-bound ideal/FK and native validation remain required.


## Actual part-feedback loss and bounded angular response

Clean9ab9b30 passes acquisition but loses the collet during lift and eventually hits an IK limit (278actions/13.9s, score0, no warnings, SDK ratio0.7681). Full-error wrist orientation correction on every50ms update is too aggressive for the observed load/contact dynamics; axial and pitch slip must never be mistaken for success. The next revision integrates measured orientation error at1.5/s with0.08rad angular reference lead, matching bounded3/s position feedback. An acquired grasp with empty-jaw feedback for0.25s terminates explicitly before pursuing a dropped part. These are authored controller parameters, not manufacturer properties. Full fresh physics remains required.


## Unsupported roll and axial symmetry

Clean d2d0e61 still loses the part during lift; the new guard terminates explicitly at531actions, physical score0. No native or full-success claim. The next servo uses actual collet-axis error instead of full quaternion error (axial yaw is physically irrelevant), and projects wrist correction away from the opposed-pad normal. It therefore does not chase weakly constrained rolling with the wrist. Measured position and supported cam-entry pitch remain controlled. Free-space lift/transfer permit0.10rad axis deviation; all entry/engagement/rocking phases retain0.02rad and task scoring remains unchanged. This is a controller repair with fresh verification required, not evidence that the point-contact backend reproduces native pad torsion.

## Reviewer-driven source repair

Persistent aperture reference now reaches the requested closing command under a blocked tapered grip, with unchanged0.05normalized/tick slew and SDK force/velocity limits. The supported-axis feedback experiment is retained, but has not demonstrated physical retention. Inspect controller completion no longer requests episode stop; only independent scorer success or run limit terminates. The prior d2d0e61 physical run lost the grip at531actions/26.55s, score0; it is historical and does not test this successor. The100um authored overlap limit repairs a reproduced scoring-envelope gap; a full-disk SAT covering bound and repeated contact fixture must pass. No native/expert/Dream result is claimed.
