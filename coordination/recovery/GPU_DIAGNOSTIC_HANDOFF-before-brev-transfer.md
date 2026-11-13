> Execution update: the user now wants one continuous authorized engineering/submission sprint, targeting at least three new PRs and then more if feasible. The commands/technical diagnostic scope below remain useful, but diagnostic completion is no longer a session stop. Use the budgeted same-session entry point in [the current sprint plan](../../GPU_RESUME_PLAN.md). Paid start is still unauthorized until explicit start/spend approval.

# First task: cargo native retraction diagnostic

**GO FOR A SEPARATELY AUTHORIZED BOUNDED GPU DIAGNOSTIC. NO-GO for paid Dream, qualification claims or official submission. No paid execution is authorized now.**

Source branch: `optimization/cargo-actuator-tracking`  
Exact source: `4740eba2b60a17041798e690d307b37a120ebfc1`  
Task folder: `tasks/cargo-bar-controlled-release`

Independent clean HTTPS checkout:50 tests pass;1172 ideal actions (58.6 simulated seconds),250 sampled full-path FK configurations pass50um unintentional/800um intended pad bounds. Ideal grasps remain assumptions. Geometry, joint mechanics and scoring are unchanged from6bc24e1, whose complete16-stage clean CPU suite passed. The affected controller/unit/FK checks were rerun rather than repeating the unchanged648-test baseline.

The genuine supplemental MuJoCo3.3.7 YAM run, source clean and hash bound, clears the handle and both pawls, passes repaired phases9/10, then stalls at phase11 controlled retraction:998 actions/49.90 simulated seconds,286.34 wall seconds, score0.25; no warnings, maximum measured SDK velocity ratio0.7896435, maximum task interference128.74um (below350um), robot contact depth21.60um. This is NOT Isaac or full task success. Persistent gripper command and physical-hold verification repairs are implemented. At the terminal state the left grip command has reached0.18 (measured0.265574), telescope remains16.266mm against the≤4.5mm target, and left TCP is12.736mm behind the retraction goal inY. Handle2.59909rad and both pawls are physically clear; this is not the earlier verification defect. Repeated substantial CPU repairs have not established controlled shortening; stop speculative same-blocker iterations and measure actual native behavior. See cpu-yam-diagnostics/cargo-retraction-stall-4740eba for immutable report/model/trace and clean checks.

On an already running, separately authorized existing Brev terminal (no provisioning), verify the installed pinned runtime and scored official station smoke. No driver changes or reinstall are requested. Fresh actual rate/balance and an explicitly bounded spend authorization are prerequisites to paid work. Historical$29.60 is not current funding. Then:

```bash
source /data/IsaacLab-Arena/yam.env
GPU_PY=/data/IsaacLab-Arena/.venv/bin/python
SOURCE_REV=4740eba2b60a17041798e690d307b37a120ebfc1
git -C /data/benchmark-tasks fetch origin optimization/cargo-actuator-tracking
git -C /data/benchmark-tasks checkout --detach "$SOURCE_REV"
test "$(git -C /data/benchmark-tasks rev-parse HEAD)" = "$SOURCE_REV"
test -z "$(git -C /data/benchmark-tasks status --porcelain)"
TASK=/data/benchmark-tasks/tasks/cargo-bar-controlled-release
timeout --signal=TERM --kill-after=30s 1200s "$GPU_PY" "$TASK/native_tests.py" \
  --mode control --case retract_controlled_inner_tube --fail-fast \
  --commit "$SOURCE_REV" --output /data/robocurve-diagnostics/cargo-4740-retract
```

Use a new output directory. Expected allowance10–20minutes including startup and two reset repeats is a planning estimate, not measured native timing. At approximately1000actions per repeat the two prefixes cover100simulated seconds; the estimate is informed by public accepted native traces, not measured performance of this source. Each prefix permits3500actions/175simulated seconds, so a worst-case run can exceed the20minute allowance and must terminate as a timeout. Stop at first failure or wall timeout, preserving results.json, events, controller failure state, native frames, robot effort/command references and process output. Specifically distinguish startup/API errors, failed forceful loaded grasp, pawl reengagement, blocked telescope, part slip and insufficient grip force. Do not equate zero Kit exit or passing a prefix with task success. Workload timeout does not stop provider billing.

For the standalone reviewer reproduction alternative, after genuine passing prefixes and only within separately authorized scope, `"$GPU_PY" "$TASK/task_runner.py" --output /data/robocurve-cargo-qualification --execute` runs every native case twice and two full experts. A third clean-checkout expert is our stronger internal reproducibility check, not an official minimum. Full scorer1.0, real release/stability, camera streams and source hashes must validate before Dream. Then `--execute --resume --model` on the same task-runner output performs genuine Dream and media. Inspect actual model/demo videos and setup/contact sheets before an explicit visual attestation. `prepare_submission.py` gates genuine evidence and the official uploader; never fabricate scores/media or collect credentials in this CPU phase. The coordinator now binds handoff claims to their actual receipts/publication checkout and checks official PR history before a push. One task-folder PR only after actual native, model/media evidence and authorized submission. PR1733 and finally rejected heads remain untouched.

ER is second: exact e665928 clean checks pass; its new actual CPU run retains the collet through lift/transfer/tilt, then stalls at phase7 lowering into the eccentric opening (676actions/33.8s,score0,SDK ratio0.83329). Preserve that trace and use only the bounded native entry diagnostic next. Nailer is third: the new b742696 actual CPU run extracts/deposits the brad but still reaches an IK limit at phase30 pin acquisition (2065actions/103.25s,score0.5,SDK ratio0.79332). It remains NO-GO for acceptance spending because routine core-job importance is unproven and real pin capture has not completed. The radial experiment has confirmed arm collisions and is explicitly excluded. These holds do not delay the first cargo diagnostic.


Exact second/third sources and bounded commands (neither currently authorized to execute):

| Priority | Branch | Exact source | Decision |
|---|---|---|---|
| ER second | optimization/er-actuator-tracking | e6659287a5ac2e2d968bc0d39122659ef7cd2a11 | Bounded grip/entry diagnostic only; no native success |
| Nailer third | repair/nailer-integrity-and-grip | b742696e49a506bfd4ef2362a06145b8a6cd3c65 | NO-GO acceptance spending; routine importance and real pin capture unresolved |

In the exact ER source checkout, after separate authorization:

```bash
timeout --signal=TERM --kill-after=30s 900s "$GPU_PY" \
 /data/benchmark-tasks/tasks/er-collet-nut-preassembly/native_tests.py \
 --mode control --case eccentric-hook-prefix --fail-fast \
 --commit e6659287a5ac2e2d968bc0d39122659ef7cd2a11 \
 --output /data/robocurve-diagnostics/er-e665-hook
```

The ER terminal CPU state has123um position error but35.82mrad physical-axis error against the unchanged20mrad phase target; no task overlap or warnings. The ER prefix repeats after reset, maximum1200actions/60simulated seconds each;5–15minutes is an unmeasured planning estimate. Stop on grip loss, cam interference>100um, IK/SDK/integrity failure or timeout. The full supported-preassembly-prefix remains a later distinct test.

Only if explicitly authorized specifically for a nailer diagnostic despite the importance hold, in its exact separate source checkout:

```bash
timeout --signal=TERM --kill-after=30s 1200s "$GPU_PY" \
 /data/benchmark-tasks/tasks/brad-nailer-jam-recovery/native_tests.py \
 --mode control --case robot_46 --fail-fast \
 --commit b742696e49a506bfd4ef2362a06145b8a6cd3c65 \
 --output /data/robocurve-diagnostics/nailer-b742-relatch
```

robot_46 is the actual configured full-controller prefix through Released fixture hold, including the phase30 pin acquisition blocker. It allows5000actions/250simulated seconds per reset repeat, so20minutes is a hard cap, not a promised completion time. Stop first failed acquisition, lost/deformed capture, interarm/task contact violation or timeout. Do not substitute the collision-failing radial experiment. This diagnostic cannot resolve occupational importance.

For later complete automatic publication, use the single-task coordinator path described in [the current coordinator instructions](../README.md). The standalone task_runner path above is a separate reviewer reproduction option; do not run both complete paths sequentially and duplicate native/expert/Dream costs. Their ledger contexts differ. The coordinator creates its own actual ready handoff, and only that handoff can enter submit_ready.py. Real media review and fresh official submission authorization remain necessary.


For SDK measurements on the first authorized cargo diagnostic, prefer the instrumented equivalent below INSTEAD OF running both commands. The wrapper executes the exact same frozen native test, keeps20Hz rendering and960Hz task physics, and adds20Hz measured velocity/applied-effort recording and first observed SDK violation stop. It does not certify unobserved physics-substep peaks. The helper itself is CPU-tested but not yet native-tested; an API/startup failure is a diagnostic failure, never grounds for an automatic expensive retry.

Keep coordinator and task sources in separate checkouts:

```bash
git -C /data/benchmark-tasks fetch origin dcac58e442a0d2da083ecdd13bd76f3c189c3576
git -C /data/benchmark-tasks worktree add --detach /data/robocurve-coordinator dcac58e442a0d2da083ecdd13bd76f3c189c3576
# TASK checkout stays at4740eba2b60a17041798e690d307b37a120ebfc1.
timeout --signal=TERM --kill-after=30s 1200s "$GPU_PY" \
 /data/robocurve-coordinator/coordination/diagnostic_native.py \
 --folder "$TASK" --mode control --case retract_controlled_inner_tube \
 --commit 4740eba2b60a17041798e690d307b37a120ebfc1 \
 --output /data/robocurve-diagnostics/cargo-4740-sdk \
 --expected-physics-hz 960 --render-every 1 --sdk-limits --fail-fast
```

If the coordinator checkout already exists, verify its clean exact dcac58e source instead of adding another worktree over it. This shares the existing Git object cache and leaves the task checkout unchanged. Native telemetry appears in native-sdk-samples.jsonl and the adjacent render-diagnostic.json receipt, including original native script/wrapper hashes, actual configured device/timing and SDK SI caps. The ordinary native failure artifact retains controller/gripper references and actual applied efforts. No source controller/scorer, gain, task geometry or state is changed by this diagnostic. For an explicitly authorized ER/nailer diagnostic the same helper accepts their actual480/1920Hz physics; keep the exact task source/case/timeouts above. No authorization to execute is implied by any command here.
