# Balance and lock a counterweighted service arm — scoring

0.3 for counterweight_aligned; 0.3 for counterweight_pinned; 0.4 for released_arm_balanced. Each goal requires all numeric predicates in SCORING.md and scene.json. Credit is recomputed, so dislodged components lose credit. Full score also requires all bodies <=0.01 m/s and <=0.2 rad/s, robot clearance >=0.02 m, continuously for 3.0 s; otherwise score is capped at 0.95. Invalid frames, lost parts, fixture motion, broken preservation constraints, joint-limit violations or penetration >0.002 m permanently score zero.

Each weighted goal requires every condition below. Position/quaternion conditions use measured simulator bodies; joint values use measured native coordinates. The scorer accepts any physically valid solution order. Historical thread and preservation checks encode physical constraints, not the expert phase index.

## counterweight_aligned (0.3)

- `weight_slide` in [-0.032, -0.03] (metres for prismatic, radians for rotary joints).
- `counterweight` linear speed <= 0.01 m/s and angular speed <= 0.2 rad/s.

## counterweight_pinned (0.3)

- `weight_slide` in [-0.032, -0.03] (metres for prismatic, radians for rotary joints).
- `counterweight` linear speed <= 0.01 m/s and angular speed <= 0.2 rad/s.
- `locking_pin` center within 0.0015 m of (-0.066, 0, -0.004), XYZW orientation (0, 0, 0, 1) within 0.105 rad relative to service_arm.
- `locking_pin` linear speed <= 0.01 m/s and angular speed <= 0.2 rad/s.

## released_arm_balanced (0.4)

- `weight_slide` in [-0.032, -0.03] (metres for prismatic, radians for rotary joints).
- `counterweight` linear speed <= 0.01 m/s and angular speed <= 0.2 rad/s.
- `locking_pin` center within 0.0015 m of (-0.066, 0, -0.004), XYZW orientation (0, 0, 0, 1) within 0.105 rad relative to service_arm.
- `locking_pin` linear speed <= 0.01 m/s and angular speed <= 0.2 rad/s.
- `arm_pivot` in [-0.04, 0.04] (metres for prismatic, radians for rotary joints).
- `service_arm` linear speed <= 0.01 m/s and angular speed <= 0.2 rad/s.


Malformed/missing/nonfinite data and nonmonotonic conflicting timestamps fail closed. The same frame can be queried twice without double-counting time. Unobserved gaps reset the stability window. Off-table loss uses the lowest rotated collision-bound corner, 25 mm below the tabletop. Anchors may move at most 5 mm / 3 degrees. Joint tolerances are 10 mrad rotary or 0.5 mm prismatic beyond physical limits.

Thread credit requires aligned angular increments with corresponding axial motion inside the thread engagement region. Free spinning, direct dropping and pitch-inconsistent motion earn no turn credit. Cable continuity uses connected joint endpoints; a forced catch crossing without release invalidates the episode. These checks apply only to mechanisms present in this task.

Offline tests inject synthetic states to test arithmetic and counterexamples. Native probes separately read actual simulation states and call this same scorer. No synthetic score is a demonstration result.
