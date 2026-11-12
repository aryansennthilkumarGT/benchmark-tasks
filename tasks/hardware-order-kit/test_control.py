"""Offline controller contract tests. No native physics is simulated here."""
import copy
import json
import math
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent))
from feedback import Controller,ControlFailure,Motion,axis_quat,interpolate,limit_vector,multiply,qangle,rotate


class GeometryTests(unittest.TestCase):
    def test_quaternion_shortest_path_across_sign(self):
        q=axis_quat([0,1,0],1.2)
        self.assertLess(qangle(interpolate(q,-q,.5),q),1e-6)
    def test_rotation_preserves_length(self):
        self.assertAlmostEqual(np.linalg.norm(rotate(axis_quat([1,2,3],2.1),[.3,-.4,.2])),math.sqrt(.29))
    def test_cartesian_step_is_bounded(self):
        self.assertAlmostEqual(np.linalg.norm(limit_vector([1,2,3],.003)),.003)
    def test_invalid_quaternion_is_rejected(self):
        with self.assertRaises(ControlFailure):interpolate([0,0,0,0],[0,0,0,1],.5)


class FeedbackTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from yam_arena import ik,station
        from yam_arena.demo import DOWN_GRIP
        from yam_arena.constants import READY
        cls.ik=ik;cls.station=station;cls.down=DOWN_GRIP
        cls.folder=Path(__file__).resolve().parent
        cls.spec=json.loads((cls.folder/'scene.json').read_text())
        cls.frame={'schema':1,'time':0.,'max_penetration':0.,'robot_clearance':.03,
                   'bodies':{b['name']:{'pos':list(b['pos']),'quat':list(b['quat']),
                               'linear':[0,0,0],'angular':[0,0,0]} for a in cls.spec['assemblies'] for b in a['bodies']},
                   'joints':{j['name']:0. for a in cls.spec['assemblies'] for j in a.get('joints',[])}}
        cls.ready=np.tile(np.r_[READY,1.],2)
    def controller(self,phase):return Controller({'phases':[dict(label='contract-test',side='left',**phase)]},self.spec)
    def test_upper_grip_has_margin_at_recorded_loaded_lift_pose(self):
        plan = json.loads((self.folder/'controller.json').read_text())
        planned = next(x['quat'] for x in plan['phases'] if x['label']=='Grasp upper collar handle')
        previous = np.array([-0.7660444431189781, 0.6427876096865394, 0.0, 0.0])
        inverse = previous.copy(); inverse[:3] *= -1
        target_q = multiply(multiply([0.5783732440671672, -0.48704451786169844, 0.505459012755517, -0.4156720036186043], inverse), planned)
        solved, pe, re = self.ik.solve([0.1432722892516486, -0.0879180433802464, 0.9063154301571943], target_q, q_init=np.array([1.681949064556588, 1.7060044574807247, 0.8933529458726809, -1.448854462096858, 1.3788384620845224, 2.086443027914426]),
                                       base_pos=self.station.BASES['right'], iters=100, damping=.015, tol=2e-5)
        self.assertLess(pe, .0015)
        self.assertLess(re, .035)
        self.assertGreater(float(np.min(np.minimum(solved-self.ik.LOWER, self.ik.UPPER-solved))), .12)

    def test_lower_grasp_engages_handle_depth_with_table_clearance(self):
        # Real recorded pose from the failed lift; geometry only, not a physics test.
        import robot_geometry
        fixture=json.loads((self.folder/'offline-evidence/recorded-lower-grasp.json').read_text())
        body=fixture['body'];observed=fixture['joints']
        phase=json.loads((self.folder/'controller.json').read_text())['phases'][1]
        target=np.asarray(body['pos'])+rotate(body['quat'],phase['offset'])
        arm,pe,re=self.ik.solve(target,phase['quat'],q_init=np.asarray(observed[:6]),
            base_pos=self.station.BASES['left'],iters=100,damping=.015,tol=2e-5)
        self.assertLess(pe,.0015);self.assertLess(re,.035)
        hulls=[h for h in robot_geometry.arm_hulls('left',np.r_[arm,observed[6]]) if 'tip' in h['link']]
        clearance=min(float(h['polyhedron'][0][:,2].min()) for h in hulls)-self.spec['table_top']
        self.assertGreater(clearance,.015)
        depths={}
        inverse=np.asarray(body['quat']).copy();inverse[:3]*=-1
        for hull in hulls:
            points=np.array([rotate(inverse,v-np.asarray(body['pos'])) for v in hull['polyhedron'][0]])
            lo=points.min(axis=0);hi=points.max(axis=0)
            if lo[0]<-.0405 and hi[0]>-.0595 and lo[1]<.1045 and hi[1]>.0755:
                overlap=max(0.,min(hi[2],.004)-max(lo[2],-.024))
                depths[hull['link']]=max(depths.get(hull['link'],0.),overlap)
        self.assertEqual(set(depths),{'tip_left','tip_right'})
        self.assertGreater(min(depths.values()),.015)

    def test_cooperative_carry_commands_a_consistent_relative_grasp(self):
        # Actual first-lift state; both hand targets must move as one held assembly.
        fixture=json.loads((self.folder/'offline-evidence/cooperative-lift-state.json').read_text())
        phase=copy.deepcopy(fixture['phase']);phase['coordinate_relative_holds']=True
        controller=Controller({'phases':[phase]},self.spec)
        controller.grasps=copy.deepcopy(fixture['grasps'])
        controller.holds=copy.deepcopy(fixture['holds'])
        frame=copy.deepcopy(fixture['frame']);unchanged=copy.deepcopy(frame)
        joints=np.asarray(fixture['joints']);targets={}
        for side in ('left','right'):
            def capture(measured,p,q,opening,*,name=side,**kwargs):
                targets[name]=(np.asarray(p),np.asarray(q))
                return np.asarray(measured),0.,0.
            controller.motion[side].target=capture
        left,lq=controller.pose(joints[:7],'left')
        # Preserve the captured support target, including its existing measured
        # compliance error; cooperative planning must not introduce a new one.
        right,rq=controller.world_target(controller.holds['right'],frame)
        controller.step(joints,frame)
        lp,lqq=targets['left'];rp,rqq=targets['right']
        lqi=np.asarray(lq).copy();lqi[:3]*=-1
        lqqi=np.asarray(lqq).copy();lqqi[:3]*=-1
        expected=rotate(lqi,right-left);commanded=rotate(lqqi,rp-lp)
        self.assertLess(np.linalg.norm(commanded-expected),.001)
        self.assertLess(qangle(multiply(lqi,rq),multiply(lqqi,rqq)),.003)
        self.assertEqual(frame,unchanged)  # Joint targets only; never move simulated bodies.

    def test_cooperative_insert_keeps_axial_alignment_gate_for_both_hands(self):
        # Actual first-lift state; both hand targets must move as one held assembly.
        fixture=json.loads((self.folder/'offline-evidence/cooperative-lift-state.json').read_text())
        phase=copy.deepcopy(json.loads((self.folder/'controller.json').read_text())['phases'][7])
        phase['coordinate_relative_holds']=True
        controller=Controller({'phases':[phase]},self.spec)
        controller.grasps=copy.deepcopy(fixture['grasps'])
        controller.holds=copy.deepcopy(fixture['holds'])
        frame=copy.deepcopy(fixture['frame']);unchanged=copy.deepcopy(frame)
        joints=np.asarray(fixture['joints']);targets={}
        for side in ('left','right'):
            def capture(measured,p,q,opening,*,name=side,**kwargs):
                targets[name]=(np.asarray(p),np.asarray(q))
                return np.asarray(measured),0.,0.
            controller.motion[side].target=capture
        left,lq=controller.pose(joints[:7],'left')
        # Preserve the captured support target, including its existing measured
        # compliance error; cooperative planning must not introduce a new one.
        right,rq=controller.world_target(controller.holds['right'],frame)
        controller.step(joints,frame)
        lp,lqq=targets['left'];rp,rqq=targets['right']
        lqi=np.asarray(lq).copy();lqi[:3]*=-1
        lqqi=np.asarray(lqq).copy();lqqi[:3]*=-1
        expected=rotate(lqi,right-left);commanded=rotate(lqqi,rp-lp)
        self.assertLess(np.linalg.norm(commanded-expected),.001)
        self.assertLess(qangle(multiply(lqi,rq),multiply(lqqi,rqq)),.003)
        inverse_left=np.asarray(lq).copy();inverse_left[:3]*=-1
        turn=multiply(lqq,inverse_left)
        body_position=np.asarray(frame['bodies']['lower_collar']['pos'])
        planned_parent=lp-rotate(turn,left-body_position)
        self.assertAlmostEqual(planned_parent[2],body_position[2],places=8)
        self.assertEqual(frame,unchanged)  # Joint targets only; never move simulated bodies.

    def test_near_goal_carry_target_contracts_instead_of_overshooting(self):
        fixture=json.loads((self.folder/'offline-evidence/cooperative-carry-near-goal.json').read_text())
        phase=json.loads((self.folder/'controller.json').read_text())['phases'][6]
        controller=Controller({'phases':[phase]},self.spec)
        frame=copy.deepcopy(fixture['frame']);joints=np.asarray(fixture['joints'])
        body=frame['bodies']['lower_collar'];bp=np.asarray(body['pos']);inverse=np.asarray(body['quat']).copy();inverse[:3]*=-1
        left,lq=controller.pose(joints[:7],'left');right,rq=controller.pose(joints[7:],'right')
        controller.grasps['left']=dict(body='lower_collar',verified=False,
            tcp_in_body=rotate(inverse,left-bp),tcp_rotation_in_body=multiply(inverse,lq))
        controller.holds['right']=dict(relative_to='lower_collar',pos=rotate(inverse,right-bp),
            quat=multiply(inverse,rq),opening=0.,speed=.035,feedback_gain=2.)
        targets={}
        for side in ('left','right'):
            def capture(measured,p,q,opening,*,name=side,**kwargs):
                targets[name]=(np.asarray(p),np.asarray(q));return np.asarray(measured),0.,0.
            controller.motion[side].target=capture
        controller.step(joints,frame)
        inverse_left=np.asarray(lq).copy();inverse_left[:3]*=-1
        turn=multiply(targets['left'][1],inverse_left)
        planned_parent=targets['left'][0]-rotate(turn,left-bp)
        goal=np.asarray(phase['target']['pos'])
        self.assertLessEqual(np.linalg.norm(planned_parent-goal),np.linalg.norm(bp-goal)+1e-8)

    def test_hold_requires_actual_stationarity(self):
        c=self.controller(dict(kind='hold',seconds=1.,opening=1.))
        frame=copy.deepcopy(self.frame)
        for t in (0,.5):frame['time']=t;c.step(self.ready,frame)
        self.assertEqual(c.index,0)
    def test_phase_timeout_is_not_success(self):
        c=self.controller(dict(kind='move',target={'pos':[.2,.24,.84],'quat':self.down.tolist()},timeout=.1))
        c.step(self.ready,self.frame)
        frame=copy.deepcopy(self.frame);frame['time']=.2
        with self.assertRaisesRegex(ControlFailure,'timeout'):c.step(self.ready,frame)
        self.assertEqual(c.index,0)
    def test_nonfinite_proprioception_rejected(self):
        m=Motion('left')
        with self.assertRaises(ControlFailure):m.target([float('nan')]*7,[.2,.2,.85],self.down,1)
    def test_physical_intersection_aborts(self):
        c=self.controller(dict(kind='hold',seconds=1))
        frame=copy.deepcopy(self.frame);frame['max_penetration']=.01
        with self.assertRaisesRegex(ControlFailure,'interpenetration'):c.step(self.ready,frame)
    def test_grasp_slip_is_detected(self):
        c=self.controller(dict(kind='hold',seconds=1));body=next(iter(self.frame['bodies']))
        c.grasps['left']={'body':body,'verified':True,'tcp_in_body':[0,0,0],
                           'tcp_rotation_in_body':[0,0,0,1],'slip_tolerance':.001}
        with self.assertRaisesRegex(ControlFailure,'slipped'):c.check_grasp_slip('left',self.ready[:7],self.frame)
    def test_grasp_never_verified_by_empty_finger_closure(self):
        plan=json.loads((self.folder/'controller.json').read_text())
        phase=next(p for p in plan['phases'] if p['kind']=='grasp')
        c=Controller({'phases':[phase]},self.spec);frame=copy.deepcopy(self.frame)
        b=frame['bodies'][phase['body']];side=phase['side'];index=0 if side=='left' else 7
        p=np.asarray(b['pos'])+rotate(b['quat'],phase['offset'])
        q,pe,re=self.ik.solve(p,phase['quat'],base_pos=self.station.BASES[side],iters=400,damping=.015)
        self.assertLess(pe,.0015);joints=self.ready.copy();joints[index:index+6]=q;joints[index+6]=0
        for t in (0,.5,1.):frame['time']=t;c.step(joints,frame)
        self.assertEqual(c.index,0);self.assertFalse(c.grasps)
    def test_incremental_action_respects_joint_and_gripper_limits(self):
        m=Motion('left');p,r=m.ik.tcp_pose(self.ready[:6],m.base)
        action,_,_=m.target(self.ready[:7],p+[.001,0,0],m.ik.matrix_to_quat_xyzw(r),0)
        self.assertLessEqual(float(np.max(np.abs(action[:6]-self.ready[:6]))),.045+1e-12)
        self.assertGreaterEqual(action[6],.9)

    def test_fingers_stay_open_during_unfinished_approach(self):
        plan=json.loads((self.folder/'controller.json').read_text());phase=next(p for p in plan['phases'] if p['kind']=='grasp')
        c=Controller({'phases':[phase]},self.spec);frame=copy.deepcopy(self.frame)
        side=phase['side'];index=0 if side=='left' else 7;body=frame['bodies'][phase['body']]
        target=np.array(body['pos'])+rotate(body['quat'],phase['offset'])
        q,pe,re=self.ik.solve(target+[0,0,.01],phase['quat'],base_pos=self.station.BASES[side],iters=500,damping=.015)
        self.assertLess(pe,.0015);joints=self.ready.copy();joints[index:index+6]=q;joints[index+6]=.3
        action=c.step(joints,frame)
        self.assertGreater(action[index+6],joints[index+6]);self.assertFalse(c.grasp_closing);self.assertEqual(c.index,0)

    def test_measured_carry_translation_avoids_rotation_induced_descent(self):
        frame = copy.deepcopy(self.frame)
        body = frame['bodies']['lower_collar']
        body['quat'] = axis_quat([0, 1, 0], .16).tolist()
        goal = np.array(body['pos']) + [0, 0, .035]
        phase = dict(kind='carry', body='lower_collar', measured_translation=True,
                     target=dict(pos=goal.tolist(), quat=[0, 0, 0, 1]))
        controller = self.controller(phase)
        controller.grasps['left'] = dict(body='lower_collar', verified=False,
            tcp_in_body=[-.05, .145, .01], tcp_rotation_in_body=[0, 0, 0, 1])
        targets = []
        def capture(joints, position, orientation, opening, **kwargs):
            targets.append(np.array(position))
            return np.array(joints), 0., 0.
        controller.motion['left'].target = capture
        tcp, _ = controller.pose(self.ready[:7], 'left')
        controller.step(self.ready, frame)
        np.testing.assert_allclose(targets[0] - tcp, [0, 0, .003], atol=1e-12)

    def test_revolute_target_follows_measured_child_rotation(self):
        phase = dict(kind='joint', body='upper_collar', joint='collar_hinge',
                     value=-1.25, increment=.01)
        controller = self.controller(phase)
        frame = copy.deepcopy(self.frame)
        frame['joints']['collar_hinge'] = -.4
        frame['bodies']['upper_collar']['quat'] = axis_quat([0, 1, 0], -.4).tolist()
        controller.grasps['left'] = dict(body='upper_collar', verified=False,
            tcp_in_body=[.07, -.22, .043], tcp_rotation_in_body=[0, 0, 0, 1])
        targets = []
        def capture(joints, position, orientation, opening, **kwargs):
            targets.append(np.array(orientation))
            return np.array(joints), 0., 0.
        controller.motion['left'].target = capture
        controller.step(self.ready, frame)
        self.assertLess(qangle(targets[0], axis_quat([0, 1, 0], -.41)), 1e-6)

    def test_collar_carry_corrects_measured_body_rotation(self):
        frame = copy.deepcopy(self.frame)
        body = frame['bodies']['lower_collar']
        body['quat'] = axis_quat([0, 1, 0], .2).tolist()
        phase = dict(kind='carry', body='lower_collar', measured_rotation=True,
                     rotation_gain=3, rotation_lead=.08,
                     target=dict(pos=body['pos'], quat=[0, 0, 0, 1]))
        controller = self.controller(phase)
        controller.grasps['left'] = dict(body='lower_collar', verified=False,
            tcp_in_body=[0, 0, 0], tcp_rotation_in_body=[0, 0, 0, 1])
        targets = []
        def capture(joints, position, orientation, opening, **kwargs):
            targets.append(np.array(orientation))
            return np.array(joints), 0., 0.
        controller.motion['left'].target = capture
        _, tcp_quat = controller.pose(self.ready[:7], 'left')
        controller.step(self.ready, frame)
        expected = multiply(axis_quat([0, 1, 0], -.08), tcp_quat)
        self.assertLess(qangle(targets[0], expected), 1e-7)

    def test_body_rotation_preserves_centroid_with_offset_grasp(self):
        frame = copy.deepcopy(self.frame)
        body = frame['bodies']['lower_collar']
        body['quat'] = axis_quat([0, 1, 0], .2).tolist()
        phase = dict(kind='carry', body='lower_collar', measured_translation=True,
                     measured_rotation=True, rotation_about_body=True,
                     rotation_gain=1, rotation_lead=.04,
                     target=dict(pos=body['pos'], quat=[0, 0, 0, 1]))
        controller = self.controller(phase)
        controller.grasps['left'] = dict(body='lower_collar', verified=False,
            tcp_in_body=[0, 0, 0], tcp_rotation_in_body=[0, 0, 0, 1])
        targets = []
        def capture(joints, position, orientation, opening, **kwargs):
            targets.append(np.array(position))
            return np.array(joints), 0., 0.
        controller.motion['left'].target = capture
        tcp, _ = controller.pose(self.ready[:7], 'left')
        controller.step(self.ready, frame)
        lever = tcp - np.array(body['pos'])
        expected = np.array(body['pos']) + rotate(axis_quat([0, 1, 0], -.04), lever)
        np.testing.assert_allclose(targets[0], expected, atol=1e-12)

    def test_pose_feedback_integrates_measured_error_and_retains_reference_bias(self):
        motion = Motion('left')
        reference = self.ready[:6].copy()
        reference[1] += .01
        motion.reference = reference.copy()
        actual_p, actual_r = self.ik.tcp_pose(self.ready[:6], motion.base)
        reference_p, reference_r = self.ik.tcp_pose(reference, motion.base)
        actual_q = self.ik.matrix_to_quat_xyzw(actual_r)
        reference_q = self.ik.matrix_to_quat_xyzw(reference_r)
        calls = []
        def solve(position, orientation, **kwargs):
            calls.append((np.array(position), np.array(orientation)))
            return reference.copy(), 0., 0.
        with patch.object(self.ik, 'solve', side_effect=solve):
            motion.target(self.ready[:7], actual_p + [.001, 0, 0], actual_q, 1., feedback_gain=2.)
            motion.target(self.ready[:7], actual_p, actual_q, 1., feedback_gain=2.)
            rotated = multiply(axis_quat([0, 1, 0], .02), actual_q)
            motion.target(self.ready[:7], actual_p, rotated, 1., feedback_gain=2.)
        np.testing.assert_allclose(calls[0][0], reference_p + [.0001, 0, 0], atol=1e-12)
        np.testing.assert_allclose(calls[1][0], reference_p, atol=1e-12)
        expected = multiply(axis_quat([0, 1, 0], .002), reference_q)
        self.assertLess(qangle(calls[2][1], expected), 1e-7)

    def test_loaded_left_wrist_bias_can_advance_reference(self):
        controller = self.controller(dict(kind='hold', seconds=1))
        motion = controller.motion['left']
        reference = self.ready[:6].copy()
        reference[4] += .10
        motion.reference = reference.copy()
        position, rotation = self.ik.tcp_pose(reference, motion.base)
        orientation = self.ik.matrix_to_quat_xyzw(rotation)
        motion.target(self.ready[:7], position + [0, 0, .001], orientation, 0.)
        self.assertGreater(np.linalg.norm(motion.reference-reference), 1e-5)
        self.assertLessEqual(np.max(np.abs(motion.reference-reference)), .02000001)

    def test_loaded_insertion_uses_declared_lead_and_reference_gain(self):
        for lead in (None, .0025):
            frame = copy.deepcopy(self.frame)
            body = frame['bodies']['lower_collar']
            goal = np.array(body['pos']) + [0, 0, .025]
            phase = dict(kind='insert', body='lower_collar', feedback_gain=2,
                         target=dict(pos=goal.tolist(), quat=[0, 0, 0, 1]))
            if lead is not None:
                phase['translation_lead'] = lead
            controller = self.controller(phase)
            controller.grasps['left'] = dict(body='lower_collar', verified=False,
                tcp_in_body=[0, 0, 0], tcp_rotation_in_body=[0, 0, 0, 1])
            captured = []
            def capture(joints, position, *args, **kwargs):
                captured.append((np.asarray(position), kwargs['feedback_gain']))
                return np.asarray(joints), 0., 0.
            controller.motion['left'].target = capture
            controller.step(self.ready, frame)
            expected = .0005 if lead is None else lead
            np.testing.assert_allclose(captured[0][0]-body['pos'], [0, 0, expected], atol=1e-12)
            self.assertEqual(captured[0][1], 2)

    def test_inactive_support_integrates_measured_tracking_error(self):
        # A loaded support can lag even when its stored reference is at target.
        # Exercise the controller routing and real Motion integration twice.
        c=self.controller(dict(kind='hold',seconds=1))
        joints=self.ready.copy()
        tcp,quat=c.pose(joints[7:],'right')
        parent='lower_collar';frame=copy.deepcopy(self.frame)
        frame['bodies'][parent]['pos']=tcp.tolist()
        frame['bodies'][parent]['quat']=[0,0,0,1]
        c.holds['right']=dict(relative_to=parent,pos=[.002,0,0],quat=quat,
                              opening=1.,speed=.02,feedback_gain=2.)
        def measured(q,base):
            offset=np.array([0.,.3,0.]) if np.allclose(base,c.motion['left'].base) else np.zeros(3)
            return tcp.copy()+offset,np.eye(3)
        def solve(pos,quat,**kwargs):return kwargs['q_init'].copy(),0.,0.
        # Preserve the real Motion law while isolating IK from the routing test.
        motion=c.motion['right']
        with patch.object(c,'check_grasp_slip'), patch.object(motion.ik,'tcp_pose',side_effect=measured), \
             patch.object(motion.ik,'matrix_to_quat_xyzw',return_value=quat), \
             patch.object(motion.ik,'solve',side_effect=solve) as solver:
            frame['time']=0.;c.step(joints,frame)
            first=np.asarray(next(x.args[0] for x in solver.call_args_list if np.allclose(x.kwargs['base_pos'],motion.base))).copy()
            solver.reset_mock()
            frame['time']=.05;c.step(joints,frame)
            second=np.asarray(next(x.args[0] for x in solver.call_args_list if np.allclose(x.kwargs['base_pos'],motion.base))).copy()
        np.testing.assert_allclose(first-tcp,[.0002,0,0],atol=1e-10)
        np.testing.assert_allclose(second-tcp,[.0002,0,0],atol=1e-10)

    def test_relative_hold_follows_measured_parent(self):
        c=self.controller(dict(kind='hold',seconds=1));name=next(iter(self.frame['bodies']))
        frame=copy.deepcopy(self.frame);target={'pos':[.01,.02,.03],'quat':[0,0,0,1],'relative_to':name}
        first,_=c.world_target(target,frame);frame['bodies'][name]['pos'][0]+=.025
        second,_=c.world_target(target,frame);np.testing.assert_allclose(second-first,[.025,0,0],atol=1e-12)

    def test_release_supports_measured_partial_opening(self):
        c=self.controller(dict(kind='release',opening=.4));joints=self.ready.copy();joints[6]=.4
        frame=copy.deepcopy(self.frame)
        for t in (0.,.5,.7):frame['time']=t;c.step(joints,frame)
        self.assertEqual(c.index,1)

    def test_invalid_release_target_fails_closed(self):
        c=self.controller(dict(kind='release',opening=0.))
        with self.assertRaisesRegex(ControlFailure,'Invalid release'):c.step(self.ready,self.frame)

    def test_thread_free_spin_aborts_without_pitch_advance(self):
        plan=json.loads((self.folder/'controller.json').read_text());phase=next((p for p in plan['phases'] if p['kind']=='thread'),None)
        if phase is None:return
        c=Controller({'phases':[phase]},self.spec);frame=copy.deepcopy(self.frame)
        side=phase['side'];index=0 if side=='left' else 7
        reference=frame['bodies'][phase['reference']];body=frame['bodies'][phase['body']]
        body['pos']=(np.array(reference['pos'])+[phase['xy'][0],phase['xy'][1],.0232]).tolist()
        tcp=np.array(body['pos'])+[0,0,.009];q=self.down
        c.grasps[side]={'body':phase['body'],'verified':False}
        for i in range(30):
            body['quat']=axis_quat([0,0,1],-.2*i).tolist()
            if i<12:c.thread_target(phase,body,tcp,q,self.ready[index:index+7],frame,i*.05)
            else:
                with self.assertRaisesRegex(ControlFailure,'axial advancement'):
                    c.thread_target(phase,body,tcp,q,self.ready[index:index+7],frame,i*.05)
                break


    def test_insert_measured_feedback_uses_current_tcp_and_body_orientation(self):
        frame = copy.deepcopy(self.frame)
        body = frame['bodies']['lower_collar']
        body['quat'] = axis_quat([0, 1, 0], .1).tolist()
        goal = np.array(body['pos']) + [0, 0, .025]
        phase = dict(kind='insert', body='lower_collar', feedback_gain=2,
                     measured_translation=True, position_gain=4, translation_lead=.0025,
                     measured_rotation=True, rotation_gain=.3, rotation_lead=.02,
                     rotation_about_body=True,
                     target=dict(pos=goal.tolist(), quat=[0, 0, 0, 1]))
        controller = self.controller(phase)
        controller.grasps['left'] = dict(body='lower_collar', verified=False,
            tcp_in_body=[0, 0, 0], tcp_rotation_in_body=[0, 0, 0, 1])
        tcp, tcpq = controller.pose(self.ready[:7], 'left')
        turn = axis_quat([0, 1, 0], -.02)
        captured = []
        def capture(joints, position, orientation, *args, **kwargs):
            captured.append((np.asarray(position), orientation))
            return np.asarray(joints), 0., 0.
        controller.motion['left'].target = capture
        controller.step(self.ready, frame)
        lever = tcp - body['pos']
        expected = tcp + [0, 0, .0025] + rotate(turn, lever) - lever
        np.testing.assert_allclose(captured[0][0], expected, atol=1e-12)
        self.assertLess(qangle(captured[0][1], multiply(turn, tcpq)), 1e-7)


    def stationary_insertion(self, **settings):
        frame = copy.deepcopy(self.frame)
        body = frame['bodies']['lower_collar']
        target = (np.asarray(body['pos']) + [0, 0, .025]).tolist()
        c = self.controller(dict(kind='insert', body='lower_collar', timeout=25,
                                 target=dict(pos=target, quat=[0, 0, 0, 1]), **settings))
        c.grasps['left'] = dict(body='lower_collar', verified=False,
            tcp_in_body=[0, 0, 0], tcp_rotation_in_body=[0, 0, 0, 1])
        c.motion['left'].target = lambda joints, *args, **kwargs: (np.asarray(joints), 0., 0.)
        return c, frame

    def test_default_insertion_stall_still_aborts_at_two_seconds(self):
        c, f = self.stationary_insertion()
        c.step(self.ready, f); f['time'] = 2.1
        with self.assertRaisesRegex(ControlFailure, 'Insertion stalled'):c.step(self.ready, f)

    def test_recovery_window_is_bounded_and_keeps_absolute_phase_timeout(self):
        c, f = self.stationary_insertion(progress_window_seconds=5.)
        c.step(self.ready, f); f['time'] = 2.1; c.step(self.ready, f)
        f['time'] = 5.1
        with self.assertRaisesRegex(ControlFailure, 'Insertion stalled'):c.step(self.ready, f)
        c, f = self.stationary_insertion(progress_window_seconds=5.)
        c.step(self.ready, f); f['time'] = 25.1
        with self.assertRaisesRegex(ControlFailure, 'Phase timeout'):c.step(self.ready, f)

    def test_unbounded_or_invalid_progress_windows_are_rejected(self):
        for value in [float('inf'), float('nan'), 0, -1, 26, True]:
            c, f = self.stationary_insertion(progress_window_seconds=value)
            with self.assertRaisesRegex(ControlFailure, 'Invalid insertion progress window'):
                c.step(self.ready, f)


if __name__=='__main__':unittest.main()
