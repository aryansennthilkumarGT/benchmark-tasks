# Asset and software provenance

All task geometry is original primitive USD construction from scene.json; no third-party task assets or identifying textures are embedded. Official robot/station dependencies are fetched at the commits in stack-lock.json. Robot collision audits use the adapter's actual convex YAM URDF. The scripts, controller, scorer, tests and native probes in this folder are the task implementation. Physical results are recorded in validation.json only after actual execution.

Fixture anchors reference the asset static Xform, with fixed-base articulation roots on the root joint, following the [OpenUSD joint reference-frame example](https://openusd.org/release/api/usd_physics_page_front.html). Offline USD checks compose the whole task at its spawn transforms and inspect real physics descriptors. The validator uses one USD worker to avoid a reproduced Windows usd-core 25.11 parallel-parser crash; this is not a native simulation setting.

Publication preparation preserves all runtimePython/scene/assets/scorer/controller phases from143732600e471baab1ef80aa7a2d81d813159866. Documentation explains noncolliding carrier links, material surrogates and actual controller targets. Final evaluated results and runtime equivalence must be verified before submission.
