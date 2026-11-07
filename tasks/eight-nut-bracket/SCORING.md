# Fasten a spring-loaded access plate while maintaining its preload — scoring

0.1 for nut_0_threaded; 0.1 for nut_1_threaded; 0.1 for nut_2_threaded; 0.1 for nut_3_threaded; 0.1 for nut_4_threaded; 0.1 for nut_5_threaded; 0.1 for nut_6_threaded; 0.1 for nut_7_threaded; 0.2 for plate_preload_retained. Each goal requires all numeric predicates in SCORING.md and scene.json. Credit is recomputed, so dislodged components lose credit. Full score also requires all bodies <=0.01 m/s and <=0.2 rad/s, robot clearance >=0.02 m, continuously for 2.0 s; otherwise score is capped at 0.95. Invalid frames, lost parts, fixture motion, broken preservation constraints, joint-limit violations or penetration >0.002 m permanently score zero.

Each weighted goal requires every condition below. Position/quaternion conditions use measured simulator bodies; joint values use measured native coordinates. The scorer accepts any physically valid solution order. Historical thread and preservation checks encode physical constraints, not the expert phase index.

## nut_0_threaded (0.1)

- `nut_0` center within 0.0007 m of (-0.09, -0.05, 0.0172), XYZW orientation (0, 0, 0, 1) within 3.14159 rad relative to bracket.
- `nut_0` local axis (0, 0, 1) within 0.10472 rad of (0, 0, 1) relative to bracket.
- `nut_0` has at least 3.4 measured pitch-coupled revolutions.
- `nut_0` linear speed <= 0.01 m/s and angular speed <= 0.2 rad/s.

## nut_1_threaded (0.1)

- `nut_1` center within 0.0007 m of (-0.03, -0.05, 0.0172), XYZW orientation (0, 0, 0, 1) within 3.14159 rad relative to bracket.
- `nut_1` local axis (0, 0, 1) within 0.10472 rad of (0, 0, 1) relative to bracket.
- `nut_1` has at least 3.4 measured pitch-coupled revolutions.
- `nut_1` linear speed <= 0.01 m/s and angular speed <= 0.2 rad/s.

## nut_2_threaded (0.1)

- `nut_2` center within 0.0007 m of (0.03, -0.05, 0.0172), XYZW orientation (0, 0, 0, 1) within 3.14159 rad relative to bracket.
- `nut_2` local axis (0, 0, 1) within 0.10472 rad of (0, 0, 1) relative to bracket.
- `nut_2` has at least 3.4 measured pitch-coupled revolutions.
- `nut_2` linear speed <= 0.01 m/s and angular speed <= 0.2 rad/s.

## nut_3_threaded (0.1)

- `nut_3` center within 0.0007 m of (0.09, -0.05, 0.0172), XYZW orientation (0, 0, 0, 1) within 3.14159 rad relative to bracket.
- `nut_3` local axis (0, 0, 1) within 0.10472 rad of (0, 0, 1) relative to bracket.
- `nut_3` has at least 3.4 measured pitch-coupled revolutions.
- `nut_3` linear speed <= 0.01 m/s and angular speed <= 0.2 rad/s.

## nut_4_threaded (0.1)

- `nut_4` center within 0.0007 m of (-0.09, 0.05, 0.0172), XYZW orientation (0, 0, 0, 1) within 3.14159 rad relative to bracket.
- `nut_4` local axis (0, 0, 1) within 0.10472 rad of (0, 0, 1) relative to bracket.
- `nut_4` has at least 3.4 measured pitch-coupled revolutions.
- `nut_4` linear speed <= 0.01 m/s and angular speed <= 0.2 rad/s.

## nut_5_threaded (0.1)

- `nut_5` center within 0.0007 m of (-0.03, 0.05, 0.0172), XYZW orientation (0, 0, 0, 1) within 3.14159 rad relative to bracket.
- `nut_5` local axis (0, 0, 1) within 0.10472 rad of (0, 0, 1) relative to bracket.
- `nut_5` has at least 3.4 measured pitch-coupled revolutions.
- `nut_5` linear speed <= 0.01 m/s and angular speed <= 0.2 rad/s.

## nut_6_threaded (0.1)

- `nut_6` center within 0.0007 m of (0.03, 0.05, 0.0172), XYZW orientation (0, 0, 0, 1) within 3.14159 rad relative to bracket.
- `nut_6` local axis (0, 0, 1) within 0.10472 rad of (0, 0, 1) relative to bracket.
- `nut_6` has at least 3.4 measured pitch-coupled revolutions.
- `nut_6` linear speed <= 0.01 m/s and angular speed <= 0.2 rad/s.

## nut_7_threaded (0.1)

- `nut_7` center within 0.0007 m of (0.09, 0.05, 0.0172), XYZW orientation (0, 0, 0, 1) within 3.14159 rad relative to bracket.
- `nut_7` local axis (0, 0, 1) within 0.10472 rad of (0, 0, 1) relative to bracket.
- `nut_7` has at least 3.4 measured pitch-coupled revolutions.
- `nut_7` linear speed <= 0.01 m/s and angular speed <= 0.2 rad/s.

## plate_preload_retained (0.2)

- `pressure_plate` center within 0.001 m of (0, 0, 0.01), XYZW orientation (0, 0, 0, 1) within 0.035 rad relative to bracket.
- `plate_preload` in [-0.013, -0.011] (metres for prismatic, radians for rotary joints).
- `plate_tilt_x` in [-0.035, 0.035] (metres for prismatic, radians for rotary joints).
- `plate_tilt_y` in [-0.035, 0.035] (metres for prismatic, radians for rotary joints).
- `pressure_plate` linear speed <= 0.01 m/s and angular speed <= 0.2 rad/s.
- `nut_0` has at least 3.45 measured pitch-coupled revolutions.
- `nut_1` has at least 3.45 measured pitch-coupled revolutions.
- `nut_2` has at least 3.45 measured pitch-coupled revolutions.
- `nut_3` has at least 3.45 measured pitch-coupled revolutions.
- `nut_4` has at least 3.45 measured pitch-coupled revolutions.
- `nut_5` has at least 3.45 measured pitch-coupled revolutions.
- `nut_6` has at least 3.45 measured pitch-coupled revolutions.
- `nut_7` has at least 3.45 measured pitch-coupled revolutions.


Malformed/missing/nonfinite data and nonmonotonic conflicting timestamps fail closed. The same frame can be queried twice without double-counting time. Unobserved gaps reset the stability window. Off-table loss uses the lowest rotated collision-bound corner, 25 mm below the tabletop. Anchors may move at most 5 mm / 3 degrees. Joint tolerances are 10 mrad rotary or 0.5 mm prismatic beyond physical limits.

Thread credit requires aligned angular increments with corresponding axial motion inside the thread engagement region. Free spinning, direct dropping and pitch-inconsistent motion earn no turn credit. Cable continuity uses connected joint endpoints; a forced catch crossing without release invalidates the episode. These checks apply only to mechanisms present in this task.

Offline tests inject synthetic states to test arithmetic and counterexamples. Native probes separately read actual simulation states and call this same scorer. No synthetic score is a demonstration result.
