# Executed CPU results

**ODRI local contact coupon: nominal PASS. Full implementation: NO.** These are restricted planar, quasistatic simulation results, not measured hardware or a completed robot assembly.

## Source/earliest gates

- CELLO raw L2/L3 solid overlap: **2929.269181 mm³**.
- CELLO raw L2/L4 solid overlap: **4143.921735 mm³**.
- CELLO raw L3/L4 solid overlap: **5761.847381 mm³**.
- CELLO raw L4/L6 solid overlap: **1223.158925 mm³**.
- CELLO gravity torque/sag/friction window: **NOT ESTABLISHED**; full chain registration/mass/stiction were not resolved. No nine-control brake suite was run.
- Chefman: original squeeze/prong/cuff instruction reread; researcher asset audited; genuine cuff section/wire force remains unknown. No YAM or contact/lift success claimed.

## Source-CAD ODRI mechanism

- Registered foot versus lower_leg_structure_base.STEP: **0.000000000 mm³** initial solid overlap.
- Registered foot versus lower_leg_structure_fork.STEP: **0.000000000 mm³** initial solid overlap.
- Beam-gradient independent finite-difference error: **1.36e-10 N**; rigid translation/rotation energy errors below 1e-10 N·mm.
- Maximum sampled signed-distance interpolation error: **0.010570 mm**, over 3000 points/body/bank. Tessellation/2D approximation error is separate.
- Source pin-center lateral clearance: **0.400000 mm**; actual pin/slot contact is included. Pin-omitted results are not canonical.

## Free-foot positive test

- Designer-reported moving assembly approximately 10 g: 9 g body plus 1 g over 12 tube elements. Initial own-weight center **[-6.897032059578824e-05, -0.11718245493221793] mm**, norm **0.117182 mm**.
- Three 1 N probe displacements from own-weight equilibrium: **[0.6710927269606561, 0.42357257855042213, 0.4234686717090556] mm**.
- Return errors after removing probes: **[0.0031793322662225358, 0.005923492713399321, 3.808150451788312e-05] mm**.
- Maximum lateral foot-center travel **0.418231 mm**; maximum pin normal reaction **0.364611 N**.
- Worst equilibrium residual **1.90555e-05 N**; worst contact penetration **0.018231 mm**. No numerical domain boundary supports the positive case.
- Full STEP pose checks also find zero foot/leg-half solid overlap at all seven nominal cycle positions. Small loaded pin intersections from the declared penalty-contact model are recorded separately in POSE_AUDIT.json; they are not treated as hard-solid compatibility.
- The foot displacement and all ring nodes are solved from energy/contact balance. Only gravity/probe forces are supplied. No installed flag, neutral-position spring, attachment latch or commanded foot pose is used.

## Executed wrong cases

|Case|Physical local score|Numerical audit|Main failed physical predicates|
|---|---:|---|---|
|missing_all|0|invalid/unresolved|twelve_source_size_elements, all_in_contact_band, own_weight_centering, finite_reversible_travel|
|missing_one|0|resolved|twelve_source_size_elements|
|missing_bank|0|resolved|twelve_source_size_elements|
|misplaced_element|0|resolved|all_in_contact_band, own_weight_centering|
|wrong_size|0|resolved|twelve_source_size_elements, finite_reversible_travel|
|too_soft|0|invalid/unresolved|finite_reversible_travel, passive_return|
|stiff_wrong_material|0|invalid/unresolved|finite_reversible_travel|
|missing_support_ring|0|invalid/unresolved|own_weight_centering, finite_reversible_travel, passive_return|

All eight wrong cases reject full local credit. **Missing one ring and missing one bank can still move and return**; their full-grade rejection depends on actual inventory, not fabricated loss of function. This is why an eventual closed-device inspection method is required.

Escaped numerical-domain cases and excessive-contact/stiffness cases are invalid-model diagnostics, not accurate hard-stop positions, measured force thresholds or physical hardware disqualifications. Damage and time-dependent return are not modeled.

## Material uncertainty

- Authored E=0.5 MPa: physical score 1; numerical audit {'equilibrium_resolved': True, 'contact_resolved': True, 'no_numerical_stop': True, 'passed': True}; full local experiment PASS; 1 N displacement [1.1623463894232586] mm; return [0.005496584565324389] mm.
- Authored E=2.0 MPa: physical score 1; numerical audit {'equilibrium_resolved': True, 'contact_resolved': True, 'no_numerical_stop': True, 'passed': True}; full local experiment PASS; 1 N displacement [0.20361069035577672] mm; return [6.675705980057794e-05] mm.

These are uncertainty experiments, not identification of the installed silicone. Friction, hysteresis and nonlinear material behavior remain uncalibrated. The mechanical return result does not establish the optical voltage response.

## Stock-YAM access

Two source-scale fixture placements and four ordinary-tweezer angles each were tested. Every template has 39 finite path samples and all 315 collision hulls per arm. Expected fingertip/foot-rim support contact alone is exempted.

|Foot center,m|Tool angle,deg|IK failures|Robot-obstacle samples|Self/arm-arm samples|Tool-obstacle samples|
|---|---:|---:|---:|---:|---:|
|[0.43, 0.0, 0.98]|0|0|39/39|39/39|39/39|
|[0.43, 0.0, 0.98]|15|4|39/39|39/39|39/39|
|[0.43, 0.0, 0.98]|30|4|39/39|37/39|39/39|
|[0.43, 0.0, 0.98]|40|4|39/39|39/39|39/39|
|[0.48, -0.03, 1.03]|0|0|39/39|39/39|39/39|
|[0.48, -0.03, 1.03]|15|2|39/39|39/39|39/39|
|[0.48, -0.03, 1.03]|30|4|39/39|29/39|39/39|
|[0.48, -0.03, 1.03]|40|4|39/39|27/39|37/39|

Only **2** templates solve every endpoint; neither has a clear sampled path. Collisions evaluated at unsolved IK results are diagnostics, not executed reachable paths. **No complete stock-YAM acquisition/placement or loaded tool motion is demonstrated.** Sampling is not continuous swept certification. The remaining test is a genuine support grasp plus one annulus seating/release with full surrounding hardware; see NEXT_GATE.md.

## Decision

Local source-section contact mechanism is implemented and executed. Axial capture, finite-rotation coupling, actual twelve-piece assembly, fork closure, loaded YAM tooling and optical function remain unverified. **READY FOR FULL IMPLEMENTATION: NO.** No GPU, Brev, Dream, paid evaluation, purchase or official submission occurred.
