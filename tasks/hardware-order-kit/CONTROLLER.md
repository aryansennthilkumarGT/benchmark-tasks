# Measured robot controller

The expert submits14-dimensional absolute joint/jaw actions through the official YAM adapter at20Hz. Object changes occur through PhysX robot contacts. It verifies grasp widths, measured body/joint motion, joint limits and bounded insertion progress. It never writes object poses or score state during a demonstration.

Both hands support the same assembly. Cooperative carry and insertion phases construct their targets from the same incremental measured parent pose and each stored relative grasp transform. This avoids anchoring one hand at the previous pose while commanding the other forward. Near-goal carry gain is1; shaft insertion uses a1mm axial increment and unchanged lateral/orientation gates. The upper collar opens to-1.30rad within the actual[-1.35,0]hinge range. Full phase targets and limits are authoritative in controller.json.

| Phase | Arm | Operation | Goal |
|---|---|---|---|
| 0 | left | move | Approach lower collar handle |
| 1 | left | grasp | Support lower collar |
| 2 | right | move | Approach upper collar handle |
| 3 | right | grasp | Grasp upper collar handle |
| 4 | right | joint | Open the split collar |
| 5 | left | carry | Lift the open collar |
| 6 | left | carry | Bring open collar beneath captive shaft |
| 7 | left | insert | Lift lower half around the shaft |
| 8 | right | joint | Close upper half over the shaft |
| 9 | right | release | Release closed upper collar |
| 10 | right | move | Clear upper handle |
| 11 | right | move | Approach transverse key head |
| 12 | right | grasp | Grasp transverse key head |
| 13 | right | carry | Lift transverse key |
| 14 | right | carry | Align key in front of the three lugs |
| 15 | right | insert | Pass key through interleaved lugs |
| 16 | right | release | Release seated transverse key |
| 17 | right | move | Lift above captive shaft |
| 18 | right | move | Retreat past shaft flange |
| 19 | right | move | Clear retained collar |
| 20 | left | release | Release lower collar support |
| 21 | right | move | Withdraw right arm |
| 22 | left | move | Withdraw left arm |
| 23 | left | hold | Observe released terminal stability |

Offline unit/geometry tests check control contracts but do not establish feasibility. Two complete cold-reset full-score experts and independent clean-checkout reproduction are required before publication. Recorded fixture replays are diagnostics only.
