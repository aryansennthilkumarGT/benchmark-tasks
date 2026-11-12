# Exchange two internal modules and close out an enclosure

Remove the grey storage sled and cooling module, collect them in the tray, seat the marked replacement storage and keyed cooler, then close the lid. Storage rails pass beneath the cooler; the lid must be physically supported to service the internal modules. This models mechanical service access and retention, without electrical or thermal operation.

## Reproduction

Use the official bimanual YAM Launchable and the pinned dependencies in `stack-lock.json` (Python3.12, Isaac Sim6.1.0.0,240Hz physics,20Hz control). The tested installed L40S profile uses driver565.57.01. Do not modify the host driver. Seed0 and object_jitter0 reproduce the fixed layout in `SETUP.md` and the setup screenshot.

From a clean repository checkout, using the installed environment Python:

```bash
python tasks/node-service-closeout/static_check.py
python tasks/node-service-closeout/run.py --mode expert --execute --commit "$(git rev-parse HEAD)" --output /data/node-expert
python tasks/node-service-closeout/validate_rollout.py --directory /data/node-expert --mode expert --limit 7200 --commit "$(git rev-parse HEAD)" --folder tasks/node-service-closeout
```

The model gets7200 control actions,360 simulated seconds. The current revision's first measured full-score expert took218.9 simulated seconds and1190.3 wall seconds; wall time depends on rendering, contention and model latency. Independent reset repetitions and model results must be verified in `validation.json` before publication. This preparation copy is not submission-ready while those records remain incomplete.

`run.py --mode dream` uses the configured official Dream-1 credentials and requires genuine native feasibility evidence via `--evidence`; credentials must stay outside this repository. `task_runner.py` and `bootstrap_task.py` retain a separate strict provider-budget path. Their historical default caps are configurable runner policy, not a claim about another operator's account balance. No script exit stops instance billing.

## Objective and evidence

Read `SCORING.md` for every numeric predicate, weights, invalid outcomes, clearance and stability requirements. `scene.json` contains all authored shapes, transforms, masses, joints and predicates; `build_assets.py` deterministically generates the included USD. Raw native traces must replay through the unchanged scorer; offline synthetic tests are not physics evidence.

Mechanism probes exercise genuine contacts and independent resets. Default-reset controller assertions may be checked against post-action phase-completion frames in two independently completed full-score expert trials; that method reuses actual expert traces and does not claim extra standalone native runs. Initialized suffix diagnostics receive no demonstration credit. A fresh HTTPS checkout must independently reproduce a complete expert before submission.

The scripted expert submits14-dimensional absolute robot-joint and jaw commands. It reads measured body/joint state, verifies grasps and alignment, and changes object state through physical robot contacts. No object teleportation or scripted scoring updates are used during demonstrations. The official camera observations are320x176 RGB from three cameras.

## Limits and provenance

Rigid guide rails, keyed cooler feet and a gravity lid approximate mechanical service. Fins do not simulate cooling; storage has no data connection. Enlarged grasp handles belong to the submitted bench fixture. Materials, friction and masses are approximate rigid surrogates, not calibrated hardware. Original primitive task geometry is described in `PROVENANCE.md`; robot/station assets remain vendor dependencies. All visual evidence must come from actual recorded observations and pass blind-review inspection before upload.
