# Reload a receipt printer: hold the sprung cover back, turn the roll so paper feeds out the front, let the cover close

## Task Overview

The receipt printer has run out of paper. Fit the new roll so that the paper feeds out of the front slot, leave the cover closed, and let go with both fingers at least 3 cm from the printer and the roll.

Cashiers (O*NET 41-2011.00, well over 500,000 US workers) change the receipt roll at the till regularly. A thermal roll must unwind the way the printer expects or it prints blank, and the roll sits under a spring cover that is held back while it goes in. Source: Epson TM-T20II User's Manual, Installing Roll Paper: "insert the roll paper. The correct direction of the paper is shown in the illustration below." (https://cdn.shopify.com/s/files/1/0026/6377/6307/files/tm-t20ii_Users_Manual.pdf). The ability: one hand holds the sprung cover back while the other turns the roll a quarter turn so its orange-taped free end leads toward the slot. Why a robot task: two hands, a spring and an orientation read off the scene. Closest on the board: TK-GPFKUG (pusher held back, nothing to turn), TK-S2ZZAS (lid held open). No receipt-roll card among 477 titles; new here: the free end decides the turn.

## Setup & Starting Configuration

Positions are object centres in cm from the midpoint between the arm bases (x forward, y left), z above the bench top (z = 0.7475 m, hardwood, friction 0.5). Materials: charcoal ABS printer, black ABS cover with a blue push tab, white thermal paper on a brown cardboard core, black rubber stand. Printer (fixed, 25 kg stand-in for a bolted-down desktop printer, friction 1.2): 14 x 20 x 10 cm at (26, 0), x 19 to 33, z 0 to 10. Open-top paper bay with its floor at z 3.0: front posts x 19 to 21 (y +/-4.5 to +/-10) leave a 9 cm wide exit slot open to the cover, its floor flush with the chute; side walls y +/-6.5 to +/-10; rear wall x 29.2 to 33; bay 8.2 cm front to back (x 21 to 29.2). Two cradle shoulders (y +/-3.4 to +/-6.5, 1.2 cm tall) make a 6.8 cm wide roll channel and leave 13 cm between the walls for the gripper pads. Chute apron 8 x 10 x 3 cm in front (x 11 to 19). A status lamp (red, green or amber, display only) and a power button sit on the front face. Cover (one sprung slide along +x, 150 g): a 14 x 20 x 1.0 cm plate resting on the walls (z 10.0 to 11.0) with three 3 mm grip ribs and a clear window; travel 12.5 cm, spring 8 N/m (1.0 N at full travel), damping 5 N s/m, no wall friction. A side arm (y +10 to +16) carries a blue push tab 1.2 x 4 x 4 cm, front face at x 17.8, z 6.9 to 10.9. The bay is open once the cover has slid 10.5 cm; a seated roll's top is 7 mm under the closed cover. Roll (loose, 90 g, friction 0.5): 58 mm wide, 60 mm across, 25 mm core; a rigid 12 x 5.8 x 0.3 cm paper strip (the free end, tipped with orange tape) runs from under it. Stand (fixed, 25 kg, friction 1.2): rubber plate 9 x 14 x 1 cm at (14, -14) with one chock 4 x 1.6 x 2.2 cm, 8.5 mm behind the roll on the +y side. At the start the roll's axis runs along x, its centre at (14, -14, z 4.3), and its free end runs toward -y. Correct seating: roll centre (25.1, 0, z 6.3), axis along y, free end toward -x on the floor and the chute, tip at x 13.1 (6 cm outside the front face). Both arms start open at ready (about (10, -/+14)). The layout is the same in every trial. Real build: a printed or sheet-metal printer bolted to the bench (this replaces the 25 kg mass), a real 58 mm thermal roll with a card strip taped to its end, and a 1 cm rubber pad on the bench.

## Reset

Cover closed (lamp red); roll on its stand with its axis along x, its centre at (14, -14, z 4.3) and its free end running toward -y; both grippers open and clear at ready; bench clear. The first video frame shows the closed printer with a red lamp and the roll on its stand.

## Scoring

Final state plus the run's facts. COVER CLOSED: the cover within 2 mm of its rest. SEATED: roll centre within 12 mm in x, 8 mm in y and 3 mm in z of (25.1, 0, z 6.3), axis within 5 degrees of y, level within 5 degrees. FEEDS: the paper's free end at x <= 17.0 cm (at least 2 cm outside the front face), within 2 cm of y 0 and below z 4.5 cm. RELEASED: both gripper centres at least 3 cm from the printer, cover and roll, and both grippers at least 90% open. STILL: the roll and the cover each move less than 1 mm over the last 1 s and the roll is slower than 1 cm/s. Zero: the printer or the stand is shifted more than 5 mm at any time (permanent); the roll ends seated with its free end toward the rear wall (+x); the roll ends anywhere other than on the stand or in the bay. 1.0: COVER CLOSED, SEATED, FEEDS, RELEASED, STILL. 0.75: the same but RELEASED or STILL fails. 0.5: SEATED and FEEDS with the cover not closed (held or stuck). 0.25: the cover was held open (10.5 cm or more) for at least 1 s in a row and the roll was lifted at least 3 cm from the stand at some time, and the roll is back on the stand or seated. Else 0. Doing nothing scores 0; a held or hovering roll does not count as seated. Possible scores: 0.0, 0.25, 0.5, 0.75, 1.0. Real trial: tape (2 cm outside, 1.2 cm centring), a feeler gauge for the closed cover, a top and a front photo.

## Fidelity

A real printer has a hinged, latched lid and a slot between lid and body; here the cover is a sprung slide (no proven hinge in the simulator) and the front exit is a 9 cm open notch so a rigid strip can be lowered into it. The paper's free end is a rigid 3 mm strip (real paper is flexible); the roll does not spin or unwind and its core is solid. The printer is a fixed 25 kg stand-in (a real one is a light desktop unit). The lamp and the orange tape are display markers, never scored.

## Execution

```bash
bash run.sh settle     # 10 s hold at ready pose (200 steps)
bash run.sh demo       # scripted two-arm demo, 1,500 steps
bash run.sh ablation   # left arm idle (ABLATION_ARM=right: right arm idle), 1,200 steps
bash run.sh dream      # Dream-1 policy
```

Run limit: 1,500 steps (75 seconds at 20 Hz). The scripted demo takes about 28 s (about 554 control steps at 20 Hz). Object jitter is disabled (object_jitter=0), so there are no random seeds.
