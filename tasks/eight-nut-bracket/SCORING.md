# Scoring

All goals use observed native poses, joint positions and pitch-coupled turn history. Three interchangeable nuts are matched one-to-one to the three available studs. A nut earns credit for at most one slot. Changing studs clears its accumulated engagement history.

Each seated nut contributes0.2. The retained plate preload contributes0.4 after all three nuts complete at least3.45turns. Full success additionally requires every body at most0.01m/s and0.2rad/s and both arms at least20mm clear for2seconds. Before that released stability hold, credit is capped at0.95. Credit is recomputed and lost when a goal is disturbed.

Invalid telemetry, a lost part, fixture displacement, a broken preservation condition, a joint-limit violation, an undersampled rotation or penetration over2mm permanently gives zero. All other outcomes receive the sum of currently satisfied goal weights, subject to the0.95 cap.

The exact numeric predicates follow. Positions are relative to the named reference body. Angular tolerances use radians. The full thread accounting definitions are in scene.json.

```json
[
  {
    "name": "nut_0_threaded",
    "all": [
      {
        "kind": "pose",
        "body": "nut_0",
        "pos": [
          -0.09,
          -0.05,
          0.0172
        ],
        "relative_to": "bracket",
        "quat": [
          0.0,
          0.0,
          0.0,
          1.0
        ],
        "tolerance": 0.0007,
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
        "min": 3.4
      },
      {
        "kind": "still",
        "body": "nut_0",
        "speed": 0.01,
        "spin": 0.2
      }
    ],
    "weight": 0.2,
    "template_body": "nut_0",
    "candidate_bodies": [
      "nut_0",
      "nut_1",
      "nut_2"
    ]
  },
  {
    "name": "nut_1_threaded",
    "all": [
      {
        "kind": "pose",
        "body": "nut_1",
        "pos": [
          0.09,
          -0.05,
          0.0172
        ],
        "relative_to": "bracket",
        "quat": [
          0.0,
          0.0,
          0.0,
          1.0
        ],
        "tolerance": 0.0007,
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
        "min": 3.4
      },
      {
        "kind": "still",
        "body": "nut_1",
        "speed": 0.01,
        "spin": 0.2
      }
    ],
    "weight": 0.2,
    "template_body": "nut_1",
    "candidate_bodies": [
      "nut_0",
      "nut_1",
      "nut_2"
    ]
  },
  {
    "name": "nut_2_threaded",
    "all": [
      {
        "kind": "pose",
        "body": "nut_2",
        "pos": [
          -0.03,
          0.05,
          0.0172
        ],
        "relative_to": "bracket",
        "quat": [
          0.0,
          0.0,
          0.0,
          1.0
        ],
        "tolerance": 0.0007,
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
        "min": 3.4
      },
      {
        "kind": "still",
        "body": "nut_2",
        "speed": 0.01,
        "spin": 0.2
      }
    ],
    "weight": 0.2,
    "template_body": "nut_2",
    "candidate_bodies": [
      "nut_0",
      "nut_1",
      "nut_2"
    ]
  },
  {
    "name": "plate_preload_retained",
    "weight": 0.4,
    "all": [
      {
        "kind": "pose",
        "body": "pressure_plate",
        "pos": [
          0,
          0,
          0.01
        ],
        "relative_to": "bracket",
        "quat": [
          0,
          0,
          0,
          1
        ],
        "tolerance": 0.001,
        "angle": 0.035
      },
      {
        "kind": "joint",
        "joint": "plate_preload",
        "min": -0.013,
        "max": -0.011
      },
      {
        "kind": "joint",
        "joint": "plate_tilt_x",
        "min": -0.035,
        "max": 0.035
      },
      {
        "kind": "joint",
        "joint": "plate_tilt_y",
        "min": -0.035,
        "max": 0.035
      },
      {
        "kind": "still",
        "body": "pressure_plate",
        "speed": 0.01,
        "spin": 0.2
      },
      {
        "kind": "turns",
        "body": "nut_0",
        "min": 3.45
      },
      {
        "kind": "turns",
        "body": "nut_1",
        "min": 3.45
      },
      {
        "kind": "turns",
        "body": "nut_2",
        "min": 3.45
      }
    ],
    "requires": [
      "nut_0_threaded",
      "nut_1_threaded",
      "nut_2_threaded"
    ]
  }
]
```

A nut must remain within1.8mm of a stud axis, and cumulative axial progress must match its4mm pitch within0.65mm. Merely placing a nut at the endpoint does not establish the required measured turns.
