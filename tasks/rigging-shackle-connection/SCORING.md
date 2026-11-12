# Recomputed, observable scoring

The native collector supplies one actual rigid-body observation per 20 Hz robot step. `scoring_base.py` validates complete finite body/joint state, time and quaternions; `scoring.py` adds through-connection span checks. Synthetic test frames are unit inputs, never robot evidence.

| Goal | Credit | Numerical condition |
|---|---:|---|
| aligned | 0.20 | Shackle origin within 0.8 mm of (0.22, 0, 0.788) m, orientation within 0.04 rad of authored orientation. |
| pin_through_lug | 0.25 | Alignment remains valid, pin position within 4.5 mm of its shallow-through reference (0,0,0.0335) m in the shackle frame, at least four pitch-coupled turns. |
| collar_seated | 0.55 | Above goals remain valid, pin origin within 0.35 mm of (0,0,0.0295) m relative to the shackle, pin axis within 0.025 rad, at least 5.8 pitch-coupled turns. |

Thread history is accumulated only while the pin axis is within 0.65 mm laterally and 0.025 rad in tilt of the matching eye axis, and its collar reference is in the 28–47 mm axial engagement interval. Relative yaw is unwrapped from successive actual observations; axial motion must match signed angle times 2.54 mm/turn, cumulatively within 0.30 mm. Disengaging, tilting out of alignment or switching sites resets credit. Free spins without descent and final-pose teleports do not earn thread credit. Rotations over 0.75 rad between observations are rejected as undersampled.

The final pin must span the lug and both eyes: lateral centre error <=0.8 mm, tip at least 25 mm below the lug reference plane, and axial projection >=0.999. The actual nominal tip is 29.5 mm below that plane. There is no arbitrary invisible attachment or success-triggered filter change.

All goal conditions must hold with every part <=0.01 m/s linear speed and <=0.2 rad/s angular speed, and both robots >=20 mm clear for two continuous seconds. Until that window completes, score is capped at 0.95. Frame gaps over 1.5 control periods reset stability. Losing alignment or backing out the pin removes dependent credit immediately.

Missing/extra bodies, invalid data/time, moved fixtures (>5 mm or 3 degrees), any part below the loss plane, and inter-part penetration over 1.5 mm latch score zero. The code defines boundary behavior, including duplicate-frame idempotence and inconsistent same-time rejection. Physical deformation is not modelled; no policy can edit shapes or attach parts.
