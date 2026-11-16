# Articulated KER reconstruction — final bounded gate

**Result: source-supported articulated hypotheses recovered; complete mechanism NOT verified.** This is new reconstruction work after `f91fab0247eeb339f1b7d5eadb2289cba92708f1`, not a rerun of the five isolated-pipe diagnostics. The allocation decision is [PARK](FINAL_KER_DECISION.md).

## Sources actually inspected

The existing official hardware 2.0.0 archive and the two checksum-verified STEP files remain unchanged. [Original manifest](SOURCE_CAD_AND_BOM_MANIFEST.md), [new immutable source URLs/hashes](evidence/ARTICULATION_SOURCE_PROVENANCE.json), [full analytic face inventory for all 509 occurrences](results/occurrence_features.json.gz).

- Official KER `general.mdx` and `calibration-workflow.mdx`, OpenArm commit `e15e09e056098348d6f437389bbf48179caa82b6`: independently read through the existing local Git objects. Workflow figures step4 and step8 were extracted and visually inspected, rather than measured as scale drawings.
- Official follower `topology.yaml`, `joint_axes.yaml`, `joint_origins.yaml`, `joint_limits.yaml`, description commit `38c64af1dd6f3bc246883754875cbb4259dce0fc`: independently read. The seven-revolute topology supplies a hypothesis, not a KER URDF. Its limits were **not transferred**.
- All 509 occurrence names, placements and analytic faces were inspected programmatically. The released BOM was read; it distinguishes encoder housings/horns, C-FL6700ZZ bearings, pipes/clamps, AUU3-15 springs and backpack friction hinges. The publisher's warning that commercial components are simplified still applies.

Native units are mm. Occurrence/face numbers below refer only to the pinned source traversal. Positive/negative X are CAD conventions, not asserted anatomical labels. Cylinder `origin` is an arbitrary point on its axis, **not** a bearing center.

## Actual axes and evidence strength

Centers below are the midpoints of the physical bearing CAD envelopes. The axis lines, not an assumed center of revolution along those lines, define rotations. Housing R7.5 bearing seats and horn R5 shafts are coaxial with the bearing cylinders on both arms; machine residuals and mounting-hole candidates are in [ARTICULATED_AXES.json](results/articulation/ARTICULATED_AXES.json).

| Joint | Negative-X bearing occurrence | Envelope midpoint XYZ | Canonical axis | Positive-X counterpart | Complete-joint status |
|---|---:|---|---|---:|---|
| J1 | 2 | (−76.75, 0, 0) | X | 183 | SOURCE-SUPPORTED HYPOTHESIS |
| J2 | 16 | (−106.75, 0, −11) | Z | 197 | SOURCE-SUPPORTED HYPOTHESIS |
| J3 | 30 | (−106.75, −129, 0) | Y | 211 | SOURCE-SUPPORTED HYPOTHESIS |
| J4 | 44 | (−114.75, −154, 0) | X | 225 | SOURCE-SUPPORTED HYPOTHESIS |
| J5 | 58 | (−106.75, −264.5, 0) | Y | 239 | SOURCE-SUPPORTED HYPOTHESIS |
| J6 | 72 | (−80.75, −305.2, 0) | X | 253 | SOURCE-SUPPORTED HYPOTHESIS |
| J7 | 86 | (−106.75, −305.2, −14) | Z | 267 | SOURCE-SUPPORTED HYPOTHESIS |
| J8 | 100 | (−101.75, −373.2, −52) | X | 281 | SOURCE-SUPPORTED HYPOTHESIS |

Positive-X midpoints mirror X. All sixteen **axis identifications are VERIFIED geometric observations**. None of the sixteen **complete joint models** is promoted to VERIFIED: the released bearing solid does not separate inner/outer rings, full fastener ownership and operating movement bounds are unresolved. Signs are coordinate conventions; these angles are not magnetic-encoder zero offsets. KER limits, bearing friction and trigger spring/stop law remain UNKNOWN.

Each encoder interface has coaxial small mounting-hole candidates to the appropriate adjacent custom part. Negative-X housing/horn candidate-line counts by joint are respectively `4/4, 2/4, 2/3, 2/4, 4/4, 2/3, 2/4, 2/4`; mirrored counts match. These count unique coaxial lines, **not installed screws or verified finite threaded engagements**. This independently supports the named graph but does not prove every attachment is rigid or correctly fastened.

## Link membership actually reconstructed

The hypothesized graph is root → J1 → link1 → J2 → link2 → J3 → link3 → J4 → link4 → J5 → link5 → J6 → link6 → J7 → link7 → J8 → link8.

| Link | Source structural membership, negative-X names; mirrored counterparts inspected |
|---|---|
| root | BASE_A/BASE_B; J1 stator; CoreS3 body envelope |
| 1 | J1 horn; J1-J2; J2 stator |
| 2 | J2 horn; J2-P1; **P1 PIPE_15_100**, its two clamps; P1-J3; J3 stator |
| 3 | J3 horn; J3-J4; J4 stator |
| 4 | J4 horn; J4-P2; P2 pipe and clamps; P2-J5; J5 stator |
| 5 | J5 horn; J5-J6; J6 stator |
| 6 | J6 horn; J6-J7; J7 stator |
| 7 | J7 horn; J7-J8; GRIP; **J8 housing/stator** |
| 8 | **J8 horn and TRG**, moving relative to the housing |

A stator includes housing, PCB spacer and its source cover where present. A simplified bearing envelope is placed with its stator for collision auditing; this is not a claim that both bearing rings rotate together. Spring occurrences134/145 were frozen at the exported trigger pose **only as collision envelopes**, not declared rigid link members or simulated springs.

[Complete 509-row assignment ledger](results/articulation/OCCURRENCE_LINK_ASSIGNMENT.json) distinguishes 113 assigned structural/envelope hypotheses from **396 UNKNOWN assignments**: 373 fasteners and 23 backpack/hinge/holder/accessory bodies. The unassigned parts were not silently deleted from a claimed complete robot. The source BOM lists eight M2-8 screws whereas the CAD names ten occurrences; this inventory mismatch is preserved, not resolved by inventing extra function.

## What the 70% statement does and does not establish

The actual shoulder-axis intersection is (−106.75,0,0); elbow intersection is (−106.75,−154,0); wrist intersection is (−106.75,−305.2,0), with mirrored X counterparts. Thus the two functional link lengths are **154mm and151.2mm**. The follower's corresponding summed origin distances are220mm and216mm: exactly70% at CAD numerical precision.

The intermediate distances are not uniformly scaled: KER's shoulder–J3-bearing/elbow split is129/25mm, versus follower66.25/153.75mm before scaling; KER's elbow–J5-bearing/wrist split is110.5/40.7mm, versus follower95.5/120.5mm. Sliding a reference point along its rotation axis can preserve endpoint kinematics while changing every collision/grasp surface. This is why the reconstruction uses actual STEP geometry and source axes rather than a scaled follower mesh/URDF.

## Reproduction and actual execution

Python3.12, existing NumPy/SciPy and OCP7.8.1.1/CadQuery2.7.0; no package or GPU installation. From repository root, using the already verified extraction:

```bash
OPENBLAS_NUM_THREADS=1 python research/robocurve-acceptance/openarm_ker/RECONSTRUCT_KER.py --output-dir /tmp/ker-articulation
XDG_CACHE_HOME=/tmp/ker-cache OPENBLAS_NUM_THREADS=1 python research/robocurve-acceptance/openarm_ker/CHECK_ARTICULATED_POSE.py --source-dir /workspace/KER-source-inspection/reproduction-source --results /tmp/ker-articulation
XDG_CACHE_HOME=/tmp/ker-cache OPENBLAS_NUM_THREADS=1 python research/robocurve-acceptance/openarm_ker/CHECK_ARTICULATED_POSE.py --source-dir /workspace/KER-source-inspection/reproduction-source --results /tmp/ker-articulation --adjacent-only --max-pairs 160
```

To regenerate the analytic inventory from the source instead of consuming the committed cache, add `--extract --source-dir /path/to/extraction --features /tmp/ker-features.json.gz` to the first command. `KER_CAD.py` checks both source STEP hashes. Compressed-file timestamps can change gzip hashes; compare decoded records when regenerating. Run from the exact pinned CAD; other revisions may change face indices.

[Registration outputs](results/articulation/ARTICULATED_REGISTRATION.json), [actual run log](results/articulation/ARTICULATION_EXECUTION.txt), [body contacts](results/articulation/REGISTERED_BODY_CONTACTS.json), [bounded interference](results/articulation/BOUNDED_INTERFERENCE.json), [adjacent audit](results/articulation/ADJACENT_INTERFERENCE.json). Forked Boolean workers have a3-second per-operation limit; the completed audits reported **zero timeouts/errors**. They inspect the structural subset, not all509 bodies. No old numerical robot controls or isolated-pipe perturbations were rerun.
