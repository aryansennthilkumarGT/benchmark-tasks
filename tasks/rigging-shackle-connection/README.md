# Fit and seat a screw-pin shackle through a lifting lug

Connect a supported sling link to a lifting lug using the matching screw-pin bow shackle. Align the two shackle eyes with the lug, insert the pin, turn it through its real contact thread until the collar seats, release and withdraw. This is an unloaded rigging-assembly subprocedure. It does not certify a lift or replace inspection, load selection or operational tightening checks.

O*NET identifies attachment of loads using rigging and tools as regular rigger work. Green Pin's G-4161 product information explicitly describes frequent assembly/disassembly applications. Its catalogue requires a matching pin, complete threaded-eye engagement and fully seated collar; a wrench or suitable tool follows hand tightening. Here the robot's parallel jaws act as the pin-tab turning tool. Their ability to produce reliable native contact and seating is untested. See SOURCES.json and NOVELTY.md.

## CPU reproduction

Use Python 3.12, NumPy 2.3.1, usd-core 25.11 and the pinned YAM/Inspect packages in requirements-cpu.txt. From the repository root:

```bash
python tasks/rigging-shackle-connection/static_check.py
```

This verifies source hashes, runs deterministic tests, composes actual USD, solves every authored TCP endpoint, checks nominal thread geometry, runs the real controller against an explicitly synthetic ideal-tracking fixture, and samples robot/fixture/table/inter-arm collision geometry using the pinned YAM URDF. It never launches a simulator, model or cloud instance. The ideal-tracking fixture assumes jaw contact; it cannot establish friction or grasp success. The robot collision audit samples critical poses, not every swept configuration. Preserve its coverage limits when reporting results.

To intentionally change the scene, edit generate_scene.py, regenerate assets with that script, update documentation/tests, and refresh source_manifest.json. Do not regenerate assets merely to bypass a changed-source error. All authored geometry is original; external drawings and catalogue pages are cited rather than redistributed.

## Runtime qualification: GPU-ONLY here

Preview the full standalone sequence:

```bash
python tasks/rigging-shackle-connection/bootstrap_task.py --output /data/shackle-qualification --model
```

On a separately authorized official Linux YAM/Arena installation, after verifying actual hardware and provider budget, use the same command with the real `--budget-file` and `--launchable-root` paths and `--execute`. For the known L40S driver 565.57.01, the existing bootstrap verifies the installed stack and requires the scored station smoke; it does not request a driver change. No GPU budget is authorized during this CPU rebuild. The inherited budget monitor retains its $170 cap and $30 reserve; reconcile those constraints with any future authorization before execution.

When already inside the exact verified runtime, the executable native commands are:

```bash
python tasks/rigging-shackle-connection/native_tests.py --mode physics --output /data/shackle-physics --commit "$(git rev-parse HEAD)"
python tasks/rigging-shackle-connection/native_tests.py --mode control --output /data/shackle-control --commit "$(git rev-parse HEAD)"
python tasks/rigging-shackle-connection/task_runner.py --output /data/shackle-trials --execute --model
```

Do not run these in the CPU engineering environment. The runner checks every declared case after two resets, two distinct full-score expert records, genuine Dream provider identity and complete actions/three-camera streams, scorer replay, actual media export and full video decoding. `--resume` verifies hashes; changed input commits create new attempts, while failed stages remain preserved. No expert/video/model score is claimed in validation.json. A fresh clean-checkout expert must additionally reproduce the qualified result before submission.

## Expert and scoring

The expert uses robot joint positions and SDK time only. Its phase machine aligns the shackle with the left arm, releases it into the passive nest, parks that arm to avoid interference, and inserts/threads the pin with the right arm. Forty-eight 45-degree strokes give six turns; each includes real jaw release, vertical clearance, wrist unwind, lowering and regrasp. The final opening occurs in two stages to clear the bow before fully opening. It has joint tracking, action limits, measured progress checks and bounded failure; no pose writes, virtual screw constraint, attachment, score-state feedback or hidden fallback exists. See CONTROLLER.md.

Full score requires visible collar seating and through-lug span, pitch-consistent turn history, stable parts and both hands clear. Credit is recomputed. Bad frame schemas, missing parts, unnormalized quaternions, fixture displacement, loss or excessive overlap latch zero. No operating WLL, structural strength, calibrated wrench torque or watertightness claim is made. See SCORING.md and MEASUREMENT.md for numeric boundaries and physical judging.

The action limit is 18,000 at 20 Hz (900 simulated seconds). Native runtime and actual completion time remain unmeasured. CPU reachability and synthetic controller completion do not establish a successful robot demonstration.

## Media and submission

After genuine qualification, inspect the initial screenshot, both independent expert videos, model video and contact sheets for framing, outcome and identifying information. Record an actual review JSON with the qualified commit, SHA-256 of `model.mp4`, `demo.mp4`, `demo-repeat.mp4`, `setup.png`, and `visually_reviewed: true`. Never create that attestation before inspection.

```bash
python tasks/rigging-shackle-connection/prepare_submission.py \
  --qualification /data/shackle-trials --review-file /data/shackle-visual-review.json \
  --output /data/prepared/rigging-shackle-connection
```

This verifies the native/expert/model/media receipt chain, binds review to exact bytes, and prepares a disposable metadata/media copy. It prints the official repository uploader command. `--upload` explicitly runs that uploader; only its server response supplies the media ID. Credentials remain in secure environment bindings. No PR is created by this package. An eventual independent PR must contain only this task folder and actual qualified results. Do not reuse or alter the finally rejected heads or PR #1733.
