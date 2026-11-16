# Robot/lab care extension: one new CPU-preflight candidate

**CE01 — Install a four-pin UV lamp and capture its free end in the Flex robot’s retaining clip:84/100, BUILD-READY FOR CPU PREFLIGHT.** This label authorizes a small source-grounded feasibility study; it does not claim stock-YAM clearance, a native demonstration, or acceptance.

The operation is literal equipment of an Opentrons Flex robot: its purpose-built HEPA/UV roof module receives two supplied18W2G11bulbs. Original manufacturer step7 says push all4prongs into the recessed receptacle, then gently press the free end into its retaining clip. The original illustration was viewed. Bulb-interface type, nominal electrical rating, module dimensions and mass were read from original source.

|Criterion|Score|
|---|---:|
|Importance|19/20|
|Novelty|22/25|
|Authentic source|18/20|
|YAM/fidelity|12/20|
|Physical scoring/economy|13/15|

## Original source pins

- [docs/hepa-uv/docs/installation.md](https://github.com/Opentrons/opentrons/blob/95ac66dea217cd169fbf98ac4573844bd65d01b3/docs/hepa-uv/docs/installation.md), SHA256 `3fe438bf14388fec39b9e0448e469da060a84fee0ed57e1b9968c447b6051e2e`.
- [docs/hepa-uv/docs/uv-specs.md](https://github.com/Opentrons/opentrons/blob/95ac66dea217cd169fbf98ac4573844bd65d01b3/docs/hepa-uv/docs/uv-specs.md), SHA256 `254e1e428ae1a10b1b48d66e8b2b83a8322829ea6caf31f11d53dd2f662895e9`.
- [docs/hepa-uv/docs/product-specs.md](https://github.com/Opentrons/opentrons/blob/95ac66dea217cd169fbf98ac4573844bd65d01b3/docs/hepa-uv/docs/product-specs.md), SHA256 `bbfb1145407e24d8bc7a207692c587b5529c3656293137cb9437230a4db26a0b`.
- [docs/hepa-uv/docs/images/instructions/7-insert-bulbs.png](https://github.com/Opentrons/opentrons/blob/95ac66dea217cd169fbf98ac4573844bd65d01b3/docs/hepa-uv/docs/images/instructions/7-insert-bulbs.png), SHA256 `e6b1bb7206489c36b8bad13ba5fe7e01547c1c606112dcd2b78c9e139a92c7b8`.
- [docs/flex/docs/system-description/robot.md](https://github.com/Opentrons/opentrons/blob/95ac66dea217cd169fbf98ac4573844bd65d01b3/docs/flex/docs/system-description/robot.md), SHA256 `e43b7625c0382b008394d159ecb615aadd16e9a19132e0ec88f2f09416337a92`.

Manufacturer pin: `95ac66dea217cd169fbf98ac4573844bd65d01b3`. All source bytes and hashes appear in [the manifest](care_cleaning/extension/extension-source-manifest.json). Exact source text: each bulb has4prongs that fit the power receptacle; push them into it; retaining clips hold the free ends; press gently until they snap into the clips.

## Hardware, instruction and skill

- component: One supplied18W actinic compact fluorescent UV-C bulb known: Single-cap2G11 base,4pins;18W,0.375A,58V nominal; twin long glass tubes on an insulating base in maker installation figure. material: Glass light-emitting tubes; metal pins; insulating base material not published. size: Exact bulb dimensions/mass not published in the inspected robot manual. For bounded CPU screening only, parameterize roughly200–250mm total length,35–45mm width,15–25mm depth and50–150g. These ranges are engineering estimates, not manufacturer specifications. starting_state: Unwrapped spare bulb in ordinary protective cradle, base exposed for acquisition.
- component: Original2G11 receptacle known: Recessed receptacle on module underside receives all4bulb pins by axial push. No screw/bayonet turn is specified. unknown: Pin pitch/diameter, keyed base shape, engagement depth and contact/friction forces are not dimensioned. Use a compatible actual2G11 standard pattern and explicitly estimate dimensions for CPU screening; dimension it before native hardware reproduction. essential: All4physical pin/channel alignments and base shoulder seating must remain explicit; no proximity attach or invisible socket weld.
- component: Remote bulb retaining clip known: Separate clip supports the free glass end after plug insertion; original image and text explicitly show a snap-capture action. unknown: Exact clip dimensions, material and force curve not specified. Topology is documented; spring compliance can be parameterized. essential: Clip lips must physically open/displace and close past bulb section, providing retention after release; a scripted latch triggered by nearness erases the skill.
- component: Flex HEPA/UV roof module known: 87×64×14cm,~20kg. Robot frame is sheet metal/aluminum. Module remains fixed throughout task, so YAM does not lift20kg. support: Full-size roof module or original full-size lamp bay supported at a documented service height in its original downward-facing orientation; an ordinary rigid service stand may react insertion forces. Retain all surrounding geometry that can block the hands. approximation: Other lamp bay, filters, fan internals and wiring may be omitted only where they do not affect the manipulation corridor. Do not shrink lamp, socket or remote support span.
- component: Test tools/support known: No handheld installation tool is specified. proposal: Ruler/feeler gauge, photographs, low-voltage continuity tester and a light spring-scale retention check after robot releases. Functional UV illumination is outside this physical installation task; module remains unpowered.

**Start:** A fixed, unpowered, cool module lamp bay has its original recessed2G11socket and remote retainingclip empty. One correct supplied lamp lies in a protective cradle within reach, with its plastic base exposed. Other lamp is already installed and is an obstacle only if source geometry places it in the approach. Whole module remains supported; no fictitious enlarged grip tabs or reduced-scale roof.

**Instruction:** Fit the supplied lamp into the module’s four-pin socket, press its free end securely into the retaining clip, and let go with both hands.

**Ability:** Register an extended fragile part into a multipin socket and complete a second, separated compliant capture without pulling or levering its seated terminal end out. This is coupled two-interface assembly, not screwing a bulb into one socket.

**Bimanual sequence:** One normal hand grasps/stabilizes the insulating base and guides axial pin entry. The other supports the long twin-tube section as its free end is brought to the remote clip, controlling pitch and bending load. The exact handoff/press sequence is to be established by CPU study; bimanual necessity is not claimed as proven. A single-arm success remains valid if physically possible.

## Physical score and reset

- partial: 0.25: all4pins are physically engaged in their actual channels and base shoulder is seated to proposed≤1mm gap, but free end is not captured.0.5: base is seated and clip lips have physically closed past the glass section, but the robot is touching either interface or they have not settled.0.75: both interfaces retained and hands clear, but independent completion test has not passed.
- full: 1.0: base shoulder seated, all4pins engaged, glass end retained by original clip, hands at least30mm clear for2s; assembly remains in original support geometry after a gentle independent proposed1N withdrawal/downward test. On real hardware, continuity across both lamp-electrode circuits verifies actual4pin socket contact without powering the UV ballast. No electronic hidden success flag is needed.
- measurement: Front/side photos with ruler show base shoulder gap and glass behind clip lips; feeler gauge verifies≤1mm gap; light spring scale tests retention; optional low-voltage ohmmeter checks the two filament contact circuits. Pin depth/gaps/force margins above are benchmark proposals, not OEM tolerances.
- invalid: Broken/cracked glass, visibly bent pins, broken clip/socket, bulb not matching2G11standard, or movement/damage of original support that changes the task. Simulation may treat glass as rigid and separately track visible excessive deformation/contact hazards; do not claim calibrated fracture physics.
- reset: Gently release actual remote clip, withdraw base axially, inspect pins/glass/clip, and return the same unpowered lamp to its protective cradle. No intended consumable, though damaged lamps or fatigued clips must be replaced.

All numeric gaps, test loads and hold times above are proposed benchmark tolerances, not OEM specifications. Routine UV operation is not needed to assess a mechanical lamp installation; source module remains unpowered.

Incorrect solutions:

- Balance free end on top of clip or wedge bulb against frame → Must be behind actual clip lips and survive hands-clear independent withdrawal test.
- Snap free end first while4pins remain outside socket → Full score needs4individual channel engagements and base shoulder seat/continuity, not only bulb pose.
- Push4pins partly into holder then release with remote end dangling → Only0.25; remote positive capture and retained final orientation required.
- Support bulb with one hand to make it look retained → Both hands≥30mm clear,2ssettle and independent test after release.
- Twist like an Edison/bayonet bulb or force misaligned pins → Explicit4channel geometry causes collision; bent pins/broken parts invalidate outcome, no rotation-to-success rule.

## Current official semantic comparisons

- [#2312](https://github.com/robocurve/benchmark-tasks/pull/2312) OPEN, head `efcb22e078b27f2f782b0c9c1965e6e65aa2d9ee`; created 2026-11-16T13:52:42Z; closed None. OPEN current H11headlamp swap. Actualtask.json/README/headlamp.py/scoring.py read:3lugPGJ19bayonet quarterturn, separate tab-latched2blade pigtail, glass-touch cap. CE01requires axial4pin2G11registration plus remote free-end clip supporting long glass tubes, with no bulb-axis locking turn or pigtail release. Same general bulb replacement label is not equivalent skill/interface. Files/hashes retained in the competitor ledgers.
- [#2135](https://github.com/robocurve/benchmark-tasks/pull/2135) CLOSED, head `6a5ed06d0714a845f39194ce67c33fecd59971f2`; created 2026-11-15T12:14:29Z; closed 2026-11-15T22:55:30Z. CLOSED E27tablelamp swap, actualtask.json/README/task.py read: continuous3.63mmpitch thread,3.5turns and regrasping free lamp. CE01has no helical thread or torque-following motion and needs a separated snap support. Files/hashes retained in the competitor ledgers.
- [#695](https://github.com/robocurve/benchmark-tasks/pull/695) CLOSED, head `f1aaedfc26ce057485083ef93bd46857a74835c5`; created 2026-11-06T06:15:53Z; closed 2026-11-12T08:15:37Z. CLOSED hanginglamp bulb installation. ActualREADME/task.json/centralcode read: counterhold swinging shade while threading small bulb. CE01counterholds an extended part during dual-interface insertion, rather than resisting a rotating free fixture. Files/hashes retained in the competitor ledgers.
- [#1986](https://github.com/robocurve/benchmark-tasks/pull/1986) OPEN, head `e8ecd21da83c33bfe2107962a4d1a28495b1e336`; created 2026-11-14T07:29:22Z; closed None. OPEN splash-shield pushclip. Actualtask.json/README/trim_clip.py inspected in main care audit: align2sheet holes then push one retainer. CE01uses4pin electrical socket and remote compliant glass support; not a relabelled coaxial fastener through2sheets. Files/hashes retained in the competitor ledgers.

OfficialHTML queries fluorescent,UVbulb,lampclip,bulb,Opentrons,longtube,illuminationunit all returned200 and saved results. No fluorescent/UVbulb/Opentrons exact family result found. Semantic comparators above still read. This is not exhaustive internal-board or pending PR clearance.

## Stock-YAM and faithful mechanism screen

- object_scale_mass: Single estimated50–150g/200–250mmlamp is within likely payload range; exact mass not verified. No need to handle fixed20kgmodule.
- normal_grasps: Plastic base estimated35–45mm cross-section is below nominal94mmaperture; real pad contact width, exposed base length and stable support on glass must be tested, not inferred from aperture alone. Normal second hand may support tube pair gently instead of pinching individual pins.
- palm_wrist: Recessed socket and roof lip may block palm/wrist even with reachable pins. Preserve module lip and other bulb in source-correct positions; screen full315collisionhulls perarm, not tip reach.
- tools: No installation tool or tool-wrench requirement. Test gauges are external scoring instruments, not robot substitutions.
- fixture_reaction: Original module casing/socket mount and service stand react axial insertion and clip snap. Fixture must not artificially guide bulb or open the clip for it.
- critical_path: Acquire base, carry long body clear, align4pins, enter axially, support free end during clip press, release bothhands, retract. Exact small angular motion follows actual compatible socket/clip geometry; do not invent a large hinging motion that would bend seated pins.
- verified_status: PLANNING PLAUSIBILITY ONLY; noYAMIK/collision/grasp-force/path execution or full-score demo ran.
- core: Rigid longglassbody with actual base/pins;4socket channels and shoulder; spring-contact/friction retention at socket; remote actual clip represented with explicit compliant lips and physical contact. Both interfaces remain mechanically meaningful afterrelease.
- allowed_approximation: Noncritical housing details and ballast internals omitted; dimensions within declared source-unpublished ranges used for bounded screening; clip flex can be rigid spring-loaded jaws matching actual snapcapture rather than continuum elasticity. Glass can be rigid with fracture omitted if explicitly disclosed.
- forbidden: Invisible weld after bulb enters a radius; base rotates to lock despite source axialpush; giant dummygrip; shortened span; holdingclip artificially open; count alone from object proximity.

**Hard blockers:** No known fatal operation/authenticity/semantic blocker from reviewed sources. Build remains conditional on CPU finding ordinary-hand access and a source-compatible standard/socket/clip representation. Unresolved tolerances are declared engineering inputs, not evidence of a passed test.

**Cheapest falsifier:** Bounded CPUonly study of one full-size2G11bulb/socket/remoteclip bay, sweeping declared source-unpublished length and plausible clip/socketforce parameters. Overlay stockYAMall-hull palm/wrist/arm geometry at base-entry and remoteclip-press poses. Negativecontrols: basepins offset by halfpitch, remoteclip captured butbaseunseated, and posedbulb besideholder must allfail mechanicalretention. Kill if normalbasegrasp/palm cannot approach or if fullscore requires fictitious clip/attachment.

**Relative effort:** Medium, cheaper than flexible band/tendon and multistage geartrain: one extendedrigidpart,two contactinterfaces,one small compliantclip,no threadedfastener or fluids. Actual CPU setupnotimplemented.

**Strongest rejection:** A lampreplacement variant, or genericlabinfrastructure, with guessedsocket/clips and servicefixture easier than realrobot.

Importance and mechanism distinction supported by exactrobotmanufacturerworkflow plus actualclosestPRcode. Dimensional fidelity and installedroof clearance remain boundedCPU questions. This supports research investment, not a completed submission.

## Source-rich extension screen

|ID|Operation|Disposition|Source-backed reason|
|---|---|---|---|
|CE01|[Install the18W2G11 bulb in the Flex HEPA/UV robot module: axial4pins plus remote retainingclip](https://github.com/Opentrons/opentrons/blob/95ac66dea217cd169fbf98ac4573844bd65d01b3/docs/hepa-uv/docs/installation.md)|FINALIST: bounded CPU preflight justified|Real robot accessory, original manufacturer procedure/figure and bulb-interface standard verified. Distinct axial insertion+remote snap support; critical dimensions and force ranges declared approximate.|
|CE02|[Replace Flex1/8channel pipette nozzle O-ring using supplied removal and roll-on tools](https://github.com/Opentrons/opentrons/blob/95ac66dea217cd169fbf98ac4573844bd65d01b3/docs/flex/docs/maintenance/cleaning.md)|DEMOTE_NOVELTY|Actual source-rich procedure, but accepted#1576 already seats an elastomeric seal over a shaft into a groove; different tool/scale alone is insufficient. Manufacturer prohibits applying procedure to96channel pipettes.|
|CE03|[Preload an OpenFlexure motorized scanning-stage actuator with a30×2mmViton loop on two hidden hooks](https://github.com/rwb27/openflexure_microscope/blob/0cedf45238bb1cf8185f4ad92d366eb36f44efc3/docs/1_actuator_assembly.md)|CROSS_AGENT_EXISTING_LEAD; NOT COUNTED AS NEW FINALIST|Complete tool/hook/foot source CAD and exact ring size; genuine fork-tool insertion and dual catch preload. Root notes already in datacenter initial bank, and AI importance of microscope needs robot-workflow argument.|
|CE04|[Install a Heater-Shaker thermal adapter with its genuine T10 Torx screw and verify flush seating](https://github.com/Opentrons/opentrons/blob/95ac66dea217cd169fbf98ac4573844bd65d01b3/docs/heater-shaker/docs/adapters.md)|DEMOTE; ROOT EXCLUDES ANCHOR FAMILY|Source gives exact tool/screw, flush/rocking test; essentially ordinary adapter bolting and too close to already considered module anchors.|
|CE05|[Attach Flex96channel pipette mounting plate after disconnecting right z-axis carriage](https://github.com/Opentrons/opentrons/blob/95ac66dea217cd169fbf98ac4573844bd65d01b3/docs/flex/docs/installation/instruments.md)|PROMISING_BUT_SOURCE_GATED|Real unlike single-pipette mount; only high-level sequence read, no carriage disconnect mechanism. Cannot invent a coupling from screenshots or generic screw attachment.|
|CE06|[Load a Flex Stacker with labware supported by its two internal latches](https://github.com/Opentrons/opentrons/blob/95ac66dea217cd169fbf98ac4573844bd65d01b3/docs/stacker/docs/loading-labware.md)|DEMOTE|Real protocol preparation, but placing a plate onto supports without a further documented retention action is not yet a distinctive ability.|
|CE07|[Dock the Flex Absorbance Plate Reader illumination lid after a plate exchange](https://github.com/Opentrons/opentrons/blob/95ac66dea217cd169fbf98ac4573844bd65d01b3/docs/flex/docs/modules/absorbance-plate-reader.md)|RESERVE; DOCK-GEOMETRY GATED|Original automated-lid role,155×95.5×57mm envelope,21Ngrip schema and grip48mm above base verified. Precise receiving/retention interface absent;95.5mm body also slightly exceeds94mm stock aperture. Do not fake magnetic/proximity retention.|
|CE08|[Press the OpenFlexure condenser lens into its housing using its prescribed insertion tool](https://github.com/rwb27/openflexure_microscope/blob/0cedf45238bb1cf8185f4ad92d366eb36f44efc3/docs/3_illumination.md)|DEMOTE|Actual lens flat-side-down tool support and vertical housing press described, but microscope AI importance and small lens acquisition unresolved; not automatically novel versus other press-fit seats.|
|CE09|[Press the keyed pinion onto an OpenFlexure stepper motor then mount it](https://github.com/rwb27/openflexure_microscope/blob/0cedf45238bb1cf8185f4ad92d366eb36f44efc3/docs/5_motors.md)|ELIMINATE_ABILITY_OVERLAP|D-flat shaft alignment and pinion press fit are existing keyed shaft/pulley family; no source-completeness bonus can make this a different ability.|
|CE10|[Replace a Flex deck slot with a staging-area extension plate](https://github.com/Opentrons/opentrons/blob/95ac66dea217cd169fbf98ac4573844bd65d01b3/docs/flex/docs/system-description/robot.md)|DEMOTE|Actual robot-equipping procedure and column-specific geometry documented, but two-screw plate exchange provides weak novelty.|
|CE11|[Replace the Flex HEPA filter and refit its prefilter with airflow arrows correct](https://github.com/Opentrons/opentrons/blob/95ac66dea217cd169fbf98ac4573844bd65d01b3/docs/hepa-uv/docs/maintenance.md)|DEMOTE_ABILITY_OVERLAP|Source-complete robot accessory maintenance, but generic filter/cartridge replacement is already crowded; arrow selection does not create a different physical skill.|
|CE12|[Install an OT.One model-specific pipette clamp and stabilizer](https://github.com/Opentrons/otone_hardware/blob/5488af883a50c170301a0c1845abd50a51b9dfb3/README.md)|SOURCE_GATED; NOT FINALIST|Manufacturer publishes all CAD/BOM for independent robot construction, including many real pipette clamps, but no matched clamp assembly operation was recovered. CAD inventory alone is not a procedure.|

CE03 is an existing cross-agent discovery lead and is not counted as a new finalist. CE02 loses to actual accepted#1576; tool choice alone does not rescue an O-ring seating variant. Source-rich alternatives were not promoted simply to fill the root portfolio.

## Secondary source-gated reserve

**CE07: Flex plate-reader illumination lid,65/100, PROMISING BUT SOURCE-GATED.** The manufacturer’s actual lid schema verifies155×95.5×57mm,21NFlexgripper setting,48mm grip height and9mmxoffset. The manufacturer requires a Flex gripper to move this lid during plate-reader operation. Its physical docking/retention interface was not recovered, and the95.5mmwidth is already wider than the nominal94mmstockYAMaperture. A side ledge might enable a normal alternative grasp, but that is not verified. Do not invent a magnetic dock or invisible attachment; do not count it toward15before the exact interface is read. The JSON preserves its proposed instruction, partial/full score, wrong solutions and cheapest falsifier.

## Bounded build path

- configuration: One originalfull-size lampbay, actual2G11lamp envelope, recessed4pinholder and remoteclip, casinglip and anysecondlamp obstacle. Fixturefixed; lampstarts inprotectivecradle.
- modules: ['source_parameters.json with verifiedversusestimatedfields', 'bulb_socket_geometry.py with4pinentryandshoulder', 'remote_clip_mechanism.py withphysicalelasticcapture', 'cpu_yam_corridor_screen.py usingvalidated315hullsperarm', 'physical_score_spec.json andnegativecontrols']
- CPU_goal: Verify ordinarygrasp/socketentry/clippress geometry and partial/fullretentionstates without GPU or scriptedstateattachment.
- finite_path: Fix sourcecompatibleparameters→CPUnegativecontrols/clearance→smallphysicalcontactprototype→eventualnative scripteddemo and paidpolicydecision handledlater.
- kill_conditions: ['Requires alteredYAMhands or enlargedbase.', 'Originalclip cannot capture usingordinarytool-freepath.', 'Needsreplacingphysicalpin/clipretention withproximityflags.', 'A currentearlierofficialtask withsame4pin+remoteclipskill isfound.']

## Executed limits

- ReadoriginalmanufacturerOpentronsprocedure/specifications andviewedbulbinstallfigure
- Currentofficialsemanticqueries returnedactual200results;6additionalPRheads fetchedunique refs/final-discovery/care/prNN
- Actual#2312/#2135/#695/#1576task.json,README andcentralcodeinspected; maincare#1986reusedwithsameexactpin
- OriginalOpenFlexureauthorinstructions,manufacturerOT.OneREADME/CADtree andOT2hardwaretreeinspected
- NoGPU,paidwork,procurement,submission,taskimplementation orYAMCPUpreflight

No YAM clearance or contact simulation ran. Unknown bulb/base/socket/clip dimensions are explicit inputs to a bounded CPU sweep, not passed measurements. Manufacturer hardware photos establish the real4pin-plus-remote-clip topology; a full OEM CAD set is not required before this small investment. Exact source-compatible dimensions and forces should be established before claiming a faithful native hardware demonstration.
