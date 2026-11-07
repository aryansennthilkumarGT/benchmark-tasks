# Fit and pin a hinged collar around a captive shaft

Open the hinged collar, fit it around the shaft between its fixed end stops, close both halves, and insert the orange-headed key through all three aligned lugs. Leave the collar retained with both hands clear.

Engineering implementation. `validation.json` records exact executed evidence. A checkout without the required native, expert, model and media records is not ready for an official PR. No unexecuted score is claimed.

## Independent reproduction

This folder is self-contained; it never imports another task or the handoff branch. In an authorized official Linux x86-64 YAM/Arena GPU environment, run from the repository root:

```bash
python3 tasks/hardware-order-kit/bootstrap_task.py --output /data/hardware-order-kit-evidence --budget-file /data/compute-budget.json --execute --model
```

Without `--execute`, this command previews only. Add `--resume` to reuse hash-verified outputs. The bootstrap uses the pinned official installer in the evidence directory, validates the official apple/bowl smoke trial, runs static checks, then native probes and two independent full-score expert episodes. `--model` adds genuine Dream-1 and media only after those succeed. It never uploads media or opens PRs. See the shared eight-task runner on the handoff branch for upload and submission gates.

If the exact pinned environment is already installed, use its Python directly:

```bash
python tasks/hardware-order-kit/static_check.py
python tasks/hardware-order-kit/task_runner.py --output /data/hardware-order-kit-trials --execute --model
```

Evidence must be outside this Git checkout, and the checkout must be clean. The same command without `--execute` is a dry run. `--retry-failed REASON` allows one documented retry of an unchanged failed stage; a code fix should produce a new commit. A failed task preserves previous evidence. Never reuse an expert video as model evidence.

## Environment and cost

`stack-lock.json` pins the official launchable, adapter, Arena release, Inspect Robots and Dream plugin commits. It uses Python 3.12, Isaac Sim 6.1.0.0, NumPy 2.3.1 and the official bimanual I2RT YAM station. The adapter's 14-D action is left six absolute joints + normalized jaw opening, then right six + opening. Physics is 240 Hz; control is 20 Hz; observations are the three official 320x176 RGB cameras and robot joints.

Use an RTX 4090/5090 or L40S ray-tracing GPU, >=16 GiB free VRAM, >=32 GB RAM with >=24 GiB available, and >=250 GiB free disk. Drivers are checked against the documented Linux recommendation 580.95.05; Isaac Sim 6.1 lists 595.58.03 as tested. The script does not modify drivers, system Python, VPN, SSH configuration or other jobs. Vendor EULA acceptance must already be configured by the authorized launchable/operator. `uv` and `git` must be present. Dream credentials stay in the official secure configuration.

The budget receipt describes actual provider facts: `hourly_usd`, `balance_usd`, `spent_before_start_usd`, `instance_started_unix`, `instance_id`, `gpu_uuid`, and `provider_evidence`. No price or credit is assumed. The launcher monitors instance wall time, including idle time, with a $170 charge cap and $30 reserve. Exiting a script does not stop provider billing. Evidence and raw observations are retained.

## Trials and scoring

Seed 0 and `object_jitter=0` are fixed for both expert repeats and the model. Maximum 6000 actions (300 simulated seconds). Real wall time is unmeasured and depends on physics/rendering/model latency. The scorer recomputes partial credit and requires 2 s of final stability and released-arm clearance. Read [SCORING.md](SCORING.md) for every numerical condition and [SETUP.md](SETUP.md) for every body, material, mass, dimension and pose.

Native probes: 5 physics cases and 3 real robot-control cases, each repeated after independent resets. Physics probes may initialize mechanism poses and apply forces for controlled measurements; those probes are explicitly excluded from demonstration/media evidence. Control probes use only robot actions. Two full expert episodes separately establish feasibility before model spending.

## Implementation and limits

Rigid faceted half-rings and a passive hinge model a service collar. Fixed end flanges prevent axial assembly; a free square key captures three interleaved lugs. Extended handles suit YAM jaws. The task tests assembly and retention, not certified clamping friction or torque transmission.

Read [CONTROLLER.md](CONTROLLER.md), [NOVELTY.md](NOVELTY.md), and `mechanics-review.json` for the feedback strategy, comparison review and five criteria. Rigid USD parse checks, synthetic scoring tests and ideal IK replay are offline evidence only. Native contacts, camera rendering, reliable reset and complete action execution require separate runtime evidence.

`build_assets.py` deterministically derives included `.usda` assets from `scene.json`; run it only when intentionally changing the scene, then update hashes and commit. `source_manifest.json` hashes LF-normalized source and asset bytes. `run.py` launches one official trial, `task_runner.py` preserves/gates native evidence, `validate_rollout.py` cross-checks logs/actions/frames/scorer replay, and `render_media.py` exports and fully decodes H.264 yuv420p media. A zero Dream score is valid evidence when the required successful demonstrations exist. Public media require visual inspection for framing, mechanical outcome and blind-review compliance before upload.
