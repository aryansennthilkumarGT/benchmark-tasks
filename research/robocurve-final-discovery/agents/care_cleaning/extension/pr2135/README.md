# Swap a dead E27 bulb in a table lamp

A table lamp with its shade off stands on the table with a dead bulb screwed into its upright E27 lampholder. A new
bulb of the same model stands cap down in a small stand, and a cardboard collection box for spent lamps stands
nearby. The robot must unscrew the dead bulb, put it into the collection box, and screw the new bulb in until it is
snug (hand-tight) without forcing it.

**Instruction:** `The lamp's bulb is dead. Put it in the collection box and screw the new bulb into the lamp.`

## Why this task

Changing a light bulb is one of the most common household chores, and screw-base (Edison E27 / E26) bulbs are still
the standard fitting in homes in most of the world. The robot has to take out a bulb that is already in hand-tight,
carry it to the box without dropping it, and only then fit the new one: the same thread turned both ways, with a
carry in between. The only thing to grip is a round, smooth, frosted 60 mm globe weighing 40 g, with no flats or
handle, so each half turn needs a regrip, the hand has to follow the thread up and down (3.63 mm per turn), and
squeezing harder is not an option on a fragile globe. The lamp is not fixed: it stands on its 1.2 kg base, so turning
hard or pulling sideways can tip it over. The new bulb's thread has to be started square on the upright lampholder
(pushing it down does nothing), and the screwing has to stop at the contact, where there is no mark to see: a bulb
that is not in far enough does not light, and a forced one can have its cap twisted off the globe.

## Hardware

**Bulbs:** Philips LED classic 60W A60 E27 WW FR ND 1CT/10, 12NC 929001243082 (Philips data sheet, 2022): frosted A60
bulb, D 60 mm, C 110 mm, net weight 0.040 kg, E27 cap, 7 W, 806 lm. Both bulbs are this model.

**Thread:** E27 Edison screw, IEC 60061-1 sheet 7004-21: 7 threads per inch (pitch 3.629 mm), thread major diameter
about 26.4 mm, cap thread length at least 22.0 mm. The simulated cap has a 22 mm threaded shell, 26.4 mm over its
crest and 24.2 mm under it.

| Data | Value | Simulation |
|---|---|---|
| Bulb diameter D (data sheet) | 60 mm | 60 mm (globe as 16-sided slices) |
| Bulb length C (data sheet) | 110 mm | 110 mm |
| Bulb weight (data sheet) | 0.040 kg | 0.040 kg |
| E27 pitch (IEC 60061-1) | 1/7 in = 3.629 mm | 3.629 mm |
| Cap thread length (IEC 60061-1, min) | 22.0 mm | 22 mm |
| Turns from the first catch to the contact | see "Our assumptions" | 3.5 turns (12.7 mm) |

## Design

| Object | Size | Mass | Notes |
|---|---|---|---|
| Table lamp, shade off | Round base 14 cm across, 2 cm thick; 2.4 cm column; black E27 lampholder 40 mm across on top, mouth 8.3 cm above the table | 1.2 kg | Free (not fixed): it stands on its weighted base. Axis at x 29, y -12 cm |
| Dead bulb | Philips LED classic 60W A60 E27 (above) | 0.040 kg | Screwed in hand-tight at the start |
| New bulb | Same model | 0.040 kg | Stands cap down in a pine stand 6 x 6 x 2.5 cm with a 30 mm square hole, at x 40, y -27 cm |
| Collection box | Cardboard, open top, 10 x 10 cm inside, 7 cm tall | fixed | At x 17, y -30 cm |

Positions are from the midpoint between the two arm bases (x forward, y left, z up).

- **The thread:** the lampholder's first thread is a ledge the cap's lowest crest rests on. Once the cap rests centred
  and square on it, a joint lets the bulb turn and slide along the lamp's axis, and its height follows the turn:
  3.629 mm per turn, clockwise (seen from above) goes in. After 3.5 turns the bulb's base contact touches the
  lampholder's base contact; that is a hard stop. Turned 10 degrees back past the first catch the bulb is off the
  thread and free. The dead bulb starts on the thread, fully in.
- **Why the lamp is low:** a straight-down grip on the globe with the wrist turning half turns is within the arm's
  reach only up to about 20 cm above the table, so the lampholder's mouth is 8.3 cm up (a low bedside-type lamp).

## Scoring

Evaluated every control step; the score at the end of the episode counts (`SCORE_OVER = "end"`).

| Condition | Score |
|---|---|
| A bulb fell off the table, a bulb was dropped (fell freely: over 1.4 m/s downward, a fall of about 10 cm), the lamp was knocked over (tilted over 30 degrees), or a bulb was forced against the contact (2 N m) at any time | 0 |
| Otherwise the sum of: | |
| the dead bulb is off the thread and out of the lamp (its cap over 5 cm from the lamp's axis) | +0.25 |
| and inside the collection box (its cap end within the box's inside, below its rim) | +0.25 |
| the new bulb is on the thread and has been turned at least one full turn | +0.25 |
| and its contact touches the lampholder's base contact (within 0.3 mm) and it is hand-tight: turned on against the contact with at least 0.3 N m (latched; backing it off 1/8 turn clears it) | +0.25 |

1.0 is success (held 1 s).

- In a real trial: the operator looks at the video for drops and checks after the trial that the new bulb is
  hand-tight (switching the lamp on shows the contact; a gentle clockwise twist by hand does not turn it further),
  and that the dead bulb is in the box.
- Unintended strategies and what stops them: doing nothing gives 0 (the dead bulb is still in); pushing the new bulb
  down without turning it does not seat it (the cap rests on the first thread); screwing the dead bulb back in, or
  leaving it on the table, gives no box credit; dropping or tossing a bulb into the box gives 0; turning the new bulb
  on hard after it is home (forcing it) gives 0.

## Scripted demo

```bash
inspect-robots run --embodiment yam_arena --policy yam_scripted \
  -E task=task.py -E object_jitter=0 -E control_hz=20 -E cam_width=320 -E cam_height=176 \
  --instruction "The lamp's bulb is dead. Put it in the collection box and screw the new bulb into the lamp." \
  --scorer task_score \
  --max-steps 2400 --store-frames --log-dir ~/yam-eval/e27-bulb-swap-demo
```

Right arm only:

1. Grips the dead bulb's globe at its equator from above and unscrews it in counterclockwise half turns: grip, turn
   180 degrees while rising with the thread, let go, rise, turn the hand back, grip again; seven half turns, then an
   eighth that lifts it off the thread while still holding it.
2. Carries it over the collection box, lowers it in and lets go 1.2 cm above the box's floor.
3. Takes the new bulb out of its stand, brings it over the lamp and sets its cap on the lampholder's first thread,
   where the thread catches. Lets go.
4. Screws it in with seven clockwise half turns, following the thread down; the last goes 35 degrees further because
   the fingers slip a little on the globe. Then it grips once more and turns the bulb 25 degrees on against the
   contact (hand-tight).

`yam_scripted` plays fixed waypoints: the demo is open loop and uses no simulator state.

`BULB_DEBUG=1` prints the lamp's and bulbs' poses and the thread's state every 0.2 s. It is off by default.

## Files

| File | What |
|---|---|
| `task.py` | The yam_arena task file: lamp, bulbs, stand and box, the thread emulation, `score()` / `success()`, and `demo()` |
| `jointkit.py` | Rigid parts made of boxes, joints between parts that can be switched on and off and driven at run time, and per-physics-step and reset hooks (hooks yam_arena without modifying it) |
| `test_e27_bulb_swap.py` | The task file loads, the real thread and bulb dimensions, the hand-tight and forced thresholds, enough half turns in the demo, the demo's reach and length |
| `task.json` | Submission details |

## Runtime and seeds

Run limit: 2,400 steps (2 minutes at 20 Hz). The layout is fixed, so always pass `-E object_jitter=0`. There is no
other randomness.

## Tests

```bash
python -m pytest -q      # in this folder, in the yam_arena environment; no GPU needed
```

## Verified in simulation

Isaac Lab-Arena (Isaac Lab 3.0, Isaac Sim 6.1), with the command above.

| Run | `task_score` | What the log and video show |
|---|---|---|
| Scripted demo | **1.0** | The dead bulb is unscrewed in seven half turns and lifted off the thread on the eighth, lowered into the collection box (it stands upright on the box floor); the new bulb is set on the thread, which catches, screwed in with seven half turns and snugged on the contact (peak 0.71 N m, hand-tight latched). Success at step 2,082 (104 s) |
| Dream-1 | **0.0** | The right arm reaches toward the lamp and touches the dead bulb's globe but never unscrews it, then moves over the collection box and back near its base; the dead bulb stays in the lamp. Step limit reached (2,400 steps) |
| `python -m pytest -q` | 8 passed | |

## Real-world build

- **Lamp:** any table lamp with an upright E27 lampholder and a weighted base, its shade taken off, about 8 cm from
  the table to the lampholder's mouth (or a standard E27 lampholder mounted on a weighted base). Unplugged.
- **Bulbs:** two Philips LED classic 60W A60 E27 WW FR ND (12NC 929001243082); one is the "dead" one.
- **Stand and box:** a pine block with a 30 mm hole; a small open cardboard box 10 x 10 x 7 cm.
- **Safety:** the lamp is unplugged during the trial; LED bulbs are light; the arm's force is limited.

## Our assumptions (not from a data sheet or standard)

- **3.5 turns from the first catch to the contact.** IEC 60061-1 gives the cap's thread (pitch, at least 22 mm long),
  but we have not found a published figure for how far a lampholder's thread engages; 3.5 turns (12.7 mm) is our
  estimate for a common lampholder.
- **Hand-tight = 0.3 N m against the contact; forced = 2 N m.** Our thresholds; no standard value for "hand-tight"
  bulb installation.
- **Dropped = over 1.4 m/s downward** (a free fall of about 10 cm): our threshold for a fall that could crack the bulb.
- **Thread running friction 0.05 N m;** the breakaway torque of a hand-tight bulb is not modelled beyond that.
- **The lamp:** its dimensions (base, column, 8.3 cm to the mouth) and 1.2 kg mass are ours; the lampholder body is
  40 mm across like common E27 lampholders.
- **Globe material:** the Philips "LED classic" range is sold as a glass-bulb range; the data sheet does not state
  the globe material, so "fragile glass" is our reading.
- **Grip force on the globe** is not limited or scored (rigid fingers on a rigid globe in simulation).

## Still approximate or unverified

- The thread is emulated (a joint that turns and slides, with friction), not modelled as a helix.
- All parts are rigid; round parts are 16-sided prisms or slices; the globe does not break in simulation.
- Dream-1 (one run, 2,400 steps) did not unscrew the bulb, so the later steps (carrying it, starting and seating the new bulb) were not reached by the model; feasibility rests on the scripted demo.
