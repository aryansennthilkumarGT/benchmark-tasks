> Archived final rejection: this package is not submission-ready. See [REVIEW_REMEDIATION.md](REVIEW_REMEDIATION.md). Do not reopen its closed PR.

# Replace opposed-polarity cells under a spring-return service cover

Open the sliding cover. Put both grey used cells in the grey collection tray. Install the two blue replacements with each orange positive end at its orange terminal, then close the cover.

Engineering implementation. `validation.json` records exact executed evidence. A checkout without the required native, expert, model and media records is not ready for an official PR. No unexecuted score is claimed.

## Independent reproduction

Use the installed Python environment for the pinned YAM Launchable in `stack-lock.json`. From a clean repository checkout:

```bash
python tasks/remote-battery-service/static_check.py
python tasks/remote-battery-service/task_runner.py --output /data/remote-battery-service-trials --execute --model
```

The self-contained task runner performs two reset repetitions of every native physics and control case, two independent expert episodes, Dream-1 evaluation, and media export. Securely configure the official Dream-1 plugin credentials first. `--resume` reuses hash-verified completed stages. Without `--execute`, the command previews its stages. Keep evidence outside the checkout. The ledger rejects failed or incomplete demonstrations.

For one expert trial and independent rescoring of its recorded trajectory:

```bash
revision=$(git rev-parse HEAD)
python tasks/remote-battery-service/run.py --mode expert --execute --commit "$revision" --output /data/remote-expert
python tasks/remote-battery-service/validate_rollout.py --directory /data/remote-expert --mode expert --limit 6000 --commit "$revision" --folder tasks/remote-battery-service
```

Expert actions are robot joint/gripper targets. Diagnostic mechanism initialization is excluded from demonstrations. Uploads and PR creation are separate operations.

## Environment and cost

`stack-lock.json` pins the official launchable, adapter, Arena release, Inspect Robots and Dream plugin commits. It uses Python 3.12, Isaac Sim 6.1.0.0, NumPy 2.3.1 and the official bimanual I2RT YAM station. The adapter's 14-D action is left six absolute joints + normalized jaw opening, then right six + opening. Physics is 240 Hz; control is 20 Hz; observations are the three official 320x176 RGB cameras and robot joints.

Use an RTX 4090/5090 or L40S ray-tracing GPU, >=16 GiB free VRAM, >=32 GB RAM with >=24 GiB available, and >=250 GiB free disk. Drivers are compared with the documented Linux recommendation 580.95.05. The fixed L40S profile on 565.57.01 uses the verified installed Launchable with `--launchable-root /data`. The bootstrap records the GPU and driver, verifies active package sources and pinned versions, and requires the scored official station smoke before task execution. The script does not modify drivers, system Python, VPN, SSH configuration or other jobs. Vendor EULA acceptance must already be configured by the authorized launchable/operator. `uv` and `git` must be present. Dream credentials stay in the official secure configuration.

The budget receipt describes actual provider facts: `hourly_usd`, `balance_usd`, `spent_before_start_usd`, `instance_started_unix`, `instance_id`, `gpu_uuid`, and `provider_evidence`. When the balance is observed after instance startup, `balance_observed_unix` records the snapshot time for reserve calculations. No price or credit is assumed. The launcher monitors instance wall time, including idle time, with a $170 charge cap and $30 reserve. Exiting a script does not stop provider billing. Evidence and raw observations are retained.

## Trials and scoring

Seed 0 and `object_jitter=0` are fixed for both expert repeats and the model. Maximum 6000 actions (300 simulated seconds). Two independently validated expert trials each used 5261 actions (263.05 simulated seconds). The second took 2701.78 wall-clock seconds on the documented L40S environment while other diagnostics shared the GPU. Runtime depends on concurrency, rendering and model latency. The scorer recomputes partial credit and requires 1 s of final stability and released-arm clearance. Read [SCORING.md](SCORING.md) for every numerical condition and [SETUP.md](SETUP.md) for every body, material, mass, dimension and pose.

Native probes: 8 physics cases and 2 real robot-control cases, each repeated after independent resets. Physics probes may initialize mechanism poses and apply forces for controlled measurements; those probes are explicitly excluded from demonstration/media evidence. Control probes use only robot actions. Two full expert episodes separately establish feasibility before model spending.

## Implementation and limits

Rigid cells, polarity markers and passive spring-contact shoes approximate terminals. A 2.5 N/m spring returns the sliding service cover, with an extended handle for YAM. The fixture models handling, identity and geometric contact readiness; it does not simulate voltage, chemistry or a commercial remote.

Read [CONTROLLER.md](CONTROLLER.md), [NOVELTY.md](NOVELTY.md), and `mechanics-review.json` for the feedback strategy, comparison review and five criteria. Rigid USD parse checks, synthetic scoring tests and ideal IK replay are offline evidence only. Native contacts, camera rendering, reliable reset and complete action execution require separate runtime evidence.

`build_assets.py` deterministically derives included `.usda` assets from `scene.json`; run it only when intentionally changing the scene, then update hashes and commit. `source_manifest.json` hashes LF-normalized source and asset bytes. `run.py` launches one official trial, `task_runner.py` preserves/gates native evidence, `validate_rollout.py` cross-checks logs/actions/frames/scorer replay, and `render_media.py` exports and fully decodes H.264 yuv420p media. A zero Dream score is valid evidence when the required successful demonstrations exist. Public media require visual inspection for framing, mechanical outcome and blind-review compliance before upload.

Interchangeable parts are matched one-to-one to valid slots. The body names in slot predicates are templates: any listed candidate may satisfy that slot, and dependent closure/preload goals reuse the same matching. Polarity and contact-spring compression remain mandatory. A single cell cannot earn two slot credits. The expert uses one convenient assignment, which is not required by scoring.

The 300-second limit accommodates the verified 263.05-second complete procedure, including both old-cell collections, polarity-correct installation, cover closure and released stability.

Dream-1 (`dreamlabs/dream-1-beta`) completed 6000 actions over 300 simulated seconds and scored 0.0, with 125 recorded model requests and dry-run disabled. Recorded trial wall time was 3637.94 seconds. Session-expiration retries recovered within the same genuine simulator episode. Both full-score experts used 5261 actions over 263.05 simulated seconds. Uploaded model, demo and initial setup media are linked by the ID in `task.json`. An independent clean HTTPS checkout of the evaluated revision also passed the full expert episode: 1.0, 5261 actions, 263.05 simulated seconds (3467.69 wall-clock seconds). Publication changes only documentation and recorded metadata; executable sources, assets, scene and controller remain byte-identical to that evaluated revision.
