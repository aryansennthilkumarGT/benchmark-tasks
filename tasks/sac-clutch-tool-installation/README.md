# Mount and retain a SAC installation-tool carrier

This is an original **BENCHMARK_AUTHORED** fixture for the unloaded mounting step in the LuK SAC installation-tool procedure. Its component dimensions are not measurements of LuK or Sealey hardware. The disc, pressure cover, dowels and lower stud installation are prepared initial conditions. Mount the three-arm carrier over the mandrel and three studs, independently screw all three knurled retainers flush, release, and stop before pressure-spindle compression.

Native physics, actual expert demonstrations, Dream-1 and physical hardware validation have **not** run. Offline ideal tracking assumes contact apertures and cannot establish grasp/retention feasibility. No official submission is permitted with the current evidence.

## CPU reproduction

Python 3.12 was used. The exact compatible CPU package versions are in `requirements-cpu.txt` and `stack-lock.json`. Use an existing prepared offline environment or run the isolated installer:

```bash
python3.12 tasks/sac-clutch-tool-installation/install_cpu.py --venv /tmp/sac-cpu-venv
/tmp/sac-cpu-venv/bin/python tasks/sac-clutch-tool-installation/static_check.py
```

The installer selects CPU PyTorch and does not install Isaac Sim. No credentials are needed. `static_check.py` verifies protected hashes, runs tests and all geometry/IK/controller/collision audits. The model/evaluation scripts are not called by it.

Intentional geometry edits require explicit regeneration and a new source freeze, invalidating old runtime evidence:

```bash
python tasks/sac-clutch-tool-installation/generate_scene.py
python tasks/sac-clutch-tool-installation/write_native_cases.py
python tasks/sac-clutch-tool-installation/write_parameter_table.py
python tasks/sac-clutch-tool-installation/freeze_source.py
python tasks/sac-clutch-tool-installation/static_check.py
```

`source_manifest.json` binds exact code/assets/metadata. Reports below `offline-evidence/` identify the source hash manifest and clearly distinguish numerical fixtures from physics. Do not copy evidence from the shackle or older spring-plate task.

## Future native qualification (requires separate GPU authorization)

Use the pinned official stack described by `bootstrap_task.py` / `stack-lock.json`. These previews do not install or launch anything:

```bash
python tasks/sac-clutch-tool-installation/bootstrap_task.py --help
python tasks/sac-clutch-tool-installation/task_runner.py --output /data/sac-new-evidence
python tasks/sac-clutch-tool-installation/run.py --mode expert --output /data/sac-expert-preview
python tasks/sac-clutch-tool-installation/run.py --mode dream --output /data/sac-dream-preview
```

After GPU access is separately authorized, `task_runner.py --execute` runs four native contact probes and two robot prefixes (each repeated after reset), then two independent expert episodes. The probes deliberately initialize isolated states and are **not** demonstrations. Any failure stops qualification. Runtime adapter reads actual rigid-body poses/velocities and collision geometry and never attaches dynamic parts. Native controls issue the same 14 robot joint/gripper commands as the expert.

Dream execution requires native suites plus two independently verified full-score expert records of the exact current commit. Complete the outstanding novelty inventory review before using `--model`; the task runner currently blocks it on that unresolved review. `run.py --mode dream --execute --evidence ...` independently verifies receipt hashes; no model request is made by default. No GPU provisioning or credit purchase script is included.

The media pipeline decodes real rendered frames, checks H.264/yuv420p, dimensions, frame count and size, and binds two demos, model video and setup image to real receipts. `prepare_submission.py` requires actual native/expert/model/media results plus a visual-review attestation. It does not create a PR; default mode does not upload. Do not supply upload credentials during this offline phase.

Read [FIDELITY.md](FIDELITY.md), [SETUP.md](SETUP.md), [PARAMETER_TABLE.md](PARAMETER_TABLE.md), [SCORING.md](SCORING.md), [CONTROLLER.md](CONTROLLER.md), [CONSTRUCT_VALIDITY.md](CONSTRUCT_VALIDITY.md) and [NOVELTY.md](NOVELTY.md) before qualification.
