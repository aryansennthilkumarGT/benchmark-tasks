"""Package and native-probe contracts. These tests never execute PhysX."""
import json
from pathlib import Path
import unittest
import numpy as np
from feedback import Controller,ControlFailure
from audit_geometry import geometry_module

HERE=Path(__file__).resolve().parent
_geometry=geometry_module(HERE)
maximum_penetration,polyhedron,convex_separation=(_geometry.maximum_penetration,_geometry.polyhedron,_geometry.convex_separation)

class PackageContractTests(unittest.TestCase):
    def test_raised_storage_grip_clears_cooler_blocking_lip(self):
        specification = json.loads((HERE/'scene.json').read_text())
        bodies = {b['name']: b for a in specification['assemblies'] for b in a['bodies']}
        blocker = bodies['new_cooler']['shapes'][2]
        blocker_min = blocker['pos'][0]-blocker['size'][0]/2
        for name in ('old_storage', 'new_storage'):
            for index in (1, 3):
                shape = bodies[name]['shapes'][index]
                handle_max = shape['pos'][0]+shape['size'][0]/2
                self.assertGreaterEqual(blocker_min-handle_max, .0029)
            self.assertEqual(bodies[name]['shapes'][4]['size'], [.014, .028, .02])

    def test_robot_usd_path_is_distinct_from_scene_key(self):
        import importlib
        from pxr import Usd,UsdGeom,UsdPhysics
        from yam_arena import task_file
        task=task_file.load(HERE/'task.py')
        runtime=importlib.import_module(task.module._name+'.arena_runtime')
        stage=Usd.Stage.CreateInMemory()
        for root in ('LeftArm','RightArm'):
            body=UsdGeom.Xform.Define(stage,'/World/envs/env_0/'+root+'/base_link')
            UsdPhysics.RigidBodyAPI.Apply(body.GetPrim())
        self.assertEqual(str(runtime.collision_link(stage,'LeftArm','base_link').GetPath()),'/World/envs/env_0/LeftArm/base_link')
        with self.assertRaises(RuntimeError):runtime.collision_link(stage,'left_robot','base_link')
    def test_robot_collision_bounds_exclude_nested_rigid_links(self):
        import importlib
        from pxr import Usd, UsdGeom, UsdPhysics
        from yam_arena import task_file
        task = task_file.load(HERE/'task.py')
        runtime = importlib.import_module(task.module._name+'.arena_runtime')
        stage = Usd.Stage.CreateInMemory()
        parent = UsdGeom.Xform.Define(stage, '/Robot/base').GetPrim()
        UsdPhysics.RigidBodyAPI.Apply(parent)
        own = UsdGeom.Cube.Define(stage, '/Robot/base/collision').GetPrim()
        UsdPhysics.CollisionAPI.Apply(own)
        child = UsdGeom.Xform.Define(stage, '/Robot/base/link').GetPrim()
        UsdPhysics.RigidBodyAPI.Apply(child)
        descendant = UsdGeom.Cube.Define(stage, '/Robot/base/link/collision').GetPrim()
        UsdPhysics.CollisionAPI.Apply(descendant)
        self.assertEqual(list(runtime.collision_shapes_for_link(parent)), [own])
        self.assertEqual(list(runtime.collision_shapes_for_link(child)), [descendant])

    def test_official_task_loader_and_expert_contract(self):
        import importlib
        from types import SimpleNamespace
        from yam_arena import task_file
        task=task_file.load(HERE/'task.py')
        self.assertEqual(task.scene,'station')
        self.assertEqual(len(task.objects),len(task.module.SPEC['assemblies']))
        self.assertEqual(task.score_over,'end')
        self.assertFalse(task.success({}));self.assertEqual(task.score({}),0)
        task_file.register('offline-contract-only',task)
        expert_module=importlib.import_module(task.module._name+'.expert')
        expert=expert_module.policy()
        expert.bind(SimpleNamespace(environment_id='offline-contract-only'))
        expert.reset(None)
        self.assertEqual(expert.info.action_space.shape,(14,))
        program=json.loads((HERE/'expert_joint_trajectory.json').read_text())
        self.assertEqual(expert.actions.shape,(len(program['actions']),14))
        self.assertFalse(hasattr(expert,'runtime'));self.assertFalse(hasattr(expert,'evaluator'))
        class OnlyRobotProprio:
            def __getitem__(self,key):
                if key!='joint_pos':raise AssertionError('Expert requested hidden task state: '+str(key))
                return np.tile([0,1,1,-.6,0,0,1.],2)
        observation=SimpleNamespace(state=OnlyRobotProprio(),state_time=0.)
        chunk=expert.act(observation)
        np.testing.assert_array_equal(chunk.actions[0].data,program['actions'][0])
        self.assertFalse(chunk.actions[0].meta['request_stop'])
        expert.index=len(expert.actions)+expert.hold-1
        observation.state_time=expert.index/20
        self.assertTrue(expert.act(observation).actions[0].meta['request_stop'])
        # Ending a fixed program is not task success. No physics is executed;
        # only an actual future scorer/record can establish full feasibility.
        self.assertFalse(task.success({}));self.assertEqual(task.score({}),0)
    def test_control_probe_labels_match_current_phases(self):
        phases=json.loads((HERE/'controller.json').read_text())['phases']
        for case in json.loads((HERE/'native-cases.json').read_text())['control']:
            self.assertEqual(phases[case['through_phase']]['label'],case['through_label'])
            self.assertTrue(case['assertions']);self.assertLessEqual(case['max_steps'],json.loads((HERE/'scene.json').read_text())['run_limit'])
    def test_native_case_names_unique(self):
        for mode,cases in json.loads((HERE/'native-cases.json').read_text()).items():
            if mode not in ('physics','control'):continue
            self.assertEqual(len(cases),len({c['name'] for c in cases}));self.assertGreaterEqual(len(cases),2)
    def test_noncolliding_articulation_dummy_does_not_crash_contact_measurement(self):
        body=dict(name='dummy',pos=[0,0,0],quat=[0,0,0,1],shapes=[dict(kind='box',pos=[0,0,0],quat=[0,0,0,1],size=[.001]*3,collision=False)])
        spec={'assemblies':[{'bodies':[body],'joints':[]}],'collision_exclusions':[]}
        self.assertEqual(maximum_penetration(spec,{'dummy':body}),0.)
    def test_sat_touching_overlap_and_separation(self):
        shape=dict(kind='box',pos=[0,0,0],size=[.02]*3,quat=[0,0,0,1])
        a=polyhedron(dict(pos=[0,0,0],quat=[0,0,0,1]),shape)
        for x,expected in ((.015,-.005),(.020,0),(.030,.010)):
            b=polyhedron(dict(pos=[x,0,0],quat=[0,0,0,1]),shape)
            self.assertAlmostEqual(convex_separation(a,b,stop_at=float('inf')),expected)
            self.assertEqual(convex_separation(a,b,stop_at=-.002)<-.002,expected<-.002)
    def test_support_lost_even_before_lift_is_rejected(self):
        c=object.__new__(Controller);c.grasps={'left':{'body':'held','verified':False,'min_width':.02}}
        with self.assertRaisesRegex(ControlFailure,'Supporting grasp closed empty'):
            c.check_grasp_slip('left',np.zeros(7),{'bodies':{}},require_support=True)

if __name__=='__main__':unittest.main()
