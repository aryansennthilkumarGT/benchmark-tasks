# Source provenance

This independent branch adds only `tasks/rigging-shackle-connection` relative to repository base `7df8bd8ad8cb19df51718e5ff46d4d610a9da6f1`. It replaces the rejected generic service-arm concept in the recovery selection; it does not revise PR #1647 or reuse its results.

Original scene generation, assets, robot phase plan/controller, shackle-specific scorer checks, geometric/sequence audits, tests, metadata, measurement procedure and occupational comparison are authored for this package. Source files and generated USD are recorded in source_manifest.json. No manufacturer's CAD/drawing/document is redistributed; SOURCES.json cites primary factual references and retrieved-document hashes.

Reusable local engineering infrastructure comes from `draft/eight-nut-bracket` commit `197d32d07bf124616d616684a07faa1efa85b993`: compound USD compilation, generic rigid-body scorer, conservative geometry/URDF hull helpers, official runtime adaptation, native test harness, immutable ledger/bootstrap, launcher and media pipeline. The policy/controller is replaced with a robot-proprioception-only implementation. The rollout validator and provider-identity fix are taken from publication prototype `eb25b0019a2a66683cdef6a4837c382b6dfafbe6`. These are code reuse, not physical-evidence transfer.

All native, expert, model and media counts for this new task start at zero. Existing `/data` records and earlier task scores are historical and cannot qualify its changed geometry, controller or scorer. No private handoff module is imported by this package.
