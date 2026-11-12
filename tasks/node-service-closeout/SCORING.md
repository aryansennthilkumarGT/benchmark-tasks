# Exchange two internal modules and close out an enclosure — scoring

0.15 for old_cooler_collected; 0.15 for old_storage_collected; 0.25 for new_storage_seated; 0.25 for new_cooler_seated; 0.2 for service_closed_out. Each goal requires all numeric predicates in SCORING.md and scene.json. Credit is recomputed, so dislodged components lose credit. Full score also requires all bodies <=0.01 m/s and <=0.2 rad/s, robot clearance >=0.02 m, continuously for 1.0 s; otherwise score is capped at 0.95. Invalid frames, lost parts, fixture motion, broken preservation constraints, joint-limit violations or penetration >0.002 m permanently score zero.

Each weighted goal requires every condition below. Position/quaternion conditions use measured simulator bodies; joint values use measured native coordinates. The scorer accepts any physically valid solution order. Historical thread and preservation checks encode physical constraints, not the expert phase index.

## old_cooler_collected (0.15)

- Entire oriented collision bound of `old_cooler` inside (0.327, -0.328, 0.7533) to (0.505, -0.122, 0.8475) in world coordinates.
- `old_cooler` linear speed <= 0.01 m/s and angular speed <= 0.2 rad/s.

## old_storage_collected (0.15)

- Entire oriented collision bound of `old_storage` inside (0.327, -0.328, 0.7533) to (0.505, -0.122, 0.8475) in world coordinates.
- `old_storage` linear speed <= 0.01 m/s and angular speed <= 0.2 rad/s.

## new_storage_seated (0.25)

- `new_storage` center within 0.0015 m of (0, 0, 0.016), XYZW orientation (0, 0, 0, 1) within 0.105 rad relative to chassis.
- `new_storage` linear speed <= 0.01 m/s and angular speed <= 0.2 rad/s.

## new_cooler_seated (0.25)

- `new_cooler` center within 0.0015 m of (0, 0, 0.048), XYZW orientation (0, 0, 0, 1) within 0.105 rad relative to chassis.
- `new_cooler` linear speed <= 0.01 m/s and angular speed <= 0.2 rad/s.

## service_closed_out (0.2)

- Entire oriented collision bound of `old_cooler` inside (0.327, -0.328, 0.7533) to (0.505, -0.122, 0.8475) in world coordinates.
- `old_cooler` linear speed <= 0.01 m/s and angular speed <= 0.2 rad/s.
- Entire oriented collision bound of `old_storage` inside (0.327, -0.328, 0.7533) to (0.505, -0.122, 0.8475) in world coordinates.
- `old_storage` linear speed <= 0.01 m/s and angular speed <= 0.2 rad/s.
- `new_cooler` center within 0.0015 m of (0, 0, 0.048), XYZW orientation (0, 0, 0, 1) within 0.105 rad relative to chassis.
- `new_cooler` linear speed <= 0.01 m/s and angular speed <= 0.2 rad/s.
- `new_storage` center within 0.0015 m of (0, 0, 0.016), XYZW orientation (0, 0, 0, 1) within 0.105 rad relative to chassis.
- `new_storage` linear speed <= 0.01 m/s and angular speed <= 0.2 rad/s.
- `lid_hinge` in [-0.000001, 0.035] radians. The 1 microradian lower margin covers numerical contact-stop residuals. A lid opened beyond 0.035 radians fails closeout.


Malformed/missing/nonfinite data and nonmonotonic conflicting timestamps fail closed. The same frame can be queried twice without double-counting time. Unobserved gaps reset the stability window. Off-table loss uses the lowest rotated collision-bound corner, 25 mm below the tabletop. Anchors may move at most 5 mm / 3 degrees. Joint tolerances are 10 mrad rotary or 0.5 mm prismatic beyond physical limits.

Thread credit requires aligned angular increments with corresponding axial motion inside the thread engagement region. Free spinning, direct dropping and pitch-inconsistent motion earn no turn credit. Cable continuity uses connected joint endpoints; a forced catch crossing without release invalidates the episode. These checks apply only to mechanisms present in this task.

Offline tests inject synthetic states to test arithmetic and counterexamples. Native probes separately read actual simulation states and call this same scorer. No synthetic score is a demonstration result.

Region containment checks every oriented collision box in each compound part. The same numeric region limits apply to every actual box vertex, including handles and tabs. This avoids fictitious corners introduced by rotating a single enclosing body bound. Synthetic tilted-compound and protruding-part regressions cover the calculation. Native collection validation remains required.

The storage target height is 16 mm above the chassis root. The 8 mm floor top plus the storage core half-height of 8 mm determines this datum. The unchanged 1.5 mm spherical tolerance applies around that physical seating position.
