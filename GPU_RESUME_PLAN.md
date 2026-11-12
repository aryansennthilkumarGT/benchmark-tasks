# GPU resumption: authorization and exact-source qualification

This recovery is incomplete. `coordination/recovery/CHECKPOINT.json` is authoritative for the new CPU mission. None of the three finally rejected tasks is eligible for resubmission; PR #1733 must retain its pending head. Offline passes preserve engineering assets, but do not clear importance, novelty or physical feasibility.

## Continue CPU engineering

```bash
cd /workspace/benchmark-tasks
source /workspace/.robocurve-offline/venv/bin/activate
export CUDA_VISIBLE_DEVICES=''
export PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
python -m pytest -q -p no:cacheprovider coordination
python coordination/offline_recovery.py --output /workspace/robocurve-recovery-evidence --audits --resume
```

The runner resolves current local `origin/draft/*` refs, not old manifest commit pins. Refresh these refs with read-only Git fetch when needed. `--dry-run` prints targets without running tests. It creates archives outside the checkout, checks source hashes and syntax, checks that the branch diff is confined to its task folder, runs real tests and six existing offline audit programs, and records immutable per-attempt logs, test counts, hashes and receipts. Failed tasks do not discard successful tasks. `--resume` verifies all retained bytes. A changed source commit creates a new attempt; one diagnosed retry of unchanged failed inputs uses `--retry-failed 'specific diagnosis'`. No zero-test or all-skipped test run passes.

Replacement task development must begin with actual primary equipment documentation and a fresh accepted/pending novelty screen. The network draft requests the destinations needed for this research; GitHub public PR conversations are already readable. Full board access and manufacturer documentation currently return proxy 403. Save these changes in environment settings, then retry; no credential values are needed for public research. Do not fill missing dimensions with claimed manufacturer values.

## Future GPU prerequisites

Obtain renewed user authorization and a fresh provider-observed budget before executing any GPU stage. Do not provision Brev, purchase credits, modify billing or reuse exposed upload credentials. The historic `/data` evidence is absent here; restoring it is optional for new work but necessary to revalidate old raw records. Never fabricate replacement records from committed summaries.

Use the task's pinned Python 3.12 / Isaac Sim 6.1 / YAM-Arena stack. Inspect actual GPU, available VRAM, RAM, free storage, package sources and driver. The existing hardware policy supports L40S driver 565.57.01 with a verified installed Launchable and requires an actual scored station smoke test; it does not require a driver replacement. CUDA 2-D/3-D observation and native PhysX compatibility remain application tests, not consequences of an `nvidia-smi` response.

The task documents specify at least 16 GiB free VRAM, 32 GB RAM (24 GB available) and 250 GiB free disk. These are stack prerequisites, not a measured cost or duration estimate. Each trial retains three 320x176 camera streams. Select one task at a time; parallel paid jobs are not part of this plan. Model run limits vary by task and are read from its exact scene. No credible replacement-task wall-time or compute cost exists until that task is implemented and measured.

## Immutable checkout and safe preview

After a replacement has been implemented, audited, committed, pushed to its independent branch and explicitly cleared for native qualification, assign its full SHA and task slug. The following shell variables are intentionally required operator inputs, not invented values:

```bash
: "${TASK_SHA:?set the reviewed full commit}"
: "${TASK_SLUG:?set the actual task folder slug}"
: "${QUALIFICATION_CHECKOUT:?set a new clean checkout directory}"
: "${TASK_EVIDENCE:?set an evidence directory outside the checkout}"
: "${BUDGET_RECEIPT:?set the actual current provider budget receipt path}"
: "${LAUNCHABLE_ROOT:?set the verified installed stack root}"
git clone --no-checkout https://github.com/aryansennthilkumarGT/benchmark-tasks.git "$QUALIFICATION_CHECKOUT"
git -C "$QUALIFICATION_CHECKOUT" checkout --detach "$TASK_SHA"
cd "$QUALIFICATION_CHECKOUT"
python3 "tasks/$TASK_SLUG/bootstrap_task.py" \
  --output "$TASK_EVIDENCE" --budget-file "$BUDGET_RECEIPT" \
  --launchable-root "$LAUNCHABLE_ROOT" --model
```

This previews only. The existing standalone bootstrap parses these flags without checking hardware, installing packages or running a trial when `--execute` is absent. All existing draft previews are tested separately in the recovery receipts. A new replacement must carry and test its own standalone bootstrap and source manifest; a preview from an old branch does not certify a new package.

Only after renewed authorization and actual budget verification, append `--execute` to that exact command. The bootstrap verifies hardware and installed package sources, matches GPU UUID to the budget, runs the official apple/bowl smoke, runs source/static checks, then delegates to the task's resumable native/expert/model/media runner. The current inherited budget class enforces a $170 total charge cap and $30 remaining reserve. These historical limits must be reconciled with the next expressly authorized budget; do not forge budget fields to pass them. The monitor stops owned subprocess groups, not cloud instance billing.

## Required validation order and failure recovery

1. Verify exact source bytes and official runtime; complete a scored station smoke.
2. Run every native mechanism and robot-control case after the independent resets specified in `native-cases.json`. Report missing, failed and skipped cases distinctly. CPU PhysX still requires Isaac and is not available in this Codex environment.
3. Complete two independent whole expert episodes at full score within the actual action limit. Validate native observations and all actions. Do not qualify a controller that reads privileged object state as an action-only expert. Diagnostic fixture initialization and controlled-force probes are not demonstration evidence.
4. Run genuine Dream-1 only after those gates, with fresh authorization/budget still valid. Preserve actual zero scores and SDK failures; do not reuse expert footage as model evidence.
5. Replay the scorer, test invalid strategies, verify all three camera streams, record exact source/stack/artifact hashes, export real H.264/yuv420p videos and the actual initial screenshot, fully decode videos, and perform visual blind-review inspection.
6. Repeat the required trial from a separate clean checkout. Resume only same-input successful receipts. Changed geometry, dynamics or controller code requires new qualification; never transfer an old score to a replacement concept.

Use the same command with `--execute --resume` after checking previous failures. Logs and ledger receipts stay immutable. An unchanged failed stage requires one explicit, supported retry diagnosis; changed code gets a new commit and evidence directory. A zero wrapper exit without complete native reports, actions, observations and scorer validation cannot pass.

## Upload and official submission

These steps remain disabled during CPU recovery and until all source/importance/novelty/runtime/media gates pass. Rotate previously exposed RoboCurve credentials before any reuse, and provide credentials through secure environment settings rather than Git or chat. Use the repository's `tools/upload_media.py` to upload the actual model video, successful demonstration and setup screenshot; retain the server-generated media ID. Populate metadata with real measured scores, never placeholders. Use a disposable metadata copy so evaluated source bytes remain immutable. Enforce setup <=4000 and fidelity <=500 characters before upload/submission.

The existing coordinator's media-review and submit-ready gates bind review to exact bytes and verify required receipts and current remote commits. A new task needs one independent branch with changes in exactly its task folder, and one official PR after qualification. Inspect existing PRs before any create action; do not reopen final closures #1647/#1703/#1772 or duplicate #1733. Respect pending review immutability and revision instructions. No submission-ready handoff should contain the three rejected concepts or any merely renamed variant.

## First rebuilt CPU candidate

The occupational screw-pin shackle replacement is published independently as `draft/rigging-shackle-connection`, commit `ef13ec77d7ac6ee56aeb3c6c62069444af4efa02`. Its complete CPU checks passed from a clean HTTPS clone. Read its task README and `offline-evidence/summary.json`; native physics, real grasp success, expert episodes, model scores and actual media remain untested. Do not use old service-arm evidence for this package.

For a safe preview, clone that branch, verify the full SHA above, activate the CPU dependencies listed in its `requirements-cpu.txt`, and run:

```bash
python tasks/rigging-shackle-connection/bootstrap_task.py --output /data/shackle-qualification --model
```

This preview does not create a runtime. The README gives the future authorized execution flags and actual native commands. Six other rebuilds remain; there is no eight-task GPU-ready manifest yet. Continue their task-by-task implementation before treating the overall engineering phase as complete.
