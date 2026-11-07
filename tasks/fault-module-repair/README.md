# Replace a fault-marked module and preserve healthy modules

**ENGINEERING DRAFT — NOT READY FOR SUBMISSION.** No GPU execution, full-score demonstration,
Dream-1 result or uploaded media exists. Synthetic unit-test frames never count as trial evidence.
The source includes unfinished mechanisms and controller steps listed below; passing offline tests
does not establish construct validity or feasibility. No upstream PR should be opened for this revision.

Replace the red-marked middle module with the blue spare. Put the removed module in the collection tray. Keep both green modules seated and finish with the retaining bar installed.

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
python run.py --mode expert --output "$RUN_ROOT/fault-module-repair/expert-1"
python run.py --mode dream --output "$RUN_ROOT/fault-module-repair/dream-1"
```

These commands print the concrete command and pending gates. They execute only with `--execute`;
execution requires an RTX 4090, existing simulator dependencies and explicit output directory.
The expert plan is a runnable nominal pick/place prototype, **not a completed expert controller**.
It lacks the task-specific access, contact and regrasp operations below. Tune and complete it before
attempting a full-score demonstration. Never evaluate Dream against an unfinished mechanism.
The Dream mode uses the real Inspect Robots policy interface, not a mock policy. Check the installed
CLI help and model identifier before an authorized paid-credit trial. Do not run this launcher on
the controller laptop as a replacement for the required GPU machine.

Control frequency: 20 Hz. Provisional limit: 3600 actions / 180 s.
Native wall-clock runtime: unmeasured. Seed: 0, no initial jitter. Human reference time: unmeasured.
Record the actual versions, GPU identity, seed, actions, per-stage timestamps and all three native
cameras for every trial. `ROBOCURVE_TRACE` is private scorer telemetry, never model input.
Run two fresh resets for the expert, one genuine Dream evaluation, then native adversarial trials.

## Exact scoring

Positions are metres; quaternion order is XYZW; angular tolerances are radians. Pose tolerance is
Euclidean distance, not an axiswise box. Region checks contain the entire rotated collision envelope.
Each goal weighs 1/3; no prescribed ordering is imposed on independent goals. Historical first
completion timestamps are analytics only. Current-state regression loses credit. Loss or invalid
geometry permanently invalidates that episode. Release and stability must be observed continuously.

### faulty_collected

```json
[
  {
    "kind": "region",
    "body": "faulty",
    "min": [
      0.323,
      -0.307,
      0.7535000000000001
    ],
    "max": [
      0.457,
      -0.193,
      0.8375
    ]
  },
  {
    "kind": "still",
    "body": "faulty",
    "speed": 0.01,
    "spin": 0.2
  }
]
```
### spare_seated

```json
[
  {
    "kind": "pose",
    "body": "spare",
    "pos": [
      0,
      0,
      0.026
    ],
    "relative_to": "rack",
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
    "body": "spare",
    "speed": 0.01,
    "spin": 0.2
  }
]
```
### retained

```json
[
  {
    "kind": "region",
    "body": "faulty",
    "min": [
      0.323,
      -0.307,
      0.7535000000000001
    ],
    "max": [
      0.457,
      -0.193,
      0.8375
    ]
  },
  {
    "kind": "still",
    "body": "faulty",
    "speed": 0.01,
    "spin": 0.2
  },
  {
    "kind": "pose",
    "body": "spare",
    "pos": [
      0,
      0,
      0.026
    ],
    "relative_to": "rack",
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
    "body": "spare",
    "speed": 0.01,
    "spin": 0.2
  },
  {
    "kind": "pose",
    "body": "retaining_bar",
    "pos": [
      -0.071,
      0,
      0.027
    ],
    "relative_to": "rack",
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
    "body": "retaining_bar",
    "speed": 0.01,
    "spin": 0.2
  }
]
```


Preservation invariants (violation invalidates the entire episode):

```json
[
  {
    "name": "healthy_0_disturbed",
    "all": [
      {
        "kind": "pose",
        "body": "healthy_0",
        "pos": [
          0,
          -0.06,
          0.026
        ],
        "relative_to": "rack",
        "quat": [
          0.0,
          0.0,
          0.0,
          1.0
        ],
        "tolerance": 0.005,
        "angle": 0.13962634015954636
      }
    ]
  },
  {
    "name": "healthy_1_disturbed",
    "all": [
      {
        "kind": "pose",
        "body": "healthy_1",
        "pos": [
          0,
          0.06,
          0.026
        ],
        "relative_to": "rack",
        "quat": [
          0.0,
          0.0,
          0.0,
          1.0
        ],
        "tolerance": 0.005,
        "angle": 0.13962634015954636
      }
    ]
  }
]
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

- This candidate is too close to existing visible-fault drive replacement tasks and is not selected for submission.
- Retaining-bar capture features, extraction resistance and a fault-state model beyond static visible markings remain unimplemented.
- Native reset, robot reach, gripper clearance, collision stability, force response and contact fidelity.
- Two genuine full-score expert trials; complete actual Dream evaluation; required media upload.
- Current novelty and ownership review. See NOVELTY.md; no acceptance claim is made.

## Media and final handoff

Keep raw logs and videos outside this branch. Once the task is actually validated, render H.264 MP4,
check duration, critical interactions and blind-review anonymity, then use the official root uploader:

```sh
python tools/upload_media.py tasks/fault-module-repair --video "$DREAM_MP4" --demo "$DEMO_MP4" --screenshot "$SETUP_PNG"
```

Run that command from the repository root with the team's securely supplied environment credentials.
The empty media field is intentional: no invented ID or accidental prior-upload fallback is acceptable.
Record the real score and returned ID only after successful execution/upload. The teammate alone opens
the official PR after all review gates pass. This revision must remain on a draft branch.
