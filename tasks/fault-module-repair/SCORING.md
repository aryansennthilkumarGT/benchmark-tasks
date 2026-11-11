# Counterweighted service-arm scoring

The aligned-weight group contributes 0.3 when the slider lies between -32 and -30 mm and the counterweight's speed is at most 0.01 m/s with spin at most 0.2 rad/s.

The pinned-weight group contributes another 0.3 when alignment is maintained and the pin centre is within 1.5 mm of arm-relative (-66,0,-4) mm. Its orientation must differ from the arm by at most 0.105 radians. Pin speed limits are 0.01 m/s and 0.2 rad/s.

The balanced-arm group contributes 0.4 when the aligned weight and seated pin remain valid, the unpowered pivot is between -0.04 and +0.04 radians, and the arm meets the same speed limits. Credit is recomputed from each native state. Lost progress removes its credit.

Full success requires every group, speeds below 0.01 m/s and 0.2 rad/s for all bodies, and robot clearance at least 20 mm continuously for 3 seconds. Until that release and stability condition holds, the maximum score is 0.95.

A body falling more than 25 mm below the table loss plane invalidates the trial. Fixture motion over 5 mm or 3 degrees, prohibited penetration over 2 mm, and joint-limit excess over 10 mrad rotary or 0.5 mm prismatic also invalidate it. Invalid or conflicting frame/time data yield zero. Unobserved time gaps reset the stability window.

Offline adversarial states test the arithmetic. Native fixture tests establish gravity response and the difference between pinned and unpinned retention under load. Genuine expert and model records replay through this same scorer.
