# Observable score and invalid states

The scorer reads actual body poses/velocities, normalized quaternions, sampled robot clearance and compound-shape penetration. It never sets states or consumes controller phase names. Native frames come from the pinned Arena adapter; synthetic fixtures are only unit tests.

Carrier credit is 0.25 when all three slot reference centres match distinct actual stud axes under a one-to-one assignment, within 0.65 mm lateral, the carrier origin is within 0.30 mm of z=0.8215 m and tilt is ≤0.025 rad. The complete carrier is C3 symmetric, so 120° rotations are equivalent.

Each separate retainer is worth 0.25 on a different stud. Its axis must remain within 0.65 mm and 0.025 rad; top must be flush with the corresponding tip to 0.30 mm. Clockwise rotation and 3 mm/turn descent must follow one continuous engagement history, with ≥3.85 turns and ≤0.30 mm cumulative axial error. An absolute helical phase datum additionally limits phase error to 0.35 rad (~0.167 mm axial equivalent). Different retainers cannot reuse one another's histories. Changing sites, leaving engagement or departing the helix resets credit. Free spinning followed by dropping to final height earns no retainer credit. Untightening or moving a seated part immediately removes its credit.

Until all conditions hold, score is capped at 0.95. Full score requires all parts' speed ≤8 mm/s, spin ≤0.15 rad/s and actual robot collision geometry ≥20 mm from dynamic parts continuously for 2 s. Gaps longer than 1.5 control periods reset the hold timer. Historical thread credit alone cannot preserve final success after disturbance.

Missing/extra bodies, invalid numeric values, non-unit quaternions, conflicting/nonmonotonic frames, >0.35 mm inter-part penetration, any anchor translation >1 mm or rotation >0.025 rad, and a dynamic part below z=0.7275 m latch zero for the trial. Retainer yaw steps >0.75 rad per observation are rejected as undersampled. The adapter computes penetration from the complete collision shapes; no mating pair is excluded. A duplicate identical timestamp/frame is idempotent.

Physical checking uses a caliper/height gauge for carrier seating and top-to-tip flush, axis/tilt gauges, witness-mark video for clockwise turns and continuous descent, video of release, and a ruler for 20 mm clearance. Reconstructed hidden simulator attributes or nonphysical counters do not award credit. The upstream disc/dowel setup is inspected before the trial; diaphragm compression and tightening torque are not success criteria.
