"""Inspect Robots policy wrapping the measured-state task controller."""
import importlib
import json
import os
from pathlib import Path
import numpy as np
from inspect_robots.policy import PolicyBase, PolicyInfo
from inspect_robots.types import Action, ActionChunk
from inspect_robots_yam.config import action_box
from yam_arena import ik,task_file
from .feedback import Controller, ControlFailure


class Expert(PolicyBase):
    def __init__(self):
        low=np.tile(np.r_[ik.LOWER,0.0],2);high=np.tile(np.r_[ik.UPPER,1.0],2)
        self.info=PolicyInfo(name='rc_expert',action_space=action_box(low,high))
        self.controller=None;self.runtime=None;self.last_event=0;self.terminal_started=None

    def bind(self,info):
        task=task_file.lookup(info.environment_id)
        if task is None:raise ControlFailure('Expert requires an explicit task file')
        module=task.module
        self.runtime=importlib.import_module(module._name+'.arena_runtime')
        self.evaluator=module.EVALUATOR;self.hold_seconds=module.SPEC['hold_seconds']
        plan=json.loads((module.HERE/'controller.json').read_text())
        self.controller=Controller(plan,module.SPEC)

    def reset(self,scene):
        if self.controller is None:raise ControlFailure('Expert has not bound to its task')
        self.controller.reset();self.last_event=0;self.terminal_started=None

    def terminal_stop(self,now):
        if not self.controller.done:return False
        result=self.evaluator.result
        if result.failure:raise ControlFailure('Terminal state invalid: '+str(result.failure))
        if result.success:return True
        if self.terminal_started is None:self.terminal_started=now
        if now-self.terminal_started>max(5.,self.hold_seconds+2.):
            raise ControlFailure('Plan ended without a stable full-score state; score='+str(result.score))
        return False

    def act(self,observation):
        frame=self.runtime.LATEST
        if frame is None:raise ControlFailure('Native frame unavailable')
        if abs(frame['time']-observation.state_time)>1e-6:raise ControlFailure('Stale native feedback')
        try:
            action=self.controller.step(observation.state['joint_pos'],frame)
            stop=self.terminal_stop(frame['time'])
        except ControlFailure as exc:
            self.controller.events.append({
                'event': 'FAILED', 'reason': str(exc), 'time': frame['time'],
                'robot_joint_pos': np.asarray(observation.state['joint_pos']).tolist(),
                'motion_references': {
                    side: motion.reference.tolist() if motion.reference is not None else None
                    for side, motion in self.controller.motion.items()
                },
            })
            self.record_events()
            raise
        self.record_events()
        return ActionChunk(actions=[Action(data=action,meta={'request_stop':stop})],control_hz=20)

    def record_events(self):
        path=os.getenv('ROBOCURVE_EXPERT_EVENTS')
        if path:
            with Path(path).open('a',encoding='utf-8') as stream:
                for event in self.controller.events[self.last_event:]:
                    stream.write(json.dumps(event,allow_nan=False)+'\n')
        self.last_event=len(self.controller.events)


def policy(**kwargs):
    if kwargs:raise ValueError('Unknown expert options')
    return Expert()
