# Robot building and lab hardware: final scoped discovery

**Recommend one bounded CPU investment: fit the passive return-spring loop to Toyota's actual YUBI teleoperation glove.** Its source has an exact procedure and registered assembly geometry. Faze4 paired cycloidal assembly is the strongest rigid backup. Four other deep dossiers remain reserves and are not promoted to fill a quota. The machine-readable dossier is [robot_build.json](robot_build.json).

Twenty initial operations and five additional operations were screened. Exact designer sources were read for eleven initial operations; other entries are explicitly marked source targets, blocked pages, or incomplete procedures. No blocked manufacturer page is represented as inspected. No belt, encoder, calibration jig, clip or dowel-joining task was revived. Dowels appear only as installed background tendon-guide supports in the OpenHand source.

| Deep candidate | Score, components I/N/S/F/E | Disposition |
|---|---:|---|
| **RB25: Install the passive spring loop on a Toyota YUBI data glove** | **88: 20/22/20/13/13** | **BUILD-READY FOR CPU PREFLIGHT** |
| RB01: Close both Faze4 cycloidal disk orbits around their common output carrier | **86: 19/20/19/15/13** | **BUILD-READY FOR CPU PREFLIGHT** |
| RB02: Install helical thread inserts and remove their drive tangs from an ODRI shell | 78: 19/22/17/9/11 | **PROMISING BUT SOURCE-GATED:** dimensioned selected coil/installation-tool interface |
| RB03: Seat and clamp the real ODRI motor rotor through its spoke windows | 77: 19/20/15/10/13 | **PROMISING BUT SOURCE-GATED:** actual spoke-window/hub/winding access geometry |
| RB04: Route and zero an OpenHand F3 finger tendon | 74: 19/18/18/8/11 | **HIGH-RISK RESERVE:** thin flexible line, finger compliance and acquisition |
| RB05: Close the real Moveo gripper's four-bar jaw loops | 73: 18/10/19/14/12 | **HIGH-RISK RESERVE:** unresolved semantic novelty, not source shortage |

These are engineering priority scores, not acceptance probabilities. The source-gated candidates have precisely identified missing essential geometry; they are not ready for a full implementation. None has an executed stock-YAM collision path or contact-physics pass.

## RB25: Toyota YUBI passive spring loop — first CPU candidate

**Real work and importance.** Toyota Frontier Research Center's YUBI is an actual finger-driven robot teleoperation/data-collection system with a robot-mounted gripper. Its right-hand glove assembly procedure, step11, explicitly fits a No16 rubber band to the outer finger-base hook and the holder hook/groove, then checks smooth finger opening/closing. This is genuine robotic hardware preparation. It is a passive restoring spring, distinct from an active driven tendon or a toothed power-transmission belt.

The exact source is [Toyota/yubi-hw at dd8bd13d](https://github.com/Toyota/yubi-hw/tree/dd8bd13d2fd8e5003057243576f88be333d95fc5), under **CERN-OHL-W v2**. The [rendered source page16](robot_build/evidence/yubi/rubber-page.png) was visually inspected. The exact PDF, BOM and assembly hashes are in [the YUBI source manifest](robot_build/evidence/yubi/source-manifest.json). The full assembly SHA256 is `7cffdf898a1cf54b897e95c116aa9dea6ac4307c06964d551001ecf938f321dd`; PDF SHA256 is `f9b185b67fc36b57850055642f609768529ef9f736bef15e2f24bd1921efb069`.

**Matched hardware.** Use one complete RIGHT-hand version, with its outer `t30_R` finger and inner `t20_L` finger. Do not use the standalone `t20_R` finger from the left-hand option. Source-native occurrence transforms for46 parts are preserved in [assembly-occurrences.json](robot_build/evidence/yubi/assembly-occurrences.json). Registered STEP exports are `registered_parts/2.step` (outer finger), `3.step` (inner finger), `16.step` (holder), `0.step` (under plate), `1.step` (upper plate), and `8.step` (grip). Their hashes and compact staging inventory are in [YUBI_CURATED_INPUTS.json](robot_build/evidence/YUBI_CURATED_INPUTS.json); do not stage the working clones.

BOM materials are PLA printed plates/fingers/holder, POM bushings, metal fasteners and a natural-rubber loop. The holder is72.1 ×26 ×58mm, under plate67 ×21.77 ×39mm and grip20 ×80.3 ×13.7mm. The spring is specifically **Kyowa Oband GE011 No16**, with product identification in BOM row39. The manufacturer's catalog was proxy403, so its free circumference, cross-section and force–strain are not independently verified. No purchase was made. Do not borrow a No16 dimension from another country's sizing standard or claim a calibrated force law.

**Starting state and instruction.** The genuine glove is assembled without the spring; all gears, pins, encoder and electronics are background. A real loose No16 loop lies in an ordinary tray. The glove can be counterheld by its normal grip or supported at its plate; the support must not retain the spring. “Fit the rubber spring loop onto the finger-base hook and the holder hook and groove, then leave the fingers opening and closing smoothly with the loop retained.”

**Physical skill.** The robot acquires a narrow closed soft loop, captures its doubled segment on a small moving hook, routes the actual groove, stretches to the rear holder hook and releases without the first end escaping. One hand can counterhold or manage the first capture while the other stretches/routes. A94mm nominal aperture is not a stock-hand feasibility proof: palm/wrist occlusion, thin-loop pinching and first-hook retention during regrasp are central questions. Use real loop contact, never a rigid enlarged ring, grasp tab or invisible attachment.

**Proposed observable score.** 0.25 for the correct finger hook retaining the loop after that hand releases;0.5 for both hooks plus the groove retaining it after both hands release;0.75 for a declared safe full open/close stroke without escape or damage. Full credit also needs a geometry-consistent passive spring response to a small displacement/release. The source says smooth opening/closing; it does **not** specify a neutral angle, return time or restoring direction. Determine direction from actual pivot/route length before fixing a benchmark criterion. A vertical joint axis or against-gravity test must make the missing-band control fail. Macro video checks hooks/groove, a protractor or camera fiducial checks motion, and the released final mechanism must remain functional.

Wrong-side attachment, bypassing the groove, looping around the grip/fixture, one-hook-plus-gripper retention, an omitted band relying on gravity, and a locked finger must all fail. Reset by unhooking without damaging the PLA features and returning the loose loop; replace a torn or permanently stretched band.

**Immediate source-local CPU inputs.** Units are millimetres in the source exported frame, with z around1000mm; these are not bench coordinates. The outer finger's8mm shaft axis is through `(-11.690496996,-10.080051812,1020.0)`, direction `(0,1,0)`, supported by source cylinder faces167/178/302/304. The small finger-base hook support face5 has center `(-22.055430442,9.919948188,1035.0)`, area2.5403mm² and bounds x[-22.690497,-21.420364], y[8.919948,10.919948], z=1035.0. Surrounding hook faces2–7 preserve the actual contact feature. This is an exact source-face center, **not** a verified band centerline or grasp pose. The second holder-hook saddle has not been confidently assigned. Do not invent one to claim a torque or return test. Full analytic feature inventory is [registered-features.json](robot_build/evidence/yubi/registered-features.json).

**Novelty checks.** Fresh [#1872](https://github.com/robocurve/benchmark-tasks/pull/1872), OPEN head `8c10b6f0`, uses graspable rigid J-hook ends on an elastic cord to restrain cargo on fixed cart tubes. [#1519](https://github.com/robocurve/benchmark-tasks/pull/1519), CLOSED head `e16dff9a`, selects an elastic strap with rigid hooks to restrain a spring-loaded tote lid. Their task.json, README and central mechanism/scoring files were read, including the current cord force/path laws. YUBI directly grasps a closed soft loop, attaches it to fixed device hooks/groove and makes a moving robot interface into a spring-loaded mechanism. That distinction is meaningful, but elastic fitting is real overlap and live ownership must be respected. Do not dismiss #1872 because its simplified cord omits robot contact. Open #2203 is an already seated toothed belt tensioned by moving/bolting a motor mount; it is not the YUBI operation. Internal F3 is an open active tendon over rollers, not this passive closed spring.

**Cheapest falsifier and finite build plan.** Root can first place the complete source-local stock gripper/palm/wrist envelope at the actual first-hook target and compare with source body geometry, with a deliberate intersecting negative control. This is only a local clearance lower bound. Then identify the second real hook, sweep the true groove route versus finger angle and test first-hook capture during regrasp. Contact implementation can use a deformable elastic closed loop with explicit source hook surfaces and friction; source-data uncertainty requires declared parameter sweeps. It cannot use a force law with no possible loop escape or omit robot–loop contact. Only after actual full-arm path and genuine loop-acquisition tests should native demonstration work begin. No contact prototype or YAM path was executed by this scoped agent; root owns the one optional preflight.

## RB01: Faze4 paired cycloidal reducer

**Real work and importance.** A robot builder assembles a Faze4 six-axis robot's J4 elbow reduction gear. The designer's *Assembly instructions 3.1.pdf* says the J4 cycloid assembly is the same as Joint5, instructs alignment of the holes in both disks, and requires the output bearings to turn freely. This is genuine robot construction, with no employment-total argument needed. A badly phased or seized reducer cannot operate its robot joint.

The pinned manufacturer/designer repository is [Source-Robotics/Faze4-Robotic-arm at a482f399](https://github.com/Source-Robotics/Faze4-Robotic-arm/tree/a482f3993457fd5b4071d740f0bc826ffc0d7b32). The exact source PDF, both original archives, extracted J4 part files, STEP and inspection output are retained under [robot_build/evidence/faze4](robot_build/evidence/faze4). The source license is **CERN-OHL-S 2.0** and must accompany derived assets.

**Use the compact J4 assembly throughout.** Do not mix J5 forearm names with J4 meshes. The J4 case is approximately 77 × 76.74 × 25 mm; its cover 90 × 80 × 14 mm; each disk 58.77 × 58.30 × 7 mm; the output carrier 46 × 45.84 × 20.5 mm; and the eccentric 17 × 19.96 × 16.6 mm. The designer used PETG; bearings and screws are ordinary metal hardware.

The analytic disk has five output holes of radius **5.503029 mm** on a **19 mm pitch radius**, a bearing recess of radius **11.54 mm**, and a **1.503029 mm feature offset from its STEP construction origin**. An 8 mm output bearing in an 11.006058 mm orbit hole therefore has nominal radial orbital room of 1.503029 mm. This is a genuine orbit allowance. It does not justify enlarging holes until every phase fits. The independent source eccentric STL has17mm seats separated by about3mm, giving1.5mm opposed eccentricity. The available static margin is small: source-frame registration and a disclosed small print-clearance sweep must precede any fit claim.

**Starting configuration.** Fix the genuine J4 housing in an ordinary bench support. Its NEMA17 motor, twelve ring-roller stacks, eccentric and first disk/bearing are already assembled at the source's intermediate stage. Leave the second disk with its 17 × 23 × 4 mm bearing, the common output carrier with five pairs of 3 × 8 × 4 mm bearings, and the real bearing cover loose. The cover already carries its 35 × 47 × 7 mm output bearing. The ordinary driver is in a tray. Prestart the five M3 × 10 mm cover screws only enough to keep them in their real bores.

The PDF contains obvious quantity errors, including a NEMA17 quantity of twelve and an output-screw quantity of one. Use the five output holes, exploded picture and matching carrier to establish five screw/bearing stacks; preserve this correction explicitly in implementation provenance.

**Instruction.** “Fit the second cycloidal disk and the output carrier into the J4 reducer, close and secure its bearing cover, and leave the reducer free to turn.”

**Central capability.** The second disk must engage its opposite eccentric orbit and fixed ring rollers. The carrier must then acquire all five output-hole pairs across both disks. This is not just selecting a dot, inserting another independent gear, or counting five pins. The proposed challenge is closing two phase-dependent moving loops around one common output while maintaining rolling freedom. If a source-mesh experiment shows that all plausible phases assemble and run equally well, that claim fails and the task should be retired.

**Bimanual manipulation.** One hand controls a disk or carrier phase while the other stabilizes/guides the other moving part. The cover then needs support while its real screws are started and tightened. The 59 mm disk diameter is only a scale screen: the full YAM pad shape, palm, wrist, elbow and second arm must still clear the ring and case. Do not grasp crushable lobe tips or assume nominal aperture establishes stability.

**Observable scoring.** Proposed partial rungs are 0.25 for the second disk on its proper bearing seat; 0.5 for both disks plus all five paired output rollers engaged; and 0.75 for the real cover and screws retaining the released stack. Full credit additionally requires one real 360° input turn, producing about 32.727° output, followed by a return turn with no jam or slip. Proposed benchmark limits are ±2° output error, cover gap at most 0.5 mm at four points, and hands at least 30 mm clear. These are benchmark proposals, not designer tolerances.

**Ratio alone is insufficient:** one disk can still transmit the nominal reduction. Count both disks, all ten output bearings, the twelve ring stacks and cover bearing by recorded preclose inspection or a simple external post-test cover opening. The latter is assessor inspection after retained operation was demonstrated, not a new agent action. Witness marks and video/protractor measure input and output; a feeler measures cover gap. The motor drives actual contact mechanics. Never animate the output or create a proximity latch.

Wrong solutions and their prevention:

- A single disk can give the right ratio: independently inspect/count both installed disks.
- Incorrectly phase and force the carrier down: the no-damage check, cap gap and complete forward/return cycle expose binding.
- Omit rolling bearings and use bare screws: inspect paired bearings and require free rotation under a declared low-speed load.
- Hold the carrier to imitate retention: require arms clear before and throughout the drive test.
- Leave the bearing cap loose or omit its bearing: inspect retained cap, bearing and screw heads before the motion proof.

Reset by opening the real cover, withdrawing carrier and second disk, inspecting bearings/lobes, and restoring the first disk and eccentric. No material is consumed unless damaged.

**Current competitors, actual task and mechanism inspected.**

| PR | Current state and head | Actual overlap and distinction |
|---|---|---|
| [#893](https://github.com/robocurve/benchmark-tasks/pull/893) | MERGED, `010e1d8f` | Three independent spur gears descend onto fixed axes; phase is found through tooth contact. Same legitimate gearbox setting. No opposed eccentric pair/common carrier. |
| [#719](https://github.com/robocurve/benchmark-tasks/pull/719) | CLOSED FINAL, `ac0114b8` | Hold a mating spur while a keyed small gear descends, then demonstrate a coupled 30° turn. Its prior simulation failure does not erase the legitimate operation. Ending Faze4 at second-disk phasing alone would make this objection much stronger. |
| [#2003](https://github.com/robocurve/benchmark-tasks/pull/2003) | OPEN, revised `cbf99b26` | Three snug dowels join two boards. Current revision is round 8 mm sockets, not an earlier square-slot version. Shared multi-interface acquisition; different physical objects, orbital contacts and reduction outcome. Treat its revision/ownership as live. |

The broader NIST/Factory gear family remains relevant. No exhaustive live task-board or external task-set audit is claimed by this scoped agent. Fresh official semantic searches included cycloidal, planetary, eccentric shaft, phase disc, roller wheel and mecanum; they produced no extra exact match.

**Bounded CPU blueprint for root.** First register the source disk, eccentric, carrier and ring positions without changing critical surfaces. Sweep the correct assembly through one input revolution; repeat with a wrongly phased upper disk, an omitted output roller and an omitted lower disk. The missing-lower-disk control must fail part-count scoring even if it runs. Only then test stock-YAM grasps and driver access using all 315 collision hulls per arm. If nominal meshes conflict, a documented 0.05–0.2 mm print-clearance sensitivity sweep can be faithful if the wrong phase still jams and the reduction remains contact-driven. Kill if only an invisible attachment, deleted roller ring or broad clearance enlargement makes the mechanism work.

Possible future modules are `source_registration.py`, `cycloid_geometry.py`, `mechanism_cpu_check.py`, `yam_access_check.py`, `task.py`, `scoring.py`, `expert.py`, and a provenance/asset manifest. This is a build plan, not files implemented here. Native contact testing and a genuine model/demo run are future stages; no GPU or paid service was used.

## RB02: ODRI helical thread inserts

The exact [ODRI shell-preparation procedure](https://github.com/open-dynamic-robot-initiative/open_robot_actuator_hardware/blob/66af1522b4fba0ec4a1d7790e66f5e4652208d30/mechanics/actuator_module_v1/details/details_shell_preparation.md) installs four M2.5 × 3.75 mm Helicoils in each shell half, then breaks off and removes each tang. The named insert is Böllhoff **41890250375**; the tool set is Hoffmann **082800 M2.5**. The source explicitly warns that tangs must not remain in the part. That is real robot shell construction and a materially different operation from pushing a heat-set sleeve with an iron.

Use the explicitly archived original 2dof-v1 shell, whose CAD is preserved; do not silently substitute the newer shell. The base is about 33.11 × 37 × 198.50 mm, 28 g, and the cover 12 × 37 × 168.30 mm, 16 g. Source print options include PC-ABS and Duraform HST. A supported, pretapped base, insertion mandrel, genuine wire coils, breakoff punch and debris tray form the focused starting state.

Instruction: “Install the four helical thread inserts in the actuator shell, break off and remove every drive tang, and leave all four screw bores clear.” Score a correctly retained insert with recovered tang; full credit requires four clear bores passing real M2.5 gauge screws after the tools and screws are removed. Plain screws, solid sleeves, retained tangs, stripped receiving threads and scripted tang disappearances earn no undeserved credit. Physical reset consumes fresh inserts and tangs.

The hard source gate is specific: **free coil diameter/diamond wire section, tang-notch geometry and the selected mandrel slot are not dimensioned in the ODRI source**. These are the contact mechanism, not cosmetic CAD. A matched selected-product dimensional package followed by one CPU screw-in/fracture negative-control test is the cheapest falsifier. The compliant coil, helical contact and debris make full implementation expensive even if that gate is resolved.

[#1212](https://github.com/robocurve/benchmark-tasks/pull/1212), current closed head `3db7df64`, was read through task, README, `heat_set_insert_flush.py` and `seat.py`. It models a hot-iron push with axial/tilt damping, not coil torque contraction and tang finishing. This distinction supports novelty but does not establish feasibility.

## RB03: ODRI rotor installation

The [actual assembly section](https://github.com/open-dynamic-robot-initiative/open_robot_actuator_hardware/blob/66af1522b4fba0ec4a1d7790e66f5e4652208d30/mechanics/actuator_module_v1/details/details_actuator_module_assembly.md) tells the builder to preserve the brass spacer, align two rotor set screws with custom shaft flats, push the rotor down, tighten both screws with a 1.5 mm driver **while pushing down**, then check free spin and negligible axial play. The motor is the genuine 45 mm diameter, 53 g T-Motor Antigravity4004, with the stator mounted by its normal M3 × 5 flatheads.

The useful task is that final assembly substep. Initial stock motor separation was dropped after the critic found that the exposed stator grasp is not established and the published custom-shaft geometry does not describe the stock shaft. This refinement is one discovery family, not a second idea.

Executed OCCT inspection found that `motor_antigravity_4004_custom_shaft.STEP` contains **only one 3.990 mm × 33.400 mm shaft solid**, with fifteen faces. It does not contain the rotor, stator, spokes or windings. The actual photo shows the driver passing **through a spoke window to a radial hub screw**. Replacing the bell with a solid cylinder or moving screws to its rim would change the task.

A retained rotor must pass a released spin and axial-play check; low position or screw angle alone is insufficient. The relevant wrong solutions are loose retention, overclamping that rubs the stator, shaft-flat misalignment, and a fictitious external screw corridor. The source gate is exactly the actual spoke-window/hub/winding collision corridor. Do not turn this into another prolonged CAD rescue.

Current actual comparator files include open [#1359](https://github.com/robocurve/benchmark-tasks/pull/1359) (`5638bf2a`, loose rotor magnet insertion beside another loose magnet), closed [#727](https://github.com/robocurve/benchmark-tasks/pull/727) (`83beaf8e`, slide a pot magnet off a plate), closed [#2037](https://github.com/robocurve/benchmark-tasks/pull/2037) (`1e5c3340`, loose key/pulley seating, no set screw), and open [#1054](https://github.com/robocurve/benchmark-tasks/pull/1054) (`fb3d3d46`, held tool flange with external locking ring). The earlier keyed-pulley board reference TK-UG9SYY remains unmapped, so no universal novelty clearance is claimed.

## RB04: OpenHand F3 tendon routing and zeroing

The [embedded designer PDF](https://github.com/grablab/openhand-hardware/blob/b10197dcd79e7bcfa92c6d5a0bfa479e6a789fba/model%20f3%20%28forces-for-free%20hand%29/Model%20F3%20Assembly%20Guide%201.0.pdf), version1.0 dated December15,2024, gives the complete workflow: route the tendon from the motor pulley through the clearance and over the guide bearings, anchor it at the distal screw or nut, command the actuator to zero, release the pulley screw, turn the pulley until taut, and secure it again. The source gives approximately 30 cm of PowerPro Spectra line per finger, PMC780 urethane flexures and DragonSkin10 silicone pads. Actual F3 pulley, bearing sleeves, mold and plates were inspected. Background guide pins are installed before the benchmark; this is not a new pin-insertion task.

The proposed instruction asks for the real route, distal anchor and zeroing. One hand manages tendon tension while the other handles the anchor or pulley fastener. Physical scoring checks guide contacts, retained anchors, unloaded reference shape, motor-driven joint response and return to zero after release. A straight shortcut, manually bent finger, excess pretension or software-welded line must fail. Exact angle/stroke limits need calibration to the chosen real flexures; no such calibration ran.

This is source rich but mechanically expensive. Thin-line acquisition with stock pads, line/guide friction and compliant fingers remain planning only. The cheapest falsifier is one authentic finger and source pulley with full-pad line acquisition plus wrong-route and excess-tension controls. The source's **CC-BY-NC3.0** restriction also needs explicit treatment before derived assets are publicly reused.

Open [#1898](https://github.com/robocurve/benchmark-tasks/pull/1898), `710c0182`, assembles a rack/pinion gripper and proves symmetric opening; open [#2203](https://github.com/robocurve/benchmark-tasks/pull/2203), `cb29b8fc`, sets a closed timing belt's tension by translating and bolting its motor plate. Both actual task/README/mechanism files were read. F3 is an open tendon route with flexure rest-shape and frictional anchors, but shared tensioned drive assembly still warrants review. It is a reserve, not the next implementation recommendation.

## RB05: Moveo four-bar gripper

The [designer manual](https://github.com/BCN3D/BCN3D-Moveo/blob/0866a92501277636f76000a195d8a16d44b5b476/USER%20MANUAL/User%20Manual%20BCN3D%20Moveo.pdf) pages17–18 and actual STLs establish the complete hardware. Start after gear meshing and plate assembly, with both actual 71.53 mm jaws loose. Closing both jaw loops uses eight M3 × 16 screws and four M3 nuts. The 48 × 6 × 8 mm pivot arms and source gear arms must turn freely; a fixture may support the body but must not pre-align the floating jaw loops.

Physical full credit requires both loops retained and both jaw faces parallel during servo opening/closing after hands withdraw. One hinge only, a crossed branch, tightened but seized hinges or a hand holding the face parallel must fail. That is authentic and plausible at the part scale.

The strongest objection remains unresolved: closed [#1376](https://github.com/robocurve/benchmark-tasks/pull/1376), `44bec9b5`, already closes a robot four-bar on the correct branch; open #1898 already assembles a robot gripper with a functional symmetry proof. A genuine brand and eight screws do not create a new ability. Therefore this remains a low-priority reserve and should not fill a portfolio slot without stronger differentiation.

## Evidence and reproduction

[Source manifest](robot_build/evidence/source-manifest.json) records pinned source heads, original paths, URLs and hashes. [Current PR statuses](robot_build/evidence/current-pr-statuses.json), [fresh fetches](robot_build/evidence/competitor-fetch-final.json), and saved actual PR files distinguish current open, closed and merged scopes. HTML responses are retained compressed; they are ordinary public GitHub pages, not API responses. GitHub API and some manufacturer domains returned proxy403; those failures were not repeatedly retried. A GitHub repository-search batch returned429 once and was not looped.

Run from the repository root:

```bash
python research/robocurve-final-discovery/agents/robot_build/evidence/inspect_geometry.py
```

It executed successfully on CPU and inspected **82 STLs and four STEP files**. Output is [geometry-reproduced.json](robot_build/evidence/geometry-reproduced.json). This verifies source geometry extraction, not a YAM reach, collision, contact, grasp or mechanism pass. No robot controller, native benchmark, Dream-1, GPU or paid service ran. Optional mechanism prototyping is left to root as assigned.

For current competitor reproduction, use read-only unique refs, for example:

```bash
git fetch --no-write-fetch-head https://github.com/robocurve/benchmark-tasks.git pull/893/head:refs/final-discovery/robot_build/pr893
git show refs/final-discovery/robot_build/pr893:tasks/gear-train/task.json
```

All source facts, estimates, proposed tolerances, hard gates and adversarial objections remain separate in the JSON. No claim of acceptance or measured full-score feasibility is made.

To fetch exact YUBI source files without a working checkout:

```bash
python research/robocurve-final-discovery/agents/robot_build/evidence/fetch_yubi_pinned.py --out /tmp/yubi-pinned-source
```

This writes a SHA256 fetch manifest. The fetch script was syntax-checked; its exact git source path was already exercised during discovery, but the standalone fetch script itself was not rerun. Assembly/frame extraction scripts were executed; material force laws and full YAM manipulation remain unverified.
