"""Feedback primitives for the official YAM absolute-joint action interface.

All motion is produced as 14 joint/gripper targets. This module never sets body
poses, attaches objects, or changes scores. This low-level module reads robot proprioception. The SAC-independent cargo
controller also reads native task state through feedback.py for physical interfaces.
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
    def __init__(self,side,dt=0.05,tracking_error_limit=0.08):
        from yam_arena import ik,station
        self.ik=ik;self.base=station.BASES[side];self.dt=dt
        self.reference = None
        self.grip_reference = None
        self.tracking_error_limit = tracking_error_limit

    def gripper_target(self,measured,opening,step=.05):
        """Slew the commanded aperture, retaining full desired closing force.

        Advancing from measured position on every tick permanently caps the
        servo error when an object blocks the jaws. The persistent command
        reaches the requested aperture; SDK actuator force limits still apply.
        """
        if not all(math.isfinite(float(v)) for v in (measured,opening,step)) or not 0<=opening<=1 or not 0<step<=.05:
            raise ControlFailure('Invalid gripper reference')
        if self.grip_reference is None:self.grip_reference=float(np.clip(measured,0.,1.))
        self.grip_reference+=float(np.clip(opening-self.grip_reference,-step,step))
        return float(self.grip_reference)

    def target(self,measured,pos,quat,opening,speed=0.06,angular_speed=0.5,feedback_gain=0.):
        q=np.asarray(measured,dtype=float)
        if q.shape!=(7,) or not np.isfinite(q).all():raise ControlFailure('Invalid proprioception')
        arm = q[:6]
        measured_pos, measured_rotation = self.ik.tcp_pose(arm, self.base)
        pos = np.asarray(pos, dtype=float)
        quat = unit(quat)
        error = float(np.linalg.norm(measured_pos - pos))
        theta = qangle(self.ik.matrix_to_quat_xyzw(measured_rotation), quat)
        grip = self.gripper_target(q[6],opening)
        if self.reference is None:
            self.reference = arm.copy()
        if np.max(np.abs(self.reference - arm)) > self.tracking_error_limit:
            command = np.clip(self.reference, arm-self.tracking_error_limit-0.02, arm+self.tracking_error_limit+0.02)
            return np.r_[command, grip], error, theta
        current, rotation = self.ik.tcp_pose(self.reference, self.base)
        current_q = self.ik.matrix_to_quat_xyzw(rotation)
        if not math.isfinite(feedback_gain) or feedback_gain < 0:
            raise ControlFailure('Invalid measured-position feedback gain')
        position_step = feedback_gain*self.dt*(pos-measured_pos) if feedback_gain else pos-current
        remaining_angle = qangle(current_q, quat)
        # One common interpolation fraction preserves screw lead and coupled
        # Cartesian/rotary paths. Independent saturation can jam a thread.
        fraction=min(1.,speed*self.dt/max(np.linalg.norm(position_step),1e-12),
                     angular_speed*self.dt/max(remaining_angle,1e-12))
        limited = current + position_step*fraction
        qtarget = interpolate(current_q, quat, fraction)
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

