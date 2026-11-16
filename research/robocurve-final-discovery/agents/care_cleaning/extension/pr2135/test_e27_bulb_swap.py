"""Checks that need no GPU: the task file loads, the thread is the real E27 one, the scoring latches, the demo is
reachable."""

import math
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import task  # noqa: E402
from yam_arena import station  # noqa: E402
from yam_arena.demo import ArmPlan  # noqa: E402
from yam_arena.task_file import load  # noqa: E402


def test_loads():
    t = load(HERE / "task.py")
    assert t.success and t.score and t.demo
    assert {"table_lamp", "old_bulb", "new_bulb"} <= set(t.free_objects)


def test_text_is_ascii():
    for s in (task.__doc__, task.INSTRUCTION):
        s.encode("ascii")


def test_real_thread():
    # E27: 7 threads per inch (3.629 mm a turn), 3.5 turns from the first catch to the contact
    assert abs(task.PITCH - 0.0254 / 7) < 1e-9
    assert abs(task.TURNS - 3.5) < 1e-9
    assert abs(task.thread_height(0.0) - task.TRAVEL) < 1e-9
    assert abs(task.thread_height(task.FULL)) < 1e-12
    assert task.thread_height(task.FULL - 1.0) > task.CONTACT  # 57 degrees short: contact not touching


def test_real_bulb():
    # Philips LED classic 60W A60 E27: 60 mm across, 110 mm long
    assert abs(task.B_LEN - 0.110) < 1e-9 and abs(2 * task.B_R - 0.060) < 1e-9
    assert task.OLD.mass == task.NEW.mass == 0.040
    assert 2 * task.CREST_A > 2 * task.LEDGE_A > 2 * task.CORE_A  # the crest rests on the first thread, the shell passes


def test_hand_tight_and_forced():
    t = task.Thread(task.FULL)
    t.step(task.FULL, 0.0)
    assert t.torque < task.TIGHT                                  # just touching: not tight
    t.step(task.FULL + 1.5 * task.TIGHT / task.K_ROT, 0.0)
    assert task.TIGHT <= t.torque < task.FORCED                   # turned on against the contact: hand-tight
    t.step(task.FULL + 1.1 * task.FORCED / task.K_ROT, 0.0)
    assert t.torque >= task.FORCED                                # forced


def test_demo_turns_enough():
    labels = [w.label for w in task.demo()["right"]]
    assert labels.count("grip") >= 4 * task.TURNS                 # half turns out and in


def test_demo_reachable():
    for arm, ws in task.demo().items():
        p = ArmPlan(list(ws), station.BASES[arm])
        for k in range(int(p.duration * 20) + 5):
            p.action7((k + 1) / 20)
        assert p.worst_ik_mm < 0.5 and p.worst_ik_deg < 0.1, arm


def test_run_limit_covers_demo():
    d = sum(w.duration for w in task.demo()["right"])
    assert d * 20 + 60 < 2400
