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
                if 'local_point' in p:
                    body=f['bodies'][p['body']]
                    body['pos']=list(S.sub(body['pos'],S.rotate(body['quat'],p['local_point'])))
            elif p['kind']=='joint':f['joints'][p['joint']]=(p['min']+p['max'])/2
            elif p['kind']=='region' and p['body'] not in assigned:
                bounds=next(b for a in SPEC['assemblies'] for b in a['bodies'] if b['name']==p['body'])
                centre=S.rotate(f['bodies'][p['body']]['quat'],[(a+b)/2 for a,b in zip(bounds['bounds_min'],bounds['bounds_max'])])
                f['bodies'][p['body']]['pos']=[(a+b)/2-c for a,b,c in zip(p['min'],p['max'],centre)]
                assigned.add(p['body'])
    for g in SPEC['goals']:
        for p in g['all']:
            if p['kind']=='axis':
                import numpy as np
                a=np.array(p.get('local_axis',[0,0,1]),dtype=float);b=np.array(p['direction'],dtype=float)
                if np.dot(a,b)<-0.9999:
                    axis=np.cross(a,[0,0,1] if abs(a[2])<.9 else [0,1,0]);axis/=np.linalg.norm(axis);q=[*axis,0]
                else:
                    q=np.r_[np.cross(a,b),1+np.dot(a,b)];q=(q/np.linalg.norm(q)).tolist()
                if p.get('relative_to'):q=S.multiply(f['bodies'][p['relative_to']]['quat'],q)
                f['bodies'][p['body']]['quat']=list(q)
    if SPEC.get("continuity"):
        fit_cables(f)
    return f


def fit_cables(frame):
    """Geometric continuity fixture for scorer tests, NOT a dynamic cable replay.

    FABRIK preserves segment lengths and the two fixed endpoints. This tests the
    scorer's continuity logic; native tests separately exercise constrained joints.
    """
    import numpy as np
    from feedback import rotate,conjugate
    for assembly in SPEC['assemblies']:
        links=[b for b in assembly['bodies'] if '_link_' in b['name']]
        if not links:continue
        joints=assembly['joints'];anchor=assembly['bodies'][0];plug=next(b for b in assembly['bodies'] if b['name'].startswith('plug_'))
        twists=[next(j for j in joints if j['child']==b['name']) for b in links]
        ends=[next(j for j in joints if j['parent']==b['name']) for b in links]
        points=[np.array(anchor['pos'])]+[np.array(b['pos'])+np.array(j['pivot_parent']) for b,j in zip(links,ends)]
        original=np.array(points);lengths=np.linalg.norm(np.diff(original,axis=0),axis=1)
        terminal=next(j for j in joints if j['child']==plug['name'])
        target=np.array(frame['bodies'][plug['name']]['pos'])+rotate(frame['bodies'][plug['name']]['quat'],terminal['pivot_child'])
        if np.linalg.norm(target-original[0])>=sum(lengths):raise ValueError('Cable fixture cannot reach target')
        points=np.array(points);root=points[0].copy()
        for _ in range(2000):
            points[-1]=target
            for i in range(len(lengths)-1,-1,-1):
                d=points[i]-points[i+1];points[i]=points[i+1]+d*lengths[i]/np.linalg.norm(d)
            points[0]=root
            for i,length in enumerate(lengths):
                d=points[i+1]-points[i];points[i+1]=points[i]+d*length/np.linalg.norm(d)
            if np.linalg.norm(points[-1]-target)<1e-7:break
        else:raise ValueError('Cable fixture did not converge')
        for i,(body,joint,end) in enumerate(zip(links,twists,ends)):
            a=original[i+1]-original[i];b=points[i+1]-points[i];a/=np.linalg.norm(a);b/=np.linalg.norm(b)
            q=np.r_[np.cross(a,b),1+np.dot(a,b)];q/=np.linalg.norm(q)
            frame['bodies'][body['name']]['quat']=q.tolist()
            frame['bodies'][body['name']]['pos']=(points[i]-rotate(q,joint['pivot_child'])).tolist()
        for joint in joints:
            child=joint['child']
            if child.startswith('cable_') and '_link_' not in child:
                parent=frame['bodies'][joint['parent']]
                frame['bodies'][child]['pos']=(np.array(parent['pos'])+rotate(parent['quat'],joint['pivot_parent'])).tolist()
        latch=next((j for j in joints if j['kind']=='prismatic'),None)
        if latch:
            parent=frame['bodies'][latch['parent']]
            frame['bodies'][latch['child']]['pos']=(np.array(parent['pos'])+rotate(parent['quat'],latch['pivot_parent'])+[0,0,frame['joints'][latch['name']]]).tolist()


def finish(sc,f=None):
    f=target_frame() if f is None else copy.deepcopy(f)
    dt=1/SPEC['control_hz']
    t=0. if sc.last_time is None else sc.last_time+dt
    if SPEC['threads']:
        turns=math.ceil(max(p['min'] for g in SPEC['goals'] for p in g['all'] if p['kind']=='turns')*8)/8
        samples=math.ceil(turns*40)
        for k in range(samples+1):
            phase=k/samples
            for thread in SPEC['threads']:
                name=thread['body'];p=next(p for g in SPEC['goals'] for p in g['all'] if p['kind']=='pose' and p['body']==name)
                ref=f['bodies'][thread['reference']]
                local=p['pos'].copy();local[2]+=(1-phase)*turns*thread['pitch']
                f['bodies'][name]['pos']=list(S.add(ref['pos'],S.rotate(ref['quat'],local)))
                f['bodies'][name]['quat']=[0,0,math.sin(-2*turns*math.pi*phase/2),math.cos(-2*turns*math.pi*phase/2)]
            f['time']=t;sc.update(f);t+=dt
    for k in range(math.ceil(SPEC['hold_seconds']/dt)+3):
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
        start = f['bodies'][name]['pos'][0]
        for step in range(61):
            f['time'] = step / SPEC['control_hz']
            f['bodies'][name]['pos'][0] = start + .00055 * (step % 2)
            result = self.sc.update(f)
            self.assertFalse(result.success)
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

    def test_every_pose_rejects_near_miss_and_wrong_target(self):
        for goal in SPEC['goals']:
            for p in goal['all']:
                if p['kind']!='pose':continue
                with self.subTest(goal=goal['name'],body=p['body']):
                    f=target_frame();body=f['bodies'][p['body']]
                    self.assertTrue(self.sc.predicate(p,f))
                    body['pos'][0]+=p['tolerance']+.00001
                    self.assertFalse(self.sc.predicate(p,f))
                    body['pos'][0]+=.05;self.assertFalse(self.sc.predicate(p,f))

    def test_every_axis_rejects_reversed_polarity(self):
        for goal in SPEC['goals']:
            for p in goal['all']:
                if p['kind']!='axis':continue
                with self.subTest(body=p['body']):
                    f=target_frame();self.assertTrue(self.sc.predicate(p,f))
                    local=p.get('local_axis',[0,0,1]);flip=[0,1,0,0] if abs(local[1])<.9 else [1,0,0,0]
                    f['bodies'][p['body']]['quat']=list(S.multiply(f['bodies'][p['body']]['quat'],flip))
                    self.assertFalse(self.sc.predicate(p,f))

    def test_completed_component_displacement_removes_credit(self):
        result,f=finish(self.sc);self.assertTrue(result.success)
        predicate=next((p for g in SPEC['goals'] for p in g['all'] if p['kind'] in ('pose','region')),None)
        if predicate is None:self.skipTest('No movable goal body')
        f['time']+=1/SPEC['control_hz'];f['bodies'][predicate['body']]['pos'][0]+=.10
        result=self.sc.update(f);self.assertLess(result.score,1);self.assertFalse(result.success)

    def test_broken_connection_cannot_earn_partial_credit(self):
        for connection in SPEC.get('continuity',[])[:1]:
            f=initial();joint=self.sc.joint_specs[connection['joint']]
            f['bodies'][joint['child']]['pos'][0]+=connection['tolerance']+.00001
            result=self.sc.update(f);self.assertEqual(result.score,0)
            self.assertTrue(result.failure.startswith('broken_connection:'))

    def test_forced_catch_is_irreversible(self):
        guards=SPEC.get('latch_release_guards',[])
        if not guards:return
        # Isolate the catch crossing rule from the independently tested cable graph.
        spec=copy.deepcopy(SPEC);spec['continuity']=[];sc=S.Scorer(spec)
        f=initial();sc.update(f);guard=guards[0]
        f['time']=.05;f['bodies'][guard['body']]['pos'][1]+=guard['catch_distance']+.0001
        result=sc.update(f);self.assertEqual(result.score,0)
        self.assertEqual(result.failure,'catch_forced_without_release:'+guard['body'])


    def test_closed_collar_numeric_stop_margin_is_bounded(self):
        frame = target_frame()
        for goal in SPEC['goals']:
            for predicate in goal['all']:
                if predicate['kind'] == 'joint' and predicate['joint'] == 'collar_hinge':
                    frame['joints']['collar_hinge'] = 7.563458193082795e-10
                    self.assertTrue(self.sc.predicate(predicate, frame))
                    frame['joints']['collar_hinge'] = .000002
                    self.assertFalse(self.sc.predicate(predicate, frame))
                    frame['joints']['collar_hinge'] = -.02501
                    self.assertFalse(self.sc.predicate(predicate, frame))


    def test_radial_fit_and_axial_registration_are_independent(self):
        predicate = next(p for g in SPEC['goals'] for p in g['all']
                         if p['kind'] == 'pose' and p['body'] == 'lower_collar')
        frame = target_frame()
        reference = frame['bodies']['captive_shaft']['pos']
        body = frame['bodies']['lower_collar']
        for delta, expected in (([-.0004058, .0005985, -.0013154], True),
                                ([.00151, 0, 0], False), ([0, .00151, 0], False)):
            body['pos'] = [a+b for a, b in zip(reference, delta)]
            self.assertEqual(self.sc.predicate(predicate, frame), expected)

    def test_invalid_pose_axis_is_rejected(self):
        specification = copy.deepcopy(SPEC)
        predicate = next(p for g in specification['goals'] for p in g['all']
                         if p['kind'] == 'pose' and p['body'] == 'lower_collar')
        predicate['position_axis'] = [0, 0, 0]
        with self.assertRaises(ValueError):
            S.Scorer(specification)


if __name__=='__main__':unittest.main()


class ObservedMotionTests(unittest.TestCase):
    def test_stationary_poses_have_zero_observed_motion_despite_solver_velocity(self):
        scorer = S.Scorer(SPEC)
        frame = initial()
        scorer.update(frame)
        next_frame = copy.deepcopy(frame)
        next_frame['time'] = .05
        name = next(iter(frame['bodies']))
        next_frame['bodies'][name]['angular'] = [1., 0., 0.]
        scorer.previous_observation = frame
        self.assertEqual(scorer.observed_motion(name, next_frame), (0., 0.))

    def test_observed_displacement_and_rotation_remain_disqualifying(self):
        scorer = S.Scorer(SPEC)
        frame = initial()
        name = next(iter(frame['bodies']))
        next_frame = copy.deepcopy(frame)
        next_frame['time'] = .05
        next_frame['bodies'][name]['pos'][0] += .001
        next_frame['bodies'][name]['quat'] = [0., 0., math.sin(.01), math.cos(.01)]
        scorer.previous_observation = frame
        speed, spin = scorer.observed_motion(name, next_frame)
        self.assertGreater(speed, .01)
        self.assertGreater(spin, .2)

    def test_unobserved_gap_uses_raw_rates(self):
        scorer = S.Scorer(SPEC)
        frame = initial()
        name = next(iter(frame['bodies']))
        next_frame = copy.deepcopy(frame)
        next_frame['time'] = .1
        next_frame['bodies'][name]['angular'] = [1., 0., 0.]
        scorer.previous_observation = frame
        self.assertEqual(scorer.observed_motion(name, next_frame), (0., 1.))


class FunctionalHangerScoringTests(unittest.TestCase):
    def test_hanger_assembly_without_payload_is_only_partial_credit(self):
        frame=target_frame()
        frame['bodies']['proof_load']=initial()['bodies']['proof_load']
        result,_=finish(S.Scorer(SPEC),frame)
        self.assertFalse(result.success)
        self.assertAlmostEqual(result.score,.65)
        self.assertNotIn('proof_load_supported',result.completed)

    def test_payload_pose_without_seam_key_cannot_earn_load_credit(self):
        frame=target_frame()
        frame['bodies']['collar_key']=initial()['bodies']['collar_key']
        result,_=finish(S.Scorer(SPEC),frame)
        self.assertFalse(result.success)
        self.assertNotIn('collar_retained',result.completed)
        self.assertNotIn('proof_load_supported',result.completed)

    def test_moving_load_blocks_full_score(self):
        frame=target_frame();base_x=frame['bodies']['proof_load']['pos'][0]
        scorer=S.Scorer(SPEC)
        for k in range(math.ceil(SPEC['hold_seconds']*SPEC['control_hz'])+4):
            frame['time']=k/SPEC['control_hz']
            frame['bodies']['proof_load']['pos'][0]=base_x+(.001 if k%2 else -.001)
            frame['bodies']['proof_load']['linear']=[.04,0,0]
            result=scorer.update(frame)
            self.assertFalse(result.success)
        self.assertNotIn('proof_load_supported',result.completed)


class EyeLandmarkScoringTests(unittest.TestCase):
    def test_valid_hanging_tilt_preserves_contact_landmark_credit(self):
        frame=target_frame();body=frame['bodies']['proof_load']
        predicate=next(p for p in SPEC['goals'][-1]['all'] if 'local_point' in p)
        seat=S.add(body['pos'],S.rotate(body['quat'],predicate['local_point']))
        body['quat']=[0,math.sin(.1/2),0,math.cos(.1/2)]
        body['pos']=list(S.sub(seat,S.rotate(body['quat'],predicate['local_point'])))
        before=copy.deepcopy(frame)
        result,_=finish(S.Scorer(SPEC),frame)
        self.assertTrue(result.success);self.assertEqual(result.score,1)
        self.assertEqual(frame,before)
