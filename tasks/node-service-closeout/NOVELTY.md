# Distinct contribution and limitations

Reviewed 2026-11-07. Internal decision: continue to native validation. This is neither a board reservation nor an acceptance guarantee; refresh the board before submission.

The cooling shroud blocks storage removal, storage enters through capped rails, keyed cooler feet occupy a different interface, and lid closure retains the cooler. Correct replacement identities and collection of both removed parts are required.

- [RoboCurve PR #422](https://github.com/robocurve/benchmark-tasks/pull/422): Drive-bay identity mapping overlaps, but that task uses open gravity slots. This fixture imposes removal and installation dependencies through a keyed cooler and horizontal rails.
- [RoboCurve PR #969](https://github.com/robocurve/benchmark-tasks/pull/969): Heatsink handling overlaps, but that task requires adhesive release without pulling a CPU. This cooler is a removable keyed obstruction; no adhesive or thermal claim is made.
- [RoboCurve PR #908](https://github.com/robocurve/benchmark-tasks/pull/908): Housing closure after internal assembly is a shared pattern; the storage/cooler access dependency defines this maintenance workflow.

Moderate maintenance overlap; dependencies must be physical rather than enforced solely by a scripted order. Native obstruction and retention probes are required.

[DataCenterBench](https://robocurve.org/datacenterbench/) already covers connector handling and lists battery/nut candidates. [RoboDojo](https://robodojo-benchmark.com/doc/sim-tasks/fasten-screws/) already tests independent threaded pairs. Neither repetition nor renaming establishes novelty.

[LIBERO's catalog](https://github.com/Lifelong-Robot-Learning/LIBERO/blob/master/libero/libero/benchmark/libero_suite_task_map.py) and [SimplerEnv's environment list](https://github.com/simpler-env/SimplerEnv#current-environments) include placement and access primitives. [RoboCasa's registered tasks](https://github.com/robocasa/robocasa/blob/main/robocasa/__init__.py) include lids and multi-step kitchen work. [BEHAVIOR furniture assembly](https://behavior.stanford.edu/knowledgebase/tasks/assembling_furniture-0.html) specifies attachment outcomes. These comparisons support a mechanism-specific contribution, not a claim that long sequences are new.

The screen examined nearby PR descriptions/available implementation and review comments, primary task catalogs, and relevant attachment definitions. Search coverage is imperfect and pending submissions change. Native feasibility remains a separate unresolved criterion.
