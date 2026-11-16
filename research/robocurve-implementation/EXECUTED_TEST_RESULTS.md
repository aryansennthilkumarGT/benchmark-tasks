# Actual executed CPU results

This checkpoint contains a **passing representative contact coupon**, two stopped candidate gates and a **blocked sampled robot path**. A unit score is not an official task score or a YAM demonstration.

## YUBI

- direct: 64 path templates, **0 complete clear paths**; {'pickup': 40, 'first-hook': 24}; 172 reachable-prefix sample checks; first-obstacle counts {None: 40, 'source-16': 24}.
- raised-transit: 64 path templates, **0 complete clear paths**; {'transit-above-band': 64}; 0 reachable-prefix sample checks; first-obstacle counts {None: 64}.

These are parameterized templates, not 128 independent grasp strategies. Two fixture placements, stock pads and one ordinary blunt-pick envelope were bounded alternatives; the other source arm was parked. IK failure is not proof of global unreachability. No stable physical band pickup or two-arm installation was demonstrated. The proposed rear-saddle centre also failed the original-solid occupancy check. Stage 2/3 installed-band physics and its eight requested controls were **not executed**.

## Faze4

- Actual five J4 meshes sectioned and registered in a nominal centred planar model. Global fits: upper mirror=1, worst gap **-0.398321mm**; upper mirror=-1, worst gap **-0.406246mm**.
- Independent ring-phase/carrier search: **121 phase pairs**, best shared-carrier gap **-0.460134mm**.
- The 73-point penalty sweep produced -32.782286degrees of output per 360-degree input, but its worst interference was 0.413919mm. **That motion is invalid, not a physical ratio demonstration.**
- Missing disk/pair, one-plane-only carrier and wrong-phase diagnostics did not produce a valid complete assembly. Full axial stack/cover-fastener and YAM insertion tests were not promoted after nominal closure failed.
- Cover triangle contacts at a shared face are not solid penetration; central-axis placement is not full source assembly registration. Source material compliance/part-revision compatibility remain unvalidated.

## Microwave contact coupon

|Case|Unit score|Pre-drive tray height,mm|Input rotation,rad|Output rotation,rad|
|---|---:|---:|---:|---:|
|correct|1.00|14.353823|7.000292|6.927395|
|wrong_phase|0.00|16.499858|7.000048|6.997192|
|missing_carrier|0.00|12.499822|7.000048|6.997164|
|missing_drive|0.25|14.353808|7.000331|0.000000|
|missing_wheel|0.00|12.968277|7.000041|6.963816|
|inverted_tray|0.00|14.353808|7.000299|0.000000|
|held_proud|0.00|22.416921|7.000108|0.000042|
|displaced_carrier|0.00|18.477534|7.000126|6.969775|
|seized_wheels|0.25|14.353904|0.193255|0.115709|

Nominal input **7.000292rad**, output **6.927395rad**, error **-0.072896rad (-4.177degrees)**. Tray centre settled from 44.5mm to **14.353823mm** under gravity.

Three pre-drive support forces: wheel0=2.326435N, wheel1=2.313533N, wheel2=2.307062N. These are simulated diagnostics, not measured hardware loads.

Relative wheel rotations through the test: wheel0=-57.974448rad, wheel1=-58.172801rad, wheel2=-58.114072rad.

Model audit: **0 equality constraints, 0 tray actuators, 0 mocap bodies, only input-shaft actuation, no externally applied tray force**. There is no runtime tray-pose assignment or capture trigger.

Mass/friction sensitivity (authored glass mass excludes 8.4g of key meshes):
- friction0.2, glass mass0.5kg → score1.00.
- friction0.2, glass mass0.9kg → score1.00.
- friction0.6, glass mass0.5kg → score1.00.
- friction0.6, glass mass0.9kg → score1.00.

Critical unverified-geometry sensitivity:
- Authored drive-arm top7.0mm → score0.25, output0.000007rad.
- Authored drive-arm top9.0mm → score1.00, output6.927136rad.
- Authored drive-arm top11.0mm → score1.00, output6.927355rad.

This validates a realizable representative support/drive mechanism over the tested parameters. It **does not validate Toshiba dimensions, real materials or compatibility**. A 7 mm drive top loses coupling: a manual alone cannot establish the missing physical section.

## Stock YAM evidence

- 10 IK endpoints solved within 1 mm/1.15degrees; actual recorded errors are substantially smaller. Both source arms contain 315 collision hulls.
- Six hypothesized bimanual keyframes cover posed acquisition, lift, insertion, lowering, release and withdrawal. The actual ready-to-pregrasp motion, physical pinch and load-bearing pickup were not demonstrated.

- Door90degrees: **65/65 sampled poses rejected by obstacle collision**; self-collision poses0, unintended tray/robot collision poses0, payload/obstacle collision poses0. The first reported obstacle is the original-role open door. The undersized-aperture control was detected.
- Door110degrees: **65/65 sampled poses rejected by obstacle collision**; self-collision poses0, unintended tray/robot collision poses0, payload/obstacle collision poses0. The first reported obstacle is the original-role open door. The undersized-aperture control was detected.

All robot hulls are represented; obstacle queries short-circuit when a rejecting collision is found. Self/arm-arm and held-object checks were run separately. Zero reported collisions in another category does not rescue a door collision. Sampling never certifies the interval between samples. **Stock-YAM installation is blocked for these representative layouts, not demonstrated on the donor.**

## Completion/resource boundary

No GPU, Brev, Dream, paid evaluation, purchase, full native task or official submission occurred. Previous research files are unchanged. The completed unit is the executable contact coupon; full implementation recommendation remains **NO**.
