# Brev execution checkpoint · 2026-11-10

Submission-ready tasks **0 of 8**. All eight original draft branch heads were checked against the fork and matched [the manifest](draft-manifest.json). The original handoff head was `a7d41476752b8ae0d265cc38f93b9ad5b3656f0a`. The all-task dry run and 35 coordinator tests passed. No candidate simulator run, model request, official upload, or PR was initiated.

## Official station evidence

The launchable completed startup and had already executed a real scripted station trial. Its saved Inspect Robots log `~/yam-eval/adhoc_4e02b1b3.json` reports `yam_arena`, `yam_scripted`, seed 0 (derived episode reset seed 1415158438), 20 Hz, instruction “put apple into the bowl”, `success_at_end=1.0`, 202 steps, and zero errored trials. The log SHA-256 is `aaf37ee2078810f347edb2929546b9e88f13cd3bb47f20a906d1f8235f511c14`. The launchable did not populate the log's environment revision. The native actions, records, and frame arrays are under `~/yam-eval` in run `20261110_224229_6a80b4bd`.

Rendered all three streams from the existing recording into `.robocurve-runs/station-startup-review/` on the workstation. FFmpeg decoded all three with errors treated as fatal. Each render contains 203 frames at 20 fps. The reviewed overhead frame at 9.5 seconds shows the apple in the bowl. This is launchable startup evidence. The exact pinned repeat smoke and contact/action audit are pending.

## Runtime and budget

Authenticated Brev CLI identified `yam-eval-launchable-0cb74b` as RUNNING, provider instance ID `rj306hdgr`, matching hostname `brev-rj306hdgr`. Outside the command sandbox the L40S reported 46068 MiB, UUID `GPU-c25d3cbd-c502-f9e8-6e13-f15c37495a44`, and driver `565.57.01`. The sandbox lacks the NVIDIA device nodes. The driver is below the coordinator's `580.95.05` gate. No driver changes were made. Available disk on /data was 271846203392 bytes (253.18 GiB) and memory available was approximately 141 GiB. The checkout's default run root is on the smaller root filesystem, so use a persistent run root under /data.

The existing environment registers `yam_arena`, `yam_scripted`, and `dream`. Isaac Sim 6.1.0.0, Inspect Robots 1.0.0, YAM 0.38.0, NumPy 2.3.1, and the Arena, adapter, Inspect Robots, and launchable checkout commits match the lock. The separate /data/IsaacLab checkout is `37ddf626871758333d6ed89cf64ad702aef127d0` versus the lock's `91a0906f93802eb859192dcb0bca879f891e92d6`. Inspect the Arena venv's active Isaac Lab package source before concluding which checkout its simulator imports. Dream distribution metadata was 0.1.0. The Dream credential, RoboCurve upload token, and Dream service quota were unverified.

The authenticated Brev list response exposed instance identity and status but no billing balance, prior spend, actual rate, or billing start timestamp. A live billing receipt could not be issued. The current reserve and overall spend headroom are therefore unknown. GitHub authentication succeeded outside the sandbox.

## Public novelty refresh

The official repository tree yielded 18 task packages and the GitHub API returned 1,426 open PR titles at collection time. The board redirected to sign-in. The [previous primary benchmark catalog review](literature-screen.json) covers DataCenterBench, RoboDojo, LIBERO, RoboCasa, SimplerEnv, and BEHAVIOR. The following candidates still require a signed-in board check and native validation of the stated mechanism.

| Draft | Closest observed overlap and disposition |
| --- | --- |
| hinged-chassis-drive | [Server chassis rail insertion #1546](https://github.com/robocurve/benchmark-tasks/pull/1546) and upstream access panel closeout. Review rail insertion in detail. Retain provisionally if gravity-loaded lid support and bar capture both constrain success. |
| remote-battery-service | [Smoke alarm battery replacement #1165](https://github.com/robocurve/benchmark-tasks/pull/1165) and [spot welder polarity and lid #615](https://github.com/robocurve/benchmark-tasks/pull/615). High overlap. Prove continuous spring-cover support and opposing polarity contacts distinguish the manipulation. |
| switch-map-rework | [Patch cords per the port-map card #136](https://github.com/robocurve/benchmark-tasks/pull/136) and DataCenterBench connector handling. Hold until native evidence demonstrates occupied-port rework with physical latch release, temporary parking, and an undisturbed working link. |
| node-service-closeout | [Server drive remapping #422](https://github.com/robocurve/benchmark-tasks/pull/422) and the hinged-chassis draft. Preserve provisionally only if the cooling shroud physically blocks storage removal and closure retains a mechanically distinct module. |
| twelve-cell-pack | [18650 pack jig #1303](https://github.com/robocurve/benchmark-tasks/pull/1303) and [UPS battery string #688](https://github.com/robocurve/benchmark-tasks/pull/688). Preserve provisionally if one plate transfers the independent spring loads to the key and stays seated after release. Cell count provides duration. |
| eight-nut-bracket | [RoboDojo Fasten Screws](https://robodojo-benchmark.com/doc/sim-tasks/fasten-screws/) and [confined-access ratchet fastening #890](https://github.com/robocurve/benchmark-tasks/pull/890). Preserve provisionally if the existing thread geometry sustains pitch-coupled travel and nuts retain common plate preload after release. |
| fault-module-repair | Upstream balance centrifuge and [indexed arm lock #236](https://github.com/robocurve/benchmark-tasks/pull/236). The free pivot and pin-locked sliding mass are a plausible distinction. This is the first candidate to prioritize once prerequisites pass. |
| hardware-order-kit | [Split spacer around a captive shaft #941](https://github.com/robocurve/benchmark-tasks/pull/941) and [clamp-on lockout #708](https://github.com/robocurve/benchmark-tasks/pull/708). Hold for a direct implementation comparison. Redesign if the hinge and cross-pin leave materially the same access and retention challenge. |

## Resume

1. On a supported Brev runtime, authenticate to the organization billing view and capture the current balance, accrued charges, running interval, and actual instance rate. Record the provider evidence with `python coordination/record_budget.py --help`. Verify at least $30 reserve and headroom below the $170 overall ceiling before starting evaluation.
2. Retrieve the signed-in board and resolve the overlap holds. Securely configure Dream credentials with verified usage limits and the RoboCurve uploader environment. Keep secrets out of the repository.
3. Reuse the installed Arena stack. Verify the venv's actual Isaac Lab and Dream sources, driver support, and /data space, then use the coordinator's official smoke configuration. Preserve the existing startup artifacts and keep the repeat smoke in a new run directory.
4. Run `ROBOCURVE_RUN_ROOT=/data/robocurve-runs ROBOCURVE_BUDGET_FILE=/data/robocurve-budget.json bash coordination/bootstrap_and_run.sh --preflight`. After correcting any failed prerequisites and validating reuse of the installed environment, run `ROBOCURVE_RUN_ROOT=/data/robocurve-runs ROBOCURVE_BUDGET_FILE=/data/robocurve-budget.json bash coordination/bootstrap_and_run.sh --task fault-module-repair --resume`. Verify the official smoke precedes the candidate and use the ledger for native and model evidence. Publish each evaluated branch independently and leave official PR submission to the registered teammate.
