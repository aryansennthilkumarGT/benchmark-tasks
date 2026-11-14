# Our four final rejections: root causes

Fresh sources: [#1647](https://github.com/robocurve/benchmark-tasks/pull/1647), [#1703](https://github.com/robocurve/benchmark-tasks/pull/1703), [#1733](https://github.com/robocurve/benchmark-tasks/pull/1733), [#1772](https://github.com/robocurve/benchmark-tasks/pull/1772). Every rendered reviewer comment was read, including intake and earlier revisions. Full text, authors and times: [evidence](evidence/pr-discussions.json). The analysis of why the internal audits missed the flaws is an inference from the published claims and audit artifacts, not a claim to know the team's private deliberations.

## #1647 — counterweighted service arm

1. **Original argument:** gravity-moment adjustment plus locking-pin retention is distinct manipulation; native probes, three expert reproductions, Dream0, media and detailed reset documentation demonstrate a robust task. The PR author claimed 8/8 mechanism and4/4 robot probes and1899-action successful experts.
2. **Hidden invalid assumption:** a generic device resembling maintenance equipment inherits the importance of general maintenance workers.
3. **Exact reviewer objection:** “The submission identifies no occupation for which adjusting this generic counterweighted service arm is regular core work, and it is not plainly a core task of general maintenance and repair workers.” The reviewer also explicitly identifies the service arm and tool load as generic surrogates.
4. **Audit blind spot:** excellent execution provenance answers whether the mechanism works, not whether actual workers regularly perform this equipment procedure.
5. **Pre-spend research:** select an actual counterbalanced equipment model, obtain its adjustment instructions, identify who does that adjustment and how routinely; abandon if only specialist commissioning or an invented fixture is found.
6. **Mandatory rule:** no jobs claim may pass on an occupation label alone. Require equipment model + exact documented operation + direct core-duty mapping before any scene work.

Intake also initially failed because the account was not matched to a team. That was separately corrected; it did not cause the final rejection.

## #1703 — opposed-polarity cells under a spring-return cover

1. **Original argument:** sustained cover access while exchanging two opposed cells supposedly adds essential simultaneous handling. Author claimed16/16 mechanism,4/4 robot probes and5261-action experts.
2. **Hidden invalid assumptions:** two cells and a spring-return door constitute a new physical capability; routine AA exchange inherits occupational importance from service work.
3. **Exact reviewer objection:** “dexhand: Remote Battery Swap already tests sliding open a battery cover, removing an AA cell, installing a replacement, and closing it; routine AA replacement is not shown to be a core job for a qualifying occupation.” Reviewer explicitly says adding the second cell and spring-return cover is insufficient.
4. **Audit blind spot:** novelty was evaluated at detailed mechanism level without first testing semantic equivalence to the complete existing operation. Feasibility evidence could not repair either importance failure.
5. **Pre-spend research:** read DexHand's actual remote-battery task and compare cover/open/remove/insert/close and success condition. Separately seek direct occupational evidence for AA replacement; do not count all maintenance jobs.
6. **Mandatory rule:** compare the nearest complete operation before considering added mechanics. Reject component-count and access-support embellishments unless evidence shows a distinct central skill.

## #1733 — twelve-cell preload captured by a cross-key

1. **Original argument:** capturing the distributed contact preload of twelve loaded cells differs from four-cell loading, blind clamps and M.2 retention; independent native experts allegedly scored1.0 in1677 actions, with Dream0 and real media.
2. **Hidden invalid assumptions:** assemblers' large employment establishes this particular cross-key procedure; simulator spring coordinates provide adequate physical scoring.
3. **Exact objections in order:** Nov12: “The twelve 0.35–1.8 mm spring compressions are beneath the cells, with no specified noninvasive measurement method for a physical trial.” Nov14 final: “Team assemblers regularly assemble products, but the submission does not establish that capturing twelve AA-cell spring contacts with a cross-key is a regular battery-pack assembly operation.” Final review also flags that earlier feedback was not supplied.
4. **Audit blind spot:** testing mechanically independent springs and rigorous state predicates validated an invented assembly, and the scorer audit checked numeric precision rather than physical observability. Repairing measurement access did not establish authenticity.
5. **Pre-spend research:** find a manufacturer assembly drawing/service instruction showing the actual pressure plate, cross-key and terminal retention. Build a physical observation plan with closed-cover sight lines before choosing scoring variables. If no authentic product exists, stop.
6. **Mandatory rule:** every essential fixture/mechanism must trace to real equipment or a justified ordinary fixture. Every internal score predicate needs a noninvasive physical measurement protocol. Preserve and disclose all earlier feedback during revision.

Intake separately rejected an overlong setup(max4000) and fidelity(max500). Those were correctable metadata failures, not the reason to revive the concept.

## #1772 — storage/cooling module exchange

1. **Original argument:** removing an obstructing cooler before storage, replacing both and closing the enclosure creates dependent service sequencing. The author explicitly disclaimed connectors, electronics and any standard server claim; native experts allegedly completed4378 actions.
2. **Hidden invalid assumption:** disclaiming interfaces makes a surrogate acceptable while keeping the importance of real equipment service. The labels “cooling” and “storage” did the occupational work that the equipment did not support.
3. **Exact reviewer objections:** “No specific equipment or regular work of an occupation such as team assemblers or general maintenance workers is identified”; “The gravity-retained cooler and connector-free storage are a generic surrogate, without an identified real service procedure whose essential interfaces they preserve.”
4. **Audit blind spot:** the audit treated explicit limitations as a construct-validity defense instead of asking whether the removed interfaces were the claimed skill itself. Correct ordering in a custom puzzle did not establish a real service outcome.
5. **Pre-spend research:** one named OEM service manual with the actual latches, drive/backplane connector, fan or heatsink restraint, cable routing and order dependencies. Compare the physical endpoint to the manual, not a story about interchangeable modules.
6. **Mandatory rule:** do not borrow an OEM operation's importance after deleting the interfaces that make it an OEM operation. If simplification removes the central manipulation, reject the design.

## Cross-cutting prevention gate

Before authoring assets, record: (a) exact real procedure, primary page/figure/step; (b) occupation and direct regular/core-duty link or a different supported domain; (c) three closest semantic comparators, including pending tasks; (d) essential-contact preservation table; (e) simple physical measurement for every score term; (f) real stock-gripper envelope, force and reach assessment. An unknown gate remains unknown. Only then do CPU mechanics checks become useful. The four PRs are negative evidence against the concepts, not failed simulations waiting for a better controller.
