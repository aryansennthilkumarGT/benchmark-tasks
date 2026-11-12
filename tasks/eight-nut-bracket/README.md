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

Run from a clean checkout using the installed environment Python. Fixed seed0 and object_jitter0 reproduce SETUP.md. The action limit is18000,900 simulated seconds. No current-revision full-score runtime is claimed while native qualification remains incomplete. This preparation copy is not submission-ready; complete experts, physics, Dream-1, media and HTTPS reproduction remain required.

`run.py --mode dream` uses securely configured official credentials and actual feasibility evidence via `--evidence`. The bootstrap/task runner retain their separate strict provider-budget path; their historical default policy is not an account-balance claim. Workload exit does not stop instance billing.

## Objective and validation

SCORING.md and scene.json define all numeric predicates and partial credit. Full score requires each fastener's measured thread advance, correct plate pose/preload/tilt, stillness and released-arm clearance over the stated stability interval. Missing or invalid physical evidence is not a passing result.

Mechanism probes exercise actual contacts and spring-load response separately from demonstrations. Default-reset control assertions may reuse post-action phase-completion frames from two independently completed full-score experts; that method claims two expert resets and no extra standalone control runs. Initialized suffix diagnostics receive no demonstration credit. All final videos must derive from genuine official camera observations and undergo full H.264 decoding plus direct visual review.

## Physical limits

Faceted thread contacts, a400N/m preload spring and two passive plate-tilt axes approximate mechanical fastening. Two tiny noncolliding inertia links encode the plate guide coordinates and are not manipulated objects. Steel/aluminium materials and contact coefficients are uncalibrated surrogates. Certified tightening torque, thread wear and elastic deformation are not modeled. All three retention points have been designed around the loaded plate; no claim that three is mechanically minimal is made without separate one/two-fastener counterfactual tests.
