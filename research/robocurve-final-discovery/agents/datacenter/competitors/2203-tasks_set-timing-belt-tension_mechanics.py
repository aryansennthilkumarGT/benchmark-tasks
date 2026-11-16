"""Mechanism and outcome checks for a free-running, unpowered joint fixture.

Lengths are metres, forces are newtons, angles are radians. The mechanism has one
sliding axis, two threaded clamp loads, and a test-force gauge.
"""
from dataclasses import dataclass, field
from math import atan2, cos, exp, hypot, pi, sin

CONTROL_HZ = 20
BELT_PITCH = 0.005
BELT_TEETH = 60
PULLEY_TEETH = 16
BELT_WIDTH = 0.009
PITCH_RADIUS = PULLEY_TEETH * BELT_PITCH / (2 * pi)
FREE_SPAN = (BELT_TEETH - PULLEY_TEETH) * BELT_PITCH / 2
START_SPAN = FREE_SPAN - 0.00075
MIN_SPAN, MAX_SPAN = 0.108, 0.112
TEST_FORCE = 2.5
TARGET_DEFLECTION = (0.00140, 0.00195)
SPAN_STIFFNESS = 100_000.0
PULL_RATIO = 8.0
HOLD_TOLERANCE = 0.000040
ALIGNMENT_LIMIT = 0.00050
YAW_LIMIT = 0.5 * pi / 180
BOLT_PITCH = 0.00070
CLAMP_GAP = 0.000105
CLAMP_STIFFNESS = 1_900_000.0
SECURE_LOAD = 185.0
MAX_LOAD = 245.0
MAX_ANGLE = (CLAMP_GAP + MAX_LOAD / CLAMP_STIFFNESS) * (2 * pi) / BOLT_PITCH
STATIC_FRICTION = 0.29
SLIDE_DAMPING = 3500.0


def span_tension(span, deflection=0.0):
    return SPAN_STIFFNESS * max(0.0, hypot(span, 2 * deflection) - FREE_SPAN)


def midspan_deflection(span, force=TEST_FORCE):
    """Solve 2 T sin(theta) = force, including stretch from the probe."""
    if force <= 0:
        return 0.0
    low, high = 0.0, 0.022
    for _ in range(25):
        d = (low + high) / 2
        normal_force = 4 * span_tension(span, d) * d / hypot(span, 2 * d)
        if normal_force < force:
            low = d
        else:
            high = d
    return (low + high) / 2


def preload(turn):
    travel = turn * BOLT_PITCH / (2 * pi)
    return CLAMP_STIFFNESS * max(0.0, travel - CLAMP_GAP)


def angle_delta(now, before):
    return atan2(sin(now - before), cos(now - before))


@dataclass
class Rig:
    span: float = START_SPAN
    bolts: list[float] = field(default_factory=lambda: [0.0, 0.0])
    seated: bool = True
    offset: float = 0.00010
    yaw: float = 0.0
    held: bool = False
    gauge_loaded: bool = False
    checking_since: float = 0.0
    checked_mm: float | None = None
    check_min: float | None = None
    check_max: float | None = None
    slip: float = 0.0
    peak_tension_span: float = START_SPAN

    @property
    def clamp(self):
        return tuple(preload(bolt) for bolt in self.bolts)

    @property
    def secured(self):
        return min(self.clamp) >= SECURE_LOAD

    @property
    def drift(self):
        if self.check_min is None or self.check_max is None:
            return 0.0
        return self.check_max - self.check_min

    def invalidate_check(self):
        self.checking_since = 0.0
        self.checked_mm = None
        self.check_min = self.check_max = None

    def step(self, *, dt=1 / CONTROL_HZ, pull=None, bolt=None, clockwise=0.0, gauge=False):
        was_held = self.held
        self.held = pull is not None
        self.gauge_loaded = gauge and self.seated
        if self.held and not was_held:
            self.invalidate_check()
        if bolt is not None and abs(clockwise) > 1e-5:
            before = self.bolts[bolt]
            self.bolts[bolt] = min(MAX_ANGLE, max(0.0, before + clockwise))
            if self.bolts[bolt] != before:
                self.invalidate_check()

        before = self.span
        normal = span_tension(before) if self.seated else 0.0
        defl = midspan_deflection(before) if self.gauge_loaded else 0.0
        restoring = normal + (span_tension(before, defl) * before / hypot(before, 2 * defl)
                              if self.seated else 0.0)
        friction = STATIC_FRICTION * sum(self.clamp)
        if self.held:
            # The back-drivable 8:1 pull fixture sets displacement while the operator
            # holds it. Its available 25 N input limits carriage force to 200 N.
            target = min(MAX_SPAN, max(MIN_SPAN, pull))
            drive = max(-200.0, min(200.0, (target - before) * 950_000.0 + restoring))
            net = drive - restoring
            if abs(net) > friction:
                direction = 1 if net > 0 else -1
                delta = direction * (abs(net) - friction) / (950_000.0) * (1 - exp(-dt / 0.055))
                self.span = min(MAX_SPAN, max(MIN_SPAN, before + delta))
        elif restoring > friction:
            # Backward movement reduces restoring force. Limit a discrete step to
            # the steady solution instead of overshooting to a fictitious slack state.
            low, high = MIN_SPAN, before
            for _ in range(20):
                q = (low + high) / 2
                d = midspan_deflection(q) if self.gauge_loaded else 0
                load = (span_tension(q) + span_tension(q, d) * q / hypot(q, 2 * d)
                        if self.seated else 0.0)
                if load < friction + 1e-8:
                    low = q
                else:
                    high = q
            self.span = max(low, before - (restoring - friction) * dt / SLIDE_DAMPING)
            self.slip += before - self.span
        self.peak_tension_span = max(self.span, self.peak_tension_span)

        if self.check_min is not None:
            self.check_min = min(self.check_min, self.span)
            self.check_max = max(self.check_max, self.span)
        if self.gauge_loaded and not self.held:
            if self.check_min is None:
                self.check_min = min(before, self.span)
                self.check_max = max(before, self.span)
            self.checking_since += dt
            if self.checking_since >= 0.45:
                self.checked_mm = midspan_deflection(self.span) * 1000
        elif not self.held:
            self.checking_since = 0.0

    def outcome(self, tools_parked=True, hands_clear=True):
        measured = None if self.checked_mm is None else self.checked_mm / 1000
        aligned = abs(self.offset) <= ALIGNMENT_LIMIT and abs(self.yaw) <= YAW_LIMIT
        released = not self.held and not self.gauge_loaded and tools_parked and hands_clear
        stable = measured is not None and self.drift <= HOLD_TOLERANCE
        in_range = measured is not None and TARGET_DEFLECTION[0] <= measured <= TARGET_DEFLECTION[1]
        secure = released and self.seated and aligned and self.secured and stable
        return 1.0 if secure and in_range else 0.25 if secure else 0.0
