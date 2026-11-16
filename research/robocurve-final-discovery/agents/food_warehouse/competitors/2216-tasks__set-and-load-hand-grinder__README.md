# Set and load a hand-crank coffee grinder

Align the grind selector with the blue index, pour the test dose into the side intake, put down the cup and turn the crank one full revolution. The body is secured to the counter by a mounting foot.

## Run and score a trial

Use the Linux image from the [RoboCurve YAM walkthrough](https://tasks.robocurve.org/walkthrough). The reference environment uses Isaac Sim 6.1.0.0, Isaac Lab 17.0.2, IsaacLab-Arena `c7edf3a9d5d8276565208f72422f8f8a0806d6cf`, YAM adapter `0059d02a1a91bc6834c1d0846022891df0c78730`, Inspect Robots 0.60.0, inspect-robots-dream 0.1.0 and dreamlabs-client 1.0.14. The runner also uses NumPy, SciPy, PyTorch, Pillow and imageio-ffmpeg.

From the task folder, choose a fresh output folder for each trial.

```bash
isaac_python=/data/IsaacLab-Arena/.venv/bin/python
export OMNI_KIT_ACCEPT_EULA=YES OPENBLAS_NUM_THREADS=1

"$isaac_python" run_grinder_probe.py --usd assets/grinder.usda --dose assets \
  --both --dial-contact-radius .047 --output runs/expert
"$isaac_python" audit_grinder_trial.py runs/expert

# Configure the Dream Labs credential using the walkthrough.
"$isaac_python" run_grinder_probe.py --usd assets/grinder.usda --dose assets \
  --both --dream --output runs/dream
"$isaac_python" audit_grinder_trial.py runs/dream
```

The layout uses seed 0 with object jitter disabled. CPU PhysX advances at 480 Hz with continuous collision detection. The controller receives up to 2,400 actions at 20 Hz, equivalent to 120 simulated seconds. The expert earns 1.0 in 1,469 control steps, or 73.45 simulated seconds. Dream-1 earns 0.0 in 2,400 controls and 50 API requests. Each video frame corresponds to a control. The trace records joint states, actions, cup and bean poses and fingertip forces.

## Fixed setup

Coordinates are metres in the robot frame. Positive X points across the counter and positive Y is to the robots' left.

| Object | Dimensions and represented material | Initial configuration |
| --- | --- | --- |
| Counter | 620 × 800 × 40 mm wood | Centre `(0.49, 0, 0.73)`, surface Z = 0.75 |
| Grinder | 54 mm diameter steel column, 60 mm base diameter, 84 × 60 × 8 mm foot with two 12 mm metal bolts | Base origin `(0.31, 0.20, 0.75)` |
| Dial and index | 62 mm diameter metal ring, wooden pointer, fixed blue index | Joint angle 0°, blue index at 30° |
| Crank | Steel arm with 60 mm radius, 22 × 26 mm wood grip on its own bearing | Grip initially along the positive X axis from the grinder |
| Side intake | 72 mm inner diameter, 78 mm outer diameter and 90 mm height, coated metal | Centre `(0.31, 0.132, 0.75)` |
| Dose cup | 64 × 44 × 26 mm aluminium scoop body, low pouring edge, 43 × 16 × 17 mm polymer grip | Origin `(0.230, 0.061, 0.75)`, yaw 180°, with 12 beans |
| Coffee beans | Twelve 7.4 mm diameter collision spheres, 0.17 g each | Inside the dose cup |
| Two fixed-base YAM arms | Six axes and parallel grippers | `(0, 0.305, 0.75)` and `(0, -0.305, 0.75)` |
| Floor and station marker | 3 × 3 × 0.04 m floor and 10 mm adapter marker outside the working area | Floor centre `(0.45, 0, -0.02)`, marker at `(-0.5, 0, -0.05)` |

## Scoring

The audit takes the final 20 control observations for the endpoint conditions.

- **0.25 for the setting.** The dial is at 26–34° and its angular spread across the final observations is at most 2°.
- **Up to 0.35 for loading.** Multiply 0.35 by the minimum fraction of the 12 beans in the intake. A bean centre counts at radius below 34 mm and height between 4 and 90 mm above the intake base.
- **Up to 0.30 for the crank.** Count positive net crank rotation beginning when all 12 beans are present for five consecutive observations. Up to 350° of net rotation earns proportional credit. The final aggregate measured gripper force on the knob must be at most 0.1 N.
- **0.10 for parking the dose cup.** After at least one bean is transferred, the released cup is within 20 mm of its starting position and its up axis is within 8° of vertical. Its final combined fingertip force is at most 0.1 N.

The timing test treats a complete turn as at least 350° of measured travel. The base is mechanically fixed to the counter, the adjustment and crank are dynamic joints, and the beans and dosing cup are free rigid bodies. The side intake retains the beans for measurement. The simulation models the loading and turning operations without modelling particle fracture or grounds.
