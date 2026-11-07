# Exchange two internal modules and close out an enclosure

**ENGINEERING DRAFT — NOT READY FOR SUBMISSION.** No GPU execution, full-score demonstration,
Dream-1 result or uploaded media exists. Synthetic unit-test frames never count as trial evidence.
The source includes unfinished mechanisms and controller steps listed below; passing offline tests
does not establish construct validity or feasibility. No upstream PR should be opened for this revision.

Replace the grey storage module and grey cooling module with their blue matching spares. Collect the removed modules in the tray, secure the orange retaining bar, and close the lid.

## Reproduce offline checks

From this task folder, using Python 3.11 or later:

```sh
python -m unittest -v test_scoring.py
python -m pip install usd-core==25.11
python build_assets.py
python verify_assets.py
```

`scene.json` is the authoritative geometry, initial poses, masses, constraints and tolerances.
`INVENTORY.txt` lists every rigid body. Each assembly USD is generated from original primitives.
Friction is 0.65 static / 0.5 dynamic; restitution is zero. Robot controls never write task poses.
USD structural validation is not a PhysX simulation test. AABB/OBB overlap checks use conservative
cylinder bounds and can reject valid corner contacts; calibrate against real contact telemetry.

## Native execution (pending)

Activate an existing isolated Isaac Lab-Arena environment on the verified RTX 4090.
Do not install or modify system drivers. The inspected adapter is
`kairosiann/yam-isaac-lab-arena@bd62771e60320433893bd1d2df0fc79b5ddcd6d1`;
its documented stack is Arena 0.3.1 / Isaac Lab 3.0 / Isaac Sim 6.1 / Python 3.12.
Inspect Robots 1.0 compatibility and the actual lab installation remain unverified.
No third-party adapter code is vendored. Use the upstream setup documentation after inspecting it.

```sh
source "$ARENA_DIR/yam.env"
python run.py --mode expert --output "$RUN_ROOT/node-service-closeout/expert-1"
python run.py --mode dream --output "$RUN_ROOT/node-service-closeout/dream-1"
```

These commands print the concrete command and pending gates. They execute only with `--execute`;
execution requires an RTX 4090, existing simulator dependencies and explicit output directory.
The expert plan is a runnable nominal pick/place prototype, **not a completed expert controller**.
It lacks the task-specific access, contact and regrasp operations below. Tune and complete it before
attempting a full-score demonstration. Never evaluate Dream against an unfinished mechanism.
The Dream mode uses the real Inspect Robots policy interface, not a mock policy. Check the installed
CLI help and model identifier before an authorized paid-credit trial. Do not run this launcher on
the controller laptop as a replacement for the required GPU machine.

Control frequency: 20 Hz. Provisional limit: 6000 actions / 300 s.
Native wall-clock runtime: unmeasured. Seed: 0, no initial jitter. Human reference time: unmeasured.
Record the actual versions, GPU identity, seed, actions, per-stage timestamps and all three native
cameras for every trial. `ROBOCURVE_TRACE` is private scorer telemetry, never model input.
Run two fresh resets for the expert, one genuine Dream evaluation, then native adversarial trials.

## Exact scoring

Positions are metres; quaternion order is XYZW; angular tolerances are radians. Pose tolerance is
Euclidean distance, not an axiswise box. Region checks contain the entire rotated collision envelope.
Each goal weighs 1/5; no prescribed ordering is imposed on independent goals. Historical first
completion timestamps are analytics only. Current-state regression loses credit. Loss or invalid
geometry permanently invalidates that episode. Release and stability must be observed continuously.

### old_storage_collected

```json
[
  {
    "kind": "region",
    "body": "old_storage",
    "min": [
      0.333,
      0.178,
      0.7535000000000001
    ],
    "max": [
      0.467,
      0.302,
      0.8375
    ]
  },
  {
    "kind": "still",
    "body": "old_storage",
    "speed": 0.01,
    "spin": 0.2
  }
]
```
### new_storage_seated

```json
[
  {
    "kind": "pose",
    "body": "new_storage",
    "pos": [
      0,
      -0.023,
      0.021
    ],
    "relative_to": "chassis",
    "quat": [
      0.0,
      0.0,
      0.0,
      1.0
    ],
    "tolerance": 0.003,
    "angle": 0.10471975511965978
  },
  {
    "kind": "still",
    "body": "new_storage",
    "speed": 0.01,
    "spin": 0.2
  }
]
```
### old_cooler_collected

```json
[
  {
    "kind": "region",
    "body": "old_cooler",
    "min": [
      0.333,
      0.178,
      0.7535000000000001
    ],
    "max": [
      0.467,
      0.302,
      0.8375
    ]
  },
  {
    "kind": "still",
    "body": "old_cooler",
    "speed": 0.01,
    "spin": 0.2
  }
]
```
### new_cooler_seated

```json
[
  {
    "kind": "pose",
    "body": "new_cooler",
    "pos": [
      0,
      0.023,
      0.021
    ],
    "relative_to": "chassis",
    "quat": [
      0.0,
      0.0,
      0.0,
      1.0
    ],
    "tolerance": 0.003,
    "angle": 0.10471975511965978
  },
  {
    "kind": "still",
    "body": "new_cooler",
    "speed": 0.01,
    "spin": 0.2
  }
]
```
### service_closed_out

```json
[
  {
    "kind": "region",
    "body": "old_storage",
    "min": [
      0.333,
      0.178,
      0.7535000000000001
    ],
    "max": [
      0.467,
      0.302,
      0.8375
    ]
  },
  {
    "kind": "still",
    "body": "old_storage",
    "speed": 0.01,
    "spin": 0.2
  },
  {
    "kind": "pose",
    "body": "new_storage",
    "pos": [
      0,
      -0.023,
      0.021
    ],
    "relative_to": "chassis",
    "quat": [
      0.0,
      0.0,
      0.0,
      1.0
    ],
    "tolerance": 0.003,
    "angle": 0.10471975511965978
  },
  {
    "kind": "still",
    "body": "new_storage",
    "speed": 0.01,
    "spin": 0.2
  },
  {
    "kind": "region",
    "body": "old_cooler",
    "min": [
      0.333,
      0.178,
      0.7535000000000001
    ],
    "max": [
      0.467,
      0.302,
      0.8375
    ]
  },
  {
    "kind": "still",
    "body": "old_cooler",
    "speed": 0.01,
    "spin": 0.2
  },
  {
    "kind": "pose",
    "body": "new_cooler",
    "pos": [
      0,
      0.023,
      0.021
    ],
    "relative_to": "chassis",
    "quat": [
      0.0,
      0.0,
      0.0,
      1.0
    ],
    "tolerance": 0.003,
    "angle": 0.10471975511965978
  },
  {
    "kind": "still",
    "body": "new_cooler",
    "speed": 0.01,
    "spin": 0.2
  },
  {
    "kind": "pose",
    "body": "service_bar",
    "pos": [
      -0.05,
      0,
      0.028
    ],
    "relative_to": "chassis",
    "quat": [
      0.0,
      0.0,
      0.0,
      1.0
    ],
    "tolerance": 0.003,
    "angle": 0.10471975511965978
  },
  {
    "kind": "joint",
    "joint": "lid_hinge",
    "min": 0,
    "max": 0.04
  }
]
```


Preservation invariants (violation invalidates the entire episode):

```json
[]
```

Forbidden kit occupancy and helical-engagement definitions, when applicable:

```json
{
  "forbidden_regions": [],
  "threads": []
}
```

Fixed bodies must remain within 5 mm and 3 degrees of their documented initial pose. A body whose
lowest collision-bound corner crosses 25 mm below the tabletop is lost. Mechanical joint limits
allow only a 0.5 mm prismatic / 0.01 rad revolute measurement margin. Nut rotation counts only while
coaxially engaged and coupled cumulatively to axial advance at the declared pitch; spinning in place
and dropping an unturned nut onto a stud do not count. Conservative bounds and thresholds require
comparison with native contact data before review approval.

## Unresolved review gates

- The gravity-loaded lid and its contact clearances require native validation. The draft expert only includes a lid-handle approach, not a calibrated hinge-following motion.
- The two modules currently share proxy geometry; component-specific interfaces, keys and retainers must be implemented before claiming a heterogeneous servicing construct.
- An independent novelty case beyond concatenating existing maintenance tasks remains unresolved.
- Native reset, robot reach, gripper clearance, collision stability, force response and contact fidelity.
- Two genuine full-score expert trials; complete actual Dream evaluation; required media upload.
- Current novelty and ownership review. See NOVELTY.md; no acceptance claim is made.

## Media and final handoff

Keep raw logs and videos outside this branch. Once the task is actually validated, render H.264 MP4,
check duration, critical interactions and blind-review anonymity, then use the official root uploader:

```sh
python tools/upload_media.py tasks/node-service-closeout --video "$DREAM_MP4" --demo "$DEMO_MP4" --screenshot "$SETUP_PNG"
```

Run that command from the repository root with the team's securely supplied environment credentials.
The empty media field is intentional: no invented ID or accidental prior-upload fallback is acceptable.
Record the real score and returned ID only after successful execution/upload. The teammate alone opens
the official PR after all review gates pass. This revision must remain on a draft branch.
