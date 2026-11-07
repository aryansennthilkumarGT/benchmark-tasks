# Source and asset provenance

All task-specific source and primitive scene definitions in this folder were authored for this
development effort. USD assets are deterministic exports of `scene.json` by `build_assets.py`.
There are no downloaded object meshes, textures, vendor logos or third-party task assets.

The external `yam_arena` adapter and robot are dependencies, not vendored code. API conventions
were inspected in the public adapter and the official accepted examples. The adapter's own license
and the I2RT robot asset license must be checked when installing/distributing those dependencies.
No license for third-party assets is inferred from their availability on GitHub.

This folder contains no simulation outputs. The unit tests deliberately construct synthetic states
to exercise predicates; their 1.0 values are mathematical fixtures, not expert demonstrations.
