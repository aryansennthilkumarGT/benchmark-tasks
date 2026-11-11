"""Offline controller contract tests. No native physics is simulated here."""
import copy
import json
import math
from pathlib import Path
import sys
import unittest
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

    def test_thread_entry_integrates_measured_body_position_error(self):
        frame = copy.deepcopy(self.frame)
        body = frame['bodies']['nut_0']
        goal = np.array(body['pos']) + [.004, 0, -.02]
        phase = dict(kind='insert', body='nut_0', integrate_body_error=True,
                     position_gain=.1, translation_lead=.0005,
                     target=dict(pos=goal.tolist(), quat=[0, 0, 0, 1]))
        controller = self.controller(phase)
        controller.check_grasp_slip = lambda *args: None
        controller.body_tcp = lambda side, position, orientation: (position, orientation)
        controller.motion['left'].reference = self.ready[:6].copy()
        reference_tcp, _ = controller.pose(controller.motion['left'].reference, 'left')
        targets = []
        def capture(joints, position, quat, opening, **kwargs):
            targets.append(np.array(position))
            return np.array(joints), 0., 0.
        controller.motion['left'].target = capture
        controller.step(self.ready, frame)
        expected = reference_tcp + limit_vector(.1 * (goal-body['pos']), .0005)
        np.testing.assert_allclose(targets[0], expected, atol=1e-12)

    def test_prismatic_error_integration_uses_bounded_motion_reference(self):
        frame = copy.deepcopy(self.frame)
        phase = dict(kind='joint', body='pressure_plate', joint='plate_preload',
                     value=-.012, increment=.0005, integrate_joint_error=True,
                     body_quat=[0, 0, 0, 1])
        controller = self.controller(phase)
        _, orientation = controller.pose(self.ready[:7], 'left')
        controller.grasps['left'] = dict(body='pressure_plate', verified=False,
            tcp_in_body=[0, 0, 0], tcp_rotation_in_body=orientation)
        reference = self.ready[:6].copy()
        reference[1] += .01
        controller.motion['left'].reference = reference
        reference_p, _ = controller.pose(np.r_[reference, self.ready[6]], 'left')
        targets = []
        def capture(joints, position, quat, opening, **kwargs):
            targets.append((np.array(position), np.array(quat)))
            return np.array(joints), 0., 0.
        controller.motion['left'].target = capture
        controller.step(self.ready, frame)
        np.testing.assert_allclose(targets[0][0], reference_p + [0, 0, -.0005], atol=1e-12)
        self.assertLess(qangle(targets[0][1], orientation), 1e-8)

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

    def test_loaded_thread_arm_uses_configured_tracking_window(self):
        controller = self.controller(dict(kind='hold', seconds=1))
        self.assertEqual(controller.motion['right'].tracking_error_limit, .08)

    def test_thread_unwind_recentres_before_closing(self):
        plan = json.loads((self.folder/'controller.json').read_text())
        phase = next(value for value in plan['phases'] if value['kind'] == 'thread')
        controller = Controller({'phases': [phase]}, self.spec)
        frame = copy.deepcopy(self.frame)
        body = frame['bodies'][phase['body']]
        reference = frame['bodies'][phase['reference']]
        body['pos'] = (np.array(reference['pos']) + [*phase['xy'], .0232]).tolist()
        body['quat'] = [0, 0, 0, 1]
        centred = np.array(body['pos']) + [0, 0, .009]
        index = 0 if phase['side'] == 'left' else 7
        controller.grasps[phase['side']] = dict(body=phase['body'], verified=False)
        controller.thread_target(phase, body, centred, self.down,
                                 self.ready[index:index+7], frame, 0.)
        controller.thread.update(mode='unwind', switch=0., opening=.5)
        position, _, _ = controller.thread_target(phase, body, centred+[.008, 0, 0],
            self.down, self.ready[index:index+7], frame, .1)
        np.testing.assert_allclose(position, centred)
        self.assertEqual(controller.thread['mode'], 'unwind')
        controller.thread_target(phase, body, centred, self.down,
                                 self.ready[index:index+7], frame, .2)
        self.assertEqual(controller.thread['mode'], 'close')

    def test_thread_without_directed_rotation_aborts_promptly(self):
        plan = json.loads((self.folder/'controller.json').read_text())
        phase = next(phase for phase in plan['phases'] if phase['kind'] == 'thread')
        controller = Controller({'phases': [phase]}, self.spec)
        frame = copy.deepcopy(self.frame)
        body = frame['bodies'][phase['body']]
        reference = frame['bodies'][phase['reference']]
        body['pos'] = (np.array(reference['pos']) + [*phase['xy'], .0232]).tolist()
        body['quat'] = [0, 0, 0, 1]
        tcp = np.array(body['pos']) + [0, 0, .009]
        index = 0 if phase['side'] == 'left' else 7
        controller.grasps[phase['side']] = dict(body=phase['body'], verified=False)
        controller.thread_target(phase, body, tcp, self.down,
                                 self.ready[index:index+7], frame, 0.)
        with self.assertRaisesRegex(ControlFailure, 'Thread rotation stalled'):
            controller.thread_target(phase, body, tcp, self.down,
                                     self.ready[index:index+7], frame, 2.1)

    def test_ninety_degree_plan_defers_early_finger_release(self):
        plan = json.loads((self.folder/'controller.json').read_text())
        phase = next(value for value in plan['phases'] if value['kind'] == 'thread')
        controller = Controller({'phases': [phase]}, self.spec)
        frame = copy.deepcopy(self.frame)
        body = frame['bodies'][phase['body']]
        reference = frame['bodies'][phase['reference']]
        side = phase['side']
        index = 0 if side == 'left' else 7
        controller.grasps[side] = dict(body=phase['body'], verified=False)
        for step in range(9):
            angle = step * .2
            body['pos'] = (np.array(reference['pos']) +
                           [*phase['xy'], .0232-phase['pitch']*angle/(2*math.pi)]).tolist()
            body['quat'] = axis_quat([0, 0, 1], -angle).tolist()
            tcp = np.array(body['pos']) + [0, 0, .009]
            controller.thread_target(phase, body, tcp, self.down,
                                     self.ready[index:index+7], frame, step*.05)
            if step == 4:
                self.assertEqual(controller.thread['mode'], 'turn')
        self.assertEqual(controller.thread['mode'], 'open')

    def test_thread_turn_advances_retained_orientation_reference(self):
        plan = json.loads((self.folder/'controller.json').read_text())
        phase = next(value for value in plan['phases'] if value['kind'] == 'thread')
        controller = Controller({'phases': [phase]}, self.spec)
        frame = copy.deepcopy(self.frame)
        body = frame['bodies'][phase['body']]
        reference = frame['bodies'][phase['reference']]
        body['pos'] = (np.array(reference['pos']) + [*phase['xy'], .0232]).tolist()
        body['quat'] = [0, 0, 0, 1]
        side = phase['side']
        index = 0 if side == 'left' else 7
        observed = self.ready[index:index+7]
        controller.motion[side].reference = observed[:6].copy()
        controller.motion[side].reference[-1] += .04
        tcp, measured_q = controller.pose(observed, side)
        _, reference_q = controller.pose(np.r_[controller.motion[side].reference, observed[6]], side)
        controller.grasps[side] = dict(body=phase['body'], verified=False)
        position, target_q, _ = controller.thread_target(
            phase, body, tcp, measured_q, observed, frame, 0.)
        expected = multiply(axis_quat(rotate(reference['quat'], [0, 0, 1]), -.018), reference_q)
        self.assertLess(qangle(target_q, expected), 1e-6)
        self.assertLessEqual(np.linalg.norm(position-tcp), .000500001)

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


    def test_thread_pilot_blocks_axial_motion_until_laterally_aligned(self):
        for offset, expected_dz in ((.0005, 0.), (.00002, -.0003)):
            frame = copy.deepcopy(self.frame)
            body = frame['bodies']['nut_0']
            body['pos'] = [.175+offset, -.05, .8425]
            body['quat'] = [0, 0, 0, 1]
            phase = dict(kind='insert', body='nut_0', align_before_insert=True,
                         lateral_tolerance=.000075, alignment_angle=.004,
                         target=dict(pos=[.175, -.05, .7827], quat=[0, 0, 0, 1]))
            controller = self.controller(phase)
            controller.motion['left'].reference = self.ready[:6].copy()
            controller.grasps['left'] = dict(body='nut_0', verified=False,
                tcp_in_body=[0, 0, 0], tcp_rotation_in_body=[0, 0, 0, 1])
            reference, _ = controller.pose(self.ready[:7], 'left')
            captured = []
            def capture(joints, position, *args, **kwargs):
                captured.append(np.asarray(position))
                return np.asarray(joints), 0., 0.
            controller.motion['left'].target = capture
            controller.step(self.ready, frame)
            self.assertAlmostEqual(captured[0][2]-reference[2], expected_dz)
            self.assertLess(captured[0][0]-reference[0], 0.)


if __name__=='__main__':unittest.main()
