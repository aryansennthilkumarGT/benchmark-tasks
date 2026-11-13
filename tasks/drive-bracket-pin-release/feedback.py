"""Drive-bracket expert: absolute joint/gripper actions with bounded proprioceptive recovery.

The scorer observes objects independently. The policy reads only robot joints and
observation time. No state writes, part attachments or score queries are present.
"""
import math
import numpy as np
try:
    from .motion import Motion,ControlFailure,axis_quat,rotate,multiply,qangle,conjugate
except ImportError:
    from motion import Motion,ControlFailure,axis_quat,rotate,multiply,qangle,conjugate


class Controller:
    def __init__(self,plan,spec):
        self.phases=plan['phases'];self.spec=spec;self.reset()

    def reset(self):
        self.index=0;self.done=False;self.failed=None;self.events=[];self.thread=None;self.grasps={}
        self.motion={s:Motion(s,tracking_error_limit=.025) for s in ('left','right')}
        self.targets={};self.started=None;self.last_time=None;self.stable=None
        self.best=float('inf');self.progress_time=None;self.actions=0
        self.recovery=None;self.attempts={}

    def fail(self,message):
        self.failed=message
        self.events.append(dict(event='FAIL_STOP',phase=self.index,reason=message,time=self.last_time))
        raise ControlFailure(message)

    def begin_recovery(self,phase,now):
        attempts=self.attempts.get(self.index,0)
        if attempts>=2:self.fail('Recovery attempts exhausted: '+phase['label'])
        from copy import deepcopy
        retry=deepcopy(phase)
        if phase['label'].startswith(('Grip','Regrasp')):
            retry['opening']=min(1.,max(.62,phase.get('grasp_width',0.)/.0939+.12));retry['grasp_width']=0.;retry['dwell']=.3;kind='REOPEN_AND_REACQUIRE'
        else:self.fail('Unrecoverable motion stall: '+phase['label'])
        self.attempts[self.index]=attempts+1
        self.recovery=dict(phase=retry,started=now,stable=None,kind=kind)
        self.targets[phase['side']]=retry
        self.events.append(dict(event='RECOVERY_START',phase=self.index,kind=kind,attempt=attempts+1,time=now))

    def step(self,joints,frame):
        now=float(frame['time']);q=np.asarray(joints,dtype=float)
        if q.shape!=(14,) or not np.isfinite(q).all() or not math.isfinite(now):raise ControlFailure('Invalid robot observation')
        if self.failed:raise ControlFailure(self.failed)
        if self.last_time is not None and now<=self.last_time:self.fail('Robot observation time did not advance')
        self.last_time=now;self.actions+=1
        if self.actions>self.spec['run_limit']:self.fail('Expert action limit exhausted')
        if self.done:return q.copy()
        phase=self.phases[self.index]
        if self.started is None:
            self.started=now;self.progress_time=now;self.best=float('inf');self.stable=None
            self.targets[phase['side']]=phase
            self.events.append(dict(event='PHASE_START',phase=self.index,label=phase['label'],time=now))
        active=self.recovery['phase'] if self.recovery else phase
        output=q.copy();error=theta=0.
        try:
            for side,p in self.targets.items():
                start=0 if side=='left' else 7
                action,pe,re=self.motion[side].target(q[start:start+7],p['target']['pos'],p['target']['quat'],
                    p['opening'],speed=p['speed'],angular_speed=.5)
                output[start:start+7]=action
                if side==phase['side']:error,theta=pe,re
        except ControlFailure as exc:self.fail(str(exc))
        offset=0 if phase['side']=='left' else 7
        closed=active.get('grasp_width',0.)>0
        # Verify obstruction in the expected solid-part aperture band. This is
        # a grasp-acquisition check, not proof of no slip during carrying.
        width=active.get('grasp_width',0.)/.0939
        gripped=(max(active['opening']+.01,width-.035)<q[offset+6]<width+.04) if closed else abs(q[offset+6]-active['opening'])<.03
        reached=error<active['position_tolerance'] and theta<active['angle_tolerance'] and gripped
        if self.recovery:
            r=self.recovery
            if now-r['started']>12.:self.fail('Recovery timeout: '+phase['label'])
            if reached:
                if r['stable'] is None:r['stable']=now
                if now-r['stable']>=active['dwell']:
                    self.events.append(dict(event='RECOVERY_COMPLETE',phase=self.index,time=now))
                    self.recovery=None;self.targets[phase['side']]=phase
                    self.started=now;self.progress_time=now;self.best=float('inf');self.stable=None
            else:r['stable']=None
            return output
        metric=error+.02*theta
        if metric<self.best-.00008:self.best=metric;self.progress_time=now
        if now-self.started>phase['timeout'] or (not reached and now-self.progress_time>8.):
            self.begin_recovery(phase,now);return output
        if reached:
            if self.stable is None:self.stable=now
            if now-self.stable>=phase['dwell']:
                self.events.append(dict(event='PROPRIOCEPTIVE_PHASE_COMPLETE',phase=self.index,label=phase['label'],time=now,
                    position_error_m=error,rotation_error_rad=theta))
                self.index+=1;self.started=None;self.done=self.index==len(self.phases)
        else:self.stable=None
        return output
