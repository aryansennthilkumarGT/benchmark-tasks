# Stock-YAM access preflight

**Result: NOT CLEARED.** Actual CAD inspection and static surface diagnostics ran. A complete KER phase path did not run. [Executed input-gate result](results/ACCESS_INPUT_GATE.json), [command output](results/ACCESS_EXECUTION.txt).

`CHECK_ACCESS_INPUTS.py` imports the existing `preflight/access_core.py` and pinned YAM assets. It retains315 hulls per arm, both station bases and the existing finger/palm/wrist/elbow collision logic. It does not rebuild a robot, suppress essential KER/jig geometry or synthesize a successful path. The evaluator returned `BLOCKED_MISSING_INPUTS`,18 missing-input entries, three unbound force groups, exit2. Eighteen includes path/phase coverage entries; it is not eighteen measured physical failures.

The genuine native BRep geometry exists, but a validated articulated KER calibration registration/link-joint definition is missing. STEP occurrence placements alone are not an articulated motion model. Neither a follower URDF nor a welded509-body KER is substituted. The second tool/grasp field is also explicitly unbound; solving the upstream registration does not automatically clear it.

## Required phase coverage

| Required action | Source geometry available | Actual access status / remaining input |
|---|---|---|
| Acquire/support articulated KER |Both arms, body,509 CAD occurrences; provider states1.7kg product mass |NOT RUN. Actual rigid-link membership, joint motion/limits/resistance, grasps and CoM/support load transfer not bound. CAD volume is not mass. |
| Seat both P1 pipes |Real15mm pipes and two R7.5 seats, including inclined seat |Static single-site CAD controls ran; **no gripper path**. Registered chain posture and full neighboring-part geometry along motion required. |
| Bring J8 against both flats |Real holder regions and paired candidate holes |NOT RUN. Correct J8-to-holder transforms and articulated chain constraints unverified. |
| Hold body against rear datum |Real body/base parts and rear fixture surfaces |NOT RUN. Verified body insertion/support pose and load path required. |
| Engage authentic body lock |Actual integral rear lock profile; workflow describes flexing frame |NOT RUN. No generic latch or permission-to-open flag. Actual insertion configuration and compliant support/load data required. |
| Access/fasten two M2 screws per side |Four real candidate clearance axes; workflow M2×12mm |NOT RUN. Suitable real tool/drive, grip, shaft/handle envelope and reaction contact unbound. Tool-point reach cannot certify palm/fixture clearance. |
| Release support |Jig and KER source bodies present |NOT RUN. Full retained readiness, support balance and collision-free withdrawal not established. |
| Repeat/preserve both sides |Mirrored/nonmirrored parts and asymmetric fixture sites present |NOT RUN. Left/right mapping and sequential postures must preserve earlier datums/lock while the other side is manipulated. |

## Actual scale, support and sweeps

Native dimensions remain unchanged. The jig underside at native Z−39 defines a flat support candidate. A future bench placement would need an explicit rigid transform, with mm→m conversion once, complete table/support geometry and all KER joint states. No world-frame placement was asserted to be manufacturer-defined, and no source part was scaled or enlarged. No material work pose or target poses were invented here.

The native exported KER envelope260×525.2×293.993mm does not prove that it exceeds YAM reach or fits. Articulation changes its envelope; source body datums and end-tool clearance matter more than the overall box. The nominal93.9mm YAM aperture does not prove purchase on a15mm carbon tube or stability of a1.7kg articulated assembly. Payload moment, friction and link sag remain unresolved. READY-pose static force ceilings are not substituted for loaded tool capability.

A later complete screen must include full fingertips, palms, wrists, elbows, both arms, actual KER links and fixture concavities, and the actual screwdriver/handled tool. Using one convex hull of the entire concave jig would wrongly fill its seating spaces; a coarse display mesh is also not an automatic collision certificate. The raw BReps and their full occurrence placements are retained for that work.

**No successful TCP-only check, complete collision-free pose, swept path, grip proof or load-bearing release is claimed.** The input gate is a useful executed refusal, while the new geometric evidence is the real CAD inventory and contact diagnostics. No previous20-control robot suite was rerun as KER evidence.
