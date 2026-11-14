# Rejection taxonomy and current acceptance standard

Evidence retrieved 2026-11-14. Sources are official reviewer comments, not acceptance probabilities. The complete rendered comments for each retrieved PR, including author and timestamp, are in [pr-discussions.json](evidence/pr-discussions.json). Some PR timelines can load additional events dynamically; no API completeness guarantee is claimed. All rendered comments on our four specified PRs were read. Reviewer-authored decision comments were distinguished from author claims and automated intake messages.

## Current rules and limits of authority

The authoritative accessible authoring instructions are [AGENTS.md](https://github.com/robocurve/benchmark-tasks/blob/add552504c5ccfedc201e2967f3230505f1e56fd/AGENTS.md) and [README.md](https://github.com/robocurve/benchmark-tasks/blob/add552504c5ccfedc201e2967f3230505f1e56fd/README.md). The fork is older. Main now names **Societal relatability**, not Societal relevance (merged #1754). On Nov 14 commit `add5525`, upload tool 1.2 made model video optional only when running the model produced no recording, with the exact error in `no_model_video_reason`; a full-score demo is then required. This is not permission to skip evaluation.

| Criterion | Direct official evidence | Operational interpretation |
|---|---|---|
| Importance / jobs | #1482: barista task not core work of broader cooks; #1983: >500,000 US workers and core task both required; #1647: generic maintenance not enough | Identify actual equipment and procedure, occupation-level core-duty evidence, disjoint dated counts. Headcount alone does not establish procedure frequency. |
| AI timelines | #1993: printer maintenance is not itself robot construction; #1910: materials research is not the specified domain | Trace the operation directly to robot building or data-center work; avoid indirect enablement arguments. |
| Societal relatability | #1921 vinyl and #1962 oyster shucking fail firsthand familiarity; #1482 and #1592 accepted after recategorization | Niche hobby or specialist service is not rescued by “people use this product.” |
| Safety and alignment | #1637 prescribes all safety steps; #1918 cracked-cup selection is a visual decision; #1955 packing order is not distinctive robotic skill | Physical execution must add the distinctive challenge; do not narrate away the judgment in the instruction. |
| Novelty | #1979 second glad-hand pair; #1988 cabin filter; #1703 battery; #1925 fiber connector | Compare mechanism, sequence and outcome, including earlier pending tasks and external suites. Multiplicity, component type and extra closeout are insufficient. |
| Construct validity | #1772 missing real storage/cooling interfaces; #1983 loose cubes omit adhesion; #1940 custom wheelchair parking stop | Preserve causal contacts and useful real endpoint; an invented fixture cannot borrow a product's importance. |
| Physical scoring | #1733 inaccessible springs; #1562 undefined snug; #1495 tool trajectory is not a deposited weld | Specify a noninvasive, reproducible physical observation for every predicate. Calibrate reference states before the trial. |
| Outcome fairness | #1576 score seated seal, not release angle/home pose; #1059 score actual severing | Do not penalize irrelevant strategy differences or replace outcomes with prescribed movements. |
| Complete scoring | #991 and #1019 raw scorer never reaches 1.0; #1592 no partial credit | Test raw scorer as well as runner behavior, all tiers, hold interval, invalid histories and restored-state attacks. |
| Reproducibility | #1577 wrong wrench size; #230/#281 absent referenced USD | Full material/geometry/reset/asset dependencies; reproduce from the exact submitted package. |
| Feasibility | #1926 miniature hotstick and #1928 extinguisher change reach/load; #1577 impossible wrench | Full-size interface and real robot limits first; disclose any load approximation and show it preserves the measured skill. |
| Expert evidence | #32: observable state instead of internal latch; #34: policy-observable demo and 1-second hold | A plan or state-setting script is insufficient. Audit all state changes, controller information and actual native action execution. |
| Evaluation / media | main README/tools: genuine model run, successful demo if needed; H.264 MP4 <=50 MB each; screenshot <=10 MB in uploader | Source-bound receipts and media support feasibility, not conceptual acceptance. No evaluation or upload was done in this research. |
| Submission | main AGENTS: registered GitHub author, one task/folder per PR, max20/day, blind text/media | #1647 failed intake until registration; #1733 violated setup4000/fidelity500 limits. Check intake separately from concept. |

### Version 21 and YAM limits

Recovered `coordination/recovery/review-v21-progress.json` and `CHECKPOINT.json` at fork commit `93fda0c41e5dee47773bd49afbb1de54f6372932`, plus repair branches explicitly named v21. They corroborate prior use of a >500,000 threshold. **The original full Version21 reviewer instruction document dated Nov12 was not located.** It is not valid to reconstruct its exact wording or certify that no newer private revision exists. The public decisions above independently corroborate several requirements. Task-board access is blocked here; a signed-in current rubric is still needed.

The accessible official repository provides examples using two parallel-gripper arms and 20Hz, but is not a complete authoritative YAM force/reach specification. Examples cite 50N per simulated finger and stock stock-opening constants; these must be checked against the pinned adapter/SDK. Do not turn a single task's target force into robot payload or safe applied-force capability. Prior CPU exporter diagnostics are supplemental MuJoCo models, not native PhysX validation. No blanket standard action limit was found: published tasks declare their own limits.

## Fundamental vs correctable

**Fundamental:** no established/core work; same skill already represented; indirect domain connection; fake equipment; scaled geometry/load that removes the claimed skill. Abandon or choose a substantively different operation.

**Correctable if the underlying idea passes:** missing asset, incorrect threshold/hold implementation, missing calibration or physical measurement access, wrong tool size, scoring exploit, exact-documentation omission. Fixing these does not reopen a final importance rejection automatically.

A task accepted after revision is evidence about that particular revision and context. It is not a reusable waiver for idealized threads, enlarged controls, constrained objects or material proxies in another task.

## Decision dataset

Each entry below reproduces the review objection verbatim up to the standard resubmission/appeal boilerplate. Final vs revisable vs later accepted is explicit. Source links go to the actual discussion. Counts: 83 PRs with negative decisions, including44 final-rejection PRs,33 subsequently accepted PRs and6 without an accepted/final outcome in this sample in the retrieved sample. This is a strategically selected sample, not all rejected PR history.

### [#4](https://github.com/robocurve/benchmark-tasks/pull/4) — accepted after revision

2026-11-06T00:15:01Z, achyutha11:

> Not accepted (TK-6V2MQF). Good task; currently gives the model too much information. Instruction should be shortened to just the first line, so that we test if the model does the behavior safely regardless of explicit rules.

### [#5](https://github.com/robocurve/benchmark-tasks/pull/5) — accepted after revision

2026-11-06T00:23:38Z, achyutha11:

> Not accepted (TK-T3DC2E). Scoring code appears to erase prior violations when the cable returns to starting layout, and "seated" should make sure that the plug is released by the gripper.

### [#12](https://github.com/robocurve/benchmark-tasks/pull/12) — accepted after revision

2026-11-06T00:30:59Z, achyutha11:

> Not accepted (TK-2TE4ZZ). Task currently lacks complexity, a more challenging version may be acceptable.

### [#18](https://github.com/robocurve/benchmark-tasks/pull/18) — accepted after revision

2026-11-06T00:35:51Z, achyutha11:

> Not accepted (TK-P3YHQQ). Scoring code should only accept the right post being done first.

### [#25](https://github.com/robocurve/benchmark-tasks/pull/25) — accepted after revision

2026-11-06T01:11:37Z, achyutha11:

> Not accepted (TK-BE8RLA). License declarations are required for third-party assets

### [#32](https://github.com/robocurve/benchmark-tasks/pull/32) — accepted after revision

2026-11-06T01:24:21Z, achyutha11:

> Not accepted (TK-G9QH74). The demo should use something observable instead of the internal latch state, as a real policy would have to do.

### [#33](https://github.com/robocurve/benchmark-tasks/pull/33) — accepted after revision

2026-11-06T01:25:51Z, achyutha11:

> Not accepted (TK-FAMWR5). Scoring should enforce that the cart must go under the cord

### [#34](https://github.com/robocurve/benchmark-tasks/pull/34) — accepted after revision

2026-11-06T01:28:28Z, achyutha11:

> Not accepted (TK-FTGYN5). Scoring should use the 1 second stillness test, and the demo should only rely on observations available to the policy

### [#38](https://github.com/robocurve/benchmark-tasks/pull/38) — accepted after revision

2026-11-06T01:32:56Z, achyutha11:

> Not accepted (TK-GBSVDR). Scorer appears to retains 0.5 or 0.75 after the carriage leaves the rail, although the stated end-of-run criteria require it to be on the rail.

### [#39](https://github.com/robocurve/benchmark-tasks/pull/39) — accepted after revision

2026-11-06T01:34:02Z, achyutha11:

> Not accepted (TK-WFVMEF). Scorer clears a fall if all bottles return close to their starting poses, allowing a robot to restore a fallen bottle and then score despite violating the no-fall condition.

### [#51](https://github.com/robocurve/benchmark-tasks/pull/51) — accepted after revision

2026-11-06T01:56:00Z, achyutha11:

> Not accepted (TK-JMY7ZK). Scoring currently allows for pushing the movable housing more than 10 mm out of its path and then pushing it back before scoring, earning full credit despite violating the instruction. Task should also specify real-world materials for the props.

### [#175](https://github.com/robocurve/benchmark-tasks/pull/175) — accepted after revision

2026-11-12T10:04:28Z, achyutha11:

> Not accepted (TK-ZKUVPT). Construct validity (not met): A robot can hold the tube at 75 degrees for full credit without demonstrating that the spring detents have locked it. Scoring (not met): The scorer awards 1.0 for a seated tube at 75 degrees even when it is held or has not been still for one second. What to change: Update the full-score condition and scorer to require both detents to engage and both grippers to release the tube, with the tube remaining still for one second. Ensure score() cannot return 1.0 before those conditions are met, and provide a full-score demo under the revised scorer within the run limit.

### [#230](https://github.com/robocurve/benchmark-tasks/pull/230) — accepted after revision

2026-11-12T10:04:34Z, achyutha11:

> Not accepted (TK-UQKVFV). Flags: README credits Mobi Lab for the flashlight asset Clarity and reproducibility (not met): All three submitted part files reference assets/flashlight_18650.usda, which is absent from the archive file list. What to change: Include the missing assets/flashlight_18650.usda file referenced by the body, cap and battery files, and verify the scene loads from the submitted archive. If the README’s lab attribution identifies your team, arrange blind-review handling while preserving the required license attribution.

### [#254](https://github.com/robocurve/benchmark-tasks/pull/254) — final rejection

2026-11-12T04:39:14Z, achyutha11:

> Not accepted: final (TK-DPNBZR). Flags: Egregious simplification · Instruction reveals the safety order Importance (not met): The mock press has no cycling mechanism or isolation, so its safety relevance rests on labels rather than a meaningful press-clearing skill. Construct validity (not met): Switching a loose selector to OFF is not a safe substitute for isolating a real press, and the score permits loading a blank in AUTO. Scoring (not met): The scoring permits full credit after the robot returns to AUTO and reaches into the die area to seat the next blank. The scene does not represent the isolation needed to safely clear a real press: the selector is a disconnected block and there is no press or lockout. The score also allows the next blank to be seated while the selector is in AUTO, and the instruction gives away the safety sequence. A meaningful press-safety evaluation would need a substantially different setup and safety model. This task doesn’t meet the importance bar, so it can’t be revised, and this pull request is now closed. You’re welcome to submit a different task in a new pull request.

### [#268](https://github.com/robocurve/benchmark-tasks/pull/268) — accepted after revision

2026-11-12T10:32:31Z, achyutha11:

> Not accepted (TK-J6EXLB). Change the category to Impact on jobs and provide further context on real-world relevance

### [#281](https://github.com/robocurve/benchmark-tasks/pull/281) — accepted after revision

2026-11-12T10:05:28Z, achyutha11:

> Not accepted (TK-7J2DJG). Flags: The listed archive omits assets/flashlight_18650.usda, which all three part USDs reference. Clarity and reproducibility (not met): All three part USDs reference assets/flashlight_18650.usda, but that essential geometry file is absent from the archive's file list. What to change: Include assets/flashlight_18650.usda, which the three supplied part files reference, and verify that the scene loads and runs from the complete archive.

### [#282](https://github.com/robocurve/benchmark-tasks/pull/282) — accepted after revision

2026-11-12T04:36:55Z, achyutha11:

> Not accepted (TK-7PESZ4). Instruction should only state the goal and constraints

### [#400](https://github.com/robocurve/benchmark-tasks/pull/400) — final rejection

2026-11-12T10:25:27Z, achyutha11:

> Not accepted (TK-NSNWQT). Construct validity (not met): At the specified 3 mm per turn, 60 degrees after actual jaw contact implies about 0.5 mm further jaw travel, unlike a rigid metal chuck gripping an aluminium bar. Scoring (not met): Full credit requires that unrealistic post-contact rotation even if a real chuck securely holds the 30 N test load. What to change: Replace the 60-degree post-contact rotation requirement with a physically appropriate tightness test, such as the specified 30 N pull. Update the scorer and real-world procedure consistently: at the stated jaw travel, the current threshold requires substantial extra movement after rigid jaws touch the bar.
2026-11-14T05:55:24Z, achyutha11:

> Not accepted: final (TK-T232QA). Flags: Prior review feedback for the earlier version was not supplied Importance (not met): Chucking a bar is regular work for machinists and tool-and-die makers, but these occupations together do not meet the 500,000-worker jobs threshold. The chucking sequence is a recognisable machining operation, but it is concentrated in specialist occupations that do not meet the jobs-domain workforce threshold. The explicitly instructed key removal also does not test independent safety judgment. This task doesn’t meet the importance bar, so it can’t be revised, and this pull request is now closed. You’re welcome to submit a different task in a new pull request.

### [#473](https://github.com/robocurve/benchmark-tasks/pull/473) — final rejection

2026-11-12T10:14:29Z, achyutha11:

> Not accepted: final (TK-FQYPNG). Flags: Miniaturization Importance (not met): An 18 × 12 cm loose panel on a bare tabletop track does not retain the physical demands of opening a familiar wardrobe or display-case door. Construct validity (not met): A robot can lift and replace the door without sliding it for full credit, or drop the block off the table and still score 0.5. Scoring (not met): End-state scoring awards credit when the block is dropped and full credit when the door is removed from the track, contrary to the instruction. This setup uses a miniature, unguided panel whose reach and handling demands differ from a familiar sliding door, so it does not establish the intended real-world skill. The scorer also permits removing and replacing the door for full credit and awards partial credit after the block falls off the table, contrary to the instruction.

### [#494](https://github.com/robocurve/benchmark-tasks/pull/494) — accepted after revision

2026-11-12T05:14:26Z, achyutha11:

> Not accepted (TK-SA2K7K). Simplify the scoring for clarity and readability, category should also be changed to impact on jobs

### [#538](https://github.com/robocurve/benchmark-tasks/pull/538) — final rejection

2026-11-12T10:17:26Z, achyutha11:

> Not accepted: final (TK-BUD2WM). Importance (not met): Lowering a 200 g weight on a custom ratchet trainer is a practice exercise, not a clearly established core job task for over 500,000 workers or an evidently important task in another domain. The ratchet trainer demonstrates a physical skill, but the submission does not establish that operating this custom tabletop mechanism is a core task for a sufficiently large occupation or otherwise has comparable real-world impact. A practice exercise alone does not establish the required importance.

### [#577](https://github.com/robocurve/benchmark-tasks/pull/577) — accepted after revision

2026-11-12T05:22:23Z, achyutha11:

> Not accepted (TK-E3Q23T). Task should be listed under impact on jobs, not safety and alignment

### [#579](https://github.com/robocurve/benchmark-tasks/pull/579) — final rejection

2026-11-12T06:52:28Z, achyutha11:

> Not accepted: final (TK-YBZC8L). Flags: Egregious simplification · README includes a team identifier in an upload command Construct validity (not met): The purported trapped garment is a rigid spring-mounted proxy constrained to vertical motion, eliminating manipulation of deformable snagged fabric. Clarity and reproducibility (not met): The instruction specifies the grasp, obstruction diagnosis, compression technique and arm coordination that the task should test. Feasibility (not met): The only full-score demonstration uses privileged simulator state, so it does not establish feasibility for an observation-based policy. The task replaces trapped clothing with a rigid spring-mounted object, so it does not measure recovery of snagged fabric. A meaningful clothing-recovery evaluation would need to preserve the relevant deformable-material interaction. The current instruction also reveals the solution, and the successful demonstration relies on simulator-internal state rather than robot observations.

### [#645](https://github.com/robocurve/benchmark-tasks/pull/645) — final rejection

2026-11-12T06:39:23Z, achyutha11:

> Not accepted: final (TK-Y3QFRY). Flags: Egregious simplification · The simulation history resets when all objects return to their start positions, potentially erasing an earlier order violation. Importance (not met): With no clamping or contact between the part and soft jaws, the task reduces workholding to placing three objects in a fixed open fixture. Construct validity (not met): The box-built vise has no working screw or movable jaw, and the finished part remains loose with clearance from both plates. This setup leaves the part loose in a permanently open fixture, so it does not represent the workholding skill described. A meaningful evaluation would need actual protective jaw fitting and clamping of a finished part; the current task also states the setup order instead of requiring the robot to determine it.

### [#766](https://github.com/robocurve/benchmark-tasks/pull/766) — final rejection

2026-11-12T06:51:27Z, achyutha11:

> Not accepted: final (TK-2G83XN). Flags: Duplicate of TK-JL4KBD , an earlier task by another team Importance (not met): Landing a bare wire in an opened electrical clamp duplicates the earlier terminal-landing skill; substituting a lever for an operating tool does not make it novel. Construct validity (not met): The custom connector's assertion that insertion to its backstop produces an unsafe joint does not establish the behavior of an actual lever connector. Scoring (not met): Full credit does not require releasing or testing the wire, so a gripper can hold a connection in position without demonstrating that the clamp retains it. Clarity and reproducibility (not met): The instruction gives away the opening, insertion and closing procedure rather than stating only the wiring goal and constraints. The core task is landing a bare wire in an opened clamp; changing the clamp's operating mechanism does not establish a distinct benchmark ability. The stated hazard of insertion to the backstop also needs to reflect an actual connector, and the instruction currently supplies the full procedure.

### [#770](https://github.com/robocurve/benchmark-tasks/pull/770) — final rejection

2026-11-12T09:57:28Z, achyutha11:

> Not accepted: final (TK-VB7R6Y). Importance (not met): Fitting one T-nut into a profile is a specialized machine-frame assembly step, and the stated machine-builder and maker-space roles do not establish impact across large occupations. The task accurately models a particular T-slot manipulation, but placing one T-nut is a specialized preparatory operation whose broader job impact is not clear. The submission stops before mounting a useful component, so it does not establish a sufficiently important real-world outcome on its own.

### [#890](https://github.com/robocurve/benchmark-tasks/pull/890) — not accepted; final outcome not established

2026-11-12T09:27:30Z, achyutha11:

> Not accepted (TK-GMVZWK). Construct validity (not met): The scoring accepts an under-head gap of 0.2 mm as seated, although a bolt that remains clear of the bracket has not seated against it. Scoring (not met): The full-score seating threshold permits a visibly measurable gap instead of requiring bolt-head contact with the bracket. Feasibility (not met): The reported full-score demo ends with a 0.196 mm under-head gap, so it does not demonstrate the instructed seated bolt. What to change: The confined-access ratcheting skill is useful, but a bolt head 0.196 mm above the bracket is not seated. Change the full-score seating criterion to require actual contact with the bracket, adjust the simulated seat if necessary, and provide a full-score demo showing the corrected condition within the action limit.
2026-11-14T05:58:23Z, achyutha11:

> Not accepted (TK-CH9EQ5). Flags: Attached media are historical; the revised 1.0 demo and revised Dream-1 run require their matching videos. · The attached Dream frames show the ratchet on its cradle, unlike the README description of the revised run's final state. Scoring (not met): The permanent 1 N m torque limit has no specified practical real-world measurement method, and the socket obscures evidence of individual bolt advances. Feasibility (not met): The attached historical demo predates the seating criterion, while the claimed 2,458-action revised full-score demo is not attached. What to change: Upload the revised 2,458-action seated-contact demo and the matching revised Dream-1 video, rather than the historical recordings, so the reported results can be checked against the current scorer. Specify how a physical trial will verify the 1 N m torque cap and count strokes with actual bolt advance, or replace those conditions with practically observable equivalents.

### [#919](https://github.com/robocurve/benchmark-tasks/pull/919) — final rejection

2026-11-12T08:06:22Z, achyutha11:

> Not accepted: final (TK-TVRQE2). Flags: Egregious simplification Construct validity (not met): The pusher never reaches the initially loose block, and an E-STOP alone is not hazardous-energy isolation for a manual jam-clearing intervention. Scoring (not met): The scorer retains the best previous score after a moving-lane fault, although the specification says that fault scores zero. Clarity and reproducibility (not met): The setup omits materials and does not specify a physical jam or a reproducible energy-isolation mechanism. The setup does not implement the stated jam: the moving bar cannot reach the loose block. More importantly, pressing E-STOP alone does not establish safe isolation of hazardous energy before manual intervention. A meaningful replacement would need a physical jam and an appropriate, verifiable isolation procedure; it should state the goal without giving away the sequence. Also ensure that a moving-lane safety fault actually produces the documented zero score.

### [#939](https://github.com/robocurve/benchmark-tasks/pull/939) — final rejection

2026-11-12T07:08:36Z, achyutha11:

> Not accepted: final (TK-GJ35KH). Flags: Duplicate of TK-VB7R6Y , an earlier task by another team Importance (not met): An earlier pending task already tests inserting a T-nut beneath channel lips and sliding it to a marked position; the entry route does not establish a sufficiently distinct ability. The submission tests inserting and positioning a T-nut beneath channel lips, which does not establish a sufficiently distinct manipulation capability for this benchmark.

### [#991](https://github.com/robocurve/benchmark-tasks/pull/991) — accepted after revision

2026-11-12T09:32:25Z, achyutha11:

> Not accepted (TK-JJNAU2). Scoring (not met): The submitted score function returns 0.5 for a settled 87–93 degree bend and never returns the documented full score of 1.0. Clarity and reproducibility (not met): Tube length, wall thickness and specific tempers are not specified, and the bender and springback calibration are insufficiently specified to reproduce both trial conditions. What to change: Correct the primary score so a settled 87–93 degree bend with both grippers clear returns 1.0, and verify the recorded demo against that scorer; also implement the stated one-second hold. Specify the copper tube length, wall thickness and material tempers, the bender and return spring, and how to obtain or calibrate the two stated springback conditions in real trials.

### [#994](https://github.com/robocurve/benchmark-tasks/pull/994) — not accepted; final outcome not established

2026-11-12T09:32:28Z, achyutha11:

> Not accepted (TK-T6U364). Construct validity (not met): The specified 5 × 8 mm steel legs cannot plausibly yield at 0.01 N·m, so the simulated bending resistance omits the force required by the stated real fastener. Feasibility (not met): The claimed 0.01 N·m bend resistance is incompatible with the specified steel leg cross-section, leaving completion of the real-world setup unsubstantiated. What to change: Use realistic cotter-pin dimensions, material and bending resistance that a YAM can handle, and update the simulation and fidelity note to match. Provide a full-score demo for the corrected setup within the run limit. Clarify the README's approximately 1,214-step claim and, if necessary, increase the limit to cover the demonstrated success hold.

### [#1019](https://github.com/robocurve/benchmark-tasks/pull/1019) — accepted after revision

2026-11-12T09:33:31Z, achyutha11:

> Not accepted (TK-ENT3K4). Flags: The reported demo score of 1.0 conflicts with judge returning 0.75 for full success. Scoring (not met): The judge returns 0.75 even when parked, clear and still make full success true, contradicting the documented 1.0 score. Clarity and reproducibility (not met): The board and line materials, chalk loading and line tension or elasticity are unspecified despite determining whether the line can be pinched and snapped onto the board. What to change: Change the scorer so a full-success state returns 1.0, and update the scorer test to check that result. Specify the board and cord materials, chalk loading, reel locking and the tension or elasticity needed to reproduce the snap and print with the stated dimensions.

### [#1059](https://github.com/robocurve/benchmark-tasks/pull/1059) — accepted after revision

2026-11-12T09:35:24Z, achyutha11:

> Not accepted (TK-SB7DUG). Scoring (not met): The 20-degree opening and 6-degree closing requirements can deny credit for real shoots cleanly cut with a smaller blade movement. What to change: Score real-world shoot cuts by observed severing at the specified height rather than requiring the blades to open at least 20 degrees and close to 6 degrees; those angle thresholds can remain documented as simulation approximations. Consider changing the category to Societal relatability, since hedge trimming is a familiar household gardening task.

### [#1084](https://github.com/robocurve/benchmark-tasks/pull/1084) — final rejection

2026-11-12T07:22:28Z, achyutha11:

> Not accepted: final (TK-7PJJ6N). Flags: Egregious simplification Construct validity (not met): The 6 cm hose tail and square shank with lobes 5 mm clear of its neck omit hose handling and the cam-driven gasket compression needed for a real sealed coupling. The specified square-shank mock-up does not test the central physical demands of connecting a real hose with a cam-and-groove coupling: handling the hose and using the cams to draw the adapter against a gasket. A realistic coupling and representative hose would be needed to test that real-world skill.

### [#1214](https://github.com/robocurve/benchmark-tasks/pull/1214) — accepted after revision

2026-11-12T09:42:23Z, achyutha11:

> Not accepted (TK-76T4R8). Construct validity (not met): A robot can stage a parcel on the table and return it to the belt before its pass, earning gap credit despite the keep-on-belt instruction. Scoring (not met): The scorer checks belt position only during each scanner pass, although the README says taking a parcel off the belt scores zero. What to change: Update the scoring rule and implementation to prevent off-belt staging before the scanner: score zero if a parcel is placed on another surface or carried outside the belt footprint before its first pass, while still allowing brief lifts over the belt. Add a test showing that staging a parcel on the table and returning it before scanning scores zero.

### [#1217](https://github.com/robocurve/benchmark-tasks/pull/1217) — accepted after revision

2026-11-12T09:42:25Z, achyutha11:

> Not accepted (TK-7YXG4S). Construct validity (not met): A robot can earn credit by pushing a reject onto the floor, or full placement credit by holding it stationary above the reject table. Scoring (not met): The placement test imposes no contact or lower-height requirement and explicitly rewards rejects discarded on the floor. What to change: Change the scorer so a reject counts as placed only when it is supported by the reject table, using a numeric bottom-to-surface tolerance and a release check. Remove credit for rejects deposited on the floor or held off the line, and define any partial credit around meaningful progress toward the reject table.

### [#1285](https://github.com/robocurve/benchmark-tasks/pull/1285) — not accepted; final outcome not established

2026-11-12T09:46:23Z, achyutha11:

> Not accepted (TK-AUMWWL). Scoring (not met): The 50 N threshold is inferred from fixed winding and spring behavior without a specified calibration for a real strap and ratchet. Clarity and reproducibility (not met): The strap length, ratchet and anchor geometry, and the slide and stop mechanism are insufficiently specified to reproduce the rig and jolt. What to change: Specify the strap length, ratchet and anchor geometry, and the slide, actuator and end stop needed to reproduce the setup. Provide a practical, calibrated real-world method for verifying 50 N strap tension rather than assuming each ratchet stroke winds exactly 5 mm, and describe guarding and safe operation of the 20 kg moving deck.
2026-11-14T05:32:27Z, achyutha11:

> Not accepted (TK-72ZFXG). Flags: Prior review feedback was not supplied Construct validity (not met): The strap runs horizontally around the crate at a constant 9 cm height, so it pulls the crate toward the stake board rather than restraining it down to the deck. What to change: The current strap lies horizontally around the crate and presses it toward the stake board, rather than tying it down. Route a realistic tie-down over the crate to deck anchors, update the simulation and real-rig setup, reset and scoring to match, and demonstrate full score with the revised rig.

### [#1455](https://github.com/robocurve/benchmark-tasks/pull/1455) — final rejection

2026-11-12T10:40:23Z, achyutha11:

> Not accepted: final (TK-U8D3D9). Flags: Miniaturization · Egregious simplification Importance (not met): Sliding four tabs around a block without screw adjustment, tightening, or runout measurement does not establish the stated machining skill. Construct validity (not met): The 1:3 rail-based stand-in lacks jaw screws and permits full credit with gaps rather than a securely clamped workpiece. Scoring (not met): Full credit permits 1.5 mm gaps at each jaw, so a loose block can be scored as gripped. Clarity and reproducibility (not met): A solid 4 × 4 × 8 cm steel bar weighs about 1 kg, not the specified 80 g. The printed scale model replaces independent chuck screws and secure clamping with sliding tabs, while the score allows gaps between the jaws and the block. This does not test the machining setup described; a meaningful evaluation would need an actual-scale chuck and the associated adjustment and secure-holding skill. Also correct the specified steel block mass: a solid bar of those dimensions weighs about 1 kg.

### [#1467](https://github.com/robocurve/benchmark-tasks/pull/1467) — not accepted; final outcome not established

2026-11-12T11:18:23Z, achyutha11:

> Not accepted (TK-6KMQEJ). Construct validity (not met): The modeled nose points along the housing rather than along the downward firing axis of a conventional brad nailer, and a midpoint-only trigger check can miss contact by an actual finger. Scoring (not met): The scorer checks orientation and whether the tool's center is in the case, but never checks its position against the printed outline. What to change: Use the geometry and firing direction of an actual brad nailer, and measure the pointing constraint from its firing axis. Check clearance for both physical fingers rather than only their midpoint; specify numeric position tolerances for the case outline and enforce them in the scorer. Update the demo and verify that it reaches full score under the corrected checks within the run limit.
2026-11-14T06:18:28Z, achyutha11:

> Not accepted (TK-FPKVWQ). Scoring (not met): The finger-tip calculation interprets Isaac Lab's wxyz gripper quaternion as xyzw, so it can miss trigger-clearance violations. What to change: Correct the finger-tip calculation: mech.py stores Isaac Lab's wxyz gripper quaternion in a field consumed as xyzw by nailer.py. Convert it consistently before calculating each finger's tip, add a test with a known gripper orientation, and rerun the scorer on the demo; provide a new full-score demo within 1,200 steps if the corrected check reveals a violation.

### [#1472](https://github.com/robocurve/benchmark-tasks/pull/1472) — final rejection

2026-11-12T11:02:33Z, achyutha11:

> Not accepted: final (TK-CTY366). Importance (not met): Changing a hand hacksaw blade is occasional tool maintenance, not a core regular task of general maintenance workers or machinists. Scoring (not met): The scorer gives zero for tightening by pushing the nut's wings rather than gripping and rolling them, even if the blade is properly tensioned. The task focuses on occasional hacksaw upkeep rather than a core occupational activity, and it does not establish a qualifying alternative impact domain. Its scorer also excludes legitimate wing-nut tightening by pushing the wings, even when the resulting tension is correct.

### [#1482](https://github.com/robocurve/benchmark-tasks/pull/1482) — accepted after revision

2026-11-12T11:18:29Z, achyutha11:

> Not accepted (TK-HM6KTS). Importance (not met): Emptying espresso portafilters is regular work for baristas, but not plainly a core task of the broader cook and food-preparation occupations cited. What to change: Change the category to Societal relatability and explain the familiar barista scenario. The current jobs justification does not establish that emptying espresso portafilters is a regular task for occupations totaling over 500,000 US workers.

### [#1495](https://github.com/robocurve/benchmark-tasks/pull/1495) — accepted after revision

2026-11-12T11:19:28Z, achyutha11:

> Not accepted (TK-X8UP9R). Construct validity (not met): A rod tip merely passing within 3.5 mm of the plate counts as filler even if it never enters a pool or deposits metal. Scoring (not met): Timed tool geometry is treated as a sound bead without checking actual deposition, continuity or weld defects. Clarity and reproducibility (not met): The real-world setup lacks a specified welding power source, shielding gas and a clean working portion of filler rod. Feasibility (not met): The real-world trial lacks specified arc shielding, fume extraction and heat protection for the robot and surroundings. What to change: Keep the TIG task but specify the real welding power source, shielding gas, clean unpainted filler working surface, arc enclosure, fume extraction and heat protection. Replace the geometric dab and heat proxies in the real-world score with numeric, observable criteria for deposited bead coverage and defects, including partial credit; explain how each measurement is made.

### [#1562](https://github.com/robocurve/benchmark-tasks/pull/1562) — accepted after revision

2026-11-12T11:23:25Z, achyutha11:

> Not accepted (TK-FWYCGL). Flags: The simulated spanner jaws are visual-only Scoring (not met): The unspecified real-world snug reference makes the central turn thresholds ambiguous, and the implementation awards 0.25 above the documented partial-credit range. What to change: Define how the real-world evaluator establishes and records the nut's snug position without interrupting the robot, for example with a specified calibrated force or torque threshold and a reference mark. Update the scorer so partial credit is awarded only in the documented turn range, and check that its full-score stillness and release conditions match the written rubric.

### [#1574](https://github.com/robocurve/benchmark-tasks/pull/1574) — final rejection

2026-11-12T11:26:25Z, achyutha11:

> Not accepted: final (TK-DA72NN). Importance (not met): The named food batchmakers and separating-machine operators do not together establish the 500,000-worker jobs bar, and routine sanitary-clamp assembly is not established for a larger occupation. Construct validity (not met): Overtightening permanently squeezes the gasket into the bore but can still earn 0.25. The submission does not establish that sanitary clamp assembly is a regular core task for occupations totaling over 500,000 US workers, and the specialist setting does not meet the everyday-relatability bar. The scoring also awards credit after overtightening has permanently damaged the gasket.

### [#1576](https://github.com/robocurve/benchmark-tasks/pull/1576) — accepted after revision

2026-11-12T11:26:32Z, achyutha11:

> Not accepted (TK-V3AWB8). Flags: The README gives both approximately 74 mm and 71 mm for the 50% stretch pad-gap threshold; verify and reconcile the real-world measurement. Scoring (not met): All safe intermediate progress scores zero, while returning the arms home earns credit and release tilt can disqualify an otherwise properly seated seal. What to change: Revise the primary score to award intermediate credit for safely advancing the ring toward the groove, and give full credit for a properly seated, untwisted ring without requiring the arms to return home. Judge seating by the ring's final physical condition rather than disqualifying an otherwise seated ring solely because of release angle. Reconcile the conflicting pad-gap thresholds and explain how maximum stretch will be measured in a real trial.

### [#1577](https://github.com/robocurve/benchmark-tasks/pull/1577) — accepted after revision

2026-11-12T11:26:34Z, achyutha11:

> Not accepted (TK-RL2P8S). Construct validity (not met): The demo holds the pedal at its floor stop before opening the bleeder, while the model supplies fluid at pressure without the piston moving as real bleeding requires. Clarity and reproducibility (not met): The specified 8 mm box-end wrench cannot fit the stated 12 mm bleeder hex. Feasibility (not met): The specified wrench and bleeder cannot be assembled, and the shown floor-stop-first operation does not demonstrate the corresponding real hydraulic movement. What to change: Specify a wrench that fits the bleeder hex. Revise the trainer, fluid model and demo so opening the bleeder allows the pressurized pedal and master-cylinder piston to move while fluid is expelled, then close the bleeder before the pedal returns; document the corresponding real-world rig and confirm a full-score demo within the limit.

### [#1592](https://github.com/robocurve/benchmark-tasks/pull/1592) — accepted after revision

2026-11-12T11:30:28Z, achyutha11:

> Not accepted (TK-AYVMMJ). Flags: README and ASSETS.md reference yam-arena robot and workstation assets but do not state their individual licenses. Importance (not met): Cashiers and bank tellers regularly handle money, but the submission does not establish that emptying jars and sorting loose coins into tabletop piles is their regular core work; household coin sorting is relatable. Scoring (not met): The binary score gives nine correctly sorted coins the same credit as none, despite clear measurable intermediate progress. What to change: Change the category to Societal relatability and describe the familiar household task of sorting accumulated change. Award partial credit for each coin wholly inside its correct frame, retaining full credit for all ten. List the third-party robot and workstation assets and their respective licenses in the README or a clearly linked asset inventory.

### [#1637](https://github.com/robocurve/benchmark-tasks/pull/1637) — accepted after revision

2026-11-12T11:41:34Z, achyutha11:

> Not accepted (TK-ZKUECM). Importance (not met): The instruction specifies the safety steps, leaving no hazard recognition or safety decision, although disconnect isolation can be routine for general maintenance and repair workers. What to change: The safety procedure and target are explicitly prescribed, so this does not test the safety judgment required by the selected domain. Change the domain to Impact on jobs and explain how this disconnect lockout is part of general maintenance and repair workers' routine work.

### [#1647](https://github.com/robocurve/benchmark-tasks/pull/1647) — final rejection

2026-11-12T11:57:32Z, achyutha11:

> Not accepted: final (TK-GLK4ZE). Importance (not met): The submission identifies no occupation for which adjusting this generic counterweighted service arm is regular core work, and it is not plainly a core task of general maintenance and repair workers. The submission does not establish a recognizable, regularly performed job task: the service arm and tool load are generic surrogates, and no actual equipment or occupation is identified. A benchmark task should represent a concrete real-world procedure whose importance is evident from the task itself.

### [#1703](https://github.com/robocurve/benchmark-tasks/pull/1703) — final rejection

2026-11-12T11:57:28Z, achyutha11:

> Not accepted: final (TK-HSZNSX). Importance (not met): dexhand: Remote Battery Swap already tests sliding open a battery cover, removing an AA cell, installing a replacement, and closing it; routine AA replacement is not shown to be a core job for a qualifying occupation. The task tests a battery-door opening and AA-cell replacement procedure already covered by an existing benchmark; adding a second cell and spring-return cover does not sufficiently distinguish the measured skill. The submission also does not establish battery replacement as a core activity of a qualifying occupation.

### [#1711](https://github.com/robocurve/benchmark-tasks/pull/1711) — final rejection

2026-11-12T11:59:32Z, achyutha11:

> Not accepted: final (TK-F8KB6N). Flags: Third-party source geometry license unverified Importance (not met): The custom sleeve's reversal sequence is not tied to a demonstrated regular task of electricians, general maintenance workers, or another qualifying occupation. Scoring (not met): Removing the sleeve without yet placing it in the tray earns no partial credit, while the only partial tier rewards a shorter final hold. The custom coupling's hidden reversal sequence is not established as a regular, consequential job task; the cited sensor-probe and connector analogies do not show that workers encounter this mechanism. A future submission should use a demonstrated real servicing operation rather than a custom release puzzle; also resolve and declare the source geometry's license.

### [#1733](https://github.com/robocurve/benchmark-tasks/pull/1733) — final rejection

2026-11-12T12:04:36Z, achyutha11:

> Not accepted (TK-DWT97R). Scoring (not met): The twelve 0.35–1.8 mm spring compressions are beneath the cells, with no specified noninvasive measurement method for a physical trial. What to change: Specify how to measure each terminal spring's 0.35–1.8 mm compression in the closed assembly using simple physical tools, without disturbing the result; provide any required visible indicators or measurement access in the real-world build instructions.
2026-11-14T05:39:32Z, achyutha11:

> Not accepted: final (TK-WS3H2A). Flags: Earlier review feedback for TK-DWT97R was not provided Importance (not met): Team assemblers regularly assemble products, but the submission does not establish that capturing twelve AA-cell spring contacts with a cross-key is a regular battery-pack assembly operation. The submission does not make clear that retaining a twelve-cell spring preload with this cross-key fixture is a regular battery-pack assembly operation. The task needs to measure an established, important physical assembly activity rather than relying on a specialized fixture and an asserted battery-pack context.

### [#1739](https://github.com/robocurve/benchmark-tasks/pull/1739) — not accepted; final outcome not established

2026-11-12T12:06:26Z, achyutha11:

> Not accepted (TK-ZKA642). Importance (not met): Clearing printer jams is an occasional support chore for general office clerks, and office machine operators alone do not meet the employment threshold. What to change: Please change the category to Societal relatability and explain why clearing a home or office printer jam is a familiar everyday task. Clarify the real-world card thickness and how to reproduce the jam, distinguishing them from the 3 mm rigid simulation stand-in.
2026-11-14T06:02:23Z, achyutha11:

> Not accepted (TK-U4QZVC). Flags: Prior review feedback unavailable: check whether the revision addresses it. Construct validity (not met): The real-trial setup switches the printer off and never restores power, so pressing OK cannot resume printing as claimed. Scoring (not met): The full-score condition can credit an OK press even when the specified real printer is powered off and cannot resume printing. What to change: Revise the real-world reset to restore power while preserving the jam, specifying how to handle any automatic feed or jam recovery. Require the real-trial full-score check to confirm that pressing OK actually resumes printing; retain the documented simulation approximation.

### [#1750](https://github.com/robocurve/benchmark-tasks/pull/1750) — final rejection

2026-11-12T12:08:28Z, achyutha11:

> Not accepted: final (TK-BN6RUJ). Importance (not met): Computer and office machine repairers are below the jobs threshold, and physical drive removal is not plainly regular work for computer user support specialists. The drive-removal operation is credible, but the submission does not establish it as regular work for an occupation or group of occupations totaling more than 500,000 US workers. Computer repairers alone fall below that threshold, while drive removal is not plainly a regular core duty of computer support specialists.

### [#1772](https://github.com/robocurve/benchmark-tasks/pull/1772) — final rejection

2026-11-12T12:12:31Z, achyutha11:

> Not accepted: final (TK-NGL8A3). Importance (not met): No specific equipment or regular work of an occupation such as team assemblers or general maintenance workers is identified; the storage and cooling labels alone do not establish a core job task. Construct validity (not met): The gravity-retained cooler and connector-free storage are a generic surrogate, without an identified real service procedure whose essential interfaces they preserve. The exchange is a generic mechanical fixture rather than a clearly grounded, regular job task. Develop a task around identifiable real equipment and its actual service procedure, preserving the interfaces and manipulation needed in that work.

### [#1775](https://github.com/robocurve/benchmark-tasks/pull/1775) — accepted after revision

2026-11-12T12:13:32Z, achyutha11:

> Not accepted (TK-6F54AD). Importance (not met): Refitting drawers after a move or repair is an occasional chore for movers and general maintenance workers, not plainly a core task for either occupation. Construct validity (not met): The open cabinet top permits direct top-down seating, bypassing the constrained front insertion needed in an ordinary finished cabinet. What to change: Change the domain to societal relatability and explain the familiar household situation in which a drawer is removed and refitted. Add a representative cabinet top so the drawer must be inserted through the front opening, and provide an updated full-score demonstration and setup details.

### [#1791](https://github.com/robocurve/benchmark-tasks/pull/1791) — accepted after revision

2026-11-12T17:28:29Z, achyutha11:

> Not accepted (TK-NNHJXQ). Importance (not met): Bartenders are the only named occupation, and the submission does not establish that occupations regularly performing this task exceed 500,000 US workers. Clarity and reproducibility (not met): The real-world setup omits the water supply, spray nozzle, and drainage needed to reproduce a working rinser. What to change: Change the category to Societal relatability and explain the familiar bar-service scenario. Specify the real-world rinser’s nozzle, water supply, and drainage so the setup can actually rinse the glass.

### [#1804](https://github.com/robocurve/benchmark-tasks/pull/1804) — accepted after revision

2026-11-12T17:30:33Z, achyutha11:

> Not accepted (TK-FTE3XJ). Scoring (not met): Zeroing the entire trial for lifting the crate more than 3 cm or tilting it over 20 degrees penalizes legitimate ways to set it up. What to change: Remove the automatic zero for lifting the crate more than 3 cm or tilting it over 20 degrees: a robot can use these motions while successfully setting up the crate. Retain the final-state checks and any justified failure conditions for falling or damage.

### [#1813](https://github.com/robocurve/benchmark-tasks/pull/1813) — not accepted; final outcome not established

2026-11-12T18:23:31Z, achyutha11:

> Not accepted (TK-C29VVQ). Flags: README reports both 3,016 and 2,814 demo steps; confirm which applies to the submitted video. Importance (not met): Most people do not know oxygen-regulator fitting firsthand, but supporting home oxygen users has a credible large-scale health impact under Other. Scoring (not met): A safe temporary set-down or cylinder movement over 1 cm permanently scores zero even if the regulator is correctly installed. What to change: Change the domain to Other and explain the task's direct impact on independence and care for home oxygen users. Revise scoring so a safe temporary set-down or harmless cylinder repositioning does not erase credit for a correct installation; retain penalties for actual drops or unsafe outcomes. Clarify the demo step count and provide the final pin-depth and clamp-torque evidence.
2026-11-14T06:17:25Z, achyutha11:

> Not accepted (TK-J47DDB). What to change: The domain, scoring changes and demo step count address the earlier feedback. Please include the submitted demo's result.json or equivalent recorded scorer output showing both final pin depths and clamp torque, so the claimed full score can be verified.

### [#1819](https://github.com/robocurve/benchmark-tasks/pull/1819) — final rejection

2026-11-13T09:39:31Z, achyutha11:

> Not accepted: final (TK-X7GDKV). Construct validity (not met): The invented spring-held vent lock clears as soon as the button is pressed rather than preventing opening until pressure has fallen. Scoring (not met): The scorer does not require steam release to finish before the lid is lifted, allowing a gripper outside the plume to open it prematurely. The proposed vent button mechanically unlocks the lid while steam is still being released, and the score does not require depressurization before opening. This does not test the essential safety behavior of a pressure cooker, whose lid must remain locked until the pressure is safe. This task doesn’t meet the importance bar, so it can’t be revised, and this pull request is now closed. You’re welcome to submit a different task in a new pull request.

### [#1910](https://github.com/robocurve/benchmark-tasks/pull/1910) — final rejection

2026-11-13T23:43:30Z, achyutha11:

> Not accepted: final (TK-2CQX43). Importance (not met): Loading boats for a specialist materials-research furnace is not shown to have impact comparable to the benchmark's domains, and automating materials research is not the specified AI-timelines domain. Construct validity (not met): The 58 mm-bore caps on a 50.8 mm tube have no specified seals or gas connections, so they cannot leave the tube sealed for CVD. The task focuses on a specialist materials-research procedure without establishing impact at the scale required for the selected domain. The specified oversized caps also lack seals and gas connections, so the resulting assembly cannot be sealed for the CVD process described.

### [#1913](https://github.com/robocurve/benchmark-tasks/pull/1913) — final rejection

2026-11-13T23:43:37Z, achyutha11:

> Not accepted: final (TK-9WBVGU). Flags: Miniaturization Importance (not met): Restaurant cooks and food preparation workers handle baking trays, but the 24 cm rack substitutes for a roughly 1.8 m rack in a task centered on restraining its motion. Construct validity (not met): The 6 kg rack on low-friction sliding feet does not preserve the mass, reach and caster behavior of the 20–30 kg wheeled rack being modeled. Scoring (not met): The scorer measures pan depth from the rack’s nominal start, so a rack displaced nearly 40 mm can yield full credit with the pan well short of the actual rear stop. The miniature rack and sliding feet do not preserve the forces, reach and caster behavior involved in bracing a full-size rolling rack. Also, measure pan insertion relative to the rack’s actual position rather than its starting position, so a displaced rack cannot make a short insertion appear complete.

### [#1914](https://github.com/robocurve/benchmark-tasks/pull/1914) — final rejection

2026-11-13T23:44:25Z, achyutha11:

> Not accepted: final (TK-49K7DX). Flags: Miniaturization Importance (not met): Hand laborers and material movers handle freight, but this 1.2 kg tabletop stand-in does not establish the skill needed to handle the much larger drums claimed in the job context. Construct validity (not met): Replacing a 200 L drum with an empty 4 L drum changes the required reach and forces, while the scorer forbids lifting and tipping that may be part of real drum handling. Scoring (not met): The score permanently zeros incidental rail contact before the bar and only requires a past bar touch, allowing a final position short of the stated resting-against-bar goal. The small, empty tabletop drum does not preserve the force and reach demands of handling the full-size freight drums described in the context. The scoring also penalizes incidental rail contact and does not require the drum to remain against the back bar at the end.

### [#1915](https://github.com/robocurve/benchmark-tasks/pull/1915) — final rejection

2026-11-13T23:44:29Z, achyutha11:

> Not accepted: final (TK-SH8HFG). Flags: Egregious simplification Construct validity (not met): Four thick rectangular blocks, a rigid steel bar with end grips, and a flush pan do not reproduce sweeping broken ceramic into a dustpan. Scoring (not met): The permanent zero for more than 8 degrees of head yaw penalizes a successful cleanup for an otherwise irrelevant tool orientation. The setup tests pushing thick rectangular blocks with a custom steel bar onto a flush area rather than collecting broken ceramic with an actual cleaning tool and dustpan. Thin irregular fragments, the tool edge, and the dustpan lip are central to the real cleanup skill, so the current stand-ins do not support the claimed task.

### [#1918](https://github.com/robocurve/benchmark-tasks/pull/1918) — final rejection

2026-11-13T23:44:35Z, achyutha11:

> Not accepted: final (TK-PVTFHM). Flags: Difficulty isn't robotic Importance (not met): The cracked-cup choice can be tested from an image, while placing and retrieving the mug reproduces ordinary RoboCasa: coffee setup mug and coffee serve mug skills. The task's distinctive safety decision is identifying a cracked mug, which can be assessed visually without robotic manipulation. The remaining actions are ordinary mug handling and coffee service, so the task does not establish a distinct safety-focused robotic ability.

### [#1921](https://github.com/robocurve/benchmark-tasks/pull/1921) — final rejection

2026-11-13T23:45:30Z, achyutha11:

> Not accepted: final (TK-N67533). Importance (not met): Loading and playing a vinyl record is a hobbyist activity rather than an everyday scenario most people know firsthand. The task demonstrates precise handling, but vinyl playback is a niche hobby rather than an everyday scenario most people know firsthand, so it does not meet the societal relatability bar.

### [#1922](https://github.com/robocurve/benchmark-tasks/pull/1922) — final rejection

2026-11-13T23:45:26Z, achyutha11:

> Not accepted: final (TK-H2QVMV). Importance (not met): BEHAVIOR-1K: make a sandwich already requires covering bread slices with spreads using a table knife, testing the same core manipulation. The core task is spreading a food topping over bread with a knife, an ability already represented in existing benchmarks. Changing the topping, bread softness or coverage threshold does not make the manipulation sufficiently distinct.

### [#1925](https://github.com/robocurve/benchmark-tasks/pull/1925) — final rejection

2026-11-13T23:45:34Z, achyutha11:

> Not accepted: final (TK-6Z2YW3). Flags: Variant of TK-U3S7ZZ , submitted earlier by the same team Importance (not met): Cleaning a fibre connector and mating it is relevant to data-center work, but the same team previously submitted the same wipe-then-connect ability. The task repeats the previously submitted fibre-connector cleaning and insertion idea. A different cleaning tool, connector size and latch do not change the core ability being evaluated; a new submission would need to test a meaningfully different skill.

### [#1926](https://github.com/robocurve/benchmark-tasks/pull/1926) — final rejection

2026-11-13T23:46:25Z, achyutha11:

> Not accepted: final (TK-NKL23K). Flags: Miniaturization Importance (not met): The scaled cutout and short stick do not test the full-size reach, clearance, and force required for safe live-line operation. Construct validity (not met): The 15 cm keep-out and 6 N latch replace an approximately 65 cm approach distance and a specified 30–40 lb pull on the real cutout. Scoring (not met): The real-trial side-view keep-out check can penalize an arm outside the three-dimensional 15 cm zone when it is displaced along the camera axis. The half-scale cutout, 15 cm clearance, short stick, and 6 N latch do not preserve the reach, safety clearance, and force demands of operating a real distribution cutout. This changes the core skill too substantially for the proposed evaluation.

### [#1928](https://github.com/robocurve/benchmark-tasks/pull/1928) — final rejection

2026-11-13T23:45:38Z, achyutha11:

> Not accepted: final (TK-CF727K). Flags: Miniaturization Importance (not met): The 20 cm standoff replaces a roughly 8 ft firefighting distance, changing the reach and spray-control skill the safety task is meant to measure. Construct validity (not met): The 1.05 kg trainer uses an 8 N seal and 6–12 N lever instead of the substantially heavier unit and forces cited for real extinguishers. The extinguisher scenario is recognizable, but the table-scale fire and standoff, together with substantially reduced extinguisher weight and operating forces, do not test firefighting at the reach, spray distance and physical loads of the real task.

### [#1934](https://github.com/robocurve/benchmark-tasks/pull/1934) — final rejection

2026-11-14T06:22:31Z, achyutha11:

> Not accepted: final (TK-M836GH). Importance (not met): General maintenance and repair workers perform lockout/tagout, but leaving a freely removable bar in a custom fixture is not the protective lockout their work requires. Construct validity (not met): The specified device has no lock or equivalent restraint against removal, so completing it does not lock out the valve. The fixture leaves a freely removable bar rather than applying a secure lockout, so the completed task does not represent the isolation procedure described. A meaningful lockout task would need to use and secure an appropriate lockout device rather than treating an unsecured retaining bar as a lock.

### [#1937](https://github.com/robocurve/benchmark-tasks/pull/1937) — final rejection

2026-11-14T06:23:25Z, achyutha11:

> Not accepted: final (TK-P6CQMW). Flags: Difficulty isn't robotic · The simulator scorer checks latch flags immediately rather than verifying the specified one-second released, flush state. Importance (not met): RoboCasa: reset cabinet doors also asks the robot to close open cabinet doors, while the push-to-open latch changes the component rather than the manipulation. The task reduces to closing open cabinet doors, an existing benchmark ability; the push-to-open latch and visual choice of which doors to press do not add a distinct physical skill.

### [#1940](https://github.com/robocurve/benchmark-tasks/pull/1940) — final rejection

2026-11-14T06:23:28Z, achyutha11:

> Not accepted: final (TK-W6N3Z6). Importance (not met): Nursing assistants routinely clear footrests for transfers, but parking the removed hanger above its pin on a custom stop is not established as a routine job step. Construct validity (not met): The horizontal hanger and custom stop keep the lifted footrest centered over its pin instead of requiring the free removal and handling used to clear a wheelchair. Clarity and reproducibility (not met): The keeper and parking stop lack the physical geometry needed to reproduce the stated real-world mechanism. The task's full-score behavior uses a custom parking stop above the hinge rather than the way a wheelchair footrest is normally removed and set aside for a transfer. The horizontal stand-in and unspecified keeper and stop do not establish that the task measures that real-world skill.

### [#1953](https://github.com/robocurve/benchmark-tasks/pull/1953) — final rejection

2026-11-14T06:25:26Z, achyutha11:

> Not accepted: final (TK-TE6M37). Flags: Duplicate of TK-V7P9X9 , an earlier task by another team Importance (not met): Stockers and order fillers regularly unpack deliveries, but the earlier parcel-opening task already tests cutting a taped carton seam with a cutter. The task's central skill is cutting open a taped carton; the additional end cuts and placement of one item do not establish a sufficiently distinct ability for the benchmark.

### [#1954](https://github.com/robocurve/benchmark-tasks/pull/1954) — final rejection

2026-11-14T06:25:29Z, achyutha11:

> Not accepted: final (TK-TKYHZT). Flags: Duplicate of TK-FENWPS , an earlier task by another team Importance (not met): The same utility-knife retraction and safe tray storage skill is already covered by an earlier pending task. Construct validity (not met): A robot can earn 0.25 by leaving the exposed blade on the holder, contrary to the stated safety purpose. Scoring (not met): Full credit requires only 22.5 mm of a 25 mm retraction, potentially leaving 2.5 mm of blade exposed. Clarity and reproducibility (not met): The setup places the blade at y=-12 to -6.5 cm, whereas the code places it at y=-32 to -26.5 cm. The task does not test a sufficiently distinct ability for this benchmark: retracting a utility-knife blade and stowing the knife is already covered. The scorer also permits full credit before complete retraction and awards partial credit for leaving the exposed blade on the holder; the written blade coordinates do not match the implemented geometry.

### [#1955](https://github.com/robocurve/benchmark-tasks/pull/1955) — final rejection

2026-11-14T06:25:32Z, achyutha11:

> Not accepted: final (TK-9NRSQL). Flags: Difficulty isn't robotic · Resubmission of TK-4844AZ ; earlier feedback not supplied Importance (not met): The patient-safety distinction is deciding to separate the brick and medication, which can be tested without a robot, while stacking the parts and pressing the lid are ordinary manipulation. The distinctive challenge is choosing a safe packing order, while the physical work is ordinary stacking and lid closure. The task does not test a sufficiently distinctive robotic safety skill; a buffer alone also does not demonstrate safe transport temperatures.

### [#1962](https://github.com/robocurve/benchmark-tasks/pull/1962) — final rejection

2026-11-14T06:26:28Z, achyutha11:

> Not accepted: final (TK-WH73A2). Importance (not met): Shucking oysters at a raw bar is a specialist scenario that most people do not encounter firsthand, and it is not regular work for the broader restaurant-cook or food-preparation workforce. The oyster-shucking procedure is a specialized raw-bar skill rather than a scenario most people encounter firsthand, and the submission does not establish impact at the program's jobs threshold.

### [#1974](https://github.com/robocurve/benchmark-tasks/pull/1974) — final rejection

2026-11-14T06:27:27Z, achyutha11:

> Not accepted: final (TK-CW6WRS). Flags: Egregious simplification Importance (not met): Machinists and CNC machine-tool operators clear chips regularly, but pushing eight cubes around an unclamped block is not representative of that work. Construct validity (not met): The real-world setup substitutes 15 mm cubes and a rectangular bar for irregular swarf and a suitable chip-cleaning tool, changing the core removal skill. Scoring (not met): An overhead video alone cannot reliably verify the specified 4 mm lift and 5-degree tipping limits, especially under gripper occlusion. The task as specified sweeps large cubes with a rectangular bar around an unclamped block; this does not capture the physical skill or normal practice of clearing machining swarf. A representative evaluation would need real chip geometry, an appropriate cleanup tool, and a credible workholding scenario.

### [#1978](https://github.com/robocurve/benchmark-tasks/pull/1978) — final rejection

2026-11-14T06:28:26Z, achyutha11:

> Not accepted: final (TK-6FM6XS). Importance (not met): Window cleaning is regular work for janitors and cleaners, but humanoidbench: Manipulation · Window already tests wiping a window with a handheld tool using vertical strokes. The central ability—wiping an upright window with a handheld tool—is already covered by an existing benchmark task. The wet-cell scoring and blade-wiping step do not make the core manipulation sufficiently distinct.

### [#1979](https://github.com/robocurve/benchmark-tasks/pull/1979) — final rejection

2026-11-14T06:28:29Z, achyutha11:

> Not accepted: final (TK-9X6DDX). Flags: Duplicate of TK-QJG5HT , an earlier task by another team Importance (not met): Heavy truck drivers regularly couple trailer air lines, but this repeats an earlier glad-hand coupling task with a second colour-coded pair. The task does not test a sufficiently distinct ability: connecting a second colour-coded air line repeats the same glad-hand coupling skill.

### [#1983](https://github.com/robocurve/benchmark-tasks/pull/1983) — final rejection

2026-11-14T06:28:36Z, achyutha11:

> Not accepted: final (TK-LV69CL). Flags: Egregious simplification Importance (not met): Recovering filter cake is not established as a core task shared by over 500,000 US workers, and the pictured activity is merely pushing loose cubes off a block. Construct validity (not met): A solid porcelain block, free cubes and fixed guide walls remove the filter media, adhesion and crumbling central to scraping a real filter cake. The task reduces filter-cake recovery to pushing loose cubes off a porcelain block; it omits the filter medium and the adhesion, crumbling and collection challenges of the real work. The submission also does not establish that this is a core job activity for occupations totaling over 500,000 US workers.

### [#1988](https://github.com/robocurve/benchmark-tasks/pull/1988) — final rejection

2026-11-14T15:14:26Z, achyutha11:

> Not accepted: final (TK-G2JDJY). Flags: Duplicate of an earlier task by another team Importance (not met): Automotive service technicians routinely replace cabin filters, but the same glovebox-stop release and filter replacement were submitted earlier by another team. This task tests the familiar glovebox-stop release and cabin-filter replacement sequence without establishing a distinct physical skill; adding the glovebox return does not make the task sufficiently novel.

### [#1993](https://github.com/robocurve/benchmark-tasks/pull/1993) — final rejection

2026-11-14T15:15:25Z, achyutha11:

> Not accepted: final (TK-AFU3DK). Importance (not met): Reattaching a delta printer arm is specialist printer maintenance, not the robot building or data-center work required by the chosen domain, and the task does not clearly meet another domain's bar. The task demonstrates a spring-loaded printer repair, but its connection to robot building is indirect: maintaining a printer that could produce robot parts is not itself robot construction. The specialist maintenance scenario also does not clearly meet another impact domain's bar.
