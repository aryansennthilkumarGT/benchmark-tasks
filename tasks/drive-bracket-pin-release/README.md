# Release a 2.5-inch drive from its pinned service bracket

A computer-service task grounded in Dell's OptiPlex 7060 Tower Service Manual, pp23–24: pull one bracket side to disengage mounting pins, then lift out the drive. The setup starts with the drive assembly already removed and cables disconnected. This is a replacement for the generic chassis/lid/retaining-bar concept, with actual pin/side-bore retention and compliant release instead of a renamed bar.

Only the drive's **100 × 69.85 × 6.8 mm external envelope** is manufacturer-dimensional (Samsung 870 EVO datasheet). The bracket, bores/pins, handling extension, support fixture, compliance, masses and tolerances are original benchmark approximations. No exact Dell/Samsung interoperability or measured hardware is claimed. Read FIDELITY.md and CONSTRUCT_VALIDITY.md.

Native physics, actual expert, Dream-1 and hardware validation remain **NOT RUN**. CPU path/ideal tracking checks use synthetic jaw contact and cannot demonstrate physical grasp success.

## Offline installation and tests

```bash
python3.12 tasks/drive-bracket-pin-release/install_cpu.py --venv /tmp/drive-cpu-venv
/tmp/drive-cpu-venv/bin/python tasks/drive-bracket-pin-release/static_check.py
```

The isolated installer uses CPU PyTorch and the tested pins in requirements-cpu.txt; no Isaac Sim is installed. `static_check.py` validates protected hashes, unit/adversarial/contracts, actual composed USD, all IK and endpoint robot collisions, inter-part geometry, ideal controller tracking and the actual-FK critical release path. None of these launches a simulator or paid service.

For intentional edits, regenerate `generate_scene.py`, `write_native_cases.py`, `write_parameters.py`, then run `freeze_source.py` and the checks. Altered mechanics/control/scoring invalidate prior runtime evidence. `scene.json` and `parameters.csv` fully specify the authored fixture.

## Future native qualification

```bash
python tasks/drive-bracket-pin-release/bootstrap_task.py --help
python tasks/drive-bracket-pin-release/task_runner.py --output /data/new-drive-evidence
python tasks/drive-bracket-pin-release/run.py --mode dream --output /data/dream-preview
```

These commands only preview. After separate GPU authorization, `task_runner.py --execute` runs three mechanism probes/two control prefixes, each repeated after independent reset, then two real expert episodes. Initializes in diagnostic probes are never demonstrations. Dream requires those prerequisites, exact revision/hash-bound evidence and completion of outstanding board novelty review. `--model` is blocked until that inventory review is cleared. Media rendering validates actual videos, H.264/yuv420p, frame counts, size and provenance; submission preparation requires real qualification and visual review. No official PR is created. Do not supply upload credentials for this offline phase.
