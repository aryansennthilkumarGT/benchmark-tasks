# Care, commercial cleaning and household-care discovery

No BUILD-READY candidate survives this domain screen. CC21 is a source-complete high-risk reserve, not a top15 quota filler; other deep assessments are exact source/novelty gates, and CC26 was rejected despite excellent source/CAD.

26 new operation leads were screened, including six additions after the original manufacturer domains failed. Five serious operations received detailed assessments; they are not five recommended finalists. Previously parked N061–N069, N075 and N087 operations were excluded. No earlier rejected task was silently resurrected.

## Verified occupational evidence

|Occupation|2025 national employment|Relevant actual O*NET30.2 Core work|
|---|---:|---|
|Janitors and cleaners37-2011|2,209,760|9538 restroom supply;9540 floor cleaning;9541 prescribed use of cleaners/power equipment (08/2023)|
|Maids and housekeepers37-2012|860,670|9566 floor scrubbing/waxing;9563 replenish supplies. Laundry9575 is Supplemental, so household dryer care is evaluated under societal relatability.|
|Nursing assistants31-1131|1,448,910|19331 daily living/toileting support;19339 supply/collect/empty bedpans;19340 patient transport is Core08/2020.|
|LPNs29-2061|648,410|508 prescribed medication administration;517 assemble/use care equipment. These do not automatically justify every specialist device.|

Counts were independently extracted from the pinned MIT mirror of BLS OEWS2025 national, all-industry, all-ownership rows. Complete downloaded CSV SHA256 `e4d6ee917dddaea9b32f0f5d392fc7873d44b77c22c33fd4b521be3a7763aede` matches prior provenance. Exact rows are in [the count evidence](care_cleaning/evidence/oews2025-care-cleaning.json). Core classifications were parsed from the pinned original-attributed O*NET30.2 Parquet SHA256 `56ee34d07b956eead1582b2f978a0fe16ab36eebfbd55b7bfb5f65b9e02948ab`; [selected task rows](care_cleaning/evidence/onet30.2-care-cleaning.json) retain task IDs, dates and respondent counts.

**Version correction:** the older07/2013 nursing-assistant CSV calls transport19340 Supplemental; the08/2020 row in30.2 calls it Core. The newer row controls. General treatment setup19337 remains Supplemental. An early research message using the old row was corrected before this deliverable.

## Initial operation ledger

A missing URL means the exact procedure was not located, not that an invented URL is being passed off as a source. Product-family knowledge is a discovery lead until an original procedure is actually read.

|ID|New operation|Source read status|Disposition/reason|
|---|---|---|---|
|CC01|[Mount a Tennant T300 removable rear squeegee assembly](https://assets.tennantco.com/globalassets/webassets/operators/t300/en_9014501.pdf)|BLOCKED403|DEEP_SOURCE_GATE: Routine setup might qualify; exact bracket/knob/hose operation and full-size access not verified.|
|CC02|[Install the T300 disk pad driver on its drive hub](https://assets.tennantco.com/globalassets/webassets/operators/t300/en_9014501.pdf)|BLOCKED403|DEMOTE: Large under-deck disk and drive-hub geometry unknown; #2169 keyed brush-roll seating is a close ability neighbor.|
|CC03|Install the Nilfisk SC250 cylindrical roller brush|NOT_RETRIEVED|ELIMINATE: Current #2169 already tests asymmetric drive-end/bearing-end brush seating and retaining flap; a brand change is insufficient.|
|CC04|Exchange a Kärcher NT30/1 flat pleated filter cassette|NOT_RETRIEVED|DEMOTE: Close #1107 filter-under-cover operation, no verified distinct retention path.|
|CC05|Crank a Numatic Henry manual cable reel while feeding cable|NOT_RETRIEVED|RESERVE_DISCOVERY_ONLY: Different crank/feed operation, but cable contact model and actual HVR200 procedure not read.|
|CC06|Release an Unger ErgoTec squeegee channel and lock its replacement|NOT_RETRIEVED|DEMOTE: Routine cleaning Core does not prove channel service is regular; #1978 operates squeegee but does not exchange channel.|
|CC07|Open a Rubbermaid Invader clamp, change wet mop head and reclamp|NOT_RETRIEVED|RESERVE_DISCOVERY_ONLY: Distinct textile clamp rather than old N087 wringer; authentic clamp dimensions and everyday replacement frequency unproved.|
|CC08|Attach a HYGEN microfiber pad across its flat mop frame|NOT_RETRIEVED|DEMOTE: Pad contact/deformation essential; simple hook-and-loop attachment and related #2105 head/handle assembly reduce novelty.|
|CC09|Refill Tork Xpress multifold towels without trapping the stack|NOT_RETRIEVED|ELIMINATE: Stack placement/replenishment too elementary absent a distinct documented mechanism.|
|CC10|Load and prime a Tork Matic H1 paper-towel roll|NOT_RETRIEVED|DEEP_SOURCE_GATE: Routine restroom supply Core verified; exact feed-nip threading path versus #2027/#1852 not verified.|
|CC11|Seat a GOJO ADX12 soap refill pump cartridge|NOT_RETRIEVED|DEMOTE: Authentic disposable pump/cartridge interface unknown; ordinary cartridge replacement may overlap accepted #312.|
|CC12|Load a 3M Easy Shine applicator bag and route its delivery tube|NOT_RETRIEVED|HIGH_RISK_DISCOVERY_ONLY: Floor-finish preparation is plausible Core, but exact connector, flexible tube path and fluid endpoint unverified.|
|CC13|Connect a Kärcher Puzzi upholstery spray/extraction nozzle|NOT_RETRIEVED|DEMOTE: Hose union alone insufficiently different from existing quick-connect work; no verified consequential multichannel coupling.|
|CC14|Prepare an empty Drive11135 drop-arm commode and replace its pail|NOT_RETRIEVED|DEEP_SOURCE_GATE: Toileting assistance/bedpan supply Core verified; actual arm latch/pail-support mechanism remains uninspected.|
|CC15|Attach the specified empty Invacare Reliant450 sling loops to its spreader|NOT_RETRIEVED|HIGH_RISK_DISCOVERY_ONLY: Authentic empty care equipment; no improvised patient jig, but sling deformation/load-path testing would be essential.|
|CC16|Lower and positively relatch an empty Hillrom Centrella side rail|NOT_RETRIEVED|DEMOTE: Real routine care, but full-size rail sweep and release mechanism unknown; simple lever operation alone weak.|
|CC17|Deploy and latch a Drive Nitro rollator from folded storage|NOT_RETRIEVED|DEMOTE: Distinct from old N065 leg-height setting but folded-frame handling likely overlaps #2280 and requires large sweep.|
|CC18|Set both Invacare wheelchair wheel locks before a transfer|NOT_RETRIEVED|ELIMINATE: Authentic likely regular action but two lever presses alone provide weak independent task importance/novelty.|
|CC19|Crush a placebo in a Silent Knight pouch using its lever press|NOT_RETRIEVED|HIGH_RISK_DISCOVERY_ONLY: LPN medication administration Core verified; actual lever procedure/pouch interfaces and meaningful particle-size score unverified.|
|CC20|Assemble the baffle, cap and air tube of an Omron NE-C28P nebulizer kit|NOT_RETRIEVED|DEMOTE: Named real equipment, but respiratory care setup cannot inherit all nursing jobs without actual procedure; small baffle grasp risky.|
|CC21|[Equip an iRobot Create3 cargo bay with the maker-designed rear caster](https://github.com/iRobotEducation/create3_docs/blob/9fb1510bbceb0e01c4764ddc458da59487519dca/docs/hw/mechanical.md)|READ_MANUFACTURER_GITHUB_CAD|DEEP_HIGH_RISK_RESERVE: Direct robot equipping; real published3part mount and complete printable geometry, but7mm retaining tab and caster-shaft details constrain YAM.|
|CC22|[Reassemble the BCED15 three-layer rear-drum lint filter after cleaning](https://github.com/gaoyz1235/RealAppliance/blob/fb7bd3c6ad7e26472d89719efe55d281cff8c528/manuals_pdfs/054_dryer_en_fr_sp/054_EN.pdf)|READ_ORIGINAL_MANUAL_MIRROR_P17|DEEP_SOURCE_GATE: Every-use actual manufacturer procedure; different from drawer screen, but latch/retention geometry absent and #598/#876/#1964 compete.|
|CC23|[Refit the BCED15 air-intake filter housing by its upward latch](https://github.com/gaoyz1235/RealAppliance/blob/fb7bd3c6ad7e26472d89719efe55d281cff8c528/manuals_pdfs/054_dryer_en_fr_sp/054_EN.pdf)|READ_ORIGINAL_MANUAL_MIRROR_P18|DEMOTE: Authentic before/after-each-use action; too close to filter-cartridge reinsertion family without extra essential ability.|
|CC24|[Remove, rinse and replace BLACK+DECKER washer built-in lint filter every10cycles](https://github.com/gaoyz1235/RealAppliance/blob/fb7bd3c6ad7e26472d89719efe55d281cff8c528/manuals_pdfs/046_washingmachine_en_fr/046_EN.pdf)|READ_ORIGINAL_MANUAL_MIRROR|DEMOTE: Manual verifies every10cycles but does not give enough physical latch detail; filter swap family already crowded.|
|CC25|[Open the same washer pump-filter compartment for monthly cleaning](https://github.com/gaoyz1235/RealAppliance/blob/fb7bd3c6ad7e26472d89719efe55d281cff8c528/manuals_pdfs/046_washingmachine_en_fr/046_EN.pdf)|READ_ORIGINAL_MANUAL_MIRROR|ELIMINATE: Monthly recommendation read, no detailed verified mechanism; household recognition of a specialist pump service is insufficient.|
|CC26|[Mount the Create3 faceplate over four locating pins and rotate into retention](https://github.com/iRobotEducation/create3_docs/blob/9fb1510bbceb0e01c4764ddc458da59487519dca/docs/hw/mechanical.md)|READ_MANUFACTURER_GITHUB_CAD|ELIMINATE_NOVELTY: Excellent procedure and exact STEP but accepted #34 already preserves keyed drop/twist undercut retention;4vs2pins and10vs90deg do not rescue it.|

## Detailed assessments

All score tolerances and low-load verification forces below are proposed benchmark design choices, not manufacturer specifications. No full-YAM reach, collision, grasp or wrench test ran. Source STEP/STL measurements prove only dimensions of the supplied model.

### CC21. Retain a swivelling rear caster in the Create3 maker-designed payload support

**78/100 — HIGH-RISK RESERVE.** Components20/25/20/20/15: 18/20/20/8/12. Not currently recommended for the root top15.

**Importance:** Impact on AI timelines. person: Robot-lab builder equipping a Create3 mobile research platform duty: Manufacturer explains rear caster is needed when added payload moves centre of gravity behind drive wheels, preventing sliding on the back edge. This is actual robot equipping; no occupation count is required. regular_core_count: Not applicable to AI category; do not borrow janitor totals from Roomba ancestry. source_pin: iRobotEducation/create3_docs@9fb1510bbceb0e01c4764ddc458da59487519dca docs/hw/mechanical.md

**Source:** url: https://github.com/iRobotEducation/create3_docs/blob/9fb1510bbceb0e01c4764ddc458da59487519dca/docs/hw/mechanical.md status: READ manufacturer original GitHub; exploded diagram inspected;3STLs parsed; robot STEP12solids parsed hash_manifest: care_cleaning/evidence/create3-source-manifest.json

**Hardware and interfaces:**
- component: Rear caster attachment; verified: Maker STL98.3489×82.4882×57.7941mm; protrudes54mm behind robot; mounted between handle and cargo-bay cable passthrough; material: 3D printed polymer, exact resin/print settings not specified; mass: unknown; cannot infer actual mass from mesh alone
- component: Top latch; verified: Maker STL24.7942×15.8733×7.5mm;2M3/#4 self-tapping screws; material: 3D printed polymer
- component: Caster lock; verified: Maker STL6.9998×11.4070×1.8mm;1M3/#4 self-tapping screw; material: 3D printed polymer
- component: Roomba front caster4624869; verified: Named exact maker-linked product and exploded diagram; vertical spindle through printed bearing opening; tab retains it while swivel remains free; unknown: Exact spindle neck/shoulder dimensions and actual pullout/rolling torque; not present in simplified publicSTEP
- component: Create3 cargo bay/chassis; verified: Original publicSTEP contains actual cargo bay and simplified chassis,12solids; cargo-bay attachment interfaces source derived; support: Normal service fixture or assembled robot support must react screwdriver torque without hiding required surfaces
- component: Screwdriver and3screws; verified: Screws specified by maker; unknown: Screw lengths/head style and torque not specified; choose compatible ordinary screws and document

**Starting state:** Assembled real cargo bay supported in service orientation; rear caster mount, top latch, caster, lock tab and3specified screws laid in a small-parts tray, screwdriver in ordinary stand. A lower-cost subtask may start mount already attached; this is declared partial real assembly, not an invented interface.

**Instruction:** “Install the rear caster support on the Create3 cargo bay, secure its caster so it cannot pull out, and leave the wheel able to swivel and roll with both hands clear.”

**Central ability:** Assemble a load-supporting swivel bearing with positive axial retention without clamping the bearing solid; support must be retained to the real cargo-bay bridge.

**Bimanual/sequence:** One arm braces the printed mount/caster or cargo bay while the other places latch/retainer and turns screwdriver. Full assembly requires two-sided access and several genuine fasteners; loose7mm tab is a major difficulty.

**Externally physical scoring:**
- partial: 0.25 mount and latch seated at source mating surfaces but not all fasteners secured;0.5 mount remains retained after hands release and its2screws are seated;0.75 caster spindle fully seated and physical tab engages its neck/shoulder.
- full: 1.0 only when mount fasteners and caster retainer are mechanically retained, source-scale wheel supports intended rear point, and caster passes an independent low-load axial tug plus full360deg swivel and wheel-roll test after release. Proposed1N tug for2s and a light spring-scale turn; final loads must be calibrated against actual caster, not presented as rated capability.
- measurement: Photos of latch and screw heads plus ruler/feeler gauge; spring scale and a manual360deg swivel check; collision/retention geometry in sim, no proximity weld.
- invalid: Broken tab/mount, extracted spindle, missing retention screw, or locked-up caster gives0for affected assembly; fixture movement must be bounded.
- reset: Undo3screws, remove caster/tab/top latch/mount, inspect self-tapping bosses for wear; reusable threaded inserts would change manufacturer interface and need separate justification.

**Wrong solutions and catch:**
- Drop wheel near opening without spindle engagement → Source-defined bearing insertion and axial tug fail.
- Clamp spindle solid with tab/screw → Free360deg swivel and wheel-roll checks fail.
- Attach wheel but leave rear mount loose on cargo bay → Independent support retention test fails.
- Hold assembly during final test → Hands-clear2s gate and independent test after release.

**Novelty:** Caster bearing retention/free motion is a different endpoint from simply mating a keyed drive or placing a panel. However ordinary small screw/bracket assembly could still make novelty weak; no categorical acceptance claim.

**Actual current official comparators:**
- [#34](https://github.com/robocurve/benchmark-tasks/pull/34) MERGED, head `ccf48db36528bda27f670e94b7ea37f9b71c659a`, head commit 2026-11-07T17:57:08-08:00; created 2026-11-03T09:51:43Z; closed 2026-11-12T04:00:46Z. Files preserved/inspected include README.md, demo.py, partkit.py, task.json, task.py. Keyed bayonet cap uses push/twist undercut retention, no free-running bearing; caster should not be converted into this mechanism.
- [#1986](https://github.com/robocurve/benchmark-tasks/pull/1986) OPEN, head `e8ecd21da83c33bfe2107962a4d1a28495b1e336`, head commit 2026-11-14T12:51:18-08:00; created 2026-11-14T07:29:22Z; closed None. Files preserved/inspected include README.md, mechanism.py, parts.py, task.json, test_trim_clip.py, trim_clip.py. Push-in panel clip fastens2aligned sheets with compliant capture; caster tab creates axial retention while preserving swivel, rather than immobilizing sheets.
- [#2003](https://github.com/robocurve/benchmark-tasks/pull/2003) OPEN, head `cbf99b266424ced8264791d9fde0783f6b5b0ac7`, head commit 2026-11-16T16:39:49+05:30; created 2026-11-14T11:14:00Z; closed None. Files preserved/inspected include README.md, linkdemo.py, linkkit.py, task.json, task.py, test_scoring.py. Three dowels align and join rigid boards; no bearing or independent retaining tab.

**Stock-YAM planning screen:**
- grasp: 98mm mount exceeds nominal94mm aperture across full width, but exposed ribs/base or caster fork may allow normal pinches; exact stock pads/palm require CAD check.7×11×1.8mm loose tab is not proven acquirable.
- palm_wrist: Deep internal tab/screw is accessible to long screwdriver shaft; palm cannot be assumed to enter printed pocket.
- tools: Normal driver handle acquisition/wrench capacity unverified; no magnetic/preloaded tool claim unless genuine ordinary bit holder is documented.
- reaction: Real cargo-bay bridge or service support takes screw torque; one hand may brace.
- paths: Seat mount around cargo bridge, top latch from above, caster from below, tab/driver from inside; possible unavoidable reorientation.
- clearance: No collision/reach/grasp test run.

**Hard blockers:**
- Stock-YAM acquisition/placement of7mm flat retainer unproved; cannot enlarge it.
- Exact caster spindle retention shoulder geometry not supplied as CAD; source exploded diagram establishes mechanism but additional dimensions may be needed before contact implementation.

**Cheapest falsifier:** Import maker3STLs, reconstruct only source-compatible spindle envelope, overlay actual YAM finger/palm hulls around tab-placement and screw approach. Kill if ordinary tool access cannot place original7mm tab or if a faithful spindle cannot be grounded in the diagram/bore.

**Relative effort:** High within portfolio:3parts,3fasteners, swivel support, two-sided access. Lower-cost authentic subtask can preattach support but must retain caster-bearing installation.

**Strongest rejection:** This is a tiny screw-and-tab accessory build, and normal YAM cannot handle the tab; a free-spinning wheel glued in place would erase the task. Resolved: False. Importance/source are resolved as actual robot equipping; small-part tool access, essential spindle geometry and strongest semantic distinction remain unresolved.

### CC22. Reassemble and retain a BCED15 three-layer rear-drum lint filter

**63/100 — PROMISING BUT SOURCE-GATED.** Components20/25/20/20/15: 17/12/17/6/11. Not currently recommended for the root top15.

**Importance:** Societal relatability. person: Ordinary user of a compact clothes dryer duty: BLACK+DECKER BCED15 manual p17 explicitly requires lint-filter assembly cleaning before or after each use, separation into3parts and reassembly in order. Household scenario is dryer lint care, not a niche maintenance occupation. jobs: Do not claim housekeeping laundry is Core: inspected O*NET37-2012 task9575 laundry is Supplemental. Society category must stand on firsthand household familiarity.

**Source:** url: https://github.com/gaoyz1235/RealAppliance/blob/fb7bd3c6ad7e26472d89719efe55d281cff8c528/manuals_pdfs/054_dryer_en_fr_sp/054_EN.pdf status: READ original BLACK+DECKER BCED15 manual p17 visually plus text pin: fb7bd3c6ad7e26472d89719efe55d281cff8c528 manifest: care_cleaning/evidence/realappliance-source-manifest.json

**Hardware and interfaces:**
- component: Exhaust vent shroud; verified: Rigid circular cover with4grip holes; turn in either direction until bump then pull outward for removal; unknown: Diameter, grip-hole sizes, underside retention profile, turning angle and detent/press-fit design not dimensioned
- component: Lint filter; verified: Circular mesh/filter piece with central opening, distinct from shroud; unknown: Frame material, rigidity, thickness, exact nesting feature
- component: Exhaust filter; verified: Separate circular filter medium behind lint filter; sequence specified exhaustfilter→lintfilter→ventshroud; unknown: Material/compliance and central opening dimensions
- component: Rear drum recessed receiving seat; verified: Maker requires align full assembly with rear-drum recess and press firmly until secured; unknown: Actual socket/retaining-lug geometry and drum depth
- component: Soft brush or vacuum; verified: Maker cleaning tools; optional to benchmark scope starting after cleaning; support: Whole cooled unplugged compact dryer or authentic drum section preserving reach/retention; do not invent giant grip tabs

**Starting state:** Unplugged cool BCED15 with door open, all3real filter pieces clean and separated on a tray. Retained full drum opening/recess geometry; no lint-removal model is needed when instruction explicitly begins after cleaning.

**Instruction:** “Reassemble the three cleaned filter parts in the maker’s order, refit them securely in the back of the dryer drum, and release them.”

**Central ability:** Nested thin filter assembly retained in a recessed vertical drum seat; order and all layers must survive hands release and a gentle axial test.

**Bimanual/sequence:** One arm stabilizes shroud/filter stack while the other aligns flexible medium and pushes/turns assembly; depth of drum can obstruct both palms. Bimanual necessity is not established.

**Externally physical scoring:**
- partial: 0.25 all3parts nested in correct order outside drum;0.5 complete stack in drum recess but not retained;0.75 source-defined physical retention engaged but hands touching.
- full: 1.0 complete stack correct order and orientation, fully seated to proposed≤2mm visible rim gap, hands≥30mm clear for2s, then survives a proposed1N axial tug without coming free. Load/gap are benchmark choices requiring actual product calibration.
- measurement: Before/after photos of every layer and assembly edge, ruler/feeler gauge, gentle pull test after release; final outer cover alone cannot prove hidden layer present, so setup/video must track labelled original layers or posttrial reopen.
- invalid: Missing exhaustfilter/lintfilter, torn medium, broken clips, loose cover or fake rigid filter replacement invalidates full credit.
- reset: Pull/turn assembly out per manufacturer, separate3pieces and place on start tray; inspect medium and retention features.

**Wrong solutions and catch:**
- Install only decorative vent shroud → All3source pieces tracked; posttrial reopen verifies layers.
- Place complete stack in recess but do not retain → Hands-clear pull test fails.
- Reverse/misnest filter layers → Exposed edge/central opening and posttrial order inspection fail.
- Hold or wedge against a gripper → Hands≥30mm clear and pull test after release.

**Novelty:** Unlike linear lint drawer #598/#876, actual rear drum unit has separate3layer assembly and rotational removal. However it may reduce to generic filter reinstallation plus bayonet #34/#1964; do not count extra layers as proof of novelty.

**Actual current official comparators:**
- [#598](https://github.com/robocurve/benchmark-tasks/pull/598) CLOSED, head `706ebc6921ec8a99e6b1b2fc90766ab70fa8b503`, head commit 2026-11-07T16:59:03-05:00; created 2026-11-05T20:01:21Z; closed 2026-11-12T07:15:33Z. Files preserved/inspected include README.md, lint_screen_clean.py, task.json. Single rigid lint tray in open slot plus loose lint flakes; no multilayer circular filter or rear-drum retention.
- [#876](https://github.com/robocurve/benchmark-tasks/pull/876) CLOSED, head `c5ee82a749f4bf61989619b07555e47e97093466`, head commit 2026-11-06T21:41:23Z; created 2026-11-06T21:41:26Z; closed 2026-11-12T07:01:28Z. Files preserved/inspected include README.md, clean_lint_drawer.py, task.json, test_scorer.py. Lift rigid lint pad into bin then linearly slide screen to stop; different preparation from nested stack, but same everyday endpoint.
- [#1964](https://github.com/robocurve/benchmark-tasks/pull/1964) CLOSED, head `7df32b52be6c57ea20e503f78e83b79d5c2639ab`, head commit 2026-11-13T17:08:05-08:00; created 2026-11-14T01:08:09Z; closed 2026-11-15T19:06:25Z. Files preserved/inspected include README.md, dishwasher_filter.py, mechanism.py, task.json. Lower flat filter under tabs then cylindrical upper bayonet cup locks; nearest multicomponent filter retention, serious novelty objection.
- [#34](https://github.com/robocurve/benchmark-tasks/pull/34) MERGED, head `ccf48db36528bda27f670e94b7ea37f9b71c659a`, head commit 2026-11-07T17:57:08-08:00; created 2026-11-03T09:51:43Z; closed 2026-11-12T04:00:46Z. Files preserved/inspected include README.md, demo.py, partkit.py, task.json, task.py. Accepted bayonet physical undercut lock; actual BCED15 retention must be inspected before claiming a different ability.

**Stock-YAM planning screen:**
- scale_mass: No source dimensions/mass for filter; image only is insufficient to assert aperture or reach.
- grasp: 4grip holes may not admit stock fingers; outer rim pinch and two-hand stack support are planning ideas only.
- palm_wrist: Back of real drum can require deep reach through circular door; entire palm/wrist path untested.
- tools: None needed for reassembly; brush only if cleaning added, which would require lint physics.
- reaction: Original drum rear wall supplies axial seating reaction, whole dryer must remain stable.
- paths: Carry separated layers, nest without wrinkle, insert along drum axis; unknown securing motion.
- clearance: No CPU/YAM tests run.

**Hard blockers:**
- Exact latch/retention surfaces, filter dimensions and medium rigidity missing; essential mechanism cannot become an arbitrary latch.
- Novelty versus #1964/#34 unresolved; extra layer count is insufficient.
- Root external RealAppliance benchmark task-overlap audit must clear exact operation.

**Cheapest falsifier:** Obtain one manufacturer/authorized parts exploded view or product measurement showing shroud backside and receiving recess; compare actual securing motion to #1964. Kill if mechanism is just the existing generic twistlock or stock fingers cannot enter at real drum depth.

**Relative effort:** Medium-high; source procedure clear, but hidden geometry/medium and full-drum access dominate.

**Strongest rejection:** An already-covered lint/filter task with extra discs; missing original retaining mechanism invites fabricated latch. Resolved: False. Actual every-use manufacturer procedure verified, but neither essential geometry nor semantic difference is closed.

### CC10. Thread and prime a Tork Matic H1 towel roll through its actual feed mechanism

**56/100 — PROMISING BUT SOURCE-GATED.** Components20/25/20/20/15: 19/10/6/10/11. Not currently recommended for the root top15.

**Importance:** Impact on jobs. person: Janitors and cleaners37-2011 count: 2209760 count_source: MIT/BLS-attributed2025 pinned CSV hash e4d6ee917dddaea9b32f0f5d392fc7873d44b77c22c33fd4b521be3a7763aede Core_task: {'id': 9538, 'text': 'Service, clean, or supply restrooms.', 'date': '08/2023', 'incumbents': 62} qualification: Routine consumable loading directly supplies restrooms; no equipment repair workforce borrowing.

**Source:** url: None manufacturer_target: https://www.torkusa.com/ status: Exact551000/H1 loading instructions NOT RETRIEVED; do not assert a feed path from memory.

**Hardware and interfaces:**
- component: Tork Matic551000 H1 dispenser; known: Named actual product family; fixed wall-mount restroom unit; unknown: Exact revision-specific roller nip, lead-in, feed wheel or auto-thread feature, cover latch and internal clearances
- component: Compatible H1 paper towel roll/core; known: Consumable roll; unknown: Correct SKU/core format, width/diameter, web direction and leader length must match exact manual
- component: Dispenser key; known: Common accessory hypothesis only; unknown: Actual key/latch style not inspected
- component: Support; proposal: Full-size dispenser on normal vertical wall board; holder rigid enough to react paper pull, without altered roller gaps

**Starting state:** Actual551000 dispenser fixed in usual wall orientation, empty, cover closed; correct full roll on tray and real service key available. Exact leader state follows manufacturer after source gate.

**Instruction:** “Load the replacement towel roll, thread it according to this dispenser’s instructions, prime it so a full towel can feed, and close the dispenser.”

**Central ability:** Flexible web enters real feed nip and becomes a functioning paper-feed path, rather than merely parking a roll near an outlet.

**Bimanual/sequence:** One hand holds/supports roll or opened cover while second presents web to feed path and operates manual advance if maker requires it; necessity depends on exact manual.

**Externally physical scoring:**
- partial: 0.25 new roll mechanically supported on correct hubs;0.5 correct web path through actual feed nip;0.75 one towel dispenses without jam while cover open.
- full: 1.0 cover latched, hands clear, independent manual dispense yields specified full sheet length without pulling roll out or tearing prematurely; proposed≥200mm cleanly advanced if compatible with actual roll.
- measurement: Photograph spindle/support and feed path before closing, ruler on dispensed web, manual dispenser activation after robot releases.
- invalid: Wrong roll/core, jam, web draped past outlet but outside rollers, broken cover/roller invalidates full credit.
- reset: Open with real key, remove roll, rewind consumed web if reusable and reset original leader; damaged paper replaced.

**Wrong solutions and catch:**
- Set roll in dispenser but never engage feed nip → Independent dispense test fails.
- Drape leader outside closed lid → Trace actual nip path and advance test, no position-only feed flag.
- Load backwards or off one spindle → Support inspection and full-sheet functional feed fail.
- Hold paper taut to mimic feeding → Robot released before independent dispense.

**Novelty:** Functioning traction through compliant web/rollers might differ from printer roll placement #2027 and jumbo tissue spindle relocation #1852, but actual feed mechanism remains unverified; generic reel loading is not novel.

**Actual current official comparators:**
- [#1852](https://github.com/robocurve/benchmark-tasks/pull/1852) OPEN, head `27df2d5642f9ff1c17edad061da839d8961c2473`, head commit 2026-11-14T11:02:20-05:00; created 2026-11-13T03:23:47Z; closed None. Files preserved/inspected include README.md, jumbo_tissue_dispenser_stub_to_reserve.py, task.json. Active OPEN. Stub-to-reserve spindle transfer with release buttons and changeover shutter; no flexible web through roller nip.
- [#2027](https://github.com/robocurve/benchmark-tasks/pull/2027) CLOSED, head `60abf2f0239ec030f4c9301ff4d839a94dc0bb1a`, head commit 2026-11-14T22:28:04+05:30; created 2026-11-14T16:58:14Z; closed 2026-11-15T02:00:34Z. Files preserved/inspected include README.md, demo_plan.py, display.py, geometry.py, logic.py, mechkit.py, scoring.py, task.json, task.py, test_receipt_printer_roll_reload_v2.py. CLOSED. Whole roll carries rigid3mm paper strip into exit notch, no actual nip/roll spin. This remains legitimate paper-reload comparator and cannot be dismissed just because simplified.

**Stock-YAM planning screen:**
- grasp: Roll diameter may exceed aperture; grip core/roll ends only after compatible-core size source. Paper leader needs controlled light pinch.
- palm_wrist: Wall cabinet opening/hinged cover may trap palm; full hand approach untested.
- tool: Key acquisition/rotation may need precision grip; actual key unknown.
- reaction: Wall board supplies feed-pull reaction.
- paths: Hub loading, leader bend/traction around rollers, cover sweep; all dependent on manual.
- clearance: Planning only.

**Hard blockers:**
- Exact product-specific feed path and essential roller/retention interfaces not inspected.
- Flexible paper cannot be rigid-strip substituted if web threading is novelty.
- Novelty against active #1852 and closed #2027 requires actual functional feed evidence.

**Cheapest falsifier:** Read actual551000 loading pictogram and obtain one internal photo/drawing. Kill if auto-thread requires only drop-in roll or if preserved skill is equivalent to #1852/#2027.

**Relative effort:** Medium-high due compliant paper/traction; simplest faithful short-strip/spring-roller model after source gate.

**Strongest rejection:** A paper dispenser is just a printer reload or tissue dispenser with a different label. Resolved: False. Core occupation is resolved; distinguishing nip-threading mechanism is a hypothesis until manual is read.

### CC01. Mount the full-size removable rear squeegee on a T300 scrubber

**54/100 — PROMISING BUT SOURCE-GATED.** Components20/25/20/20/15: 18/15/3/7/11. Not currently recommended for the root top15.

**Importance:** Impact on jobs. person: Janitors and cleaners37-2011 count: 2209760 Core_tasks: [{'id': 9540, 'text': 'Clean building floors by sweeping, mopping, scrubbing, or vacuuming.', 'date': '08/2023', 'incumbents': 62}, {'id': 9541, 'text': 'Follow procedures for the use of chemical cleaners and power equipment to prevent damage to floors and fixtures.', 'date': '08/2023', 'incumbents': 62}] qualification: Only ordinary pre/post-cleaning installation qualifies; an occasional blade repair/reversal cannot borrow all janitor jobs.

**Source:** url: https://assets.tennantco.com/globalassets/webassets/operators/t300/en_9014501.pdf status: OEM PDF and authorized-dealer alternatives403; not inspected; product/manual number is a search lead, not a verified passage.

**Hardware and interfaces:**
- component: Tennant T300 matching rear squeegee assembly; known: Real named walk-behind scrubber family; hypothesis: Wide curved metal carrier, rubber wiping blades and vacuum nipple; proposed700–900mm span is an unverified scale estimate
- component: Matching scrubber lift/mount receiver and hand knobs; hypothesis: Dual slot/stud hanging interfaces with hand-knob clamping, not verified for exact revision
- component: Vacuum hose; hypothesis: Short flexible hose seals onto squeegee nipple; exact engagement unknown
- component: Support; proposal: Actual scrubber in manufacturer service state, or original full-scale mount receiver on representative stable service stand only if procedure remains authentic; unknown: Deck height, rear-chassis collision envelope, knob torque, mount and blade mass

**Starting state:** Detached original matched squeegee on tray; scrubber powered off and squeegee lift in maker-specified position. No scaled tabletop substitute or enlarged knobs.

**Instruction:** “Attach this squeegee to its scrubber mount, secure both retainers, connect the vacuum hose, and leave the assembly ready to lower to the floor.”

**Central ability:** Wide carrier alignment on two separated supports plus securing the genuine retention interfaces and hose seal; actual mechanism must be established.

**Bimanual/sequence:** Carry and level wide assembly with two hands, support while tightening one side, reposition and complete other side; mechanical fixture is normal chassis.

**Externally physical scoring:**
- partial: 0.25 both supports engaged without falling when released;0.5 both actual clamps retained;0.75 correct hose connection.
- full: 1.0 source retention engaged on both sides and hose connected, hands clear, lowering through actual sweep gives blade contact at both ends on level floor and carrier remains retained under proposed2N horizontal test. All margins need hardware calibration.
- measurement: Ruler/feeler gauge at both mount supports and blade contacts; simple pull test and source-specified hose-seat mark. No cleaning-fluid model necessary for setup endpoint.
- invalid: Only one side hung, knobs missing, carrier reversed, damaged blade or hose on false nipple invalidates relevant credit.
- reset: Raise lift, disconnect hose, loosen actual knobs and remove squeegee per source; no consumable.

**Wrong solutions and catch:**
- Hang on one support and prop other on floor → Both support positions/retention and lift-lower test.
- Tighten knobs beside rather than through brackets → Actual captured slot/stud interface and independent pull.
- Put hose near nipple without seal → Seating depth/physical attachment inspection.
- Reverse carrier so blade edge lifts → Correct source orientation and both-end floor-contact test.

**Novelty:** Squeegee operation #1978 and debris sweep #1915 do not mount a wide machine attachment; however two-knob bracket mounting may have no independent ability beyond generic panel/tool support assembly.

**Actual current official comparators:**
- [#1986](https://github.com/robocurve/benchmark-tasks/pull/1986) OPEN, head `e8ecd21da83c33bfe2107962a4d1a28495b1e336`, head commit 2026-11-14T12:51:18-08:00; created 2026-11-14T07:29:22Z; closed None. Files preserved/inspected include README.md, mechanism.py, parts.py, task.json, test_trim_clip.py, trim_clip.py. Two-sheet alignment and push clip capture, rather than spaced hanger/clamp mounting. Different mechanism is possible but not yet documented.
- [#2003](https://github.com/robocurve/benchmark-tasks/pull/2003) OPEN, head `cbf99b266424ced8264791d9fde0783f6b5b0ac7`, head commit 2026-11-16T16:39:49+05:30; created 2026-11-14T11:14:00Z; closed None. Files preserved/inspected include README.md, linkdemo.py, linkkit.py, task.json, task.py, test_scoring.py. Simultaneous multipoint dowel joining means dual support alignment alone is not enough novelty.
- [#1940](https://github.com/robocurve/benchmark-tasks/pull/1940) CLOSED, head `d531294d80b79d1f09b5759e707abd1c8aa4ac6a`, head commit 2026-11-14T02:08:00+05:30; created 2026-11-13T20:38:08Z; closed 2026-11-14T06:23:29Z. Files preserved/inspected include README.md, linkdemo.py, linkkit.py, task.json, task.py, test_scoring.py. CLOSED wheelchair hanger release/swing/lift: actual mount kinematics must be compared if T300 also uses drop-on hanger.

**Stock-YAM planning screen:**
- grasp: Wide span probably needs two arms, assembly mass unverified; do not claim payload feasibility.
- palm_wrist: Knobs/hose potentially behind carrier and chassis; palms/wrists may be blocked even if fingertips reach.
- tools: Hypothesized tool-free hand knobs; actual wrench/torque requirement unknown.
- reaction: Heavy real chassis reacts clamp and hose forces; fixed receiver stand must not change mating interface.
- paths: Two-slot simultaneous capture and chassis-lift sweep, correct hose routing.
- clearance: No verified path/reach test.

**Hard blockers:**
- Exact manufacturer installation procedure and clamp mechanism not inspected.
- Full-size geometry/mass and ordinary equipment service height are unknown.
- Core regularity of this exact removable attachment setup not established by manual.

**Cheapest falsifier:** Obtain correct T300 operator section and dimensioned rear mount/squeegee view. Kill if operation is rare blade maintenance, if real assembly cannot fit normal YAM two-arm envelope, or if mounting reduces to existing generic dual-feature placement.

**Relative effort:** High before sources; potentially medium after original receiver/assembly mesh exists.

**Strongest rejection:** A scaled cleaning-machine bracket puzzle justified with all janitors, with essential mounting hardware invented. Resolved: False. General floor-cleaning Core verified; all product-specific authenticity, frequency and scale gates stay explicit.

### CC14. Restore the empty drop-arm commode for toileting use

**48/100 — PROMISING BUT SOURCE-GATED.** Components20/25/20/20/15: 19/8/3/9/9. Not currently recommended for the root top15.

**Importance:** Impact on jobs. person: Nursing assistants31-1131 count: 1448910 Core_tasks: [{'id': 19331, 'text': 'Provide physical support to assist patients to perform daily living activities, such as getting out of bed, bathing, dressing, using the toilet, standing, walking, or exercising.', 'date': '08/2020', 'incumbents': 83}, {'id': 19339, 'text': 'Supply, collect, or empty bedpans.', 'date': '08/2020', 'incumbents': 84}] qualification: Empty real bedside commode preparation is plausibly routine care; exact11135 bucket/arm handling must be documented, not borrowed from general nursing equipment setup Supplemental19337.

**Source:** url: None manufacturer_target: https://www.drivemedical.com/ status: OEM domain403;11135 manual not retrieved

**Hardware and interfaces:**
- component: Drive11135 padded drop-arm commode; known: Named actual bedside commode; unknown: Exact release lever/button, swing axis, positive arm-catch geometry, pail support/mount path, dimensions and revision
- component: Original matching pail/lid/handle; hypothesis: Removable under-seat pail; must not invent slide rails if original hangs on ring
- component: Chair frame and feet; proposal: Full-size empty commode on level floor or service-height platform reflecting real handling, not a miniature trainer
- component: Tools; proposal: None unless actual manual specifies; no patient/manikin needed for arm/pail preparation

**Starting state:** Empty genuine11135 frame, one drop arm lowered, clean original pail outside on tray; original lid/seat in maker-consistent starting state. No patient.

**Instruction:** “Refit the clean pail and raise and lock the lowered arm, leaving the commode ready for use with both hands clear.”

**Central ability:** Pail capture under constrained seat geometry and positive arm retention, if actual manufacturer geometry supports distinct actions.

**Bimanual/sequence:** One hand may stabilize frame/arm while other operates latch or aligns pail. Necessity not established; do not add artificial two-handed lock.

**Externally physical scoring:**
- partial: 0.25 original pail correctly supported under opening;0.5 arm at use position but latch not verified;0.75 pail correctly seated and genuine catch fully engaged but hands touching.
- full: 1.0 pail supported with mouth under seat aperture and no tilt/spill path, original arm catch engaged, hands clear, independent gentle outward/downward arm tug fails to release it. Proposed1N tug2s is a benchmark check, not clinical load rating.
- measurement: Photo of pail support interfaces and catch, ruler on seat/pail alignment, manual tug after robot releases.
- invalid: Pail balancing on floor or unsupported edge, arm merely leaned upright, broken catch, moved/tipped frame gives no full credit.
- reset: Release real arm catch, lower arm, remove pail by actual documented path; clean empty equipment only.

**Wrong solutions and catch:**
- Stand pail below commode on floor → Original pail support interface must carry it.
- Hold raised arm without locking → Hands-clear physical catch inspection/tug.
- Leave pail cocked on one edge → Both original supports/seat aperture alignment and tilt check.
- Tip whole commode to make arm look raised → Frame upright/feet on level support gate.

**Novelty:** Empty commode preparation differs in use from wheelchair footrest clearance, but a generic bucket placement+button latch may not justify a new benchmark. Exact original mechanism is decisive.

**Actual current official comparators:**
- [#1940](https://github.com/robocurve/benchmark-tasks/pull/1940) CLOSED, head `d531294d80b79d1f09b5759e707abd1c8aa4ac6a`, head commit 2026-11-14T02:08:00+05:30; created 2026-11-13T20:38:08Z; closed 2026-11-14T06:23:29Z. Files preserved/inspected include README.md, linkdemo.py, linkkit.py, task.json, task.py, test_scoring.py. Wheelchair hanger latch held while swinging90deg then lifting off keeper pin; if commode uses equivalent latch/swing, substantial overlap.
- [#2034](https://github.com/robocurve/benchmark-tasks/pull/2034) CLOSED, head `cbfae41522d70964f1e5a8966976642e6843cc5c`, head commit 2026-11-14T13:40:39-05:00; created 2026-11-14T18:50:29Z; closed 2026-11-15T02:02:25Z. Files preserved/inspected include README.md, task.json, toilet_seat_quick_release_hinge.py. Toilet seat simultaneously placed on two posts and button-retained; commode cannot be relabelled dual-socket seat mount.
- [#1986](https://github.com/robocurve/benchmark-tasks/pull/1986) OPEN, head `e8ecd21da83c33bfe2107962a4d1a28495b1e336`, head commit 2026-11-14T12:51:18-08:00; created 2026-11-14T07:29:22Z; closed None. Files preserved/inspected include README.md, mechanism.py, parts.py, task.json, test_trim_clip.py, trim_clip.py. Simple aligned-hole fastening is already represented; original commode cannot be replaced with fake pin/clip jig.

**Stock-YAM planning screen:**
- grasp: Full-size pail handle and padded arm may be graspable; actual cross-sections/mass unknown.
- palm_wrist: Under-seat space may fit only fingers and collide with palm; no clearance evidence.
- tools: None expected, not verified.
- reaction: Frame feet supply reaction; pushing arm may tip/move empty chair without stabilization.
- paths: Under-seat pail insertion plus arm swing and latch; exact order unknown.
- clearance: Planning only; no stock geometry test.

**Hard blockers:**
- Actual11135 arm catch and pail supports unknown; cannot invent a clinical jig.
- Standalone mechanical complexity/novelty may remain weak after source retrieval.

**Cheapest falsifier:** Obtain original11135 manual/parts drawing; kill if pail merely sits on shelf or arm release is equivalent to existing wheelchair/seat task without a distinct essential ability.

**Relative effort:** Medium if authentic interfaces are simple; low research priority given current source and novelty gaps.

**Strongest rejection:** Routine patient-care language disguises a generic bucket/lever task and unverified hardware. Resolved: False. Core toileting duties and workforce verified, but actual product mechanism and distinct physical ability remain unsupported.

## Decisive exclusions despite useful sources

**Create3 faceplate (CC26):** manufacturer original procedure, FAQ and complete publicSTEP were retrieved. FAQ says position approximately10° off-center without downward force, rotate clockwise at thumbrests until click/centered. STEP yielded12solids; faceplate294.177×292.875×15mm, four8mm pin heads. This still matches the accepted [#34 bayonet task](https://github.com/robocurve/benchmark-tasks/pull/34) at its essential distributed keyed drop/twist undercut retention. Number of pins, amount of turn and robot label do not establish a different ability. Critic independently read manufacturer text and actual #34 task.json. Do not include it merely because the CAD is excellent.

**SC250 roller brush (CC03):** [#2169](https://github.com/robocurve/benchmark-tasks/pull/2169) CLOSED2026-11-16T06:39:36Z at `55214b46c76aa2a934adf87b5df321a588133eef`; its actual task seats a round stub and square drive stub and closes drive-end retainer. Closed status is not by itself a perpetual ownership block. The same legitimate physical skill remains prior art.

**Vacuum bag:** old N075 was not placed in the new26, and current [#2334](https://github.com/robocurve/benchmark-tasks/pull/2334) OPEN at `999bcc9f9665273d89f97e04a079edc0c706e2f4` is the exact collar-out/new-collar-in dustbag task.

**False manual repository:** `springchun0801/manuals-hub@67c6bbb2170702b59ace03e0f17028c689195039` was actually inspected. It is an HTML mock interface with every manual link `#`, not a manufacturer manual mirror. It supplied no procedure evidence.

## Executed checks and their practical limits

- Current officialGitHub HTML semantic searches with explicit200/429 logs
- Fetch20exact PRheads into unique refs/final-discovery/care/prNN without checkout/reset/FETCH_HEAD
- Read close task.json,README and mechanism/scoring excerpts, preserve hashed files
- Parse pinnedO*NET30.2Parquet and freshly downloaded100MB BLS-attributed2025CSV; exact selected rows saved
- Download manufacturerCreate3GitHub docs/CAD; parse3STL trianglebounds and originalSTEP12solids
- Retrieve5original-manualPDFs via attributedRealAppliance mirror; pdftotext;BCED15p17visually inspected,p18textread,046caretextread,078controltextread;040/100image-heavy extractionnotread.

Not executed:
- No robotIK/collision/grasp/wrench/path validation
- No mechanism implementation/demonstration
- No GPU/Dream/paid computation/procurement/submission
- No exhaustive currentPRcoverage: some search batches429; liveboard inaccessible
- No new acceptance claim

Current official main accepted180 inventory was also read from the root shared artifact. [The official competitor ledger](care_cleaning/evidence/official-competitor-ledger.json) retains exact current state, source-head match, dates and file hashes. Search batches retain actualHTTP200/429 outcomes; no empty result from a429was treated as clearance.

[Manufacturer source manifest](care_cleaning/evidence/create3-source-manifest.json) pins all Create3 procedure/CAD/image assets. [Original-manual mirror manifest](care_cleaning/evidence/realappliance-source-manifest.json) records all5PDFs actually retrieved, their hashes and read status. BCED15 PDF/p17render are retained; other large PDFs can be fetched from immutable URLs and extracted text is retained. The18.6MB Create3 publicSTEP was fetched and parsed but is not duplicated in the research artifact; [CAD bounds output](care_cleaning/evidence/create3-public-cad-inspection.json) and exact source hash permit reproduction.

Root performs the broader external benchmark audit. A manufacturer manual appearing in RealAppliance does not imply task clearance. Exact RealAppliance operation overlap remains a gate forCC22.
