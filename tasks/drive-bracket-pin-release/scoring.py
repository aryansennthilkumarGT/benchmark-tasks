"""Observed physical rail/pin-release sequence and unsupported final placement."""
from dataclasses import dataclass
import copy,math
try:
    from .motion import rotate,qangle
except ImportError:
    from motion import rotate,qangle


def finite(v,n):return isinstance(v,(list,tuple)) and len(v)==n and all(isinstance(x,(int,float)) and not isinstance(x,bool) and math.isfinite(x) for x in v)


@dataclass(frozen=True)
class Result:
    score:float
    success:bool
    failure:str|None
    completed:tuple


class Scorer:
    def __init__(self,scene):self.spec=scene['score_spec'];self.reset()
    def reset(self):
        self.failed=None;self.time=None;self.previous=None;self.stable=None
        self.released=False;self.tilted=False;self.withdrawn=False
        self.result=Result(0.,False,None,())
    def fail(self,reason):
        self.failed=self.failed or reason;self.result=Result(0.,False,self.failed,());return self.result
    def update(self,f):
        s=self.spec
        if not isinstance(f,dict) or f.get('schema')!=1:return self.fail('frame_schema')
        if not finite([f.get('time')],1) or f['time']<0:return self.fail('time')
        bodies=f.get('bodies');required={'bracket','release_rail','drive','staging_tray'}
        if not isinstance(bodies,dict) or set(bodies)!=required:return self.fail('body_set')
        for b in bodies.values():
            if not isinstance(b,dict):return self.fail('body_state')
            for k,n in [('pos',3),('quat',4),('linear',3),('angular',3)]:
                if not finite(b.get(k),n):return self.fail('nonfinite_state')
            if abs(sum(v*v for v in b['quat'])-1)>1e-5:return self.fail('quaternion_norm')
        joints=f.get('joints')
        if not isinstance(joints,dict) or set(joints)!={s['rail_joint']} or not finite([joints[s['rail_joint']]],1):return self.fail('joint_state')
        if not finite([f.get('max_penetration'),f.get('robot_clearance')],2):return self.fail('contact_telemetry')
        if not 0<=f['max_penetration']<=s['penetration_limit']:return self.fail('penetration')
        t=f['time']
        if self.time is not None and t<=self.time:
            if t==self.time and f==self.previous:return self.result
            return self.fail('time_order')
        if self.time is not None and t-self.time>1.5/s['control_hz']:self.stable=None
        self.time=t;self.previous=copy.deepcopy(f)
        if self.failed:return self.fail(self.failed)
        for name,a in s['anchors'].items():
            if math.dist(bodies[name]['pos'],a['pos'])>s['fixture_tolerance'] or qangle(bodies[name]['quat'],a['quat'])>s['tilt_tolerance']:
                return self.fail('anchor_moved:'+name)
        q=joints[s['rail_joint']];rail=bodies['release_rail'];origin=s['rail_origin']
        if q<-.0002 or q>s['rail_limit']+.0002:return self.fail('rail_limit')
        if math.dist(rail['pos'],[origin[0],origin[1]+q,origin[2]])>.0004 or qangle(rail['quat'],[0,0,0,1])>.025:
            return self.fail('rail_joint_pose_mismatch')
        drive=bodies['drive'];p=drive['pos'];initial=s['initial_drive']
        if p[2]<s['loss_plane']:return self.fail('drive_lost')
        if q>=s['rail_release'] and math.dist(p,initial)<.003:self.released=True
        left_edge=rotate(drive['quat'],[0,.06985/2,0])+p
        right_edge=rotate(drive['quat'],[0,-.06985/2,0])+p
        tilted=left_edge[2]>=initial[2]+.012 and abs(right_edge[2]-initial[2])<=.002 and abs(p[0]-initial[0])<.002
        if self.released and q>=s['rail_release'] and tilted:self.tilted=True
        if self.tilted and q>=s['rail_release'] and p[1]-initial[1]>=.0025 and p[2]<initial[2]+.025:
            self.withdrawn=True
        clear=self.withdrawn and (p[2]>initial[2]+.055 or math.dist(p[:2],initial[:2])>.125)
        staged=clear and math.dist(p[:2],s['target_drive'][:2])<=s['position_tolerance'] and abs(p[2]-s['target_drive'][2])<=s['axial_tolerance'] and qangle(drive['quat'],[0,0,0,1])<=s['tilt_tolerance']
        returned=abs(q)<=s['rail_return']
        still=all(math.sqrt(sum(v*v for v in b['linear']))<=s['speed_limit'] and math.sqrt(sum(v*v for v in b['angular']))<=s['spin_limit'] for b in bodies.values())
        ready=staged and returned and still and f['robot_clearance']>=s['release_clearance']
        if ready:
            if self.stable is None:self.stable=t
        else:self.stable=None
        success=self.stable is not None and t-self.stable+1e-9>=s['hold_seconds']
        goals=tuple(n for n,ok in [('rail_released',q>=s['rail_release'] and not clear),('drive_extracted',clear),('rail_returned',clear and returned),('drive_staged',staged)] if ok)
        score=.5*clear+.25*(clear and returned)+.25*staged if clear else (.25 if q>=s['rail_release'] and self.released else 0.)
        self.result=Result(1. if success else min(.95,score),success,None,goals);return self.result
