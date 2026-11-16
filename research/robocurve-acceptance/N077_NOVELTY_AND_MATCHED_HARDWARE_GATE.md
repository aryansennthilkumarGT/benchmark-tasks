# N077 novelty and matched-hardware gate

**Decision: PARK N077.** Continue from `d9794eb46647be015098d6fda11a4be485fd23a4`. KER remains PARKED and was not reconstructed or tested again.

The proposed operation—mount a moteus controller's on-axis sensor over its rotor magnet, retain lateral registration and an appropriate air gap—overlaps the central installation ability of official PR #2212. No independently documented additional manipulation was established that makes this a different task. Matched commercial hardware could strengthen authenticity, but does not by itself establish novelty. **Do not proceed to N077 matched-CAD reconstruction or a CPU prototype.**

## 1. Actual #2212 submission inspected

Official [PR #2212](https://github.com/robocurve/benchmark-tasks/pull/2212) was independently retrieved as **OPEN**, received as **TK-TAZ446**, waiting for review. Fetched head: **`0e50dbc85fedc7624a13a7fff033c161692f18c3`**. This is a pending legitimate operation, not an accepted task or an asserted official duplicate ruling.

All six task files were read statically at that immutable head:

- [task.json](https://github.com/robocurve/benchmark-tasks/blob/0e50dbc85fedc7624a13a7fff033c161692f18c3/tasks/install-a-motor-shaft-encoder/task.json) and [README](https://github.com/robocurve/benchmark-tasks/blob/0e50dbc85fedc7624a13a7fff033c161692f18c3/tasks/install-a-motor-shaft-encoder/README.md): real-world instruction, reset, outcome, fidelity and claimed evidence.
- [task.py](https://github.com/robocurve/benchmark-tasks/blob/0e50dbc85fedc7624a13a7fff033c161692f18c3/tasks/install-a-motor-shaft-encoder/task.py):501 total Python lines across this and the other three Python files were read; waypoint sequence, part seating, catch, test and scorer inspected.
- `geom.py`, `run_task.py`, `make_evidence.py`: geometry, actual-YAM hand-pose integration, success termination and recorded-frame video construction inspected. No task file was imported or executed.

The legitimate procedure is: fit a D-keyed magnetic carrier to the shaft; lower a PCB/sensor bracket onto two locating posts; retain it with a catch; perform the installation field check; release the assembly with hands clear. The setup identifies an80mm motor,8mm D-shaft,24mm carrier and71×95mm bracket. Its fixture stops establish a nominal1.5mm gap.

The source declares partial stages for carrier seating, sensor/bracket seating and retention; full credit additionally requires a passed post-installation check and release. The PR, README and task.json report **scripted YAM1.0 in581 steps**, **Dream-1 0.0 at1,400 steps**. These are **independently read submission claims**, not our independently replayed or video-verified results. No model/demo run was performed here.

Actual implementation limits were checked rather than inferred from the title: `Part.update` follows YAM hand position/yaw and applies geometric seating conditions; `State.advance` evaluates seated/released parts and the catch, with a button hold before a geometry-based field result. `air_gap_mm` reports1.5 when both parts are seated. `run_task.py` obtains actual YAM TCP poses/joint-derived finger opening, updates the custom state and requires five successive full-score steps to terminate successfully. The code does not model magnetic flux or powered angle calibration, consistent with its declared limits.

These simplifications do **not** erase the legitimate earlier installation scope. We did not dismiss the submission, rerun its score, or claim an official construct-validity rejection. [File hashes/read scope](evidence/N077-novelty-hardware-gate/PR2212-files.json), [static line locators](evidence/N077-novelty-hardware-gate/PR2212-static-inspection.json), [public state/receipt record](evidence/N077-novelty-hardware-gate/PR2212-current-status.json).

## 2. Semantic comparison under Version21

The [supplied Version21](CURRENT_RUBRIC_AND_SOURCES.md) compares physical skill, kind of setting/objects/manipulation and equivalent success condition. Shared elementary motions alone are insufficient for duplication; different hardware alone is insufficient for distinctness.

| Role or essential work | #2212 legitimate operation | Proposed real moteus mounting | Finding |
|---|---|---|---|
| Setting and useful outcome | Unpowered robot-motor encoder installation, correctly positioned and retained | Unpowered motor controller/on-axis sensor installation, correctly positioned and retained | Same kind of useful assembly outcome, not merely a shared word such as calibration |
| Rotating reference | Seat keyed carrier containing the shaft-end diametric magnet | An already rigidly attached rotor magnet in the nominated bounded start | Removing the carrier-placement stage narrows N077; it does not add a new central ability |
| Sensor registration | Locate PCB bracket over the shaft-end magnet using guide posts and stops | Locate the actual off-center sensor IC over the rotor magnet through a compatible mount | Same central sensor-over-magnet registration; the r4 PCB outline/offset changes the interface, not yet the ability |
| Air gap | Nominal1.5mm set by fixture geometry | Approximately2mm in the read manufacturer guidance | A different target dimension is not a distinct manipulation; no genuine independent adjustment procedure was established |
| Retention | Close catch and release | Rigidly fasten PCB/bracket without slip; actual matched fasteners/interface unverified | Catch versus screws is a real method difference, but ordinary fastening does not establish a separate central skill here |
| Completion check | Installation geometry/field-status check with hands clear; no angular calibration claim | Retained gap/centering check after release; no powered encoder-accuracy claim | Equivalent installation endpoint; using a gauge or actual CAD would improve evidence, not establish novelty |

**Strongest possible reviewer rejection:** this still installs and secures a shaft-end magnetic encoder in the same kind of robot-motor assembly, with equivalent centered/retained sensor–magnet registration. The controller PCB, bracket, off-center IC and screws change how the same assembly goal is achieved. No authentic additional adjustment, contact-controlled support transfer or materially different joining operation has been shown to be essential.

This is a decisive **internal implementation-queue decision**, not a claim that every sensor installation is equivalent or that shared fastening automatically makes two tasks duplicates. The evidence is stronger than an abstract “align then secure” resemblance: the rotating reference, sensing element, sensitive relative geometry, robot-building setting and retained installation goal all correspond. A different domain or genuinely essential different manipulation could change a future comparison; neither is established for this N077 proposal.

Research notes predating #2212 are not an official task submission or a demonstrated earlier reservation. No ownership expiry or exclusion was inferred from another team's implementation limitations or current review state. We will not rescue N077 by adding an invented gap jig, powered calibration, extra field-check buttons, a different magnetic readhead or generic screw steps.

## 3. Manufacturer evidence and what remains unknown

Independently re-read publisher sources at `mjbots/moteus@d37bff0ff9798594801469bc899c47e3425f8375`; fresh `git ls-remote` returned that same HEAD:

1. [Mechanical setup](https://github.com/mjbots/moteus/blob/d37bff0ff9798594801469bc899c47e3425f8375/docs/guides/mechanical-setup.md): attach the diametric magnet rigidly to the rotor, not the reducer output; center the sensor over it with approximately2mm air gap; prevent mounting slip. The r4 sensor is not centered under its mounting-bolt pattern. Adhesive is generally required for the magnet attachment.
2. [Calibration troubleshooting, sense-magnet section](https://github.com/mjbots/moteus/blob/d37bff0ff9798594801469bc899c47e3425f8375/docs/troubleshooting/calibration.md): for **the magnets mjbots sells**,2mm is near optimal and1.5–2.5mm is suitable. This is new explicit source support for a range, not a new fixture tolerance invented by us. It does not authenticate #2212's different magnet/fixture or establish its magnetic performance. It further weakens a1.5mm-versus2mm novelty argument.
3. [Quick start](https://github.com/mjbots/moteus/blob/d37bff0ff9798594801469bc899c47e3425f8375/docs/quick-start.md): bare-board users mount the magnet/controller; the generic developer-kit path says the motor is already mounted, configured, calibrated and tuned. This does not prove the contents or geometry of the blocked current product pages, nor preclude an authentic manufacturing assembly task. It does prevent treating the kit as evidence that every purchaser performs manual gap adjustment.

New exact leads supplied by the user:

| Source | Executor result | Claim status |
|---|---|---|
| [moteus-r4-11-developer-kit](https://mjbots.com/products/moteus-r4-11-developer-kit) | Proxy tunnel403 | Matched mj5208/controller/magnet/bracket is **externally located/user-supplied**, not independently re-read from this page |
| [moteus-devkit-bracket](https://mjbots.com/products/moteus-devkit-bracket) | Proxy tunnel403 | A manufacturer STEP is **externally located/user-supplied**; no download/geometry inspection or verified STEP URL from this page |

[Exact request/error records](evidence/N077-novelty-hardware-gate/http-source-attempts.json), [publisher hashes/provenance](evidence/N077-novelty-hardware-gate/publisher-source-manifest.json).

**Is the matched bracket's gap mechanically fixed? UNKNOWN in our independently inspected evidence.** No adjustable slots, shim stack, movable standoff or free gap-setting operation was established. Conversely, blocked pages are not proof that the bracket is fixed or lacks adjustment. The already inspected r4.5 controller envelope is not a verified complete r4.11/mj5208/bracket assembly. We did not graft it onto assumed motor dimensions.

The decision does **not** depend on the403s. Even taking the user's matched-hardware lead as correct, a genuine bracket and CAD do not by themselves demonstrate a new central physical ability. Since novelty did not survive, the conditional second-priority CAD compatibility/fixed-gap investigation was **not advanced**. No magnetic performance, fastening torque, mechanical compatibility or completed YAM-access result is claimed.

## 4. Allocation moves to unrelated, documented physical families

A bounded follow-on acquisition located and read actual **manufacturer/designer-published procedures**, not another magnetic encoder or calibration fixture: Source Robotics' [PAROL6 repository](https://github.com/Source-Robotics/PAROL6-Desktop-robot-arm/tree/e2169c163244d647739cc34fc5da15c24b042a61). Two manuals and the BOM were downloaded through publisher Git objects. Relevant diagrams were visually inspected. This is a source gate only; no CAD reconstruction, mechanism prototype or full robot assembly was started.

### A. Toothed-belt loop installation on an actual robot drive

[PAROL6 assembly manual](https://github.com/Source-Robotics/PAROL6-Desktop-robot-arm/blob/e2169c163244d647739cc34fc5da15c24b042a61/Building%20instructions/Parol%20building%20instructions.pdf), version1.2 rev1 dated27.10.2023, **PDF pages43–44**: route the actual wires/tubes through the elbow first, put the J4 belt over the two pulleys in the illustrated assembly configuration, then fit tension bearings at the designated locations. Page18 describes paired tension bearings. The [BOM](https://github.com/Source-Robotics/PAROL6-Desktop-robot-arm/blob/e2169c163244d647739cc34fc5da15c24b042a61/BOM/README.md) lists the J4 belt as **HTD3 201,6mm width**; exact vendor/tooth/material compatibility still needs binding. This is a documented robot-belt family related to bank N035, **not** a claim to have verified the original Gates automotive spring-tensioner task.

The central candidate ability is acquiring and installing the initially uninstalled flexible toothed loop through the genuine drive's assembly constraints. Do not substitute a pre-seated rigid loop and make tension the only task. The published STL paths for the elbow and output pulley are present, but were not downloaded or validated as matched complete interface CAD.

**Immediate novelty caution found before promotion:** official [#2203](https://github.com/robocurve/benchmark-tasks/pull/2203) already proposes setting robot timing-belt tension while holding a sliding motor mount and tightening two clamps. Its task.json/README were read at **`cb29b8fc8d4ca1d6a237d91d4932115d9db7598b`**. Its belt is **already seated at reset**. A potentially different loop-acquisition/installation skill remains to compare; a different belt size or tension-bearing design alone is insufficient. **No novelty clearance or prototype allocation.** Do not borrow #2203's2.5N force or numerical pass band for PAROL6.

Next inexpensive kill gate: compare actual initially-uninstalled loop fitting against current belt-installation tasks, then bind pulley/belt/harness geometry and inspect how the real loop gets into place. Stop if only ordinary tension setting remains, if the operation needs an invented split belt or omitted assembly obstruction, or if stock-YAM purchase is unavailable. No arbitrary spring tensioner, deformation law or tension target is justified by the PDF.

### B. Structural robot-link splicing with dowels and adhesive

[PAROL6 small-print-bed modification](https://github.com/Source-Robotics/PAROL6-Desktop-robot-arm/blob/e2169c163244d647739cc34fc5da15c24b042a61/Building%20instructions/Parol%20small%20print%20bed%20modification.pdf), **PDF pages9–12**: prepare the real upper-arm seam/holes, dry-fit four6×22mm solid dowels into the two printed halves, then apply the specified thin adhesive films and close/clamp the structural seam. Page11 gives13mm receiving depth in B and11mm in A, leaving9mm exposed from B; page12 cautions against filling blind pin holes with epoxy and calls for an18° seam-aware clamping arrangement. Pages14–18 separately describe the three-pin turret lap joint. These are structural joining procedures, not zero-reference fixturing.

The source's indicated4–6h set/24h full cure is a **guide statement**, not a validated cure law for a named adhesive. This makes the full bonded outcome an expensive candidate; a dry-fit-only endpoint may omit its useful purpose. No bonding, cure, strength test or material simulation was performed.

**Immediate novelty caution:** official [#2003](https://github.com/robocurve/benchmark-tasks/pull/2003) already joins two boards on multiple dowels while keeping their seam square. Its task.json/README were read at **`0de69b91145c4d8be4727cb46153ba12acdb7da2`**; the reset is a reusable dry fit and glue is not modeled. Four metal pins/PETG rather than three wood dowels is not sufficient originality. Any distinct central adhesive preparation/application/clamping operation would have to remain genuine and consequential; omitting it would risk another pin/socket variant. The search shows an open “Not accepted” label, which is **not** a finding that its reservation expired. **Research reserve only; no implementation allocation.**

Next inexpensive kill gate: full legitimate-operation comparison and assessment of whether the actual bonded outcome can be scored and reproduced with acceptable cure/reset cost. Stop if only aligned dry insertion can be modeled, or if bond retention needs a scripted attachment/cure shortcut. No original robot-building/AI-impact clearance follows merely from a robot part number or an optional printer-bed modification.

Both families have now-read manufacturer procedures. **Neither is declared novel, source-geometry-complete, robot-feasible or GPU-ready.** The extra comparisons prevent replacing one unexamined encoder overlap with another obvious overlap. [Manual hashes/pages](evidence/N077-novelty-hardware-gate/publisher-source-manifest.json), [bounded official searches](evidence/N077-novelty-hardware-gate/different-family-official-searches.json), [replacement-comparator file pins](evidence/N077-novelty-hardware-gate/different-family-comparator-files.json). These searches are not exhaustive board clearance. No replacement implementation has been selected.

## 5. Final gate record

| Gate | Result |
|---|---|
| Semantic novelty vs #2212 | **FAIL for queue promotion:** corresponding on-axis encoder objects, robot-motor setting, central registration/retention and installation outcome; no essential distinct documented manipulation established |
| Manufacturer operation | **Verified at pinned publisher-doc level:** rigid rotor magnet, sensor centering, appropriate retained gap; new exact product-page contents remain externally located |
| Matched mj5208/r4.11/bracket CAD and fixed-gap claim | **Not established; conditional second priority not advanced after novelty failure** |
| CPU prototype / YAM trial | **Not started** |
| Decision | **PARK N077** |
| New research allocation | Uninstalled robot-belt loop fitting and actual structural adhesive splicing, with read procedures and identified competitor gates; neither cleared for implementation |

Verification consisted of successful shell/Git access, immutable task/source extraction, static reading/AST parsing, PDF text extraction and selected diagram inspection. No candidate mechanism code, simulation, GPU/Brev/Dream/paid evaluation, procurement, messages to other teams or official submission occurred. KER/N022/N040 remain parked; N013/N006 remain excluded.
