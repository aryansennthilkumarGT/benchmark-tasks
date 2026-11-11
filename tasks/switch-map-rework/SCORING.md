# Correct two latched patch connections while preserving a third — scoring

0.5 for link_0_correct; 0.5 for link_1_correct. Each goal requires all numeric predicates in SCORING.md and scene.json. Credit is recomputed, so dislodged components lose credit. Full score also requires all bodies <=0.01 m/s and <=0.2 rad/s, robot clearance >=0.02 m, continuously for 1.0 s; otherwise score is capped at 0.95. Invalid frames, lost parts, fixture motion, broken preservation constraints, joint-limit violations or penetration >0.002 m permanently score zero.

Each weighted goal requires every condition below. Position/quaternion conditions use measured simulator bodies; joint values use measured native coordinates. The scorer accepts any physically valid solution order. Historical thread and preservation checks encode physical constraints, not the expert phase index.

## link_0_correct (0.5)

- `plug_0` center within 0.0015 m of (0.2, -0.1, 0.7825), XYZW orientation (0, 0, 0, 1) within 0.10472 rad in world coordinates.
- `latch_slide_0` in [-0.0006, 0] (metres for prismatic, radians for rotary joints).
- `plug_0` linear speed <= 0.01 m/s and angular speed <= 0.2 rad/s.

## link_1_correct (0.5)

- `plug_1` center within 0.0015 m of (0.3, -0.1, 0.7825), XYZW orientation (0, 0, 0, 1) within 0.10472 rad in world coordinates.
- `latch_slide_1` in [-0.0006, 0] (metres for prismatic, radians for rotary joints).
- `plug_1` linear speed <= 0.01 m/s and angular speed <= 0.2 rad/s.

## Preservation constraints

The healthy plug can settle against its port guides at approximately 12° of roll. The preservation check includes 0.1° of angular allowance for that seated play. The 6 mm translation limit and latch engagement still apply.

- `healthy_link_disturbed`: `plug_2` center within 0.006 m of (0.4, -0.1, 0.7825), XYZW orientation (0, 0, 0, 1) within 12.1° in world coordinates; `latch_slide_2` in [-0.0008, 0] (metres for prismatic, radians for rotary joints).

Malformed/missing/nonfinite data and nonmonotonic conflicting timestamps fail closed. The same frame can be queried twice without double-counting time. Unobserved gaps reset the stability window. Off-table loss uses the lowest rotated collision-bound corner, 25 mm below the tabletop. Anchors may move at most 5 mm / 3 degrees. Joint tolerances are 10 mrad rotary or 0.5 mm prismatic beyond physical limits.

Thread credit requires aligned angular increments with corresponding axial motion inside the thread engagement region. Free spinning, direct dropping and pitch-inconsistent motion earn no turn credit. Cable continuity uses connected joint endpoints; a forced catch crossing without release invalidates the episode. These checks apply only to mechanisms present in this task.

Offline tests inject synthetic states to test arithmetic and counterexamples. Native probes separately read actual simulation states and call this same scorer. No synthetic score is a demonstration result.

Native release probes apply a finite 100 ms pull. A separate six-second unloaded settling probe checks finite, valid dynamics, penetration at most 2 mm and protected-link displacement at most 5 mm after that pull. Earlier three-second constant-load probes reached cable tension and produced nonfinite telemetry. Those failed reports remain diagnostic evidence. The unchanged robot controller must still demonstrate the complete withdrawal.
