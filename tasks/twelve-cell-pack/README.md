# Load and retain twelve polarity-marked cells

**ENGINEERING DRAFT — NOT READY FOR SUBMISSION.** No GPU execution, full-score demonstration,
Dream-1 result or uploaded media exists. Synthetic unit-test frames never count as trial evidence.
The source includes unfinished mechanisms and controller steps listed below; passing offline tests
does not establish construct validity or feasibility. No upstream PR should be opened for this revision.

Load every blue cell into the twelve-slot holder with its orange positive end matching the orange mark for that slot. Put the retaining plate over the cells and release the completed holder.

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
python run.py --mode expert --output "$RUN_ROOT/twelve-cell-pack/expert-1"
python run.py --mode dream --output "$RUN_ROOT/twelve-cell-pack/dream-1"
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
Each goal weighs 1/13; no prescribed ordering is imposed on independent goals. Historical first
completion timestamps are analytics only. Current-state regression loses credit. Loss or invalid
geometry permanently invalidates that episode. Release and stability must be observed continuously.

### cell_0_seated

```json
[
  {
    "kind": "pose",
    "body": "cell_0",
    "pos": [
      -0.125,
      -0.028,
      0.03275
    ],
    "relative_to": "holder",
    "quat": [
      0.0,
      0.0,
      0.0,
      1.0
    ],
    "tolerance": 0.0015,
    "angle": 0.10471975511965978
  },
  {
    "kind": "still",
    "body": "cell_0",
    "speed": 0.01,
    "spin": 0.2
  }
]
```
### cell_1_seated

```json
[
  {
    "kind": "pose",
    "body": "cell_1",
    "pos": [
      -0.075,
      -0.028,
      0.03275
    ],
    "relative_to": "holder",
    "quat": [
      1.0,
      0.0,
      0.0,
      6.123233995736766e-17
    ],
    "tolerance": 0.0015,
    "angle": 0.10471975511965978
  },
  {
    "kind": "still",
    "body": "cell_1",
    "speed": 0.01,
    "spin": 0.2
  }
]
```
### cell_2_seated

```json
[
  {
    "kind": "pose",
    "body": "cell_2",
    "pos": [
      -0.024999999999999994,
      -0.028,
      0.03275
    ],
    "relative_to": "holder",
    "quat": [
      0.0,
      0.0,
      0.0,
      1.0
    ],
    "tolerance": 0.0015,
    "angle": 0.10471975511965978
  },
  {
    "kind": "still",
    "body": "cell_2",
    "speed": 0.01,
    "spin": 0.2
  }
]
```
### cell_3_seated

```json
[
  {
    "kind": "pose",
    "body": "cell_3",
    "pos": [
      0.025000000000000022,
      -0.028,
      0.03275
    ],
    "relative_to": "holder",
    "quat": [
      1.0,
      0.0,
      0.0,
      6.123233995736766e-17
    ],
    "tolerance": 0.0015,
    "angle": 0.10471975511965978
  },
  {
    "kind": "still",
    "body": "cell_3",
    "speed": 0.01,
    "spin": 0.2
  }
]
```
### cell_4_seated

```json
[
  {
    "kind": "pose",
    "body": "cell_4",
    "pos": [
      0.07500000000000001,
      -0.028,
      0.03275
    ],
    "relative_to": "holder",
    "quat": [
      0.0,
      0.0,
      0.0,
      1.0
    ],
    "tolerance": 0.0015,
    "angle": 0.10471975511965978
  },
  {
    "kind": "still",
    "body": "cell_4",
    "speed": 0.01,
    "spin": 0.2
  }
]
```
### cell_5_seated

```json
[
  {
    "kind": "pose",
    "body": "cell_5",
    "pos": [
      0.125,
      -0.028,
      0.03275
    ],
    "relative_to": "holder",
    "quat": [
      1.0,
      0.0,
      0.0,
      6.123233995736766e-17
    ],
    "tolerance": 0.0015,
    "angle": 0.10471975511965978
  },
  {
    "kind": "still",
    "body": "cell_5",
    "speed": 0.01,
    "spin": 0.2
  }
]
```
### cell_6_seated

```json
[
  {
    "kind": "pose",
    "body": "cell_6",
    "pos": [
      -0.125,
      0.028,
      0.03275
    ],
    "relative_to": "holder",
    "quat": [
      0.0,
      0.0,
      0.0,
      1.0
    ],
    "tolerance": 0.0015,
    "angle": 0.10471975511965978
  },
  {
    "kind": "still",
    "body": "cell_6",
    "speed": 0.01,
    "spin": 0.2
  }
]
```
### cell_7_seated

```json
[
  {
    "kind": "pose",
    "body": "cell_7",
    "pos": [
      -0.075,
      0.028,
      0.03275
    ],
    "relative_to": "holder",
    "quat": [
      1.0,
      0.0,
      0.0,
      6.123233995736766e-17
    ],
    "tolerance": 0.0015,
    "angle": 0.10471975511965978
  },
  {
    "kind": "still",
    "body": "cell_7",
    "speed": 0.01,
    "spin": 0.2
  }
]
```
### cell_8_seated

```json
[
  {
    "kind": "pose",
    "body": "cell_8",
    "pos": [
      -0.024999999999999994,
      0.028,
      0.03275
    ],
    "relative_to": "holder",
    "quat": [
      0.0,
      0.0,
      0.0,
      1.0
    ],
    "tolerance": 0.0015,
    "angle": 0.10471975511965978
  },
  {
    "kind": "still",
    "body": "cell_8",
    "speed": 0.01,
    "spin": 0.2
  }
]
```
### cell_9_seated

```json
[
  {
    "kind": "pose",
    "body": "cell_9",
    "pos": [
      0.025000000000000022,
      0.028,
      0.03275
    ],
    "relative_to": "holder",
    "quat": [
      1.0,
      0.0,
      0.0,
      6.123233995736766e-17
    ],
    "tolerance": 0.0015,
    "angle": 0.10471975511965978
  },
  {
    "kind": "still",
    "body": "cell_9",
    "speed": 0.01,
    "spin": 0.2
  }
]
```
### cell_10_seated

```json
[
  {
    "kind": "pose",
    "body": "cell_10",
    "pos": [
      0.07500000000000001,
      0.028,
      0.03275
    ],
    "relative_to": "holder",
    "quat": [
      0.0,
      0.0,
      0.0,
      1.0
    ],
    "tolerance": 0.0015,
    "angle": 0.10471975511965978
  },
  {
    "kind": "still",
    "body": "cell_10",
    "speed": 0.01,
    "spin": 0.2
  }
]
```
### cell_11_seated

```json
[
  {
    "kind": "pose",
    "body": "cell_11",
    "pos": [
      0.125,
      0.028,
      0.03275
    ],
    "relative_to": "holder",
    "quat": [
      1.0,
      0.0,
      0.0,
      6.123233995736766e-17
    ],
    "tolerance": 0.0015,
    "angle": 0.10471975511965978
  },
  {
    "kind": "still",
    "body": "cell_11",
    "speed": 0.01,
    "spin": 0.2
  }
]
```
### plate_seated

```json
[
  {
    "kind": "pose",
    "body": "retaining_plate",
    "pos": [
      0,
      0,
      0.061
    ],
    "relative_to": "holder",
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
    "body": "retaining_plate",
    "speed": 0.01,
    "spin": 0.2
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

- A positive capture for the retaining plate is missing. Cell polarity marks on the holder and contact-compression tolerances require completion before model evaluation.
- Twelve repetitions alone do not clear novelty; an independently justified task redesign is required.
- Native reset, robot reach, gripper clearance, collision stability, force response and contact fidelity.
- Two genuine full-score expert trials; complete actual Dream evaluation; required media upload.
- Current novelty and ownership review. See NOVELTY.md; no acceptance claim is made.

## Media and final handoff

Keep raw logs and videos outside this branch. Once the task is actually validated, render H.264 MP4,
check duration, critical interactions and blind-review anonymity, then use the official root uploader:

```sh
python tools/upload_media.py tasks/twelve-cell-pack --video "$DREAM_MP4" --demo "$DEMO_MP4" --screenshot "$SETUP_PNG"
```

Run that command from the repository root with the team's securely supplied environment credentials.
The empty media field is intentional: no invented ID or accidental prior-upload fallback is acceptable.
Record the real score and returned ID only after successful execution/upload. The teammate alone opens
the official PR after all review gates pass. This revision must remain on a draft branch.
