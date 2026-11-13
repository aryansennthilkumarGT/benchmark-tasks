"""Carrier placement and three independent retainer histories.

This is executable scorer logic, not a validated scene. Geometry/tolerances are
explicit inputs; no manufacturer dimensions or contact forces are invented.
"""
from dataclasses import dataclass
import itertools
import math


def finite(values,n):
    return isinstance(values,(tuple,list)) and len(values)==n and all(
        isinstance(v,(int,float)) and not isinstance(v,bool) and math.isfinite(v) for v in values)


def rotate(q,v):
    x,y,z,w=q;X,Y,Z=v
    tx,ty,tz=2*(y*Z-z*Y),2*(z*X-x*Z),2*(x*Y-y*X)
    return [X+w*tx+y*tz-z*ty,Y+w*ty+z*tx-x*tz,Z+w*tz+x*ty-y*tx]


@dataclass(frozen=True)
class Result:
    score:float
    success:bool
    failure:str|None
    seated_carrier:bool
    secured_studs:tuple


class Scorer:
    def __init__(self,spec):
        self.spec=spec
        studs=spec['studs']
        if len(studs)!=3 or len(spec['retainers'])!=3:raise ValueError('Three studs and retainers required')
        if len(set(spec['retainers']))!=3:raise ValueError('Duplicate retainer identity')
        if len(spec['carrier_slot_centres'])!=3 or not all(finite(v,3) for v in spec['carrier_slot_centres']):
            raise ValueError('Three finite carrier slot centres required')
        for s in studs:
            if not finite(s['axis_xy'],2):raise ValueError('Invalid stud axis')
        if len({tuple(s['axis_xy']) for s in studs})!=3:raise ValueError('Duplicate stud site')
        for s in studs:
            if not finite([s[k] for k in ('tip_z','engagement_min_z','engagement_max_z','minimum_turns')],4):
                raise ValueError('Invalid stud engagement specification')
            if s['minimum_turns']<=0 or s['engagement_min_z']>=s['engagement_max_z']:
                raise ValueError('Invalid stud engagement interval')
        if not math.isfinite(spec['pitch']) or spec['pitch']<=0:raise ValueError('Invalid pitch')
        tolerances=('lateral_tolerance','axial_tolerance','tilt_tolerance','hold_seconds')
        if any(isinstance(spec[k],bool) or not 0<spec[k]<float('inf') for k in tolerances):raise ValueError('Invalid scoring tolerance')
        self.reset()

    def reset(self):
        self.failed=None;self.previous=None;self.time=None;self.history={};self.stable_since=None
        self.result=Result(0.,False,None,False,())

    def fail(self,reason):
        self.failed=self.failed or reason
        self.result=Result(0.,False,self.failed,False,())
        return self.result

    def update(self,frame):
        required={'carrier',*self.spec['retainers'],*self.spec['anchors']}
        if not isinstance(frame,dict) or frame.get('schema')!=1:return self.fail('frame_schema')
        if not finite([frame.get('time')],1) or frame['time']<0:return self.fail('invalid_time')
        bodies=frame.get('bodies')
        if not isinstance(bodies,dict) or set(bodies)!=required:return self.fail('missing_or_extra_body')
        for b in bodies.values():
            if not isinstance(b,dict):return self.fail('invalid_body_state')
            for key,n in [('pos',3),('quat',4),('linear',3),('angular',3)]:
                if not finite(b.get(key),n):return self.fail('nonfinite_body_state')
            if abs(sum(v*v for v in b['quat'])-1)>1e-5:return self.fail('quaternion_norm')
        if not finite([frame.get('robot_clearance'),frame.get('max_penetration')],2):
            return self.fail('missing_contact_measurement')
        if frame['max_penetration']<0 or frame['max_penetration']>self.spec['penetration_limit']:
            return self.fail('interpenetration')
        t=frame['time']
        if self.time is not None and t<=self.time:
            if t==self.time and frame==self.previous:return self.result
            return self.fail('nonmonotonic_frame')
        if self.time is not None and t-self.time>1.5/self.spec['control_hz']:self.stable_since=None
        self.time=t
        import copy
        self.previous=copy.deepcopy(frame)
        if self.failed:return self.fail(self.failed)
        for name in ['carrier',*self.spec['retainers']]:
            if bodies[name]['pos'][2]<self.spec['loss_plane']:
                return self.fail('part_lost:'+name)
        for name,anchor in self.spec['anchors'].items():
            if math.dist(bodies[name]['pos'],anchor['pos'])>self.spec['fixture_tolerance']:
                return self.fail('fixture_moved:'+name)
            if abs(sum(x*y for x,y in zip(bodies[name]['quat'],anchor['quat'])))<math.cos(self.spec['tilt_tolerance']/2):
                return self.fail('fixture_rotated:'+name)
        carrier=bodies['carrier'];axis=rotate(carrier['quat'],[0,0,1])
        cpos=carrier['pos'];carrier_ok=axis[2]>=math.cos(self.spec['tilt_tolerance'])
        # C3 symmetry: every slot must match a distinct actual stud. A carrier
        # rotated by 120 degrees is equivalent; a translated or tipped one is not.
        slots=[rotate(carrier['quat'],slot) for slot in self.spec['carrier_slot_centres']]
        distances=[[math.hypot(cpos[0]+v[0]-s['axis_xy'][0],cpos[1]+v[1]-s['axis_xy'][1])
                    for s in self.spec['studs']] for v in slots]
        carrier_ok=carrier_ok and any(all(distances[i][p[i]]<=self.spec['lateral_tolerance'] for i in range(3))
                                    for p in itertools.permutations(range(3)))
        carrier_ok=carrier_ok and abs(cpos[2]-self.spec['carrier_seat_z'])<=self.spec['axial_tolerance']
        matches={i:[] for i in range(3)}
        for name in self.spec['retainers']:
            b=bodies[name];axis=rotate(b['quat'],[0,0,1])
            site=next((i for i,s in enumerate(self.spec['studs']) if
                math.hypot(b['pos'][0]-s['axis_xy'][0],b['pos'][1]-s['axis_xy'][1])<=self.spec['lateral_tolerance']
                and s['engagement_min_z']<=b['pos'][2]<=s['engagement_max_z']
                and axis[2]>=math.cos(self.spec['tilt_tolerance'])),None)
            yaw=2*math.atan2(b['quat'][2],b['quat'][3]);prev=self.history.get(name)
            if site is None:
                self.history.pop(name,None);continue
            if prev is None or prev['site']!=site:
                prev=dict(site=site,yaw=yaw,origin_z=b['pos'][2],angle=0.)
            else:
                delta=(yaw-prev['yaw']+math.pi)%(2*math.pi)-math.pi
                if abs(delta)>.75:return self.fail('undersampled_retainer_rotation')
                prev=dict(prev,yaw=yaw,angle=prev['angle']+delta)
            turns=-prev['angle']/(2*math.pi)
            expected=prev['origin_z']+self.spec['pitch']*prev['angle']/(2*math.pi)
            consistent=abs(b['pos'][2]-expected)<=self.spec['axial_tolerance']
            # Once motion leaves the helical path, past free rotations must not
            # become valid merely by dropping the retainer to the final height.
            # Reacquisition starts a new engagement history without old credit.
            if not consistent:
                self.history.pop(name,None)
                continue
            self.history[name]=prev
            s=self.spec['studs'][site]
            flush=abs(b['pos'][2]+self.spec['retainer_top_offset']-s['tip_z'])<=self.spec['axial_tolerance']
            if consistent and flush and turns>=s['minimum_turns']:matches[site].append(name)
        # One physical retainer cannot close two stud sites.
        secured=tuple(i for i in range(3) if matches[i]) if carrier_ok else ()
        still=all(math.sqrt(sum(x*x for x in b['linear']))<=self.spec['speed_limit'] and
                  math.sqrt(sum(x*x for x in b['angular']))<=self.spec['spin_limit'] for b in bodies.values())
        ready=carrier_ok and len(secured)==3 and still and frame['robot_clearance']>=self.spec['release_clearance']
        if ready:
            if self.stable_since is None:self.stable_since=t
        else:self.stable_since=None
        success=self.stable_since is not None and t-self.stable_since+1e-9>=self.spec['hold_seconds']
        score=(.25 if carrier_ok else 0)+.25*len(secured)
        self.result=Result(1. if success else min(.95,score),success,None,carrier_ok,secured)
        return self.result
