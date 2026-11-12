# Capture a twelve-cell pack's shared spring preload with a cross-key

Close a loaded pack by seating the pressure plate across twelve independent spring contacts and transferring the load to a retaining cross-key. The task starts with the cells loaded. The plate and key are loose.

## Reproduction

Use the pinned official YAM Launchable Python environment. From a clean repository checkout, set `ARENA_PYTHON` to its Python and `RUN_DIR` to an empty persistent directory outside the checkout.

```bash
"$ARENA_PYTHON" tasks/twelve-cell-pack/static_check.py
"$ARENA_PYTHON" tasks/twelve-cell-pack/native_tests.py --mode physics --commit "$(git rev-parse HEAD)" --output "$RUN_DIR/physics"
"$ARENA_PYTHON" tasks/twelve-cell-pack/native_tests.py --mode control --commit "$(git rev-parse HEAD)" --output "$RUN_DIR/control"
"$ARENA_PYTHON" tasks/twelve-cell-pack/run.py --mode expert --execute --commit "$(git rev-parse HEAD)" --seed 0 --output "$RUN_DIR/expert-1"
"$ARENA_PYTHON" tasks/twelve-cell-pack/run.py --mode expert --execute --commit "$(git rev-parse HEAD)" --seed 0 --output "$RUN_DIR/expert-2"
```

Each native physics case and robot-control case runs twice after independent resets. Six physics cases produce twelve results. Two robot-control cases produce four results. Physics fixtures may initialize isolated mechanism states. Recorded experts start from the declared setup and use fourteen-dimensional joint/gripper actions throughout.

The run limit is 3600 actions at 20 Hz, or 180 simulated seconds. Seed 0 and zero object jitter are fixed. Two independently executed full-score expert runs each used 1677 actions (83.85 simulated seconds), with measured wall times of 1998.36 and 2544.47 seconds under shared GPU load. Dream-1 completed 3,600 genuine actions with score 0.0. A third full-score expert from a fresh HTTPS checkout also used 1,677 actions, taking 1,665.59 seconds. Wall time depends on shared GPU load. Check finalized Inspect logs, native traces and `validate_rollout.py` before claiming a successful trial. `run.py` without `--execute` previews its command.

## Mechanism and fidelity

A rigid pressure plate simultaneously loads twelve 500 N/m contact springs. The cross-key must retain this compression after both hands release. Cylindrical cell geometry includes polarity-dependent terminal profiles. The model omits electrical and electrochemical behavior. Geometry, masses and local transforms are defined in `scene.json` and its generated USD assets.

Read [SETUP.md](SETUP.md), [SCORING.md](SCORING.md) and [NOVELTY.md](NOVELTY.md) for the fixed layout, numerical objectives and mechanism-specific comparison. Measured native, expert and model evidence is recorded in validation.json. Clean-checkout reproduction also reached full score.


## Fixed-action expert revision

The expert executes1677 offline-authored14-dimensional joint and jaw commands, reading only robot proprioception and elapsed action index. It reads no object poses, task joints or scoring state. Two complete cold episodes each scored1.0 in83.85 simulated seconds; the second ran from a fresh HTTPS checkout. The original genuine Dream-1 result remains0.0 at its original source revision; scene, scoring, physics and model inputs are unchanged. Diagnostic feedback controllers and fixture initialization are excluded from these demonstrations.


## Physical measurement access

See [MEASUREMENT.md](MEASUREMENT.md) for twelve independent noncontact compression readings after closure, using solid optical windows in the physical holder/guide walls and coplanar reference scales. The simulator retains opaque solid walls; the judging-only windows and witness marks are omitted from its rendering. The design does not add a manipulation opening, remove a support or change the score thresholds.
