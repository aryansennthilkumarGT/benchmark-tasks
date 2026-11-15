# N044 CPU preflight: rear crankshaft seal

**Decision: PARK as the first implementation; retain as a conditional later prototype.** The program ran and returned exit2, `BLOCKED_MISSING_INPUTS`, with16 geometry/path/phase gaps and5 missing force-data groups. No seal/driver clearance, grasp or hammer-impulse proof was obtained. This is not a demonstrated physical failure.

## Exact binding achieved and not achieved

Read pinned CHARM pages265/4278 for the 2013 Elantra L4-1.8L application: archive rear main seal identifier **HYD214432E000**, SST **09231-H1100 /09214-2E000**, fresh engine oil on the new lip and source-permitted hammer to the block rear-face datum. The actual block/crankshaft/flange must remain; normal engine-service support can carry reaction. Prior disassembly is outside the bounded install operation.

That binds procedure and identifiers through an attributed reproduction, not actual selected-part dimensions or current VIN compatibility. Seal OD/ID/width, internal lip/case orientation profile, housing interference, shaft/flange envelopes, driver/handle shape, hammer mass/shape, actual support and work pose are missing. New hemanual links returned403, so exact engine/applicability of those unread pages was not verified. No driver was inferred from its name or diagram scale.

## Actual executed CPU result

[N044_ACCESS_TEST.py](N044_ACCESS_TEST.py), [input](inputs/N044.json), [JSON output](results/N044_ACCESS_RESULT.json), [command log](results/N044_EXECUTION.txt). Actual robot collision geometry includes both full arms, palms/wrists and fingers. No seal/housing/tool geometry or complete path was invented, so acquisition, unstarted alignment, driver seating, hammer sweep and final inspection phases remain unassessed. A point inside the loose robot reach sphere does not change that result.

The CPU code computes the actual READY-pose Jacobian and gravity loads from the pinned joint/CoM data. For that pose only, configured-effort static external vertical-load ceilings are approximately **41.99N upward /27.64N downward on the robot TCP** (joint4 limiting), with no tool/payload, grasp, contact, dynamics or safety factor. Force applied by the robot to an object has the opposite direction. These are optimistic model screens, **not achievable seal force, a gripper rating, or an impact limit**. Actual service/strike pose is unknown, as are the needed insertion force and tap energy. They cannot be compared or declared sufficient. No-load wrist speed and spring/driver dimensions do not fill that gap.

A genuine hammer analysis needs its mass/COM/inertia, stroke/contact geometry, local effective robot inertia, achievable loaded velocity, grip slip, actual insertion force-depth/cocking response and engine-stand reaction. Static `tau = Jᵀw + gravity` cannot certify a transient impact. No load curve or impulse was guessed from seal part count or a7Nm wrist setting.

## Importance scrutiny

Mirrored mechanics employment704,640 qualifies the occupation scale, but not every precise repair. O*NET 30.2 Core 23532 concerns faulty assembly repair, and Core 23544 names engine parts such as pistons/rods/gears/valves/bearings. Neither explicitly establishes rear main-seal installation frequency. Crankshaft/cylinder-block rebuilding23547 is **Supplemental**. The read seal step occurs in engine reassembly; it does not prove an independently regular rear-seal procedure across the qualifying occupation.

This is an authentic service operation with a plausible Core-repair bridge, not yet a strong verified specific regular-duty claim. Unlike N040's explicit power-window Core duty plus required trim-access sequence, the narrow rear-seal frequency/support remains weaker. We do not aggregate unrelated roles or count the Supplemental duty as Core. This contributes to parking N044 as first choice; it is not a claim that mechanics never replace rear seals.

## Press-fit/seal comparison, corrected against actual accepted content

Accepted [#1800 oil-feed sleeve](https://github.com/robocurve/benchmark-tasks/pull/1800) was newly inspected at official main `2f9900866d314690bd5322e59f90e3860789694d`. Its actual task ends at released axial seating **and radial-port registration**; fidelity expressly states a0.8mm radial **clearance fit, not press fitting**, and allows gravity seating. It must not be cited as an accepted plain bearing press merely because of its folder name.

Accepted#1576 stretches/seats an O-ring over a hydraulic plug thread; #1562 assembles/tightens an olive/nut compression joint. These differ from genuine seal-case interference around a crankshaft, correct driver load path and lip/shaft interaction. Shared insertion or annular objects alone do not establish duplication. Previously read#995/#1199 bearing/bushing cases are final/closed; their old duplicate/importance findings are not current accepted press-fit clearance.

Nevertheless, if N044 only presses a different rigid annulus to a depth stop and leaves its lip/shaft behavior decorative, its proposed new capability is not demonstrated. A real unstarted square-seating and seal-interface model could matter; we have neither geometry nor physical counterexamples to establish it. **Park the depth-only representation and N044 as first build; do not claim an official duplicate ruling.** A legitimate sourced approximation is allowed, not a license for a generic ring trainer.

## Mechanical score that still needs physical validation

Nominal source target is flush with the actual rear block face (offset0), not a verified allowable±band. Read depths at several circumferential sites with a straightedge/depth gauge; source-bound resolution/tolerance remains absent. Check actual orientation/part identity, real retention and available visible case/lip/spring condition through ordinary assembly views/inspection. No modified viewing hole or imaginary inspection access.

| Negative state | Why depth-only scoring is inadequate | Required future evidence |
|---|---|---|
|Tilted/cocked case|A centre/average depth can hide circumferential step.|Multiple real datum readings and justified allowable spread.|
|Reversed seal|A hypothetical depth-only observer has no orientation measurement.|Actual part profile/marking and whether reverse can physically seat; not yet verified.|
|Damaged/rolled lip or displaced spring|Same observed outer plane need not encode internal condition.|Normal visible inspection or justified benign physical check. Do not assert such a bad genuine specimen was tested.|
|Wrong driver engagement or wrong part|Tap count/command is not assembled geometry.|Actual load-path/contact and part/seat observations.|
|Still supported by tool|A pressed-looking final pose may be tool-held.|Ordinary released retained-seat check.|

Correct/incorrect specimens were **not physically executed**. The table identifies observability requirements, not a demonstrated counterexample on this unmeasured seal. A hidden-state lip flag cannot silently become a ruler measurement. Bound the final mechanical claim honestly; neither pose nor a real seal catalogue rating proves oil tightness. Minor unobservable details need proportionate treatment, while a consequential false-completion strategy must be resolved.

## Stop threshold and later CPU milestone

Before any genuine seal-contact prototype, obtain compatible part/SST/housing sections and actual normal work/support geometry. Then the existing evaluator can check acquisition/driver/hammer paths with whole robot geometry, and a small CPU contact unit can test unstarted/cocked/loaded seating against measured or sourced parameters. If the claimed skill collapses to depth-only pressing, park it. If access requires a smaller block, absent flange, larger handle or unsupported reaction, park it. Missing data cannot be turned into a feasibility pass by selecting arbitrary dimensions.

N044 does not outrank N040 for the first small CPU prototype on the evidence now available. No native test is authorized to discover these source/geometry/importance gaps.
