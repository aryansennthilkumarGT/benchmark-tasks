# Distinct contribution and limitations

Reviewed 2026-11-07. Internal decision: continue to native validation. This is neither a board reservation nor an acceptance guarantee; refresh the board before submission.

A collar cannot slide over the shaft's fixed flanges. The robot must open its hinge, support both halves around the captive shaft, close the seam and insert a transverse key through three lugs. This replaces generic kitting.

- [RoboCurve PR #708](https://github.com/robocurve/benchmark-tasks/pull/708): Clamp-on valve lockout is the closest physical neighbor: two halves and a lock surround hardware. Here a hinged shaft collar must bypass fixed end flanges and capture an interleaved seam with a cross-pin; there is no valve or padlock.
- [RoboCurve PR #1027](https://github.com/robocurve/benchmark-tasks/pull/1027): Collar-on-guide manipulation overlaps in name, but that task transports an already-threaded opaque collar without touching a curved guide. Here opening, fitting, contact and seam retention are the challenge.
- [RoboCurve PR #994](https://github.com/robocurve/benchmark-tasks/pull/994): Clevis pin retention is a shared primitive, but the captive-shaft split-access dependency adds the substantive workflow.

Moderate-to-high overlap with clamp-on lockout. The captive-shaft access constraint and pin-captured seam must be demonstrated, and reviewer acceptance cannot be guaranteed.

[DataCenterBench](https://robocurve.org/datacenterbench/) already covers connector handling and lists battery/nut candidates. [RoboDojo](https://robodojo-benchmark.com/doc/sim-tasks/fasten-screws/) already tests independent threaded pairs. Neither repetition nor renaming establishes novelty.

[LIBERO's catalog](https://github.com/Lifelong-Robot-Learning/LIBERO/blob/master/libero/libero/benchmark/libero_suite_task_map.py) and [SimplerEnv's environment list](https://github.com/simpler-env/SimplerEnv#current-environments) include placement and access primitives. [RoboCasa's registered tasks](https://github.com/robocasa/robocasa/blob/main/robocasa/__init__.py) include lids and multi-step kitchen work. [BEHAVIOR furniture assembly](https://behavior.stanford.edu/knowledgebase/tasks/assembling_furniture-0.html) specifies attachment outcomes. These comparisons support a mechanism-specific contribution, not a claim that long sequences are new.

The screen examined nearby PR descriptions/available implementation and review comments, primary task catalogs, and relevant attachment definitions. Search coverage is imperfect and pending submissions change. Native feasibility remains a separate unresolved criterion.
