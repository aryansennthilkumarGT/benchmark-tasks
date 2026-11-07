"""Synthetic state tests only. None of these are simulation or demonstration evidence."""
import copy
import importlib.util
import json
import math
from pathlib import Path
import sys
import types
import unittest

HERE=Path(__file__).resolve().parent
PACKAGE='_test_'+HERE.name.replace('-','_')
module=types.ModuleType(PACKAGE);module.__path__=[str(HERE)];sys.modules[PACKAGE]=module
from importlib import import_module
S=import_module(PACKAGE+'.scoring')
G=import_module(PACKAGE+'.geometry')
SPEC=json.loads((HERE/'scene.json').read_text(encoding='utf-8'))


def initial():
    return dict(schema=1,time=0.,robot_clearance=.10,max_penetration=0.,
       bodies={b['name']:dict(pos=list(b['pos']),quat=list(b['quat']),linear=[0.,0.,0.],angular=[0.,0.,0.])
               for a in SPEC['assemblies'] for b in a['bodies']},
       joints={j['name']:0. for a in SPEC['assemblies'] for j in a.get('joints',[])})


def target_frame():
    """Semantic goal fixture. It is deliberately NOT a physical replay or native result."""
    f=initial()
    assigned=set()
    for g in SPEC['goals']:
        for p in g['all']:
            if p['kind']=='pose':
                ref=f['bodies'].get(p.get('relative_to'))
                f['bodies'][p['body']]['pos']=list(S.add(ref['pos'],S.rotate(ref['quat'],p['pos']))) if ref else p['pos'].copy()
                f['bodies'][p['body']]['quat']=list(S.multiply(ref['quat'],p['quat'])) if ref else p['quat'].copy()
            elif p['kind']=='joint':f['joints'][p['joint']]=(p['min']+p['max'])/2
            elif p['kind']=='region' and p['body'] not in assigned:
                f['bodies'][p['body']]['pos']=[(a+b)/2 for a,b in zip(p['min'],p['max'])]
                assigned.add(p['body'])
    return f


def finish(sc,f=None):
    f=target_frame() if f is None else copy.deepcopy(f)
    dt=1/SPEC['control_hz']
    t=0. if sc.last_time is None else sc.last_time+dt
    if SPEC['threads']:
        for k in range(81):
            phase=k/80
            for thread in SPEC['threads']:
                name=thread['body'];p=next(p for g in SPEC['goals'] for p in g['all'] if p['kind']=='pose' and p['body']==name)
                ref=f['bodies'][thread['reference']]
                local=p['pos'].copy();local[2]+=(1-phase)*2*thread['pitch']
                f['bodies'][name]['pos']=list(S.add(ref['pos'],S.rotate(ref['quat'],local)))
                f['bodies'][name]['quat']=[0,0,math.sin(-4*math.pi*phase/2),math.cos(-4*math.pi*phase/2)]
            f['time']=t;sc.update(f);t+=dt
    for k in range(22):
        f['time']=t;result=sc.update(f);t+=dt
    return result,f


class SemanticTests(unittest.TestCase):
    def setUp(self):self.sc=S.Scorer(copy.deepcopy(SPEC))
    def test_initial_zero(self):self.assertEqual(self.sc.update(initial()).score,0.)
    def test_synthetic_target_earns_full_after_hold(self):
        result,_=finish(self.sc);self.assertTrue(result.success);self.assertEqual(result.score,1.)
    def test_no_instant_full_credit(self):self.assertLess(self.sc.update(target_frame()).score,1.)
    def test_no_credit_when_held(self):
        f=target_frame();f['robot_clearance']=.019
        result,_=finish(self.sc,f);self.assertFalse(result.success);self.assertLess(result.score,1.)
    def test_release_threshold_inclusive(self):
        f=target_frame();f['robot_clearance']=.02
        result,_=finish(self.sc,f);self.assertTrue(result.success)
    def test_missing_body_fails_closed(self):
        f=initial();f['bodies'].pop(next(iter(f['bodies'])))
        self.assertEqual(self.sc.update(f).failure,'missing_or_unexpected_body')
    def test_unexpected_body_fails_closed(self):
        f=initial();f['bodies']['unexpected']=copy.deepcopy(next(iter(f['bodies'].values())))
        self.assertEqual(self.sc.update(f).score,0.);self.assertIsNotNone(self.sc.result.failure)
    def test_nan_rejected(self):
        f=initial();next(iter(f['bodies'].values()))['pos'][0]=math.nan
        self.assertIsNotNone(self.sc.update(f).failure)
    def test_invalid_quaternion_rejected(self):
        f=initial();next(iter(f['bodies'].values()))['quat']=[0,0,0,2]
        self.assertIsNotNone(self.sc.update(f).failure)
    def test_malformed_body_fails_closed(self):
        f=initial();f['bodies'][next(iter(f['bodies']))]=None
        self.assertIsNotNone(self.sc.update(f).failure)
    def test_negative_weight_rejected(self):
        spec=copy.deepcopy(SPEC);spec['goals'][0]['weight']=-1
        with self.assertRaises(ValueError):S.Scorer(spec)
    def test_unknown_reference_rejected(self):
        spec=copy.deepcopy(SPEC);spec['goals'][0]['all'].append(dict(kind='still',body='missing'))
        with self.assertRaises(ValueError):S.Scorer(spec)
    def test_joint_limit_violation_invalidates(self):
        if not self.sc.joint_specs:self.skipTest('No mechanical joint in this scene')
        f=initial();name=next(iter(self.sc.joint_specs));f['joints'][name]=self.sc.joint_specs[name]['upper']+.02
        self.assertEqual(self.sc.update(f).failure,'joint_limit_violation:'+name)
    def test_quaternion_sign_is_irrelevant(self):
        f=target_frame()
        for b in f['bodies'].values():b['quat']=[-v for v in b['quat']]
        result,_=finish(self.sc,f);self.assertTrue(result.success)
    def test_robot_clearance_required(self):
        f=initial();del f['robot_clearance']
        self.assertEqual(self.sc.update(f).failure,'missing_robot_clearance')
    def test_penetration_latches(self):
        f=initial();f['max_penetration']=SPEC['penetration_limit']+.00001
        self.sc.update(f);r,_=finish(self.sc);self.assertEqual(r.score,0.);self.assertEqual(r.failure,'interpenetration')
    def test_loss_is_irreversible(self):
        f=initial();name=next(b['name'] for a in SPEC['assemblies'] for b in a['bodies'] if not b['anchor'])
        f['bodies'][name]['pos'][2]=SPEC['table_top']-.1
        self.sc.update(f);r,_=finish(self.sc);self.assertEqual(r.score,0.);self.assertIn('off_table',r.failure)
    def test_same_frame_does_not_advance_hold(self):
        f=target_frame()
        for _ in range(100):r=self.sc.update(f)
        self.assertFalse(r.success);self.assertEqual(r.simulated_seconds,0.)
    def test_conflicting_same_timestamp_invalidates(self):
        self.sc.update(initial());f=target_frame();r=self.sc.update(f)
        self.assertEqual(r.failure,'nonmonotonic_or_conflicting_frame')
    def test_reversed_time_invalidates(self):
        f=initial();f['time']=1.;self.sc.update(f);f['time']=.5
        self.assertIsNotNone(self.sc.update(f).failure)
    def test_gap_does_not_prove_hold(self):
        f=target_frame();self.sc.update(f);f['time']=10.
        self.assertFalse(self.sc.update(f).success)
    def test_reset_removes_failure_and_history(self):
        f=initial();f['max_penetration']=.1;self.sc.update(f);self.sc.reset()
        self.assertIsNone(self.sc.result.failure);self.assertFalse(self.sc.first);self.assertEqual(self.sc.update(initial()).score,0.)
    def test_mutating_input_does_not_change_cached_result(self):
        f=initial();r=self.sc.update(f);f['time']=10.
        self.assertEqual(r.simulated_seconds,0.);self.assertEqual(self.sc.last_frame['time'],0.)
    def test_motion_blocks_full_score(self):
        f=target_frame();name=next(b['name'] for a in SPEC['assemblies'] for b in a['bodies'] if not b['anchor'])
        f['bodies'][name]['linear']=[.011,0,0];r,_=finish(self.sc,f);self.assertFalse(r.success)
    def test_fixture_displacement_rejected(self):
        anchors=[b for a in SPEC['assemblies'] for b in a['bodies'] if b['anchor']]
        if not anchors:
            f=initial();f['bodies']['bracket']['pos'][0]+=.03
        else:
            f=initial();f['bodies'][anchors[0]['name']]['pos'][0]+=.006
        self.assertIsNotNone(self.sc.update(f).failure)
    def test_pose_distance_boundary(self):
        p=next(p for g in SPEC['goals'] for p in g['all'] if p['kind']=='pose') if any(p['kind']=='pose' for g in SPEC['goals'] for p in g['all']) else None
        if p is None:
            p=dict(kind='pose',body=next(iter(initial()['bodies'])),pos=[.3,0,.8],quat=[0,0,0,1],tolerance=.003,angle=.1)
            f=initial();f['bodies'][p['body']]['pos']=p['pos'].copy();f['bodies'][p['body']]['quat']=p['quat'].copy()
        else:f=target_frame()
        f['bodies'][p['body']]['pos'][0]+=p['tolerance']
        self.assertTrue(self.sc.predicate(p,f));f['bodies'][p['body']]['pos'][0]+=.000001
        self.assertFalse(self.sc.predicate(p,f))
    def test_region_requires_entire_object(self):
        name=next(iter(initial()['bodies']));f=initial()
        p=dict(kind='region',body=name,min=f['bodies'][name]['pos'].copy(),max=[v+.001 for v in f['bodies'][name]['pos']])
        self.assertFalse(self.sc.predicate(p,f))
    def test_distractors_cannot_be_kit_contents(self):
        if not SPEC.get('forbidden_regions'):self.skipTest('No kit distractors in this scene')
        for forbidden in SPEC.get('forbidden_regions',[]):
            with self.subTest(body=forbidden['body']):
                sc=S.Scorer(SPEC);f=target_frame();f['bodies'][forbidden['body']]['pos']=[(x+y)/2 for x,y in zip(forbidden['min'],forbidden['max'])]
                self.assertIsNotNone(sc.update(f).failure)
    def test_healthy_component_preservation(self):
        if not SPEC['invariants']:self.skipTest('No preservation invariant in this scene')
        for inv in SPEC['invariants']:
            with self.subTest(invariant=inv['name']):
                sc=S.Scorer(SPEC);f=initial();name=inv['all'][0]['body'];f['bodies'][name]['pos'][0]+=.04
                self.assertIsNotNone(sc.update(f).failure)
    def test_direct_thread_drop_gets_no_turn_credit(self):
        if not SPEC['threads']:self.skipTest('No threaded parts in this scene')
        if SPEC['threads']:
            f=target_frame()
            for k in range(22):f['time']=k/20;result=self.sc.update(f)
            self.assertEqual(result.score,0.)
    def test_free_spinning_does_not_thread(self):
        if not SPEC['threads']:self.skipTest('No threaded parts in this scene')
        if SPEC['threads']:
            f=target_frame()
            for k in range(81):
                for t in SPEC['threads']:f['bodies'][t['body']]['quat']=[0,0,math.sin(-4*math.pi*k/160),math.cos(-4*math.pi*k/160)]
                f['time']=k/20;result=self.sc.update(f)
            self.assertEqual(result.score,0.)
    def test_wrong_joint_position_loses_condition(self):
        if not any(p['kind']=='joint' for g in SPEC['goals'] for p in g['all']):self.skipTest('No scored joint in this scene')
        for g in SPEC['goals']:
            for p in g['all']:
                if p['kind']=='joint':
                    f=target_frame();f['joints'][p['joint']]=p['max']+.01
                    self.assertFalse(self.sc.predicate(p,f))
    def test_wrong_orientation_fails_pose(self):
        if not any(p['kind']=='pose' and p['angle']<math.pi/2 for g in SPEC['goals'] for p in g['all']):self.skipTest('No oriented pose in this scene')
        for g in SPEC['goals']:
            for p in g['all']:
                if p['kind']=='pose' and p['angle']<math.pi/2:
                    f=target_frame();f['bodies'][p['body']]['quat']=list(S.multiply(f['bodies'][p['body']]['quat'],[1,0,0,0]))
                    self.assertFalse(self.sc.predicate(p,f))
    def test_weight_and_identity_schema(self):
        self.assertAlmostEqual(sum(g['weight'] for g in SPEC['goals']),1.)
        self.assertEqual(len(self.sc.body_specs),sum(len(a['bodies']) for a in SPEC['assemblies']))
    def test_geometry_separation_and_overlap(self):
        a=([0,0,0],[.01,.02,.03],[(1,0,0),(0,1,0),(0,0,1)])
        self.assertEqual(G.penetration(a,([1,0,0],a[1],a[2])),0.)
        self.assertAlmostEqual(G.penetration(a,([.019,0,0],a[1],a[2])),.001)


if __name__=='__main__':unittest.main()
