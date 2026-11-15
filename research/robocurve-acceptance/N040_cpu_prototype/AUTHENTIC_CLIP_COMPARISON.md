# Authentic clip comparison and disposition

**Disposition: PARKED.** The existing two-leg/single-shoulder coupon is not justified as an approximation of Hyundai 82315-2P000 or Disco 12612PK. Preserve it as an explicitly hypothetical mechanics archive; do not tune it further as Hyundai hardware. There is insufficient independently inspected evidence to replace it with an authentic model in this revision.

## What the new lead actually establishes here

The user located the [Disco Automotive Hyundai catalog](https://discoautomotive.com/wp-content/uploads/2025/03/Section-22-2-Hyundai.pdf), **printed page 7 / PDF page 7, row 12612PK**. The user reports an aftermarket equivalent for Hyundai 82315-2P000, a 9 mm hole, 13 mm stem, 13 mm top head, white nylon, and a side-view illustration of a slotted/tapered stem with multiple upper flanges. These are **externally reported findings, not independently inspected in this environment**: the PDF returned proxy tunnel 403. The independent [FR12612 listing](https://www.shop-supplies.com/proddetail.php?prod=FR12612) and both supplied HyundaiPartsDeal pages also returned 403.

No image, crop, contour, flange count or dimension was reconstructed from this unseen PDF. Exact-PDF/part/supplier GitHub searches yielded no usable mirror; archive discovery was blocked. Even an inspected supplier image would establish an aftermarket equivalent, not original Hyundai CAD, precise internal sections or a calibrated force curve. See [CLIP_SOURCE_INVENTORY.md](CLIP_SOURCE_INVENTORY.md) for provenance and value labels.

## Mechanism comparison

| Feature | Existing equations / geometry | Authentic evidence available here | Consequence |
|---|---|---|---|
| Flexible member count | Two independently deflecting equivalent beams with symmetric results | UNKNOWN. User reports a slotted stem; no inspected orthogonal views or section. A visible slot alone would not establish the number of 3D legs. | Neither two legs nor their orientation/cross-section is justified. Do not infer two or four members from an unseen side view. |
| Stem slot | No actual slot width/depth, closed tip, bridge or leg-to-leg self-contact | UNKNOWN | The model cannot identify the flexure root, coupling or maximum inward travel. It only rejects negative-radius results afterward. |
| Retaining stem | A single peak at assumed axial 7.2 mm, preceded by a steep shoulder and followed by a linear taper | Only externally reported slotted/tapered appearance | The shoulder slope determines axial resisting force. Matching overall length cannot validate that slope or the retaining edge. |
| Upper flanges | Head diameter is metadata; flanges are not represented as contact geometry | Multiple upper flanges externally reported, count/thickness/gaps UNKNOWN | Potential mounting/cushioning/sealing features are absent. Upper flanges must not automatically be interpreted as multiple retaining barbs. |
| Door-trim mounting | A unilateral 180 N/mm spring with 0.2 mm slack transfers panel lift to clip root | Carrier slot/keyhole/pocket, neck capture, installed stack and pull-through resistance UNKNOWN | This invented coupling may select the wrong load path or suppress a real carrier failure. |
| Receiving sheet | Fixed 0.8 mm plate, 9 mm round cylindrical hole without lip/chamfer | 9 mm nominal hole externally reported; sheet thickness, burr, embossment and installed orientation UNKNOWN | Retaining engagement depth and edge contact are unbound. |
| Removal tool | A rotating 2D nose beneath a panel patch; no actual fork slot/prongs or head/carrier collision | Plastic tool supported at type level by the previously read workshop reproduction; exact tool and placement UNKNOWN | No demonstration that an ordinary tool can acquire this contact. |
| Compliance | One cantilever mode per assumed leg; independent reduced panel plasticity | White nylon externally reported; grade, moisture, section, nonlinear response and force curve UNKNOWN | Neither elastic stiffness, yield limit nor rigid/flexible partition follows from the material name. |
| Removal/reuse | Plastic set invalidates this coupon's strict nondestructive-release flag | Workshop reproduction says replace damaged clips; no part-specific damage frequency or consumption policy | Universal reuse and universal permitted breakage are both unsupported. |

The two-leg hypothesis is **not proved false** by a user-described side view. It is also **not demonstrated representative**. The unresolved slot, retaining edge, carrier and tool contact are essential to the equations, not cosmetic details. Drawing new flanges while preserving an incompatible two-beam energy law would not fix construct validity.

## Load path that must be resolved before replacement

Two candidate paths require authentic interface evidence: a fork may bear directly under an accessible clip flange/head, or a wedge may lift a panel region whose real carrier then transmits the load. They imply different contact surfaces, local panel bending and pull-through failure. Neither is selected as a verified operation here. The receiving edge must load the real retaining surfaces, the correct slotted portions must deform, and any upper flange compression or carrier compliance must be modeled where consequential. No particular flange is declared rigid without evidence.

A single side image may permit an **IMAGE-ESTIMATED outer silhouette** once actually inspected and appropriately scaled. It would still leave out-of-plane section, hidden bridges, installed stack and force response UNKNOWN. No inferred pixel length should be relabeled an OEM dimension. A replacement model should follow the actual topology—coupled slotted shell/legs, fins or another verified structure—not an a priori choice of two beams.

## A–E state separation using the archived outputs

This is an interpretation of the existing 51-run archive, **not new simulation or an authentic fastener score**. Machine-readable observations are in [ARCHIVED_STATE_CROSSWALK.json](evidence/authentic-correction/ARCHIVED_STATE_CROSSWALK.json).

- **A — retaining features disengaged:** the hypothetical free/recovered oversized profile clears the receiving seat, wall contact vanishes and elastic deflection recovers. This is the existing read-only retention audit.
- **B — stem partially withdrawn:** some axial withdrawal occurred but part of the stem remains in the receiving sheet. B can coexist with A or with retained barbs.
- **C — complete clip withdrawal from the receiving sheet:** all hypothetical stem material has cleared that sheet. This does not mean removal from its panel carrier, which is not geometrically modeled.
- **D — safe panel separation:** all real clips/upper edge, handle cage and plugs released as required; panel supported; seat/panel/harness condition acceptable. **NOT ASSESSED in every coupon run.**
- **E — destructive/invalid outcome:** modeled plastic set, invalid contact geometry, or absent initial retention. A or C may still be true; neither overrides E.

| Archived case | A | B | C | D | E | Interpretation |
|---|---|---|---|---|---|---|
| Nominal `correct` | Yes | Yes | No | Not assessed | No in model | Retaining shoulder clear, stem remains in hole; no full-panel success claim. |
| Nearby tool | No | No | No | Not assessed | No in model | No contact and no withdrawal. |
| Wrong upper surface | No | No | No | Not assessed | Yes | Excessive penalty overclosure, outside model domain. |
| Partial extraction | No | Yes | No | Not assessed | No in model | Withdrawn material is not equivalent to released retention. |
| Panel moves, clip captured | No | Yes | No | Not assessed | No in model | Panel moves about 3.856 mm, clip only 0.295 mm. |
| Excessive panel load | Yes | No | Yes | Not assessed | Yes | Complete stem withdrawal with about 2.370 mm modeled panel plastic set. |
| Yielding legs | Yes | Yes | No | Not assessed | Yes | Retention clears with about 0.346 mm irreversible leg set. |
| No initial retention | Yes at end | Yes | No | Not assessed | Yes | Already unretained starting interface is not a successful release. |

These are distinct observations, not interchangeable completion thresholds. No contact code, geometry, force law or existing result was changed. There are **zero new contact experiments** in this correction revision.
