"""Executable bounded expert using robot joint observations only.

Object transforms below are authored waypoints. No object pose, scorer result,
simulator handle, attachment or state-write API is available to this controller.
"""
import math
import numpy as np
try:
    from .motion import Motion, ControlFailure, axis_quat, rotate, multiply, qangle, conjugate
except ImportError:
    from motion import Motion, ControlFailure, axis_quat, rotate, multiply, qangle, conjugate


class Controller:
    def __init__(self, plan, spec):
        self.phases=plan['phases'];self.spec=spec
        self.reset()

    def reset(self):
        self.index=0;self.done=False;self.failed=None;self.events=[];self.thread=None
        self.motion={s:Motion(s,tracking_error_limit=.025) for s in ('left','right')}
        self.targets={};self.started=None;self.last_time=None;self.stable=None
        self.best=float('inf');self.progress_time=None;self.actions=0

    def step(self, joints, frame):
        # The native test harness supplies a frame for timing. Only time is read.
        now=float(frame['time'])
        q=np.asarray(joints,dtype=float)
        if q.shape!=(14,) or not np.isfinite(q).all() or not math.isfinite(now):
            raise ControlFailure('Invalid robot observation')
        if self.failed:raise ControlFailure(self.failed)
        if self.last_time is not None and now<=self.last_time:
            raise ControlFailure('Robot observation time did not advance')
        self.last_time=now;self.actions+=1
        if self.actions>self.spec['run_limit']:raise ControlFailure('Expert action limit exhausted')
        if self.done:return q.copy()
        phase=self.phases[self.index]
        if self.started is None:
            self.started=now;self.progress_time=now;self.best=float('inf');self.stable=None
            self.targets[phase['side']]=phase
            self.events.append(dict(event='PHASE_START',phase=self.index,label=phase['label'],time=now))
        if now-self.started>phase['timeout']:
            self.failed='Phase timeout: '+phase['label'];raise ControlFailure(self.failed)
        output=q.copy();error=0.;theta=0.
        for side,p in self.targets.items():
            start=0 if side=='left' else 7
            action,pe,re=self.motion[side].target(q[start:start+7],p['target']['pos'],p['target']['quat'],
                p['opening'],speed=p['speed'],angular_speed=.5)
            output[start:start+7]=action
            if side==phase['side']:error,theta=pe,re
        offset=0 if phase['side']=='left' else 7
        grip_error=abs(q[offset+6]-phase['opening'])
        # Closing on a real solid head/leg prevents reaching the no-load command.
        # Verify a physically plausible measured jaw aperture after closing.
        closed=phase['opening']<.3
        gripped=(phase['opening']+.01<q[offset+6]<.35) if closed else grip_error<.03
        reached=error<phase['position_tolerance'] and theta<phase['angle_tolerance'] and gripped
        metric=error+.02*theta
        if metric<self.best-.00008:
            self.best=metric;self.progress_time=now
        if not reached and now-self.progress_time>8.:
            self.failed='No measured joint-space progress: '+phase['label'];raise ControlFailure(self.failed)
        if reached:
            if self.stable is None:self.stable=now
            if now-self.stable>=phase['dwell']:
                self.events.append(dict(event='PROPRIOCEPTIVE_PHASE_COMPLETE',phase=self.index,
                    label=phase['label'],time=now,position_error_m=error,rotation_error_rad=theta))
                self.index+=1;self.started=None;self.done=self.index==len(self.phases)
        else:self.stable=None
        return output
