# Data centre and robot electrical discovery

The strongest final addition is **CELLO rotary drum-brake tuning**, documented by the real teleoperation-hardware designer with exact five-part contact geometry. It is **BUILD-READY FOR CPU PREFLIGHT only**,84/100, pending a genuine loose-brake load baseline, a useful hold-versus-drag window and complete YAM support/driver checks. Independent criticism found no exact duplicate. The final section gives its full readable dossier. The **ODRI optical foot contact switch** is a costlier independent reserve,77/100.

The Opentrons Heater-Shaker GEN1 has clear installation instructions and an authentic captive-anchor mechanism. Independent review found substantive overlap with accepted#1283, which also tightens a screw-driven jaw beneath an edge. Keep it as a reserve rather than filling the final15 with a weak variant.

The machine-readable `datacenter.json` contains the20-operation initial ledger,4 later expansions and9 complete dossiers, including all source pins/hashes, inventories, scoring proposals, negative controls, semantic comparisons and limitations. The source manifest and actual files live under `agents/datacenter/`.

## Initial screen

| ID | Real operation | Result |
|---|---|---|
| DC01 | [Capture an OpenFlexure stage actuator preload band](https://raw.githubusercontent.com/rwb27/openflexure_microscope/0cedf45238bb1cf8185f4ad92d366eb36f44efc3/docs/1_actuator_assembly.md) | HIGH-RISK RESERVE — Excellent genuine preload mechanism; motorized microscope is not independently established as robot-building under official AI domain. |
| DC02 | [Remove a PiCamera v2 lens without twisting its ribbon-connected camera](https://raw.githubusercontent.com/rwb27/openflexure_microscope/0cedf45238bb1cf8185f4ad92d366eb36f44efc3/docs/2b_high_resolution_optics_module.md) | HIGH-RISK RESERVE — Real procedure with CAD;14mm×2mm tool acquisition and importance are decisive risks. |
| DC03 | [Replace a Flex pipette nozzle seal using OEM roll-on tool](https://raw.githubusercontent.com/Opentrons/opentrons/95ac66dea217cd169fbf98ac4573844bd65d01b3/docs/flex/docs/maintenance/cleaning.md) | REJECT — Merged#1576 preserves same ring-over-shaft/seated-seal skill; different roll-on tool insufficient strong novelty. Exact OEM tool dimensions missing too. |
| DC04 | [Fit the GELLO trigger return spring](https://raw.githubusercontent.com/wuphilipp/gello_mechanical/8ea3f2e661b55d4a128683b09227f8e771cd729e/README.md) | PROMISING BUT SOURCE-GATED — Unambiguous robotics-data-collection importance; spring endpoints, exact spring specification and assembly step not independently read. |
| DC05 | [Assemble OpenMANIPULATOR-X crank-link gripper drive](https://raw.githubusercontent.com/robotis-git/emanual/0807b1b5f7472bbbbb2c9751f1d3406678e86d37/docs/en/platform/openmanipulator_x/assembly.md) | PROMISING BUT SOURCE-GATED — Distinct linkage from rack/pinion#1898, but actual linkage pivots are collapsed out of URDF; do not invent them from mimic sliders. |
| DC06 | [Assemble the DYNAMIXEL430 hollow idler around a joint cable](https://raw.githubusercontent.com/robotis-git/emanual/0807b1b5f7472bbbbb2c9751f1d3406678e86d37/_includes/en/dxl/assembly/430_horn_assembly.md) | PROMISING BUT SOURCE-GATED — Authentic robot assembly. Assembly/reverse are ONE family. Need exact tiny interaction/support sequence; schematic geometry approximate is allowed but cannot invent release causality. |
| DC07 | [Seat a thrust washer and index a DYNAMIXEL output horn](https://raw.githubusercontent.com/robotis-git/emanual/0807b1b5f7472bbbbb2c9751f1d3406678e86d37/_includes/en/dxl/assembly/430_horn_assembly.md) | REJECT — Same keyed-hub/indexed mating family as priorN043; mostly object swap, not a fresh physical skill. |
| DC08 | [Fit a rack square-hole cage nut](https://github.com/robocurve/benchmark-tasks/pull/2274) | REJECT — Earlier pending#2274 and#946 already claim operation; no build. |
| DC09 | [Extract a QSFP28 transceiver by its bail](https://github.com/robocurve/benchmark-tasks/pull/2143) | REJECT — Earlier#2143 and#640 make semantic/ownership risk decisive. |
| DC10 | [Install Flex waste chute onto deck adapter](https://raw.githubusercontent.com/Opentrons/opentrons/95ac66dea217cd169fbf98ac4573844bd65d01b3/docs/flex/docs/system-description/robot.md) | PROMISING BUT SOURCE-GATED — Real robot equipping, but only attachment relationship is documented in retrieved manual; tilt/hooks/latch not verified. Do not invent them. |
| DC11 | [Seat OT2 removable trash hopper on its dedicated support](https://raw.githubusercontent.com/Opentrons/opentrons/95ac66dea217cd169fbf98ac4573844bd65d01b3/docs/ot-2/docs/installation/unboxing.md) | REJECT — Manual step9 says only put in place. Image shows nested hopper/support; no mechanism evidence for a richer tilt/lock task. Would be generic placement. |
| DC12 | [Mount a Flex96-channel pipette across both carriages](https://raw.githubusercontent.com/Opentrons/opentrons/95ac66dea217cd169fbf98ac4573844bd65d01b3/docs/flex/docs/installation/instruments.md) | HIGH-RISK RESERVE — Direct robot construction but heavy instrument, mounting dimensions and carriage-disconnection mechanics unverified; ordinary captive-fastener skill risks#1054 overlap. |
| DC13 | [Hand-tap GELLO printed joint mounting threads](https://raw.githubusercontent.com/wuphilipp/gello_mechanical/8ea3f2e661b55d4a128683b09227f8e771cd729e/franka_fr3/README.md) | REJECT — True robot assembly but generic hand tapping already#936; chip/fracture simulation increases cost. |
| DC14 | [Connect an OpenFlexure camera ribbon in its ZIF socket](https://raw.githubusercontent.com/rwb27/openflexure_microscope/0cedf45238bb1cf8185f4ad92d366eb36f44efc3/docs/4_clips_and_wiring.md) | HIGH-RISK RESERVE — Authentic electrical preparation, but tiny latch grasp and precise mechanism dimensions unavailable; microscope importance unresolved. |
| DC15 | [Release Flex gantry transport locks for commissioning](https://raw.githubusercontent.com/Opentrons/opentrons/95ac66dea217cd169fbf98ac4573844bd65d01b3/docs/flex/docs/installation/unboxing.md) | REJECT — Real commissioning, but generic screw/bracket removal and robot-wide access; no distinct central ability beyond existing fastening. |
| DC16 | [Replace Flex Stacker side window and access panel](https://raw.githubusercontent.com/Opentrons/opentrons/95ac66dea217cd169fbf98ac4573844bd65d01b3/docs/stacker/docs/installation.md) | REJECT — Large sheet panel held while screws inserted; near existing panel-fastening families. Stacker itself13.6kg exceeds stockYAM manipulation. |
| DC17 | [Solder the OpenFlexure illumination LED series lead](https://raw.githubusercontent.com/rwb27/openflexure_microscope/0cedf45238bb1cf8185f4ad92d366eb36f44efc3/docs/3_illumination.md) | REJECT — Essential solder metallurgy adds cost; robotic importance unresolved, common electrical joining lacks distinctive final skill. |
| DC18 | [Press an AC127-050-A tube lens into the optics housing](https://raw.githubusercontent.com/rwb27/openflexure_microscope/0cedf45238bb1cf8185f4ad92d366eb36f44efc3/docs/2b_high_resolution_optics_module.md) | REJECT — Genuine12.7mm optical interference fit, but little novelty over square press-fit placement and importance remains unresolved. |
| DC19 | [Assemble a REV mecanum-wheel angled roller](https://docs.revrobotics.com/duo-build/mecanum-drivetrain-kit) | PROMISING BUT SOURCE-GATED — No exact assembled-wheel manual read, so proposed workflow unverified. Fresh semantic search found no mecanum/omni-wheel/roller PR; cannot promote on title alone. |
| DC20 | [Anchor an Opentrons Heater-Shaker GEN1 in an OT2 deck slot](https://raw.githubusercontent.com/Opentrons/opentrons/95ac66dea217cd169fbf98ac4573844bd65d01b3/docs/heater-shaker/docs/installation-ot2.md) | HIGH-RISK RESERVE — Fully sourced and finite-cost geometry preflight possible; accepted#1283 screw-driven edge clamp creates substantive novelty risk. No claim of build-ready qualification. |

## ODRI optical foot: complete reserve dossier

A robot builder assembles the Foot Contact Switch v1 used on ODRI's quadruped. Twelve silicone tube pieces centre a floating aperture between an LED and receiver. External contact displaces the aperture, changing received light. The guided steel pin prevents rotation. The author explicitly reports up to2mm foot deflection,270degree directional sensitivity and a3V-to0V analogue output. This is construction of a documented robot sensor, without an employment-count argument.

Use the original revision pinned at `66af1522b4fba0ec4a1d7790e66f5e4652208d30`, not a later Solo foot. The complete author README,1:1 drawing, component photographs,3 STEP files,3 STL files and full SolidWorks assembly archive are preserved with SHA256 hashes. Actual STL bounds are:

| Part | Source dimensions / mass |
|---|---|
| Foot |27mm diameter ×16.5mm; Accura Extreme Gray SLA;3.4g |
| Lower-leg base |181 ×27 ×20mm; FDM/SLS;18g |
| Fork |62.5 ×16.78 ×13.5mm; FDM/SLS;5g |
| Elastic elements |12 silicone pieces;6mm OD,4mm ID,3mm long; six per side |
| Pin |Steel;1.5 ×12mm |
| Electronics |Two10mm PCBs, prewired for this mechanical task |
| Closure |Real M2.5×6 screws with source-specified inserts; no glue substitutes |

The tread/pin foot and prewired boards begin as authentic prior subassemblies. The twelve precut annuli and fork begin separate. A real support holds the long leg without holding the foot in its final position. Ordinary electronics tweezers are a plausible aid, but no source says they were used; this is a disclosed implementation choice. The parts must remain source-sized. Their printed pockets, aperture and pin channel come from actual geometry. The retrieved author material provides a component overview and CAD rather than a numbered twelve-piece assembly order; that order still needs to be checked against the assembly.

**Instruction:** Assemble all12 silicone centring elements and the optical boards around the foot. Close and secure the fork with the pin in its guide, then leave the foot centred and able to move and return after contact.

One arm supports the leg and retains the first bank while the other places and releases the second bank. The tool shaft, first bank, foot, fork, palm and second arm must all fit inside a27mm mechanism. Stock fingertips are much wider than an annulus. A full tweezer/contact sequence is unverified. No IK, collision or physical-force test was executed.

Proposed partial credit is0.25 for a genuinely retained first bank,0.5 for both banks and correctly oriented boards,0.75 for a retained fork pending function, and1.0 only for intact, hands-free mechanical and optical function. Remove any partial tier that the real hardware cannot retain without help. Completion requires all12 elements, guided pin, reversible foot travel and passive return, plus an actual reversible optical voltage/LED response. Use photographs, a dial indicator or scaled macro video, a spring scale and the real low-voltage circuit. A return tolerance such as0.2mm is a benchmark proposal, not an OEM specification. Select and disclose force levels from the actual author response curve; this report does not invent a measured force threshold.

A jammed foot missing annuli fails travel and inventory. A foot held at neutral fails release. Adhesive or rigid shims fail the genuine compliant mechanism. Wrong board orientation or blocked aperture fails actual optical response. An omitted pin or pinched wire fails inspection. Reset by removing real fork screws, recovering and inspecting all12 annuli, then returning the intact subassemblies to their source state. Replace permanently set or cut silicone pieces.

The essential physics is distributed compliant contact and passive recentering. A disclosed deformable-ring or unilateral compliant-contact approximation can be tested against the author curve, but fixed annuli, a reset-to-centre script or a proximity-triggered green light would erase the task. Optics may be simplified through real aperture/light overlap with disclosed parameters.

Current official comparison reads:

- **#2212**, open, head `0e50dbc85fedc7624a13a7fff033c161692f18c3`: keyed magnet carrier, fixed-gap bracket, retention catch and field-test button. Actual `State.advance`, task.json and README were read. It mounts fixed-gap encoder parts; it does not assemble distributed compliant supports around a moving aperture. Its implementation weaknesses are not used to dismiss its legitimate scope.
- **#2014**, merged Nov16: Franka guiding holds an existing6mm enabling button within its mid-band while moving and teaching the robot. Actual `Trial.step`, `Trial.moment`, task.json and README were read. Using an existing compliant button differs from assembling a new switch and testing passive final function.
- **#1576**, merged: stretch an elastic seal over a shaft into one groove. Its actual ring/stretch/twist scorer was read. The ODRI tubes act as separate springs around a floating aperture rather than one sealing ring.

The retired battery cross-key task is not being revived. This foot has independently published robot provenance, exact geometry, twelve dimensioned elastic elements and measured optical response. It has no battery, invented pack fixture or transverse preload key.

The strongest rejection is that twelve tiny parts inside27mm need an unavailable helper, and a rigid approximation would reduce the task to peg counting. That objection remains unresolved. The cheapest falsification is one deepest pocket placement/release using a normal tweezer envelope, the actual foot/fork and all315 YAM hulls per arm, followed by a complete bank-retention/support sequence. Do this before a full material model. **Effort: high.**

## Other deep investigations

| Candidate | Evidence and decisive result |
|---|---|
| Heater-Shaker GEN1 | Full OT2 installation instructions,1.34kg body specifications, actual lateral-anchor drawing, moduleV1 JSON and historical deckRevA2 DXF. Captive Torx anchors are real. Source envelope156.25×91.75 differs from bare152×90; use conservative clearance and do not claim matched current deck revision. Accepted#1283 is the substantive semantic objection. |
| DYNAMIXEL430 idler | Full OEM text and both diagrams viewed. Bearing/idler/cap around a routed cable is real robot assembly. Reverse button and side hooks require a detached rear case. Assembly and reverse are one family. Tiny multiple-contact support remains unresolved. |
| OpenMANIPULATOR-X crank linkage | Official BOM and current palm geometry verified. Link rods and bushes differ mechanically from#1898's rack/pinion, but actual assembly pages are vendor403. Operational mimic-slider URDF is not genuine linkage-assembly geometry. |
| GELLO trigger spring | Direct teleoperation/data-collection importance and actual handle/trigger STLs. Exact spring row, endpoints and assembly step remain behind the blocked official Google document. Do not invent preload or mix FR3 and original parts. |
| OpenFlexure preload band | Exceptionally clear author instructions,30×2mm Viton and complete tool/body CAD. The fork has flexible links. Independent importance objection remains: an automated microscope is not thereby proven robot-building. |
| PiCamera lens removal | Real counterholding jig and directional tool CAD. Lens tool is14mm diameter and2mm thick, presenting a major stock-hand acquisition problem; microscope importance remains unresolved. |
| Flex pipette O-ring | Full OEM roll-on instructions, but accepted#1576 preserves the same seal-over-shaft/groove outcome. Reject rather than relabel a known skill. |

## Expansion and evidence limits

The REV mecanum vendor pages and GitBook were403. Actual MantisRover designer wheel STEP/STL files were found, but its README only identifies CAD files. Two other assembly repositories contained isolated SLDASM files, and Wisty supplied control code. No assembly instructions were claimed from these sources. Broad current official mecanum/omni-wheel/roller searches returned no matching PR; later GitHub429 results are not negative evidence. Staged hand reaming was read in ODRI's real procedure but root had already eliminated it for material-removal cost.

No source-perfect cosmetic CAD was demanded. Unknown essential contact causality or a missing complete tool/support sequence remains material. No task implementation, YAM CPU/GPU run, paid/model run, physical trial, purchase, commit, push or submission occurred.

## Final bounded pass: CELLO rotary drum-brake tuning — DC24

**BUILD-READY FOR CPU PREFLIGHT only,84/100** (20/21/19/12/12). This is the strongest final new family from this domain. No CPU clearance or completed physical test is claimed. Kill the concept if the genuine loose-brake arm already holds or no hold/backdrive torque window exists.

The actual CELLO designer builds a GELLO leader for a Franka Panda, replacing degrading spring/band joint regularizers with passive brakes so links stay put. The brake acts in parallel with the joint, preserving encoder synchrony. The GitHub build note explicitly says: “Tune each brake by tightening both M3×25 preload screws symmetrically until the link holds its own weight with minimal drift while still driving smoothly.” This is genuine robot teleoperation hardware commissioning, not a generic service arm with an invented occupation.

Source: [CELLO build note](https://github.com/pilcsimo/cello_mechanical/blob/f4b572107fcd4c2d59bb563462e21ba39d878fa6/franka/brake%20version/README.md), pin `f4b572107fcd4c2d59bb563462e21ba39d878fa6`. The author contribution is open [GELLO hardware PR22](https://github.com/wuphilipp/gello_mechanical/pull/22); it is not claimed merged. The full linked Google assembly guide is403. That does not block the tuning-only task: start with its authentic assembled joint, using the directly retrieved tuning instruction and exact geometry. The MIT license and source files are retained and hashed.

Actual imported `Brake Axial.step` contains five solids: one PETG inner rotor, two TPU95A half-pads and two PETG outer half-shells. The rotor contact radius is12.5mm. Pad contact radii are12.6–14.6mm and thickness8mm. Shell inner/outer contact radii are14.7/24.7mm; overall nominal brake diameter49.4mm and axial thickness10.5mm. Two3.2mm clamp bores at X±19.7mm align with the symmetric screw draw. L1 bounds are39.5×37.49×119.95mm; L2 bounds45.25×82.5×24mm. These are measured STEP surfaces/bounds, not manufacturer fit tolerances. [The inspected source geometry](datacenter/cello-axial-inspection.png) and contact-axis/bounds JSON are preserved.

Use the actual axial L1–L2 joint and authentic downstream links, motors, handle and cables as its gravity load. Do not add a counterweight to make the task work. Start with both screws reproducibly loose, the source pads retained, and the downstream chain on an ordinary temporary support. The upstream link mounts through its actual interface. One YAM supports a genuine link while the other acquires an ordinary hex driver and adjusts both opposed screws; support may need to transfer before reaching the second ear. No enlarged hardware or custom YAM fingers are permitted.

**Instruction:** Support the CELLO leader arm and adjust both brake screws evenly. Leave it holding its own weight at the marked pose while it can still be moved smoothly. Park the driver and release it.

The screw draw must physically compress the TPU pads against the inner drum and create circumferential friction. Disclosed thread coupling and a friction/compliant-contact model are reasonable approximations. A screw-setting-to-hold lookup or a hidden stiff joint would erase the mechanism. Exact friction, printing properties, chain mass/COM and screw torque remain unmeasured.

Proposed physical tiers are0.25 for a genuine static hold after release,0.5 for holds at two poses, and1.0 only if the same unchanged setting also permits a bounded bidirectional movement test and still holds afterwards. Measure angular drift with a protractor/video and breakaway/running torque with a spring scale at an actual measured lever point, subtracting gravity's contribution. Initial possibilities such as≤2degree drift in5s, a60degree sweep and≤2N at a real100mm lever point are benchmark proposals, not author specifications. They must be selected from the actual source arm and a demonstrated nonempty torque window. A photo/feeler check can verify symmetric ear gaps; equal screw-turn counts alone do not establish correct compression.

Seizing the brake fails the movement test. One-sided tightening fails pad/seating and smoothness checks. Continued hand support fails release. Changing screws between tests fails the same-setting rule. Adding a load/counterweight or removing source arm parts fails inventory. Crucially, the loose-brake start must actually sag: if servo gear stiction already holds the arm, doing nothing must not earn a full score.

Reset by supporting the chain, backing off both screws to the specified gap, verifying the initial hold test fails, returning the genuine chain to its marked support and inspecting pads/threads. No destructive step is part of normal reset.

Actual current official comparisons were read:

- **#813**, closed final: adjust/lock tabs tune V-wheel carriage lateral rigidity and rolling drag, followed by a1N side test and100mm sweep. Its real claimed skill remains relevant despite rejected implementation. CELLO adjusts two real split-drum screws for static rotary friction and backdrivability of an actual teleoperation link; no guide play or rolling carriage. Shared preload reasoning alone is insufficient duplication.
- **#2203**, open: translate and bolt down a motor mount to achieve timing-belt deflection/retention. It does not tune friction resisting a gravity-loaded revolute joint.
- **#1647**, our retired service arm, closed final: slide a counterweight to cancel gravity moment and capture alignment with a transverse pin. CELLO leaves gravity torque present and resists it through distributed pad friction. Its robot workflow and hardware are independently documented. It is not a relabelled counterweight/pin task.

Full17-field inventory, scoring/controls/reset, current heads/source files, adversarial review and YAM screen are in `datacenter.json`. The key unresolved rejection is that the motor already holds the arm or that no useful hold-versus-drag window exists. The cheapest next check is the genuine loose-brake load baseline, then CPU full-hull support/driver poses for both source screw axes using the actual chain. All315 hulls per arm, palms, wrists, tool and second arm matter. No full source registration or YAM path has yet been demonstrated. Effort is medium/high but the five supplied solids and real instruction make this more tractable than12 tiny compliant foot pieces.

A correction from the bounded pass: the earlier original-GELLO **extension-spring** description was unverified and is withdrawn. Community issue31 reports torsion springs, and the CELLO author explicitly supplies a printable spiral torsion spring, but neither original winding/preload/capture procedure was retrieved. No spring-assembly task was promoted. The final candidate is the independently documented **rotary brake tuning** operation.

Independent final criticism found no exact duplicate: #813 lateral rolling preload differs from rotary gravitational hold and backdrive friction, and a shared adjust/test tradeoff is insufficient under Version21. The authentic CELLO README resolves importance but does not permit a surrogate arm/load. This supports source-guided CPU readiness with the explicit kill conditions, not a completed feasibility claim.
