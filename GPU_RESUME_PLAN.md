> Budget amended by the user: $12 TOTAL for the SAME already-started sprint, $11 operational shutdown trigger, original six-hour/start/charge history preserved. Reported rate$1.79/hour and credits$13 require fresh verification; do not assume they are current. Existing bd3c404 transfer updates only through explicit --refresh-from. Cloud must not access Brev. See coordination/brev_transfer/START_HERE.md (repository-root path).

# Single continuous GPU engineering and submission sprint

Current authorization: **Cloud must not access/start Brev or incur charges**. The user approved a maximum$12 NEW spending for the forthcoming session and a conservative$11 estimated-spend shutdown trigger, with six hours maximum; actual startup/provider facts remain unverified. Use [the tested Cloud-to-Brev transfer package](coordination/brev_transfer/START_HERE.md) on the existing machine after the user starts it. This supersedes prior diagnostic-only stopping instructions and the old requirement to have three offline-ready candidates before beginning. Preserve pending1733 and finally rejected1647/1703/1772 heads.

Objective: at least three genuinely qualified NEW official PRs, then continue if qualified work and approved resources remain. Three diagnostics, tests or evaluations do not count. Three is not a promise that currently unproven candidates will work or meet the rubric; no weakened importance/novelty/scoring gate is permitted to reach a quota.

The active assistant carries out one continuous session. A command returning an incomplete stage transfers control to the same assistant for actual trace inspection, targeted repairs, real visual review or candidate switching. It is not a reason to end the turn or ask whether to continue. A successful diagnostic, repair, evaluation, report, commit or submission is not a stopping milestone. Once actual start/spend approval covers this sprint, do not ask for another routine approval between its authorized stages.

## Start and billing control

Before startup, verify actual Brev credits, quoted GPU rate, approved spending limit and a working provider control path for stopping the existing instance. Do not provision replacements. If available, configure provider-native auto-stop at the approved deadline and verify it; a guest shutdown or killed Python process is not proof of stopped billing. After startup immediately verify actual GPU UUID/driver, pinned installed runtime, secure credential availability/authentication and registered GitHub account. Never print/store token values. A credential-presence flag alone is not proof that a service will authenticate; use an actual supported nonpaid identity/health check where available.

The cost receipt must contain observed provider evidence, actual instance billing start, current balance/rate, GPU UUID, `authorized_session_spend_usd` and `authorization_reference` to the real user approval. No value is assumed from the historical$29.60. `record_budget.py` records facts, never launches compute. Its format checks do not authenticate a provider. For this exact approval, `brev_policy.py` binds the$12 hard cap/$11 trigger to the named instance, uploaded authorization hash, dedicated transfer session UUID and receipt directory. Its reserve is0 for this approved NEW-session scope; other receipts keep the historical$170/$30 guards. Fresh balance/rate/start facts are never filled from guesses. Old observations and session history remain intact.

`open_sprint` creates sprint-session.json before the first diagnostic and fixes the six-hour outer deadline to the actual instance start. Resumes preserve deadline, instance/rate/spending identity, provider observations, repairs and submissions. Fresh provider receipts on resume cannot reset elapsed charges or increase the cap. A verified continuation of the same scoped session can retain the original timestamped observation while estimating elapsed charges, without falsely claiming a fresh provider query. The meter uses actual observed rate/balance plus conservative elapsed-instance charges, including idle/startup/review time; it is not a live billing API. Workload checks retain one minute of rate-based shutdown headroom and stop one minute before the outer session deadline. This margin is not a claim that provider shutdown is automatic or always completes within that time. Refresh provider observations between candidates and after costly failures. The active assistant must stop paid work AND stop the actual Brev instance before the approved cap/deadline, then verify provider state. If shutdown cannot be confirmed, report that precise fact; do not claim billing stopped.

## Continuous execution

1. Run the bounded cargo diagnostic from the exact current [handoff](coordination/recovery/GPU_DIAGNOSTIC_HANDOFF.md), using the SAME session root and a budgeted command. Current cargo source4740eba remains frozen; no native success is claimed.
2. On failure preserve full native/SDK/process traces. Inspect the actual failure, implement a substantive targeted source change, rerun affected offline checks and publish its exact independent task source. Record the precise blocker, old/new commits, diff hash and reason using sprint_state.py. Maximum two substantial repairs per blocker; unchanged failed inputs are not automatically retried. Switch to ER or another already defensible candidate when unproductive. Do not spend on nailer acceptance qualification while its importance hold remains unresolved.
3. When a candidate meets the per-task source/quality conditions, run its full native mechanism/control checks, real expert demonstrations, genuine Dream evaluation, media rendering and actual visual review. Only genuine expert full score and complete model evidence unlock submission. A genuine Dream score0 is valid evidence, not an automatic rejection. Prefixes are not demonstrations.
4. Submit that individual compliant task immediately when all evidence is valid; do not wait for a batch. Record its URL, publication/evaluated commits, receipt chain and actual official PR read-back. Preserve a created URL even if an API read-back fails; resolve read-back without rerunning evaluations or creating a duplicate PR.
5. Proceed immediately to the next viable candidate. Continue after the third new verified PR if authorized resources and productive work remain. If media awaits visual inspection, the assistant inspects the actual files and resumes verified stages; no invented attestation or new permission prompt. Preserve exact-source passed work to avoid repeating expensive stages.
6. Stop paid work only for an actual authorization/cost/deadline limit, exhausted productive/affordable work, or a material operational blocker; stop provider billing as described above. Do not buy credits, exceed the approved cap or fabricate a third qualifying task.

## Tested commands and checkpoints

Pure preview (no GPU, provider, credential probe or PR):

```bash
python coordination/marathon.py --manifest coordination/recovery/diagnostic-sources.json --run-root /data/robocurve-sprint
```

First diagnostic, ONLY on the existing machine after user startup and factual preflight. Sources are independent `/data/robocurve-ops` and `/data/robocurve-task-cargo`; `/data/benchmark-tasks` is never modified:

```bash
bash /data/robocurve-ops/coordination/brev_transfer/preflight.sh --free
bash /data/robocurve-ops/coordination/brev_transfer/preflight.sh --record-provider-facts
bash /data/robocurve-ops/coordination/brev_transfer/preflight.sh --gpu
bash /data/robocurve-ops/coordination/brev_transfer/run_first_diagnostic.sh --execute
```

This uses ordinary native robot controls and20Hz SDK telemetry at the original960Hz physics. It is fail-fast, budget/deadline bounded and receipt/checkpoint protected. Isaac instrumentation itself remains unrun. Do not run both this and the older equivalent direct diagnostic unnecessarily. A passing diagnostic does not itself qualify a full task. Failed output remains immutable.

As actual quality/source evidence becomes available, maintain an exact manifest naming reviewed bundles and qualified candidates. Start qualification with ONE qualified candidate; no three-candidate startup gate remains:

```bash
SESSION_ROOT=$(python3 /data/robocurve-ops/coordination/brev_transfer/transfer.py session-path)
BUDGET_FILE=$(python3 -c 'import json; print(json.load(open("/data/robocurve-sprint/active-provider-receipt.json"))["receipt"])')
/data/IsaacLab-Arena/.venv/bin/python /data/robocurve-ops/coordination/marathon.py \
 --manifest "$SESSION_ROOT/qualified-manifest.json" --run-root "$SESSION_ROOT" \
 --budget-file "$BUDGET_FILE" --launchable-root /data \
 --registered-account aryansennthilkumarGT --execute --resume --submit
```

The current diagnostic-sources.json is not a qualification manifest and must not be relabeled to bypass known failures. Each per-task gate remains. `--submit` now submits inside the task loop, before the next candidate. Do not first run a separate complete task_runner and then run this entire coordinator: that repeats expensive evaluations because receipt contexts differ.

Durable records: sprint-session.json (cap/deadline/provider observations/repair attempts/new PR count), ledger.json (immutable source-bound stage outcomes), submissions/<slug>.json (per-task creation/read-back), report.json and ready-handoff.json. After a source repair, update only the relevant task manifest entry and resume in the same session. The assistant owns the outer engineering loop; no Python script can invent a correct controller repair or genuine visual inspection.

Provider billing stop, from the separate LOCAL laptop/WSL terminal: `brev stop yam-eval-launchable-0cb74b`. Verify actual stopped state afterwards. No verified automatic provider shutdown is claimed. A$12 application-side cap cannot guarantee a$12 invoice if the instance stays running.
