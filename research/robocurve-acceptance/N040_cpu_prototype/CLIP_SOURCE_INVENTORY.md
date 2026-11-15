# Clip source inventory — uploaded evidence checkpoint

`VERIFIED` identifies what was actually read in the supplied catalog or directly visible in its illustration; it is explicitly scoped as a **supplier claim/depiction**, not measured OEM geometry. `IMAGE-ESTIMATED` would denote a disclosed metric estimate; **none were made**. `UNKNOWN` remains the status for hidden geometry, installed interfaces and model assumptions.

## Source chain

| Source | Inspection status | What it supports |
|---|---|---|
| D1 — Disco Automotive Hyundai catalog, original URL https://discoautomotive.com/wp-content/uploads/2025/03/Section-22-2-Hyundai.pdf | **Uploaded original-format supplier PDF independently inspected**, page 7 / row12612PK. SHA-256 `69422e4ae4f6310576ec40f88a7358c57af0c7c2b92feb558ab394946fe98651`. No new outbound attempt. | Nominal supplier dimensions, material/part cross-reference and visible topology. Aftermarket equivalent, not original Hyundai dimensional CAD. Byte identity with the blocked URL was not independently checked. |
| Uploaded `N040_external_source_handoff.md` | Independently read as **external evidence report**, not extra user instructions | Source leads and externally inspected SC280/retailer/photo reports. Its suggestion to request a catalog upload was not reissued; the user already supplied it. |
| Kia SC280, https://static.nhtsa.gov/odi/rcl/2023/RCRIT-23V610-6691.pdf | Handoff read; primary retrieval returned proxy403; bounded GitHub mirror search found no relevant bulletin | Externally attested Sorento service reuse/damage policy and part identity; no independent primary-bulletin inspection claimed. See [SC280 scope](SC280_SCOPE_AND_REUSE.md). |
| Shop-Supplies FR12612 / HyundaiPartsDeal supersession and 2013 catalog | Previously blocked; **not retried** | External equivalence/supersession/donor leads only. Do not infer installed Elantra fitment from the new supplier row. |
| Exist.ua / eBay genuine-parts photo leads in handoff | Not fetched or independently inspected | External visual leads only; no dimensions or donor fitment inferred from a reported bag label. |
| Prior pinned CHARM workshop reproduction | Previously read source retained | Elantra trim access, handle cage and plugs; replace damaged clips. Attributed reproduction, not OEM geometry or force data. |

[New source inspection manifest](evidence/uploaded-catalog-inspection/SOURCE_INSPECTION.json) records attachment IDs/hashes, original URL, PDF metadata, inspected page, observations and rendering commands. Full catalog and rendered images stay in the local workspace; they are not republished in this public branch. Facts and provenance are committed. Earlier failed retrieval records remain historical; they no longer describe the uploaded catalog as uninspected.

## Identity, material and visible topology

| Field | New status | Remaining limit |
|---|---|---|
| Disco12612PK ↔ Hyundai82315-2P000 | VERIFIED catalog cross-reference | Commercial equivalence, not identical OEM CAD or fitment for a selected donor. |
| White nylon | VERIFIED catalog material/color label | Polymer grade, reinforcement, moisture/conditioning, modulus, yield, fracture and friction UNKNOWN. |
| 50 pieces | VERIFIED package label | Not clip mass, geometry or task count. |
| Multiple flanges / slot / taper / nose | VERIFIED depiction, including three distinguishable side profiles and a slot/window ending before the nose outline | Actual independent member count, connectivity, section and contact surfaces UNKNOWN. No image-scaled metric reconstruction. |
| 82315-38000 supersession and selected Elantra application | UNKNOWN independently | Previously supplied catalog links remain unread. |
| Nondestructive reuse | UNKNOWN for this installed Elantra operation | SC280 external evidence distinguishes reusable/damaged clips on a Sorento; no universal reuse/breakage criterion follows. |

## Every geometric value used or sought

| Feature | Value / extent | Label | Source / interpretation |
|---|---|---|---|
| Receiving-hole nominal label | 23/64 inch (9 mm) | VERIFIED — supplier label | Independently read in uploaded D1 page 7. Rounded dual-unit label, not measured diameter/tolerance; 23/64 inch =9.128125 mm by arithmetic. |
| Stem nominal length | 13 mm | VERIFIED — supplier label | Independently read in uploaded D1. No dimensioned datum/end definition or tolerance. |
| Top-head nominal diameter | 13 mm | VERIFIED — supplier label | Independently read in uploaded D1. Not stem diameter or lower-flange diameter. |
| Overall length | About 19 mm | UNKNOWN | Earlier user-attributed supplier only; the inspected D1 row does not contain this field. |
| Actual stem cross-section, leg count and slot | No values | UNKNOWN | Need slot depth/width, end condition, bridges and orthogonal views/section. |
| Upper flange count, diameters, spacing, thickness and root radii | No values | UNKNOWN | Three flange-like profiles visible in side depiction; exact 3D count/sections still unbound. The 13 mm top head does not determine other flange dimensions. |
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

Only the nominal supplier labels and visual depiction now earn the limited VERIFIED labels described above. No IMAGE-ESTIMATED metric dimensions were produced; original OEM/installed geometry is still unknown. Solver coordinates, sampling counts, numerical bounds and audit tolerances remain declared algorithm settings in the archived code, not purported physical measurements.

## Mechanical unknowns that dimensions alone cannot resolve

The real flexible/rigid partition, force–displacement curve, unload recovery, leg coupling/contact, viscoelasticity, fracture, molding history, moisture/temperature, local sheet/clip friction, flange preload, carrier tear-out and permissible consumable damage remain UNKNOWN. The now-inspected white-nylon catalog label and outer side profile cannot determine them. No hardware purchase or physical test was performed.
