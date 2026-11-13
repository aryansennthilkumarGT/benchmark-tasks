# Controlled release of a clamped cargo load bar

Independent CPU engineering package. Native Isaac, robot expert demonstrations, Dream, physical hardware and media qualification are **not run**. No official PR or paid service is authorized by this package. Its full-scale fixture follows the documented HF96811 release operation, with explicitly original internal geometry.

The task goal is to unload and shorten the installed bar, clear both wall feet, support it on the receiving cradles and release it. Instructions state the objective without revealing the release procedure. See OCCUPATION.md, NOVELTY.md, GEOMETRY_DESIGN.md, FIDELITY.md, PARAMETERS.md and REPRODUCTION.md.

Use Python3.12. The pinned CPU requirements install pytest, NumPy, USD composition, official YAM IK/FK, evidence/media utilities and optional MuJoCo3.3.7. Torch uses its CPU wheel. No Isaac/CUDA/Brev component is installed:

    python3.12 tasks/cargo-bar-controlled-release/install_cpu.py --venv /tmp/cargo-cpu
    /tmp/cargo-cpu/bin/python tasks/cargo-bar-controlled-release/static_check.py --output /tmp/cargo-checks

The previously prepared compatible RoboCurve CPU environment can run the same checks without reinstalling. Run output belongs outside Git. static_check.py checks the complete source manifest,31 unit/adversarial/workflow tests, both composed USDs, original gear flanks, actual CPU gear/pawl/cam contacts, repeated native-case protocols in MuJoCo, provenance, camera/IK, nominal geometry, all robot endpoints, ideal-controller replay and sampled full-controller FK collisions. It never starts native simulation or calls a model.

To reproduce authored source/assets deliberately, then review changes:

    python tasks/cargo-bar-controlled-release/generate_scene.py
    python tasks/cargo-bar-controlled-release/plan_controller.py
    python tasks/cargo-bar-controlled-release/provenance.py

A scene edit invalidates provenance and cam-reference hashes. Review and update provenance deliberately; never refresh hashes to hide a failed check. freeze_source.py only records intentionally reviewed source/assets, not execution evidence. The primitive/convex scene table is complete and all meshes are original.

The21-phase expert emits14 normal stock YAM joint/gripper commands at20Hz. It reads physical native telemetry through ROBOCURVE_TRACE, not score. Missing, stale or wrong-producer telemetry fails closed. Motions include independent tube support, latch squeeze, a continuous physical-circle handle path, actual pawl clearance checks, controlled retraction, wall clearance, cradle placement and withdrawal. Capture of the actual grasp transform and adaptive angular step reduction preserve the hinge constraint under bounded joint rates. Aperture/physical feedback detects missing grasps and stalls; grasp reacquisition is limited to two attempts. No expert code sets task roots/joints, attaches objects or advances gearing.

Current local ideal tracking is approximately1,161 actions/58s, well inside5,000 actions/250s. IdealFixture assumes rigid grasps, ideal tracking, quasistatic wall compliance and release support. It is synthetic even when its scorer reaches1.0. audit_path.py uses actual commanded robot FK with pinned URDF convex pieces, not just waypoint endpoints; sampled geometry is not a swept-volume or physical-grasp guarantee.

MuJoCo tests use actual original contact geometry. The full fixture export has no gear equality. Cam actuation uses explicitly disclosed test-rig actuators; it is not a YAM demonstration. cpu_native_cases.py repeats each physics protocol from native-cases.json with new data/reset state; initialized release/final-state tests are diagnostics. The unheld handle relaxes after unloading; the objective deliberately permits this. Native constraints/contact may behave differently.

Future commands **only on an already authorized GPU runtime** with the official stack in stack-lock.json:

    python tasks/cargo-bar-controlled-release/setup_environment.py --help
    python tasks/cargo-bar-controlled-release/task_runner.py --output /data/cargo-evidence
    python tasks/cargo-bar-controlled-release/native_tests.py --mode physics --commit EXACT_COMMIT --output /data/cargo-physics
    python tasks/cargo-bar-controlled-release/native_tests.py --mode control --commit EXACT_COMMIT --output /data/cargo-control
    python tasks/cargo-bar-controlled-release/task_runner.py --output /data/cargo-evidence --execute

The task-runner default is a pure preview. Execution requires a clean exact-source checkout, runs five native physics cases and three robot-control prefixes twice after independent resets, and records two distinct full-score expert demonstrations with complete action/camera/state logs. Validate/replay actual logs; do not accept interpreter exit status alone. The recovery coordinator additionally requires a third expert from a fresh independent HTTPS checkout before any paid evaluation.

Dream/media configuration is executable in run.py, dream_identity.py, task_runner.py, render_media.py and prepare_submission.py. Future --model requires real same-source feasibility and a cleared novelty decision; no dry-run/transcript substitute qualifies. Render model/demo/demo-repeat/setup from actual native records; visually review exact hashes before preparing metadata. prepare_submission.py defaults to preparation, with no upload or official PR. The current novelty decision is pending final acceptance review and blocks model qualification.

No upload credentials are requested/stored. Keep the environment private; preserve pendingPR1733 and rejected historical heads. Every mechanical/scoring edit needs new native evidence. Existing shackle/ER/SAC results do not qualify this task.
