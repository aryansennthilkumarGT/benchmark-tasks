# Distinct contribution and limitations

Reviewed 2026-11-07. Internal decision: continue to native validation. This is neither a board reservation nor an acceptance guarantee; refresh the board before submission.

The task measures replacement under sustained access support: two used identities must leave, opposite polarities must match spring contacts, and the spring-return cover must close. It is a bench service fixture, not a replica of a particular remote.

- [RoboCurve PR #615](https://github.com/robocurve/benchmark-tasks/pull/615): Battery polarity and lid closure overlap with a welder-battery task. This fixture requires both used-cell removal and replacement while holding a spring-return sliding cover.
- [RoboCurve PR #281](https://github.com/robocurve/benchmark-tasks/pull/281): Flashlight battery polarity overlaps, but its screw-cap closure is a different mechanism.
- [RoboCurve PR #234](https://github.com/robocurve/benchmark-tasks/pull/234): Robot battery swapping is a close maintenance neighbor. More cells alone is insufficient; the access-support and opposed-contact constraints are the contribution.

Higher thematic overlap with battery service. The physical access dependency and full identity-preserving exchange must remain central; cosmetic differences are not evidence of novelty.

[DataCenterBench](https://robocurve.org/datacenterbench/) already covers connector handling and lists battery/nut candidates. [RoboDojo](https://robodojo-benchmark.com/doc/sim-tasks/fasten-screws/) already tests independent threaded pairs. Neither repetition nor renaming establishes novelty.

[LIBERO's catalog](https://github.com/Lifelong-Robot-Learning/LIBERO/blob/master/libero/libero/benchmark/libero_suite_task_map.py) and [SimplerEnv's environment list](https://github.com/simpler-env/SimplerEnv#current-environments) include placement and access primitives. [RoboCasa's registered tasks](https://github.com/robocasa/robocasa/blob/main/robocasa/__init__.py) include lids and multi-step kitchen work. [BEHAVIOR furniture assembly](https://behavior.stanford.edu/knowledgebase/tasks/assembling_furniture-0.html) specifies attachment outcomes. These comparisons support a mechanism-specific contribution, not a claim that long sequences are new.

The screen examined nearby PR descriptions/available implementation and review comments, primary task catalogs, and relevant attachment definitions. Search coverage is imperfect and pending submissions change. Native feasibility remains a separate unresolved criterion.
