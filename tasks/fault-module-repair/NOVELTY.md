# Distinct contribution and limitations

Reviewed 2026-11-07. Internal decision: continue to native validation. This is neither a board reservation nor an acceptance guarantee; refresh the board before submission.

The redesigned task balances a freely pivoted loaded service arm by changing the counterweight moment, then pins the sliding weight against drift. The robot must support the arm during adjustment and leave it balanced after release.

- [RoboCurve PR #236](https://github.com/robocurve/benchmark-tasks/pull/236): The indexed arm-angle lock task supports a loaded arm and clamps its pivot. This task leaves the pivot free and changes the center of mass; the pin locks the counterweight, not the arm angle.
- [RoboCurve PR #80](https://github.com/robocurve/benchmark-tasks/pull/80): Counterweighted overhang placement shares static equilibrium, but this task uses a captive rail, a free rotary degree of freedom and pin retention of the tuned mass position.
- [RoboCurve PR #799](https://github.com/robocurve/benchmark-tasks/pull/799): Board balancing is a related principle; the guided counterweight and independent locking operation define the service task.

Moderate overlap in balancing. Correct behavior must come from gravitational moments and the free pin rather than a hidden centering actuator.

[DataCenterBench](https://robocurve.org/datacenterbench/) already covers connector handling and lists battery/nut candidates. [RoboDojo](https://robodojo-benchmark.com/doc/sim-tasks/fasten-screws/) already tests independent threaded pairs. Neither repetition nor renaming establishes novelty.

[LIBERO's catalog](https://github.com/Lifelong-Robot-Learning/LIBERO/blob/master/libero/libero/benchmark/libero_suite_task_map.py) and [SimplerEnv's environment list](https://github.com/simpler-env/SimplerEnv#current-environments) include placement and access primitives. [RoboCasa's registered tasks](https://github.com/robocasa/robocasa/blob/main/robocasa/__init__.py) include lids and multi-step kitchen work. [BEHAVIOR furniture assembly](https://behavior.stanford.edu/knowledgebase/tasks/assembling_furniture-0.html) specifies attachment outcomes. These comparisons support a mechanism-specific contribution, not a claim that long sequences are new.

The screen examined nearby PR descriptions/available implementation and review comments, primary task catalogs, and relevant attachment definitions. Search coverage is imperfect and pending submissions change. Native feasibility remains a separate unresolved criterion.
