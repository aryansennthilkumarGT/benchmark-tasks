# Distinct contribution and limitations

Reviewed 2026-11-07. Internal decision: continue to native validation. This is neither a board reservation nor an acceptance guarantee; refresh the board before submission.

A spring-loaded access plate can rise and tip until the threaded nuts capture its load. The expert transfers support between hands to reach both rows, turns and regrips every nut, and releases a level, compressed plate. This replaces an independent-nut repetition task.

- [RoboCurve PR #330](https://github.com/robocurve/benchmark-tasks/pull/330): The pending star-pattern flange task places solid nut props on stud tops. Here real thread contact, axial advance and retained spring preload are required; stud count is not the distinction.
- [RoboCurve PR #618](https://github.com/robocurve/benchmark-tasks/pull/618): Holding a nut while turning a screw overlaps in bimanual threading. Here the hand supports a separate spring-loaded plate while nuts advance on fixed studs and eventually carry the plate load.

Highest contact and runtime risk. Fine compound thread collision, repeated regrasping and load transfer must pass native probes before any paid model trial. RoboDojo already tests independent threaded pairs.

[DataCenterBench](https://robocurve.org/datacenterbench/) already covers connector handling and lists battery/nut candidates. [RoboDojo](https://robodojo-benchmark.com/doc/sim-tasks/fasten-screws/) already tests independent threaded pairs. Neither repetition nor renaming establishes novelty.

[LIBERO's catalog](https://github.com/Lifelong-Robot-Learning/LIBERO/blob/master/libero/libero/benchmark/libero_suite_task_map.py) and [SimplerEnv's environment list](https://github.com/simpler-env/SimplerEnv#current-environments) include placement and access primitives. [RoboCasa's registered tasks](https://github.com/robocasa/robocasa/blob/main/robocasa/__init__.py) include lids and multi-step kitchen work. [BEHAVIOR furniture assembly](https://behavior.stanford.edu/knowledgebase/tasks/assembling_furniture-0.html) specifies attachment outcomes. These comparisons support a mechanism-specific contribution, not a claim that long sequences are new.

The screen examined nearby PR descriptions/available implementation and review comments, primary task catalogs, and relevant attachment definitions. Search coverage is imperfect and pending submissions change. Native feasibility remains a separate unresolved criterion.
