# SAC spindle-carrier mounting core — incomplete task

This branch is work in progress. It does **not** contain a completed scene, generated assets, a SAC robot phase plan, native qualification or submission-ready metadata. It must not be counted as a rebuilt task or sent for evaluation. No replacement hardware dimensions are asserted.

## Bounded procedure

The selected subset is the unloaded mounting step: with the clutch disc already centered, cover already located on its dowels and three correct temporary studs installed, lower the three-arm carrier over those studs and the centering tool, then fit all three knurled retainers as specified by the LuK instructions. Stop before turning the central pressure spindle against the diaphragm. The pressure spindle remains retracted; diaphragm force, permanent bolt torque and later tool removal are outside this subset. This is section 10.6, page 29's carrier/retainer setup, not a renamed generic spring-loaded plate or a claim to install an entire clutch.

The exact instruction interpretation and final flush/support datum must be checked against the measured tool before freezing the scene. The counterpart Sealey manual describes mounting the three-slot plate with stud retainers before hand-contact and subsequent pressure-screw compression. It corroborates the bounded step, not dimensional interchangeability of the two brands.

## Implemented and tested

- `mounting_score.py`: executable three-site/C3-symmetric carrier placement, independent pitch-consistent retainer histories, one-to-one site credit, released-hand stability, invalid-state/fixture/lost-part guards and recomputed partial credit.
- `dimensions.py`: explicit measurement units, provenance and uncertainty; source-backed flywheel thread-family lookup; bore/slot/thread compatibility checks; rejection of missing or synthetic hardware dimensions in production use.
- `feedback.py`, `motion.py`, `expert.py`: retained reusable joint-observation executor from the completed shackle package. They are not a generated SAC-specific phase plan and are not claimed to complete this task.
- `test_mounting_core.py`: synthetic numerical and adversarial tests. Its geometry is explicitly fictional test input, rejected as production measurements. No test frame or ideal result is physics evidence.

```bash
python -m pytest -q -p no:cacheprovider tasks/sac-clutch-tool-installation/test_mounting_core.py
```

## Required inputs before scene authoring

The LuK manual specifies the procedure, 120-degree stud arrangement, M6/M7/M8 stud families and centering-adapter ranges. It does not dimension the carrier, retainer or stud lengths. The Sealey VS011A.V3 manufacturer product/manual confirms flywheel-side M6×1, M7×1 and M8×1.25. Those values **do not establish the separate upper stud/knurled-retainer thread**. Neither source supplies a carrier mass, component dimensions or a diaphragm load curve.

The required measured hardware fields are enumerated in `dimensions.REQUIRED`. In particular: installed stud circle and tip height, usable upper thread and its actual diameter/pitch, carrier thickness/slot limits/central clearance, retracted spindle/centering-tool clearance, and retainer dimensions/masses. A published dimensioned drawing or actual measurement reference is required for each; case/shipping dimensions and perspective photographs are not accepted as component measurements.

The overall kit weight is not a carrier mass. The LuK 22 Nm + 90-degree permanent-fastener instruction on page 30 is not a load law for the diaphragm or pressure spindle and is not used by this core.

If the user explicitly permits a dimensioned benchmark fixture, its authored geometry must be clearly distinguished from manufacturer hardware and this input policy revised accordingly. Until that modeling choice or measurements are supplied, filling the missing values would contradict the instruction not to invent dimensions. No placeholder assets or silent geometric defaults are generated.

## Primary references

- Schaeffler/LuK, *LuK Repair Solution for Clutch Modules*, September 2012, single-plate Audi 0B1/0B2/0B3 module; tool 400 0237 10, pages 14–15 and section 10.6 pages 27–30. Exact URL and retrieved hash are in SOURCES.json.
- Sealey, [SAC Clutch Alignment Tool VS011A](https://www.sealey.co.uk/sac-clutch-alignment-tool-vs011a/) and [manufacturer instructions](https://www.sealey.co.uk/content/pdfs/instructions/VS011A_V3.PDF), specification and fitting steps 5.3.8–5.3.13.
- O*NET [Automotive Service Technicians and Mechanics, 49-3023.00](https://www.onetonline.org/link/summary/49-3023.00).

No GPU work, model evaluation, upload or official PR has been performed. The completed shackle branch and pending/finally rejected PR heads remain unchanged.
