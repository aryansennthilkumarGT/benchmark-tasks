# Eight-task engineering handoff

This branch coordinates eight independent task branches. Two tasks are engineering-complete and officially received for review: [service-arm repair #1647](https://github.com/robocurve/benchmark-tasks/pull/1647), task TK-GLK4ZE, and [spring-cover cell exchange #1703](https://github.com/robocurve/benchmark-tasks/pull/1703), task TK-HSZNSX. Neither is confirmed accepted. Six tasks remain in engineering.

For the current execution, read `mission-checkpoint.json` and the latest entries in [the live checkpoint](live-execution-2026-11-10.md), then inspect the recorded producer PIDs and actual logs before launching anything. Existing standalone qualifications and queued jobs use four long-running GPU lanes. A bounded additional diagnostic can use verified spare memory while those runs progress; its timeout and evidence scope are recorded in the checkpoint. Do not start `--all` alongside them. A missing result or zero wrapper exit is never a passing test. Source revisions remain frozen while their qualification is active or queued.

The original draft manifest and offline receipts preserve earlier reproducible coordinator runs; they are historical evidence, not the current task heads. Current task revisions, queued dependencies, official PRs and budget receipts are in the machine-readable checkpoint. The latest user-authorized reserve is $22. Owned workload cancellation does not stop Brev instance billing. Never stop the partner instance; stop the original Launchable only after all eight tasks are genuinely complete and submitted.

## One entry point

From this handoff checkout in the authorized official Linux GPU environment:

```bash
bash coordination/bootstrap_and_run.sh --all
```

The default run directory is `.robocurve-runs` and the provider budget receipt is `.robocurve-budget.json`, both ignored by Git. Configure `ROBOCURVE_RUN_ROOT` and `ROBOCURVE_BUDGET_FILE` to use persistent storage outside the checkout. The runner itself needs Python 3.10+ and Git; the isolated official stack uses Python 3.12. No source editing or manual branch switching is required.

Before executing, the operator/agent supplies actual provider price, credit balance and observation timestamp, instance start time, prior spend, instance ID and GPU UUID. `record_budget.py --help` records these facts without credentials. Dream credentials use the official secure configuration; uploads read `ROBOCURVE_TOKEN` and set `ROBOCURVE_TEAM=T-06` only in the uploader process. Git credentials must permit pushes to the fork. No credentials belong in a task folder, receipt, command argument or commit.

Useful modes:

```bash
bash coordination/bootstrap_and_run.sh --dry-run
bash coordination/bootstrap_and_run.sh --preflight
bash coordination/bootstrap_and_run.sh --task fault-module-repair --launchable-root /data
bash coordination/bootstrap_and_run.sh --resume
bash coordination/bootstrap_and_run.sh --all --no-upload
bash coordination/bootstrap_and_run.sh --all --offline
```

`--dry-run` performs no network, installation, simulator or model work. `--preflight` reports hardware and credential presence without starting evaluation. `--offline` requires NumPy, usd-core and the pinned YAM adapter importable in the current Python; it never advances past static checks. The GPU runner verifies the existing vendor stack when given `--launchable-root`, or installs the pinned stack in an isolated directory. It requires a full-score official apple/bowl smoke trial before any task. Each task is fetched at its manifest SHA into its own clean detached worktree. The diff must remain under that one task folder.

## Required environment

Use the official walkthrough launchable and the commits in `stack-lock.json`. Hardware profiles: L40S / RTX 4090 / RTX 5090, at least 16 GiB free VRAM, 32 GB system RAM with 24 GiB available, and 250 GiB free disk. Isaac Lab recommends Linux driver 580.95.05. Isaac Sim 6.1 lists 595.58.03 as tested. On the specific L40S profile with fixed driver 565.57.01, preflight reports that the official smoke is required. Use `--launchable-root /data` with the existing pinned Launchable. The successful smoke and task receipts include the selected GPU and driver. The bootstrap uses the official pinned installer in an isolated project directory and preserves existing vendor EULA acceptance. It does not update drivers, alter system Python, connect SSH/VPN, deploy Brev or stop another user's jobs.

The launchable, adapter, Arena, IsaacLab, Inspect Robots and Dream plugin revisions are documented in the lock. Arena's release branch is named 0.3.1 although its distribution metadata says 0.3.0. Isaac Sim 6.1.0.0 and NumPy 2.3.1 come from that supported stack; no assumed compatibility with an old 5.1 environment. The same production asset-bucket correction used by the official launchable is applied explicitly.

GPU work is sequential. The cost monitor counts instance wall time, including idle time, and refuses a stage whose timeout would exceed $170 total charges or the $30 reserve. It checks during subprocess execution and terminates its own process group at the limit. Brev billing continues until the user stops the instance through the provider. No model cost or compute price is fabricated. Retain provider receipts for reconciliation.

## Evidence and failure behavior

Each stage has an immutable attempt directory and a receipt containing input revision, predecessor keys and artifact hashes. Successful evidence survives independent task failures. `--resume` verifies hashes and reuses success; it does not rerun successful GPU work. An unchanged failed stage stops without spending again. One explicit `--retry-failed 'diagnostic reason'` is allowed; a genuine code fix should be committed, pushed and pinned as a new revision. Never edit an evaluated worktree or modify old receipts. Fixes create new attempt paths and preserve old trajectories.

The stages are implementation review, static/unit/USD/URDF audits, native physics, robot-control prefixes, expert episode 1, expert episode 2, Dream, media rendering, visual verification, upload, exact remote commit verification and ready handoff. Native cases must all pass after two independent resets. Two distinct expert records must each score 1.0 within the action limit. Dream cannot start until their native traces, actions and all three observation streams are checked against the pinned Inspect format and the same source revision. A real Dream score of zero is retained truthfully.

Raw native probes explicitly distinguish controlled fixture initialization/force application from demonstrations. Expert and model episodes never teleport task objects, automatically attach parts or alter score state. Physics probes are not media evidence. Every task branch includes its own bootstrap, native runner, feedback expert, scorer, ledger, evidence validator and media exporter, so reviewers need no other branch.

## Media review and upload

The official exporter generates all camera videos; the task package uses the top-camera model run, successful demo and initial screenshot. Both expert videos are retained. Validation fully decodes H.264 yuv420p, matches frame counts to the action log, enforces 50 MB per video / 10 MB screenshot, checks nonblank samples and native initial camera coverage, and scans public text for identifying information. No overlays or identifying textures are added.

Pixel statistics cannot establish visual quality. The runner preserves rendered media and stops before upload until an actual agent/reviewer has inspected the setup, both demos, model video and contact sheets. This is review of finished results, not manual media generation. Locate and record that review with:

```bash
python coordination/review_media.py .robocurve-runs --task <slug>
# After actually inspecting the displayed directory and all listed checks:
python coordination/review_media.py .robocurve-runs --task <slug> --confirm-reviewed
bash coordination/bootstrap_and_run.sh --resume
```

The attestation is bound to exact media bytes and source SHA. There is no preapproved/placeholder review. The official uploader is called only after that gate and genuine validation. It operates on a disposable metadata copy, never on the evaluated checkout. Publication permits only `task.json`, `validation.json` and `source_manifest.json` metadata changes; executable code remains identical to the evaluated commit. A lease protects concurrent branch changes. The pushed commit is fetched back and checked.

## Reports, status and authorized submission

Read `.robocurve-runs/report.json` for every task, failure diagnostic and cost estimate. `ready-handoff.json` contains only fully verified tasks. Exit 0 means all requested runtime stages passed, or explicitly requested offline checks passed; offline success never means submission readiness. Exit 2 means requested tasks are incomplete, exit 3 means an environment/configuration blocker, and argparse uses exit 2 for invalid options. Dry-run exit 0 means only that a plan was printed.

The user authorized official submissions on 2026-11-11 and confirmed `aryansennthilkumarGT` as the registered submitting account for T-06. Submit each task after its complete evidence gates pass. Preview the verified subset with:

```bash
python coordination/submit_ready.py .robocurve-runs/ready-handoff.json
```

The authorized agent can then execute:

```bash
python coordination/submit_ready.py .robocurve-runs/ready-handoff.json --execute --registered-account aryansennthilkumarGT
```

The script checks every required immutable receipt and current remote SHA, refuses unfinished tasks, reuses an existing open/merged PR and stops on a closed prior PR for review. It supplies concrete titles and evidence-based bodies. The service-arm task has official PR #1647 at publication commit 93d23b21dd1a725c67f21ac039ab64bafe800b18 with media M-NRTVLQ; its evaluated simulation revision is 46bf1008e01546b266b5ba973d31e75e64bf8f89. Cell exchange has PR #1703 at publication commit 3c335ebd5c2bd006bd00d6a7bcfbc9ff4cd06ac8 with media M-3JA7DA; its evaluated simulation revision is 0b6f32b31578c508ed8ca6909f1f89079656bc31. Both official intake acknowledgments are confirmed. Preserve the existing PRs and do not change tasks waiting for review. Official acceptance remains unconfirmed.

## Engineering recovery

The current task revisions are the live checkpoint SHAs and their self-contained folders; manifest SHAs identify earlier coordinator runs. The manifest records the final service-arm publication SHA separately from its evaluated simulation SHA. Reuse its sealed completed evidence and existing official PR. For subsequent engineering runs, select the remaining task explicitly with the coordinator task selector. Do not rerun the historical draft generator: it would discard the later mechanism/controller changes. Preserve this handoff checkout and persistent run root. To recover, use the same manifest/stack/code and `--resume`. A new pipeline implementation hash invalidates stage reuse conservatively; keep the exact handoff revision used by a paid run unless deliberately investigating a defect.

Offline evidence includes numerical scorer counterexamples, measured-state controller unit tests, USD structure, warm-start IK, camera projection, nominal body paths, official convex YAM grasp/thread envelopes, and sampled table/inter-arm trajectories. It does not certify contact forces, flexible cable trajectories, actuator tracking, grasp robustness or successful full episodes. All five review criteria are recorded per task. The service-arm task has native physics, two full-score experts, a genuine Dream-1 score of 0.0, uploaded media and a clean-checkout reproduction. The cell-exchange task has also completed those gates and was received for review. The other six require completion of their recorded native/control/expert/model checks. Novelty is an internal mechanism comparison, not an external acceptance guarantee. The current board must be refreshed before submission.

Run coordinator tests with `python -m unittest discover -s coordination -p 'test_*.py' -v`. They include real temporary Git checkouts and subprocesses, intentional Task 3 failure, preservation/resume, changed-revision recovery, tamper rejection, native case coverage and media review binding. Test fixtures are explicitly not physics or Dream evidence.

## Reproduced offline verification

The final pinned packages passed the actual Bash `--all --offline` workflow from clean checkouts: 484 task tests passed, 32 were inapplicable, and all 35 coordinator tests passed. Eight composed-USD checks and 33 applicable geometry/kinematics audit programs passed; seven thread audits were inapplicable. A second invocation with `--resume` left the ledger byte-identical and created zero duplicate stages. Exact task revisions, artifact hashes and the tested coordinator code revision are recorded in [offline-run-verification.json](offline-run-verification.json). These checks ran under Python 3.12 and do not constitute native physics, expert, model or media validation.
