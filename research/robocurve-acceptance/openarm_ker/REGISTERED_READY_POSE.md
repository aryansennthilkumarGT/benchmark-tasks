# Registered ready-pose hypotheses — not a verified full configuration

**New result:** real source axes admit exact connected-chain registration to both asymmetric P1 seats and the J8 radial screw interfaces, **with the arms crossing to opposite holders**. This is consistent with the publisher's step4/step8 images. It is not a full ready-pose validation, insertion path or retention demonstration.

## Constrained fit

One whole-body transform, identity in the shared release coordinates, is used. Every link transform is a product of rotations about the eight actual exported bearing-axis lines; individual parts are never independently placed at datums. P1 belongs to link2. J8 housing belongs to link7; TRG is a separate J8-rotating member.

The P1 axes use the actual jig seats: negative-X parallel Y; positive-X tilted20.9248324276°. The source pipes have100mm length and R7.5 outer surfaces; jig seating spans48mm. In this registration q1 is0°/−20.9248324276° and q2=0. The source negative-Y pipe span is preserved, rather than declaring parallel cylinder axes sufficient without axial overlap.

J8 mapping is a **SOURCE-SUPPORTED HYPOTHESIS**: the housing radial R0.8 drill lines at native `(±100.05, −373.2±3, z)` and its unused Z−63 flat mate with the jig's Y-oriented R1.2 clearance lines and Y−110 plane. J7-J8's existing mounting pair is on the other radial side; the selected jig interface is not the TRG horn's7mm mounting pattern. This supports screw orientation and nominal alignment, **not thread quality, actual unused threads or M2×12 clamping engagement**.

- Negative-X arm → positive-X jig pair: X65.079022274/71.079022274, Z−6.7.
- Positive-X arm → negative-X jig pair: X−80.365220892/−74.365220892, Z48.3.

The workflow independently specifies two M2×12 screws per J8, a seated flat, pressed-in P1, rear body seating and gentle jig-frame flex to engage the body lock. These steps are genuine; their force response is not supplied by nominal BRep coincidence.

## Numerical registration and ambiguity

Twelve deterministic starts per case tested both holder assignments and two orientation signs:96 least-squares solves. This is a bounded search, not exhaustive global IK or a physical joint-limit search. The optimizer scales its rotation residual by50mm/radian for numerical conditioning; that weight is not a torque, physical property or acceptance tolerance. An independent elbow-to-required-wrist distance check verifies the151.2mm forearm invariant. Source face/axis data, not a rendered silhouette, supply the measurements.

| Case | Position residual mm | Orientation residual degrees |
|---|---:|---:|
| Negative-X arm, own-side holder, better tested orientation |0.459345|0.344237|
| Positive-X arm, own-side holder, better tested orientation |5.449915|4.604733|
| Negative-X arm, crossed holder, fitted orientation |1.40e−11|2.97e−11|
| Positive-X arm, crossed holder, fitted orientation |4.89e−11|1.04e−10|

The wrong-side rows are failed controls **for the tested root, pipe branch and interface hypothesis**, not a proof that every possible orientation or modified hardware layout is impossible. Numerical precision is not an OEM assembly tolerance.

Four distinct exact-fitting angle branches per arm were found. For diagnostics only, the smallest sum of absolute coordinate angles selected:

| Native side | q1,q2,q3,q4,q5,q6,q7,q8 in degrees |
|---|---|
| Negative X |0,0,90,−135.045814,≈0,45.045814,≈0,0*|
| Positive X |−20.924832,0,−73.412883,−126.745329,26.468317,39.829145,≈0,0*|

`*` q8=0 is the exported trigger angle, **not an independently established spring-return/stop state**. The J8 housing constraints do not determine this revolute coordinate. Other branches are retained in [the complete output](results/articulation/ARTICULATED_REGISTRATION.json); no minimum-angle preference is a physical acceptance rule. Forearm reach-invariant errors are about6.21e−11/−2.16e−10mm; P1 line errors are zero to floating-point precision.

## Independent source-BRep checks actually completed

Both sides were present in the selected hypothesis. Conservative transformed AABBs only selected pairs; actual OCCT BRep Common operations measured intersections. The audit did not use proximity as a release/latch/success trigger.

| Check | Executed result | Interpretation |
|---|---|---|
| BASE_A rear face100 vs jig face45 |0mm distance;220mm² shared area | Actual finite rear contact at the hypothesized root placement |
| BASE_B ledge face45 vs jig face42 |≈1.78e−15mm distance;43.331222mm² shared area | Actual nominal lock-ledge contact; does not prove flex/retention |
| Structural/envelope bodies vs jig |94 broad-phase candidate checks,47 per arm; all0mm³ | No intersection detected in this tested subset |
| Nonadjacent/opposing-arm bodies |21/21 candidate checks; all0mm³ | No detected nonadjacent interference in this selected pair of branches |
| Adjacent-link bodies |119/119 candidate checks; one positive | Not an all-clear for rigid interfaces |

The positive adjacent result is **occurrence73 ENC_HOUSING (J6 stator/link5) vs occurrence130 J6-J7 (link6):0.0379651777mm³**. The corresponding exported-pose intersection is0mm³. This small nominal CAD intersection was neither deleted nor replaced with a latch/clearance shortcut. Its physical significance is unresolved: source simplification, actual clearance, tolerances and other IK branches have not been resolved. It is not evidence that real KER cannot be calibrated. It prevents claiming a penetration-free validation of this selected ideal-rigid pose. Version21 allows explained approximations; this is an internal evidence/cost gate, not an invented official zero-overlap rule.

All234 posed pair checks and the positive pair's exported-baseline Boolean completed without timeouts/errors. Actual outputs: [bounded audit](results/articulation/BOUNDED_INTERFERENCE.json), [adjacent audit](results/articulation/ADJACENT_INTERFERENCE.json), [run scope](results/articulation/BOUNDED_AUDIT_RUN.json), [adjacent scope](results/articulation/ADJACENT_AUDIT_RUN.json). Source fasteners and23 accessory bodies were not assigned complete moving-link poses; this is **not an all509 collision certificate**. Other IK branches and a nonzero trigger angle were not audited.

## Full assembly blocker: backpack and trigger state

[Actual accessory bounds](results/articulation/UNASSIGNED_ACCESSORY_BOUNDS.json) establish an additional concrete problem with calling the core fit a complete ready pose: the exported backpack/chest assembly reaches **Z−274mm**, while the jig underside is **Z−39mm**. Thus its lowest parts extend235mm below a bench plane at the jig underside. A bench occupying those projected locations would intersect them. This is a conditional plane comparison, not a completed collision check against a chosen real table.

The manufacturer describes the backpack as foldable, and the BOM includes four HG-TS03 friction hinges and a VRIG magnetic quick release. The workflow pictures show the calibration body/arms but do not establish the complete509-occurrence accessory pose, whether a backpack was detached, or a legitimate articulated folding sequence. Treating these parts as absent, teleporting them or fixing the exported backpack below the bench would all evade the requested whole-assembly test. No verified folded/detached configuration was recovered in this bounded gate.

The trigger's spring anchors/rest angle, actual hard stops and retained angle are also not established. Housing screw alignment cannot substitute for verifying all encoder-joint reference states. Consequently **the complete manufacturer-ready configuration remains unverified**, despite the exact core-chain fit. [Final decision](FINAL_KER_DECISION.md): PARK; no further speculative KER fitting sprint or YAM path claim.
