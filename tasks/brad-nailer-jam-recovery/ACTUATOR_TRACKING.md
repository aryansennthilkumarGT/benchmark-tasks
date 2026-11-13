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


## Actual live acquisition reaches a joint limit; radial closing repair

Clean9307894 still fails phase30: following the displaced pin eventually reaches a robot joint limit at2065actions/103.25s, physical score0.5, no warnings. Slow live tracking alone did not repair the tangential first-pad impulse. The new grasp aligns the actual stock gripper closing axis with the bail/pin frame+X radius, with toolZ parallel to the vertical pin. A first normal force then acts toward the bail pivot instead of sweeping the pin around it. Slow closure, live measured reference, empty-jaw guard, retries and all scorer/geometry parameters remain. An actual-recorded fixture endpoint passes full stock-mesh50um clearance and has0.505rad joint margin; a180degree alternative had only0.106rad margin and was not selected. Full current-source dynamics is required; this static/replay result is not a success demonstration.


The first radial orientation (zero in-plane flip) clears initial acquisition but fails the ideal phase33 circle at a wrist/rate constraint. It is excluded. The radial180degree flip preserves the same closing-force line and starts with0.106rad static joint margin; it is being tested across the entire controller before selection. Neither endpoint margin alone establishes a viable full path.


The full ideal orientation screen excludes both zero-roll radial flips and eleven of twelve tested roll/flip combinations. Selected closing normal is radial with0.8rad roll about that normal and zero in-plane flip; it completes49ideal phases in2782actions. This retains a radial first-pad force while canting the approach to fit the robot wrists. The coupled-reference regression now uses the actual recorded released-pin state; the old force-rig nominal free-link orientation is different and is not a demonstrated native reset pose. Runtime pose feedback and future native qualification remain mandatory. A fresh exact-source full ideal/FK and actual robot run must validate this selected plan.


## Full-path arm interference repair

Selected radial0.8rad-roll plan completes2782ideal actions, but its first635-sample FK audit fails: link4 interference235um during pin approach and gripper interference255um near acquisition. The unchanged50um unintentional-contact gate correctly rejects it. The second door grasp moves7mm along the same original plate toward its hinge (localX25→18mm); initial door opening retains the proven25mm grasp. This separates the held left hand from the right pin hand without altering geometry or scoring. Door release opens at measured TCP, then withdraws along its actual tool axis. Full fresh ideal/FK and actual robot validation are required.

## Preserved experiment — not qualified

This radial-grasp/door-offset experiment passes ideal phase completion and unit checks but FAILS full FK collision QA: independently confirmed 207um interarm gripper overlap exceeds the unchanged50um bound. It must not be selected for GPU qualification or submission. Preserved to retain source/evidence rather than overwrite the published9307894 baseline. A static -0.03rad door-grasp cant screen is not a full-path repair and is not implemented here.
