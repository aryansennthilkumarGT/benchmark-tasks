# Observable mechanical endpoint and negative controls

**Proposed endpoint:** the manufacturer-defined calibration-ready mechanical posture, with both P1 sites and both J8 datums seated, the actual integral body lock retained, required fasteners secure, and the assembly stable after both hands release. This is not encoder zero writing. No hidden completion bit or source-CAD position alone substitutes for the physical interfaces.

## Ordinary physical inspection to bind

| Condition | Potential real observation | Remaining bound needed |
|---|---|---|
| P1 at each cylindrical datum | Inspect intended bottom/contact region and both axial seat ends; accessible feeler/profile checks against the actual pipe/seat | Registered target region, accessible views and a justified gap/measurement resolution. Overall minimum distance is inadequate. |
| J8 flat datum at each site | View or gauge the intended mating flat at multiple locations while the other established datums remain seated | Correct whole-assembly mapping and allowable flatness/gap. Candidate source planes/holes exist but target chain configuration is not validated. |
| Rear body datum and lock | Inspect actual rear mating surface and hook engagement; verify the body remains retained after hands/tool leave | Actual insertion/ready state and a justified benign retained-state check. No invented force threshold or generic plunger. |
| Correct fastening | Confirm actual specified screws/heads, engagement and source-appropriate securing check | Drive form, thread engagement and securing/preload method; no torque value was supplied. A flush head alone cannot distinguish all loose-fastener states. |
| Both sides ready | Separate checklist for each actual interface, with earlier contacts preserved through the other-side operation | Registered complete posture, not two independent decorative poses. |
| Stable released structure | Hands and any tool physically withdraw; observe assembly relative to jig from fixed views | Justified observation duration/resolution. No welded articulated KER or invisible actuator may hold the target posture. |
| No excessive deformation/damage | Compare loaded/unloaded fixture/body profile; inspect cracks and permanent set using appropriate views/reference measurements | Jig material/print properties and allowed elastic travel/set. Rigid CAD overlap does not predict damage. |

Manufacturer nominal CAD contact is an exact target **geometry**, not an allowable tolerance. No±0.2mm/±1degree/hold-time value is copied from another task. A defensible measurement procedure may later establish finite resolution/acceptance bands; it was not physically calibrated here. This is therefore not a completed reproducible full-task scorer.

## Distinct negative states

| Counterexample required | Required interpretation | Executed this pass? |
|---|---|---|
| Apparently seated but misaligned | At least one specific datum/contact fails even if another surface touches | **Static P1 geometry examples only.** Other full-assembly states not executed. |
| One loose J8 fastener | Mechanical readiness fails despite plausible head pose | No. Thread/load-bearing assembly state unbound. |
| Body lock not engaged | Body supported by hand or merely adjacent to hook is incomplete | No. No invented latch-state test. |
| Only one side complete | Partial mechanical preparation, never full completion | No full articulated assembly trial. |
| Robot-supported final state | No completion while the robot supplies required retention/support | No loaded physical/simulated release trial. |
| Excessive jig deformation/damage | Destructive retention is not valid preparation | No compliant/contact damage model was run. |

## What the executed CAD diagnostics actually show

[CAD_CONTACT_DIAGNOSTICS.json](results/CAD_CONTACT_DIAGNOSTICS.json) uses the actual source pipe, full jig solid and exact surfaces, not a goal-radius trigger. The unshifted negative-X overlay has0mm³ solid interference and1130.973355mm² coincident cylindrical surface. The1mm raised layout still has effectively zero overall distance elsewhere but **0mm²** common cylindrical patch. A60mm axial shift retains471.238898mm²;1mm lateral interference produces495.579700mm³ incompatible rigid overlap;120mm axial shift is23.5mm away.

These demonstrate that proximity/touching or partial contact can give false seating observations. They are **static geometric counterexamples**, not causal engagement/deformation/release experiments. Source surfaces are nominally coincident, so their shared area is not a pressure distribution or measured bearing area. The selected perturbations are not OEM tolerance limits. An overlap is not a force or damage estimate. Every output explicitly sets `force_or_retention_or_task_success_assessed=false`.

No body lock opened on proximity, no object was teleported inside a physics trial, no fastener flag was asserted as physical engagement, and no simulated success was generated. Future causal controls must operate through actual contact and compliant geometry after the missing registered articulated state is resolved.
