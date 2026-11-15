# Actual plastic-tool and YAM access gate

**Result: BLOCKED_MISSING_AUTHENTIC_TOOL_AND_INTERFACE.** No identified commercial plastic tool has both independently inspected documentation and usable geometry here. No actual tool grasp, palm-clearance or swept-access test can legitimately be reported. The earlier invented nose is not accepted as a replacement for that input.

## Commercial tool investigation

| Lead | What was actually inspected | Disposition |
|---|---|---|
| GEARWRENCH 84090 candidate, [product-path lead](https://www.gearwrench.com/all-tools/auto-specialty/body-interior/84090-5-pc-auto-trim-removal-set), [manufacturer SKU search](https://www.gearwrench.com/search?search=84090) | Both returned proxy tunnel 403; no product page, image, material claim, SKU constituent or dimensional drawing read. | **Unverified commercial-tool lead**, not an independently documented selected tool. Do not assert its material, blade thickness or handle shape. |
| [Toolsource search](https://www.toolsource.com/search?q=gearwrench+84090) | Proxy tunnel 403 | No independent product specification. |
| [Bojo manufacturer](https://bojotools.com/) | Proxy tunnel 403; no exact SKU document recovered | Too generic to bind a tool. |
| [iFixit opening-tool comparison lead](https://www.ifixit.com/products/ifixit-opening-tool) | Proxy tunnel 403 | No inspected geometry; not selected as an automotive trim-removal substitute. |
| GitHub mirrors/community mentions | Search extracts read; accessible Vhedia head-unit README only mentions supplied trim tools | No documented plastic material, SKU, scale, fork profile or grippable surface. Not accepted as geometry evidence. |
| Existing workshop reproduction, p887 | Previously read plastic panel-removal-tool instruction in general interior-trim context | Supports ordinary tool type only. Does not identify a commercial tool or establish access at this exact clip/carrier. |

The exact retrieval/search provenance is under [evidence/authentic-correction](evidence/authentic-correction). Manufacturer/retailer paths above are discovery leads, not a claim that the blocked endpoints contain the required documents. The task requirement to use an actual commercially documented plastic tool is **still unmet**. No geometry has been fabricated to make it pass.

## Authentic fit and load path

Every tool geometric input is **UNKNOWN**: full body, blade/nose thickness, taper, fork gap, prong width/depth, offsets, root radii, handle cross-section, length, flat grippable patch and strength. The clip's lower/upper flange spacing, panel/carrier stack and adjacent free channel are also UNKNOWN. Therefore neither these alternatives nor a choice between them is verified:

1. A fork passes around a real neck/stem and bears against a specific accessible flange/head. Its slot must clear the neck but still overlap the intended bearing surface; prongs must clear the receiving panel and carrier without loading a fragile unintended feature.
2. A wedge lifts an actual panel edge near the carrier, transferring load through the real mounting pocket. This needs the actual panel bending response, fulcrum and head/pocket retention; panel pull-through or tearing must remain possible failure modes.

There is no source-bound numeric clearance for either path. The archived 0.6–0.8 mm planar nose, fixed pivot and collapsed contact resultant have no verified commercial-tool analogue. A 13 mm reported top-head diameter cannot supply the fork gap, accessible underside or mounting stack. Tool proximity or apparent head overlap cannot establish an acquired load path.

## YAM geometry: known source model versus missing task inputs

The existing [YAM reference](../preflight/assets/YAM_REFERENCE.json.gz) remains the source of robot geometry. Pin `0059d02a1a91bc6834c1d0846022891df0c78730`, asset-source commit `120c3c81400171174604e503943f8d1ebc891058`, includes 315 hulls per arm, with 44 gripper/palm hulls and 45/47 finger hulls. These are **VERIFIED pinned source-model counts**, not an empirical clearance result.

The source model's **93.9 mm nominal aperture** is VERIFIED as a model/configuration value, not proof that any particular tool fits or can be held. The existing gripper-local hull extents are approximately 102×65×74 mm; these are VERIFIED calculated bounding extents of the pinned geometry, **not** a rectangular collision-free zone, finger-contact depth or measured real hardware tolerance. Actual convex hulls and joint poses must be used. These robot dimensions do not infer any missing tool dimension.

[TOOL_ACCESS_GATE.json](evidence/authentic-correction/TOOL_ACCESS_GATE.json) records the pinned robot information and null task/tool inputs. Missing inputs prevent the following checks:

| Check requested | Required authentic inputs | Current outcome |
|---|---|---|
| Handle fits jaws and lies on usable contact patches | Real handle surface/cross-section, jaw opening, selected contact pair | Not assessed |
| Grip can resist slipping/rolling and transmit moment | Grip transform, surface friction, normal-force limits, handle strength, actual contact wrench | Not assessed |
| Nose/fork reaches intended clip contact without palm collision | Full tool mesh, head/carrier/panel section, gripper-to-tool transform, work joint pose | Not assessed |
| Acquisition and pry sweep remain clear | Tool/robot paths, receiving structure, panel motion/support, both arms and surroundings | Not assessed |
| Bimanual safe panel separation | Full panel/clip/upper-edge/handle/plug geometry, harness slack and support | Not assessed |

Use [access_core.py](../preflight/access_core.py) and [N040_ACCESS_TEST.py](../preflight/N040_ACCESS_TEST.py) when actual inputs exist. Keep intended finger/tool contacts explicit; they must not mask palm/wrist collision. No proxy wedge, invented grasp transform, READY-pose clearance or necessary reach radius has been substituted. The existing full-size result remains `BLOCKED_MISSING_INPUTS`, not a proved collision or reachability pass.

## Force is not tool capability

Archived nominal outputs are 46.126 N sampled nose reaction, 453.997 N·mm peak moment about the **assumed** pivot, and 4.540 N ideal force at the **assumed** 100 mm handle. These maxima need not occur at the same increment. The lever geometry, tool elasticity, grip site and load direction are not source-bound. These are neither authentic Hyundai extraction loads nor YAM force/torque requirements.

A gripper normal-force configuration cannot be compared directly with the clip reaction to certify a grasp; normal force is not available tangential force, and frictional moment, payload, wrist/arm effort and leverage matter. No two-finger ratings were added together and no nominal wrist rating was used as a transferable tool-wrench guarantee. A real tool could flex, slip, roll, fail or collide before producing the modeled nose motion. Without authentic geometry and a measured/source-supported wrench, there is no valid YAM capability conclusion.
