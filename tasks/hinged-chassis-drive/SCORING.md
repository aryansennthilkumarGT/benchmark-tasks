# Install and retain a drive under a gravity-closing lid — scoring

0.333333 for carrier_seated; 0.333333 for carrier_retained; 0.333333 for enclosure_closed. Each goal requires all numeric predicates in SCORING.md and scene.json. Credit is recomputed, so dislodged components lose credit. Full score also requires all bodies <=0.01 m/s and <=0.2 rad/s, robot clearance >=0.02 m, continuously for 1.0 s; otherwise score is capped at 0.95. Invalid frames, lost parts, fixture motion, broken preservation constraints, joint-limit violations or penetration >0.002 m permanently score zero.

Each weighted goal requires every condition below. Position/quaternion conditions use measured simulator bodies; joint values use measured native coordinates. The scorer accepts any physically valid solution order. Historical thread and preservation checks encode physical constraints, not the expert phase index.

## carrier_seated (0.333333)

- `drive` center within 0.003 m of (0, 0, 0.018), XYZW orientation (0, 0, 0, 1) within 0.10472 rad relative to chassis.
- `drive` linear speed <= 0.01 m/s and angular speed <= 0.2 rad/s.

## carrier_retained (0.333333)

- `drive` center within 0.003 m of (0, 0, 0.018), XYZW orientation (0, 0, 0, 1) within 0.10472 rad relative to chassis.
- `retainer` center within 0.003 m of (-0.065, 0, 0.025), XYZW orientation (0, 0, 0, 1) within 0.10472 rad relative to chassis.
- `retainer` linear speed <= 0.01 m/s and angular speed <= 0.2 rad/s.
- `lid_hinge` in [0, 0.04] (metres for prismatic, radians for rotary joints).

## enclosure_closed (0.333333)

- `drive` center within 0.003 m of (0, 0, 0.018), XYZW orientation (0, 0, 0, 1) within 0.10472 rad relative to chassis.
- `retainer` center within 0.003 m of (-0.065, 0, 0.025), XYZW orientation (0, 0, 0, 1) within 0.10472 rad relative to chassis.
- `lid_hinge` in [0, 0.04] (metres for prismatic, radians for rotary joints).


Malformed/missing/nonfinite data and nonmonotonic conflicting timestamps fail closed. The same frame can be queried twice without double-counting time. Unobserved gaps reset the stability window. Off-table loss uses the lowest rotated collision-bound corner, 25 mm below the tabletop. Anchors may move at most 5 mm / 3 degrees. Joint tolerances are 10 mrad rotary or 0.5 mm prismatic beyond physical limits.

Thread credit requires aligned angular increments with corresponding axial motion inside the thread engagement region. Free spinning, direct dropping and pitch-inconsistent motion earn no turn credit. Cable continuity uses connected joint endpoints; a forced catch crossing without release invalidates the episode. These checks apply only to mechanisms present in this task.

Offline tests inject synthetic states to test arithmetic and counterexamples. Native probes separately read actual simulation states and call this same scorer. No synthetic score is a demonstration result.
