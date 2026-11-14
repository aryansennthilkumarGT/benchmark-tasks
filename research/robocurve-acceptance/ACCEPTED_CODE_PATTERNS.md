# Accepted implementation patterns:20 targeted static dossiers

These twenty tasks were selected for diverse mechanics and authors: assembly, construction/plumbing, electrical installation, data-center service, hydraulic service, manufacturing and familiar household work. The review read scorer/mechanism/controller source sections, metadata, documentation and available tests/receipts. **This is a targeted static code review, not an exhaustive read of every helper/asset line or a native runtime reproduction.** For larger packages, the remaining asset/contact audit is explicitly outstanding. Source locations and hashes are preserved so another reviewer can extend it. Do not report these as twenty independently reproduced demonstrations.

All paths below are pinned to official main `add552504c5ccfedc201e2967f3230505f1e56fd`. Each dossier includes the task's latest acceptance/source commit and the traced merged PR. “Reported” means submitted evidence. No native expert, Dream or real physical trial was run here.

## din-rail-mount — [PR#37](https://github.com/robocurve/benchmark-tasks/pull/37)

**Operation/category:** Hook the fixed upper edge, pivot the housing and force the spring slider past the lower rail lip. End clamps prevent sliding on from an end. Impact on jobs.

**Actual implementation:** task.py geometry/_update uses transformed hook/back points, latch slider return, milestone history and20-position stillness window. partkit.py authors actual articulated sliders; demo.py uses observed module pose for staged hook/push.

**Limit and published evidence:** 1,200 steps (1 minute at 20 Hz); Dream-1 run: 0.0; demo: 1.0. Media `M-BTH2R5`. Media records were not downloaded or visually verified. Latest task commit `8ac86a9ae420f091850e4b12a4f5789443f46e2b`.

**Review inference / limits:** No-hook and no-push controls are documented; top lip2mm versus real1mm is disclosed. Published420-step success is an author claim. Generalization: preserve constrained motion order, rather than adding a decorative latch.

**Source map** (entry points and state transitions; all exact files pinned):

- [`tasks/din-rail-mount/partkit.py`](https://github.com/robocurve/benchmark-tasks/blob/add552504c5ccfedc201e2967f3230505f1e56fd/tasks/din-rail-mount/partkit.py#L128): `_spawn_part` L128, `on_step` L317, `on_reset` L323, `_task_step` L363, `reset` L369.
- [`tasks/din-rail-mount/task.py`](https://github.com/robocurve/benchmark-tasks/blob/add552504c5ccfedc201e2967f3230505f1e56fd/tasks/din-rail-mount/task.py#L116): `_reset_state` L116, `_count_step` L121, `_update` L145, `success` L178, `score` L184.

**Assets/reset/tests:** No separate test*.py suite found; documented controller variants are not equivalent to a full test suite. Geometry is authored/generated in code. Read reset callbacks together with README reset instructions; neither static tests nor success receipts prove mechanical reset on hardware.

## push-fit-release — [PR#662](https://github.com/robocurve/benchmark-tasks/pull/662)

**Operation/category:** Hold a release collet while extracting a pipe along its bore. Impact on jobs.

**Actual implementation:** task.py _release raises a stiff tooth drive only while collet travel>=2.5mm; _update latches fitting movement>5mm and records press/pull/out. partkit.py authors both sliders. demo.py simultaneously presses and pulls, then lays down.

**Limit and published evidence:** 1,200 steps (1 minute at 20 Hz); Dream-1 run: 0.0; demo: 1.0. Media `M-S6D5AK`. Media records were not downloaded or visually verified. Latest task commit `5543e22cf91613417ce8e90f613935a8f8d9f0aa`.

**Review inference / limits:** Explicit cone/tooth and grooved-pipe surrogate, square bore/no O-ring. Release-then-pull and no-press controls matter. This is a recognizable fitting operation, not permission to invent any spring-release service fixture.

**Source map** (entry points and state transitions; all exact files pinned):

- [`tasks/push-fit-release/partkit.py`](https://github.com/robocurve/benchmark-tasks/blob/add552504c5ccfedc201e2967f3230505f1e56fd/tasks/push-fit-release/partkit.py#L163): `_spawn_part` L163, `on_step` L412, `on_reset` L418, `_task_step` L458, `reset` L464.
- [`tasks/push-fit-release/task.py`](https://github.com/robocurve/benchmark-tasks/blob/add552504c5ccfedc201e2967f3230505f1e56fd/tasks/push-fit-release/task.py#L120): `_reset_state` L120, `_update` L151, `success` L172, `score` L177.

**Assets/reset/tests:** No separate test*.py suite found; documented controller variants are not equivalent to a full test suite. Geometry is authored/generated in code. Read reset callbacks together with README reset instructions; neither static tests nor success receipts prove mechanical reset on hardware.

## bayonet-mate — [PR#34](https://github.com/robocurve/benchmark-tasks/pull/34)

**Operation/category:** Axially insert two lugs, push below a roof against a spring plate, then quarter-turn under the roof. Impact on jobs.

**Actual implementation:** task.py actual slot/roof/stop colliders and PLATE slider; cap_in_box and _update check insertion, rotation, seating, box displacement/tilt and all-finger release/stillness. demo.py grips/stabilizes and follows the push-turn sequence.

**Limit and published evidence:** 1,200 steps (1 minute at 20 Hz); Dream-1 run: 0.0; demo: 1.0. Media `M-FG3VMR`. Media records were not downloaded or visually verified. Latest task commit `28037f7109b16bd63939771d6f32a7564f7d7d95`.

**Review inference / limits:** #34 requested observable demo state and a1-second stillness test before acceptance. Full credit requires retention after release; an inserted cap still held does not suffice.

**Source map** (entry points and state transitions; all exact files pinned):

- [`tasks/bayonet-mate/partkit.py`](https://github.com/robocurve/benchmark-tasks/blob/add552504c5ccfedc201e2967f3230505f1e56fd/tasks/bayonet-mate/partkit.py#L110): `_spawn_part` L110, `on_step` L311, `on_reset` L317, `_task_step` L357, `reset` L363.
- [`tasks/bayonet-mate/task.py`](https://github.com/robocurve/benchmark-tasks/blob/add552504c5ccfedc201e2967f3230505f1e56fd/tasks/bayonet-mate/task.py#L87): `_reset_state` L87, `_update` L126, `success` L160, `score` L167.

**Assets/reset/tests:** No separate test*.py suite found; documented controller variants are not equivalent to a full test suite. Geometry is authored/generated in code. Read reset callbacks together with README reset instructions; neither static tests nor success receipts prove mechanical reset on hardware.

## hold-an-m2-drive-flat-and-latch-it — [PR#692](https://github.com/robocurve/benchmark-tasks/pull/692)

**Operation/category:** Press a spring-up M.2 card flat while rotating a separate latch over its end. Impact on AI timelines.

**Actual implementation:** hold_an_m2_drive_flat_and_latch_it.py defines card/latch hinges, up-spring and colliding latch arm; _status/_points report flatness and latch angle plus gripper clearance. bodykit.py installs mechanisms and clears per-episode state. Waypoint demo is in the task file.

**Limit and published evidence:** 1,200 steps (60 s at 20 Hz); Dream-1 run: 0.0; demo: 1.0. Media `M-5M4XXV`. Media records were not downloaded or visually verified. Latest task commit `7a2638c4ec47d36ec5974cf086bd12cedda9c7ac`.

**Review inference / limits:** The card starts already in its socket: this is retention, not full drive installation. Stem height is explicitly authored. Do not infer permission to remove connectors from a task claiming complete storage exchange.

**Source map** (entry points and state transitions; all exact files pinned):

- [`tasks/hold-an-m2-drive-flat-and-latch-it/bodykit.py`](https://github.com/robocurve/benchmark-tasks/blob/add552504c5ccfedc201e2967f3230505f1e56fd/tasks/hold-an-m2-drive-flat-and-latch-it/bodykit.py#L424): `_spawn_body` L424, `on_reset` L580, `on_step` L586, `build` L152, `reset` L598, `_task_step` L606.
- [`tasks/hold-an-m2-drive-flat-and-latch-it/hold_an_m2_drive_flat_and_latch_it.py`](https://github.com/robocurve/benchmark-tasks/blob/add552504c5ccfedc201e2967f3230505f1e56fd/tasks/hold-an-m2-drive-flat-and-latch-it/hold_an_m2_drive_flat_and_latch_it.py#L231): `score` L231, `success` L238, `demo` L348.

**Assets/reset/tests:** No separate test*.py suite found; documented controller variants are not equivalent to a full test suite. Geometry is authored/generated in code. Read reset callbacks together with README reset instructions; neither static tests nor success receipts prove mechanical reset on hardware.

## install-processor — [PR#891](https://github.com/robocurve/benchmark-tasks/pull/891)

**Operation/category:** Open a real socket lever/shield interlock, orient keyed loose CPU, close shield and catch. Impact on AI timelines.

**Actual implementation:** install_processor.py _seated/score require correct CPU position/rotation before shield/lever tiers. mechanism.py authors hinged shield, lever and spring catch; parts.py authors keyed loose body. demo phases and static tests include wrong keying and interlock checks.

**Limit and published evidence:** 3,000 steps (150 seconds at 20 Hz); Dream-1 run: 0.0; demo: 1.0. Media `M-GZ84M4`. Media records were not downloaded or visually verified. Latest task commit `039441f20e30416eb8e62c6fc811c12785a1f3b6`.

**Review inference / limits:** README cites Dell R260 operation. Rigid sprung catch substitutes for lever-wire flex; actual order and keyed seating remain. Published1051-action expert / Dream0 are receipts/metadata claims, not rerun here.

**Source map** (entry points and state transitions; all exact files pinned):

- [`tasks/install-processor/install_processor.py`](https://github.com/robocurve/benchmark-tasks/blob/add552504c5ccfedc201e2967f3230505f1e56fd/tasks/install-processor/install_processor.py#L185): `score` L185, `success` L198, `demo` L243.
- [`tasks/install-processor/mechanism.py`](https://github.com/robocurve/benchmark-tasks/blob/add552504c5ccfedc201e2967f3230505f1e56fd/tasks/install-processor/mechanism.py#L180): `_spawn` L180, `on_reset` L389, `patched_reset` L478, `patched_step` L496.
- [`tasks/install-processor/test_install_processor.py`](https://github.com/robocurve/benchmark-tasks/blob/add552504c5ccfedc201e2967f3230505f1e56fd/tasks/install-processor/test_install_processor.py#L68): `test_the_start_scores_zero` L68, `test_seated_with_the_shield_and_lever_shut_is_success` L72, `test_credit_climbs_with_each_step` L77, `test_demo_reaches_and_fits_the_run_limit` L147.

**Assets/reset/tests:** Tests are supplied in test_install_processor.py. Geometry is authored/generated in code. Read reset callbacks together with README reset instructions; neither static tests nor success receipts prove mechanical reset on hardware.

## compression-joint — [PR#1562](https://github.com/robocurve/benchmark-tasks/pull/1562)

**Operation/category:** Pipe home, olive first, nut next, then wrench tightening relative to snug. Impact on jobs.

**Actual implementation:** fittingkit.CompressionJoint.update tracks ring-on-pipe, thread engagement, spanner-flat capture, helical nut travel and irreversible overcompression. It explicitly poses nut/olive after thread capture; spanner jaws are visual-only. compression_joint.py _update/score impose useful sealed tiers and hold.

**Limit and published evidence:** 2,400 steps (2 minutes at 20 Hz); Dream-1 run: 0.0 (the left hand reaches down over the parts tray and the right over the spanner's board, but nothing is picked up or assembled); demo: 1.0 (success at step 1,913). Media `M-5GW2N7`. Media records were not downloaded or visually verified. Latest task commit `de817b994315d23b7e2abae35bdd5536e4ea32f8`.

**Review inference / limits:** #1562 required a physically calibrated snug reference and raw score correction. README specifies a2Nm pretrial line calibration and new olives. Accepted approximation does not certify true contact-threading or leak tightness.

**Source map** (entry points and state transitions; all exact files pinned):

- [`tasks/compression-joint/compression_joint.py`](https://github.com/robocurve/benchmark-tasks/blob/add552504c5ccfedc201e2967f3230505f1e56fd/tasks/compression-joint/compression_joint.py#L205): `_reset_state` L205, `_update` L212, `success` L229, `score` L238, `demo` L309.
- [`tasks/compression-joint/fittingkit.py`](https://github.com/robocurve/benchmark-tasks/blob/add552504c5ccfedc201e2967f3230505f1e56fd/tasks/compression-joint/fittingkit.py#L469): `on_reset` L469, `_spawn_body` L480, `update` L334, `reset` L821.
- [`tasks/compression-joint/test_compression_joint.py`](https://github.com/robocurve/benchmark-tasks/blob/add552504c5ccfedc201e2967f3230505f1e56fd/tasks/compression-joint/test_compression_joint.py#L51): `step` L51, `test_no_olive_scores_nothing` L221, `test_overtightened_scores_nothing_for_good` L227, `test_past_one_and_a_quarter_turns_scores_nothing` L233, `test_nothing_done_scores_nothing` L248, `test_the_demo_reaches_every_target_along_its_path` L259, `test_the_demo_passes_the_run_guards` L273, `test_the_demo_fits_the_run_limit` L279, `test_the_demo_drops_the_olive_before_the_nut` L283, `test_the_demo_keeps_the_spanner_hand_clear_until_the_left_hand_is_home` L288.

**Assets/reset/tests:** Tests are supplied in test_compression_joint.py. Geometry is authored/generated in code. Read reset callbacks together with README reset instructions; neither static tests nor success receipts prove mechanical reset on hardware.

## tube-bender — [PR#991](https://github.com/robocurve/benchmark-tasks/pull/991)

**Operation/category:** Overbend a copper tube to compensate for springback; judge after relaxing. Impact on jobs.

**Actual implementation:** task.py Trial.step reads lever joint and commands displayed tube angle; update keeps maximum lever-minus-springback set, overbend latch, clearance and settled_s. demo_script uses observed joint/pose feedback; mechkit authors lever return spring.

**Limit and published evidence:** 800 steps (40 s at 20 Hz); Dream-1 run: 0.0; demo: 1.0. Media `M-HQ7DCQ`. Media records were not downloaded or visually verified. Latest task commit `f19e584158e9976e04340b0565dd86455cfea7c1`.

**Review inference / limits:** Tube material deformation is a state model, not native deformable copper. #991 corrected raw score0.5/full mismatch and specified stock/temper/spring calibration. No blanket permission to miniaturize load-sensitive operations.

**Source map** (entry points and state transitions; all exact files pinned):

- [`tasks/tube-bender/demokit.py`](https://github.com/robocurve/benchmark-tasks/blob/add552504c5ccfedc201e2967f3230505f1e56fd/tasks/tube-bender/demokit.py#L479): `_step_limit` L479.
- [`tasks/tube-bender/mechkit.py`](https://github.com/robocurve/benchmark-tasks/blob/add552504c5ccfedc201e2967f3230505f1e56fd/tasks/tube-bender/mechkit.py#L757): `on_step` L757, `on_reset` L763, `build` L536, `task_step_hook` L820, `reset_hook` L829.
- [`tasks/tube-bender/task.py`](https://github.com/robocurve/benchmark-tasks/blob/add552504c5ccfedc201e2967f3230505f1e56fd/tasks/tube-bender/task.py#L155): `success` L155, `score` L160, `demo_script` L172, `reset` L95, `step` L108, `update` L117.

**Assets/reset/tests:** No separate test*.py suite found; documented controller variants are not equivalent to a full test suite. Geometry is authored/generated in code. Read reset callbacks together with README reset instructions; neither static tests nor success receipts prove mechanical reset on hardware.

## tram-milling-vise-with-indicator — [PR#1799](https://github.com/robocurve/benchmark-tasks/pull/1799)

**Operation/category:** Sweep an indicator, adjust a swivel vise, clamp, and resweep with adjustment hand clear. Impact on jobs.

**Actual implementation:** scoring.py TrammingScore.update requires continuous contacting sweep through both endpoints and center, probe not at stop, <=0.20mm variation, stable jaw and clamp contact. task.py observe uses native link pose/contact/joint values and moves the visual dial; demo is fixed waypoints without reading scoring state.

**Limit and published evidence:** 2400 control steps at 20 Hz; Dream 1 scored 0.0 in 2400 steps. The scripted demonstration scored 1.0 in 1056 steps.. Media `M-4LWV7V`. Media records were not downloaded or visually verified. Latest task commit `7035491f324fdecc90dda7a1aaac9c972f3ca3c1`.

**Review inference / limits:** Retightening can shift alignment; scorer invalidates verification on clamp/yaw change. Source includes measured_results.json and counterexamples. Real-world manual cited: Sherline3570; workforce numbers in README are submitted claims requiring direct BLS verification.

**Source map** (entry points and state transitions; all exact files pinned):

- [`tasks/tram-milling-vise-with-indicator/counterexamples.py`](https://github.com/robocurve/benchmark-tasks/blob/add552504c5ccfedc201e2967f3230505f1e56fd/tasks/tram-milling-vise-with-indicator/counterexamples.py#L8): `demo` L8.
- [`tasks/tram-milling-vise-with-indicator/native_contacts.py`](https://github.com/robocurve/benchmark-tasks/blob/add552504c5ccfedc201e2967f3230505f1e56fd/tasks/tram-milling-vise-with-indicator/native_contacts.py#L10): `reset` L10, `step` L72.
- [`tasks/tram-milling-vise-with-indicator/runtime/yam_articulated.py`](https://github.com/robocurve/benchmark-tasks/blob/add552504c5ccfedc201e2967f3230505f1e56fd/tasks/tram-milling-vise-with-indicator/runtime/yam_articulated.py#L128): `spawn` L128, `reset` L217, `_task_step` L226.
- [`tasks/tram-milling-vise-with-indicator/runtime/yam_articulated_base.py`](https://github.com/robocurve/benchmark-tasks/blob/add552504c5ccfedc201e2967f3230505f1e56fd/tasks/tram-milling-vise-with-indicator/runtime/yam_articulated_base.py#L63): `_install_spawn` L63, `spawn` L69, `reset` L118, `_task_step` L130.
- [`tasks/tram-milling-vise-with-indicator/scoring.py`](https://github.com/robocurve/benchmark-tasks/blob/add552504c5ccfedc201e2967f3230505f1e56fd/tasks/tram-milling-vise-with-indicator/scoring.py#L32): `update` L32.
- [`tasks/tram-milling-vise-with-indicator/task.py`](https://github.com/robocurve/benchmark-tasks/blob/add552504c5ccfedc201e2967f3230505f1e56fd/tasks/tram-milling-vise-with-indicator/task.py#L65): `reset_history` L65, `score` L128, `success` L129, `demo` L139.

**Assets/reset/tests:** No separate test*.py suite found; documented controller variants are not equivalent to a full test suite. Geometry is authored/generated in code. Read reset callbacks together with README reset instructions; neither static tests nor success receipts prove mechanical reset on hardware.

## sealant-cartridge-reload — [PR#312](https://github.com/robocurve/benchmark-tasks/pull/312)

**Operation/category:** Release ratchet, retract rod, exchange actual cartridge, re-engage piston behind replacement. Impact on jobs.

**Actual implementation:** build_scene.py authors prismatic/revolute mechanisms and pawl contact. sealant_reload/scoring.py evaluate uses replacement identity, tray bounds, piston gap, rod rotation, pawl angle, frame pose and complete robot envelope clearance. environment.py reset restores joints and checks initial score0; controller.py emits robot actions from phased plan.

**Limit and published evidence:** 2400 control steps at 20 Hz (120 seconds), fixed layout, seed 0.; Dream-1 run: 0.0; demo: 1.0. Media `M-GX5B82`. Media records were not downloaded or visually verified. Latest task commit `7541cfd225a03056b64668e696e7de6c21ae7171`.

**Review inference / limits:** validation receipts bind source fingerprints and native runs; tests include reverse cartridge, missing used cartridge, held support and permanent escape. Carrier/outlet geometry is explicitly simplified; do not transfer a dispensing-quality claim.

**Source map** (entry points and state transitions; all exact files pinned):

- [`tasks/sealant-cartridge-reload/sealant_reload/controller.py`](https://github.com/robocurve/benchmark-tasks/blob/add552504c5ccfedc201e2967f3230505f1e56fd/tasks/sealant-cartridge-reload/sealant_reload/controller.py#L14): `demo_plan` L14, `reset` L115.
- [`tasks/sealant-cartridge-reload/sealant_reload/environment.py`](https://github.com/robocurve/benchmark-tasks/blob/add552504c5ccfedc201e2967f3230505f1e56fd/tasks/sealant-cartridge-reload/sealant_reload/environment.py#L141): `reset` L141, `_task_step` L194.
- [`tasks/sealant-cartridge-reload/sealant_reload/scoring.py`](https://github.com/robocurve/benchmark-tasks/blob/add552504c5ccfedc201e2967f3230505f1e56fd/tasks/sealant-cartridge-reload/sealant_reload/scoring.py#L15): `reset` L15.
- [`tasks/sealant-cartridge-reload/tests/test_scoring.py`](https://github.com/robocurve/benchmark-tasks/blob/add552504c5ccfedc201e2967f3230505f1e56fd/tasks/sealant-cartridge-reload/tests/test_scoring.py#L23): `update_bounds` L23.

**Assets/reset/tests:** Tests are supplied in tests/test_scoring.py. Geometry is authored/generated in code. Read reset callbacks together with README reset instructions; neither static tests nor success receipts prove mechanical reset on hardware.

## rack-blanking-panel — [PR#943](https://github.com/robocurve/benchmark-tasks/pull/943)

**Operation/category:** Insert two panel pegs simultaneously into the target rack unit and leave it retained. Impact on AI timelines.

**Actual implementation:** build_assets.py generates actual square rack holes and panel peg chamfers. task.py _monitor transforms endpoints into rack holes; score distinguishes targetU6, single end home and released hold. scenekit.py checks robot hull clearance; demo.py carries by two ends.

**Limit and published evidence:** 2,400 steps (2 minutes at 20 Hz); Dream-1 run: 0.0 (both arms reached toward the stand, within about 1 cm of the panel, but the panel never moved); demo: 1.0. Media `M-XRFNCY`. Media records were not downloaded or visually verified. Latest task commit `da724577d44ce473887f25e554491a89e5d1ad44`.

**Review inference / limits:** Panel pegs are rigid slip fits rather than deforming clips; electrical/airflow claims are absent. Wrong rack unit and mismatched hole pair must fail. Dream0/demo1 are submitted results.

**Source map** (entry points and state transitions; all exact files pinned):

- [`tasks/rack-blanking-panel/build_assets.py`](https://github.com/robocurve/benchmark-tasks/blob/add552504c5ccfedc201e2967f3230505f1e56fd/tasks/rack-blanking-panel/build_assets.py#L193): `build_rack` L193, `build_stand` L236, `build_panel` L252.
- [`tasks/rack-blanking-panel/scenekit.py`](https://github.com/robocurve/benchmark-tasks/blob/add552504c5ccfedc201e2967f3230505f1e56fd/tasks/rack-blanking-panel/scenekit.py#L250): `on_step` L250, `on_reset` L256, `before_reset` L262, `task_step_hook` L302, `reset_hook` L316.
- [`tasks/rack-blanking-panel/task.py`](https://github.com/robocurve/benchmark-tasks/blob/add552504c5ccfedc201e2967f3230505f1e56fd/tasks/rack-blanking-panel/task.py#L46): `_reset_state` L46, `success` L139, `score` L145.

**Assets/reset/tests:** No separate test*.py suite found; documented controller variants are not equivalent to a full test suite. USD assets are supplied; source hashes are in inventory. Read reset callbacks together with README reset instructions; neither static tests nor success receipts prove mechanical reset on hardware.

## battery-pack-assembly — [PR#1303](https://github.com/robocurve/benchmark-tasks/pull/1303)

**Operation/category:** Load four correctly oriented18650 cells in standard holder halves and assemble a pack in a jig. Impact on jobs.

**Actual implementation:** pack_assembly.py uses holder_in_jig, cell_in_cup, lid_on, steps_done and _violation; USD holder halves have cup contacts/SDF collision. Demo separately handles holder halves and cells; tests reject wrong polarity, rim support and wrong lid orientation.

**Limit and published evidence:** 2,400 steps (2 minutes at 20 Hz); Dream-1 run: 0.0 (both arms reached over the jig, the holder halves and the cell tray again and again, but it never picked up a holder half or a cell); demo: 1.0 (all four steps by step 1892, success at step 1971). Media `M-5TZ7WL`. Media records were not downloaded or visually verified. Latest task commit `ba41d00e7b3f4f91908d74c287f5d1fbff4cc78d`.

**Review inference / limits:** Upper half retained only by weight; no spring-preload capture is claimed. Real holder/cell assembly is a different operation from the invented twelve-cell cross-key. Older success includes arms-home requirements: #1576 shows that should not be copied as a current universal rule.

**Source map** (entry points and state transitions; all exact files pinned):

- [`tasks/battery-pack-assembly/pack_assembly.py`](https://github.com/robocurve/benchmark-tasks/blob/add552504c5ccfedc201e2967f3230505f1e56fd/tasks/battery-pack-assembly/pack_assembly.py#L128): `_spawn` L128, `steps_done` L356, `success` L384, `score` L391, `demo` L634, `update` L345.
- [`tasks/battery-pack-assembly/test_pack_assembly.py`](https://github.com/robocurve/benchmark-tasks/blob/add552504c5ccfedc201e2967f3230505f1e56fd/tasks/battery-pack-assembly/test_pack_assembly.py#L110): `test_start_scores_zero` L110, `test_two_cells_seated_is_a_step` L143, `test_four_cells_seated_is_a_step` L152, `test_top_holder_on_the_cells_is_a_step` L196, `test_arms_not_home_is_not_success` L235, `test_still_holding_the_top_holder_is_not_success` L241, `test_moving_pack_is_not_success` L247, `test_cell_off_the_table_scores_zero` L253, `test_holder_off_the_table_scores_zero` L259, `test_demo_is_reachable` L265, `step` L59.

**Assets/reset/tests:** Tests are supplied in test_pack_assembly.py. USD assets are supplied; source hashes are in inventory. Read reset callbacks together with README reset instructions; neither static tests nor success receipts prove mechanical reset on hardware.

## split-cable-guide-retrofit — [PR#539](https://github.com/robocurve/benchmark-tasks/pull/539)

**Operation/category:** Close a split guide around an existing cable and prove unassisted drawer travel without unplugging. Impact on jobs.

**Actual implementation:** task.py Trial.step captures eligible guide at proof start, enforces installation before movement, plug_gap<=2mm, no assisted travel and released hold. run.py authors jointed slack loop, sleeve and native contact carriage.

**Limit and published evidence:** 800 steps (40 seconds at 20 Hz); Dream-1: 0.0 in 800 steps. Scripted demo: 1.0 in 463 steps.. Media `M-D4EQMT`. Media records were not downloaded or visually verified. Latest task commit `8d63660770df0d2c073674d1137973fb3bd2ae46`.

**Review inference / limits:** Tests reject travel-before-installation and restored violations. Clamp fit alone is insufficient: an independent mechanical functional test establishes a useful retrofit outcome. Gripper proximity is a disclosed assistance approximation.

**Source map** (entry points and state transitions; all exact files pinned):

- [`tasks/split-cable-guide-retrofit/run.py`](https://github.com/robocurve/benchmark-tasks/blob/add552504c5ccfedc201e2967f3230505f1e56fd/tasks/split-cable-guide-retrofit/run.py#L169): `reset` L169, `step` L232, `spawn` L64, `update` L206.
- [`tasks/split-cable-guide-retrofit/task.py`](https://github.com/robocurve/benchmark-tasks/blob/add552504c5ccfedc201e2967f3230505f1e56fd/tasks/split-cable-guide-retrofit/task.py#L329): `score` L329, `success` L333, `demo` L337, `step` L288.
- [`tasks/split-cable-guide-retrofit/test_task.py`](https://github.com/robocurve/benchmark-tasks/blob/add552504c5ccfedc201e2967f3230505f1e56fd/tasks/split-cable-guide-retrofit/test_task.py#L11): `test_installed_guide_must_clear_sleeve_and_hold_at_mark` L11, `test_drawer_travel_alone_cannot_score_and_late_fit_cannot_pass` L22.

**Assets/reset/tests:** Tests are supplied in test_task.py. Geometry is authored/generated in code. Read reset callbacks together with README reset instructions; neither static tests nor success receipts prove mechanical reset on hardware.

## u-joint-cross — [PR#903](https://github.com/robocurve/benchmark-tasks/pull/903)

**Operation/category:** Pass one journal through a yoke ear, swing the too-wide cross level, then recenter both journals. Impact on jobs.

**Actual implementation:** u_joint_cross.py journals/_in/installed use both symmetric journal pairs, world endpoints, ear depth and angular alignment; make_meshes.py authors hollow yoke ears and cross. demo uses an offset insertion/swing/recenter path with documented grip-droop compensation.

**Limit and published evidence:** 2,400 steps (2 minutes at 20 Hz); Dream-1 run: 0 (2,400 steps); demo: 1.0 (success at 33.5 s). Media `M-YZNZ23`. Media records were not downloaded or visually verified. Latest task commit `30bb2f1b05573d9e47a0da3c47757a72c2fcb0ec`.

**Review inference / limits:** No needle bearings/seals/grease; some dimensions from Spicer1310, journal span and ear geometry estimated. Raw score returns0.75 installed; success() lets harness award1 after hold. This illustrates a runner/raw distinction, not an unexplained passed full-score test here.

**Source map** (entry points and state transitions; all exact files pinned):

- [`tasks/u-joint-cross/test_u_joint_cross.py`](https://github.com/robocurve/benchmark-tasks/blob/add552504c5ccfedc201e2967f3230505f1e56fd/tasks/u-joint-cross/test_u_joint_cross.py#L42): `test_start_scores_zero` L42, `test_centred_and_still_is_success` L46, `test_centred_but_moving_is_not_success` L52, `test_rolled_in_its_holes_is_still_installed` L71, `test_the_end_state_of_a_simulated_demo_is_success` L81, `test_pushed_deep_into_one_ear_is_not_installed` L95, `test_on_top_of_the_ears_scores_zero` L118, `test_outside_the_yoke_scores_zero` L132, `test_fallen_on_the_table_scores_zero` L137, `test_distance_is_zero_only_when_installed` L141, `test_demo_is_reachable` L173, `test_demo_delay_only_shifts_the_start` L183.
- [`tasks/u-joint-cross/u_joint_cross.py`](https://github.com/robocurve/benchmark-tasks/blob/add552504c5ccfedc201e2967f3230505f1e56fd/tasks/u-joint-cross/u_joint_cross.py#L129): `installed` L129, `success` L135, `score` L145, `demo` L176.

**Assets/reset/tests:** Tests are supplied in test_u_joint_cross.py. USD assets are supplied; source hashes are in inventory. Read reset callbacks together with README reset instructions; neither static tests nor success receipts prove mechanical reset on hardware.

## brake-bleed-close-before-release — [PR#1577](https://github.com/robocurve/benchmark-tasks/pull/1577)

**Operation/category:** Press pedal, open bleeder while piston expels fluid, shut bleeder, then release pedal; repeat. Impact on jobs.

**Actual implementation:** task.py _score/score uses remaining air, backflow latch and actual gripper geometry. livekit.py solves pressure/fluid network; yamkit.py provides articulated parts; demo keeps pressure until screw shut. test_task.py exercises air ingress and pressure/motion behavior.

**Limit and published evidence:** 2,400 steps (2 minutes at 20 Hz); Dream-1 run: 0 (2,400 steps); demo: 1.0 (789 steps). Media `M-27J2FN`. Media records were not downloaded or visually verified. Latest task commit `39f0ae7f4ded7447855c38def683efea0cc9c04b`.

**Review inference / limits:** #1577 rejected floor-stop-first fake fluid delivery and mismatched wrench; revised published model allows piston travel under pressure and uses11mm wrench.6psi trainer is disclosed scaling of pressure; preserve causal hydraulic order, not fake the physical response.

**Source map** (entry points and state transitions; all exact files pinned):

- [`tasks/brake-bleed-close-before-release/livekit.py`](https://github.com/robocurve/benchmark-tasks/blob/add552504c5ccfedc201e2967f3230505f1e56fd/tasks/brake-bleed-close-before-release/livekit.py#L450): `reset` L450, `step` L470, `update` L938.
- [`tasks/brake-bleed-close-before-release/task.py`](https://github.com/robocurve/benchmark-tasks/blob/add552504c5ccfedc201e2967f3230505f1e56fd/tasks/brake-bleed-close-before-release/task.py#L351): `_score` L351, `success` L355, `score` L360, `demo` L402.
- [`tasks/brake-bleed-close-before-release/test_task.py`](https://github.com/robocurve/benchmark-tasks/blob/add552504c5ccfedc201e2967f3230505f1e56fd/tasks/brake-bleed-close-before-release/test_task.py#L59): `step` L59.
- [`tasks/brake-bleed-close-before-release/yamkit.py`](https://github.com/robocurve/benchmark-tasks/blob/add552504c5ccfedc201e2967f3230505f1e56fd/tasks/brake-bleed-close-before-release/yamkit.py#L531): `_watch_resets` L531, `_patch_demo` L661, `reset` L539.

**Assets/reset/tests:** Tests are supplied in test_task.py. Geometry is authored/generated in code. Read reset callbacks together with README reset instructions; neither static tests nor success receipts prove mechanical reset on hardware.

## o-ring-into-groove — [PR#1576](https://github.com/robocurve/benchmark-tasks/pull/1576)

**Operation/category:** Stretch an elastomer ring over threads and seat square/untwisted in a groove. Impact on jobs.

**Actual implementation:** ringkit.py _step models radius, sliding, roll, cocking, stretch damage and closing; task.py _score awards safe progress/physical seating rather than home pose. demo spreads fingertips, advances ring, then withdraws. tests include too-small stretch, roll-on twist and correcting a cocked seal.

**Limit and published evidence:** 2,400 steps (2 minutes at 20 Hz); Dream-1 run: 0 (2,400 steps); demo: 1.0 (248 steps). Media `M-GRLEQ7`. Media records were not downloaded or visually verified. Latest task commit `a9aa72842322307e94266f033897c662e0f9d3f7`.

**Review inference / limits:** Not a full deformable continuum simulation. #1576 demanded score outcomes instead of release-angle history and reconcile stretch calibration. Final seat must remain observable, while damage history must have a physical observation.

**Source map** (entry points and state transitions; all exact files pinned):

- [`tasks/o-ring-into-groove/ringkit.py`](https://github.com/robocurve/benchmark-tasks/blob/add552504c5ccfedc201e2967f3230505f1e56fd/tasks/o-ring-into-groove/ringkit.py#L352): `_step` L352, `update` L426.
- [`tasks/o-ring-into-groove/task.py`](https://github.com/robocurve/benchmark-tasks/blob/add552504c5ccfedc201e2967f3230505f1e56fd/tasks/o-ring-into-groove/task.py#L134): `_score` L134, `success` L138, `score` L143, `demo` L166.
- [`tasks/o-ring-into-groove/test_task.py`](https://github.com/robocurve/benchmark-tasks/blob/add552504c5ccfedc201e2967f3230505f1e56fd/tasks/o-ring-into-groove/test_task.py#L95): `demo_like` L95, `test_demo_full` L115, `test_episode_resets_history` L447, `step` L58.
- [`tasks/o-ring-into-groove/yamkit.py`](https://github.com/robocurve/benchmark-tasks/blob/add552504c5ccfedc201e2967f3230505f1e56fd/tasks/o-ring-into-groove/yamkit.py#L497): `_watch_resets` L497, `_patch_demo` L618, `reset` L505.

**Assets/reset/tests:** Tests are supplied in test_task.py. Geometry is authored/generated in code. Read reset callbacks together with README reset instructions; neither static tests nor success receipts prove mechanical reset on hardware.

## toilet-roll-spindle — [PR#1847](https://github.com/robocurve/benchmark-tasks/pull/1847)

**Operation/category:** Remove spindle, exchange tube for new roll and refit two spring-loaded tips into sockets. Societal relatability.

**Actual implementation:** rollkit.py authors spring prismatic spindle and rigid hollow rolls. task.py spindle_ends/on_spindle/seated/_update evaluate socket capture, supported roll, empty tube collection and fingertip clearance. demo.py is actual successful-controller entry; task.py demo returns empty waypoints for a do-nothing baseline.

**Limit and published evidence:** 3,000 steps (2.5 minutes at 20 Hz); Dream-1 run: 0.0 (3000 steps); demo: 1.0 (1500 steps). Media `M-YPS3UT`. Media records were not downloaded or visually verified. Latest task commit `db3fd7223544dd07942b97ddf57bc52d9ccfcebf`.

**Review inference / limits:** A model-run command using yam_scripted on task.py alone does not reproduce the successful expert. Spring200N/m is explicitly assumed. Distinction from a tension rod is socket acquisition while the roll blocks central grasp.

**Source map** (entry points and state transitions; all exact files pinned):

- [`tasks/toilet-roll-spindle/rollkit.py`](https://github.com/robocurve/benchmark-tasks/blob/add552504c5ccfedc201e2967f3230505f1e56fd/tasks/toilet-roll-spindle/rollkit.py#L144): `_spawn_part` L144, `on_step` L385, `on_reset` L391, `_task_step` L431, `reset` L437.
- [`tasks/toilet-roll-spindle/task.py`](https://github.com/robocurve/benchmark-tasks/blob/add552504c5ccfedc201e2967f3230505f1e56fd/tasks/toilet-roll-spindle/task.py#L231): `_reset_state` L231, `_update` L261, `success` L286, `score` L292, `demo` L298.

**Assets/reset/tests:** No separate test*.py suite found; documented controller variants are not equivalent to a full test suite. Geometry is authored/generated in code. Read reset callbacks together with README reset instructions; neither static tests nor success receipts prove mechanical reset on hardware.

## push-in-terminal — [PR#268](https://github.com/robocurve/benchmark-tasks/pull/268)

**Operation/category:** Land a ferruled flexible conductor in the named WAGO terminal and verify retention. Impact on jobs.

**Actual implementation:** terminal_sim/task.py resets leaf joints/history, applies after-release pull test and gathers wrong-terminal events. terminal_sim/scorer.py latches wrong-terminal history; terminal_props.py supplies terminal/leaf geometry. task scorer returns0 on wrong-entry events.

**Limit and published evidence:** 1,200 steps (60 s at 20 Hz); Dream-1 run: 0.0; demo: 1.0. Media `M-FHNTKK`. Media records were not downloaded or visually verified. Latest task commit `de6142bf7c4b96637c4c3016e002806e10401d48`.

**Review inference / limits:** Physical50N pull check is an evaluator test, not a claim the YAM applies it. Branded product numbers and conductor specification are explicit. #268 was recategorized to jobs; identifiable panel wiring supports that domain.

**Source map** (entry points and state transitions; all exact files pinned):

- [`tasks/push-in-terminal/push_in_terminal.py`](https://github.com/robocurve/benchmark-tasks/blob/add552504c5ccfedc201e2967f3230505f1e56fd/tasks/push-in-terminal/push_in_terminal.py#L48): `score` L48.
- [`tasks/push-in-terminal/terminal_sim/kit.py`](https://github.com/robocurve/benchmark-tasks/blob/add552504c5ccfedc201e2967f3230505f1e56fd/tasks/push-in-terminal/terminal_sim/kit.py#L170): `reset_robot_home` L170.
- [`tasks/push-in-terminal/terminal_sim/policy.py`](https://github.com/robocurve/benchmark-tasks/blob/add552504c5ccfedc201e2967f3230505f1e56fd/tasks/push-in-terminal/terminal_sim/policy.py#L46): `terminal_demo` L46, `reset` L34.
- [`tasks/push-in-terminal/terminal_sim/scorer.py`](https://github.com/robocurve/benchmark-tasks/blob/add552504c5ccfedc201e2967f3230505f1e56fd/tasks/push-in-terminal/terminal_sim/scorer.py#L39): `reset` L39, `update` L51, `success` L64.
- [`tasks/push-in-terminal/terminal_sim/station.py`](https://github.com/robocurve/benchmark-tasks/blob/add552504c5ccfedc201e2967f3230505f1e56fd/tasks/push-in-terminal/terminal_sim/station.py#L122): `success` L122, `score` L125, `demo` L129, `wrapped_reset` L280, `wrapped_step` L286, `build_task_environment` L336, `patched_step` L394, `reset_then_hold` L421.
- [`tasks/push-in-terminal/terminal_sim/task.py`](https://github.com/robocurve/benchmark-tasks/blob/add552504c5ccfedc201e2967f3230505f1e56fd/tasks/push-in-terminal/terminal_sim/task.py#L204): `reset` L204, `step` L234.

**Assets/reset/tests:** No separate test*.py suite found; documented controller variants are not equivalent to a full test suite. USD assets are supplied; source hashes are in inventory. Read reset callbacks together with README reset instructions; neither static tests nor success receipts prove mechanical reset on hardware.

## wrap-a-pipe-thread-with-thread-seal-tape-from-a-dispenser-the-way-the-fitting-turns-on — [PR#1465](https://github.com/robocurve/benchmark-tasks/pull/1465)

**Operation/category:** Wind thread-seal tape in the mating direction with coverage, tension, tear and tail laydown. Impact on jobs.

**Actual implementation:** tapekit.py tracks paid-out tape, orbital angle, stretch/tear and forces on the roll; tape_wrap.py wound_right/taped_heights/_update score direction and height coverage plus tail-down/return/release. Demo orbits roll, tears and presses tail.

**Limit and published evidence:** 1,600 steps (80 seconds at 20 Hz); Dream-1 run: 0.0 (both arms draw back towards their bases and never reach the dispenser or the pipe); demo: 1.0 (success at step 609). Media `M-4KYK3E`. Media records were not downloaded or visually verified. Latest task commit `becf10922d4ded74517d70e297333c875028e321`.

**Review inference / limits:** No tape mesh/material wrinkling; outcome model is disclosed. Clockwise direction is judged from thread end. Winding without correct coverage or leaving tail loose is not full completion.

**Source map** (entry points and state transitions; all exact files pinned):

- [`tasks/wrap-a-pipe-thread-with-thread-seal-tape-from-a-dispenser-the-way-the-fitting-turns-on/tape_wrap.py`](https://github.com/robocurve/benchmark-tasks/blob/add552504c5ccfedc201e2967f3230505f1e56fd/tasks/wrap-a-pipe-thread-with-thread-seal-tape-from-a-dispenser-the-way-the-fitting-turns-on/tape_wrap.py#L199): `_update` L199, `success` L213, `score` L220, `demo` L293.
- [`tasks/wrap-a-pipe-thread-with-thread-seal-tape-from-a-dispenser-the-way-the-fitting-turns-on/tapekit.py`](https://github.com/robocurve/benchmark-tasks/blob/add552504c5ccfedc201e2967f3230505f1e56fd/tasks/wrap-a-pipe-thread-with-thread-seal-tape-from-a-dispenser-the-way-the-fitting-turns-on/tapekit.py#L465): `on_reset` L465, `_spawn_body` L476, `update` L348, `reset` L812.
- [`tasks/wrap-a-pipe-thread-with-thread-seal-tape-from-a-dispenser-the-way-the-fitting-turns-on/test_tape_wrap.py`](https://github.com/robocurve/benchmark-tasks/blob/add552504c5ccfedc201e2967f3230505f1e56fd/tasks/wrap-a-pipe-thread-with-thread-seal-tape-from-a-dispenser-the-way-the-fitting-turns-on/test_tape_wrap.py#L64): `step` L64, `test_wound_the_wrong_way_scores_nothing` L222, `test_no_tape_scores_nothing` L227, `test_less_than_a_turn_scores_nothing` L267, `test_the_demo_reaches_every_target_along_its_path` L279, `test_the_demo_passes_the_run_guards` L294, `test_the_demo_fits_the_run_limit` L300.

**Assets/reset/tests:** Tests are supplied in test_tape_wrap.py. Geometry is authored/generated in code. Read reset callbacks together with README reset instructions; neither static tests nor success receipts prove mechanical reset on hardware.

## tig-seam — [PR#1495](https://github.com/robocurve/benchmark-tasks/pull/1495)

**Operation/category:** Coordinate TIG torch travel and filler dabs along an L seam. Impact on jobs.

**Actual implementation:** task.py note_step/weld_state track arc geometry, heat per segment, filler dips, contamination and burn-through; score uses40 sound-segment outcomes with caps. tig_seam/mech.py generates tools/bench; embodiment reset clears trial state.

**Limit and published evidence:** 3,000 steps (2.5 minutes at 20 Hz); Dream-1 run: 0.0 (recorded with the earlier wording "the yellow filler rod"; on the revised wording Dream-1 refused: "unsafe instruction, refused: Using a hot welding torch presents severe thermal and fire risks"); demo: 1.0. Media `M-97LA4N`. Media records were not downloaded or visually verified. Latest task commit `bad5af816b67638e89989958c930dbaa851b2cc1`.

**Review inference / limits:** Arc, heat and deposited metal are proxies in simulation. #1495 required a separate physical bead/defect scoring method, actual power/gas and protective equipment. Real welding quality cannot be inferred from simulated tip geometry. Reported model refusal is preserved.

**Source map** (entry points and state transitions; all exact files pinned):

- [`tasks/tig-seam/task.py`](https://github.com/robocurve/benchmark-tasks/blob/add552504c5ccfedc201e2967f3230505f1e56fd/tasks/tig-seam/task.py#L77): `reset_latch` L77, `note_step` L177, `score` L257, `demo` L471, `step` L358.
- [`tasks/tig-seam/test_score.py`](https://github.com/robocurve/benchmark-tasks/blob/add552504c5ccfedc201e2967f3230505f1e56fd/tasks/tig-seam/test_score.py#L95): `test_start_scores_zero` L95, `test_full_seam_tools_not_back_scores_point_nine` L109, `test_torch_alone_scores_zero` L140, `test_rod_in_the_torch_hand_scores_zero` L146, `test_rod_not_held_scores_zero` L151, `test_a_tool_off_the_table_scores_zero` L243.
- [`tasks/tig-seam/tig_seam/embodiment.py`](https://github.com/robocurve/benchmark-tasks/blob/add552504c5ccfedc201e2967f3230505f1e56fd/tasks/tig-seam/tig_seam/embodiment.py#L32): `reset` L32, `_task_step` L131, `spawn` L54.
- [`tasks/tig-seam/tig_seam/mech.py`](https://github.com/robocurve/benchmark-tasks/blob/add552504c5ccfedc201e2967f3230505f1e56fd/tasks/tig-seam/tig_seam/mech.py#L299): `build_torch` L299, `build_rod` L336, `build_bench` L351.

**Assets/reset/tests:** Tests are supplied in test_score.py. Geometry is authored/generated in code. Read reset callbacks together with README reset instructions; neither static tests nor success receipts prove mechanical reset on hardware.

## lift-a-glass-pane-with-suction-lifters — [PR#931](https://github.com/robocurve/benchmark-tasks/pull/931)

**Operation/category:** Seal two lever cups, carry pane from sash to bearers, release cups and hands. Impact on jobs.

**Actual implementation:** glazekit.py uses three force springs per sealed cup with breakaway limit; glass_pane.py _update latches dropped/tilted/directly-touched pane, requires both-cup lift, on-bearers geometry, cup unlock and release. demo has place/lock/carry/unlock phases.

**Limit and published evidence:** 2,400 steps (2 minutes at 20 Hz); Dream-1 run: 0.0; demo: 1.0. Media `M-KRCGQB`. Media records were not downloaded or visually verified. Latest task commit `1c094102e0d59d16394ade30dd61e1a97ad30042`.

**Review inference / limits:** Cup engagement must depend on flatness and edge margin. Real cup load rating is not inherited by spring model; glass flex/breakage omitted. Tests include one-cup lift and edge attempts, not merely pose-at-goal states.

**Source map** (entry points and state transitions; all exact files pinned):

- [`tasks/lift-a-glass-pane-with-suction-lifters/glass_pane.py`](https://github.com/robocurve/benchmark-tasks/blob/add552504c5ccfedc201e2967f3230505f1e56fd/tasks/lift-a-glass-pane-with-suction-lifters/glass_pane.py#L178): `_reset_state` L178, `_update` L219, `success` L249, `score` L254, `demo` L365.
- [`tasks/lift-a-glass-pane-with-suction-lifters/glazekit.py`](https://github.com/robocurve/benchmark-tasks/blob/add552504c5ccfedc201e2967f3230505f1e56fd/tasks/lift-a-glass-pane-with-suction-lifters/glazekit.py#L451): `on_reset` L451, `_spawn_body` L465, `update` L295, `update` L361, `reset` L711.
- [`tasks/lift-a-glass-pane-with-suction-lifters/test_glass_pane.py`](https://github.com/robocurve/benchmark-tasks/blob/add552504c5ccfedc201e2967f3230505f1e56fd/tasks/lift-a-glass-pane-with-suction-lifters/test_glass_pane.py#L106): `test_start_scores_zero` L106, `test_pane_laid_on_the_bearers_and_let_go_is_full_score` L122, `test_still_moving_is_not_success_yet` L131, `test_dropped_then_put_right_scores_zero` L181, `test_tilted_in_the_carry_then_laid_flat_scores_zero` L191, `test_reset_clears_the_latches` L210, `test_the_demo_is_within_reach_and_passes_the_run_guards` L302, `test_the_demo_fits_the_run_limit` L309.

**Assets/reset/tests:** Tests are supplied in test_glass_pane.py. Geometry is authored/generated in code. Read reset callbacks together with README reset instructions; neither static tests nor success receipts prove mechanical reset on hardware.

## What transfers to future concepts

1. Real constraints cause the required coordination: undercuts, keys, sprung parts, coupled motion, retention and actual tool engagement. A sequence forced only by scorer history is weak evidence of a distinct skill.
2. A useful physical endpoint makes importance and scoring concrete: retained wire, clamped/aligned fixture, completed joint, correctly supported assembly. Stopping at a fixture's arbitrary intermediate state invites rejection.
3. Approximation is acceptable only locally and explicitly. Published tasks use idealized threads, tooth drives, suction springs and outcome models. Their acceptance is not a guarantee for newly invented equipment or changed physical loads.
4. Review separates simulator proxy from physical criterion. TIG tip motion is not a weld; internal spring coordinates are not a ruler measurement; jaw pose is not holding force.
5. Counterexamples reveal scorer weaknesses. Wrong target, early release, wrong keying, unsupported final placement, stale milestones and reset/restoration attacks belong in the design before engine work.
6. Successful native code is subordinate to importance/novelty. Our four rejected packages demonstrate that source integrity, multiple full-score experts and genuine model/media can all coexist with conceptual invalidity.

## Remaining deep-audit work

These twenty dossiers include actual code-level behavior, but not a complete line-by-line audit of all generated USD, contact materials, reset internals, source-bound video receipts and controller information-flow for all twenty. Native executability, full media playback and every historical PR revision are unverified. The report deliberately avoids substituting text inspection for those checks.
