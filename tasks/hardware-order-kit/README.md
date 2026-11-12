# Fit and pin a hinged collar around a captive shaft

Open the hinged collar, carry it beneath a shaft with fixed end flanges, fit and register both halves around the shaft, close the seam, and pass the loose key through three interleaved lugs. Withdraw both hands while the keyed collar remains retained.

## Reproduction

Use the official bimanual YAM Launchable with the versions in stack-lock.json. The evaluated environment is Python3.12, Isaac Sim6.1.0.0, L40S with fixed driver565.57.01. Physics uses480Hz and robot actions20Hz. This task uses the installed vendor stack; do not change the host driver.

From a clean checkout with the installed environment Python:

```bash
python tasks/hardware-order-kit/static_check.py
python tasks/hardware-order-kit/run.py --mode expert --execute --commit "$(git rev-parse HEAD)" --output /data/collar-expert
python tasks/hardware-order-kit/validate_rollout.py --directory /data/collar-expert --mode expert --limit 6000 --commit "$(git rev-parse HEAD)" --folder tasks/hardware-order-kit
```

The limit is6000 actions,300 simulated seconds. Runtime remains unmeasured until a complete expert is verified. Fixed seed0, object_jitter0 and the exact layout in SETUP.md reproduce the scene. This preparation copy is not submission-ready: complete physics, two genuine experts, Dream-1, media and fresh HTTPS reproduction are still required. Never interpret incomplete evidence as passing.

`run.py --mode dream` uses securely configured official credentials and requires real feasibility evidence via `--evidence`. The bootstrap/task runner retain their separate strict provider-budget path; historical default reserve/caps are configurable policy and not a claim about another account balance. Exiting a workload does not stop instance billing.

## Scoring and evidence

SCORING.md and scene.json define every numeric predicate, partial weight, invalid outcome, clearance and stability condition. Parts that are displaced lose credit. Full success requires physically retained assembly and both hands clear. Native force/contact tests are separate from complete cold-reset robot demonstrations; initialized diagnostics receive no demonstration credit.

Default-reset control assertions can be recomputed from actual post-action phase-completion frames in two independent complete full-score expert traces. That method explicitly reuses existing traces and claims no additional standalone control runs. Actual mechanism probes and a fresh HTTPS full expert remain separate requirements. Model and expert videos must use the official observation exporter, with complete H.264 frame decoding and direct visual review before upload.

## Mechanism limits

Rigid faceted half-rings, a passive hinge, shaft rib and loose square key approximate mechanical assembly and retention. Handles are enlarged fixture features. Intended steel/aluminium surrogates use specified masses and uncalibrated contact coefficients. Tests of keyed opening retention do not establish certified clamping friction or whole-collar shaft-torque transmission. See SETUP.md, CONTROLLER.md, NOVELTY.md and PROVENANCE.md for geometry, controls, comparisons and dependencies.
