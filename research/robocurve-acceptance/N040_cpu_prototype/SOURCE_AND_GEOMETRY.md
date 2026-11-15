# N040 local clip/seat/tool coupon — provenance and mechanism

**Exploratory parameterized study; not a Hyundai-specific physics validation.** Candidate hardware is Hyundai trim fastener **82315-2P000**, user-reported replacement for **82315-38000**, with a nominal **9 mm receiving hole**. Compatibility with the proposed left-front 2013 U.S. Elantra UD donor is **not independently established**. The exact retainer topology could invalidate this entire two-leg hypothesis. No authenticated part photograph or measured cross-section was obtained. This is the bounded alternative authorized when the real interface cannot be established.

## Source inventory

| Source | What was actually obtained | What it supports / does not support |
|---|---|---|
| [HyundaiPartsDeal door-trim catalog](https://www.hyundaipartsdeal.com/parts-list/2013-hyundai-elantra-us_alabama_made/trim/front_door_trim.html) | User-located link; new retrieval failed with proxy tunnel 403. | User attribution of old/replacement number and donor catalog only. **Not independently re-read; no OEM fitment certification.** |
| [Supplier catalog, page 784](https://online.flippingbook.com/view/153487453/784/) | User-located link and approximate dimensions; retrieval failed with proxy tunnel 403. | Supplier-attributed 9 mm receiving hole, 13 mm upper head, 13 mm stem, 19 mm overall. No validated CAD, tolerances, leg shape, material or force. |
| [CHARM reproduction, page 863](https://github.com/Kmberry1989/Elantra/blob/0f7b23efdcf6ecc48919fb781be7e95a1b8f0f06/2013%20Hyundai%20Elantra%20L4-1.8L/pages/863.html) | Re-read pinned Git source, extracted in evidence/workshop-extracts.json. | Door-trim procedure: quadrant cover, screws, trim removal, inside-handle cage, connectors; replace damaged clips. Attributed workshop reproduction, **not authenticated Hyundai OEM publication**. No metric door/clip dimensions. |
| [CHARM reproduction, page 887](https://github.com/Kmberry1989/Elantra/blob/0f7b23efdcf6ecc48919fb781be7e95a1b8f0f06/2013%20Hyundai%20Elantra%20L4-1.8L/pages/887.html) | Re-read pinned source. | General interior-trim instruction to use a plastic panel removal tool and avoid bending/scratching. The cited section is scuff/pillar/interior trim, **not an exact front-door tool SKU or clip release drawing**. |
| Alternative supplier/photo investigation | Bing, Google, eBay, ClipsAndFasteners, Dorman and Auveco search endpoints all returned tunnel 403. GitHub exact-part repository/issue searches and Hyundai trim-clip README search returned zero results. | No alternative drawing, equivalent supplier dimension or authentic part photo was recovered. Zero bounded search results do not establish absence elsewhere. No inferred part equivalence. |

[evidence/source-attempts.json](evidence/source-attempts.json), [alternative attempts](evidence/alternative-source-attempts.json) and [bounded GitHub search extracts](evidence/additional-source-searches.json) preserve URLs, UTC attempts, errors and available hashes. The guessed individual-part URL in the attempts file is labelled exploratory here; it is not evidence that such a page exists. No blocked passage was quoted or fabricated.

## Geometry inventory: supplied, estimated and unknown

| Quantity / feature | Value used | Provenance / role |
|---|---|---|
| Receiving diameter | 9 mm nominal | User-attributed supplier specification, not re-read. Used in contact equations. |
| Upper-head diameter | 13 mm nominal | Same attribution. Envelope metadata only; exact head/carrier shape not known or simulated. |
| Stem length | 13 mm nominal | Same attribution. Used as hypothetical profile extent. |
| Overall length | 19 mm nominal | Same attribution. Envelope metadata only. **19−13 is not a verified mounting-stack height.** |
| Dimensions estimated from drawings/photos | **None** | No uncalibrated service illustration was scaled. |
| Receiving sheet | 0.8 mm thickness, fixed, cylindrical hole | Assumption; actual sheet material, thickness, burrs, chamfer, embossment, coating and flange curvature unknown. |
| Stem root position | 6 mm above upper hole face | Independent assumption, not inferred as authentic from the envelope lengths. |
| Rest radial profile | Radius 2.7 mm to axial coordinate 6.8 mm; rises to 5.3 mm at 7.2 mm; tapers to 2.4 mm at 13 mm | Entirely assumed opposed-barb geometry. Coordinates run down from root. Exact clip may be multi-fin/fir-tree, slotted or another topology. |
| Flexible legs | Two symmetric equivalent beams: effective L=7, width=4, thickness=1 mm | Assumed reduced deformation basis, not measured wall thicknesses. Beam mode continues linearly beyond effective flexure. No assertion of actual two-leg construction. |
| Adjacent panel | Local uplift spring 8 N/mm; 2 mm thick contact surface; footprint x∈[−9,4] mm | Assumed panel section/support, not whole-door stiffness or geometry. |
| Captured head carrier | Unilateral uplift coupling, 0.2 mm slack, 180 N/mm stiffness | Assumed mounting-pocket compliance. Real head neck, slot, keyhole/carrier, pull-through and tearing geometry unknown. Not a literal CAD head-seat contact. |
| Tool | Plastic-type tapered nose: local x=8…10 mm, top z=0.8…0.6 mm, pivot (−10,−1) mm; 100 mm effective handle | Assumed ordinary pry/wedge surface. Nine surface points, rigid rotation, compliant unilateral contact. Two fork/prong contacts are collapsed into one planar resultant. No actual SKU, fork slot, 3D thickness, root radius or strength has been verified. |

The full authoritative numerical input for each run is its `parameters` object in [results/summary.json](results/summary.json); the nose shape is in `Coupon.__init__`. Motion is a **prescribed tool boundary condition**, not a commanded retainer trajectory. Neither root extraction nor leg deflection is prescribed. This model does not establish that a real fork can fit behind the authentic clip; out-of-plane slot/prong collisions are absent.

## Material, contact and uncertainty

Assumed equivalent plastic modulus is 1500 N/mm², yield strain 0.04 and isotropic hardening ratio 0.05. They are not verified nylon/polypropylene properties for this part. The two leg spring stiffnesses follow `k=E*b*t³/(4*L³)` (4.373 N/mm baseline). Cantilever root strain is approximated by `1.5*t*q_elastic/L²`; 1D irreversible plastic set is solved by an incremental return map. The panel has a separate assumed yield displacement of 6 mm (48 N internal spring load). This models permanent set, **not fracture, tearing, whitening, fatigue or damage calibration**.

Hole contact uses a unilateral normal penalty, 30,000 N/mm for the *weighted wall resultant*, sampled at 48 midpoint positions over finite sheet thickness. Plastic-tool contact has 1000 N/mm effective penalty stiffness. These are numerical regularizations, not measured local material stiffnesses. Coulomb axial friction is regularized at 0.0001 mm, coefficient 0.25, and uses the previous load increment's normal force. That lag and the continuation term 0.01 N/mm are numerical approximations. Friction, temperature, moisture, aging, molding orientation and repeated extraction history are unknown. See [sensitivity](PARAMETER_SENSITIVITY.md) for assumed ranges and nonconverged peak-force detail.

## Physical load path and state observation

1. The nose rotates under the local underside. Its actual transformed points must overlap the panel contact footprint; a translated nearby tool has no contact.
2. Nose normal force lifts the compliant panel. Once the carrier slack closes, the panel pulls the captured head/root through a unilateral spring.
3. The oversized shoulder bears against the finite receiving-hole wall. Contact energy depends on axial position and leg deflection. Its gradient resists extraction and bends the legs inward. Beam/plastic energy, panel bending, friction and carrier load determine equilibrium together.
4. When the shoulder passes the upper hole face, wall contact falls away and elastic legs recover. No latch state is changed and no force law is disabled by a success flag.
5. A **read-only** audit checks whether any oversized portion of the *free recovered material profile*, including plastic set, is still below the seat. It also requires negligible wall load and recovered elastic deflection. This differs from panel position, tool proximity, extraction depth or the current compressed diameter. Complete stem withdrawal is reported separately.

Audit tolerances are numerical: 5,201 material-profile samples, 0.002 mm oversized-radius margin, residual wall normal below 0.05 N, elastic deflection recovery within 0.02 mm, and irreversible set above 0.001 mm flagged as damage. Solver bounds are 0–20 mm panel/root motion and 0–2.4 mm inward leg amplitude; they are continuation limits, not stops measured on a real part. No valid reported release depends on an upper bound. In eventual real-hardware scoring, a backside view or direct retaining-shoulder inspection and a separately justified low-load retention check would be needed; panel displacement alone cannot establish release. No such physical measurement was performed here.

Wrong upper-face contact pushes against the installed lower stop; it cannot engage the lifting carrier. It produces excessive penalty overclosure in the imposed motion and is flagged outside the contact model's domain, rather than reported as a plausible 3.5 kN plastic-tool result. Large-barb sweep cases that make the one-mode legs cross the axis are likewise explicitly invalid. No physically admissible success is awarded to them.

## Can the genuine part be removed nondestructively?

**Unresolved.** The reduced hypothesis admits nondestructive release over some assumed parameter sets. That is not evidence that 82315-2P000 behaves this way. Neither leg topology, insertion orientation, extraction force curve, strain limit nor receiving seat is authenticated. The workshop reproduction explicitly permits replacement of damaged clips, so universal genuine-clip reuse must not become an invented task requirement. For this coupon, `valid_success` uses a deliberately strict no-plastic-set diagnostic to distinguish reversible mechanics from a destructive bypass. A later service task needs a source-bound consumable-clip policy; a normally replaceable damaged clip is different from a torn panel/seat, broken connector or unrecovered fragment. No hardware was purchased or tested.
