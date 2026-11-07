"""Draft hardware-maintenance task. See task.json for the observable objective and setup.

No physics feasibility, expert score, or Dream score has been established.
"""
import hashlib
import importlib
import json
from pathlib import Path
import sys
import types

HERE = Path(__file__).resolve().parent
_name = '_rc_' + hashlib.sha256(str(HERE).encode()).hexdigest()[:16]
if _name not in sys.modules:
    _package = types.ModuleType(_name)
    _package.__path__ = [str(HERE)]
    sys.modules[_name] = _package
SPEC = json.loads((HERE/'scene.json').read_text(encoding='utf-8'))
SCENE = 'station'
SCORE_OVER = 'end'
SUCCESS_HOLD_S = 0.0  # The scorer itself measures the one-second hold exactly once per frame.
EVALUATOR = importlib.import_module(_name+'.scoring').Scorer(SPEC)
OBJECTS = importlib.import_module(_name+'.arena_runtime').install(SPEC, EVALUATOR, HERE)
__doc__ = json.loads((HERE/'task.json').read_text(encoding='utf-8'))['setup']


def success(objects):
    return EVALUATOR.result.success


def score(objects):
    return EVALUATOR.result.score


def demo():
    from yam_arena.demo import Waypoint
    from yam_arena.constants import FINGER_OPEN, FINGER_CLOSED
    plan = json.loads((HERE/'expert_plan.json').read_text(encoding='utf-8'))
    if plan['status'] != 'EXECUTABLE_DRAFT_UNVALIDATED':
        raise ValueError('Unexpected plan status')
    return {side: [Waypoint(w['duration'], tuple(w['pos']), FINGER_OPEN if w['open'] else FINGER_CLOSED,
                            w['label'], w.get('yaw', 0.0)) for w in moves]
            for side, moves in plan['arms'].items()}
