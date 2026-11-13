# ER collet and eccentric nut preassembly

Prepare a supported ER32 collet/nut by engaging its extraction groove with the eccentric cam. The task is grounded in manufacturer dimensions and ER assembly guidance; it ends before toolholder fastening. Original cam/bench geometry is explicitly authored. It does not claim that the cam holds a collet unsupported.

Native physics, real experts, Dream-1 and hardware validation are **NOT RUN**. Ideal tracking and actual FK geometry assume jaw contact and are not demonstrations. No official submission is ready.

## CPU reproduction

```bash
python3.12 tasks/er-collet-nut-preassembly/install_cpu.py --venv /tmp/er-cpu-venv
/tmp/er-cpu-venv/bin/python tasks/er-collet-nut-preassembly/static_check.py
```

The compatible pinned CPU setup installs no Isaac Sim. The check verifies exact source/asset hashes, unit/adversarial/loader/media tests, composed USD, IK, all nominal geometry/robot endpoints, actual FK cam-path geometry and ideal controller completion. Contact physics is not run. To edit intentionally, run `generate_scene.py`, `write_native_cases.py`, `write_parameters.py`, then `freeze_source.py` and checks. Never refresh hashes to hide a failure. Changed source requires new native evidence.

The measured ideal fixture uses 586 actions / 29.3 simulated seconds. The 2,400-action / 120-second run limit allows tracking and bounded-recovery headroom. Twenty short rocking increments maintain the geometric pivot path; their dwell is 0.12 s each. No repeated full tool rotation or unnecessary long settling interval is included. Real runtime remains unmeasured.

## Future GPU qualification, only after separate authorization

```bash
python tasks/er-collet-nut-preassembly/bootstrap_task.py --help
python tasks/er-collet-nut-preassembly/task_runner.py --output /data/er-new-evidence
python tasks/er-collet-nut-preassembly/run.py --mode dream --output /data/er-dream-preview
```

These are previews. `task_runner.py --execute` later runs three native contact/layout probes and two robot prefixes, each repeated after reset, then two independent actual expert episodes. Diagnostic pose initializations are never demonstrations. Dream execution requires the hash-bound native suites and both full-score experts; `--model` also requires completion of the outstanding board novelty review. The real-media pipeline decodes/render-checks videos and binds model/two demos/setup image to receipts and visual review. Submission preparation rejects unexecuted prerequisites. Default workflows do not upload or create PRs; no upload credentials are needed in this offline phase.

Read FIDELITY.md, SETUP.md, PARAMETERS.md, SCORING.md, CONTROLLER.md, CONSTRUCT_VALIDITY.md and NOVELTY.md before native qualification.

## Supplemental CPU contact diagnostics

The offline requirements now include MuJoCo3.3.7. static_check.py runs the exact-scene contact probes twice after reset, as well as unit/geometry/kinematic checks. Read CPU_CONTACT_DIAGNOSTICS.md for solver differences, transient risks and the strict distinction from native Isaac/robot evidence. The standalone command is `python cpu_contact_probe.py --folder . --output /tmp/new-contact-probe`. No GPU or rendering is used.
