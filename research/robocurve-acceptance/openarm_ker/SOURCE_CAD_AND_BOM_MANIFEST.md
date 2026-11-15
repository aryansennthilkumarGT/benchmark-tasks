# Official source, CAD and BOM manifest

**Actual CAD obtained and used.** Shell/Git access was verified on the research branch at parent `36ab82708e1ca9706c0462db75220290de0ded96`. The official [hardware release2.0.0](https://github.com/enactic/openarm_hardware/releases/tag/2.0.0) was downloaded, its published checksum matched, and both KER STEP files imported on CPU. No geometry was reconstructed from a photograph.

## Single CAD snapshot

- Asset: [openarm-hardware-2.0.0.tar.gz](https://github.com/enactic/openarm_hardware/releases/download/2.0.0/openarm-hardware-2.0.0.tar.gz).
- Actual archive size: **163,124,751 bytes**;74 archive members.
- SHA-256: **247ce0141a9be6ebbb5a6c206cf0557574929ea0b80e20dddbff7c0c0919db75**, equal to the publisher's `.sha256` asset and release-page digest.
- Tag commit: `08fd58364cb96b4841c601d87f5aba5557565de7`.
- Raw archive and CAD stay outside Git. Scripts, extracted numeric metadata, source hashes and a derived visualization are committed. Publisher attribution/license is preserved in [LICENSE.openarm_hardware.txt](LICENSE.openarm_hardware.txt).

| KER file in that same archive | Bytes | SHA-256 |
|---|---:|---|
| OpenArm KER.STEP |26,645,206|`f9fdb476bb460ca396511bdde9d528ea7bc9d15a145963cfa0e4816240dcd17a`|
| OpenArm KER JIG BASE.STEP |3,687,501|`7912bc827c20e01e45b97ee4eaa68ad9e2399aac88b28baf002d254af77ee3b1`|
| OpenArm KER BOM.xlsx |15,803|`49082ad2eb5ef2ad6fdc0767238c87f0c38e4a8e49cd8699cd5f7475d0703edc`|
| KER README.pdf |61,267|`d39bcba0634634694378d72d3a94be8f74cd38d10289d320ec4bf06b072a8924`|

[Archive provenance](evidence/archive-provenance.json), [all members](evidence/archive-members.json), [individual extracted-file hashes](evidence/extracted-manifest.json). The archive also contains electronics/cable files; those were inventoried, not used as mechanical geometry or mixed across their sub-revisions.

## What the STEP files actually contain

Both declare **millimetres**, radians and steradians. XCAF import yields:

| File | Free roots | Leaf solid occurrences | Native-coordinate bounds, mm |
|---|---:|---:|---|
| KER assembly |1|**509**|X−130.000002…130.000002; Y−395.200000…130; Z−273.993152…20.000000|
| Jig base |1|**1**|X−121.75…121.750000; Y−120…40.000000; Z−39…51.000000|

The assembly is not one rigid robot link:509 includes fasteners and repeated encoder/module parts. The source jig is a single detailed solid with **797 faces**, not a primitive replacement. Both native root bounds exactly match the union of imported occurrence bounds in this run. All occurrence paths, definition names, local and accumulated4×4 placements, bounds and geometric volumes are retained in [cad_inventory.json.gz](results/cad_inventory.json.gz).

**XCAF placements are static assembly placements, not joint definitions.** Some parts have identity placement matrices while their BRep geometry already contains offset coordinates. No identity matrix was interpreted as a joint axis or a weld. The STEP files do not provide the KER articulation/limit/ready-state definition needed for a validated manipulation path.

## BOM and fidelity findings

The actual workbook was read, preserving Excel row coordinates in [KER_BOM_ROWS.json](evidence/KER_BOM_ROWS.json). Examples: PA12S-HP nylon/MJF custom frame and base parts; A7075 encoder housing/horn and pipe clamps; SmallRig15mm carbon-fibre rods; Misumi bearings and screw families. This does **not** assign PA12 or a modulus to the jig: no jig material/elastic curve was established from that workbook.

The workflow's M2×12mm jig-fastening screws are not listed among the assembly workbook's M2-8/M2-10/M2-15 rows. That may be separate jig hardware, not proof of a revision conflict. Do not substitute one length or infer the drive form/torque. The jig has real candidate clearance/counterbore geometry, detailed in the interface report.

The bundled KER README explicitly says commercial components are represented by **simplified models**, with possible omitted detail/generic names, and directs exact purchased-component specifications to the BOM/manufacturers. Custom jig datums are mechanically useful BRep geometry; simplified screw visuals do not establish a real driver/socket fit. CAD volumes are not calibrated mass/CoM/inertia.

## Documentation and version binding

The user-pinned [calibration workflow](https://github.com/enactic/openarm/blob/e15e09e056098348d6f437389bbf48179caa82b6/website/docs/hardware/openarm-ker/calibration-workflow.mdx), data-collection tutorial and KER overview were read at `e15e09e056098348d6f437389bbf48179caa82b6`. [Documentation hashes](evidence/PRIMARY_DOCS.json). The jig's P1 seats, rear lock and paired fastener sites are recognizable, but a complete registered calibration-ready articulated pose was not established. No latest-version follower meshes were combined with the release KER.

The publisher's versioned Drive folder is the source of truth; a single attempt returned proxy403 ([record](evidence/drive-v2-attempt.json)). GitHub's snapshot was sufficient to obtain real CAD. The missing ready-state/kinematic binding was also sought in official `openarm_ker` and `openarm_description` repositories ([pins/path inventory](evidence/joint-source-discovery.json)). The former supplies streaming/mapping software; the latter describes follower OpenArm1.0/2.0/Cell. Their inspected contents did not supply a version-matched KER assembly constraint/ready-pose definition. A scaled follower URDF is not a legitimate substitute.
