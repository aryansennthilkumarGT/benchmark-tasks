# Observable geometry and score

Native telemetry reads actual poses/velocities, collision geometry and robot clearance. The scorer never uses controller phase names or writes object state.

Correct hook engagement (0.25) requires the groove origin within 1 mm of the declared negative-X pivot pose and the tilted collet axis within 0.06 rad of the −0.25 rad entry axis. The pose derives from rocking about (−15.6,0,0) mm relative to the nut. Upright supported preassembly adds 0.50 when groove midplane is within 0.6 mm lateral/0.3 mm vertical of (0.24,0,0.8055), and axis tilt ≤0.025 rad. Collet yaw is irrelevant for its axisymmetric groove. Leaving a 8 mm neighborhood removes engagement credit. An unobserved final pose alone earns zero.

Full score requires the valid engagement and final pose, both grippers ≥20 mm clear, all parts ≤8 mm/s and ≤0.15 rad/s, continuously for 2 s. Gaps >1.5 control periods reset the hold. Moving a seated collet immediately removes seating/success credit.

Missing/extra bodies/joints, nonfinite values, non-unit quaternions, conflicting/nonmonotonic frames, part loss below z=0.7275, anchor motion >1 mm or 0.025 rad and inter-part penetration >0.35 mm permanently score zero. Exact duplicate frames are idempotent. No nut/collet collision pair is excluded.

Physical checking uses a marked cam side, witness video and angle/height gauges for the hook/pivot path, calipers for final groove alignment, and a ruler/video for clear unsupported-by-gripper stability. The part rests on the documented pads; no test of unsupported cam retention, torque or pull-out strength is implied. Video plus simple measurements reproduce the observed geometric success conditions.
