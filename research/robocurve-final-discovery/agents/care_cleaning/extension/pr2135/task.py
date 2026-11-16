"""On the station table:

- a table lamp with its shade off (free, 1.2 kg): a round weighted base 14 cm across and 2 cm thick, a 24 mm column
  and on top an upright E27 lampholder (body 40 mm across) whose mouth is 8.3 cm above the table;
- screwed into it, a dead bulb: Philips LED classic 60W A60 E27 WW FR ND (12NC 929001243082): frosted A60 bulb 60 mm
  across and 110 mm long, E27 screw cap, 0.040 kg;
- a new bulb of the same model standing cap down in a pine bulb stand (a block with a 30 mm hole);
- a cardboard collection box for spent lamps (open top, 10 x 10 cm inside, 7 cm tall).

The robot must unscrew the dead bulb (counterclockwise seen from above, 3.5 turns from seated to off the thread), put
it into the collection box, and screw the new bulb in (clockwise, 3.5 turns from the thread's first catch) until its
contact touches the lampholder's base contact, and then tighten it by hand (hand-tight), without forcing it.

Run it:  inspect-robots run --embodiment yam_arena -E task=task.py -E object_jitter=0 --scorer task_score ...
"""

from __future__ import annotations

import math
import os
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import numpy as np  # noqa: E402
from jointkit import (Attach, PartState, on_physics, on_reset, part, rot_z, set_attach_target,  # noqa: E402
                      set_attached, set_collision)
from yam_arena.task_file import TABLE_TOP, Box  # noqa: E402

SCENE = "station"
SCORE_OVER = "end"
TOP = TABLE_TOP[SCENE]
INSTRUCTION = "The lamp's bulb is dead. Put it in the collection box and screw the new bulb into the lamp."

WHITE, FROST, BRASS = (0.92, 0.92, 0.90), (0.95, 0.95, 0.93), (0.78, 0.74, 0.62)
BLACK, PINE, CARD = (0.12, 0.12, 0.12), (0.80, 0.64, 0.42), (0.62, 0.48, 0.32)
SIDES = 16


def ring(a_in, a_out, z0, z1, color, sides=SIDES):
    """A 16-sided ring between apothems ``a_in`` and ``a_out`` (m), from z0 to z1 (part frame)."""
    side = 2 * a_out * math.tan(math.pi / sides) * 1.02
    return [(((a_in + a_out) / 2 * math.cos(t), (a_in + a_out) / 2 * math.sin(t), (z0 + z1) / 2),
             (a_out - a_in, side, z1 - z0), color, math.degrees(t))
            for t in (2 * math.pi * k / sides for k in range(sides))]


def disc(a, z0, z1, color, sides=SIDES):
    """A solid 16-sided disc of apothem ``a`` from z0 to z1: sides / 2 full-width boxes turned about z."""
    side = 2 * a * math.tan(math.pi / sides) * 1.02
    return [((0.0, 0.0, (z0 + z1) / 2), (2 * a, side, z1 - z0), color, 360.0 * k / sides) for k in range(sides // 2)]


def fixed(name, lo, hi, color):
    """A fixed box between world corners ``lo`` and ``hi``."""
    lo, hi = np.asarray(lo, float), np.asarray(hi, float)
    return Box(name=name, pos=tuple(float(v) for v in (lo + hi) / 2), size=tuple(float(v) for v in hi - lo),
               color=color)


# -- the E27 thread (IEC 60061-1 sheet 7004-21: 7 threads per inch) ------------------------------------------------
PITCH = 0.0254 / 7                   # 3.629 mm per turn
TURNS = 3.5                          # from the first catch to the contact (see README: our reading of a lampholder)
TRAVEL = PITCH * TURNS               # 12.7 mm

# -- the bulb (origin: on its axis at the tip of the base contact; cap down) ---------------------------------------
# Philips LED classic 60W A60 E27 WW FR ND, 12NC 929001243082: D 60 mm, C 110 mm, 0.040 kg (Philips data sheet).
B_LEN, B_R = 0.110, 0.030
CAP_TOP = 0.026                      # the cap's shell: 22 mm of thread (IEC 60061-1: E27 thread length >= 22 mm)
CREST_A, CORE_A = 0.0132, 0.0121     # thread major 26.4 mm, minor 24.2 mm (as apothems)
CREST = (0.004, 0.008)               # the cap's lowest thread crest (it rides on the lampholder's first thread)
GLOBE_C = B_LEN - B_R                # the globe's centre, 80 mm above the contact
NECK = (CAP_TOP, 0.058, 0.0145, 0.0215)  # the neck tapers from 29 mm to 43 mm across


def bulb_boxes():
    crest = ring(CORE_A - 0.0003, CREST_A, *CREST, BRASS)
    body = (disc(0.0045, 0.0, 0.002, BRASS) + disc(0.010, 0.002, 0.004, BLACK)        # contact and insulator
            + disc(CORE_A, CREST[0], CAP_TOP, BRASS))                                 # the threaded shell
    z0, z1, r0, r1 = NECK
    for k in range(3):
        a, b = z0 + (z1 - z0) * k / 3, z0 + (z1 - z0) * (k + 1) / 3
        body += disc(r0 + (r1 - r0) * (k + 0.5) / 3, a, b, WHITE)
    n = 8
    for k in range(n):
        a, b = z1 + (B_LEN - z1) * k / n, z1 + (B_LEN - z1) * (k + 1) / n
        zm = (a + b) / 2 - GLOBE_C
        body += disc(max(math.sqrt(max(B_R * B_R - zm * zm, 0.0)), 0.004), a, b, FROST)
    return crest + body, range(len(crest))


BULB_BOXES, CRESTS = bulb_boxes()    # CRESTS: indices of the crest boxes in BULB_BOXES

# -- the lamp (origin: on its axis at the table) ----------------------------------------------------------------
XL, YL = 0.29, -0.12                 # the lamp's axis
BASE_A, BASE_H = 0.070, 0.020
SEAT = 0.060                         # the lampholder's base contact: a seated bulb's contact tip is here
BORE_A = 0.0140                      # the lampholder's shell, clear of the cap
LEDGE_A = 0.0123                     # its first thread: the cap's crest rests on it until it is turned
LEDGE_TOP = SEAT + TRAVEL + CREST[0]  # 76.7 mm: the lampholder's first thread
MOUTH = LEDGE_TOP + 0.006            # 82.7 mm: the lampholder's top
HOLDER_A = 0.020                     # 40 mm lampholder body
LAMP_BOXES = (disc(BASE_A, 0.0, BASE_H, WHITE) + disc(0.012, BASE_H, SEAT - 0.006, WHITE)
              + disc(HOLDER_A, SEAT - 0.006, SEAT, BLACK)
              + ring(BORE_A, HOLDER_A, SEAT, LEDGE_TOP - 0.002, BLACK)
              + ring(LEDGE_A, HOLDER_A, LEDGE_TOP - 0.002, LEDGE_TOP, BLACK)
              + ring(0.0165, HOLDER_A, LEDGE_TOP, MOUTH, BLACK))
LAMP = part("table_lamp", pos=(XL, YL, TOP + 0.0005), mass=1.2, color=WHITE, friction=0.8, boxes=LAMP_BOXES)

K_ROT, K_LIN = 3.0, 20000.0
LAMP_SEAT = (0.0, 0.0, SEAT)


def screw(enabled: bool) -> Attach:
    return Attach("table_lamp", pos0=LAMP_SEAT, stiffness=K_ROT, damping=0.02, travel=TRAVEL + 0.002, lin_stiffness=K_LIN,
                  lin_damping=100.0, lin_max_force=40.0, enabled=enabled)


OLD = part("old_bulb", pos=(XL, YL, TOP + SEAT + 0.0005), mass=0.040, color=FROST, friction=0.8, boxes=BULB_BOXES,
           attach=screw(True))

# -- the new bulb's stand and the collection box (fixed) ---------------------------------------------------------
XN, YN = 0.40, -0.27                 # the new bulb's axis in its stand
STAND_H, STAND_HOLE = 0.025, 0.015
NEW = part("new_bulb", pos=(XN, YN, TOP + 0.0055), mass=0.040, color=FROST, friction=0.8, boxes=BULB_BOXES,
           attach=screw(False))
STAND = [fixed("stand_l", (XN - 0.03, YN + STAND_HOLE, TOP), (XN + 0.03, YN + 0.03, TOP + STAND_H), PINE),
         fixed("stand_r", (XN - 0.03, YN - 0.03, TOP), (XN + 0.03, YN - STAND_HOLE, TOP + STAND_H), PINE),
         fixed("stand_f", (XN - 0.03, YN - STAND_HOLE, TOP), (XN - STAND_HOLE, YN + STAND_HOLE, TOP + STAND_H), PINE),
         fixed("stand_b", (XN + STAND_HOLE, YN - STAND_HOLE, TOP), (XN + 0.03, YN + STAND_HOLE, TOP + STAND_H), PINE),
         fixed("stand_floor", (XN - STAND_HOLE, YN - STAND_HOLE, TOP), (XN + STAND_HOLE, YN + STAND_HOLE, TOP + 0.005),
               PINE)]
XB, YB = 0.17, -0.30                 # the collection box's centre
BOX_IN, BOX_H, WALL = 0.050, 0.070, 0.004
BOX = [fixed("box_floor", (XB - BOX_IN - WALL, YB - BOX_IN - WALL, TOP), (XB + BOX_IN + WALL, YB + BOX_IN + WALL,
                                                                             TOP + WALL), CARD),
       fixed("box_l", (XB - BOX_IN - WALL, YB + BOX_IN, TOP), (XB + BOX_IN + WALL, YB + BOX_IN + WALL, TOP + BOX_H), CARD),
       fixed("box_r", (XB - BOX_IN - WALL, YB - BOX_IN - WALL, TOP), (XB + BOX_IN + WALL, YB - BOX_IN, TOP + BOX_H), CARD),
       fixed("box_f", (XB - BOX_IN - WALL, YB - BOX_IN, TOP), (XB - BOX_IN, YB + BOX_IN, TOP + BOX_H), CARD),
       fixed("box_b", (XB + BOX_IN, YB - BOX_IN, TOP), (XB + BOX_IN + WALL, YB + BOX_IN, TOP + BOX_H), CARD)]

OBJECTS = STAND + BOX + [LAMP, OLD, NEW]
BULBS = ("old_bulb", "new_bulb")

# -- the thread (pure Python; the physics hook below feeds it) ---------------------------------------------------
# n: the bulb's net tightening turn (rad, clockwise seen from above), 0 at the first catch, 2 pi TURNS at the contact.
# h: the bulb's contact tip above the lampholder's base contact (m). The thread wants h = PITCH * (TURNS - n / 2 pi).
FRICTION = 0.05                 # N m: running torque of the thread (our assumption: a free-running brass thread)
SLACK = math.radians(30)        # give: the bulb can be turned 30 degrees past where its height says it should be
CONTACT = 0.0003                # m: contact tip on the base contact (0.3 mm allows for the solver's give)
TIGHT = 0.3                     # N m: turned against the contact at least this hard = hand-tight (our assumption)
FORCED = 2.0                    # N m: turned against the contact this hard = forced (our assumption; see README)
RELEASE = math.radians(10)      # unscrewed 10 degrees past the first catch: the bulb is off the thread


def thread_height(n: float) -> float:
    return PITCH * (TURNS - min(max(n, -RELEASE), 2 * math.pi * TURNS) / (2 * math.pi))


class Thread:
    def __init__(self, n: float = 0.0):
        self.reset(n)

    def reset(self, n: float) -> None:
        self.anchor = n
        self.torque = 0.0

    def step(self, n: float, h: float) -> tuple[float, float]:
        pull = K_ROT * (self.anchor - n)  # breakaway friction: a stiff spring to an anchor that slips
        if abs(pull) > FRICTION:
            self.anchor = n + math.copysign(FRICTION, pull) / K_ROT
        # it cannot turn further on than its height allows; with the contact touching, the seat is a hard stop
        n_max = 2 * math.pi * TURNS if h <= CONTACT else 2 * math.pi * (TURNS - h / PITCH) + SLACK
        self.anchor = min(self.anchor, n_max)
        self.torque = K_ROT * max(0.0, n - self.anchor)  # torque the contact takes when the bulb is turned against it
        return self.anchor, thread_height(n)


def _wrap(a: float) -> float:
    return (a + math.pi) % (2 * math.pi) - math.pi


def _twist(lamp: PartState, bulb: PartState) -> float:
    r = lamp.rotation().T @ bulb.rotation()
    return math.atan2(r[1, 0], r[0, 0])


def _relative(lamp: PartState, bulb: PartState):
    """The bulb's contact tip in the lamp frame, relative to the base contact, and its tilt from the lamp's axis."""
    p = lamp.to_local(bulb.pos) - np.array(LAMP_SEAT)
    tilt = math.acos(max(-1.0, min(1.0, float((lamp.rotation().T @ bulb.rotation())[2, 2]))))
    return p, tilt


def can_catch(lamp: PartState, bulb: PartState) -> bool:
    """The cap rests on the lampholder's first thread: on the axis within 3 mm, tilted under 8 degrees, within 3 mm of
    the thread's start, nearly still."""
    p, tilt = _relative(lamp, bulb)
    return bool(math.hypot(p[0], p[1]) < 0.003 and tilt < math.radians(8) and abs(p[2] - TRAVEL) < 0.003
                and np.linalg.norm(bulb.lin_vel - lamp.lin_vel) < 0.05)


FULL = 2 * math.pi * TURNS
THREADS = {b: Thread() for b in BULBS}
_STATE: dict = {}
_DEBUG = [0] if os.environ.get("BULB_DEBUG") else []


def _reset_state(environment=None) -> None:
    THREADS["old_bulb"].reset(FULL)
    THREADS["new_bulb"].reset(0.0)
    _STATE.clear()
    _STATE.update(dropped=False, forced=False, max_torque=0.0)
    for b in BULBS:
        old = b == "old_bulb"
        _STATE[b] = dict(engaged=old, n=FULL if old else 0.0, twist=None, tight=old, catches=0)
        if environment is not None:
            set_attached(environment, b, old)
            set_collision(environment, b, CRESTS, not old)
            if old:
                set_attach_target(environment, b, 0.0, 0.0)


_reset_state()
on_reset(_reset_state)


def _thread_one(environment, name: str, lamp: PartState, bulb: PartState) -> None:
    st, thread = _STATE[name], THREADS[name]
    twist = _twist(lamp, bulb)
    if not st["engaged"]:
        if can_catch(lamp, bulb):
            thread.reset(0.0)
            st.update(engaged=True, n=0.0, twist=twist, catches=st["catches"] + 1, tight=False)
            set_attach_target(environment, name, twist, TRAVEL)
            set_attached(environment, name, True)
            set_collision(environment, name, CRESTS, False)
        return
    if st["twist"] is not None:
        st["n"] -= _wrap(twist - st["twist"])  # clockwise (seen from above) tightens
    st["twist"] = twist
    n = st["n"]
    h = float(_relative(lamp, bulb)[0][2])
    target, height = thread.step(n, h)
    if h <= CONTACT:  # contact touching: turned against it hard enough, it is hand-tight (and stays so)
        _STATE["max_torque"] = max(_STATE["max_torque"], thread.torque)
        st["tight"] |= thread.torque >= TIGHT
        _STATE["forced"] |= thread.torque >= FORCED
    elif h > CONTACT + PITCH / 8:  # backed off (unscrewed 1/8 turn): no longer tight
        st["tight"] = False
    set_attach_target(environment, name, _wrap(twist - (target - n)), height)
    if n < -RELEASE:
        set_attached(environment, name, False)  # unscrewed off the thread
        set_collision(environment, name, CRESTS, True)
        st["engaged"] = False


@on_physics
def _thread(environment) -> None:
    """Every physics step, for each bulb: catch the thread, count the turn, set the screw's drive targets, release."""
    from yam_arena.scene import object_states

    s = object_states(environment, ["table_lamp", *BULBS])
    for b in BULBS:
        _thread_one(environment, b, s["table_lamp"], s[b])
    if _DEBUG:
        _DEBUG[0] += 1
        if _DEBUG[0] % 48 == 0:
            out = []
            for b in BULBS:
                p, tilt = _relative(s["table_lamp"], s[b])
                st = _STATE[b]
                out.append(f"{b} {np.round(s[b].pos * 1000, 1)} rel {np.round(p * 1000, 1)} tilt "
                           f"{math.degrees(tilt):4.1f} eng {st['engaged']} n {math.degrees(st['n']):7.1f} "
                           f"tight {st['tight']} torque {THREADS[b].torque:4.2f}")
            print(f"[bulb] t {_DEBUG[0] / 240:6.2f} lamp {np.round(s['table_lamp'].pos * 1000, 1)}  " + "  ".join(out)
                  + f"  max_torque {_STATE['max_torque']:4.2f}", flush=True)


# -- scoring ---------------------------------------------------------------------------------------------------
OFF_TABLE = TOP - 0.03
DROP_SPEED = 1.4                # m/s downward: a free fall of 10 cm (our assumption for a glass bulb that may crack)


def in_box(bulb: PartState) -> bool:
    """The bulb's cap end inside the collection box: within its inside footprint, below its rim."""
    c = bulb.pos
    return bool(abs(c[0] - XB) < BOX_IN and abs(c[1] - YB) < BOX_IN and c[2] < TOP + BOX_H)


def out_of_lamp(lamp: PartState, bulb: PartState) -> bool:
    p, _ = _relative(lamp, bulb)
    return bool(not _STATE["old_bulb"]["engaged"] and math.hypot(p[0], p[1]) > 0.05)


def _update(objects) -> float:
    lamp, old, new = objects["table_lamp"], objects["old_bulb"], objects["new_bulb"]
    for b in (old, new):
        _STATE["dropped"] |= bool(b.low[2] < OFF_TABLE or b.lin_vel[2] < -DROP_SPEED)
    _STATE["dropped"] |= bool(lamp.tilt() > math.radians(30))  # the lamp knocked over
    if _STATE["dropped"] or _STATE["forced"]:
        return 0.0
    s = 0.0
    if out_of_lamp(lamp, old):
        s += 0.25
        if in_box(old):
            s += 0.25
    st = _STATE["new_bulb"]
    if st["engaged"] and st["n"] >= 2 * math.pi:
        s += 0.25
        if float(_relative(lamp, new)[0][2]) <= CONTACT and st["tight"]:
            s += 0.25
    return s


def success(objects) -> bool:
    """Dead bulb out of the lamp and in the box, new bulb screwed in to the contact and hand-tight; held 1 s."""
    return _update(objects) == 1.0


def score(objects) -> float:
    """0 if a bulb fell off the table or fell freely (over 1.4 m/s downward), the lamp was knocked over, or a bulb was
    forced against the contact (2 N m). Otherwise the sum of: 0.25 dead bulb off the thread and out of the lamp; 0.25
    and in the collection box; 0.25 new bulb threaded at least one full turn; 0.25 and its contact on the lampholder's
    base contact and hand-tight (0.3 N m)."""
    return _update(objects)


# -- scripted demo (pure NumPy plans; demo() wraps them in yam_arena Waypoints) ---------------------------------
OPEN = -0.04695
PINCH = -(B_R - 0.005)               # 5 mm into the globe's equator: a firm hold (rigid fingers on a rigid globe)
GRIP = GLOBE_C                       # TCP above the bulb's contact tip when gripping the globe at its equator
SEATED = TOP + SEAT                  # the bulb's contact tip, seated


def frame(z, x) -> np.ndarray:
    z = np.asarray(z, float) / np.linalg.norm(z)
    x = np.asarray(x, float) - z * np.dot(x, z)
    x /= np.linalg.norm(x)
    return np.column_stack([x, np.cross(z, x), z])


def down(yaw: float) -> np.ndarray:
    """Straight-down grip turned ``yaw`` about the vertical (yam_arena.demo.grip_rotation)."""
    return rot_z(yaw) @ frame((0, 0, -1), (0, -1, 0))


YAW_HI, YAW_LO = 3 * math.pi / 4, -math.pi / 4   # the wrist's working range for half turns
FIX = np.array([float(v) for v in os.environ.get("DEMO_FIX", "0,0,0").split(",")])  # right arm's tracking error
EXTRA = math.radians(float(os.environ.get("DEMO_EXTRA", "35")))   # last tightening half turn goes this much further
SNUG = math.radians(float(os.environ.get("DEMO_SNUG", "25")))     # then a short turn to snug it against the contact
LIFT = 0.025


def _at(z: float) -> tuple:
    return (XL + FIX[0], YL + FIX[1], z + FIX[2])


def _strokes(k: int, h0: float, sign: int, extra: float = 0.0, last_lift: bool = False):
    """``k`` half turns of the bulb (sign -1: clockwise = in, +1: counterclockwise = out), the hand following the
    thread; between turns it lets go, rises and turns back. The last turn goes ``extra`` further; with ``last_lift``
    the hand keeps hold after the last turn and lifts the bulb off the thread."""
    plan, h = [], h0
    a0 = YAW_HI if sign < 0 else YAW_LO
    for i in range(k):
        last = i == k - 1
        end = a0 + sign * (math.pi + (extra if last else 0.0))
        h1 = min(h + PITCH / 2, TRAVEL + 0.004) if sign > 0 else max(h - PITCH / 2, 0.0)
        z0, z1 = SEATED + h + GRIP, SEATED + h1 + GRIP
        plan += [(1.0, _at(z0 + 0.015), down(a0), OPEN, "over the bulb"), (0.7, _at(z0), down(a0), OPEN, "down"),
                 (0.6, _at(z0), down(a0), PINCH, "grip"),
                 (1.1, _at((z0 + z1) / 2), down((a0 + end) / 2), PINCH, "turn"),
                 (1.1, _at(z1), down(end), PINCH, "turn")]
        if last and last_lift:
            plan += [(1.0, _at(z1 + LIFT), down(end), PINCH, "lift it off the thread")]
        else:
            plan += [(0.5, _at(z1), down(end), OPEN, "let go"), (0.5, _at(z1 + 0.015), down(end), OPEN, "up")]
        h = h1
    return plan


HIGH = 0.19                          # travel height of the TCP above the table


def plan() -> dict[str, list]:
    n = int(round(2 * TURNS))        # 7 half turns
    right = [(2.5, _at(TOP + HIGH), down(YAW_LO), OPEN, "over the lamp")]
    # out: 7 half turns counterclockwise, the 8th lifts it off the thread
    right += _strokes(n + 1, 0.0, +1, last_lift=True)
    yaw = down(math.pi / 4)          # the wrist turns back to mid-range while carrying (the globe is round)
    box = np.array([XB, YB])
    right += [(2.0, (*box, TOP + HIGH), yaw, PINCH, "over the collection box"),
              (1.5, (*box, TOP + WALL + 0.012 + GRIP), yaw, PINCH, "down into the box"),
              (0.6, (*box, TOP + WALL + 0.012 + GRIP), yaw, -0.040, "let go"),
              (1.0, (*box, TOP + HIGH), yaw, -0.040, "up")]
    stand = np.array([XN, YN, TOP + 0.005 + GRIP])
    g = down(math.pi / 4)
    right += [(2.0, stand + [0, 0, 0.04], g, OPEN, "over the new bulb"), (1.2, stand, g, OPEN, "down"),
              (0.6, stand, g, PINCH, "grip the new bulb"), (1.2, stand + [0, 0, 0.06], g, PINCH, "lift it out"),
              (2.0, _at(SEATED + TRAVEL + GRIP + 0.03), g, PINCH, "over the lamp"),
              (2.0, _at(SEATED + TRAVEL + GRIP - 0.001), g, PINCH, "cap onto the thread"),
              (0.5, _at(SEATED + TRAVEL + GRIP - 0.001), g, OPEN, "let go"),
              (0.5, _at(SEATED + TRAVEL + GRIP + 0.015), g, OPEN, "up")]
    # in: 7 half turns clockwise, the last 35 degrees further (the fingers slip a little on the globe), then a short
    # turn of 25 degrees: the contact touches and the bulb is turned on against it (hand-tight)
    right += _strokes(n, TRAVEL, -1, extra=EXTRA)
    a0 = YAW_HI - EXTRA              # the hand turns back half a turn from where the last half turn ended
    a1, z = a0 - SNUG, SEATED + GRIP
    right += [(0.6, _at(z + 0.015), down(a0 - math.pi / 2), OPEN, "turn back"),
              (0.6, _at(z + 0.015), down(a0), OPEN, "over the bulb"), (0.7, _at(z), down(a0), OPEN, "down"),
              (0.6, _at(z), down(a0), PINCH, "grip"), (1.0, _at(z), down(a1), PINCH, "snug it"),
              (0.5, _at(z), down(a1), OPEN, "let go"), (0.5, _at(z + 0.015), down(a1), OPEN, "up")]
    right += [(1.0, _at(TOP + HIGH), right[-1][2], OPEN, "clear")]
    return {"right": right}


def demo():
    """Right arm: grips the dead bulb's globe and unscrews it in counterclockwise half turns, regripping between them,
    lifts it off the thread and lowers it into the collection box; takes the new bulb out of its stand, sets its cap
    on the lampholder's thread and screws it in in clockwise half turns until it is hand-tight."""
    from yam_arena.demo import Waypoint

    return {arm: [Waypoint(d, tuple(p), f, label, r) for d, p, r, f, label in wps] for arm, wps in plan().items()}
