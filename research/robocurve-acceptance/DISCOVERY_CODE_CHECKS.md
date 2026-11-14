# Fresh-discovery comparison evidence

This stage compares new concepts, not the four old rejected packages. Source retrieval used public Git/GitHub. The exact commits, source paths and hashes are in evidence/discovery-code-manifest.json;35 additional PR discussions are retained in evidence/discovery-pr-discussions.json. Fourteen new task packages were retrieved for inspection, but not every helper/asset line was read. The observations below come from actual metadata/scorer source reads. Other comparator references are marked as definition/title-level where applicable; none is claimed to be an independently reproduced native run.

| Source | Concrete code/definition finding | Discovery consequence |
|---|---|---|
|#1916, close-cable-carrier-over-robot-cable.py `score` L379|Scores actual carrier links, both cables, latched crossbars, released/still hold and sticky strain-relief slip.|N023 repeats an earlier carrier-filling operation. Do not rank it as a new industrial capability.|
|#757, strip_a_wire_end_in_a_stripping_station.py `score` L306 and task.json|Controls lever cut/retention/pull; disclosed event model moves removed insulation segments and uses real-size rigid cable.|N011 hand-stripper is not automatically new merely because the tool differs.|
|#741, crimp_a_terminal_onto_a_cable_end.py `score` L291 and task.json|Combines valid cable depth, lever-triggered crimp, extraction, rest and arms-home. Physical pull test is specified; simulation substitutes a crimp event.|N012/N018 need more than a different ferrule/connector. Do not copy the old home-pose requirement into current outcomes.|
|#1892, hose-clamp-barb/task.json|Real goal is hose fully on pump barb and clamp tight; worm-drive screw angle/axial proxy; rigid hose, drawn-only bead and no driver reaction torque disclosed.|N031/N036 cannot claim novelty from irrigation hose size or spring clamp alone. Missing essential hose mechanics is a fidelity risk, not automatic permission for us.|
|#1681, cuff_scoring.py `evaluate` L137|Scores correctly sized rigid arch position over a square beam; no fabric wrapping/fastening.|N062 genuine cuff wrapping is not shown equivalent by this rejected rigid stand-in.|
|#1380, bp-manual-auscultate/task.json, commit1fb5a8d|Starts with cuff already wrapped. Goal is pumping/bleeding with chestpiece listening contact.|N062 addresses an omitted physical setup step, but other cuff tasks still need screening. No source-backed claim of complete novelty.|
|#2006, rail-plate-mount/task.py `score` L122 and task.json|Two screws fix DIN rail to a plate, with simplified thread model.|N099 server slide-rail bracket capture is not the same named rail operation. Compare full mounting topology, not the word “rail.”|
|#1835, punch_down_blade_to_waste_side.py `score` L369|Checks IDC conductor seat, trimming wrong run, tool clearance/release and stillness.|N020 has an earlier directly matching operation; N017 ribbon IDC must justify a different perpendicular multiwire-contact problem.|
|#1561, task.py `_score` L241 / `score` L262|External circlip spread/seat, damage latch, groove-turn check, put-down requirement.|N039 internal ring is a serious component-family variation, not an automatically new pliers operation.|
|#1882, scoring.py `evaluate` L34|Earlier chain connector uses wide bores and keeper-position predicates; reviewer requests actual matched link and positive retention.|N084 is not made new by correcting that earlier mockup; avoid the existing operation unless its independent origin/availability and distinct skill are established.|
|#1468, pop_rivet.py `score` L272|Full score depends on correct rivet tier and actual stillness accounting; reviewer separately checks manufacturer-rated grip range.|N002 directly overlaps. N003 rivet-nut setting may share the same mandrel-upset capability despite a different future purpose.|
|#1854, task.py `score` L353|Calls `_update`, `_count_still`, `_pull_step` and returns `_done`; the discussion specifically requires a physical tightness/pull check.|N001 encounters an earlier same-kind toggle installation; exclude from the leading portfolio rather than swapping anchor brand.|
|#1411, wire-nut-twisted-on/task.json|Two conductors, helical connector, real tug/insulation coverage/snug criteria; simulation uses coil/slide proxies.|N015 directly overlaps, so it was removed from the ranked twenty.|
|#1264, join-the-duct-sections-and-drive-the-cleats/task.json|Same duct/flange/drive-cleat operation, explicitly scaled and simplified without normal hammer/bent-end mechanics.|N010 overlaps an earlier proposed operation. Its problems do not establish our novelty.|
|#1335, replace-a-wiper-blade-holding-its-arm-off-the-glass/task.json|Real spring arm/J-hook exchange and collection, with snap-down guard and simplified hook slide.|N041 repeats the intended operation; removed from leading twenty.|
|#2037, shaft-key-pulley/task.json|Loose parallel key, shaft keyway, pulley keyed bore, shoulder seating and released hold.|N043 directly overlaps a newly discovered earlier submission.|
|#17, drip-loop-before-entry/task.json|Cable gland is fixed, with cable welded outside it; score measures released drip-loop geometry.|N013 gland assembly is a different proposed operation from this existing gland-labelled routing task.|

## External definitions actually read this stage

At BEHAVIOR-1K commitb544acbbb76b461349bcba21f93b870b11da6608:

- `bddl3/bddl/activity_definitions/emptying_trash_cans/problem0.bddl`: debris goes into sacks placed on floor; the goal does not specify fitting a fresh liner cuff to a bin.
- `bddl3/bddl/activity_definitions/clean_a_vacuum/problem0.bddl`: cleaning/disinfection of vacuum and canister; does not establish the dust-bag collar replacement operation.
- `bddl3/bddl/activity_definitions/mopping_floors/problem0.bddl`: remove floor stain, with bucket/mop/soap in scene; the goal does not explicitly test wringer moisture extraction.

These are exact local distinctions, not proofs that all1018 definitions or all external suites omit a procedure. Earlier LIBERO/RoboCasa/RoboDojo/DataCenterBench pinned inspections remain available in EXTERNAL_BENCHMARK_SCOPE.md. Correct DexHand source and complete external retrieval remain gaps.

## Search and source limits

Fifty-six candidate keyword queries were attempted. Forty returned rendered results; sixteen returned HTTP429 and were not interpreted as zero matches. Search results include title/body text and can miss alternate terms; no candidate is novelty-cleared from a brand or zero-hit query. Publisher/O*NET/BLS probes across35 destinations returned network-proxy403. Exact logs are preserved. No alternate proxy, access-control bypass or invented source passage was used.
