# Replace opposed-polarity cells under a spring-return service cover — scoring

0.2 for old_cell_0_collected; 0.2 for old_cell_1_collected; 0.2 for new_cell_0_installed; 0.2 for new_cell_1_installed; 0.2 for cover_closed. Each goal requires all numeric predicates in SCORING.md and scene.json. Credit is recomputed, so dislodged components lose credit. Full score also requires all bodies <=0.01 m/s and <=0.2 rad/s, robot clearance >=0.02 m, continuously for 1.0 s; otherwise score is capped at 0.95. Invalid frames, lost parts, fixture motion, broken preservation constraints, joint-limit violations or penetration >0.002 m permanently score zero.

Each weighted goal requires every condition below. Position/quaternion conditions use measured simulator bodies; joint values use measured native coordinates. The scorer accepts any physically valid solution order. Historical thread and preservation checks encode physical constraints, not the expert phase index.

## old_cell_0_collected (0.2)

- Entire oriented collision bound of `old_cell_0` inside (0.323, -0.287, 0.7533) to (0.457, -0.193, 0.8275) in world coordinates.
- `old_cell_0` linear speed <= 0.01 m/s and angular speed <= 0.2 rad/s.

## old_cell_1_collected (0.2)

- Entire oriented collision bound of `old_cell_1` inside (0.323, -0.287, 0.7533) to (0.457, -0.193, 0.8275) in world coordinates.
- `old_cell_1` linear speed <= 0.01 m/s and angular speed <= 0.2 rad/s.

## new_cell_0_installed (0.2)

- `new_cell_0` center within 0.001 m of (0, -0.033, 0.01525), XYZW orientation (0, 0, 0, 1) within 3.14159 rad relative to controller.
- `new_cell_0` local axis (1, 0, 0) within 0.105 rad of (1, 0, 0) relative to controller.
- `spring_0` in [-0.0016, -0.00025] (metres for prismatic, radians for rotary joints).
- `new_cell_0` linear speed <= 0.01 m/s and angular speed <= 0.2 rad/s.

## new_cell_1_installed (0.2)

- `new_cell_1` center within 0.001 m of (0, 0.033, 0.01525), XYZW orientation (0, 0, 0, 1) within 3.14159 rad relative to controller.
- `new_cell_1` local axis (1, 0, 0) within 0.105 rad of (-1, 0, 0) relative to controller.
- `spring_1` in [0.00025, 0.0016] (metres for prismatic, radians for rotary joints).
- `new_cell_1` linear speed <= 0.01 m/s and angular speed <= 0.2 rad/s.

## cover_closed (0.2)

- Entire oriented collision bound of `old_cell_0` inside (0.323, -0.287, 0.7533) to (0.457, -0.193, 0.8275) in world coordinates.
- `old_cell_0` linear speed <= 0.01 m/s and angular speed <= 0.2 rad/s.
- Entire oriented collision bound of `old_cell_1` inside (0.323, -0.287, 0.7533) to (0.457, -0.193, 0.8275) in world coordinates.
- `old_cell_1` linear speed <= 0.01 m/s and angular speed <= 0.2 rad/s.
- `new_cell_0` center within 0.001 m of (0, -0.033, 0.01525), XYZW orientation (0, 0, 0, 1) within 3.14159 rad relative to controller.
- `new_cell_0` local axis (1, 0, 0) within 0.105 rad of (1, 0, 0) relative to controller.
- `spring_0` in [-0.0016, -0.00025] (metres for prismatic, radians for rotary joints).
- `new_cell_0` linear speed <= 0.01 m/s and angular speed <= 0.2 rad/s.
- `new_cell_1` center within 0.001 m of (0, 0.033, 0.01525), XYZW orientation (0, 0, 0, 1) within 3.14159 rad relative to controller.
- `new_cell_1` local axis (1, 0, 0) within 0.105 rad of (-1, 0, 0) relative to controller.
- `spring_1` in [0.00025, 0.0016] (metres for prismatic, radians for rotary joints).
- `new_cell_1` linear speed <= 0.01 m/s and angular speed <= 0.2 rad/s.
- `cover_slide` in [0, 0.002] (metres for prismatic, radians for rotary joints).


Malformed/missing/nonfinite data and nonmonotonic conflicting timestamps fail closed. The same frame can be queried twice without double-counting time. Unobserved gaps reset the stability window. Off-table loss uses the lowest rotated collision-bound corner, 25 mm below the tabletop. Anchors may move at most 5 mm / 3 degrees. Joint tolerances are 10 mrad rotary or 0.5 mm prismatic beyond physical limits.

Thread credit requires aligned angular increments with corresponding axial motion inside the thread engagement region. Free spinning, direct dropping and pitch-inconsistent motion earn no turn credit. Cable continuity uses connected joint endpoints; a forced catch crossing without release invalidates the episode. These checks apply only to mechanisms present in this task.

Offline tests inject synthetic states to test arithmetic and counterexamples. Native probes separately read actual simulation states and call this same scorer. No synthetic score is a demonstration result.

Interchangeable parts are matched one-to-one to valid slots. The body names in slot predicates are templates: any listed candidate may satisfy that slot, and dependent closure/preload goals reuse the same matching. Polarity, contact-spring compression and measured turn history remain mandatory. A single part cannot earn two slot credits; changing studs resets its thread history. The expert uses one convenient assignment, which is not required by scoring.

Collection-region containment uses the exact support extent of each cylindrical collision shape, including the positive terminal button. For a cylinder with unit axis component a, half-height h and radius r, its extent on that coordinate is |a|h + r sqrt(1 − a²). This makes containment invariant to axial roll while detecting actual tilted or protruding material. Native tray retention initially exposed a false floor intersection from rotating the cell’s enclosing rectangular box. Numerical collection-region boundaries and stillness criteria are unchanged.
