# Distinct contribution and limitations

Original literature and implementation screen 2026-11-07; board mechanisms refreshed 2026-11-12. Internal decision: continue to native validation. This is neither a board reservation nor an acceptance guarantee; refresh the board before submission.

The task measures replacement under sustained access support: two used identities must leave, opposite polarities must match spring contacts, and the spring-return cover must close. It is a bench service fixture, not a replica of a particular remote.

- [RoboCurve PR #615](https://github.com/robocurve/benchmark-tasks/pull/615): Battery polarity and lid closure overlap with a welder-battery task. This fixture requires both used-cell removal and replacement while holding a spring-return sliding cover.
- [RoboCurve PR #281](https://github.com/robocurve/benchmark-tasks/pull/281): Flashlight battery polarity overlaps, but its screw-cap closure is a different mechanism.
- [RoboCurve PR #234](https://github.com/robocurve/benchmark-tasks/pull/234): Robot battery swapping is a close maintenance neighbor. More cells alone is insufficient; the access-support and opposed-contact constraints are the contribution.

Higher thematic overlap with battery service. The physical access dependency and full identity-preserving exchange must remain central; cosmetic differences are not evidence of novelty.

[DataCenterBench](https://robocurve.org/datacenterbench/) already covers connector handling and lists battery/nut candidates. [RoboDojo](https://robodojo-benchmark.com/doc/sim-tasks/fasten-screws/) already tests independent threaded pairs. Neither repetition nor renaming establishes novelty.

[LIBERO's catalog](https://github.com/Lifelong-Robot-Learning/LIBERO/blob/master/libero/libero/benchmark/libero_suite_task_map.py) and [SimplerEnv's environment list](https://github.com/simpler-env/SimplerEnv#current-environments) include placement and access primitives. [RoboCasa's registered tasks](https://github.com/robocasa/robocasa/blob/main/robocasa/__init__.py) include lids and multi-step kitchen work. [BEHAVIOR furniture assembly](https://behavior.stanford.edu/knowledgebase/tasks/assembling_furniture-0.html) specifies attachment outcomes. These comparisons support a mechanism-specific contribution, not a claim that long sequences are new.

The screen examined nearby PR descriptions/available implementation and review comments, primary task catalogs, and relevant attachment definitions. Search coverage is imperfect and pending submissions change. Native feasibility remains a separate unresolved criterion.

Current board comparison: pilot TK-PUCVX4 is titled “Insert batteries into a TV remote” and provides no setup, scorer or fidelity specification. Battery insertion itself is therefore an existing theme, and this submission does not claim it as new. The contribution is maintaining access against a physically verified spring-return sliding cover through complete old-cell removal and opposed-polarity replacement. More cells or colors alone would not distinguish it.

Pending TK-ATKRUQ installs one cell in a spot welder whose lid springs open and stays open; TK-6FB8W7 releases that lid and tips a cell out. This fixture instead has a cover that closes when support is removed, so supported access persists across collection and replacement. TK-2GRHHM imposes a four-second empty-bay limit on block-shaped packs without contacts or latches; this fixture imposes actual spring-contact geometry and return-force access, with no artificial hot-swap timer.

Both cold expert demonstrations continuously support the cover with a robot hand, and the native return probe passes twice. The score accepts alternative nondestructive physical strategies that achieve the stated outcomes; it does not require matching the expert's exact arm choreography. These distinctions support submission for review, with residual overlap in the battery-service theme and no guarantee of official acceptance.
