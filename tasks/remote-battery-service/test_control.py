"""Offline controller contract tests. No native physics is simulated here."""
import copy
import json
import math
from pathlib import Path
import sys
import unittest
from unittest.mock import Mock
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
    def test_rolled_fresh_cell_keeps_vertical_grasp_approach(self):
        plan = json.loads((self.folder/'controller.json').read_text())
        phase = next(p for p in plan['phases'] if p.get('body') == 'new_cell_0' and p['kind'] == 'grasp')
        self.assertEqual(phase['offset_frame'], 'world')
        frame = copy.deepcopy(self.frame)
        frame['bodies']['new_cell_0']['quat'] = axis_quat([1, 0, 0], .67).tolist()
        frame['bodies']['new_cell_0']['pos'][1] = -.244845
        target = np.asarray(frame['bodies']['new_cell_0']['pos']) + phase['offset']
        joints, position_error, rotation_error = self.ik.solve(
            target + [0, 0, .0025], phase['quat'], base_pos=self.station.BASES['right'],
            iters=500, damping=.015, tol=1e-5)
        self.assertLess(position_error, .0015)
        self.assertLess(rotation_error, .04)
        observed = self.ready.copy()
        observed[7:13] = joints
        controller = Controller({'phases': [phase]}, self.spec)
        controller.step(observed, frame)
        self.assertTrue(controller.grasp_closing)
        self.assertEqual(controller.index, 0)

    def test_cylindrical_carry_ignores_roll_and_rejects_axis_tilt(self):
        plan = json.loads((self.folder/'controller.json').read_text())
        phase = next(p for p in plan['phases'] if p.get('body') == 'new_cell_0' and p.get('verify_lift'))
        phase = dict(phase, hold=0)
        for axis, expected_index in (([1, 0, 0], 1), ([0, 1, 0], 0)):
            with self.subTest(axis=axis):
                frame = copy.deepcopy(self.frame)
                frame['bodies']['new_cell_0']['pos'] = phase['target']['pos']
                frame['bodies']['new_cell_0']['quat'] = axis_quat(axis, .4).tolist()
                controller = Controller({'phases': [phase]}, self.spec)
                controller.grasps['right'] = {
                    'body': 'new_cell_0', 'verified': False,
                    'tcp_in_body': [0, 0, .01],
                    'tcp_rotation_in_body': phase['target']['quat'],
                    'start_z': phase['target']['pos'][2] - .05,
                }
                controller.step(self.ready, frame)
                self.assertEqual(controller.index, expected_index)

    def test_fresh_cell_translation_preserves_captured_wrist_orientation(self):
        plan = json.loads((self.folder/'controller.json').read_text())
        phase = next(p for p in plan['phases'] if p.get('body') == 'new_cell_0' and p.get('verify_lift'))
        frame = copy.deepcopy(self.frame)
        frame['bodies']['new_cell_0']['pos'] = (np.asarray(phase['target']['pos']) - [0, 0, .02]).tolist()
        frame['bodies']['new_cell_0']['quat'] = axis_quat([1, 0, 0], .7).tolist()
        controller = Controller({'phases': [phase]}, self.spec)
        controller.grasps['right'] = {
            'body': 'new_cell_0', 'verified': False,
            'tcp_in_body': [0, .006, .008],
            'tcp_rotation_in_body': [0, 0, 0, 1],
            'tcp_orientation_at_grasp': self.down.copy(),
            'start_z': .75475,
        }
        motion = controller.motion['right']
        motion.target = Mock(return_value=(self.ready[7:].copy(), 0., 0.))
        measured_tcp, _ = controller.pose(self.ready[7:], 'right')
        controller.step(self.ready, frame)
        target, orientation = motion.target.call_args.args[1:3]
        np.testing.assert_allclose(target, measured_tcp + [0, 0, .003], atol=1e-12)
        self.assertLess(qangle(orientation, self.down), 1e-6)
        self.assertEqual(controller.index, 0)

    def test_spring_feedback_gain_is_bounded_by_declared_increment(self):
        for gain, current, expected in [(1, 0., -.00115), (8, 0., -.003), (8, -.00105, -.0008)]:
            with self.subTest(gain=gain, current=current):
                phase = {'kind': 'joint', 'label': 'Spring feedback', 'side': 'right',
                         'body': 'new_cell_0', 'joint': 'spring_0', 'value': -.00115,
                         'position_gain': gain, 'increment': .003, 'tolerance': .00025}
                controller = Controller({'phases': [phase]}, self.spec)
                frame = copy.deepcopy(self.frame)
                frame['joints']['spring_0'] = current
                controller.motion['right'].target = Mock(return_value=(self.ready[7:].copy(), 0., 0.))
                measured, _ = controller.pose(self.ready[7:], 'right')
                controller.step(self.ready, frame)
                target = controller.motion['right'].target.call_args.args[1]
                np.testing.assert_allclose(target - measured, [expected, 0, 0], atol=1e-12)

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

    def test_free_end_lowering_combines_axial_integration_and_lateral_support(self):
        plan = json.loads((self.folder/'controller.json').read_text())
        phases = [phase for phase in plan['phases']
                  if phase['label'].startswith('Lower the free end')]
        self.assertEqual(len(phases), 2)
        for phase in phases:
            self.assertTrue(phase['integrate_axial_error'])
            self.assertEqual(phase['lateral_gain'], 8)
            self.assertEqual(phase['lateral_lead'], .008)
            self.assertEqual(phase['lateral_tolerance'], .0008)

    def test_axial_insertion_preserves_reference_load_bias(self):
        frame = copy.deepcopy(self.frame)
        body = frame['bodies']['new_cell_0']
        goal = np.array(body['pos']) + [0, 0, -.02]
        phase = dict(kind='insert', body='new_cell_0', side='right',
                     insertion_axis_world=[0, 0, 1], integrate_axial_error=True,
                     axial_gain=.1, axial_lead=.0005,
                     target=dict(pos=goal.tolist(), quat=[0, 0, 0, 1]))
        controller = Controller({'phases': [dict(label='axial-bias-test', **phase)]}, self.spec)
        controller.check_grasp_slip = lambda *args: None
        controller.body_tcp = lambda side, position, orientation: (position, orientation)
        controller.motion['right'].reference = self.ready[7:13].copy()
        original_pose = controller.pose
        measured, orientation = original_pose(self.ready[7:], 'right')
        reference = controller.motion['right'].reference
        controller.pose = lambda joints, side: (measured + [0, 0, -.003], orientation) if joints is reference else original_pose(joints, side)
        motion = controller.motion['right']
        motion.target = Mock(return_value=(self.ready[7:].copy(), 0., 0.))
        controller.step(self.ready, frame)
        target = motion.target.call_args.args[1]
        np.testing.assert_allclose(target - measured, [0, 0, -.0035], atol=1e-12)

    def test_vertical_entry_aligns_laterally_before_descending(self):
        frame = copy.deepcopy(self.frame)
        body = frame['bodies']['new_cell_0']
        goal = np.array(body['pos']) + [.005, 0, -.02]
        phase = dict(kind='insert', body='new_cell_0',
                     insertion_axis_world=[0, 0, 1], lateral_gain=8,
                     lateral_lead=.008, lateral_tolerance=.0008,
                     target=dict(pos=goal.tolist(), quat=axis_quat([0, 1, 0], -.3).tolist()))
        controller = self.controller(phase)
        controller.grasps['left'] = dict(body='new_cell_0', verified=False,
            tcp_in_body=[0, 0, 0], tcp_rotation_in_body=[0, 0, 0, 1])
        targets = []
        def capture(joints, position, orientation, opening, **kwargs):
            targets.append(np.array(position))
            return np.array(joints), 0., 0.
        controller.motion['left'].target = capture
        tcp, _ = controller.pose(self.ready[:7], 'left')
        controller.step(self.ready, frame)
        np.testing.assert_allclose(targets[0] - tcp, [.008, 0, 0], atol=1e-12)

    def test_spring_press_holds_transverse_position_and_captured_wrist(self):
        rotation = axis_quat([0, 1, 0], -.3)
        phase = dict(kind='joint', body='new_cell_0', joint='spring_0', value=-.00115,
                     position_gain=8, increment=.003, hold_transverse=True,
                     preserve_grasp_orientation=True, wrist_rotation=rotation.tolist())
        controller = self.controller(phase)
        controller.grasps['left'] = dict(body='new_cell_0', verified=False,
            tcp_in_body=[0, 0, 0], tcp_rotation_in_body=[0, 0, 0, 1],
            tcp_orientation_at_grasp=self.down.tolist())
        targets = []
        def capture(joints, position, orientation, opening, **kwargs):
            targets.append((np.array(position), np.array(orientation)))
            return np.array(joints), 0., 0.
        controller.motion['left'].target = capture
        start, _ = controller.pose(self.ready[:7], 'left')
        frame = copy.deepcopy(self.frame)
        controller.step(self.ready, frame)
        moved = self.ready.copy()
        moved[0] += .01
        frame['time'] = .05
        controller.step(moved, frame)
        np.testing.assert_allclose(targets[-1][0][1:], start[1:], atol=1e-12)
        self.assertLess(qangle(targets[-1][1], multiply(rotation, self.down)), 1e-6)

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
