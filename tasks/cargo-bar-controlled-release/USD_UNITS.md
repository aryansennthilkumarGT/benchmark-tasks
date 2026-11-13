# USD angular drive repair

Primary API reference: https://openusd.org/release/api/class_usd_physics_drive_a_p_i.html. Angular DriveAPI stiffness and damping are expressed per degree. Authored scene values and Isaac implicit actuator values are SI per radian. Exported angular coefficients therefore divide by180/pi; angular positions and limits multiply by180/pi. Linear quantities are unchanged. Four rotational dampers and the two pawl springs are corrected in the original USD. No geometry, mass, contact, scene parameter, controller, scorer or native SI actuator value changes.

The original validated2f82123 branch and its evidence are preserved. This successor requires new actual USD-attribute tests and clean HTTPS reproduction. Unchanged scene/controller/MuJoCo source may retain its exact-source historical CPU evidence only through explicit file equivalence, without claiming it re-ran or establishes Isaac success. Native physics and YAM robot validation remain unrun.
