"""Self-contained physical task implementation. See task.json for the observable objective and setup.

Executed physics evidence, expert scores and model scores are recorded in validation.json.
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
SUCCESS_HOLD_S = 0.0  # The scorer measures the task-specific stability window once per frame.
EVALUATOR = importlib.import_module(_name+'.scoring').Scorer(SPEC)
OBJECTS = importlib.import_module(_name+'.arena_runtime').install(SPEC, EVALUATOR, HERE)
__doc__ = json.loads((HERE/'task.json').read_text(encoding='utf-8'))['setup']


def success(objects):
    return EVALUATOR.result.success


def score(objects):
    return EVALUATOR.result.score


def demo():
    raise RuntimeError("This task uses the measured-state rc_expert policy. Run task_runner.py --output /data/task-evidence --execute; see README.md.")
