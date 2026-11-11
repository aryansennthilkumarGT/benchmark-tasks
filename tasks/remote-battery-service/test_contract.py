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

    def test_contact_driven_joint_path_moves_its_child_and_held_cell(self):
        from audit_geometry import frames
        spec = json.loads((HERE/'scene.json').read_text())
        plan = {'phases': [
            {'kind': 'grasp', 'side': 'right', 'body': 'new_cell_0', 'label': 'Hold cell'},
            {'kind': 'joint', 'side': 'right', 'body': 'new_cell_0',
             'joint': 'spring_0', 'value': -.00115, 'label': 'Press spring'},
        ]}
        samples = list(frames(spec, plan))
        initial, final = samples[0][1], samples[-1][1]
        for name in ['new_cell_0', 'contact_0']:
            np.testing.assert_allclose(np.asarray(final[name]['pos']) - initial[name]['pos'],
                                       [-.00115, 0, 0], atol=1e-12)

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
        self.assertEqual(len(expert.controller.phases),len(json.loads((HERE/'controller.json').read_text())['phases']))
        # No environment, simulator, real sensor, or model is created here.
        with self.assertRaisesRegex(expert_module.ControlFailure,'Native frame unavailable'):
            expert.act(SimpleNamespace(state_time=0))
        # Finishing waypoints is not a full-score demonstration. Waiting is
        # bounded and only the actual scorer can approve terminal success.
        expert.controller.done=True
        expert.evaluator=SimpleNamespace(result=SimpleNamespace(failure=None,success=False,score=.95))
        self.assertFalse(expert.terminal_stop(0))
        self.assertFalse(expert.terminal_stop(1))
        with self.assertRaisesRegex(expert_module.ControlFailure,'without a stable full-score'):
            expert.terminal_stop(10)
        expert.evaluator.result.success=True
        self.assertTrue(expert.terminal_stop(10))
        expert.evaluator.result.failure='lost part'
        with self.assertRaisesRegex(expert_module.ControlFailure,'Terminal state invalid'):
            expert.terminal_stop(10)
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
