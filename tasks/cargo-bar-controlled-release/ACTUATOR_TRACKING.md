# Actual robot/controller repair, not native qualification

Original72e33f89853577aadebb78e64a1e783bd9087e84 is preserved. Fresh clean actual CPU YAM trial1410actions/70.5s stops at phase8, physical score0.25, no solver warnings. Handle angle2.598982rad and trigger9.041mm satisfy all independent physical guards, but the acquired-grasp TCP error352.706um misses350um controller tolerance. Robot SDK peak grip-speed ratio1.4556 also fails.

This successor retains every task solid, joint, mass, friction and scoring threshold. Only phase8 controller position tolerance becomes400um; physical handle/trigger checks stay unchanged. Joint tracking allowance0.08rad accounts for official wrist D/K0.15s at bounded reference0.4rad/s. Grip reference slew becomes0.05normalized/tick. The handle circle maintains a persistent0.5rad/s reference, limited by Cartesian speed,0.12rad physical lead, real IK/rate/effort constraints and existing stall/timeouts. Previously commanding only25mrad ahead of the measured handle on every tick made an unnecessarily slow proportional velocity loop.

The recorded physical terminal state is retained for response/constraint regressions. These changes require fresh full actual robot dynamics and native Isaac validation. No full-score physical or model result is claimed.


## Stricter geometry audit exposes an ideal-fixture defect

50um unintentional and800um intended-pad checks expose two old synthetic trigger overlaps:2.433mm during first squeeze and1.270mm during opening. They are not native contacts. The ideal fixture formerly subtracted full jaw-gap change from trigger travel, though only one jaw presses the paddle; it also reset the trigger as soon as the assumed handle grasp was released. The corrected explicit quasistatic fixture derives unpulled paddle support, inner-pad plane and transverse overlap from original trigger geometry and stock pad pieces5/8, projected into actual robot TCP axes. It retains contact during jaw opening and clips travel to the unchanged original joint limits. A regression checks actual URDF/task interference through intermediate apertures and release. This synthetic correction never changes native dynamics, assets, contact parameters or scoring.


## Actual moving-base reference failure

Clean c23fb66 reaches phase8 with SDK velocity ratio0.7301, then fails at746actions/37.3s, score0.25, no warnings. Releasing the loaded mechanism translates the real outer tube at63.6mm/s. Its live circle center moves about3.2mm per observation, so even halving arc advancement to zero cannot fit a20mrad reference increment. The successor holds arc-angle progress and slews the robot toward the same-angle pose at the unchanged20mrad/tick bound.50consecutive catch-up ticks terminate after2.5s. This bounded joint-space catch-up is disclosed; it is not an exact Cartesian circle while the base is moving. Physical task state is never frozen/set. Joint, trigger, scoring and SDK effort checks remain. A prescribed4mm base-motion stress verifies no reference jump or false arc progress; a fresh actual integration remains mandatory.


## Submission-first correction: persistent gripper command

The f75fb54 actual CPU run clears handle opening and both pawl checks, then stalls at phase11/1037actions/51.85s, physical score0.25; no warnings and SDK speed ratio0.7301. The gripper limiter advanced from measured aperture every tick. Once a part blocked closure it stayed measured−0.05, artificially limiting spring error/closing force instead of reaching the requested aperture. The fix retains a persistent aperture reference, slewed by at most0.05normalized per20Hz command, including circular-motion holds. Desired apertures, SDK force/velocity limits, mechanics, collision bounds and scorer are unchanged. A blocked-jaw regression proves eventual requested command and bounded command-to-command slew. Actual native force/velocity and retraction remain to be measured.

Further MuJoCo perfection is not a precondition for a separately authorized bounded Isaac diagnostic. Cargo is the first-priority candidate. Run the native retraction prefix to distinguish actual PhysX friction/actuation from this supplemental model before another redesign. No official submission or paid evaluation is authorized by this source change.


## Verify the achieved physical release without a redundant reposition

Clean6bc24e1 passes all16offline stages and the SDK velocity check (maximum0.7897), then stops at phase9/973actions. Actual handle/trigger/pawl guards are all true, but redundant nominal TCP positioning differs520.7um from the compliant acquired grip. Verification/outer-hold phases now retain the previously emitted valid joint reference while checking the same real physical guards. They command no new Cartesian move and do not weaken task success, joint thresholds or geometry. A regression replays the actual achieved state and rejects an un-released pawl. Native validation remains required; no full-score physical result is claimed.

The Inspect expert no longer requests stop merely because controller phases ended. Native scorer success or the declared run limit terminates the episode, allowing independent release/stillness conditions to decide success. This does not turn controller completion into evidence of a successful physical task.
