"""Official Inspect policy. Uses read-only native state for the scripted expert; all manipulation is robot action."""
import json
import os
from pathlib import Path
import numpy as np
from inspect_robots.policy import PolicyBase, PolicyInfo
from inspect_robots.types import Action, ActionChunk
from inspect_robots_yam.config import action_box
from yam_arena import ik, task_file
from .feedback import Controller, ControlFailure
from .native_feedback import NativeFrameReader


class Expert(PolicyBase):
    def __init__(self):
        self.info=PolicyInfo(name='rc_expert',action_space=action_box(
            np.tile(np.r_[ik.LOWER,0.],2),np.tile(np.r_[ik.UPPER,1.],2)))
        self.controller=None;self.last_event=0;self.frames=None

    def bind(self, info):
        task=task_file.lookup(info.environment_id)
        if task is None:raise ControlFailure('Explicit task binding required')
        self.controller=Controller(json.loads((task.module.HERE/'controller.json').read_text()),task.module.SPEC)

    def reset(self, scene):
        if self.controller is None:raise ControlFailure('Expert not bound')
        self.controller.reset();self.last_event=0
        trace=os.environ.get('ROBOCURVE_TRACE')
        if not trace:raise ControlFailure('Native frame trace required for state-aware expert')
        self.frames=NativeFrameReader(trace)

    def act(self, observation):
        try:frame=self.frames.read(observation.state_time)
        except (OSError,ValueError) as exc:raise ControlFailure(str(exc)) from exc
        command=self.controller.step(observation.state['joint_pos'],frame)
        path=os.getenv('ROBOCURVE_EXPERT_EVENTS')
        if path:
            with Path(path).open('a') as stream:
                for event in self.controller.events[self.last_event:]:stream.write(json.dumps(event)+'\n')
        self.last_event=len(self.controller.events)
        return ActionChunk(actions=[Action(data=command,meta={'request_stop':self.controller.done})],control_hz=20)


def policy(**kwargs):
    if kwargs:raise ValueError('Unknown expert options')
    return Expert()
