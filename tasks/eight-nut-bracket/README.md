# Thread eight nuts onto a supported bracket

**ENGINEERING DRAFT — NOT READY FOR SUBMISSION.** No GPU execution, full-score demonstration,
Dream-1 result or uploaded media exists. Synthetic unit-test frames never count as trial evidence.
The source includes unfinished mechanisms and controller steps listed below; passing offline tests
does not establish construct validity or feasibility. No upstream PR should be opened for this revision.

Fit all eight orange nuts onto the bracket studs. Each must advance at least two complete turns and reach the marked seating band. Leave the bracket on its outline and release all parts.

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
python run.py --mode expert --output "$RUN_ROOT/eight-nut-bracket/expert-1"
python run.py --mode dream --output "$RUN_ROOT/eight-nut-bracket/dream-1"
```

These commands print the concrete command and pending gates. They execute only with `--execute`;
execution requires an RTX 4090, existing simulator dependencies and explicit output directory.
The expert plan is a runnable nominal pick/place prototype, **not a completed expert controller**.
It lacks the task-specific access, contact and regrasp operations below. Tune and complete it before
attempting a full-score demonstration. Never evaluate Dream against an unfinished mechanism.
The Dream mode uses the real Inspect Robots policy interface, not a mock policy. Check the installed
CLI help and model identifier before an authorized paid-credit trial. Do not run this launcher on
the controller laptop as a replacement for the required GPU machine.

Control frequency: 20 Hz. Provisional limit: 7200 actions / 360 s.
Native wall-clock runtime: unmeasured. Seed: 0, no initial jitter. Human reference time: unmeasured.
Record the actual versions, GPU identity, seed, actions, per-stage timestamps and all three native
cameras for every trial. `ROBOCURVE_TRACE` is private scorer telemetry, never model input.
Run two fresh resets for the expert, one genuine Dream evaluation, then native adversarial trials.

## Exact scoring

Positions are metres; quaternion order is XYZW; angular tolerances are radians. Pose tolerance is
Euclidean distance, not an axiswise box. Region checks contain the entire rotated collision envelope.
Each goal weighs 1/8; no prescribed ordering is imposed on independent goals. Historical first
completion timestamps are analytics only. Current-state regression loses credit. Loss or invalid
geometry permanently invalidates that episode. Release and stability must be observed continuously.

### nut_0_threaded

```json
[
  {
    "kind": "pose",
    "body": "nut_0",
    "pos": [
      -0.09,
      -0.05,
      0.016
    ],
    "relative_to": "bracket",
    "quat": [
      0.0,
      0.0,
      0.0,
      1.0
    ],
    "tolerance": 0.002,
    "angle": 3.141592653589793
  },
  {
    "kind": "axis",
    "body": "nut_0",
    "relative_to": "bracket",
    "direction": [
      0,
      0,
      1
    ],
    "angle": 0.10471975511965978
  },
  {
    "kind": "turns",
    "body": "nut_0",
    "min": 2.0
  },
  {
    "kind": "still",
    "body": "nut_0",
    "speed": 0.01,
    "spin": 0.2
  }
]
```
### nut_1_threaded

```json
[
  {
    "kind": "pose",
    "body": "nut_1",
    "pos": [
      -0.03,
      -0.05,
      0.016
    ],
    "relative_to": "bracket",
    "quat": [
      0.0,
      0.0,
      0.0,
      1.0
    ],
    "tolerance": 0.002,
    "angle": 3.141592653589793
  },
  {
    "kind": "axis",
    "body": "nut_1",
    "relative_to": "bracket",
    "direction": [
      0,
      0,
      1
    ],
    "angle": 0.10471975511965978
  },
  {
    "kind": "turns",
    "body": "nut_1",
    "min": 2.0
  },
  {
    "kind": "still",
    "body": "nut_1",
    "speed": 0.01,
    "spin": 0.2
  }
]
```
### nut_2_threaded

```json
[
  {
    "kind": "pose",
    "body": "nut_2",
    "pos": [
      0.03,
      -0.05,
      0.016
    ],
    "relative_to": "bracket",
    "quat": [
      0.0,
      0.0,
      0.0,
      1.0
    ],
    "tolerance": 0.002,
    "angle": 3.141592653589793
  },
  {
    "kind": "axis",
    "body": "nut_2",
    "relative_to": "bracket",
    "direction": [
      0,
      0,
      1
    ],
    "angle": 0.10471975511965978
  },
  {
    "kind": "turns",
    "body": "nut_2",
    "min": 2.0
  },
  {
    "kind": "still",
    "body": "nut_2",
    "speed": 0.01,
    "spin": 0.2
  }
]
```
### nut_3_threaded

```json
[
  {
    "kind": "pose",
    "body": "nut_3",
    "pos": [
      0.09,
      -0.05,
      0.016
    ],
    "relative_to": "bracket",
    "quat": [
      0.0,
      0.0,
      0.0,
      1.0
    ],
    "tolerance": 0.002,
    "angle": 3.141592653589793
  },
  {
    "kind": "axis",
    "body": "nut_3",
    "relative_to": "bracket",
    "direction": [
      0,
      0,
      1
    ],
    "angle": 0.10471975511965978
  },
  {
    "kind": "turns",
    "body": "nut_3",
    "min": 2.0
  },
  {
    "kind": "still",
    "body": "nut_3",
    "speed": 0.01,
    "spin": 0.2
  }
]
```
### nut_4_threaded

```json
[
  {
    "kind": "pose",
    "body": "nut_4",
    "pos": [
      -0.09,
      0.05,
      0.016
    ],
    "relative_to": "bracket",
    "quat": [
      0.0,
      0.0,
      0.0,
      1.0
    ],
    "tolerance": 0.002,
    "angle": 3.141592653589793
  },
  {
    "kind": "axis",
    "body": "nut_4",
    "relative_to": "bracket",
    "direction": [
      0,
      0,
      1
    ],
    "angle": 0.10471975511965978
  },
  {
    "kind": "turns",
    "body": "nut_4",
    "min": 2.0
  },
  {
    "kind": "still",
    "body": "nut_4",
    "speed": 0.01,
    "spin": 0.2
  }
]
```
### nut_5_threaded

```json
[
  {
    "kind": "pose",
    "body": "nut_5",
    "pos": [
      -0.03,
      0.05,
      0.016
    ],
    "relative_to": "bracket",
    "quat": [
      0.0,
      0.0,
      0.0,
      1.0
    ],
    "tolerance": 0.002,
    "angle": 3.141592653589793
  },
  {
    "kind": "axis",
    "body": "nut_5",
    "relative_to": "bracket",
    "direction": [
      0,
      0,
      1
    ],
    "angle": 0.10471975511965978
  },
  {
    "kind": "turns",
    "body": "nut_5",
    "min": 2.0
  },
  {
    "kind": "still",
    "body": "nut_5",
    "speed": 0.01,
    "spin": 0.2
  }
]
```
### nut_6_threaded

```json
[
  {
    "kind": "pose",
    "body": "nut_6",
    "pos": [
      0.03,
      0.05,
      0.016
    ],
    "relative_to": "bracket",
    "quat": [
      0.0,
      0.0,
      0.0,
      1.0
    ],
    "tolerance": 0.002,
    "angle": 3.141592653589793
  },
  {
    "kind": "axis",
    "body": "nut_6",
    "relative_to": "bracket",
    "direction": [
      0,
      0,
      1
    ],
    "angle": 0.10471975511965978
  },
  {
    "kind": "turns",
    "body": "nut_6",
    "min": 2.0
  },
  {
    "kind": "still",
    "body": "nut_6",
    "speed": 0.01,
    "spin": 0.2
  }
]
```
### nut_7_threaded

```json
[
  {
    "kind": "pose",
    "body": "nut_7",
    "pos": [
      0.09,
      0.05,
      0.016
    ],
    "relative_to": "bracket",
    "quat": [
      0.0,
      0.0,
      0.0,
      1.0
    ],
    "tolerance": 0.002,
    "angle": 3.141592653589793
  },
  {
    "kind": "axis",
    "body": "nut_7",
    "relative_to": "bracket",
    "direction": [
      0,
      0,
      1
    ],
    "angle": 0.10471975511965978
  },
  {
    "kind": "turns",
    "body": "nut_7",
    "min": 2.0
  },
  {
    "kind": "still",
    "body": "nut_7",
    "speed": 0.01,
    "spin": 0.2
  }
]
```


Preservation invariants (violation invalidates the entire episode):

```json
[
  {
    "name": "bracket_displaced",
    "all": [
      {
        "kind": "pose",
        "body": "bracket",
        "pos": [
          0.285,
          0,
          0.7515000000000001
        ],
        "relative_to": null,
        "quat": [
          0.0,
          0.0,
          0.0,
          1.0
        ],
        "tolerance": 0.025,
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
  "threads": [
    {
      "body": "nut_0",
      "reference": "bracket",
      "xy": [
        -0.09,
        -0.05
      ],
      "radial_tolerance": 0.0018,
      "z_min": 0.008,
      "z_max": 0.04,
      "pitch": 0.004,
      "axial_slack": 0.0008
    },
    {
      "body": "nut_1",
      "reference": "bracket",
      "xy": [
        -0.03,
        -0.05
      ],
      "radial_tolerance": 0.0018,
      "z_min": 0.008,
      "z_max": 0.04,
      "pitch": 0.004,
      "axial_slack": 0.0008
    },
    {
      "body": "nut_2",
      "reference": "bracket",
      "xy": [
        0.03,
        -0.05
      ],
      "radial_tolerance": 0.0018,
      "z_min": 0.008,
      "z_max": 0.04,
      "pitch": 0.004,
      "axial_slack": 0.0008
    },
    {
      "body": "nut_3",
      "reference": "bracket",
      "xy": [
        0.09,
        -0.05
      ],
      "radial_tolerance": 0.0018,
      "z_min": 0.008,
      "z_max": 0.04,
      "pitch": 0.004,
      "axial_slack": 0.0008
    },
    {
      "body": "nut_4",
      "reference": "bracket",
      "xy": [
        -0.09,
        0.05
      ],
      "radial_tolerance": 0.0018,
      "z_min": 0.008,
      "z_max": 0.04,
      "pitch": 0.004,
      "axial_slack": 0.0008
    },
    {
      "body": "nut_5",
      "reference": "bracket",
      "xy": [
        -0.03,
        0.05
      ],
      "radial_tolerance": 0.0018,
      "z_min": 0.008,
      "z_max": 0.04,
      "pitch": 0.004,
      "axial_slack": 0.0008
    },
    {
      "body": "nut_6",
      "reference": "bracket",
      "xy": [
        0.03,
        0.05
      ],
      "radial_tolerance": 0.0018,
      "z_min": 0.008,
      "z_max": 0.04,
      "pitch": 0.004,
      "axial_slack": 0.0008
    },
    {
      "body": "nut_7",
      "reference": "bracket",
      "xy": [
        0.09,
        0.05
      ],
      "radial_tolerance": 0.0018,
      "z_min": 0.008,
      "z_max": 0.04,
      "pitch": 0.004,
      "axial_slack": 0.0008
    }
  ]
}
```

Fixed bodies must remain within 5 mm and 3 degrees of their documented initial pose. A body whose
lowest collision-bound corner crosses 25 mm below the tabletop is lost. Mechanical joint limits
allow only a 0.5 mm prismatic / 0.01 rad revolute measurement margin. Nut rotation counts only while
coaxially engaged and coupled cumulatively to axial advance at the declared pitch; spinning in place
and dropping an unturned nut onto a stud do not count. Conservative bounds and thresholds require
comparison with native contact data before review approval.

## Unresolved review gates

- Box-segment helical collision surfaces are an unvalidated coarse approximation. Clearance, handedness, friction, crest overlap and two-turn retention need native tests.
- The expert plan currently positions nuts; repeated wrist rotation and regrasp control are not calibrated or validated.
- RoboDojo Fasten Screws and existing multi-stud tasks create a high novelty risk. Eight fasteners alone is not a substantive distinction.
- Native reset, robot reach, gripper clearance, collision stability, force response and contact fidelity.
- Two genuine full-score expert trials; complete actual Dream evaluation; required media upload.
- Current novelty and ownership review. See NOVELTY.md; no acceptance claim is made.

## Media and final handoff

Keep raw logs and videos outside this branch. Once the task is actually validated, render H.264 MP4,
check duration, critical interactions and blind-review anonymity, then use the official root uploader:

```sh
python tools/upload_media.py tasks/eight-nut-bracket --video "$DREAM_MP4" --demo "$DEMO_MP4" --screenshot "$SETUP_PNG"
```

Run that command from the repository root with the team's securely supplied environment credentials.
The empty media field is intentional: no invented ID or accidental prior-upload fallback is acceptable.
Record the real score and returned ID only after successful execution/upload. The teammate alone opens
the official PR after all review gates pass. This revision must remain on a draft branch.
