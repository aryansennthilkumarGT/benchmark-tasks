"""Run the belt fixture inside the standard Inspect Robots / YAM station."""
import argparse
import json
import os
import sys
from dataclasses import dataclass
from math import acos, atan2, pi
from pathlib import Path

import numpy as np
from yam_arena import ik, inspect_embodiment
from yam_arena.constants import FINGER_OPEN, PAD_TIP_PAST_TCP
from yam_arena.demo import grip_rotation

import belt_task as task
from mechanics import PULL_RATIO, Rig, START_SPAN, angle_delta


@dataclass
class Hand:
    position: np.ndarray
    grip: float
    yaw: float
    downward: bool


class Contacts:
    """Constrain only the degrees of freedom provided by the physical interfaces."""

    def __init__(self, case):
        self.rig = Rig(seated=case != "unseated", offset=0.0012 if case == "misaligned" else 0.0001)
        self.driver_xyz = np.array(task.DRIVER_HOME)
        self.driver_yaw = task.DRIVER_HOME_YAW
        self.driver_owner = None
        self.driver_parked = True
        self.pull_owner = None
        self.pull_origin = task.PULL_HOME[0]
        self.pull_span = START_SPAN
        self.socket = None
        self.engagement_yaw = 0.0
        self.gauge_travel = 0.0

    @property
    def pull_xyz(self):
        return np.array(task.PULL_HOME) + ((self.rig.span - START_SPAN) * PULL_RATIO, 0, 0)

    def advance(self, hands, dt):
        if self.driver_owner is not None:
            hand = hands[self.driver_owner]
            self.driver_xyz = hand.position.copy()
            self.driver_yaw = hand.yaw
            if hand.grip >= 0.58:
                self.driver_owner = None
                self.driver_parked = bool(np.linalg.norm(self.driver_xyz - task.DRIVER_HOME) < 0.012)
                if self.driver_parked:
                    self.driver_xyz = np.array(task.DRIVER_HOME)
                    self.driver_yaw = task.DRIVER_HOME_YAW
                else:
                    self.driver_xyz[2] = task.TOP + task.DRIVER_LENGTH
        if self.driver_owner is None:
            for name, hand in hands.items():
                if (name != self.pull_owner and hand.downward and hand.grip < 0.30
                        and np.linalg.norm(hand.position - self.driver_xyz) < 0.009):
                    self.driver_owner, self.driver_parked = name, False
                    break

        if self.pull_owner is not None:
            hand = hands[self.pull_owner]
            if (hand.grip >= 0.58 or abs(hand.position[1] - task.PULL_HOME[1]) > 0.012
                    or abs(hand.position[2] - task.PULL_HOME[2]) > 0.012):
                self.pull_owner = None
        if self.pull_owner is None:
            for name, hand in hands.items():
                if (name != self.driver_owner and hand.grip < 0.30 and hand.downward
                        and np.linalg.norm(hand.position - self.pull_xyz) < 0.009):
                    self.pull_owner = name
                    self.pull_origin = hand.position[0]
                    self.pull_span = self.rig.span
                    break
        pull = None
        if self.pull_owner is not None:
            pull = self.pull_span + (hands[self.pull_owner].position[0] - self.pull_origin) / PULL_RATIO

        bolt, turn = None, 0.0
        if self.driver_owner is not None and hands[self.driver_owner].downward:
            tip = self.driver_xyz - (0, 0, task.DRIVER_LENGTH)
            for i, bx in enumerate(task.BOLT_X):
                drop = self.rig.bolts[i] * 0.00070 / (2 * pi)
                if (np.linalg.norm(tip[:2] - (bx, task.BOLT_Y)) <= 0.0035
                        and abs(tip[2] - (task.BOLT_Z - drop)) <= 0.0026):
                    phase = (self.driver_yaw + self.rig.bolts[i] + pi / 6) % (pi / 3) - pi / 6
                    if self.socket == i or abs(phase) <= 0.24:
                        bolt = i
                        if self.socket == i:
                            turn = -angle_delta(self.driver_yaw, self.engagement_yaw)
                        break
        self.socket = bolt
        self.engagement_yaw = self.driver_yaw

        self.gauge_travel = 0.0
        for name, hand in hands.items():
            tip_z = hand.position[2] - PAD_TIP_PAST_TCP
            if (name not in (self.driver_owner, self.pull_owner) and hand.downward and hand.grip < 0.40
                    and np.linalg.norm(hand.position[:2] - task.GAUGE_XY) < 0.010
                    and task.GAUGE_CAP_Z - 0.024 < tip_z < task.GAUGE_CAP_Z):
                self.gauge_travel = min(task.GAUGE_TRAVEL, task.GAUGE_CAP_Z - tip_z)

        self.rig.step(dt=dt, pull=pull, bolt=bolt, clockwise=turn, gauge=bool(self.gauge_travel >= task.GAUGE_CONTACT))
        hands_clear = all(
            h.position[2] > task.TOP + 0.110 or h.position[1] < -0.108 or h.position[1] > 0.115
            for h in hands.values()
        )
        return self.rig.outcome(tools_parked=self.driver_parked, hands_clear=hands_clear)

    def status(self, score):
        return dict(
            span_mm=round(self.rig.span * 1000, 4),
            clamp_n=[round(n, 2) for n in self.rig.clamp],
            gauge_mm=None if self.rig.checked_mm is None else round(self.rig.checked_mm, 4),
            test_loaded=self.rig.gauge_loaded,
            lever_arm=self.pull_owner,
            driver_arm=self.driver_owner,
            socket=self.socket,
            driver_parked=self.driver_parked,
            seated=self.rig.seated,
            drift_mm=round(self.rig.drift * 1000, 5),
            slip_mm=round(self.rig.slip * 1000, 5),
            score=score,
        )


def bind_task(path, case, output):
    cls = inspect_embodiment.YamArenaEmbodiment
    reset, advance = cls.reset, cls._task_step

    def is_this(instance):
        return instance.task is not None and instance.task.path == path

    def reset_fixture(self, *args, **kwargs):
        obs = reset(self, *args, **kwargs)
        if not is_this(self):
            return obs
        from rig_view import FixtureView

        self._belt = Contacts(case)
        self._belt_view = FixtureView(self._belt)
        self._belt_pass_steps = 0
        self._belt_trace = (output / "mechanism.jsonl").open("w", encoding="utf-8")
        for _ in range(8):
            self._base.sim.render()
        for name in ("top_cam", "left_cam", "right_cam"):
            self._base.scene[name].update(self._base.step_dt, force_recompute=True)
        screenshot = os.environ.get("BELT_SETUP_PNG")
        if screenshot:
            import cv2

            rgb = self._base.scene["top_cam"].data.output["rgb"]
            rgb = rgb.torch if hasattr(rgb, "torch") else rgb
            cv2.imwrite(screenshot, cv2.cvtColor(rgb[0, ..., :3].cpu().numpy(), cv2.COLOR_RGB2BGR))
        return self._observation()

    def step_fixture(self):
        if not is_this(self):
            return advance(self)
        from inspect_robots.types import StepResult

        hands = {}
        down = grip_rotation()
        for arm in ("left", "right"):
            name = arm + "_robot"
            arm_ids, finger_ids = self._ids[name]
            joints = self._base.scene[name].data.joint_pos.torch[0]
            pos, rot = ik.tcp_pose(joints[arm_ids].cpu().numpy(), self.rig.bases[arm])
            spin = rot @ down.T
            hands[arm] = Hand(pos, float(joints[finger_ids].mean().item() / FINGER_OPEN),
                              atan2(spin[1, 0], spin[0, 0]),
                              acos(float(np.clip(rot[:, 2] @ down[:, 2], -1, 1))) < 0.22)
        grade = self._belt.advance(hands, self._base.step_dt)
        self._belt_view.update(self._belt)
        self._belt_pass_steps = self._belt_pass_steps + 1 if grade == 1 else 0
        complete = self._belt_pass_steps >= 5
        info = self._belt.status(grade)
        info["success"] = complete
        info["hands"] = {arm: [*map(float, h.position), h.grip, h.yaw, bool(h.downward)]
                         for arm, h in hands.items()}
        self._belt_trace.write(json.dumps({"t": round(self._t, 5), **info}) + "\n")
        self._belt_trace.flush()
        return StepResult(observation=self._observation(), terminated=complete,
                          termination_reason="success" if complete else None, info=info)

    cls.reset, cls._task_step = reset_fixture, step_fixture


def main():
    from inspect_robots.cli import main as inspect_main

    parser = argparse.ArgumentParser()
    parser.add_argument("policy", choices=("yam_scripted", "dream"))
    parser.add_argument("--log-dir", type=Path, required=True)
    parser.add_argument("--control", default="nominal", choices=(
        "nominal", "slack", "overtight", "single-bolt-slip", "release-before-tightening", "unseated", "misaligned"))
    args, rest = parser.parse_known_args()
    args.log_dir.mkdir(parents=True, exist_ok=True)
    path = Path(__file__).with_name("belt_task.py").resolve()
    os.environ["BELT_CONTROL"] = args.control
    bind_task(path, args.control, args.log_dir)
    sys.argv[1:] = [
        "run", "--embodiment", "yam_arena", "--policy", args.policy,
        "-E", f"task={path}", "-E", "object_jitter=0", "-E", "control_hz=20",
        "-E", "cam_width=320", "-E", "cam_height=176",
        "--instruction", task.INSTRUCTION, "--scorer", "task_score", "--max-steps", "1400",
        "--store-frames", "--log-dir", str(args.log_dir), *rest,
    ]
    inspect_main()


if __name__ == "__main__":
    main()
