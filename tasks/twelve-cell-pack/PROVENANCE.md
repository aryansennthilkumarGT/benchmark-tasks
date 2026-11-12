# Asset and software provenance

All task geometry is original primitive USD construction from scene.json; no third-party task assets or identifying textures are embedded. Official robot/station dependencies are fetched at the commits in stack-lock.json. Robot collision audits use the adapter's actual convex YAM URDF. The scripts, controller, scorer, tests and native probes in this folder are the task implementation. Physical results are recorded in validation.json only after actual execution.

Fixture anchors reference the asset static Xform, with fixed-base articulation roots on the root joint, following the [OpenUSD joint reference-frame example](https://openusd.org/release/api/usd_physics_page_front.html). Offline USD checks compose the whole task at its spawn transforms and inspect real physics descriptors. The validator uses one USD worker to avoid a reproduced Windows usd-core 25.11 parallel-parser crash; this is not a native simulation setting.


The evaluated executable revision is `1e7df189c4cf7e86ad57a9cb37fe584a7adfc5f3`. Native physics and control suites, two expert episodes and the Dream-1 trial use that revision. Publication changes update documentation, measured validation metadata, scores, media ID and the unused controller status annotation; the controller phase data, executable Python, scene, scoring, physics probes and USD assets remain unchanged. A fresh HTTPS checkout of the evaluated revision independently reproduced a full-score expert trial.


The offline-evidence directory retains historical static audit outputs. Current measured native, expert, model, media and clean-checkout results are in validation.json; running static_check.py executes the current offline tests and audits.
