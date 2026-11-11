# Objective scoring

Each of twelve seated-contact groups contributes 0.04, for 0.48 total. A group requires a cell within 1 mm of its specified holder-relative centre, its longitudinal axis within 0.105 radians of the specified polarity, contact-spring compression between 0.35 and 1.8 mm, speed at most 0.01 m/s and spin at most 0.2 rad/s. The pressure plate must also be within 0.8 mm and 0.105 radians of its specified seated pose. Identical cells are matched one-to-one to eligible positions.

The retaining-key group contributes 0.52. It requires all twelve seated-contact groups, the plate's seated pose, and the key within 1 mm and 0.105 radians of its specified captured pose. Plate and key speed limits are 0.01 m/s and 0.2 rad/s. Full success requires the complete state for 3 seconds with robot clearance at least 20 mm.

The initial plate and key are separate from the loaded holder, yielding score 0. A seated plate with all twelve contacts and an absent key yields 0.48. Partial contact states receive 0.04 per valid group. A key-looking pose with missing contact groups cannot receive the capture credit.

Fixture movement over 5 mm or 3 degrees, a body falling over 25 mm below the tabletop loss plane, or prohibited interpenetration over 2 mm invalidates the trial and yields 0. Frame schema, timing and finite-state checks also apply. Exact target poses, limits and dependencies are listed in `scene.json`.

The scorer reads native measured poses and joint states. The expert uses the normal robot action interface. Controlled physics fixtures are separate from demonstrations.

For the cylindrical cells, angular stability is the rate of change of their longitudinal axis between consecutive20Hz pose observations, at most0.2rad/s. Axial spin leaves the collision geometry and terminal polarity unchanged. Centre speed remains at most0.01m/s. Other bodies use their native angular velocity. An absent or oversized observation interval uses the measured transverse angular velocity and resets the full-score hold. All full-score conditions, including robot withdrawal, must hold for1s. Native linear/angular velocities remain in the raw evidence.
