# Five conditional implementation blueprints

These are concrete mechanism/controller/scoring plans, **not implementation-ready specifications**. Importance/novelty are unresolved, live primary documents remain unavailable and key dimensions/forces have not been measured. No scene code, GPU run or model evaluation was created. Numeric score weights below are proposed benchmark design choices, not OEM requirements. Unset tolerances/load values deliberately prevent a fabricated build-ready status.

Every blueprint needs source-bound asset dimensions/materials/masses, an ordinary physical mounting/reset protocol, task-independent robot controls, complete action/time accounting and source-matched receipts. No prescribed controller trajectory should become the success criterion. Avoid worktrees: use the existing isolated task checkout unless explicitly asked otherwise.

## 1. Double-stud L-track cargo-anchor engagement

**Go/no-go before implementation:** Reject unless exact keeper access works with stock fingers and an anchor-only endpoint survives#770 importance/novelty review.

**Assets:** Rail segment with two or more actual aperture pairs, ordinary mounting plate, selected two-stud fitting, real keeper/link and reference scale. Primitive meshes must retain circular entry edges, undercut thickness and keeper collision geometry. Store product SKU/source-page provenance beside each dimension.

**Articulations/contact:** Fitting free6DOF; keeper actual passive slider/hinge and spring only after its real mechanism is documented; link articulation if present. Fixed rail does not actuate the fitting.

**Controller phases:** Acquire fitting without touching keeper inadvertently → hold actual keeper disengaged if required → align both discs with openings → insert to real depth → translate to captured position → release keeper → release both hands → observe retention. A separate evaluator performs the calibrated proof check.

**Scoring/physical observations:** 0 if damage/fixture detachment or no meaningful capture; proposed0.25 for both studs truly under lips,0.5 with fitting positioned and keeper engaged,1 only when released retention/proof test passes. Do not reward a single captured stud if it is an unsafe unusable anchor. All pose tolerances and proof load remain unset pending hardware evidence.

**Reset:** Remove fitting by documented release, return same aperture location/keeper start, inspect rail and keeper for damage, restore fitting and mount positions. Photograph start with scale.

**Negative controls:** One stud captured; keeper perched but not engaged; finger holds link; rail pulled off mount; translated but keeper absent; reverse-direction pull; wrong aperture pitch; a second valid manipulation sequence; safe repositioning; reset does not erase genuine damage.

**Required tests:**

1. Source/equipment audit maps every essential contact to a real interface; compare closest three tasks and signed-in board before authoring.
2. Physical measurement rehearsal demonstrates all score conditions can be observed without dismantling or disturbing the result.
3. Full-size stock YAM grasp/IK/collision/force feasibility check over the complete path, including simultaneous hands and tool inertia. Endpoints alone are insufficient.
4. Unit scorer tests cover all tiers, boundary tolerances, safe alternative solutions, released hold, invalid histories, time discontinuity and repeated physical reset.
5. CPU contact diagnostics must preserve task geometry and force limits. A task-only mechanism pass or initialized grasp fixture is not a full robot pass; report both separately.
6. Only after conceptual clearance and separately authorized compute: native exact-source contact checks, full robot expert, independent fresh-reset reproduction, genuine model evaluation and matching media. These are future requirements, not research results.

**Cost control:** no action count or wall-runtime estimate is measured for this design. Stop early on the stated conceptual or grasp-access blocker; do not solve it by inventing larger knobs, lighter hardware or hidden task actuators.

## 2. SDS-plus full-size chisel exchange

**Go/no-go before implementation:** Reject if semantic comparison to#662/#175 shows only a different connector or if force/gripper dimensions cannot be met at actual scale.

**Assets:** Exact unpowered hammer front/tool holder, actual sleeve, retaining ball, guide keys, two matched SDS-plus shanks/chisels, supported storage rack and scale. Do not turn real circular interfaces into square peg sockets.

**Articulations/contact:** Tool free6DOF; passive sleeve axial motion and radial ball contact; key grooves block rotation appropriately; locked tool retains intended axial freedom. No state-triggered weld joint or ball actuator based on score.

**Controller phases:** Acquire old shank → other arm retracts actual sleeve → withdraw tool along permitted axis → let sleeve return and store old tool → acquire new shank → rotate/advance through guide keys until automatic capture → release → evaluator confirms retention and axial float.

**Scoring/physical observations:** Proposed0 for no valid change/damage,0.25 old tool removed and safely supported,0.5 correct replacement inserted but lock unproven,1 correct retained replacement after release and proper pull/float check. The physical evaluator test must distinguish allowed float from withdrawal; numeric limits require manual/hardware measurement.

**Reset:** Use genuine sleeve release to remove new tool, restore old shank/lock and starting sleeve state; confirm power isolated, tools clean/lightly lubricated per manual, same orientation and insertion state.

**Negative controls:** Wrong groove orientation; shallow insertion; sleeve still held back; removing without sleeve; tool held in place rather than locked; intended axial float; tool identity swapped; no task-object pose setters; valid rotate-and-insert alternatives.

**Required tests:**

1. Source/equipment audit maps every essential contact to a real interface; compare closest three tasks and signed-in board before authoring.
2. Physical measurement rehearsal demonstrates all score conditions can be observed without dismantling or disturbing the result.
3. Full-size stock YAM grasp/IK/collision/force feasibility check over the complete path, including simultaneous hands and tool inertia. Endpoints alone are insufficient.
4. Unit scorer tests cover all tiers, boundary tolerances, safe alternative solutions, released hold, invalid histories, time discontinuity and repeated physical reset.
5. CPU contact diagnostics must preserve task geometry and force limits. A task-only mechanism pass or initialized grasp fixture is not a full robot pass; report both separately.
6. Only after conceptual clearance and separately authorized compute: native exact-source contact checks, full robot expert, independent fresh-reset reproduction, genuine model evaluation and matching media. These are future requirements, not research results.

**Cost control:** no action count or wall-runtime estimate is measured for this design. Stop early on the stated conceptual or grasp-access blocker; do not solve it by inventing larger knobs, lighter hardware or hidden task actuators.

## 3. Removable scroll-chuck jaw setup and concentric verification

**Go/no-go before implementation:** Importance gate is first: prove direct regular-core duty across valid disjoint occupations above threshold. If not, abandon before modeling teeth.

**Assets:** One real-size chuck body with actual scroll/key drive, three independently removable numbered jaws and their true guide/tooth profiles, original key and a documented gauge/mandrel. Include spindle-lock/bench mount only as an ordinary unpowered workholding aid.

**Articulations/contact:** Passive scroll rotation driven by key contact; jaw radial guides become constrained by tooth engagement, with genuine out-of-phase states. A simplistic synchronized-prismatic-jaw actuator is insufficient for this objective.

**Controller phases:** Index scroll to the actual pickup position → present first jaw until tooth acquisition → rotate to acquire subsequent jaws at physical phases → close on gauge → inspect concentricity and retention → remove key and release. Allow any physically correct cyclic numbering/order.

**Scoring/physical observations:** Proposed0 if no functional engagement or loose unsupported jaws;0.25 all three jaws engaged,0.5 concentric closure established,1 gauge retained and verified with key removed/hands clear. Do not score a fixed number of post-contact turns (#400). Indicator/caliper tolerance and load require gauge/chuck specification first.

**Reset:** Reverse scroll to release gauge, remove jaws via proper terminal tooth position, restore key and loose jaws with original numbering. Check guides/teeth and ensure no powered spindle state.

**Negative controls:** Jaw one tooth out; missing jaw; nominal pose without tooth capture; wrong jaw family; no gauge contact; software forced centering; incorrect valid-order rejection; excessive post-contact rotation; key still present; released gauge fails proof.

**Required tests:**

1. Source/equipment audit maps every essential contact to a real interface; compare closest three tasks and signed-in board before authoring.
2. Physical measurement rehearsal demonstrates all score conditions can be observed without dismantling or disturbing the result.
3. Full-size stock YAM grasp/IK/collision/force feasibility check over the complete path, including simultaneous hands and tool inertia. Endpoints alone are insufficient.
4. Unit scorer tests cover all tiers, boundary tolerances, safe alternative solutions, released hold, invalid histories, time discontinuity and repeated physical reset.
5. CPU contact diagnostics must preserve task geometry and force limits. A task-only mechanism pass or initialized grasp fixture is not a full robot pass; report both separately.
6. Only after conceptual clearance and separately authorized compute: native exact-source contact checks, full robot expert, independent fresh-reset reproduction, genuine model evaluation and matching media. These are future requirements, not research results.

**Cost control:** no action count or wall-runtime estimate is measured for this design. Stop early on the stated conceptual or grasp-access blocker; do not solve it by inventing larger knobs, lighter hardware or hidden task actuators.

## 4. ER collet-to-nut supported preassembly

**Go/no-go before implementation:** Resolve importance/useful endpoint and failed stock grasp before any native scene effort. Source discrepancy is an elimination trigger, not a request to strengthen the virtual snap.

**Assets:** Matching ER32 collet/nut from one source family, accurate extraction groove and eccentric ring, ordinary bench supports, optional matching holder only if endpoint scope is explicitly expanded and re-reviewed. Mark all authored quantities as authored.

**Articulations/contact:** Collet and nut free rigid bodies; their ring/groove contact alone defines pivot path. Support objects fixed. No fake spring, attachment, fixture-driven task actuator or guaranteed hanging retention.

**Controller phases:** Acquire real collet lands and lift (reproduce failed CPU grasp first) → acquire supported nut → incline collet into eccentric ring → move groove into engagement → pivot axes coaxial → lower pair onto support → clear hands → inspect engagement. Expanded holder insertion requires new source/importance/novelty review.

**Scoring/physical observations:** Proposed0 no valid engagement;0.5 supported groove/ring acquisition;1 verified supported preassembly with correct coaxial fit and released hands. A physically valid but unsupported collet must not fail an invented hanging test. No depth/angle tolerances finalized before drawing and sight-line protocol.

**Reset:** Separate using manufacturer tilt/release procedure; inspect groove/ring for burrs; restore same supports/part orientations and cleanliness. Do not prefit so deeply that straight placement suffices.

**Negative controls:** Straight coaxial push; contact on wrong lip; apparently aligned but unengaged pair; correct pair supported; unsupported drop is not proof manufacturer guarantee; gripper still supports; different collet yaw accepted; alternative valid tilt direction; reset state scores0.

**Required tests:**

1. Source/equipment audit maps every essential contact to a real interface; compare closest three tasks and signed-in board before authoring.
2. Physical measurement rehearsal demonstrates all score conditions can be observed without dismantling or disturbing the result.
3. Full-size stock YAM grasp/IK/collision/force feasibility check over the complete path, including simultaneous hands and tool inertia. Endpoints alone are insufficient.
4. Unit scorer tests cover all tiers, boundary tolerances, safe alternative solutions, released hold, invalid histories, time discontinuity and repeated physical reset.
5. CPU contact diagnostics must preserve task geometry and force limits. A task-only mechanism pass or initialized grasp fixture is not a full robot pass; report both separately.
6. Only after conceptual clearance and separately authorized compute: native exact-source contact checks, full robot expert, independent fresh-reset reproduction, genuine model evaluation and matching media. These are future requirements, not research results.

**Cost control:** no action count or wall-runtime estimate is measured for this design. Stop early on the stated conceptual or grasp-access blocker; do not solve it by inventing larger knobs, lighter hardware or hidden task actuators.

## 5. RIDGID811A quick-opening die-head setup

**Go/no-go before implementation:** Obtain cam/guide drawing, stock-control access and core-duty proof. If the bounded setup is not independently consequential, reject or redesign around an authentic complete operation before any spending.

**Assets:** Exact811A head, matched die set/slot marks, size bar/link, washer tongue and clamp lever; original throwout control, restrained unpowered mount. Asset pack requires one documented head configuration rather than combining parts catalogs.

**Articulations/contact:** Real die radial guides and common positioning/retention mechanism; physical washer/tongue engagement; actual clamp screw/link. No automatic seating or color-matching rewards without contact consequences.

**Controller phases:** Open throwout → loosen clamp approximately3turns per manual → lift tongue and move washer to slot end → insert each correct die with indicator line flush → align index to requested size and seat tongue → tighten clamp → perform normal open/close retention inspection → release. Do not cut a thread in this CPU research scope.

**Scoring/physical observations:** Proposed0 no usable die capture;0.25 correct complete die set at required seating marks;0.5 correct size setting/tongue engagement;1 retained configured assembly after release/normal head travel. This scores setup only. A gauge/thread quality/pressure-seal claim requires the manufacturer-mandated subsequent test cut, outside this blueprint.

**Reset:** Open/loosen through documented controls, remove dies, restore selected start size/washer slot and mark orientations. Track matched set; inspect guide/cam damage. No synthetic fixture resets posed as physical reset.

**Negative controls:** Wrong die/slot ID; mixed dies; shallow indicator line; tongue outside slot; clamp loose; dies fall on opening; false positive from color order; software captures free die; safe alternate insertion order; correct setup still not labeled cut-thread-ready.

**Required tests:**

1. Source/equipment audit maps every essential contact to a real interface; compare closest three tasks and signed-in board before authoring.
2. Physical measurement rehearsal demonstrates all score conditions can be observed without dismantling or disturbing the result.
3. Full-size stock YAM grasp/IK/collision/force feasibility check over the complete path, including simultaneous hands and tool inertia. Endpoints alone are insufficient.
4. Unit scorer tests cover all tiers, boundary tolerances, safe alternative solutions, released hold, invalid histories, time discontinuity and repeated physical reset.
5. CPU contact diagnostics must preserve task geometry and force limits. A task-only mechanism pass or initialized grasp fixture is not a full robot pass; report both separately.
6. Only after conceptual clearance and separately authorized compute: native exact-source contact checks, full robot expert, independent fresh-reset reproduction, genuine model evaluation and matching media. These are future requirements, not research results.

**Cost control:** no action count or wall-runtime estimate is measured for this design. Stop early on the stated conceptual or grasp-access blocker; do not solve it by inventing larger knobs, lighter hardware or hidden task actuators.

## Why these plans remain conditional

The user requested five strongest implementation blueprints. The available evidence supports only five research-level plans, so claiming five build-ready packages would repeat the failure this mission is meant to prevent. The primary-source/board/robot-envelope gaps must be resolved first. In particular, manufacturer-required test cuts, product-specific extraction behavior and real control forces cannot be replaced by confidence in a mesh or scorer.
