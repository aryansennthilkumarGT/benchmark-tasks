# Fit and pin a hinged collar around a captive shaft — scoring

0.25 for lower_half_located; 0.25 for collar_closed; 0.5 for collar_retained. Each goal requires all numeric predicates in SCORING.md and scene.json. Credit is recomputed, so dislodged components lose credit. Full score also requires all bodies <=0.01 m/s and <=0.2 rad/s, robot clearance >=0.02 m, continuously for 2.0 s; otherwise score is capped at 0.95. Invalid frames, lost parts, fixture motion, broken preservation constraints, joint-limit violations or penetration >0.002 m permanently score zero.

Each weighted goal requires every condition below. Position/quaternion conditions use measured simulator bodies; joint values use measured native coordinates. The scorer accepts any physically valid solution order. Historical thread and preservation checks encode physical constraints, not the expert phase index.

## lower_half_located (0.25)

- `lower_collar` radial distance from the captive shaft Y axis <= 0.0015 m and axial Y offset <= 0.0015 m, XYZW orientation (0, 0, 0, 1) within 0.105 rad relative to captive_shaft.
- `lower_collar` linear speed <= 0.01 m/s and angular speed <= 0.2 rad/s.

## collar_closed (0.25)

- `lower_collar` radial distance from the captive shaft Y axis <= 0.0015 m and axial Y offset <= 0.0015 m, XYZW orientation (0, 0, 0, 1) within 0.105 rad relative to captive_shaft.
- `collar_hinge` in [-0.025, 0.000001] (metres for prismatic, radians for rotary joints).

## collar_retained (0.5)

- `lower_collar` radial distance from the captive shaft Y axis <= 0.0015 m and axial Y offset <= 0.0015 m, XYZW orientation (0, 0, 0, 1) within 0.105 rad relative to captive_shaft.
- `collar_hinge` in [-0.025, 0.000001] (metres for prismatic, radians for rotary joints).
- `collar_key` center within 0.0015 m of (0.045, 0.006, 0), XYZW orientation (0, 0, 0, 1) within 0.105 rad relative to lower_collar.
- `collar_key` linear speed <= 0.01 m/s and angular speed <= 0.2 rad/s.
- `upper_collar` linear speed <= 0.01 m/s and angular speed <= 0.2 rad/s.


Malformed/missing/nonfinite data and nonmonotonic conflicting timestamps fail closed. The same frame can be queried twice without double-counting time. Unobserved gaps reset the stability window. Off-table loss uses the lowest rotated collision-bound corner, 25 mm below the tabletop. Anchors may move at most 5 mm / 3 degrees. Joint tolerances are 10 mrad rotary or 0.5 mm prismatic beyond physical limits.

Thread credit requires aligned angular increments with corresponding axial motion inside the thread engagement region. Free spinning, direct dropping and pitch-inconsistent motion earn no turn credit. Cable continuity uses connected joint endpoints; a forced catch crossing without release invalidates the episode. These checks apply only to mechanisms present in this task.

Offline tests inject synthetic states to test arithmetic and counterexamples. Native probes separately read actual simulation states and call this same scorer. No synthetic score is a demonstration result.

The one-microradian positive hinge margin covers the measured closed-stop residual of about 7.6e-10 radians. The opening bound remains -0.025 radians.

Radial fit and axial registration are measured independently around the shaft. The former combined sphere mixed the two and rejected a1.376mm radial fit with0.599mm axial offset. Each placement bound remains1.5mm. Orientation and key-retention predicates retain their existing values.

Stability is measured from consecutive 20 Hz full-body poses. Translational speed must remain at most 0.01 m/s and angular speed at most 0.2 rad/s for the existing two-second final hold. Missing or widely separated observations use raw simulator velocities and cannot establish an unobserved hold. Raw native velocities remain in the evidence. This definition follows observable pose motion after contact solver velocity noise interrupted holds while poses remained stationary. Fresh native validation is required.
