"""Feedback primitives for the official YAM absolute-joint action interface.

All motion is produced as 14 joint/gripper targets. This module never sets body
poses, attaches objects, or changes scores. Experts may read simulator geometry;
the Dream policy receives only the official cameras and joint observations.
"""
from __future__ import annotations
import math
import numpy as np


class ControlFailure(RuntimeError):
    pass


def unit(q):
    q=np.asarray(q,dtype=float)
    if q.shape!=(4,) or not np.isfinite(q).all() or np.linalg.norm(q)<1e-9:
        raise ControlFailure('Invalid target quaternion')
    return q/np.linalg.norm(q)


def multiply(a,b):
    x,y,z,w=a;X,Y,Z,W=b
    return np.array([w*X+x*W+y*Z-z*Y,w*Y-x*Z+y*W+z*X,w*Z+x*Y-y*X+z*W,w*W-x*X-y*Y-z*Z])


def conjugate(q):
    return np.asarray(q)*[-1,-1,-1,1]


def rotate(q,v):
    return multiply(multiply(q,np.r_[v,0]),conjugate(q))[:3]


def axis_quat(axis,angle):
    axis=np.asarray(axis,dtype=float);axis/=np.linalg.norm(axis)
    return np.r_[axis*math.sin(angle/2),math.cos(angle/2)]


def qangle(a,b):
    return 2*math.acos(float(np.clip(abs(np.dot(unit(a),unit(b))),0,1)))


def interpolate(a,b,amount):
    a,b=unit(a),unit(b)
    if np.dot(a,b)<0:b=-b
    angle=math.acos(float(np.clip(np.dot(a,b),-1,1)))
    if angle<1e-8:return a
    return (math.sin((1-amount)*angle)*a+math.sin(amount*angle)*b)/math.sin(angle)


def limit_vector(delta,maximum):
    delta=np.asarray(delta,dtype=float)
    return delta*min(1,maximum/max(np.linalg.norm(delta),1e-12))


class Motion:
    """Track a rate-limited IK reference while waiting for all joints to catch up."""
    def __init__(self,side,dt=0.05,tracking_error_limit=0.025):
        from yam_arena import ik,station
        self.ik=ik;self.base=station.BASES[side];self.dt=dt
        self.reference = None
        self.tracking_error_limit = tracking_error_limit

    def target(self,measured,pos,quat,opening,speed=0.06,angular_speed=0.5,feedback_gain=0.):
        q=np.asarray(measured,dtype=float)
        if q.shape!=(7,) or not np.isfinite(q).all():raise ControlFailure('Invalid proprioception')
        arm = q[:6]
        measured_pos, measured_rotation = self.ik.tcp_pose(arm, self.base)
        pos = np.asarray(pos, dtype=float)
        quat = unit(quat)
        error = float(np.linalg.norm(measured_pos - pos))
        measured_quat = self.ik.matrix_to_quat_xyzw(measured_rotation)
        theta = qangle(measured_quat, quat)
        if not math.isfinite(feedback_gain) or feedback_gain < 0:
            raise ControlFailure('Invalid measured-pose feedback gain')
        grip = q[6] + float(np.clip(opening-q[6], -0.10, 0.10))
        if self.reference is None:
            self.reference = arm.copy()
        if np.max(np.abs(self.reference - arm)) > self.tracking_error_limit:
            command = np.clip(self.reference, arm-self.tracking_error_limit-0.02,
                              arm+self.tracking_error_limit+0.02)
            return np.r_[command, grip], error, theta
        current, rotation = self.ik.tcp_pose(self.reference, self.base)
        current_q = self.ik.matrix_to_quat_xyzw(rotation)
        if feedback_gain > 0:
            position_step = feedback_gain * self.dt * (pos - measured_pos)
            rotation_error = multiply(quat, conjugate(measured_quat))
            amount = min(feedback_gain * self.dt, angular_speed * self.dt / max(theta, 1e-9))
            qtarget = multiply(interpolate([0, 0, 0, 1], rotation_error, amount), current_q)
        else:
            position_step = pos - current
            remaining_angle = qangle(current_q, quat)
            qtarget = interpolate(current_q, quat, min(1, angular_speed*self.dt/max(remaining_angle, 1e-9)))
        limited = current + limit_vector(position_step, speed*self.dt)
        solved,position_error,rotation_error=self.ik.solve(limited,qtarget,q_init=self.reference,base_pos=self.base,
                                                         iters=100,damping=0.015,tol=2e-5)
        if position_error>0.0015 or rotation_error>0.035:
            raise ControlFailure(f'IK did not converge: {position_error*1000:.2f} mm, {math.degrees(rotation_error):.2f} deg')
        if np.any(solved<self.ik.LOWER+1e-5) or np.any(solved>self.ik.UPPER-1e-5):
            raise ControlFailure('IK reached a joint limit')
        step = solved - self.reference
        step *= min(1.0, 0.02/max(np.max(np.abs(step)), 1e-12))
        self.reference = self.reference + step
        return np.r_[self.reference, grip], error, theta


class Controller:
    """Measured-state phase machine. A phase cannot pass on elapsed time alone.

    Types: move, grasp, carry, insert, joint, release, hold, thread.
    Concurrent arm targets permit one arm to support a passive mechanism while the
    other works. Mechanical completion always comes from the independent scorer.
    """
    def __init__(self,plan,spec):
        from yam_arena import ik,station
        self.plan=plan;self.spec=spec;self.ik=ik;self.station=station
        self.motion={'left': Motion('left'), 'right': Motion('right', tracking_error_limit=0.10)}
        self.phases=plan['phases'];self.reset()

    def reset(self):
        self.index=0;self.started=None;self.stable_since=None;self.grasps={};self.holds={}
        self.phase_start={};self.events=[];self.attempts={};self.last_progress=None;self.last_progress_t=None
        self.thread=None;self.done=False;self.failed=None;self.grasp_closing=False;self.recovery=None
        for motion in self.motion.values():
            motion.reference = None

    def pose(self,joints,side):
        p,r=self.ik.tcp_pose(joints[:6],self.station.BASES[side])
        return p,self.ik.matrix_to_quat_xyzw(r)

    def world_target(self,target,frame):
        p=np.asarray(target['pos'],dtype=float);q=unit(target.get('quat',[0,0,0,1]))
        if target.get('relative_to'):
            ref=frame['bodies'][target['relative_to']]
            p=np.asarray(ref['pos'])+rotate(ref['quat'],p);q=multiply(ref['quat'],q)
        return p,q

    def body_tcp(self,side,body_pos,body_quat):
        grasp=self.grasps.get(side)
        if grasp is None:raise ControlFailure('No verified grasp for '+side)
        return (np.asarray(body_pos)+rotate(body_quat,grasp['tcp_in_body']),
                multiply(body_quat,grasp['tcp_rotation_in_body']))

    def advance(self,now):
        self.events.append({'phase':self.index,'label':self.phases[self.index]['label'],'time':now,'event':'MEASURED_PHASE_COMPLETE'})
        self.index+=1;self.started=None;self.stable_since=None;self.last_progress=None;self.thread=None
        self.grasp_closing=False;self.recovery=None

    def check_grasp_slip(self,side,joints,frame,require_support=False):
        grasp=self.grasps.get(side)
        if not grasp or not (grasp.get('verified') or require_support):return
        if require_support and joints[6]*.0939<grasp.get('min_width',.005):
            raise ControlFailure('Supporting grasp closed empty: '+grasp['body'])
        body=frame['bodies'][grasp['body']]
        desired,_=self.body_tcp(side,body['pos'],body['quat']);actual,_=self.pose(joints,side)
        if np.linalg.norm(actual-desired)>grasp.get('slip_tolerance',0.012):
            raise ControlFailure('Grasp slipped: '+grasp['body'])

    def step(self,joints,frame):
        joints=np.asarray(joints,dtype=float)
        if joints.shape!=(14,):raise ControlFailure('Expected 14 joint observations')
        if not np.isfinite(joints).all():raise ControlFailure('Nonfinite joint observations')
        now=frame['time']
        if self.index>=len(self.phases):
            self.done=True;return joints.copy()
        phase=self.phases[self.index]
        if self.started is None:
            self.started=now;self.phase_start={s:self.pose(joints[i*7:i*7+7],s) for i,s in enumerate(('left','right'))}
            self.events.append({'phase':self.index,'label':phase['label'],'time':now,'event':'START'})
        if now-self.started>phase.get('timeout',20):raise ControlFailure('Phase timeout: '+phase['label'])
        if frame.get('max_penetration',0)>self.spec['penetration_limit']:
            raise ControlFailure('Task geometry interpenetration')
        targets={}
        for held_side,value in self.holds.items():
            held_index=0 if held_side=='left' else 7
            if phase['kind']!='release' or phase['side']!=held_side:
                self.check_grasp_slip(held_side,joints[held_index:held_index+7],frame,require_support=True)
            if isinstance(value,dict):
                hp,hq=self.world_target(value,frame)
                targets[held_side]=(hp,hq,value['opening'],value['speed'])
            else:targets[held_side]=value
        complete=True;kind=phase['kind'];side=phase.get('side','left')
        offset=0 if side=='left' else 7;observed=joints[offset:offset+7]
        tcp,tcpq=self.pose(observed,side)
        body=frame['bodies'].get(phase.get('body'))
        if kind=='move':
            p,q=self.world_target(phase['target'],frame)
            targets[side]=(p,q,phase.get('opening',1.0),phase.get('speed',0.06))
            complete=np.linalg.norm(tcp-p)<phase.get('tolerance',0.002) and qangle(tcpq,q)<0.04
        elif kind=='grasp':
            p=np.asarray(body['pos'])+rotate(body['quat'],phase['offset'])
            q=unit(phase['quat'])
            if phase.get('quat_relative_to_body'):q=multiply(body['quat'],q)
            # Keep the jaws open until the measured TCP reaches the grasp. Closing
            # during descent would arrive with empty, closed fingers.
            aligned=np.linalg.norm(tcp-p)<0.0015 and qangle(tcpq,q)<0.04
            if aligned:self.grasp_closing=True
            approach_width=phase.get('approach_width',phase['width'][1]+0.012)
            targets[side]=(p,q,0.0 if self.grasp_closing else min(1.0,approach_width/0.0939),0.025)
            width=float(observed[6])*0.0939
            complete=(self.grasp_closing and phase['width'][0]<=width<=phase['width'][1] and np.linalg.norm(tcp-p)<0.004
                      and qangle(tcpq,q)<0.06 and now-self.started>0.4)
            if complete:
                self.grasps[side]={'body':phase['body'],'tcp_in_body':rotate(conjugate(body['quat']),tcp-np.asarray(body['pos'])),
                    'tcp_rotation_in_body':multiply(conjugate(body['quat']),tcpq),'verified':False,
                    'min_width':max(.003,phase['width'][0]-.003),
                    'start_z':body['pos'][2],'start_pos':list(body['pos']),'slip_tolerance':phase.get('slip_tolerance',0.012)}
        elif kind in ('carry','insert'):
            self.check_grasp_slip(side,observed,frame)
            desired_p,desired_q=self.world_target(phase['target'],frame)
            body_p,body_q=np.asarray(body['pos']),body['quat']
            # Correct measured body error, so slip is not hidden by a precomputed TCP path.
            commanded=body_p+limit_vector(desired_p-body_p,0.0005 if kind=='insert' else 0.003)
            p,q=self.body_tcp(side,commanded,desired_q)
            if phase.get('measured_translation'):
                tracking_base = tcp
                reference = self.motion[side].reference
                if phase.get('integrate_body_error') and reference is not None:
                    tracking_base, _ = self.pose(np.r_[reference, observed[6]], side)
                p = tracking_base + limit_vector(phase.get('position_gain', 1.0) * (desired_p - body_p),
                                                 phase.get('translation_lead', 0.003))
            progress_error = None
            progress_margin = .0003
            if kind == 'insert' and 'insertion_axis_world' in phase:
                axis = np.asarray(phase['insertion_axis_world'], dtype=float)
                length = np.linalg.norm(axis)
                if axis.shape != (3,) or not np.isfinite(axis).all() or length < 1e-12:
                    raise ControlFailure('Invalid insertion axis')
                axis = axis / length
                position_error = desired_p - body_p
                axial = np.dot(position_error, axis) * axis
                lateral = position_error - axial
                correction = limit_vector(phase.get('lateral_gain', 2.) * lateral,
                                          phase.get('lateral_lead', .001))
                orientation_error = qangle(body_q, desired_q)
                lateral_tolerance = np.asarray(phase.get('lateral_tolerance', .0004), dtype=float)
                if (lateral_tolerance.shape not in [(), (3,)]
                        or not np.isfinite(lateral_tolerance).all() or np.any(lateral_tolerance <= 0)):
                    raise ControlFailure('Invalid lateral insertion tolerance')
                aligned = (np.linalg.norm(lateral) <= lateral_tolerance if lateral_tolerance.shape == ()
                           else bool(np.all(np.abs(lateral) <= lateral_tolerance)))
                oriented = orientation_error <= phase.get('insertion_orientation_tolerance', .02)
                if aligned and oriented:
                    correction += limit_vector(axial, phase.get('axial_lead', .001))
                p = tcp + correction
                progress_error = np.array([np.linalg.norm(axial), np.linalg.norm(lateral), orientation_error])
                progress_margin = np.array([.0003, float(np.min(lateral_tolerance))*.1, .0005])
            if phase.get('measured_rotation'):
                rotation_error = multiply(desired_q, conjugate(body_q))
                angle_error = qangle([0, 0, 0, 1], rotation_error)
                amount = min(phase.get('rotation_gain', 1.),
                             phase.get('rotation_lead', .08) / max(angle_error, 1e-9))
                correction = interpolate([0, 0, 0, 1], rotation_error, amount)
                q = multiply(correction, tcpq)
                if phase.get('rotation_about_body'):
                    lever = tcp - body_p
                    p += rotate(correction, lever) - lever
            speed=0.01 if kind=='insert' else phase.get('speed',0.05)
            if any(isinstance(value,dict) and value['relative_to']==phase['body'] for value in self.holds.values()):
                speed=min(speed,.025)  # Supporting arm must be able to follow.
            targets[side]=(p,q,0.0,speed)
            error=float(np.linalg.norm(body_p-desired_p))
            if progress_error is None:
                progress_error = error
            complete=error<phase.get('tolerance',0.0015) and qangle(body_q,desired_q)<phase.get('angle',0.06)
            if phase.get('verify_lift'):
                grasp=self.grasps[side]
                complete=complete and body_p[2]-grasp['start_z']>=phase.get('min_lift',0.015)
                if complete:grasp['verified']=True
            if phase.get('verify_displacement'):
                grasp=self.grasps[side]
                complete=complete and np.linalg.norm(body_p-grasp['start_pos'])>=phase.get('min_displacement',.015)
                if complete:grasp['verified']=True
            if kind=='insert':
                if self.last_progress is None:
                    self.last_progress, self.last_progress_t = progress_error, now
                if np.any(progress_error < self.last_progress-progress_margin):
                    self.last_progress = np.minimum(self.last_progress, progress_error)
                    self.last_progress_t = now
                elif now-self.last_progress_t>2.0 and not complete:
                    # Bounded retreat/alignment recovery is specified as explicit plan phases.
                    # Fail rather than increase insertion force into a jam.
                    raise ControlFailure('Insertion stalled; no unbounded force or retry: '+phase['label'])
        elif kind=='joint':
            self.check_grasp_slip(side,observed,frame)
            joint=next(j for a in self.spec['assemblies'] for j in a.get('joints',[]) if j['name']==phase['joint'])
            actual=frame['joints'][phase['joint']];desired=phase['value']
            delta=float(np.clip(desired-actual,-phase.get('increment',0.01),phase.get('increment',0.01)))
            parent=frame['bodies'][joint['parent']];axis=np.eye(3)['XYZ'.index(joint['axis'])]
            world_axis=rotate(parent['quat'],axis)
            if joint['kind']=='revolute':
                pivot=np.asarray(parent['pos'])+rotate(parent['quat'],joint['pivot_parent'])
                turn=axis_quat(world_axis,delta)
                p=pivot+rotate(turn,tcp-pivot);q=multiply(turn,tcpq)
            else:p=tcp+world_axis*delta;q=tcpq
            targets[side]=(p,q,0.0,0.035)
            complete=abs(desired-actual)<phase.get('tolerance',0.006 if joint['kind']=='revolute' else 0.001)
        elif kind=='release':
            opening=phase.get('opening',1.0)
            if not 0<opening<=1:raise ControlFailure('Invalid release opening')
            p,q=self.phase_start[side];targets[side]=(p,q,opening,0.02)
            complete=observed[6]>=opening-.015 and now-self.started>0.35
            if complete:self.grasps.pop(side,None)
        elif kind=='hold':
            p,q=self.phase_start[side];targets[side]=(p,q,phase.get('opening',0.0),0.02)
            complete=now-self.started>=phase['seconds'] and np.linalg.norm(tcp-p)<0.003
        elif kind=='thread':
            p,q,complete=self.thread_target(phase,body,tcp,tcpq,observed,frame,now)
            targets[side]=(p,q,self.thread['opening'],0.012)
        else:raise ControlFailure('Unknown phase '+kind)
        # Inactive arms hold their last measured target, rather than moving through the work.
        action=joints.copy()
        for name,(p,q,opening,speed) in targets.items():
            index=0 if name=='left' else 7
            if p[2]<self.spec['table_top']+0.004:raise ControlFailure('TCP target below table guard')
            target,_,_=self.motion[name].target(joints[index:index+7],p,q,opening,speed=speed,
                                                     feedback_gain=phase.get('feedback_gain', 0.) if name == side else 0.)
            action[index:index+7]=target
        # Reject arm-to-arm TCP collisions; link/fixture checks run in native validation.
        left,_=self.pose(action[:7],'left');right,_=self.pose(action[7:],'right')
        if np.linalg.norm(left-right)<phase.get('minimum_tcp_separation',0.055):
            raise ControlFailure('End effectors too close')
        if complete:
            if self.stable_since is None:self.stable_since=now
            if now-self.stable_since>=phase.get('hold',0.15):
                if phase.get('keep_hold'):
                    value=targets[side]
                    if phase.get('hold_relative_to'):
                        ref=frame['bodies'][phase['hold_relative_to']];rp,rq=ref['pos'],ref['quat']
                        value=dict(relative_to=phase['hold_relative_to'],pos=rotate(conjugate(rq),value[0]-np.asarray(rp)),
                                   quat=multiply(conjugate(rq),value[1]),opening=value[2],speed=value[3])
                    self.holds[side]=value
                if phase.get('clear_hold'):self.holds.pop(side,None)
                self.advance(now)
        else:self.stable_since=None
        return action

    def thread_target(self,phase,body,tcp,tcpq,observed,frame,now):
        """Rotate at most 45 degrees per grip, then reopen and unwind the wrist.

        Axial pitch targets follow measured angular advance. No helical attachment
        is made: native thread contacts must carry the nut during every regrasp.
        """
        side=phase['side'];reference=frame['bodies'][phase['reference']]
        local=rotate(conjugate(reference['quat']),np.asarray(body['pos'])-reference['pos'])
        relative_q=multiply(conjugate(reference['quat']),body['quat'])
        yaw=math.atan2(2*(relative_q[3]*relative_q[2]+relative_q[0]*relative_q[1]),1-2*(relative_q[1]**2+relative_q[2]**2))
        if self.thread is None:
            self.thread={'yaw':yaw,'total':0.0,'segment':0.0,'mode':'turn','opening':0.0,
                         'z0':local[2],'tcp0':tcp.copy(),'q0':tcpq.copy(),'switch':now}
        state=self.thread;delta=math.atan2(math.sin(yaw-state['yaw']),math.cos(yaw-state['yaw']))
        if abs(delta)>0.25:raise ControlFailure('Thread angular jump')
        state['yaw']=yaw;state['total']+=phase.get('direction',-1)*delta
        if np.linalg.norm(local[:2]-phase['xy'])>0.002:raise ControlFailure('Thread lost coaxial engagement')
        expected=state['z0']-phase['pitch']*state['total']/(2*math.pi)
        if abs(local[2]-expected)>0.0015:raise ControlFailure('Nut rotation did not produce axial advancement')
        if state['mode']=='turn':
            self.check_grasp_slip(side,observed,frame)
            state['segment']+=phase.get('direction',-1)*delta
            if state['segment']>=math.pi/4:
                state.update(mode='open',switch=now,opening=min(1.,(phase.get('grasp_width_max',.040)+.012)/.0939))
            turn=axis_quat(rotate(reference['quat'],[0,0,1]),phase.get('direction',-1)*0.018)
            q=multiply(turn,tcpq);p=tcp-rotate(reference['quat'],[0,0,phase['pitch']*0.018/(2*math.pi)])
        elif state['mode']=='open':
            p,q=tcp,tcpq
            if observed[6]>state['opening']*.95:state.update(mode='unwind',switch=now)
        elif state['mode']=='unwind':
            # Open fingers rotate about the nut without moving its body.
            p,q=tcp,state['q0']
            if qangle(tcpq,q)<0.04:state.update(mode='close',switch=now,opening=0.0)
        else:
            p,q=tcp,state['q0']
            if 0.005<observed[6]*0.0939<phase.get('grasp_width_max',0.045) and now-state['switch']>0.4:
                state.update(mode='turn',segment=0.0,switch=now)
                grasp=self.grasps[side]
                grasp['tcp_in_body']=rotate(conjugate(body['quat']),tcp-np.asarray(body['pos']))
                grasp['tcp_rotation_in_body']=multiply(conjugate(body['quat']),tcpq)
        if now-state['switch']>6 and state['mode']!='turn':raise ControlFailure('Thread regrasp timeout')
        complete=(state['total']>=phase['turns']*2*math.pi and local[2]<=phase['seat_z']+0.001
                  and state['mode']=='turn')
        return p,q,complete
