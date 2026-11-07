# Preload and retain a twelve-cell service pack — scoring

0.06 for cell_0_contacted; 0.06 for cell_1_contacted; 0.06 for cell_2_contacted; 0.06 for cell_3_contacted; 0.06 for cell_4_contacted; 0.06 for cell_5_contacted; 0.06 for cell_6_contacted; 0.06 for cell_7_contacted; 0.06 for cell_8_contacted; 0.06 for cell_9_contacted; 0.06 for cell_10_contacted; 0.06 for cell_11_contacted; 0.28 for preload_captured. Each goal requires all numeric predicates in SCORING.md and scene.json. Credit is recomputed, so dislodged components lose credit. Full score also requires all bodies <=0.01 m/s and <=0.2 rad/s, robot clearance >=0.02 m, continuously for 1.0 s; otherwise score is capped at 0.95. Invalid frames, lost parts, fixture motion, broken preservation constraints, joint-limit violations or penetration >0.002 m permanently score zero.

Each weighted goal requires every condition below. Position/quaternion conditions use measured simulator bodies; joint values use measured native coordinates. The scorer accepts any physically valid solution order. Historical thread and preservation checks encode physical constraints, not the expert phase index.

## cell_0_contacted (0.06)

- `cell_0` center within 0.001 m of (-0.125, -0.028, 0.03325), XYZW orientation (0, 0, 0, 1) within 3.14159 rad relative to holder.
- `cell_0` local axis (0, 0, 1) within 0.105 rad of (0, 0, 1) relative to holder.
- `contact_spring_0` in [-0.0018, -0.00035] (metres for prismatic, radians for rotary joints).
- `cell_0` linear speed <= 0.01 m/s and angular speed <= 0.2 rad/s.

## cell_1_contacted (0.06)

- `cell_1` center within 0.001 m of (-0.075, -0.028, 0.03455), XYZW orientation (1, 0, 0, 6.12323e-17) within 3.14159 rad relative to holder.
- `cell_1` local axis (0, 0, 1) within 0.105 rad of (0, 0, -1) relative to holder.
- `contact_spring_1` in [-0.0018, -0.00035] (metres for prismatic, radians for rotary joints).
- `cell_1` linear speed <= 0.01 m/s and angular speed <= 0.2 rad/s.

## cell_2_contacted (0.06)

- `cell_2` center within 0.001 m of (-0.025, -0.028, 0.03325), XYZW orientation (0, 0, 0, 1) within 3.14159 rad relative to holder.
- `cell_2` local axis (0, 0, 1) within 0.105 rad of (0, 0, 1) relative to holder.
- `contact_spring_2` in [-0.0018, -0.00035] (metres for prismatic, radians for rotary joints).
- `cell_2` linear speed <= 0.01 m/s and angular speed <= 0.2 rad/s.

## cell_3_contacted (0.06)

- `cell_3` center within 0.001 m of (0.025, -0.028, 0.03455), XYZW orientation (1, 0, 0, 6.12323e-17) within 3.14159 rad relative to holder.
- `cell_3` local axis (0, 0, 1) within 0.105 rad of (0, 0, -1) relative to holder.
- `contact_spring_3` in [-0.0018, -0.00035] (metres for prismatic, radians for rotary joints).
- `cell_3` linear speed <= 0.01 m/s and angular speed <= 0.2 rad/s.

## cell_4_contacted (0.06)

- `cell_4` center within 0.001 m of (0.075, -0.028, 0.03325), XYZW orientation (0, 0, 0, 1) within 3.14159 rad relative to holder.
- `cell_4` local axis (0, 0, 1) within 0.105 rad of (0, 0, 1) relative to holder.
- `contact_spring_4` in [-0.0018, -0.00035] (metres for prismatic, radians for rotary joints).
- `cell_4` linear speed <= 0.01 m/s and angular speed <= 0.2 rad/s.

## cell_5_contacted (0.06)

- `cell_5` center within 0.001 m of (0.125, -0.028, 0.03455), XYZW orientation (1, 0, 0, 6.12323e-17) within 3.14159 rad relative to holder.
- `cell_5` local axis (0, 0, 1) within 0.105 rad of (0, 0, -1) relative to holder.
- `contact_spring_5` in [-0.0018, -0.00035] (metres for prismatic, radians for rotary joints).
- `cell_5` linear speed <= 0.01 m/s and angular speed <= 0.2 rad/s.

## cell_6_contacted (0.06)

- `cell_6` center within 0.001 m of (-0.125, 0.028, 0.03325), XYZW orientation (0, 0, 0, 1) within 3.14159 rad relative to holder.
- `cell_6` local axis (0, 0, 1) within 0.105 rad of (0, 0, 1) relative to holder.
- `contact_spring_6` in [-0.0018, -0.00035] (metres for prismatic, radians for rotary joints).
- `cell_6` linear speed <= 0.01 m/s and angular speed <= 0.2 rad/s.

## cell_7_contacted (0.06)

- `cell_7` center within 0.001 m of (-0.075, 0.028, 0.03455), XYZW orientation (1, 0, 0, 6.12323e-17) within 3.14159 rad relative to holder.
- `cell_7` local axis (0, 0, 1) within 0.105 rad of (0, 0, -1) relative to holder.
- `contact_spring_7` in [-0.0018, -0.00035] (metres for prismatic, radians for rotary joints).
- `cell_7` linear speed <= 0.01 m/s and angular speed <= 0.2 rad/s.

## cell_8_contacted (0.06)

- `cell_8` center within 0.001 m of (-0.025, 0.028, 0.03325), XYZW orientation (0, 0, 0, 1) within 3.14159 rad relative to holder.
- `cell_8` local axis (0, 0, 1) within 0.105 rad of (0, 0, 1) relative to holder.
- `contact_spring_8` in [-0.0018, -0.00035] (metres for prismatic, radians for rotary joints).
- `cell_8` linear speed <= 0.01 m/s and angular speed <= 0.2 rad/s.

## cell_9_contacted (0.06)

- `cell_9` center within 0.001 m of (0.025, 0.028, 0.03455), XYZW orientation (1, 0, 0, 6.12323e-17) within 3.14159 rad relative to holder.
- `cell_9` local axis (0, 0, 1) within 0.105 rad of (0, 0, -1) relative to holder.
- `contact_spring_9` in [-0.0018, -0.00035] (metres for prismatic, radians for rotary joints).
- `cell_9` linear speed <= 0.01 m/s and angular speed <= 0.2 rad/s.

## cell_10_contacted (0.06)

- `cell_10` center within 0.001 m of (0.075, 0.028, 0.03325), XYZW orientation (0, 0, 0, 1) within 3.14159 rad relative to holder.
- `cell_10` local axis (0, 0, 1) within 0.105 rad of (0, 0, 1) relative to holder.
- `contact_spring_10` in [-0.0018, -0.00035] (metres for prismatic, radians for rotary joints).
- `cell_10` linear speed <= 0.01 m/s and angular speed <= 0.2 rad/s.

## cell_11_contacted (0.06)

- `cell_11` center within 0.001 m of (0.125, 0.028, 0.03455), XYZW orientation (1, 0, 0, 6.12323e-17) within 3.14159 rad relative to holder.
- `cell_11` local axis (0, 0, 1) within 0.105 rad of (0, 0, -1) relative to holder.
- `contact_spring_11` in [-0.0018, -0.00035] (metres for prismatic, radians for rotary joints).
- `cell_11` linear speed <= 0.01 m/s and angular speed <= 0.2 rad/s.

## preload_captured (0.28)

- `cell_0` center within 0.001 m of (-0.125, -0.028, 0.03325), XYZW orientation (0, 0, 0, 1) within 3.14159 rad relative to holder.
- `cell_0` local axis (0, 0, 1) within 0.105 rad of (0, 0, 1) relative to holder.
- `contact_spring_0` in [-0.0018, -0.00035] (metres for prismatic, radians for rotary joints).
- `cell_0` linear speed <= 0.01 m/s and angular speed <= 0.2 rad/s.
- `cell_1` center within 0.001 m of (-0.075, -0.028, 0.03455), XYZW orientation (1, 0, 0, 6.12323e-17) within 3.14159 rad relative to holder.
- `cell_1` local axis (0, 0, 1) within 0.105 rad of (0, 0, -1) relative to holder.
- `contact_spring_1` in [-0.0018, -0.00035] (metres for prismatic, radians for rotary joints).
- `cell_1` linear speed <= 0.01 m/s and angular speed <= 0.2 rad/s.
- `cell_2` center within 0.001 m of (-0.025, -0.028, 0.03325), XYZW orientation (0, 0, 0, 1) within 3.14159 rad relative to holder.
- `cell_2` local axis (0, 0, 1) within 0.105 rad of (0, 0, 1) relative to holder.
- `contact_spring_2` in [-0.0018, -0.00035] (metres for prismatic, radians for rotary joints).
- `cell_2` linear speed <= 0.01 m/s and angular speed <= 0.2 rad/s.
- `cell_3` center within 0.001 m of (0.025, -0.028, 0.03455), XYZW orientation (1, 0, 0, 6.12323e-17) within 3.14159 rad relative to holder.
- `cell_3` local axis (0, 0, 1) within 0.105 rad of (0, 0, -1) relative to holder.
- `contact_spring_3` in [-0.0018, -0.00035] (metres for prismatic, radians for rotary joints).
- `cell_3` linear speed <= 0.01 m/s and angular speed <= 0.2 rad/s.
- `cell_4` center within 0.001 m of (0.075, -0.028, 0.03325), XYZW orientation (0, 0, 0, 1) within 3.14159 rad relative to holder.
- `cell_4` local axis (0, 0, 1) within 0.105 rad of (0, 0, 1) relative to holder.
- `contact_spring_4` in [-0.0018, -0.00035] (metres for prismatic, radians for rotary joints).
- `cell_4` linear speed <= 0.01 m/s and angular speed <= 0.2 rad/s.
- `cell_5` center within 0.001 m of (0.125, -0.028, 0.03455), XYZW orientation (1, 0, 0, 6.12323e-17) within 3.14159 rad relative to holder.
- `cell_5` local axis (0, 0, 1) within 0.105 rad of (0, 0, -1) relative to holder.
- `contact_spring_5` in [-0.0018, -0.00035] (metres for prismatic, radians for rotary joints).
- `cell_5` linear speed <= 0.01 m/s and angular speed <= 0.2 rad/s.
- `cell_6` center within 0.001 m of (-0.125, 0.028, 0.03325), XYZW orientation (0, 0, 0, 1) within 3.14159 rad relative to holder.
- `cell_6` local axis (0, 0, 1) within 0.105 rad of (0, 0, 1) relative to holder.
- `contact_spring_6` in [-0.0018, -0.00035] (metres for prismatic, radians for rotary joints).
- `cell_6` linear speed <= 0.01 m/s and angular speed <= 0.2 rad/s.
- `cell_7` center within 0.001 m of (-0.075, 0.028, 0.03455), XYZW orientation (1, 0, 0, 6.12323e-17) within 3.14159 rad relative to holder.
- `cell_7` local axis (0, 0, 1) within 0.105 rad of (0, 0, -1) relative to holder.
- `contact_spring_7` in [-0.0018, -0.00035] (metres for prismatic, radians for rotary joints).
- `cell_7` linear speed <= 0.01 m/s and angular speed <= 0.2 rad/s.
- `cell_8` center within 0.001 m of (-0.025, 0.028, 0.03325), XYZW orientation (0, 0, 0, 1) within 3.14159 rad relative to holder.
- `cell_8` local axis (0, 0, 1) within 0.105 rad of (0, 0, 1) relative to holder.
- `contact_spring_8` in [-0.0018, -0.00035] (metres for prismatic, radians for rotary joints).
- `cell_8` linear speed <= 0.01 m/s and angular speed <= 0.2 rad/s.
- `cell_9` center within 0.001 m of (0.025, 0.028, 0.03455), XYZW orientation (1, 0, 0, 6.12323e-17) within 3.14159 rad relative to holder.
- `cell_9` local axis (0, 0, 1) within 0.105 rad of (0, 0, -1) relative to holder.
- `contact_spring_9` in [-0.0018, -0.00035] (metres for prismatic, radians for rotary joints).
- `cell_9` linear speed <= 0.01 m/s and angular speed <= 0.2 rad/s.
- `cell_10` center within 0.001 m of (0.075, 0.028, 0.03325), XYZW orientation (0, 0, 0, 1) within 3.14159 rad relative to holder.
- `cell_10` local axis (0, 0, 1) within 0.105 rad of (0, 0, 1) relative to holder.
- `contact_spring_10` in [-0.0018, -0.00035] (metres for prismatic, radians for rotary joints).
- `cell_10` linear speed <= 0.01 m/s and angular speed <= 0.2 rad/s.
- `cell_11` center within 0.001 m of (0.125, 0.028, 0.03455), XYZW orientation (1, 0, 0, 6.12323e-17) within 3.14159 rad relative to holder.
- `cell_11` local axis (0, 0, 1) within 0.105 rad of (0, 0, -1) relative to holder.
- `contact_spring_11` in [-0.0018, -0.00035] (metres for prismatic, radians for rotary joints).
- `cell_11` linear speed <= 0.01 m/s and angular speed <= 0.2 rad/s.
- `retaining_plate` center within 0.0008 m of (0, 0, 0.0635), XYZW orientation (0, 0, 0, 1) within 0.105 rad relative to holder.
- `capture_key` center within 0.001 m of (0, 0, 0.0732), XYZW orientation (0, 0, 0, 1) within 0.105 rad relative to holder.
- `retaining_plate` linear speed <= 0.01 m/s and angular speed <= 0.2 rad/s.
- `capture_key` linear speed <= 0.01 m/s and angular speed <= 0.2 rad/s.


Malformed/missing/nonfinite data and nonmonotonic conflicting timestamps fail closed. The same frame can be queried twice without double-counting time. Unobserved gaps reset the stability window. Off-table loss uses the lowest rotated collision-bound corner, 25 mm below the tabletop. Anchors may move at most 5 mm / 3 degrees. Joint tolerances are 10 mrad rotary or 0.5 mm prismatic beyond physical limits.

Thread credit requires aligned angular increments with corresponding axial motion inside the thread engagement region. Free spinning, direct dropping and pitch-inconsistent motion earn no turn credit. Cable continuity uses connected joint endpoints; a forced catch crossing without release invalidates the episode. These checks apply only to mechanisms present in this task.

Offline tests inject synthetic states to test arithmetic and counterexamples. Native probes separately read actual simulation states and call this same scorer. No synthetic score is a demonstration result.
