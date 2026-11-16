"""Install and field-check a shaft-end magnetic motor encoder."""
from math import pi, atan2, cos, sin
import os

import numpy as np
from yam_arena.constants import FINGER_CLOSED, FINGER_OPEN
from yam_arena.demo import Waypoint
from yam_arena.task_file import Box, TABLE_TOP

from geom import Geometry

SCENE = "station"
TOP = TABLE_TOP[SCENE]
MAX_STEPS = 1400
INSTRUCTION = (
    "Install the magnetic encoder on the motor shaft. Seat the magnet carrier, "
    "lower the sensor bracket onto its guide posts, and close its retaining catch. "
    "Press the field-test button, then release the assembly."
)
CASES = ("nominal", "skip-catch", "missing-magnet")
CASE = os.environ.get("ROBOCURVE_FIXTURE_CASE", "nominal")
CENTER = (0.306, 0.010)
DECK = TOP + 0.013
MOTOR_TOP = TOP + 0.077
SHAFT_TOP = TOP + 0.092
MAGNET_TOP = SHAFT_TOP + 0.0040
BOARD_Z = MAGNET_TOP + 0.0015
CAP_SEAT = (*CENTER, MAGNET_TOP + 0.003)
HEAD_SEAT = (*CENTER, BOARD_Z + 0.025)
CAP_HOME = (0.179, -0.148, TOP + 0.044)
HEAD_HOME = (0.269, 0.139, TOP + 0.050)
LATCH_XY = (0.365, -0.054)
LATCH_OPEN = TOP + 0.118
LATCH_TRAVEL = 0.012
TEST_XY = (0.250, -0.124)
TEST_CAP = TOP + 0.052
HOVER = TOP + 0.155

OBJECTS = [
    Box("test_fixture_base", (0.305, 0, TOP + .006), size=(.265, .205, .012),
        color=(.16, .22, .28)),
    Box("carrier_dock", (*CAP_HOME[:2], TOP + .007), size=(.050, .046, .014), color=(.18, .25, .29)),
    Box("encoder_dock", (*HEAD_HOME[:2], TOP + .006), size=(.115, .082, .012), color=(.18, .25, .29)),
]


def configure_demo(case):
    global CASE
    CASE = case


def demo():
    c, o = FINGER_CLOSED, FINGER_OPEN

    def move(duration, position, grip, name, yaw=0.0):
        return Waypoint(duration, position, grip, name, yaw)

    left_park = (0.275, 0.175, HOVER + .018)
    left = [move(2.7, left_park, o, "clear motor"),
            move(7.0, left_park, o, "wait for magnet")]
    left += [
        move(1.2, (*HEAD_HOME[:2], HOVER), o, "approach sensor bracket"),
        move(1.5, HEAD_HOME, o, "reach sensor grip"),
        move(.85, HEAD_HOME, c, "grasp sensor bracket"),
        move(1.2, (*HEAD_HOME[:2], HOVER + .03), c, "lift bracket"),
        move(1.2, (*CENTER, HOVER + .03), c, "align keyed guide"),
        move(1.5, (*CENTER, HEAD_SEAT[2] - .003), c, "seat bracket"),
        move(.65, (*CENTER, HEAD_SEAT[2] - .003), c, "settle bracket"),
        move(.8, (*CENTER, HEAD_SEAT[2] - .003), o, "release bracket"),
        move(1.3, (*CENTER, HOVER + .04), o, "lift clear of bracket"),
        move(1.3, left_park, o, "retract left"),
    ]
    right_park = (0.230, -0.190, HOVER + .020)
    if CASE == "missing-magnet":
        right = [move(2, right_park, o, "clear dock"), move(7.7, right_park, o, "leave carrier in dock")]
    else:
        right = [
            move(1.8, (*CAP_HOME[:2], HOVER), o, "approach carrier"),
            move(1.4, CAP_HOME, o, "reach carrier"),
            move(.85, CAP_HOME, c, "grasp carrier"),
            move(1.3, (*CAP_HOME[:2], HOVER), c, "lift carrier"),
            move(1.3, (*CENTER, HOVER), c, "align D-flat with shaft"),
            move(1.4, (*CENTER, CAP_SEAT[2] - .0025), c, "press carrier onto shaft"),
            move(.75, (*CENTER, CAP_SEAT[2] - .0025), o, "release carrier"),
            move(.9, (*CENTER, HOVER + .025), o, "clear shaft"),
            move(1.1, right_park, o, "clear motor"),
        ]
    delay = max(.4, sum(p.duration for p in left) - .20 - sum(p.duration for p in right))
    right.append(move(delay, right_park, o, "wait for sensor bracket"))
    if CASE != "skip-catch":
        right += [
            move(1.0, (*LATCH_XY, HOVER + .020), c, "approach bracket catch"),
            move(1.5, (*LATCH_XY, LATCH_OPEN + .013 - LATCH_TRAVEL - .002), c, "press catch closed"),
            move(.60, (*LATCH_XY, LATCH_OPEN + .013 - LATCH_TRAVEL - .002), c, "seat catch"),
            move(.9, (*LATCH_XY, HOVER + .020), c, "lift from catch"),
        ]
    right += [
        move(1.0, (*TEST_XY, HOVER), c, "approach test button"),
        move(1.4, (*TEST_XY, TEST_CAP + .005), c, "press field test"),
        move(.70, (*TEST_XY, TEST_CAP + .005), c, "read field check"),
        move(1.0, (*TEST_XY, HOVER), o, "release test button"),
        move(1.0, right_park, o, "retract right"),
    ]
    return {"left": left, "right": right}


def near(hand, xyz, radius):
    return bool(hand.upright and np.linalg.norm(hand.position - xyz) < radius)


def key_matches(yaw):
    return abs(atan2(sin(yaw), cos(yaw))) < .13


class Part:
    def __init__(self, home, seated, tolerance):
        self.xyz = np.array(home)
        self.home = np.array(home)
        self.seat = np.array(seated)
        self.yaw = 0.0
        self.held = None
        self.seated = False
        self.tolerance = tolerance

    def update(self, hands, excluded, locked, blocker):
        if self.held is None and not locked:
            for name, hand in hands.items():
                if name not in excluded and hand.open_fraction < .32 and near(hand, self.xyz, .011):
                    self.held = name
                    break
        if self.held is None:
            return
        hand = hands[self.held]
        self.xyz = hand.position.copy()
        self.yaw = hand.yaw
        self.seated = False
        aligned = (key_matches(self.yaw) and np.linalg.norm(self.xyz[:2] - self.seat[:2]) <= self.tolerance)
        if self.xyz[2] <= self.seat[2] and np.linalg.norm(self.xyz[:2] - self.seat[:2]) < .042:
            self.xyz[2] = self.seat[2] if aligned and not blocker else self.seat[2] + .008
            self.seated = bool(aligned and not blocker)
        if hand.open_fraction > .58:
            self.held = None
            if self.seated:
                self.xyz = self.seat.copy()
                self.yaw = 0
            elif np.linalg.norm(self.xyz - self.home) < .018:
                self.xyz = self.home.copy()
                self.yaw = 0
            else:
                self.xyz[2] = max(TOP + .025, self.xyz[2] - .010)


class State:
    def __init__(self, case="nominal"):
        self.carrier = Part(CAP_HOME, CAP_SEAT, .004)
        self.head = Part(HEAD_HOME, HEAD_SEAT, .005)
        self.latch = False
        self.test_motion = 0.0
        self.test_time = 0.0
        self.test_result = None
        self.ok_time = 0.0

    def advance(self, hands, dt):
        self.carrier.update(hands, (self.head.held,), self.head.seated, self.head.seated)
        self.head.update(hands, (self.carrier.held,), self.latch, False)
        if self.carrier.held or self.head.held:
            self.test_result = None
        if not self.latch and self.head.seated and self.head.held is None:
            for name, hand in hands.items():
                if name != self.carrier.held and hand.open_fraction < .40 and near(
                    hand, (*LATCH_XY, LATCH_OPEN + .013 - LATCH_TRAVEL), .008
                ):
                    self.latch = True
                    break
        self.test_motion = 0.0
        for name, hand in hands.items():
            if name not in (self.carrier.held, self.head.held) and hand.open_fraction < .4 and near(
                hand, (*TEST_XY, TEST_CAP + .006), .008
            ):
                self.test_motion = .006
        if self.test_motion:
            self.test_time += dt
            if self.test_time >= .30:
                self.test_result = bool(self.carrier.seated and self.head.seated and self.latch
                                        and self.carrier.held is None and self.head.held is None)
        else:
            self.test_time = 0.0
        clear = all(hand.position[2] > TOP + .133 or abs(hand.position[1]) > .160 for hand in hands.values())
        score = 0.0
        if self.carrier.seated and self.carrier.held is None:
            score = .25
        if self.head.seated and self.head.held is None and score:
            score = .65 if self.latch else .45
        if score == .65 and self.test_result is True and not self.test_motion and clear:
            score = 1.0
        return {
            "score": score, "carrier": self.carrier.seated, "bracket": self.head.seated,
            "catch": self.latch, "field_check": self.test_result,
            "carrier_grasp": self.carrier.held, "bracket_grasp": self.head.held,
            "air_gap_mm": 1.5 if self.carrier.seated and self.head.seated else None,
            "caption": (
                "Field check passed" if self.test_result else
                "Field check failed" if self.test_result is False else
                "Press the field-test button" if self.latch else
                "Close the retaining catch" if self.head.seated else
                "Seat encoder bracket on both guides" if self.carrier.seated else
                "Seat the magnet carrier on the shaft"
            ),
        }


class View:
    def __init__(self, state):
        g = self.g = Geometry()
        x, y = CENTER
        silver, blue, charcoal = (.62, .67, .72), (.10, .29, .42), (.10, .14, .18)
        gold, pcb, yellow = (.75, .43, .13), (.09, .34, .27), (.85, .57, .09)
        g.cylinder("MotorHousing", (x, y, (DECK + MOTOR_TOP) / 2), .040, MOTOR_TOP - DECK, blue)
        g.cylinder("MotorFace", (x, y, MOTOR_TOP - .002), .039, .006, silver)
        g.cylinder("MotorShaft", (x, y, (MOTOR_TOP + SHAFT_TOP) / 2), .004, SHAFT_TOP - MOTOR_TOP, silver)
        g.box("DFlatReference", (x + .0038, y, SHAFT_TOP - .0035), (.001, .005, .005), blue)
        for i, yoff in enumerate((-.038, .038)):
            g.cylinder(f"Guide{i}", (x, y + yoff, TOP + .080), .004, .060, silver)
            g.cylinder(f"Standoff{i}", (x, y + yoff, TOP + .071), .009, .038, charcoal)
        g.box("LatchStand", (LATCH_XY[0], LATCH_XY[1], TOP + .051), (.022, .034, .082), charcoal)
        g.box("TestBox", (*TEST_XY, TOP + .022), (.062, .051, .041), charcoal)
        self.catch = g.group("RetainingCatch")
        g.box("RedCatch", (0, 0, -.004), (.027, .023, .008), (.65, .10, .08), self.catch)
        g.box("RetainingTongue", (-.017, .015, -.003), (.040, .010, .006), charcoal, self.catch)
        self.test = g.group("TestButton")
        g.cylinder("BlueTestKey", (0, 0, -.004), .009, .008, (.13, .38, .72), self.test)
        self.light = g.sphere("FieldLED", (TEST_XY[0] - .019, TEST_XY[1] + .012, TOP + .045),
                              (.008, .008, .004), (.16, .16, .16))
        self.cap = g.group("MagnetCarrier")
        g.cylinder("CarrierBody", (0, 0, -.010), .012, .020, gold, self.cap)
        g.cylinder("DiscMagnet", (0, 0, -.0035), .003, .0025, silver, self.cap)
        g.box("KeyIndex", (.011, 0, -.004), (.003, .007, .004), charcoal, self.cap)
        self.head = g.group("EncoderBracket")
        g.box("Bridge", (0, 0, -.021), (.071, .095, .010), silver, self.head)
        g.box("CircuitBoard", (0, 0, -.0146), (.047, .045, .0028), pcb, self.head)
        for i, yoff in enumerate((-.038, .038)):
            g.cylinder(f"GuideSocket{i}", (0, yoff, -.023), .007, .012, charcoal, self.head)
        g.box("PinHeader", (-.016, 0, -.009), (.009, .024, .006), charcoal, self.head)
        g.box("InsulatedGrip", (0, 0, 0), (.026, .025, .017), yellow, self.head)
        g.box("LocatorMark", (.019, -.015, -.011), (.008, .009, .003), yellow, self.head)
        self.update(state)

    def update(self, state):
        g = self.g
        g.move(self.cap, state.carrier.xyz, state.carrier.yaw)
        g.move(self.head, state.head.xyz, state.head.yaw)
        g.move(self.catch, (*LATCH_XY, LATCH_OPEN - (.012 if state.latch else 0)))
        g.move(self.test, (*TEST_XY, TEST_CAP - state.test_motion))
        g.color(self.light, (.05, .75, .22) if state.test_result else
                (.76, .09, .08) if state.test_result is False else (.16, .16, .16))
