# Cloud → existing Brev: start here

This transfer package is CPU-tested. It does not prove that Isaac, the controllers or credentials work on the stopped machine. **No Cloud access/start of Brev is authorized.** You will start your EXISTING instance only when ready and explicitly authorized. Never create a replacement.

Instance: `yam-eval-launchable-0cb74b`. New spending: **$15 maximum**. Conservative estimated shutdown trigger: **$13.50**, or six hours from the original actual instance start, whichever comes first. The scoped policy replaces the old$30 reserve only for this approved, dedicated session. Other receipts retain their legacy guards. No balance/rate/start time is guessed.

The target remains at least three genuinely qualified NEW PRs, then more if affordable. None of the three candidates currently has native full-score evidence; nailer additionally has an importance hold. A quota never permits weaker scoring, novelty or fabricated results. A failed Dream score is acceptable if the genuine required run and full-score expert evidence satisfy the official rules.

## 1. Understand the two computers

Your Windows laptop/PowerShell/WSL is the **local** computer. The commands in sections2–6 run in the **remote Brev Linux SSH terminal**, not in your laptop's WSL filesystem. Installing/authenticating Codex or GitHub on the laptop does not automatically install/authenticate them remotely.

Before paying for time, check your existing laptop `brev` CLI is available and keep a separate LOCAL terminal ready for:

```bash
brev stop yam-eval-launchable-0cb74b
```

Verify the actual stopped state in the Brev console afterwards. Do not mistake a detached TMUX session, killed Python process, disconnected SSH or guest shutdown for verified stopped provider billing. No automatic provider-level shutdown has been verified. **The application-side$15 cap cannot guarantee a$15 invoice if the instance stays running.** The$13.50 trigger leaves a margin; it is not an automatic billing stop.

## 2. One-command source transfer (REMOTE SSH)

The final Cloud answer gives the exact new recovery commit. Set `OPS_REF` to those40hex characters; do not substitute `main`, a task branch, or a moving branch head. A commit cannot literally embed its own SHA in a tracked manifest: the bootstrap verifies this supplied immutable Git commit, then records the resolved coordinator commit outside Git in handoff-state.json.

The remote machine needs `git`, `python3` and an already authenticated `gh` CLI with repository read access. Authenticate securely on that machine if necessary, never by pasting credentials into this README, Git or chat. No installer, driver change, Isaac reinstall, instance provisioning or provider connection is hidden in the bootstrap.

```bash
OPS_REF=PASTE_EXACT_RECOVERY_COMMIT_FROM_FINAL_CLOUD_ANSWER
BOOT=$(mktemp)
gh api -H 'Accept: application/vnd.github.raw+json' \
 "repos/aryansennthilkumarGT/benchmark-tasks/contents/coordination/brev_transfer/bootstrap.sh?ref=$OPS_REF" > "$BOOT" \
 && printf '%s  %s\n' 'ed011bb6b58e01aab445c36f644dd5304acb41861f1fc7f8f590d02f4ab33921' "$BOOT" | sha256sum --check --status \
 && bash "$BOOT" --ops-ref "$OPS_REF"
```

This verifies/creates ONLY:

- `/data/robocurve-ops`: independent, pinned coordinator repository.
- `/data/robocurve-task-cargo`: independent Cargo repository, exact4740eba2b60a17041798e690d307b37a120ebfc1.
- `/data/robocurve-sprint`: persistent transfer, provider observations and session evidence.

New checkouts use sparse Git files to avoid downloading unrelated task assets. Existing folders must already have the right origin, exact SHA and clean Git state; otherwise the bootstrap refuses to change them. It never deletes/resets `/data/benchmark-tasks`, old raw trajectories, credentials, other task evidence or TMUX sessions. A failed new clone may leave a clearly named transfer directory; no old folder is removed. Rerunning the same command validates identity and preserves the session UUID instead of resetting it.

Evidence for this approval lives in `/data/robocurve-sprint/sessions/<persisted-session-id>/`, leaving any older top-level sprint receipts untouched. The shell scripts and manifest use only the three requested top-level locations. No mutable source branch is treated as the execution pin.

## 3. FREE preflight (REMOTE; no CUDA or paid APIs)

```bash
bash /data/robocurve-ops/coordination/brev_transfer/preflight.sh --free
bash /data/robocurve-ops/coordination/brev_transfer/run_first_diagnostic.sh --dry-run
```

“FREE” means no simulation, GPU probe, paid model/API, provider start or upload. **A running Brev instance still bills for idle time during free checks.** These checks validate both Git identities/SHAs/clean state, task source hashes, source-bound offline/diagnostic inventory, writable outputs, TMUX, Codex CLI availability/authentication and registered GitHub login `aryansennthilkumarGT`. Codex login-status output is discarded; no secrets are printed. If an essential tool is missing, stop the instance rather than paying while rebuilding the host.

The bootstrap's own preview is also safe:

```bash
bash /data/robocurve-ops/coordination/brev_transfer/bootstrap.sh --ops-ref "$OPS_REF" --dry-run
```

## 4. Actual provider facts and GPU preflight (after YOU start the instance)

Use the provider console to obtain the real current balance, hourly rate, billing start and observation time. Use an ISO8601 timezone, e.g. `-05:00` or `+00:00`. Do not use “now” as a fictional billing start if the instance has already been running. The wizard accepts nonsecret provider facts, NOT tokens. Record a genuine console/screenshot/time reference; its format checks cannot independently authenticate that reference.

Get the real GPU UUID locally on Brev, then enter the observed facts:

```bash
nvidia-smi --query-gpu=uuid --format=csv,noheader
bash /data/robocurve-ops/coordination/brev_transfer/preflight.sh --record-provider-facts
bash /data/robocurve-ops/coordination/brev_transfer/preflight.sh --gpu
```

The first observation must be no older than five minutes. New observations are immutable files; refreshing cannot change instance, GPU, rate, original start or the approved cap. The policy is bound to this actual transfer's persistent UUID and dedicated receipt directory. Historical spending is not falsified: this approval accounts for NEW session spending. The initial approved observation establishes the original six-hour deadline, including transfer/startup/idle time. A verified continuation of this SAME scoped session may use its timestamped observation with rate-based charge estimates; it does not pretend to have re-queried a fresh provider balance. Refresh actual provider observations when available. A restart cannot reset the deadline or charges.

GPU preflight checks the expected existing L40S/565.57.01 profile, existing `/data/IsaacLab-Arena/yam.env`, its pinned Python3.12 and exact installed SDK sources/versions. It will not change the driver or reinstall packages. A read-only preflight is not a successful scored native smoke. **Native-only Cargo does not require Dream/upload authentication.** `--gpu --stage qualification` and the full coordinator retain the required Dream/upload gates before those services run; credential presence is not falsely called API authentication.

If any essential check fails, it prints `PREFLIGHT BLOCKED`. Read the precise reason. Do not repeatedly run expensive commands or “fix” a pin by substituting an unrelated branch. Stop billing from the laptop while resolving a host prerequisite that cannot be repaired quickly within the budget.

## 5. Launch Codex CLI inside remote TMUX

After the free preflight and provider record are valid:

```bash
tmux new-session -A -s robocurve-sprint -c /data/robocurve-ops \
 'bash /data/robocurve-ops/coordination/brev_transfer/codex_session.sh'
```

`-A` attaches if that named session exists; it does not destroy any other session or start a second Codex in it. Detach with Ctrl+B then D; reattach with `tmux attach-session -t robocurve-sprint`. Detaching DOES NOT stop charges.

The launcher uses the remote Codex binary authenticated by preflight. It keeps normal workspace sandboxing, enables network for the authorized GitHub/model workflow, and adds only the Cargo checkout and sprint outputs as writable directories. Runtime caches are directed into sprint outputs. It does not disable approval safeguards. If the actual native runtime needs a real sandbox exception, inspect the specific failure and request only the necessary access; do not blanket-disable sandboxing or reinstall the GPU stack.

The initial Codex prompt loads this document and GPU_RESUME_PLAN.md. The agent should remain active: inspect genuine Isaac traces, perform at most two supported repair approaches per blocker, verify changed source, switch to ER when unproductive, and preserve every exact-source result. Use separate independent task source checkouts under sprint outputs for later candidates. Keep the coordinator checkout unchanged during source-bound runs. Do not edit pending1733 or finally rejected1647/1703/1772 heads.

## 6. First bounded native action

Inside the remote Codex/TMUX workflow, execute exactly:

```bash
bash /data/robocurve-ops/coordination/brev_transfer/run_first_diagnostic.sh --execute
```

This performs the real preflight then ONLY Cargo's `retract_controlled_inner_tube` native case, twice after reset, with SDK telemetry, original960Hz physics, fail-fast and a20minute maximum. Spend/deadline limits may stop it earlier. No automatic Dream, media, upload or PR runs after a failure. A passing prefix is not full task qualification or a full-score expert demo.

Completed, failed or interrupted existing diagnostic receipts block automatic repetition. Do not delete them. After a supported source repair, the agent uses the general sprint entry point with the exact NEW commit and SAME session root/receipt, documenting the diff and blocker. The baseline first-diagnostic wrapper intentionally does not silently change its pinned source.

Find the durable run directory without guessing:

```bash
SESSION_ROOT=$(python3 /data/robocurve-ops/coordination/brev_transfer/transfer.py session-path)
```

For actual qualified candidate manifests, the same coordinator can subsequently use `marathon.py --execute --resume --submit` with `--run-root "$SESSION_ROOT"`. Follow GPU_RESUME_PLAN.md; never relabel diagnostic-only evidence as qualification. Preserve full experts/model/media/visual-review/PR provenance. A real model score0 alone does not block a compliant submission. Submit each genuinely qualified task immediately and continue, aiming for three new PRs and more only while affordable.

## 7. Stop the actual provider instance

At the$13.50 estimated trigger, six-hour limit, unaffordable work or exhausted productive candidates, stop workloads and run in the separate LOCAL laptop/WSL terminal:

```bash
brev stop yam-eval-launchable-0cb74b
```

Then verify the existing instance is actually stopped in the Brev console and record that observed state. No code here claims automatic provider-level shutdown or guarantees a final invoice if the instance is left running.
