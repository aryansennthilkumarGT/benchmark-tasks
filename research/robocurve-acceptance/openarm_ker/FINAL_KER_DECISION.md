# Final KER decision

**PARK AND MOVE TO ANOTHER CANDIDATE.** Do not start a KER contact prototype, GPU work or another speculative fixture-reconstruction sprint. This supersedes the previous HOLD in GO_NO_GO.md; it does **not** say that the real product cannot be calibrated.

## Decisive finding

The actual CAD **does support** a much stronger result than the previous checkpoint: a seven-joint core graph with a separate trigger joint, verified bearing/shaft axis lines,70% functional link lengths, and a crossed-arm fit to both asymmetric P1 seats and radial J8 fastener interfaces with position residuals below5e−11mm. Rear-body and lock-ledge shared patches were measured. No component was independently teleported to its target.

That is **not a verified complete calibration-ready assembly**:

1. Four exact-fitting branches per side remain; the diagnostic minimum-angle branch is not manufacturer-certified. Its J6 stator/bracket pair has0.0379651777mm³ of new nominal rigid intersection. The other tested structural pairs are clear, but other angle branches and tolerance/clearance explanations remain unverified.
2. The housing screw constraints leave J8's moving trigger angle undetermined. Freezing the exported spring/trigger pose does not establish the actual stop/return load path or retained reference.
3. The509-row ledger has113 structural/envelope assignments and396 unknown assignments:373 fasteners plus23 actual backpack/hinge/accessory bodies. The exported backpack reaches235mm below the jig underside. A source-compatible folded/detached ready configuration and its connectivity were not verified. Silently omitting this hardware would invalidate the requested whole-assembly test.

These are central configuration/construct gaps, not a demand for perfectly calibrated materials before any prototype. Version21 permits disclosed physical approximations. Here the full physical starting/ready configuration to approximate remains unverified. Per the user's final bounded-gate instruction, this is **PARK**, not another HOLD. Preserve the recovered axes, branches and diagnostics; do not tune hypothetical springs or prune inconvenient source bodies.

## Gate ledger

| Gate | Evidence-based result |
|---|---|
| Manufacturer procedure | **VERIFIED:** pressed-in P1, seated J8 flats, gently flexed body lock, rear contact, two M2×12 screws per side; mechanical preparation precedes electronic zero reset. |
| Importance | **Credibly supported, still conditional:** actual robot leader/data-collection commissioning under Version21 AI-timelines category. A robot label alone is not the argument; the full useful mechanical operation must survive. No jobs threshold claim. |
| Actual mechanism/ready pose | **NOT VERIFIED:** exact core hypotheses exist, but trigger, accessory configuration, complete link assignments and branch validation remain open. |
| Novelty/current official scope | **CONDITIONAL, serious #1900 risk:** comparison below. No claim of cleared novelty. |
| Physical scoring | **CONDITIONAL:** real pipe/flat/body contact, retained fixture/fasteners, hand release and stability can be measured; OEM tolerances and retained states are unbound. Numerical fit precision is not an allowed-error specification. |
| Stock-YAM access | **NOT RUN:** upstream whole-assembly gate failed. No grasp, screw approach, swept-access or support-transfer pass claimed. |
| Allocation | **PARK AND MOVE TO ANOTHER CANDIDATE.** |

## #1900: actual novelty reassessment

[Fresh public recheck](evidence/PR1900_ARTICULATION_RECHECK.json): official [PR #1900](https://github.com/robocurve/benchmark-tasks/pull/1900) is **OPEN**. A fresh `git ls-remote` confirms head `1893637a3248bc93d716cce2d8ed6313f8901a4c`, identical to the previously inspected implementation. Its legitimate operation is holding an unpowered gravity-loaded robot link at zero and inserting a reference pin to retain it before storing controller offsets. Earlier code inspection remains applicable; its scope is not dismissed because the task is open or simplifies a detent.

The KER procedure genuinely adds two **nonparallel pipe datums**, planar J8 interfaces, a flexed integral body lock and four required screws. The recovered crossed-arm configuration confirms articulation matters; it is not one rigid platform put on a tray. The publisher also specifies **sequential** right-P1/right-J8/body-lock/right-fastening, then left-P1/left-J8/left-fastening. It does not demand simultaneous free-space support of both arms. The jig may carry substantial load between steps; a necessary difficult bimanual support transfer has not been demonstrated.

The strongest reviewer rejection is therefore: **the useful physical skill is still registering unpowered robot joints at a zero reference and retaining them, with extra joints, an OEM fixture and screws adding complexity but not a clearly different ability.** KER could only defend distinctness by preserving and demonstrating consequential cross-datum coordination and contact/support maintenance during actual lock/fastening. The source sequence makes that plausible, but our incomplete configuration and lack of real contact execution do not establish it. Shared elementary placement/fastening motions alone do not prove duplication under Version21; conversely, the brand, more joints, crossed posture or20.9° datum difference alone do not prove novelty. No official duplicate verdict is invented.

## What the actual CPU results establish

[Articulation report](ARTICULATED_KER_RECONSTRUCTION.md), [registered-pose report](REGISTERED_READY_POSE.md), [recorded numerical results](results/articulation/):96 deterministic fitting attempts; four exact branches per side in the supported crossed assignment;94 jig,21 nonadjacent/opposing-arm and119 adjacent Boolean checks; zero worker timeouts/errors; one small positive adjacent intersection. Independent rear/ledge contact areas220/43.331222mm². No causal contact dynamics, insertion/release, screw engagement, retention force or damage law was tested.

An initial transform conversion failed (`gp_GTrsf::Trsf() - non-orthogonal GTrsf`); proper rigid `gp_Trsf.SetValues` construction corrected that code issue. An uncached draft audit was stopped without claiming completion. Final bounded audits cached conservative boxes and completed; only their recorded results support the findings.

## YAM obligations that remain untested

The existing315-collision-hull-per-arm infrastructure is retained unchanged. Stage5 was conditional on a supported full ready configuration and therefore was not bypassed by a point-TCP IK calculation. No20-control numerical replay was used.

Before any future externally resolved revival, the exact full assembly/accessory state and allowed motions would have to be supplied, then actual-scale whole-structure paths and both YAM arms checked. The published1.7kg product mass implies about16.68N total gravity at9.81m/s²; it supplies neither link masses/centers of mass nor hinge/spring loads or allowable gripper purchase. Nominal93.9mm jaw aperture does not prove stable support. Jig anchoring/flex, snap force/damage, support transfer, realistic M2 driver/socket geometry, fastening reaction and released retention are untested. An endpoint is not an insertion path.

## Next portfolio nomination: N077, with a concrete new source basis

**Nominate N077 for the next independent source gate: mount a moteus-r4.5 on-axis encoder/controller centered over an already attached rotor sense magnet at the publisher's approximately2mm gap.** This is a documented **axial magnet/PCB** variant, not the bank's original unverified RLS ring/readhead or an invented curved-track gauge operation. No magnet bonding, powered calibration or robot actuation is included in this nomination.

This reserve now has actual downloadable publisher CAD and a read manufacturer procedure, rather than another blocked-product URL:

- [Mechanical setup, pinned](https://github.com/mjbots/moteus/blob/d37bff0ff9798594801469bc899c47e3425f8375/docs/guides/mechanical-setup.md): attach a diametrically magnetized sense magnet rigidly to the **rotor**, not the reducer output; mount the controller centered laterally over it with an approximately2mm gap and no slip. It explicitly warns that r4's encoder is **not centered under the bolt pattern**.
- [Actual r4.5 STEP](https://github.com/mjbots/moteus/blob/d37bff0ff9798594801469bc899c47e3425f8375/hw/controller/r4.5/20210124-moteus-controller-r45-mechanical.step) and [matched drawing](https://github.com/mjbots/moteus/blob/d37bff0ff9798594801469bc899c47e3425f8375/hw/controller/r4.5/20210124-moteus-controller-r45-mechanical.pdf): independently downloaded/read; the drawing was visually inspected. Four M2.5 mounting sites form a40×38mm pattern; the encoder origin is15/23mm between the two mounting rows, not19/19mm. The board outline is46×53mm.
- [Executed CAD inspection](evidence/N077_MOTEUS_CAD_INSPECTION.json):1 solid,265 faces,46×13.35×53mm model envelope, units mm. STEP SHA256 `ec1c7a9212cf34ea8845fcc627ee5b9f683293ff1901a01d55b0d40c3c483908`. This is the released controller envelope, not a measured production assembly or a complete motor.
- [Source manifest](evidence/ARTICULATION_SOURCE_PROVENANCE.json) retains all three hashes and immutable URLs. This source set is sufficient to begin an independent CAD/procedure comparison without speculative encoder-board geometry. No replacement simulation was implemented.

**Nomination status: RESEARCH ONLY, NOT GO FOR A CPU COUPON.** A compatible real motor/rotor/magnet and mounting arrangement with actual geometry must still be bound. Do not invent an adjustable bracket, shim procedure, precise tolerance around “approximately2mm”, a gauge mandated by the OEM, or force response. This reserve is stronger on read procedure and controller CAD; it is not yet a complete source-bound task. No existing portfolio candidate was established here to have every assembly input needed for implementation; that limitation is explicit rather than presenting this partial CAD package as full clearance.

Its useful outcome would be retained lateral/axial encoder registration after fastening, observable with a real dimensional gauge or calibrated image and a released mount check. Magnetic/electronic accuracy cannot be inferred from geometry alone. Its strongest rejection is a generic PCB fastening/alignment task with a robot label, or a contrived adjustable gap not present in actual robot assembly. A next source gate must establish consequential authentic mounting and compare current encoder/calibration/PCB tasks; #1900's joint-zero retaining operation is a relevant but not automatically equivalent skill. Actual stock-finger/driver access may fail on the small board. The original RLS candidate's occupational and feasibility claims do not transfer automatically.

N040/N022 remain parked; N013/N006 remain excluded. No purchases, GPU/Brev/Dream/paid evaluation, full task implementation or official submission occurred.
