# Supplemental CPU robot/contact diagnostics

This workflow integrates actual robot dynamics and contacts in MuJoCo3.3.7. It is a supplemental engineering diagnostic, not Isaac/PhysX qualification, a hardware test, a Dream run or evidence for official submission. It does not start or connect to external compute.

`cpu_yam_dynamics.py` exports both pinned YAM URDF chains with every original collision piece, joint origin/axis, mass, COM and full rotated inertia tensor. SDK SHOULDER/WRIST/GRIPPER gains and force limits override the URDF's placeholder effort1. Robot-only gravity compensation follows `yam_arena.actions`; joint effort limits include compensation. Same-arm collision is disabled as in the official articulation; inter-arm/table/task collisions remain enabled.

PhysX joint friction coefficients0.3/0.06 are not torque magnitudes and are **not** converted into MuJoCo `frictionloss`. Zero Coulomb joint loss and robot contact coefficient0.5 are disclosed diagnostic assumptions. Engine friction combination, contact compliance, velocity saturation, camera hardware, optics, room geometry and native import behavior still require Isaac checks. Robot source hashes and exact exported model hashes accompany every result.

```sh
python coordination/cpu_yam_dynamics.py --seconds 2 --output /tmp/yam-hold.json
python -m pytest -q coordination/test_cpu_yam_dynamics.py
python coordination/cpu_yam_trial.py \
  --task-folder /path/to/independent-checkout/tasks/brad-nailer-jam-recovery \
  --output /tmp/nailer-prefix-new --max-actions 1000 --stop-after-phase 7
```

Use the pinned CPU environment in the recovery setup. Output directories must be new. A prefix passes only after its actual requested phase boundary, without solver warnings or scorer integrity failures. A full controller run additionally needs its actual terminal scorer result; prefix success never implies full-score success. A bounded diagnostic that runs out of actions or wall time is incomplete. No object joint actuators, virtual grasps, object pose setters, physics-state projections, phase-switched collisions or completed-object freezing are used.

Seven exporter tests compare independently computed SDK FK at multiple configurations, every original collision hull support plane, rotated full inertia tensors, actual actuator settings, collision masks, invalid-action atomicity and a genuine gravity negative control. Removing compensation causes drift; the compensated arm holds. These tests do not validate task grasps.

The first integrated task prefix exposed a harness bug: the exact terminal time was scored twice, causing an artificial nonmonotonic-time failure. Its raw report is retained as excluded harness history. The corrected scorer boundary passes the same real-controller park prefix in119actions/5.95simulationseconds, with34.83µm maximum task interference and no robot/task contact or solver warnings. This is only one prefix; no native expert success is claimed.

Continue contact-bearing prefixes, inspect failures, distinguish backend limitations from genuine source defects, and requalify affected task sources if changed. Preserve existing exact-source evidence. The native Isaac/YAM, real same-source experts, model evaluation and media gates remain mandatory before any future authorized official submission.

## Thin-object normal-contact convergence

The stock1mm,0.5g brad exposed excessive numerical contact compliance in the first supplemental model. At the unchanged2.2ms robot-contact time constant, the reconstructed pre-grip fixture closes to0.284mm joint aperture and reaches605µm of raw robot-contact overlap. Raising impedance alone does not fix it. Increasing physics subdivisions and reducing the robot contact time constant together converges: subdivision4 gives0.923mm aperture/178µm peak; subdivision8 gives0.933mm/7.87µm. Empty-object controls close to zero at every subdivision. No solver warnings occurred. These are diagnostic static-pose initializations, not full expert demonstrations.

The runner now accepts `--physics-subdivision 1|2|4|8`, default1 for the historical comparison. This leaves all task geometry, masses, friction, physical joints, force limits and scoring unchanged. Task/task contact settings remain authored; robot contact time constant becomes2.2ms/subdivision, with high solver-mix weight to prevent the unchanged task default from dominating it. This is an explicit supplemental numerical refinement, not an OEM contact stiffness or native-engine equivalence claim. Native task physics remains1920Hz; the diagnostic reports its separate actual timestep.

`cpu_grasp_contact_probe.py --recording <real-diagnostic-directory> --phase 17 --empty-control-body bent_brad --output <new.json>` reproduces the calibration, validates the recorded model hash and includes an empty-object negative control. It never advertises expert success. The full repaired-source contact run must still pass; do not replace that run with these isolated fixtures.
