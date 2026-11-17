# ODRI collision root cause

**Original support/base collision confirmed. The support orientation can be corrected geometrically; no complete manipulation is established.**

## What actually intersects

- All eight old layouts use one of two right-hand support configurations. Both contain stock `tip_right:5` and `tip_right:8` hull vertices inside the analytic source STEP base.
- Registered mesh/STEP bounding discrepancy: **1e-10 m**. The original +160 mm leg registration, foot rotation and millimetre/metre conversion agree; no placement-transform fix removes this intersection.
- `tip_right:5` strict witness: point [12.341850312382107, -0.2972912994547161, 13.531927043436642] mm is **1.071916 mm** from the nearest analytic STEP boundary while inside material.
- `tip_right:8` strict witness: point [11.366047771781629, 7.4967955218982505, 15.803478682438477] mm is **0.003204 mm** from the nearest analytic STEP boundary while inside material.

The independent FK perturbation shows that opening the original support fingers moves them along **world Z**, parallel to the leg stem. The former rotation therefore places the upper finger into the stem. The gripper closes along its actual local X direction. A fingertip/base collision is not legitimate foot-rim contact and is never exempted. FCL triangle-contact depths are diagnostic, not a calibrated hardware penetration measurement.

## Bounded alternatives

Tested **32** templates: two existing placements × axial shifts −3/−6 mm × eight rolls. All 315 hulls per arm, both arms, direct-URDF nonadjacent self pairs, known source base/open foot/parked fork, pin/PCB envelopes, table, proximal support, tool rest and unheld tool are included. No sibling-finger exemption is used. Ready self-collision audit: `[]`.

|Placement,m|Shift,mm|Roll,deg|First blocking stage|First identified cause|
|---|---:|---:|---|---|
|[0.43, 0.0, 0.98]|-3|0|support_precontact|[['right', 'tip_right', 'tip_right:5', 'lower_leg_structure_base.STL']]|
|[0.43, 0.0, 0.98]|-3|45|support_precontact|[['right', 'tip_right', 'tip_right:8', 'lower_leg_structure_base.STL']]|
|[0.43, 0.0, 0.98]|-3|90|finite samples clear only|no sampled known-solid/self/interarm collision; purchase unproved|
|[0.43, 0.0, 0.98]|-3|135|support_precontact|[['right', 'tip_left', 'tip_left:15', 'lower_leg_structure_base.STL']]|
|[0.43, 0.0, 0.98]|-3|180|support_precontact|[['right', 'tip_left', 'tip_left:14', 'lower_leg_structure_base.STL']]|
|[0.43, 0.0, 0.98]|-3|225|support_approach_IK|IK UNRESOLVED; not physical impossibility|
|[0.43, 0.0, 0.98]|-3|270|support_approach_IK|IK UNRESOLVED; not physical impossibility|
|[0.43, 0.0, 0.98]|-3|315|support_approach_IK|IK UNRESOLVED; not physical impossibility|
|[0.43, 0.0, 0.98]|-6|0|support_precontact|[['right', 'tip_right', 'tip_right:5', 'lower_leg_structure_base.STL']]|
|[0.43, 0.0, 0.98]|-6|45|support_precontact|[['right', 'tip_right', 'tip_right:8', 'lower_leg_structure_base.STL']]|
|[0.43, 0.0, 0.98]|-6|90|finite samples clear only|no sampled known-solid/self/interarm collision; purchase unproved|
|[0.43, 0.0, 0.98]|-6|135|support_precontact|[['right', 'tip_left', 'tip_left:15', 'lower_leg_structure_base.STL']]|
|[0.43, 0.0, 0.98]|-6|180|support_precontact|[['right', 'tip_left', 'tip_left:14', 'lower_leg_structure_base.STL']]|
|[0.43, 0.0, 0.98]|-6|225|support_approach_IK|IK UNRESOLVED; not physical impossibility|
|[0.43, 0.0, 0.98]|-6|270|support_approach_IK|IK UNRESOLVED; not physical impossibility|
|[0.43, 0.0, 0.98]|-6|315|support_approach_IK|IK UNRESOLVED; not physical impossibility|
|[0.48, -0.03, 1.03]|-3|0|support_precontact|[['right', 'tip_right', 'tip_right:5', 'lower_leg_structure_base.STL']]|
|[0.48, -0.03, 1.03]|-3|45|support_precontact|[['right', 'tip_right', 'tip_right:8', 'lower_leg_structure_base.STL']]|
|[0.48, -0.03, 1.03]|-3|90|finite samples clear only|no sampled known-solid/self/interarm collision; purchase unproved|
|[0.48, -0.03, 1.03]|-3|135|support_precontact|[['right', 'tip_left', 'tip_left:15', 'lower_leg_structure_base.STL']]|
|[0.48, -0.03, 1.03]|-3|180|support_precontact|[['right', 'tip_left', 'tip_left:14', 'lower_leg_structure_base.STL']]|
|[0.48, -0.03, 1.03]|-3|225|support_approach_IK|IK UNRESOLVED; not physical impossibility|
|[0.48, -0.03, 1.03]|-3|270|support_approach_IK|IK UNRESOLVED; not physical impossibility|
|[0.48, -0.03, 1.03]|-3|315|support_approach_IK|IK UNRESOLVED; not physical impossibility|
|[0.48, -0.03, 1.03]|-6|0|support_precontact|[['right', 'tip_right', 'tip_right:5', 'lower_leg_structure_base.STL']]|
|[0.48, -0.03, 1.03]|-6|45|support_precontact|[['right', 'tip_right', 'tip_right:8', 'lower_leg_structure_base.STL']]|
|[0.48, -0.03, 1.03]|-6|90|finite samples clear only|no sampled known-solid/self/interarm collision; purchase unproved|
|[0.48, -0.03, 1.03]|-6|135|support_precontact|[['right', 'tip_left', 'tip_left:15', 'lower_leg_structure_base.STL']]|
|[0.48, -0.03, 1.03]|-6|180|support_precontact|[['right', 'tip_left', 'tip_left:14', 'lower_leg_structure_base.STL']]|
|[0.48, -0.03, 1.03]|-6|225|support_approach_IK|IK UNRESOLVED; not physical impossibility|
|[0.48, -0.03, 1.03]|-6|270|support_approach_IK|IK UNRESOLVED; not physical impossibility|
|[0.48, -0.03, 1.03]|-6|315|support_approach_IK|IK UNRESOLVED; not physical impossibility|

Counts: `{'support_precontact': 16, 'finite_support_samples_clear': 4, 'support_approach_IK': 12}`. The four roll 90° alternatives remove the original base collision and have clear finite support-approach/close/open/withdraw samples. These are **not loaded grasps or continuous certificates**. Repeated segment endpoints are sample visits, not independent trials.

## Acquisition and working-tool obstruction

The 27 mm nominal setting leaves a small gap to the bare plastic foot. Closing further gives these first geometric contacts:
- Shift -3 mm at [0.43, 0.0, 0.98]: first contact bracket **26.937744–26.937866 mm jaw setting**, pairs `[['right', 'tip_left', 'tip_left:14', 'foot_structure.STL']]`.
- Shift -6 mm at [0.43, 0.0, 0.98]: first contact bracket **26.937744–26.937866 mm jaw setting**, pairs `[['right', 'tip_left', 'tip_left:14', 'foot_structure.STL']]`.
- Shift -3 mm at [0.48, -0.03, 1.03]: first contact bracket **26.937744–26.937866 mm jaw setting**, pairs `[['right', 'tip_left', 'tip_left:14', 'foot_structure.STL']]`.
- Shift -6 mm at [0.48, -0.03, 1.03]: first contact bracket **26.937744–26.937866 mm jaw setting**, pairs `[['right', 'tip_left', 'tip_left:14', 'foot_structure.STL']]`.

This is contact detection, not force closure, frictional holding or proof that both fingers carry the load. The displayed digits describe collision-search resolution, not as-built manufacturing accuracy. The original source drawing/README also show a bonded 65×10 mm tire segment. Its loaded contact profile is not in the three plastic STEP parts. The published eDrawings viewer was acquired, but its embedded geometry was not decoded in this bounded pass. No tire thickness was fabricated. A bare-plastic clearance cannot certify an assembled-foot purchase.

For each of the four conditional support configurations:
- At [0.43, 0.0, 0.98], shift -3 mm: first acquisition blocker **tool_pregrasp: IK not solved**. Independently, the placement wrist IK solves, but the required two-arm configuration collides at `['gripper', 'gripper:0', 'link3', 'link3:1']`; tool/support pairs `[['tweezer-handle', 'support-arm', 'gripper', 'gripper:0'], ['tweezer-branch0', 'support-arm', 'gripper', 'gripper:0'], ['tweezer-branch1', 'support-arm', 'gripper', 'gripper:0']]`.
- At [0.43, 0.0, 0.98], shift -6 mm: first acquisition blocker **tool_pregrasp: IK not solved**. Independently, the placement wrist IK solves, but the required two-arm configuration collides at `['gripper', 'gripper:0', 'link3', 'link3:1']`; tool/support pairs `[['tweezer-handle', 'support-arm', 'gripper', 'gripper:0'], ['tweezer-branch0', 'support-arm', 'gripper', 'gripper:0'], ['tweezer-branch1', 'support-arm', 'gripper', 'gripper:0']]`.
- At [0.48, -0.03, 1.03], shift -3 mm: first acquisition blocker **tool_pregrasp: IK not solved**. Independently, the placement wrist IK solves, but the required two-arm configuration collides at `['gripper', 'gripper:0', 'link3', 'link3:1']`; tool/support pairs `[['tweezer-handle', 'support-arm', 'gripper', 'gripper:0'], ['tweezer-branch0', 'support-arm', 'gripper', 'gripper:0'], ['tweezer-branch1', 'support-arm', 'gripper', 'gripper:0']]`.
- At [0.48, -0.03, 1.03], shift -6 mm: first acquisition blocker **tool_pregrasp: IK not solved**. Independently, the placement wrist IK solves, but the required two-arm configuration collides at `['gripper', 'gripper:0', 'link3', 'link3:1']`; tool/support pairs `[['tweezer-handle', 'support-arm', 'gripper', 'gripper:0'], ['tweezer-branch0', 'support-arm', 'gripper', 'gripper:0'], ['tweezer-branch1', 'support-arm', 'gripper', 'gripper:0']]`.

The working gripper/right-forearm counterexample remains even if tool purchase is optimistically assumed. The counterexample is a posed configuration used to reject a plan, not a carried-object attachment or physical manipulation. Alternative IK branches, grips or sourced tools may behave differently; these tests do not prove global ODRI impossibility.

The connected generic tweezer envelope has 142.5 mm end-to-end length and 120 mm handle-center-to-tip offset. It is an ordinary-tool hypothesis, not manufacturer CAD or validated spring/purchase geometry. Original source obstructions were not removed to obtain a pass. The tread and exact electronics/retention geometry remain input gates to any complete scene.

**PARK ODRI for this implementation queue.** Tool purchase, one-annulus insertion, released retention and installed-annulus withdrawal were not executed. No silicone calculation was rerun.
