# Actual interfaces and datums

**Measurements below come from the checked release STEP, in native millimetres.** They are CAD nominal geometry, not manufacturing tolerances. No metric quantities were estimated from source illustrations. Source face/occurrence IDs are reproducible for the pinned files, not universal hardware identifiers. Anatomical left/right is not inferred from native X signs.

## Source pipe and P1 seats

Occurrence0 is named `PIPE_15_100`: outer cylinder radius7.5mm,100mm axial span, native bounds X−114.25…−99.25, Y−116…−16, Z−7.5…7.5. The positive-X counterpart is also present. These are actual source bodies, not synthesized cylinders used in place of them.

| Source jig feature | Exact extracted geometry | Binding limit |
|---|---|---|
| Negative-X cylindrical seat, face688 |R7.5; axis along +Y through X−106.75,Z≈0; face spans Y−84…−36; area1130.973355mm² | Matches the source pipe's outer surface in the unshifted local overlay. Does not establish the whole KER's ready posture. |
| Positive-X cylindrical seat, face700 |R7.5; axis `(0,0.934049774,−0.357142857)`; bounds X99.25…114.25, Y−84…−35.642857, Z5.598836…32.118203 | Axis is **20.924832°** from the exported Y-oriented pipe. This is a CAD-axis comparison, **not an encoder offset**. Rotating/reposing the appropriate articulated chain is necessary; mirroring the first seat is incorrect. |

Full analytic surface records: [jig_faces.json.gz](results/jig_faces.json.gz). The two seats are present; the archive is **not** being declared to lack its fixture merely because the file is called JIG BASE.

## J8 holder/datums and four candidate fastener axes

The jig contains two holder regions with planar locating faces, through/counterbore surfaces and access from native −Y. Four unique cylinder axes (their half-faces must not be counted as eight holes) have radius1.2mm, hence nominal clearance diameter2.4mm. Each pair has6mm native X spacing:

| Candidate site | Two X coordinates | Z | Axis |
|---|---|---:|---|
| Negative-X holder |−80.365220892, −74.365220892|48.300000|parallel Y|
| Positive-X holder |65.079022274, 71.079022274|−6.700000|parallel Y|

These clearance surfaces span about native Y−118…−110; accompanying radius2.2mm surfaces are present. Holder-plane candidates at Y−110 include faces402/429; other locating flats include Z37 and Z−18 pads (faces405/440). These are **candidate functional mappings from actual geometry and workflow**, not a certified target registration. The corresponding J8/trigger assembly parts are present in the KER STEP, but the whole articulated placement that mates each flat and screw pair was not established. Do not put a tool target at a hole centre and call that stock-YAM access.

M2×12mm is verified in the workflow. Drive/socket form, selected real driver body/grippable area, actual engagement, torque/preload and allowed approach are still unbound. Hole diameter is not permission to enlarge the screw/tool or assume an arbitrary precision-driver shape.

## Rear body datum and integral lock geometry

The one-piece jig includes a rear upright, undercut/lead-in geometry and locating/support surfaces. Relevant exact profile records include:

- Face45: a planar surface at native Y30, spanning Z−25…0 over X±27.5.
- Face41: a planar upper face at Y26, Z12…20.
- Face42: a horizontal ledge at Z11; Y≈26.577350…28.5, width55mm by its bounds.
- Face14: rear plane Y40, spanning X±25.5 and Z−39…20.
- Face35: planar base underside Z−39. Face16 is at Z−31, giving an8mm floor in that region.

The manufacturer explicitly describes gently flexing the jig frame for its snap fit. Geometry/connectivity is present; **we did not replace it by a spring latch**. Which whole-body insertion configuration loads which exact profile, the fixed/support boundary, jig material/printing properties and force–deflection/damage response are not validated. Distances between profile planes must not silently become a cantilever thickness, spring stiffness or release-force curve.

The source assembly includes `BASE_A`, `BASE_B`, both mirrored/nonmirrored link/trigger parts and all509 occurrences. Example nominal BASE_A bounds are135.5×60×45mm. The native assembly envelope is260×525.2×293.993mm in its exported pose; the jig is243.5×160×90mm. An exported envelope is not its articulated swept envelope or its calibration-ready footprint.

## Source topology versus missing configuration

The files preserve both arms' components and their static placements. They do **not** establish a verified mapping of509 CAD occurrences into the actual rigid links, sixteen encoder-joint axes/limits and the registered ready configuration in the jig. The official KER library supplies angle streams, not that mechanical definition. The motorized follower's kinematics must not be grafted onto the motorless KER.

This missing registered articulated definition is the upstream geometry blocker for a complete source-bound path and full load-transfer test. It is potentially resolvable with a matching ready-state assembly/constraint model or an independently checked reconstruction from the real parts. It is not evidence that the actual fixture or robot is infeasible.

## Executed static CAD controls

[Exact Boolean/distance outputs](results/CAD_CONTACT_DIAGNOSTICS.json) use the actual pipe and full jig BReps, including two outer-cylinder face pieces. No proxy groove, force solver or scripted attachment was used.

| Diagnostic pose of that pipe | Minimum distance mm | Interference volume mm³ | Shared cylindrical seat surface mm² |
|---|---:|---:|---:|
| Unshifted source overlay |0|0|1130.973355|
| Raised1mm |≈0|0|0|
| Lateral shift1mm |0|495.579700|0|
| Axial shift60mm |0|0|471.238898|
| Axial shift120mm |23.5|0|0|

**Important result:** touching the jig somewhere does not imply cylindrical datum seating. The raised pipe still has zero minimum distance elsewhere but no shared seat patch; partial axial placement preserves some patch without establishing the required pose. These1/60/120mm shifts are diagnostic counterexamples, not allowable OEM errors. Coincident ideal-CAD area is not measured load-bearing contact area. Interference volume indicates incompatible rigid geometry, not a prediction of real deformation/damage. No row proves retained calibration readiness or complete KER support. These isolated-body perturbations do not assert that the assembled articulated KER can reach those layouts.
