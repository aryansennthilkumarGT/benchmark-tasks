# Executed YUBI geometry study

This is **one bounded CPU geometry study**, with an envelope screen followed by exact CAD resolution of its least-overlapping case. It is not a contact prototype or full YAM-access pass.

## Actual results

- 315 source collision hulls per arm,630 total; both arms at valid source ready joint coordinates,8mm declared jaw gap.
- 45 source STEP occurrence envelopes, excluding only the controller installed after band step11.
- 28 static placements:7 fixture yaws ×4 hook/TCP offsets. All28 overlapped conservative envelopes and were **inconclusive**, not proved collisions.
- The separated control was clear; a source grip envelope deliberately placed in the palm was detected as overlapping.
- Exact OCCT narrow phase on the least-overlapping case (`yaw=-90°`, hook25mm ahead of TCP): upper plate/left-tip distance1.485316mm; FLAP_R/right-tip common volume26.395221mm³; another flap/tip pair touched within numerical precision. This rejects that particular direct-hand pose.

Outputs: [envelope JSON](YUBI_ENVELOPE_RESULT.json), [execution](EXECUTION.txt), [exact CAD JSON](YUBI_NARROWPHASE_RESULT.json), [narrow-phase execution](NARROWPHASE_EXECUTION.txt).

## Reproduce

From repository root, use the existing CPU Python environment with NumPy/SciPy; exact narrow phase additionally uses CadQuery2.7/OCCT. This execution used NumPy2.3.5 and SciPy1.17.0. No CUDA, Isaac or simulator package is required.

```bash
python research/robocurve-final-discovery/cpu_preflight/yubi_envelope_screen.py
python research/robocurve-final-discovery/agents/robot_build/evidence/fetch_yubi_pinned.py --out /tmp/yubi-pinned-source
python research/robocurve-final-discovery/cpu_preflight/narrowphase_best_case.py --source '/tmp/yubi-pinned-source/STEP/glove/YUBI Glove Assy_ver2_R.STEP'
```

The compact source occurrence manifest is committed. The larger original STEP is freely reproducible with the pinned fetcher and its SHA256 is checked before use. No checkout of the research branch is changed. An ezdxf cache-directory warning is harmless; it does not affect output.

## What these numbers mean

The first stage compares actual robot convex hulls with conservative per-part bounding boxes in the original assembled frame, transformed into declared candidate fixture poses. Intersecting boxes cannot prove source-solid collision. The second stage constructs the actual convex hull solids and intersects the exact transformed source STEP bodies for **all three** overlapping pairs of the selected case. One pair proves real model penetration.

No loop exists in this study. The8mm jaw gap is an approach setting, not a validated band grasp. Source placement is an authored bench-placement hypothesis, not Toyota's fixture specification. There is no fixture collision geometry, complete continuous trajectory, arm self-collision certificate, second-hook route, material force/retention result, native expert or model evaluation. Zero clear envelope cases does not prove all possible approaches impossible; one rejected pose does not justify deleting the source flap. A different grasp or an ordinary tool requires a new finite coupon gate.
