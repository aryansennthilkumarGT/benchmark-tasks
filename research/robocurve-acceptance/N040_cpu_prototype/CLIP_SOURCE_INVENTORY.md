# Clip source and dimensional inventory

**Status: PARKED pending inspectable authentic geometry.** `VERIFIED` means independently read/inspected supporting source or an actual authorized measurement; `IMAGE-ESTIMATED` means a disclosed estimate from an image actually inspected; `UNKNOWN` includes uninspected external reports and model assumptions. An external report is retained as a useful lead, without promoting it to independently verified geometry. No image-estimated dimensions were produced in this revision.

## New source chain and provenance

| ID | Exact source | Intended evidence | Retrieval/result |
|---|---|---|---|
| D1 | https://discoautomotive.com/wp-content/uploads/2025/03/Section-22-2-Hyundai.pdf | Printed/PDF p7, row 12612PK: equivalent 82315-2P000, stated dimensions/material, illustrated shape | Proxy tunnel 403. **Externally located and user-described; not independently inspected.** No PDF bytes, page rendering or measurements obtained. |
| D2 | https://www.shop-supplies.com/proddetail.php?prod=FR12612 | Independent supplier listing / equivalence cross-check | Proxy tunnel 403. Not read. No purported confirming quotation. |
| D3 | https://www.hyundaipartsdeal.com/genuine/hyundai-fastener-dr-trim~82315-2p000.html | Part identity / supersession | Proxy tunnel 403. This is the new user-supplied exact URL, distinct from the guessed part URL recorded in the previous sprint. |
| D4 | https://www.hyundaipartsdeal.com/parts-list/2013-hyundai-elantra-us_alabama_made/trim/front_door_trim.html | Original 2013 catalog context / donor applicability | Proxy tunnel 403. No specific left-front donor/VIN/options compatibility independently established. |
| W1/W2 | Previously read [workshop extracts](evidence/workshop-extracts.json), pinned `Kmberry1989/Elantra@0f7b23efdcf6ecc48919fb781be7e95a1b8f0f06`, pages 863/887 | Front-door trim steps; general plastic trim-tool instruction; replace damaged clips | Preserved attributed workshop reproduction, not authenticated Hyundai OEM CAD or force data. Page 887 is general interior/scuff/pillar context. No metric reconstruction. |

New [retrieval records](evidence/authentic-correction/retrievals.json) and [follow-up records](evidence/authentic-correction/followup-retrievals.json) preserve exact URLs, UTC attempts, errors, and hashes where content was received. The user request was supplied as `sediment://file_0000000092c481f6abd17f91f47fc09f`; that attribution is not a downloaded supplier document. No newly supplied manufacturer/supplier document was independently inspected.

### Legitimate mirror investigation

[Search records](evidence/authentic-correction/mirror-tool-geometry-searches.json) include exact PDF filename, `12612PK`, `FR12612` and Disco Automotive repository/issue searches. No usable catalog mirror, part illustration or authenticated photograph was recovered. Archive.org CDX discovery also returned tunnel 403. GitHub search cannot exhaust all code/documents without authenticated code search; negative results are bounded, not proof of absence. We did not attempt to bypass network restrictions.

Tool searches returned unrelated numeric issue IDs for `84090`, generic community trim-tool mentions and marketing/catalog keyword repositories, none an authoritative calibrated tool drawing. The accessible `phil-gg/vhedia-head-unit` README mentions supplied generic trim tools but provides no identified SKU, material or metric shape. The Elantra/door/CAD README search returned a book-title repository, not usable geometry. These are **search exclusions**, not sources supporting clip or tool dimensions.

## Identity, material and installation facts

| Field | External finding / value | Label | Limit |
|---|---|---|---|
| Commercial equivalent | Disco 12612PK ↔ Hyundai 82315-2P000 | UNKNOWN | Reported by user from D1; not independently cross-read in D1/D2. Aftermarket equivalence would not establish identical OEM CAD. |
| Supersession | 82315-38000 → 82315-2P000 | UNKNOWN | User-provided catalog lead, D3/D4 inaccessible. |
| Material/color | White nylon | UNKNOWN | User report from D1. Does not establish polymer grade, conditioning, reinforcement, E, yield or friction. |
| Topology | Slotted/tapered stem; multiple upper flanges | UNKNOWN | Externally reported appearance. No inspected view/section; no leg count or hidden shape inferred. |
| Donor fitment / exact mounted carrier | Proposed 2013 U.S. Elantra front door | UNKNOWN | VIN/variant/side and installed carrier stack remain unbound. |
| Normal damage/reuse | No part-specific data | UNKNOWN | W1/W2 say replace damaged clips, not how often this part breaks or whether nondestructive reuse is expected. |

## Every geometric value used or sought

| Feature | Value / extent | Label | Source / interpretation |
|---|---|---|---|
| Receiving-hole nominal diameter | 9 mm | UNKNOWN | User report from D1 and earlier supplier. Useful nominal lead, not an independently verified tolerance. |
| Stem nominal length | 13 mm | UNKNOWN | User report from D1; datum/end definition not inspected. |
| Top-head nominal diameter | 13 mm | UNKNOWN | User report from D1. Not a stem diameter or lower-flange diameter. |
| Overall length | About 19 mm | UNKNOWN | Earlier user-attributed supplier only; the new D1 report did not independently confirm this field. |
| Actual stem cross-section, leg count and slot | No values | UNKNOWN | Need slot depth/width, end condition, bridges and orthogonal views/section. |
| Upper flange count, diameters, spacing, thickness and root radii | No values | UNKNOWN | Multiple upper flanges reported; 13 mm top head does not determine the others. |
| Actual retaining maximum diameter, slope and axial edges | No values | UNKNOWN | Essential to installed overlap and extraction force. |
| Actual carrier slot/pocket, neck capture and sheet details | No values | UNKNOWN | Need installed section, seat lip/chamfer/burr/embossment and contact directions. |
| Coupon sheet thickness / root height | 0.8 / 6 mm | UNKNOWN | Old model assumptions. **19−13 is not a validated stack dimension.** |
| Coupon shoulder start / peak axial coordinate | 6.8 / 7.2 mm | UNKNOWN | Invented single-shoulder profile, not image estimates. |
| Coupon neck / peak / tip radius | 2.7 / 5.3 / 2.4 mm | UNKNOWN | Invented profile, not supplier dimensions. |
| Coupon effective flexure length / width / thickness | 7 / 4 / 1 mm | UNKNOWN | One-mode beam hypotheses, not real leg dimensions. |
| Coupon head-carrier slack | 0.2 mm | UNKNOWN | Invented mounting coupling. |
| Coupon panel thickness / contact patch | 2 mm / x∈[−9,4] mm | UNKNOWN | Local invented panel section, not measured door trim. |
| Coupon nose coordinates | x=8…10, z=0.8…0.6 mm | UNKNOWN | Invented planar surface, not an actual plastic tool. |
| Coupon tool pivot / ideal handle | (−10,−1) mm / 100 mm | UNKNOWN | Model boundary geometry; no source-bound grasp or fulcrum. |
| Actual fork gap/prong thickness/offset/handle/grip area | No values | UNKNOWN | No actual tool drawing or photograph independently inspected. |
| Full panel/door dimensions; clip-site coordinates | No values | UNKNOWN | Workshop diagrams uncalibrated; no scale or actual-size surfaces inferred. |
| Handle cage / plug / harness / support dimensions | No values | UNKNOWN | Illustrated/mentioned interfaces are not metric inputs. |

No real clip geometry currently earns the independently `VERIFIED` or `IMAGE-ESTIMATED` label. Solver coordinates, sampling counts, numerical bounds and audit tolerances remain declared algorithm settings in the archived code, not purported physical measurements.

## Mechanical unknowns that dimensions alone cannot resolve

The real flexible/rigid partition, force–displacement curve, unload recovery, leg coupling/contact, viscoelasticity, fracture, molding history, moisture/temperature, local sheet/clip friction, flange preload, carrier tear-out and permissible consumable damage remain UNKNOWN. White nylon and an outer side profile cannot determine them. No hardware purchase or physical test was performed.
