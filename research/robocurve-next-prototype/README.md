# Next executed CPU prototype

Implemented unit: **ODRI Foot Contact Switch v1 silicone-centering contact coupon**. It uses sections of the actual registered manufacturer STEP parts, twelve free deformable 6/4 × 3 mm tube cross-sections and the designer-reported approximately 10 g moving assembly. This is a planar mechanical feasibility unit, not a full twelve-piece assembly or sensor simulation.

CELLO and Chefman were examined first and stopped at essential source gates. Their inspections and failures are retained. The earlier discovery portfolio and the YUBI/Faze4/Toshiba checkpoint are unchanged.

**READY FOR FULL IMPLEMENTATION: NO.** The nominal contact unit passes; axial capture, loaded acquisition, complete YAM access and real material response remain unproved. See [executed results](EXECUTED_TEST_RESULTS.md), [source boundary](SOURCE_AND_ASSUMPTIONS.md), [physical scoring](PHYSICAL_SCORING.md), [decisions](CANDIDATE_DECISIONS.md) and [remaining gate](NEXT_GATE.md).

## Reproduce

From repository root, Python 3.12:

```bash
python -m pip install --only-binary=:all: --target /workspace/robocurve-cpu-deps -r research/robocurve-next-prototype/requirements-cpu.txt
python research/robocurve-next-prototype/run_all.py
python research/robocurve-next-prototype/hash_manifest.py --verify
```

The CPU dependency versions are the same as the previous checkpoint. No Isaac, CUDA, GPU context or paid service is invoked. The complete runner uses committed CAD and previous committed source/YAM assets; it needs no network. Hash verification checks bytes, not physical validity. Inspect platform-dependent numerical/PNG differences before explicitly refreshing the manifest.

For the mechanism only:

```bash
PYTHONPATH=/workspace/robocurve-cpu-deps python research/robocurve-next-prototype/odri/mechanism_tests.py
PYTHONPATH=/workspace/robocurve-cpu-deps python research/robocurve-next-prototype/odri/mechanism_tests.py --mode sensitivity
```

[elastic_ring.py](odri/elastic_ring.py) implements intrinsic curved-beam stretch/bending and finite-thickness self/contact energy; [mechanism_tests.py](odri/mechanism_tests.py) solves the free foot and rings under gravity and declared probe forces. No node is attached to a target, no foot pose is assigned after initialization, and no hold state or installed latch exists. A numerical domain hit invalidates a trial; it is never a physical retaining stop.

The full-hull [YAM screen](odri/yam_access.py) is a separate static held-tool/support hypothesis. Its configurations cannot be used as a loaded robot demonstration. Raw outputs, immutable sources and hashes are committed alongside the code. Optional source-refresh scripts use public Git/GitHub; the preserved snapshots suffice for offline inspection.
