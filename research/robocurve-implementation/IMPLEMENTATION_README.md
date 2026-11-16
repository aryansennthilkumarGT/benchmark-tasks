# Executed CPU implementation

**Implemented: a representative microwave turntable/carrier/drive contact coupon, following the Toshiba installation topology.** Its physical mechanism and eight negative controls pass. It is **not** exact Toshiba CAD, a completed YAM task or permission to begin native/GPU work. Full implementation recommendation: **NO at present**.

YUBI was attempted first and stopped at its source/access gate. Faze4 was attempted next and stopped at nominal rigid closure. Their code and negative results are preserved in separate directories. No fourth candidate was investigated and the previous research portfolio was left unchanged.

## Run

Python3.12 and CPU wheels are required. From repository root:

```bash
python -m pip install --only-binary=:all: --target /workspace/robocurve-cpu-deps -r research/robocurve-implementation/requirements-cpu.txt
python research/robocurve-final-discovery/agents/robot_build/evidence/fetch_yubi_pinned.py --out /tmp/yubi-pinned-source
python research/robocurve-implementation/run_all.py
python research/robocurve-implementation/hash_manifest.py --verify
```

The committed [hash manifest](MANIFEST.json) records code, inputs, outputs and reused source hashes. Regenerating outputs can produce platform-dependent floating-point or image-byte differences; inspect those differences before deliberately refreshing the manifest with `python research/robocurve-implementation/hash_manifest.py`.

`run_all.py` writes each command's output beside its results and stops on an unexpected failure. A deliberately failed candidate gate is a recorded experiment result, not a crashed runner. Source CAD/frame extraction uses CadQuery; access uses the existing YAM reference and FCL; the contact coupon uses headless MuJoCo CPU. No rendering context, CUDA, Isaac, Brev, Dream or paid service is invoked.

For the successful mechanism alone:

```bash
PYTHONPATH=/workspace/robocurve-cpu-deps python research/robocurve-implementation/toshiba/contact_coupon.py
PYTHONPATH=/workspace/robocurve-cpu-deps python research/robocurve-implementation/toshiba/yam_access.py
PYTHONPATH=/workspace/robocurve-cpu-deps python research/robocurve-implementation/verify_results.py
```

## Inspect

- [Actual results](EXECUTED_TEST_RESULTS.md), [negative controls](NEGATIVE_CONTROLS.md), [physical scoring](PHYSICAL_SCORING.md)
- [Source/assumption boundary](SOURCE_AND_ASSUMPTIONS.md), [candidate decisions](CANDIDATE_DECISION.md), [remaining native gates](NEXT_NATIVE_MILESTONE.md)
- [Contact code](toshiba/contact_coupon.py), [independent observation scorer](toshiba/scoring.py), [explicit parameters](toshiba/parameters.json)
- [Raw contact results](toshiba/results/CONTACT_RESULTS.json), [full-hull access results](toshiba/results/YAM_ACCESS.json)
- [YUBI access code](yubi/access_gate.py), [Faze4 closure code](faze4/closure_gate.py), [independent Faze4 checks](faze4/independent_checks.py)

The positive experiment starts with a genuinely free, unengaged tray 30 mm above its nominal seat. Gravity, three hinged wheels and actual three-lug contact geometry determine the final pose. Only the input shaft is actuated. There is no tray actuator, equality/gear constraint, mocap body, success latch or post-initialization tray-pose assignment. A prescribed held-tray relationship appears **only in the separate collision-planning hypothesis**, never in the successful contact experiment.

The stock-YAM paths are **blocked in the tested representative door layouts**. No dynamic acquisition, gripping-wrench capacity, continuous path or exact-donor clearance is claimed. This contact result must not be presented as a scripted robot demonstration or official score.
