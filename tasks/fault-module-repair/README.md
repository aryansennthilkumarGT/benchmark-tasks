# Balance and lock a counterweighted service arm

Support the loaded arm, slide its counterweight until the pin holes align at the orange index, insert the locking pin through both holes, and leave the arm level with both hands clear.

`validation.json` records the native tests, two full-score expert episodes, completed Dream-1 trial and official media ID.

## Independent reproduction

This folder contains its scene, assets, scorer and fixed robot joint-command expert. Use the Python environment installed by the pinned official YAM Launchable. Set `ARENA_PYTHON` to that environment's Python and `RUN_DIR` to an empty evidence directory outside this checkout. Run from the repository root with a clean Git tree.

```bash
export ARENA_PYTHON=/path/to/IsaacLab-Arena/.venv/bin/python
export RUN_DIR=/path/to/persistent/service-arm-evidence
"$ARENA_PYTHON" tasks/fault-module-repair/static_check.py
"$ARENA_PYTHON" tasks/fault-module-repair/run.py --mode expert --execute --commit "$(git rev-parse HEAD)" --seed 0 --output "$RUN_DIR/expert-1"
"$ARENA_PYTHON" tasks/fault-module-repair/run.py --mode expert --execute --commit "$(git rev-parse HEAD)" --seed 0 --output "$RUN_DIR/expert-2"
```

Each expert invocation creates a fresh simulator and reset. Inspect the finalized Inspect log, native frames, scorer replay and recorded actions with `validate_rollout.py`. A process exit by itself does not establish success. `run.py` without `--execute` previews the command. Native initialization and controlled force probes are available through `native_tests.py`; their fixture manipulation is excluded from expert demonstrations.

The optional `bootstrap_task.py` prepares the pinned environment and applies managed-provider cost controls. `task_runner.py` supports an installed environment and preserves native, expert, model and media evidence with hash-verified resume.

## Environment and cost

`stack-lock.json` pins the official launchable, adapter, Arena release, Inspect Robots and Dream plugin commits. It uses Python 3.12, Isaac Sim 6.1.0.0, NumPy 2.3.1 and the official bimanual I2RT YAM station. The adapter's 14-D action is left six absolute joints + normalized jaw opening, then right six + opening. Physics is 240 Hz; control is 20 Hz; observations are the three official 320x176 RGB cameras and robot joints.

The tested native installation uses NVIDIA L40S with 48 GB VRAM and driver 565.57.01. The installed Launchable provides the pinned simulator and adapters. Recordings use approximately 0.51 MB per action for three uncompressed RGB observations, plus metadata and exported media. Allocate persistent storage for all required trials.

The optional managed launcher accepts a provider budget record for its cost guard. Independent expert reproduction uses the direct commands above. Keep model and upload credentials in their secure configuration.

## Trials and scoring

Seed 0 and `object_jitter=0` are fixed for both expert repeats and the model. Maximum 4800 actions (240 simulated seconds). The two validated expert episodes each used 1899 actions and 94.95 simulated seconds. Inspect reported trial durations of 1067.723 s and 590.097 s on the tested L40S stack. Simulator startup adds overhead. Wall time depends on physics, rendering and model latency. The scorer recomputes partial credit and requires 3 s of final stability and released-arm clearance. Read [SCORING.md](SCORING.md) for every numerical condition and [SETUP.md](SETUP.md) for every body, material, mass, dimension and pose.

The native suite contains 4 physics cases and 2 real robot-control cases, each repeated after independent resets. Physics probes may initialize mechanism poses and apply forces for controlled measurements; those probes are explicitly excluded from demonstration/media evidence. Control probes use only robot actions. Two full expert episodes separately establish feasibility before model spending.

## Implementation and limits

A damped, unpowered pivot and explicit mass/center-of-mass values model a loaded service arm. Prismatic guidance approximates the counterweight rail. A free pin enters collision-defined holes. The pivot has no centering spring.

Read [CONTROLLER.md](CONTROLLER.md), [NOVELTY.md](NOVELTY.md), and `mechanics-review.json` for the demonstration strategy, comparison review and five criteria. Rigid USD parse checks, synthetic scoring tests and ideal IK replay are offline evidence only. Native contacts, camera rendering, reliable reset and complete action execution require separate runtime evidence.

`build_assets.py` deterministically derives included `.usda` assets from `scene.json`; run it only when intentionally changing the scene, then update hashes and commit. `source_manifest.json` hashes LF-normalized source and asset bytes. `run.py` launches one official trial, `task_runner.py` preserves/gates native evidence, `validate_rollout.py` cross-checks logs/actions/frames/scorer replay, and `render_media.py` exports and fully decodes H.264 yuv420p media. A zero Dream score is valid evidence when the required successful demonstrations exist. Public media require visual inspection for framing, mechanical outcome and blind-review compliance before upload.

Dream-1 (dreamlabs/dream-1-beta) completed 4800 actions and scored 0.0. The validated record reports a genuine non-dry-run model execution; recorder chunk counts are not asserted as provider request counts. Temporary session-expiration retries recovered during the same simulator episode. The model trial used 240 simulated seconds and 2034.729 seconds of recorded wall time. All three camera streams contain 4801 observations.


## Fixed-action demonstration revision

The revised expert executes an offline-authored 14-dimensional robot joint/jaw program. It reads no runtime task object pose, mechanism joint, evaluator or score. Authored checkpoints mark action indices, not measured phase completion. Two new whole cold episodes each scored 1.0 in 1899 actions (94.95 simulated seconds), including one from a fresh HTTPS checkout. Runtime measurements were 1067.7 and 590.1 wall seconds. The prior genuine Dream-1 run remains 0.0; its exact source revision is retained rather than relabeled. Scene, physics, scoring and model inputs are unchanged.
