# Observable geometry and score

Native telemetry reads actual poses/velocities, collision geometry and robot clearance. The scorer never uses controller phase names or writes object state.

Current geometric hook engagement earns 0.25: the declared groove-side point is within 1.2 mm of the cam edge with collet tilt in the valid 0.05–0.45 rad range. Upright supported preassembly earns 0.75 when its groove midplane is within 0.6 mm lateral/0.3 mm vertical of (0.24,0,0.8055), and axis tilt ≤0.025 rad. Collet yaw is irrelevant for its axisymmetric groove. Credit is recomputed from the current pose; moving out of the hook or seating region removes it. Success does not depend on matching the expert's exact angle, approach or phase history. A distinct −0.15 rad collision-free entry is tested in addition to the scripted −0.25 rad entry.

The first frame must show the specified initial collet position to 3 mm. Subsequent displacement above 2 m/s times elapsed time plus 10 mm latches an impossible state-jump failure. This permissive bound exceeds commanded motion substantially; it catches instantaneous final-state substitution without excluding physically valid entry paths. Deliberately initialized diagnostic probes do not establish a valid trial and cannot be demonstrations.

Full score requires the valid final groove pose, both grippers ≥20 mm clear, all parts ≤8 mm/s and ≤0.15 rad/s, continuously for 2 s. Gaps >1.5 control periods reset the hold. Moving a seated collet immediately removes seating/success credit.

Missing/extra bodies/joints, nonfinite values, non-unit quaternions, conflicting/nonmonotonic frames, part loss below z=0.7275, anchor motion >1 mm or 0.025 rad and inter-part penetration >0.35 mm permanently score zero. Exact duplicate frames are idempotent. No nut/collet collision pair is excluded.

Physical checking uses a marked cam side, witness video and angle/height gauges for the hook/pivot path, calipers for final groove alignment, and a ruler/video for clear unsupported-by-gripper stability. The part rests on the documented pads; no test of unsupported cam retention, torque or pull-out strength is implied. Video plus simple measurements reproduce the observed geometric success conditions.
