# Fasten a spring-loaded access plate while maintaining its preload

Compress and level a spring-loaded access plate, thread three noncollinear nuts down its studs, hand support between the robot arms as needed, then release both hands while the fasteners retain the plate's spring load and level attitude.

The target centre of the flat plate is14mm above the tabletop, within1mm and0.035radians of level. No visual height-marker texture is claimed.

## Reproduction

Use the official bimanual YAM Launchable and stack-lock.json dependencies. The tested stack is Python3.12, Isaac Sim6.1.0.0, L40S with fixed driver565.57.01. Physics runs240Hz, robot control20Hz. Use the installed vendor stack and retain its host driver.

```bash
python tasks/eight-nut-bracket/static_check.py
python tasks/eight-nut-bracket/run.py --mode expert --execute --commit "$(git rev-parse HEAD)" --output /data/plate-expert
python tasks/eight-nut-bracket/validate_rollout.py --directory /data/plate-expert --mode expert --limit 18000 --commit "$(git rev-parse HEAD)" --folder tasks/eight-nut-bracket
```

Run from a clean checkout using the installed environment Python. Fixed seed0 and object_jitter0 reproduce SETUP.md. The action limit is18000,900 simulated seconds. Two whole cold fixed-action expert episodes scored1.0 in12961 actions each (648.05 simulated seconds), including a fresh HTTPS checkout. Native contact tests passed12/12 on GPU PhysX and independently12/12 on CPU PhysX. A genuine Dream-1 evaluation completed18000 actions and scored0.0. Its full record and three camera streams were revalidated; actual H.264 model and expert media were exported and visually inspected. The task remains a prototype: importance and real-equipment procedure grounding are unresolved, so no official upload or PR has been made.

`run.py --mode dream` uses securely configured official credentials and actual feasibility evidence via `--evidence`. The bootstrap/task runner retain their separate strict provider-budget path; their historical default policy is not an account-balance claim. Workload exit does not stop instance billing.

## Objective and validation

SCORING.md and scene.json define all numeric predicates and partial credit. Full score requires each fastener's measured thread advance, correct plate pose/preload/tilt, stillness and released-arm clearance over the stated stability interval. Missing or invalid physical evidence is not a passing result.

Mechanism probes exercise actual contacts and spring-load response separately from demonstrations. Default-reset control assertions may reuse post-action phase-completion frames from two independently completed full-score experts; that method claims two expert resets and no extra standalone control runs. Initialized suffix diagnostics receive no demonstration credit. All final videos must derive from genuine official camera observations and undergo full H.264 decoding plus direct visual review.

## Physical limits

Faceted thread contacts, a400N/m preload spring and two passive plate-tilt axes approximate mechanical fastening. Two tiny noncolliding inertia links encode the plate guide coordinates and are not manipulated objects. Steel/aluminium materials and contact coefficients are uncalibrated surrogates. Certified tightening torque, thread wear and elastic deformation are not modeled. All three retention points have been designed around the loaded plate; no claim that three is mechanically minimal is made without separate one/two-fastener counterfactual tests.


## Executed expert and native CPU profile

The expert reads robot proprioception and its action index and emits an offline-authored14D joint/jaw program. It does not read task object poses, mechanism joints, evaluator state or score. The official SDK clamp and delta-limit safety guards remain enabled; the latter limits normalized jaw changes to0.05 per control. The two genuine expert records exactly match the authored program after those recorded official guards, including177 guarded jaw steps. No actions or recordings were rewritten.

The full-score expert episodes used GPU PhysX at sourcec62808268782ede6a38f70eb3697aeea4336e135. The separately verified native CPU PhysX profile uses `cpu_launcher.py`, which accepts the same arguments as `run.py` and explicitly appends `-E device=cpu` to the actual SDK command. Physics runs on CPU while the L40S renders the three real RTX RGB views. No host driver or installed vendor file is modified. Geometry, masses, friction,240Hz physics,20Hz control, solver settings and scoring remain unchanged. The genuine model source isec5da4fbdc9376fbf77e44fbd50f884346792792, score0.0 over18000 actions. GPU dynamics are not claimed for CPU trials.

The development feedback controller is retained for engineering inspection and is not imported by the fixed-action expert. Authored checkpoints identify program indices, not measured completion. Fixture initialization and force probes are mechanism diagnostics and do not count as demonstrations.


The original validator rejected a missing generic `policy_config.model` field. The finalized SDK record instead names the checkpoint, and its provider transcript identifies Dream-1 Beta, explicit non-dry-run mode and375 actual requests. The corrected validator requires this consistent recorded identity and rechecks every native frame, camera stream and scorer output. The original validation failure remains in the external evidence ledger; the simulation was not repeated and its raw record was not edited.
