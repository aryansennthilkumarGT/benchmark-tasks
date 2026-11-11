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


if __name__=='__main__':unittest.main()
