# Intermediate/debug captures

Excluded from the final pass count:

- `INVALID_STL_FRAME_SECTIONS.png`: incorrect assumption that print STL and STEP frames coincide. Canonical sections are extracted from STEP, with explicit source registration.
- `INVALID_SUPPORT_IK_ACCESS.json`, `INVALID_REVERSE_GRIP_IK_ACCESS.json`: upward/reversed support hypotheses with unsolved IK; collision observations at these misreached configurations cannot prove a grasp.
- `BILINEAR_CONTROLS.json`: initial passing nominal equilibria/negative controls with a bilinear SDF. `UNCONVERGED_BILINEAR_SENSITIVITY.json` records iteration-limit/gradient failures; these are not passing material tests.
- `CONTACT_TRIAL*`, `FREE_FOOT*`, `DEFORMED_RING_NODES.npy`: intermediate prescribed-displacement/first free-foot trials. Prescribed motion is not evidence of passive return. Canonical free-body controls/sensitivity are under `odri/results/`.

Cubic signed-distance interpolation smooths the numerical grid-normal discontinuities. Source shapes and material parameters were not altered to force success. Its approximation error is independently checked. Some deliberately invalid material/contact cases can remain numerically unresolved; the final reports distinguish that from a physical hardware failure.

`PIN_OMITTED*` preserves an interrupted preliminary model that missed lateral guide-pin contact. Its roughly0.61 mm horizontal response is not valid evidence for the real source guide. The final model derives a0.4 mm center gap from actual STEP bores and applies unilateral normal contact. The grouped field evaluation changes computation batching, not the physical energy.
