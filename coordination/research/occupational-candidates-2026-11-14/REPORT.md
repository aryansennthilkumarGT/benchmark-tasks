# New occupational candidates: evidence and elimination round

Research date: 2026-11-14 UTC. Research branch: `research/next-occupational-candidates`.

These are researched task proposals, not implemented or GPU-qualified tasks. This branch leaves the running Brev sprint, its budget, coordinator pins, task sources, pending PR #1733 and rejected submission heads untouched. No official submission was created.

## Recommendation

Advance **double-stud L-track cargo-anchor connection** first for detailed geometry and gripper-access investigation. Keep **scroll-chuck jaw setup** second and **RIDGID quick-opening die-head setup** third. They have identifiable equipment and documented operations, and test different mechanisms. None has unconditional novelty or acceptance clearance.

| Priority | Operation and useful endpoint | Distinct physical ability | Principal unresolved risk |
|---|---|---|---|
| 1 | Connect a double-stud cargo fitting to its logistic rail; leave a usable, locked tie-down anchor | Two-disc simultaneous insertion, undercut translation, independent release-clip locking against reverse travel | Clip access with stock fingers; distinction from earlier undercut/latch mounting tasks; exact same-product geometry |
| 2 | Configure a scroll chuck's removable jaws for the requested workpiece, then verify concentric closure | Sequential engagement of independently loose jaw teeth with one shared scroll | Fine contact fidelity; running torque and grasp access; production-setup importance and PR #400 boundary |
| 3 | Install a matched numbered die set and set an 811A quick-opening head for the requested pipe size | Four radial tools captured and positioned by a shared setting mechanism | Exact internal geometry; clamp operation; setup alone must not imply a verified usable thread |

These rankings prioritize an important outcome, authentic mechanical constraints, original scoring possibilities and manageable robot motions. They are qualitative research judgments, not estimated acceptance probabilities or measured runtimes.

## 1. Double-stud L-track cargo-anchor connection

**Actual procedure.** US Cargo Control's own product page for SKU **1519-DSR**, a double-stud fitting with pear link, instructs the operator to lift the end clip, insert the two lower discs into rail slots, slide halfway between openings, and release the clip to lock. This establishes a specific insertion/translation/locking operation; it does not establish undocumented spring geometry or actuator force.

- [Product and installation procedure](https://www.uscargocontrol.com/products/double-stud-fitting-w-pear-link)
- [Supplier's L-track installation/use guide](https://www.uscargocontrol.com/collections/How-to-Use-and-Install-L-Track-and-L-Track-Systems)
- [Ancra 50362-11 commercial double-stud fitting](https://ancracargo.com/double-stud-track-fitting-round-ring)

Ancra independently establishes that commercial double-stud fittings provide a connection between tie-down assemblies and aircraft logistic track. Its **round-ring 50362-11 is a different product** from the US Cargo Control pear-link fitting. Do not transfer mass, load rating, release mechanism or dimensions between them. Ancra lists rounded mass values of 0.1 kg and 0.3 lb; those are not precision measurements. The page's working-load rating is not evidence that a simulated fixture withstands that load. US Cargo Control's page does not supply the complete dimensional drawing needed for a hardware replica.

**Occupational importance.** O*NET 53-3032.00 explicitly lists securing cargo using ropes, blocks, chain, binders or covers, and inspecting cargo securement. BLS lists **2,221,200 heavy and tractor-trailer truck-driver jobs in 2025**. This supports cargo connection as core work; it does not mean every driver uses this particular fitting. The task should end with a mechanically usable anchor, not merely put a loose accessory at a colored mark.

- [O*NET duties](https://www.onetonline.org/link/summary/53-3032.00)
- [BLS occupation and employment](https://www.bls.gov/ooh/transportation-and-material-moving/heavy-and-tractor-trailer-truck-drivers.htm)

**Nearest comparisons.** [PR #770](https://github.com/robocurve/benchmark-tasks/pull/770) inserts, turns and positions a T-nut under profile lips. [PR #939](https://github.com/robocurve/benchmark-tasks/pull/939) was rejected as duplicating that capability despite a different entry route. Accepted `din-rail-mount` hooks a module over one rail edge and pivots a spring latch over the other. Accepted `bayonet-mate` captures lugs by axial insertion and rotation. These are substantive neighbors, not irrelevant title matches.

The proposed difference must reside in the two-disc capture and independent keeper that prevents translation back to the extraction openings. A new cargo label, an added hook, or a different entry direction alone would not establish novelty. Keyword searches for L-track, E-track, double stud, stud fitting, logistic and lashing found no exact named PR, but that is only a scoped absence result.

**Robot and scene concept.** Use full-size rail and fitting, with the rail fixed to an explicitly reproduced mounting plate. Keep the fitting loose; model both lower discs, rail apertures/undercuts, keeper and actual release travel. One hand handles the fitting while the other manipulates the release interface if needed. First verify stock fingertip access to the real end clip: no invented handle or enlarged clip passed off as OEM hardware. This is likely the shortest action sequence of the three, but neither action count nor runtime has been measured.

**Scoring concept.** Measure actual under-lip capture of both studs, keeper seating, absence of an unobstructed release path, hands-clear retention and a reproducible modest pull check. Reject damage, prying the rail off its mounting, incomplete second-stud capture, fingers supporting the fitting, and a keeper resting on top rather than engaged. The proof load would be a disclosed benchmark check calibrated with a spring scale, not the manufacturer's rated cargo load. Choose numerical tolerances only after selecting and documenting the geometry. Do not require one prescribed hand sequence when another valid strategy works.

**Before implementation:** select one exact fitting/rail pair; obtain a drawing or clearly declare authored interface geometry; establish keeper travel and grasp access; resolve semantic novelty against the named neighbors and the signed-in board. If the keeper adds no consequential distinct skill, reject the candidate rather than enlarge the sequence.

## 2. Scroll-chuck jaw setup and concentric-closure check

**Actual procedure.** Röhm's operating instructions **DC0000364**, printed/PDF page **17**, explicitly require jaw insertion in sequence **1–2–3 while turning the scroll**, with the embossed numbers facing outward and the correct inward/outward stepped-jaw arrangement. This supports jaw-to-scroll phase engagement, not an arbitrary memorized order invented by a scorer.

- [Röhm manufacturer's operating manual](https://www.roehm.biz/fileadmin/products/media/en/DC0000364.PDF)
- [Manufacturer manual index, identifying this as ZG/ZS, ZGU/ZSU, EG/ES geared scroll chucks](https://www.roehm.biz/en/downloads/operating-instructions/)
- [Manufacturer lathe-chuck catalog](https://www.roehm.biz/fileadmin/user_upload/produkte/PG3_Handspannfutter/en_03_Lathe_chucks_Innenteil_250703.pdf)

The manual includes actual chuck families and gripping-range tables. The catalog covers several different mechanisms, including DURO-M scroll and DURO key-bar designs: do not combine their parts or dimensions. The first downloaded DC0000324 was a **face-driver manual**, not jaw-installation evidence; it is excluded from the source manifest for this candidate. No inferred dimension is a manufacturer measurement.

**Occupational importance.** O*NET lists aligning/securing holding fixtures for machinists, and mounting/alignment of tools, fixtures and workpieces for CNC tool operators. Current sources report **288,300 machinists + 170,000 CNC tool operators + 56,700 tool-and-die makers = 515,000 jobs in 2025**. These are distinct occupation counts. The qualifying activity must be routine production workholding setup for a different requested workpiece, not occasional cleaning or tool repair. The employment sum alone does not establish that every member regularly changes manual scroll jaws.

- [Machinists](https://www.onetonline.org/link/summary/51-4041.00)
- [CNC tool operators](https://www.onetonline.org/link/summary/51-9161.00)
- [Tool-and-die makers](https://www.onetonline.org/link/summary/51-4111.00)
- [BLS machinists/tool-and-die makers](https://www.bls.gov/ooh/production/machinists-and-tool-and-die-makers.htm)

**Nearest comparisons.** [PR #400](https://github.com/robocurve/benchmark-tasks/pull/400), head `50c4c790cbb65653161a041b129eb10fd493d1cd`, already has installed jaws on radial slides coupled to a pinion; its task is bar clamping and key removal/stowage. Its README and task source were read. The proposed task must actually start with independently removable jaws and make phase engagement determine closure, rather than repeat bar clamping with an extra token step.

[PR #1455](https://github.com/robocurve/benchmark-tasks/pull/1455) was finally rejected for a miniature four-jaw stand-in lacking the claimed screws/tightening/runout. [PR #645](https://github.com/robocurve/benchmark-tasks/pull/645) was finally rejected because its supposed soft-jaw workholding was loose object placement in a permanently open fixture. [PR #1472](https://github.com/robocurve/benchmark-tasks/pull/1472) also warns that occasional blade maintenance is not a core job task. These failures rule out passive tabs, pretend workholding and maintenance-based importance padding.

**Robot and scene concept.** Anchor a real-size chuck assembly; provide actual removable jaws and its key. Keep the machine unpowered. Model scroll teeth, jaw teeth, radial guides and meaningful engagement depth. One arm presents a jaw while the other indexes the key. Choose a real chuck size after checking jaw/key grasp geometry and free-running effort. Maximum tightening torque, maximum clamping force and moving jaw mass must not be guessed from the chuck outside diameter. No claim of full machining-load clamping is appropriate for a light closure check.

**Scoring concept.** Check engagement and concentric closure using a documented gauge/workpiece and dial-indicator or caliper procedure. A jaw inserted one scroll pitch out of phase must fail the physical check. Permit valid cyclic permutations or alternative manipulation orders if they produce the correct physical assembly; do not simply reward a hard-coded 1–2–3 event log. Require release and stillness, and detect unsupported or incompletely engaged jaws. If the endpoint includes actual workpiece holding, use a calibrated retention check rather than an arbitrary required number of turns after contact, the problem already identified on #400.

**Before implementation:** select one matching manual/catalog family; establish tooth/guide geometry and torque; verify actual loose-jaw contacts can represent wrong-phase engagement; settle whether this differs enough from #400 and the team's ER task. Keep the production-setup importance claim conditional until this narrower scope is defensible.

## 3. RIDGID 811A quick-opening die-head size setup

**Actual procedure.** RIDGID **300 Compact/1233 operator's manual, 999-998-098.10_REV C, printed page 9 (PDF page 11)** describes quick-opening die-head setup, including model **811A**:

1. Face the head's numbers upward and move the throwout lever to OPEN.
2. Loosen the clamp lever approximately three turns.
3. Lift the washer tongue from the size-bar slot and move the washer to the slot end.
4. Insert a complete matched set of appropriate dies, numbered edge up, with each indicator line flush with the head edge and die numbers corresponding to slot numbers.
5. Align the link index with the requested size mark, adjusting insertion as necessary. The washer tongue belongs in the slot to the left.
6. Tighten the clamp lever.

These are manufacturer steps, unlike the earlier speculative idea of moving past a generic CHANGE DIES mark. That speculative description is not used. The manufacturer also states: **always cut a test thread after changing/adjusting dies**. A setup-only task stops before that powered verification and cannot claim correct finished threads, leak tightness or production readiness.

- [Manufacturer machine page and manuals](https://www.ridgid.com/us/en/300-compact-threading-machine)
- [Exact operator manual](https://cdn2.ridgid.com/resources/media?key=06e6774f-b369-441e-8f82-1004e013cbf3&languageCode=en&type=document)
- [Manufacturer parts list](https://cdn2.ridgid.com/resources/media?key=65d57a77-6f33-48df-bdf6-a98ff62b807b&languageCode=en&type=document)

**Occupational importance.** O*NET 47-2152.00 explicitly lists cutting/threading pipes with pipe threaders. BLS lists **510,600 plumbers, pipefitters and steamfitters in 2025**. This supports pipe-threading setup within a qualifying occupation; it does not establish the frequency of this exact die change. The meaningful scope is a matched tooling setup for a requested pipe size during work, not arbitrary machine maintenance.

- [O*NET](https://www.onetonline.org/link/summary/47-2152.00)
- [BLS](https://www.bls.gov/ooh/construction-and-extraction/plumbers-pipefitters-and-steamfitters.htm)

**Nearest comparisons.** Searches for die head, diehead, chaser, dies and threading found no exact die-head setup. [PR #936](https://github.com/robocurve/benchmark-tasks/pull/936) concerns cutting with a two-hand tap wrench, while [PR #1562](https://github.com/robocurve/benchmark-tasks/pull/1562) makes a compression pipe joint. Those are not this tooling setup, but their full implementations have not been reviewed here. Generic block insertion and RoboDojo fastening remain important external neighbors if the shared die-setting mechanism is simplified away.

**Robot and scene concept.** Use the full-size head on a stable, reproduced support. Begin with the empty head already open and released if selecting the installation-only subset; disclose this prepared state. Provide the actual matched four-die set. Implement the radial guides, engagement/capture mechanism, washer tongue, size bar and clamp as physical interfaces. The printed exploded diagram does not by itself establish precise internal dimensions or a force curve. Do not replace the four dies with ordinary blocks permanently constrained into slots, or give a fake powered cam permission to seat them.

**Scoring concept.** Check each die's real seating depth/orientation and number-slot correspondence, tongue engagement, physical retention through normal open/close travel, selected size setting and hands-clear stability. Wrong-numbered dies can fit mechanically yet cut the wrong thread, so geometric closure alone must not certify a good thread. In the bounded setup task their documented identity matters, but an artificial rule that destroys a die for a nonstandard insertion order would be invalid. Numeric inspection tolerances must be specified after the geometry is established. No cutting-force, pitch accuracy, torque or leakage evidence is claimed.

**Before implementation:** establish the actual 811A cam/die interfaces and dimensions from further documentation or explicitly authored geometry; prove stock-gripper clamp access; make a defensible case that the bounded setup is consequential despite the required subsequent test cut. This has more documentation and action-count risk than L-track.

## Ideas eliminated or demoted in this round

| Idea | Evidence and decision |
|---|---|
| Two-wrench pipe-union release | #798 finally rejected as a variant of an earlier pipe-union ability. Adding self-energizing wrench mechanics would require a genuinely different task, not this repeat. Excluded. |
| Tri-clamp / cosmetic V-band substitute | #1574 finally rejected for importance and damaged-joint partial credit. No V-band title hit does not make a reskin novel. Excluded. |
| Quarter-turn strut nut | #939 duplicate finding against #770; #770 also finally rejected for importance and stopping before mounting a useful component. Excluded. |
| Oxygen regulator installation | Earlier open #1813. Excluded. |
| Two-pin fluorescent tube | Earlier #175 already tests socket insertion and turning into detents; revision requested for hands-clear retention. Excluded even though the word fluorescent had zero hits. |
| Hacksaw blade installation | Exact #1472, final importance rejection. Excluded. |
| Espresso portafilter setup | Earlier #665 and #1482. Excluded. |
| Pressure-cooker vent/open | Earlier #1816, #1817, #1819 and other pressure-cover tasks. Excluded. |
| Industrial rectangular lever-lock connector | No Harting brand hit, but the rubric rejects changing only connector type; accepted #1540 and multiple connector tasks are close. Demoted, not a recommended build. |
| Ratchet chain binder / turnbuckle | No exact name hit, but #1285 already tests cargo tensioning/ratchet securement. Added tool or chain alone is insufficient; real forces and reproduction remain unresolved. Demoted. |
| Concealed hinge / cabinet mounting | Numerous door/hinge tasks, including #166, #989 and #1865. No verified sufficiently different operation. Demoted. |
| Toy container twistlocks | #1323 explicitly rejected miniature mass/forces/reach and missing lifting equipment. Excluded; full-size small fittings are not equivalent to scaling an entire cargo operation down. |
| Arbitrary multistage coupling puzzle | #1711 rejected lack of a demonstrated regular operation. Excluded. |

## Scope and remaining uncertainty

- Refreshed official main: **a0afa6cddddcc4e154a8b662a8603af8d75a4a83**, **94 accepted task folders**. This is newer than the earlier 92-task forensic snapshot.
- Saved **67 GitHub keyword search responses**, with returned PR records and raw-response hashes, and **16 actual PR/comment snapshots**. At least one exact duplicate was found only with alternate wording (lamp tube), illustrating why zero brand-name hits are insufficient.
- Read #400 source/README, #770 metadata and #1285 metadata/README; read the relevant accepted rail/bayonet/latch/camera metadata. Do not describe every search hit as a code review.
- Screened all **1,018 current BEHAVIOR-1K BDDL definitions** at `b544acbbb76b461349bcba21f93b870b11da6608` for the recorded literal mechanical terms; no hits. This is a content screen, not proof of semantic uniqueness.
- Inventoried pinned LIBERO, RoboCasa and RoboDojo trees; additionally read RoboDojo `FastenScrews`, `InsertKey`, `InsertTubes` and `PlugInCharger` reward/task sources. Fine physical mechanisms differ from those definitions, but complete semantic coverage of all suites has not been established.
- The board host is reachable with a normal browser User-Agent, but returns a **sign-in page**, not the authenticated task catalog. A default urllib request still received 403. No credentials were requested or sign-in attempted. Signed-in pending-task coverage, DataCenterBench and complete SimplerEnv coverage remain unavailable in this round.
- The primary-source manifest records actual retrieval hashes. No physical hardware was measured. No proposal has scene assets, native physics, expert success, Dream-1 evidence, media or submission qualification from this research round.

The next productive step is the **same-product L-track dimensional/clip-access investigation**, followed by comparison against the signed-in board before investing in a scene. If that cannot establish a distinct, usable cargo-connection operation, switch to the documented scroll-jaw setup rather than invent another latch puzzle.
