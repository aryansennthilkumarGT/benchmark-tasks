# Cargo first: bounded native diagnostic

Decision: **source verification in progress; no native feasibility or acceptance claimed**. This task is first because the actual CPU controller already opens the handle, confirms both pawls clear and reaches controlled retraction. Its next known code defect—measured-aperture-based grip slew—is repaired by a persistent command. Native contact/force/velocity and full score remain unproven. MuJoCo is supplemental, not the target simulator.

Do not provision/connect/start compute or execute paid work until separately authorized with fresh provider balance/price observations. The historical$29.60 is not a current balance or spending authorization. Use the existing pinned environment, without driver or full-stack reinstallation. Workload timeout does not stop provider billing.

On the authorized existing Brev terminal, verify the official environment and use its installed Python:

```bash
source /data/IsaacLab-Arena/yam.env
GPU_PY=/data/IsaacLab-Arena/.venv/bin/python
TASK=/data/benchmark-tasks/tasks/cargo-bar-controlled-release
SOURCE_REV=$(git -C /data/benchmark-tasks rev-parse HEAD)
test -z "$(git -C /data/benchmark-tasks status --porcelain)"
# Exact SOURCE_REV must match the published recovery handoff, not a moving head.
# One real native prefix, repeated after reset; first failure stops the suite.
timeout --signal=TERM --kill-after=30s 1200s "$GPU_PY" "$TASK/native_tests.py"   --mode control --case retract_controlled_inner_tube --fail-fast   --commit "$SOURCE_REV" --output /data/robocurve-diagnostics/cargo-retract
```

Expected planning allowance:10–20minutes including startup and two reset repeats; cold RTX compilation may exceed this and must be reported as timeout, not success. This is an estimate, not measured performance. The two native prefixes each allow3500actions/175simulated seconds. Do not automatically retry the same failed source.

Checkpoints: trigger displacement7–9.3mm; handle angle2.45–2.63rad; both pawl clearances per controller; telescoping coordinate at most4.5mm; task interference at most0.35mm; valid original scorer. On failure retain `results.json`, `*-control-failure.json`, events, native telemetry and process log. Failure diagnostics include measured robot positions, persistent gripper references, actual applied actuator efforts, task joints and last physical state. Report early startup failure separately from controller/contact failure. A partial prefix or zero Kit exit is not task success.

A passing diagnostic authorizes no further paid action by itself. If the authorized budget covers it, next run the existing one-task qualification tool:

```bash
"$GPU_PY" "$TASK/task_runner.py" --output /data/robocurve-cargo-qualification --execute
```

It runs every mechanism/control case after reset and two distinct full-score expert episodes. Then independently clone the same exact source and run a third expert with `run.py --mode expert --commit "$SOURCE_REV" --output <new-directory> --execute`, validating its log using `validate_rollout.py --directory <trial> --mode expert --limit 5000 --commit "$SOURCE_REV" --folder <clean-task-folder>`.

Only after genuine native/expert success and separately authorized evaluation:

```bash
"$GPU_PY" "$TASK/task_runner.py" --output /data/robocurve-cargo-qualification --execute --resume --model
```

This uses verified same-source feasibility receipts for the actual Dream-1 call and renders real media. Inspect the actual videos/setup/contact sheets; do not fabricate a visual-review attestation. `prepare_submission.py --help` lists the exact verified-evidence packaging/upload options. Official upload uses repository `tools/upload_media.py`; credentials must be securely configured only in that later authorized phase. Update genuine scores/media IDs, preserve source/runtime equivalence, and open one task-folder PR only after all required evidence is valid. The recovery coordinator provides receipt-gated media review and PR submission; its batch top-three gate is not a prerequisite for this bounded single-task diagnostic.

Stop conditions: timeout, bad environment/source, missing/failed native report, physical integrity failure, joint/velocity/effort violation, dropped/slipping grip or stalled retraction. After two substantial unsuccessful fixes at one blocker, retain the exact trace and use a focused native mechanism diagnostic; do not spend the window on repeated broad runs. Do not launch Dream or uploads on a failed prefix. Official PR#1733 and all finally rejected heads remain untouched.
