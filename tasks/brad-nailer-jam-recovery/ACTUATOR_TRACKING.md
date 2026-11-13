# Actuator/contact repair in progress

This successor preserves original scene geometry, materials, masses, joints and scoring. It is **not currently qualified OFFLINE READY**. The original d8d454b source and evidence remain preserved on their branch. No Isaac, hardware, Dream or official submission ran.

A genuine supplemental MuJoCo model with both full URDF arms and pinned SDK actuators found the old brad-acquisition target blocked by a stock finger entering the tool's front bumper by409µm. The previous500µm collision tolerance hid this. The grasp moves2mm forward along the same actual brad; a new real-URDF test rejects the old target and verifies the new clearance. Unexpected FK contacts now have a50µm bound. All638 sampled complete-controller FK configurations pass and synthetic outcome scoring reaches1.0, under explicitly ideal grasps. These do not establish physical grasps.

The arc reference now advances at a bounded0.5rad/s along the actual joint circle. IK commands remain bounded relative to the previous emitted reference, with physical feedback and existing stall/timeout/recovery checks. An0.08rad actuator-lag allowance reflects the official wrist D/K0.15s at the0.4rad/s joint reference cap plus0.02rad of room; it is an authored controller setting, not a manufacturer force specification. Gripper reference steps reduce to0.05 normalized units, eliminating the supplemental model's earlier1.44× SDK velocity-limit excursion (new maximum0.723×).

The earlier real-physics lever-release prefix improves from1029actions/51.45s to520/26s before the gripper slew repair. The complete new ideal replay uses2793actions/139.65s with2.96µm maximum synthetic grasp residual. It is not a full real-physics expert.

The current real-physics run passes the repaired brad approach/reach but fails acquisition after two bounded retries. Both fingers contact the1mm,0.5g brad while the reported joint aperture compresses below the empty-jaw threshold. A higher-impedance-only contact calibration did not fix it. Investigate the supplemental contact time constant/resolution and actual closed-jaw geometry without weakening the scorer, changing object mass/dimensions or fabricating a grasp. No readiness claim is restored until this is resolved. Root recovery coordination contains the source-bound raw physical traces and separate model-calibration scripts; they are optional diagnostics, not task runtime dependencies.

## Contact calibration and capture feedback successor

The source-bound clean subdivision4 experiment was interrupted by a real cloud environment restart. Its retained complete frames show the bar captured between both fingers with0.923mm joint aperture and about0.73mm TCP deflection. The unchanged0.4mm acquisition tolerance caused needless retries. Only this capture phase now permits1mm of TCP acquisition compliance, while preserving the actual jaw-width check, all task scoring/clearance/integrity bounds and all other phase tolerances. The recorded-state unit regression accepts that physical capture and still rejects an empty gripper. Its input frames are tracked in test_fixtures/ and included in both manifest and runtime hashing.

Independent contact refinement converges to0.923/0.933mm aperture at4/8subdivisions, with178/7.87µm peak robot-contact depths and no warnings. Removing the bar closes the same jaws to zero at every resolution. This calibrates the supplemental rigid-contact approximation; it does not establish native physics or completed-expert success.

The optional root CPU diagnostic now preserves actual MuJoCo integration state, complete controller/scorer history and a hashed trace prefix. A killed process can resume that exact computational episode without simulated grasps or pose projections. Restarts are explicitly labeled; this is not a substitute for independent fresh-reset native demonstrations. Full clean-checkout qualification remains pending.


## Actual door reacquisition failure and entry repair

Clean source4315875 with clean CPU harness06b8c7f completes brad acquisition, extraction and deposition, but stops at phase26/1993actions/99.65s with physical score0.5. No solver warnings; SDK velocity ratio0.7322. It is a failed supplemental run, not native qualification. The5.6mm entry gap contacts the freely hinged3mm door and pushes its angle from1.9159rad to1.7613rad; the phase retains its bound world target. The new32.9mm approach/reach opening matches the successful initial door entry; final acquisition still closes onto the unchanged3mm plate. A regression uses the actual start/stall observations and original stock finger meshes: the former target overlaps the displaced door by3.758mm; the wider entry has no task collision at that same target/door state. A fresh full physical run is required; static clearance does not prove the capture or relatching succeeds.


## Actual free-pin capture failure and live slow closure

Clean0d27a3b completes the formerly failing door reach/regrasp, then exhausts two bounded retries on phase30 crosspin grip.2614actions/130.7s, score0.5, no solver warnings, SDK velocity ratio0.7328. The initial finger contact rotates the unrestrained bail/lever and the frozen world target closes on empty space. The successor follows measured pin pose only during acquisition and closes at0.005normalized per tick (0.47mm jaw aperture per50ms). Actual nonempty-jaw, TCP, timeout and two-retry checks remain. All task mechanics/scoring are unchanged. Recorded early failed frames exercise live reference updating and the slower command bound, without claiming fresh physics success.

## Independent source repair after red-team review

This successor starts from9307894, excluding the collision-failing radial experiment preserved at experiments/nailer-radial-clearance. Every command path (ordinary, arc leader and coupled follower) now slews a persistent aperture reference, preserving phase30 slow0.005normalized/tick closure and the SDK limits. A blocked jaw can reach the requested closing reference instead of permanently capping force error at one slew step. Scorer telemetry rejects malformed time/contact/joint sets and impossible free-brad jumps (>2m/s times elapsed plus10mm), without imposing an expert phase sequence. Controller completion no longer requests stop before independent physical success. Latest physical evidence remains the older9307894 pin-acquisition failure; no physical success is claimed for this repair.

Importance remains a substantive acceptance risk: manufacturer jam-clearing instructions and general carpentry employment establish an authentic procedure, but regular core-job jam clearing frequency has not been demonstrated. Do not spend on acceptance qualification/Dream until that gap is resolved. Scoring integrity is sampled at20Hz, not continuously at every physics substep.
