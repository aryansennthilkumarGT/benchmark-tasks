# PR1733: appeal evidence and limited factual clarification

**Current conclusion: a substantive importance appeal remains weak.** No independently read source establishes that the exact or materially equivalent twelve-AA-cell pressure-plate/cross-key closure is regular core battery-assembly work. The proposed patents are leads, not verified appeal evidence. Nothing has been posted, amended or resubmitted.

## Decision, chronology and deadline

[PR1733](https://github.com/robocurve/benchmark-tasks/pull/1733) final head: `a312bcac0f29098731ad40ce30df5fe3a6fcca78`. Read-only fetch and source inspection confirm:

| Time (UTC, from Git/comments) | Event |
|---|---|
| Nov12 12:04:36 | TK-DWT97R not accepted: twelve0.35–1.8mm hidden spring compressions lack specified noninvasive physical measurement. |
| Nov12 12:18:17 | Commit6ff8f739ea5df53a89af198310d202c2d6a1f395 adds the physical measurement design. |
| Nov12 12:19:00 | Intake rejects fidelity note over500characters. |
| Nov12 12:21:56 | a312bcac shortens fidelity; final submitted head includes measurement document. |
| Nov12 12:22:24 | Revised TK-WS3H2A received. |
| Nov14 05:39:32 | Final rejection: regular use of the twelve-AA-cell cross-key operation not established; flag says earlier review feedback was not provided. |

The posted final decision offers48hours for a human-review request. On that wording, the nominal deadline is **November16,2026 at12:39:32a.m. Eastern (05:39:32UTC)**. This is arithmetic from the preserved comment, not confirmation of an extension or later moderator action. No comment was posted by the agent.

## Submitted code versus claimed procedure

[scene.json](https://github.com/aryansennthilkumarGT/benchmark-tasks/blob/a312bcac0f29098731ad40ce30df5fe3a6fcca78/tasks/twelve-cell-pack/scene.json) describes original primitive geometry: fixed holder, twelve independent spring-contact shoes, twelve already-loaded cylindrical cell surrogates, loose plate and cross-key. [build_assets.py](https://github.com/aryansennthilkumarGT/benchmark-tasks/blob/a312bcac0f29098731ad40ce30df5fe3a6fcca78/tasks/twelve-cell-pack/build_assets.py) authors rigid assets/joints from it. This establishes the authored mechanical model, not a deployed manufacturer's operation.

[scoring.py](https://github.com/aryansennthilkumarGT/benchmark-tasks/blob/a312bcac0f29098731ad40ce30df5fe3a6fcca78/tasks/twelve-cell-pack/scoring.py) evaluates holder-relative pose, longitudinal polarity axis, each spring coordinate, stillness, one-to-one matching of interchangeable cells, dependent key capture and released hold. It explicitly treats axial spin as irrelevant. Those are substantive engineering features; none proves occupational regularity.

[expert.py](https://github.com/aryansennthilkumarGT/benchmark-tasks/blob/a312bcac0f29098731ad40ce30df5fe3a6fcca78/tasks/twelve-cell-pack/expert.py) replays a fixed14-dimensional joint/jaw trajectory, with robot/time validation. Earlier feedback controllers were separate. Under supplied Version21 even simulator-state feedback planning is allowed, so the fixed-action restriction is not needed to defend feasibility. No new native execution was performed here.

## Measurement document: what is and is not established

The submitted [MEASUREMENT.md](https://github.com/aryansennthilkumarGT/benchmark-tasks/blob/a312bcac0f29098731ad40ce30df5fe3a6fcca78/tasks/twelve-cell-pack/MEASUREMENT.md) and [geometry record](https://github.com/aryansennthilkumarGT/benchmark-tasks/blob/a312bcac0f29098731ad40ce30df5fe3a6fcca78/tasks/twelve-cell-pack/MEASUREMENT_GEOMETRY.json) provide:

- Two same-thickness solid transparent patches on each sightline: outer wall and individual guide wall. These are not manipulation openings.
- 0.05mm contact-disc witness line; coplanar fixed scale with0.1mmdivisions; zero datum set using the defined mechanical stop.
- Twelve external macro photographs/inspection-mirror views without touching task parts; at least50pixels/mm and stated0.05mm line-center resolution.
- Compression formula `c_i=8.000-h_i` in millimetres; accepted0.35–1.80mm corresponds to witness height6.20–7.65mm. No threshold change.
- Analytical checks against69 fixed holder boxes; explicitly no actual physical-build/photographic validation. Native rendered walls remain opaque.

**Finding:** the final submitted archive does specify a noninvasive measurement design addressing the earlier requested change. Claiming no method was specified in that revision would be inaccurate. Claiming it was physically validated would also be inaccurate.

**Remaining concerns:** initial analysis covers fixed-holder boxes, not every loaded movable-body posture. Optical refraction/glare, actual focus/resolution, camera/stand access and changing wall material are unvalidated. The document discloses judging-only geometry absent from rendering. The rubric allows explained simulation gaps, but humans still need to judge whether the physical reconstruction is practical and preserves the skill.

An unsubmitted follow-up at `1d92c6ef09b61b94d886efd49f587d898513fdc2` adds96 analytical rays for two recorded successful loaded postures and a dimensioned external mirror. Its own limits exclude optics, camera/stand/robot geometry and physical photos. It is **not** evidence that the final submitted archive already included that loaded-part check, and not physical validation.

## Is “earlier review feedback was not provided” factually wrong?

Not established. Measurement repair, original feedback text and the official model's supplied revision context are different facts. Version21 says the model never sees reviewers' comments automatically and receives only a capped code excerpt. GitHub having the earlier comment does not prove it was present in the review message. We have not inspected that private message. The measurement commit demonstrates a response to the scoring issue; it does not prove the flag's provenance or overturn the final importance objection.

## Patent and occupation leads

All four supplied URLs were attempted directly in this machine; each returned network-proxy403. No text/claims/drawings were read, so none can be classified as an established engineering analogue yet. The following are **provisional search roles based solely on the user's descriptions**, not source findings:

| Lead | Intended classification to investigate | Why insufficient even if described content is confirmed |
|---|---|---|
| [EP0613201A1](https://patents.google.com/patent/EP0613201A1/en), user also namesB1 | Potential STRONG ENGINEERING ANALOGUE: compression cage/locking pins; unverified | Plate compression may involve a different battery construction/process; patenting alone does not show twelve-AA terminal closure or routine production use. A1 application andB1 grant must not be conflated. |
| [US20250158191A1](https://patents.justia.com/patent/20250158191) | Potential STRONG ENGINEERING ANALOGUE or GENERAL RELATED TECHNOLOGY: frames/reversible fastening; unverified | “Maintains multicell compression” is broader than this free plate and cross-key operator procedure; deployment and worker regularity still needed. |
| [US20240356165A1](https://patents.justia.com/patent/20240356165) | Potential GENERAL RELATED TECHNOLOGY: conductor plate contacting twelve cells; unverified | A shared cell count/conductor plate does not establish independent spring preload captured by a cross-key. |
| [O*NET51-2022.00](https://www.onetonline.org/link/details/51-2022.00) | OCCUPATIONAL CONTEXT ONLY, if relevant entry confirmed | Occupation title/general assembly duties cannot establish that this exact operation is regularly performed. Check any SOC changes and actual employment scope. |

**Verified EXACT procedural matches:0.** No patent can be honestly quoted or treated as evidence of deployed commercial work from the current access results. Stronger evidence would be a named commercial holder/product drawing and production/service work instruction showing equivalent preload capture, plus direct regular/core occupational use. No such chain is established here.

## Defensible human-review wording—limited correction only, not a recommendation to appeal importance

If the team independently chooses to request clarification within the window, the strongest currently supportable statement is:

> The revised archive at a312bcac includes MEASUREMENT.md, added in6ff8f739 before TK-WS3H2A was received. It specifies twelve noncontact spring readings through solid optical patches, calibrated witness marks and coplanar scales, with unchanged thresholds. This is a measurement design, not a physically validated build. Could a human check whether that submitted repair and the prior scoring feedback were included in the revision context? We recognize that this does not by itself answer the final importance objection about established regular battery-pack assembly work.

This is an optional factual clarification, not a source-backed claim that the importance rejection should be reversed. **No substantive acceptance appeal is recommended on the present patent/occupation evidence.** Do not claim the optical repair, native score or patent analogues prove the missing real-world duty.
