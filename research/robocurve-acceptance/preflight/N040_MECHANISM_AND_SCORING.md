# N040 CPU preflight: genuine front-door trim removal

**Decision: first choice for a small CPU prototype, not cleared for a full task or native evaluation.** The access program actually ran and returned exit2, `BLOCKED_MISSING_INPUTS`, with19 missing geometry/path/phase inputs. This is a data blocker, not measured physical infeasibility. No full-size clearance pass exists.

## Selected equipment and source limits

Target platform: 2013 U.S. Hyundai Elantra UD1.8L front door; left-front was the proposed donor side. The exact donor VIN/trim, panel/clip part numbers, fitted plug variants and tool SKU remain unbound. This is not an actually measured selected door.

Pinned CHARM reproduction `Kmberry1989/Elantra@0f7b23efdcf6ecc48919fb781be7e95a1b8f0f06`: pages863/887 and diagrams945643715,945655092,945669489,945681280 establish real perimeter retention, quadrant-cover/screw prerequisites, inside-handle cage and rear connectors. The ordinary tool is a plastic panel-removal tool; its actual blade/handle geometry is absent. Do not substitute a steel fork or enlarged tab by assumption. The source instructs replacement of damaged clips; it does not establish universal clip reuse.

Both new charm.li URLs supplied for this sprint returned proxy 403. The hemanual pages also returned403. None was inspected or used to infer dimensions/applicability. Parts-index and bounded source/CAD searches did not supply the missing panel/clip/tool geometry. We did not scale the uncalibrated diagrams or use whole-car exterior width as door/clip clearance.

## Current #1986 comparison

A fresh public-page read reports **OPEN**, with a latest receipt awaiting review. Its current head is still `e8ecd21da83c33bfe2107962a4d1a28495b1e336`. Repeated review/revision receipts concern reproducibility of catch spring/profile geometry. The current task.json was re-read; the legitimate operation remains aligning a loose splash-shield hole to a fixed body hole and pushing a loose clip through both until captured/flush.

N040's proposed central work is acquiring a plastic-tool leverage contact behind an already engaged retainer, controlling panel release while other sites/upper edge remain attached, then completing the actual handle/connector handoff. That can differ from loose-clip insertion under Version 21; merely reversing a motion, adding clips or plugs does not prove it. The intended release mechanism must actually differ and remain consequential. Defects in #1986's custom catch do not extinguish its legitimate active claim. Current focused door-trim/panel-removal searches found no additional direct match; this is not private-board or exhaustive semantic clearance.

**Finding:** no direct same-operation finding against #1986, but exact clip mechanism/current origin comparison remains a pre-full-task gate. This supports a small prototype investigation, not a novelty certificate.

## Executed geometry check

[N040_ACCESS_TEST.py](N040_ACCESS_TEST.py) delegates to the shared CPU evaluator. [Input](inputs/N040.json), [result](results/N040_ACCESS_RESULT.json), [actual command log](results/N040_EXECUTION.txt).

The robot side is source-bound: actual `yam_arm.urdf` CoACD hulls, not the old visual-mesh bounds. It includes315 hulls per arm:45/47 finger hulls,44 gripper/palm hulls,16 link5 wrist hulls, and the remaining arm/base hulls. Both station bases are included at `(0,±0.305,0.75)` m. FK was independently compared with the pinned source evaluator on all links; the largest transform-element discrepancy was below5e-16 over six arm/configuration comparisons.

Reusable checks include actual joint limits, FK/pose demands, full robot-vs-surrounding geometry, inter-arm and nonadjacent same-arm checks, tool/panel swept-envelope checks and conservative interval motion bounds. A midpoint collision with clear endpoints is an executed regression control. Intersecting conservative envelopes return uncertainty, not an endpoint-only pass. Intended finger contacts remain explicitly unvalidated interactions; they cannot hide full palm/wrist/arm collisions.

**What did not run:** an entire candidate-specific path/sweep. The input has no trusted full-panel/door/clip/tool/handle/plug geometry, calibrated service pose, support, site inventory or two-arm path. The program refuses to invent them. The necessary-only reach radius0.941269m is a loose chain-length upper bound, not reachable workspace or IK proof; the READY TCP is not a service grasp. Sensor housings absent from the pinned robot collision asset need separate treatment if relevant. No room/cowl/door structure was silently removed.

## Actual mechanism to preserve in a later prototype

Normal screws/quadrant cover may be removed in a declared service start. Target retainers start physically engaged. The tool must contact the actual clip/panel load path; genuine local elastic deformation/retention and panel reaction cause release. No tool-proximity pop, phase flag, dummy plunger or prescribed clip trajectory. The handle cage and fitted plugs remain connected until genuinely disengaged. A real support receives the panel; wires/cables are not support slings.

A calibrated local clip plus reduced compliant panel representation is permissible. It must preserve wrong-contact, still-engaged and damaging-pry cases. Real geometry/force parameters are not yet available, so no authentic contact law was fitted or run. A parametric mathematical coupon may falsify code, but cannot count as a full-size Hyundai test.

## Repeatable physical score proposal and counterexamples

| Observed state | Required interpretation | Physical observation still to bind |
|---|---|---|
|Panel moved but one clip/upper edge still carries load|Incomplete, never full credit.|Actual retained sites and a benign independent movement/inspection check.|
|Clips released but cage/plug attached|Incomplete; a position threshold is insufficient.|Back-side access/views, actual latch/cage inspection, normal slack.|
|Panel separated and independently supported; expected interfaces sound|Potential full mechanical handoff.|Source-matched site inventory, attachment condition and ordinary support check.|
|Wires pulled out, clip seats torn or panel permanently creased to free it|Invalid destructive shortcut; no completion credit from bypass.|Photographed baseline, specific structural criteria and straightedge/profile inspection.|
|A retainer breaks during otherwise normal service|Cannot silently assume all clips reusable or all breakage acceptable.|Bind selected consumable/reset policy from actual hardware/procedure; never license ripping seats/panel or cutting wires.|
|Tool approaches the panel but is not under the retainer load path|Must not create release.|Actual clip/tool section and wrong-position force/displacement negative.|

These are source-backed design counterexamples, **not executed physical release trials**. No bend tolerance, clip count, panel mass, release force or cable-load threshold is fabricated. Numeric tolerances and observation repeatability must be fixed before a task scorer. Minor cosmetic uncertainty receives proportionate treatment; unclear sampled frames alone are not failure evidence.

## Cheapest next CPU milestone

Proceed with N040 as the first **small CPU prototype priority**: one authentic clip/seat/tool contact unit plus adjacent full-scale panel/flange section, parameter provenance enforced by the existing checker. Its purpose is to test release/contact/scoring hypotheses cheaply, not to stand in for the whole door. Obtain the actual compatible clip/tool section first; run must stop on missing parameters. Wrong wedge placement, incomplete engagement and destructive prying must differ causally. A successful local coupon still does not clear whole-panel perimeter, upper edge, rear-plug or second-arm access.

Full task implementation remains blocked until actual complete geometry/path and reaction/force data are bound and the script can evaluate them without deleting hardware or enlarging clips. If a faithful full-size layout is proven impossible, PARK N040; missing geometry alone is not that proof.
