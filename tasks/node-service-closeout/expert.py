"""Fixed robot-action expert: no hidden object state or score access.

The authored trajectory was compiled from a disclosed successful development
rollout. Feasibility requires new complete cold-reset physical replay trials.
"""
import json
import os
from pathlib import Path
import numpy as np
from inspect_robots.policy import PolicyBase, PolicyInfo
from inspect_robots.types import Action, ActionChunk
from inspect_robots_yam.config import action_box
from yam_arena import ik, task_file


class Expert(PolicyBase):
    def __init__(self):
        low=np.tile(np.r_[ik.LOWER,0.0],2);high=np.tile(np.r_[ik.UPPER,1.0],2)
        self.info=PolicyInfo(name='rc_expert',action_space=action_box(low,high))
        self.actions=None;self.index=0;self.checkpoints={}

    def bind(self, info):
        task=task_file.lookup(info.environment_id)
        if task is None:raise ValueError('Explicit task file required')
        data=json.loads((task.module.HERE/'expert_joint_trajectory.json').read_text())
        if data['kind']!='FIXED_ROBOT_JOINT_ACTION_TRAJECTORY' or data['control_hz']!=20:
            raise ValueError('Wrong robot trajectory format')
        self.actions=np.asarray(data['actions'],dtype=float)
        if (self.actions.ndim!=2 or self.actions.shape[1]!=14 or not len(self.actions)
                or not np.isfinite(self.actions).all()):raise ValueError('Invalid robot actions')
        self.hold=int(data['terminal_hold_actions'])
        if not 1<=self.hold<=100:raise ValueError('Invalid fixed terminal hold')
        self.checkpoints={}
        for item in data['checkpoints']:
            self.checkpoints.setdefault(item['post_action_frame_index'],[]).append(item)

    def reset(self, scene):
        if self.actions is None:raise ValueError('Policy not bound')
        self.index=0

    def act(self, observation):
        joints=np.asarray(observation.state['joint_pos'],dtype=float)
        if joints.shape!=(14,) or not np.isfinite(joints).all():
            raise ValueError('Invalid robot proprioception')
        now=float(observation.state_time)
        if abs(now-self.index/20)>1e-5:raise ValueError('Noncontiguous robot action time')
        trace=os.environ.get('ROBOCURVE_PROPRIO_TRACE')
        if trace:
            with Path(trace).open('a') as stream:
                stream.write(json.dumps({'time':now,'joint_pos':joints.tolist()},allow_nan=False)+'\n')
        marker_path=os.environ.get('ROBOCURVE_EXPERT_EVENTS')
        if marker_path:
            with Path(marker_path).open('a') as stream:
                for item in self.checkpoints.get(self.index+1,[]):
                    stream.write(json.dumps(dict(item,event='SCRIPTED_ACTION_CHECKPOINT',
                        action_index=self.index,state_time=now),allow_nan=False)+'\n')
        action=self.actions[min(self.index,len(self.actions)-1)].copy()
        self.index+=1
        stop=self.index>=len(self.actions)+self.hold
        return ActionChunk(actions=[Action(data=action,meta={'request_stop':stop})],control_hz=20)


def policy(**kwargs):
    if kwargs:raise ValueError('Unknown expert options')
    return Expert()
