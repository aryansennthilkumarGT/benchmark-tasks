# External benchmarks: actual inspection scope

All observations are pinned to Git revisions retrieved on2026-11-14. No “not found” below establishes semantic absence. Hardware datasets, submodules and media were not downloaded or executed.

## Lifelong-Robot-Learning/LIBERO

Commit `8f1084e3132a39270c3a13ebe37270a43ece2a01`. Inspected source/reference paths:

- [`libero/libero/benchmark/libero_suite_task_map.py`](https://github.com/Lifelong-Robot-Learning/LIBERO/blob/8f1084e3132a39270c3a13ebe37270a43ece2a01/libero/libero/benchmark/libero_suite_task_map.py)
## robocasa/robocasa

Commit `425684d332f135f5b30a40b321f52d15a0fe9250`. Inspected source/reference paths:

- [`robocasa/environments/kitchen/composite/arranging_cabinets/reset_cabinet_doors.py`](https://github.com/robocasa/robocasa/blob/425684d332f135f5b30a40b321f52d15a0fe9250/robocasa/environments/kitchen/composite/arranging_cabinets/reset_cabinet_doors.py)
## StanfordVL/BEHAVIOR-1K

Commit `b544acbbb76b461349bcba21f93b870b11da6608`. Inspected source/reference paths:

- [`bddl3/bddl/activity_definitions/assembling_furniture/problem0.bddl`](https://github.com/StanfordVL/BEHAVIOR-1K/blob/b544acbbb76b461349bcba21f93b870b11da6608/bddl3/bddl/activity_definitions/assembling_furniture/problem0.bddl)
- [`bddl3/bddl/activity_definitions/make_a_sandwich/problem0.bddl`](https://github.com/StanfordVL/BEHAVIOR-1K/blob/b544acbbb76b461349bcba21f93b870b11da6608/bddl3/bddl/activity_definitions/make_a_sandwich/problem0.bddl)
## robodojo-benchmark/RoboDojo

Commit `f57e1633ffed59761bc8e568cfe7530c4b33381c`. Inspected source/reference paths:

- [`task/RoboDojo/tasks/fasten_screws.py`](https://github.com/robodojo-benchmark/RoboDojo/blob/f57e1633ffed59761bc8e568cfe7530c4b33381c/task/RoboDojo/tasks/fasten_screws.py)
- [`task/RoboDojo/tasks/insert_key.py`](https://github.com/robodojo-benchmark/RoboDojo/blob/f57e1633ffed59761bc8e568cfe7530c4b33381c/task/RoboDojo/tasks/insert_key.py)
- [`task/RoboDojo/tasks/insert_tubes.py`](https://github.com/robodojo-benchmark/RoboDojo/blob/f57e1633ffed59761bc8e568cfe7530c4b33381c/task/RoboDojo/tasks/insert_tubes.py)
- [`task/RoboDojo/tasks/plug_in_charger.py`](https://github.com/robodojo-benchmark/RoboDojo/blob/f57e1633ffed59761bc8e568cfe7530c4b33381c/task/RoboDojo/tasks/plug_in_charger.py)
## robocurve/datacenterbench

Commit `59bdd147040bb47227a20d8336ead3d4fdca27dd`. Inspected source/reference paths:

- [`docs/tasks/clip.md`](https://github.com/robocurve/datacenterbench/blob/59bdd147040bb47227a20d8336ead3d4fdca27dd/docs/tasks/clip.md)
- [`docs/tasks/cover.md`](https://github.com/robocurve/datacenterbench/blob/59bdd147040bb47227a20d8336ead3d4fdca27dd/docs/tasks/cover.md)
- [`docs/tasks/join.md`](https://github.com/robocurve/datacenterbench/blob/59bdd147040bb47227a20d8336ead3d4fdca27dd/docs/tasks/join.md)
- [`docs/tasks/key.md`](https://github.com/robocurve/datacenterbench/blob/59bdd147040bb47227a20d8336ead3d4fdca27dd/docs/tasks/key.md)
- [`docs/tasks/keypad.md`](https://github.com/robocurve/datacenterbench/blob/59bdd147040bb47227a20d8336ead3d4fdca27dd/docs/tasks/keypad.md)
- [`docs/tasks/knob.md`](https://github.com/robocurve/datacenterbench/blob/59bdd147040bb47227a20d8336ead3d4fdca27dd/docs/tasks/knob.md)
- [`docs/tasks/plug.md`](https://github.com/robocurve/datacenterbench/blob/59bdd147040bb47227a20d8336ead3d4fdca27dd/docs/tasks/plug.md)
- [`docs/tasks/slider.md`](https://github.com/robocurve/datacenterbench/blob/59bdd147040bb47227a20d8336ead3d4fdca27dd/docs/tasks/slider.md)
- [`docs/tasks/toggle.md`](https://github.com/robocurve/datacenterbench/blob/59bdd147040bb47227a20d8336ead3d4fdca27dd/docs/tasks/toggle.md)
- [`docs/tasks/unplug.md`](https://github.com/robocurve/datacenterbench/blob/59bdd147040bb47227a20d8336ead3d4fdca27dd/docs/tasks/unplug.md)
- [`src/datacenterbench/specs.py`](https://github.com/robocurve/datacenterbench/blob/59bdd147040bb47227a20d8336ead3d4fdca27dd/src/datacenterbench/specs.py)

## Code-level observations

- **RoboDojo FastenScrews:** reward checks nut-axis orientation, <=1mmXY alignment and9mm depth for three bolt/nut pairs, plus gripper/home conditions. Its task code does not establish a native contact-thread model. A proposed task cannot assert generic fastening is new merely because this scorer is abstract.
- **RoboDojo InsertKey:** insertion-depth/alignment checks, with an instruction naming handover/turn. The shown reward predicates do not independently enforce every narrated action. Distinguish instruction and actual success definition.
- **RoboDojo InsertTubes:** three insertions with45mmdepth, containment and axis checks; count/layout variants are already represented.
- **RoboDojo PlugInCharger:**15mmdepth/containment/alignment and home checks; tool/connector labels do not create novelty.
- **RoboCasa ResetCabinetDoors:** actual `_check_success` calls closed-state predicates on three cabinets; initial setup opens them. This directly supports the#1937 overlap objection.
- **LIBERO:** actual named suite map contains spatial/object pick-place, articulated drawer/cabinet, stove and multistage household tasks.130 map entries were counted; BDDL files were inventoried. This is not an exhaustive mechanistic equivalence proof against five industrial leads.
- **BEHAVIOR-1K:**1018 BDDL definitions were read by a literal screen for chuck, collet, l-track, die head, sds, cargo, shackle and nailer, with zero hits. Furniture assembly explicitly uses attached predicates for bracket/top/legs; sandwich includes covered bread with spreads and a knife in the setup. Those actual definitions show why low-level control/contact novelty cannot be inferred just from absent object names.
- **DataCenterBench:** all ten real-procedure sections and four detailed task pages were read. The official pages themselves distinguish substitute bench interfaces from vendor equipment: Ethernet coupler versus UPS connector, little cable clip versus switch-tray channel, maintained cover versus emergency shutdown, key switch versus breaker interlock. They are separate benchmark design choices, not current RoboCurve submission permission. Generic switch/plug/cover primitives are already represented.

## Corpus identification gaps

The official reviewer names `dexhand: Remote Battery Swap` in#1703. GitHub repository search returned `Dexterous-Hand-Manipulation-Benchmarks/dexhand-bench`, whose tree is a DexMachina/RL training harness with environment submodules. That is **not verified to be the cited Remote Battery Swap corpus**, so it is excluded as evidence for exhaustive DexHand task coverage. No repository was fabricated to fill the gap.

Full SimplerEnv definitions, HumanoidBench Window source, any private/unindexed suites and signed-in RoboCurve board were not fully inspected. A reviewer-supplied comparator is attributable negative evidence but not a substitute for reading its original implementation. No new candidate is novelty-cleared while those critical neighbors remain unresolved.
