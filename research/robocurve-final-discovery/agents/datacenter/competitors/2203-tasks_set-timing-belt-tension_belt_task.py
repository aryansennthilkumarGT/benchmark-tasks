"""Set the timing belt to the specified tension and secure the motor mount.

The orange pull tab operates the sliding motor plate. The 7 mm socket driver fits
both M4 motor-mount bolts. The fixture-mounted spring gauge applies a 2.5 N test
load at its detent. Green on its 10:1 indicator corresponds to 1.40–1.95 mm actual
midspan deflection. Press the marked blue cap, then return the driver to its cradle.
"""
import os
from math import pi

from yam_arena.constants import FINGER_CLOSED, FINGER_OPEN
from yam_arena.demo import Waypoint
from yam_arena.task_file import Box, TABLE_TOP

from mechanics import PULL_RATIO, START_SPAN

SCENE = "station"
TOP = TABLE_TOP[SCENE]
DRIVEN_X = 0.202
AXIS_Z = TOP + 0.041
BOLT_Y = -0.072
BOLT_X = (0.288, 0.332)
BOLT_Z = TOP + 0.032
DRIVER_LENGTH = 0.053
DRIVER_HOME = (0.165, -0.149, TOP + 0.070)
DRIVER_HOME_YAW = pi / 3
PULL_HOME = (0.271, 0.095, TOP + 0.049)
GAUGE_XY = (DRIVEN_X + 0.055, 0.032)
GAUGE_CAP_Z = TOP + 0.086
GAUGE_TRAVEL = 0.010
GAUGE_CONTACT = 0.0085
HOVER = TOP + 0.131
TARGET_SPAN = 0.11038
INSTRUCTION = (
    "Set the timing belt to the specified tension and secure the motor mount. "
    "Leave the belt seated on both pulleys, then put down the tools and release the assembly."
)

# The fixed deck and driver cradle have native contact colliders. The moving,
# axis-constrained subassembly is implemented by mechanics.Rig.
OBJECTS = [
    Box("joint_fixture_deck", (0.266, 0.004, TOP + 0.007),
        size=(0.224, 0.175, 0.014), color=(0.30, 0.35, 0.39)),
    Box("driver_cradle", (*DRIVER_HOME[:2], TOP + 0.008),
        size=(0.063, 0.051, 0.016), color=(0.19, 0.22, 0.28)),
]


def demo():
    """Fixed Cartesian waypoints. This policy reads only observation time."""
    c, o = FINGER_CLOSED, FINGER_OPEN
    start_yaw = DRIVER_HOME_YAW
    end_yaw = -1.077
    x, y, z = PULL_HOME
    case = os.environ.get("BELT_CONTROL", "nominal")
    target = {"slack": 0.10975, "overtight": 0.11061}.get(case, TARGET_SPAN)
    pull_x = x + (target - START_SPAN) * PULL_RATIO
    left = [
        Waypoint(2.0, (x, y, HOVER), o, "pull-tab approach"),
        Waypoint(1.5, (x, y, z), o, "lower to pull tab"),
        Waypoint(0.9, (x, y, z), c, "grip pull tab"),
        Waypoint(1.4, (pull_x, y, z), c, "set span"),
    ]
    tool_x, tool_y, tool_z = DRIVER_HOME
    right = [
        Waypoint(2.0, (tool_x, tool_y, HOVER), o, "driver approach", start_yaw),
        Waypoint(1.5, DRIVER_HOME, o, "lower to driver", start_yaw),
        Waypoint(0.9, DRIVER_HOME, c, "grasp driver", start_yaw),
        Waypoint(1.3, (tool_x, tool_y, HOVER), c, "lift driver", start_yaw),
    ]
    bolts = () if case == "release-before-tightening" else BOLT_X[:1] if case == "single-bolt-slip" else BOLT_X
    for bx in bolts:
        right.extend([
            Waypoint(1.1, (bx, BOLT_Y, HOVER), c, "above socket", start_yaw),
            Waypoint(1.3, (bx, BOLT_Y, BOLT_Z + DRIVER_LENGTH), c, "engage driver", start_yaw),
            Waypoint(0.45, (bx, BOLT_Y, BOLT_Z + DRIVER_LENGTH), c, "settle socket", start_yaw),
            Waypoint(2.1, (bx, BOLT_Y, BOLT_Z + DRIVER_LENGTH - 0.00019), c, "tighten bolt", end_yaw),
            Waypoint(0.4, (bx, BOLT_Y, BOLT_Z + DRIVER_LENGTH - 0.00021), c, "hold final turn", end_yaw),
            Waypoint(1.1, (bx, BOLT_Y, HOVER), c, "lift from socket", end_yaw),
        ])
    if case == "release-before-tightening":
        right.append(Waypoint(0.8, (tool_x, tool_y, HOVER), c, "no bolts tightened", start_yaw))
    clamp_end = sum(w.duration for w in right)
    left.extend([
        Waypoint(max(0.8, clamp_end - sum(w.duration for w in left) + 0.25), (pull_x, y, z), c, "hold tension"),
        Waypoint(0.9, (pull_x, y, z), o, "release pull tab"),
        Waypoint(1.0, (pull_x, y, HOVER), o, "clear subassembly"),
    ])
    right.extend([
        Waypoint(1.2, (tool_x, tool_y, HOVER), c, "return driver over cradle", start_yaw),
        Waypoint(1.2, DRIVER_HOME, c, "lower driver into cradle", start_yaw),
        Waypoint(0.9, DRIVER_HOME, o, "release driver", start_yaw),
        Waypoint(1.2, (tool_x, tool_y, HOVER + 0.025), o, "clear the tools", start_yaw),
    ])
    left.extend([
        Waypoint(1.1, (*GAUGE_XY, HOVER), c, "approach gauge"),
        Waypoint(1.2, (*GAUGE_XY, GAUGE_CAP_Z + 0.013 - GAUGE_TRAVEL), c, "apply gauge to detent"),
        Waypoint(1.15, (*GAUGE_XY, GAUGE_CAP_Z + 0.013 - GAUGE_TRAVEL), c, "read 2.5 N test"),
        Waypoint(1.25, (*GAUGE_XY, HOVER + 0.025), o, "remove hand from gauge"),
        Waypoint(0.65, (*GAUGE_XY, HOVER + 0.025), o, "hands clear"),
    ])
    return {"left": left, "right": right}
