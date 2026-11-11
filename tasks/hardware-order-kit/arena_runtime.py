"""Original adapter extension for compound USD bodies and passive mechanisms.

Adapter contract: yam-arena 0059d02a1a91bc6834c1d0846022891df0c78730.
Native integration evidence is recorded in validation.json.
Uses the Arena reset event for articulated fixtures and reads telemetry during robot steps.
"""
from dataclasses import dataclass
import importlib.abc
import importlib.machinery
import json
import os
from pathlib import Path
import sys

from yam_arena.task_file import Box
from .geometry import maximum_penetration, robot_clearance, box


def array(value):
    value = getattr(value, 'torch', value)
    return value.detach().cpu().numpy()


LATEST = None


def collision_link(stage,root_name,link_name):
    from pxr import UsdPhysics
    matches=[p for p in stage.Traverse() if p.GetName()==link_name
             and root_name in str(p.GetPath()).split('/') and p.HasAPI(UsdPhysics.RigidBodyAPI)]
    if len(matches)!=1:raise RuntimeError(f'Cannot identify unique {root_name} collision link {link_name}')
    return matches[0]


def collision_shapes_for_link(link):
    from pxr import Usd, UsdPhysics
    descendants = iter(Usd.PrimRange(link))
    for prim in descendants:
        if prim != link and prim.HasAPI(UsdPhysics.RigidBodyAPI):
            descendants.PruneChildren()
            continue
        if prim.HasAPI(UsdPhysics.CollisionAPI):
            yield prim


def install(spec, scorer, here):
    @dataclass(frozen=True)
    class Assembly(Box):
        description: object = None

        def _check(self):
            super()._check()
            if not (here/'assets'/f'{self.name}.usda').is_file():
                raise FileNotFoundError('Run build_assets.py before native loading')

    objects = [Assembly(a['name'], tuple(a['origin']), mass=None if a.get('fixed') else 1.0,
                        description=a) for a in spec['assemblies']]
    by_name = {a.name: a for a in objects}
    robot_bounds = {}
    episode = {'number': 0}

    def arena_object(a):
        import isaaclab.sim as sim
        from isaaclab.actuators import ImplicitActuatorCfg
        from isaaclab_arena.assets.object import Object
        from isaaclab_arena.assets.object_type import ObjectType
        from isaaclab_arena.utils.pose import Pose
        data = a.description
        articulated = bool(data.get('joints')) or data.get('fixed', False)

        class NativeObject(Object):
            def _build_reset_event(self):
                event = super()._build_reset_event()
                if event is not None and data.get('joints'):
                    from isaaclab_arena.terms.events import reset_articulation_pose_and_joints
                    event.func = reset_articulation_pose_and_joints
                return event

            def _generate_articulation_cfg(self):
                cfg = super()._generate_articulation_cfg()
                cfg.init_state.joint_pos = {j['name']: 0.0 for j in data.get('joints', [])}
                cfg.init_state.joint_vel = {name: 0.0 for name in cfg.init_state.joint_pos}
                cfg.actuators = {j['name']: ImplicitActuatorCfg(
                    joint_names_expr=[j['name']], stiffness=j.get('stiffness', 0.0),
                    damping=j.get('damping', 0.02)) for j in data.get('joints', [])}
                return cfg

        addon = {
            'collision_props': sim.CollisionPropertiesCfg(contact_offset=0.0003, rest_offset=0.0),
            'rigid_props': sim.RigidBodyPropertiesCfg(
                solver_position_iteration_count=64, solver_velocity_iteration_count=16,
                max_depenetration_velocity=0.5, sleep_threshold=0.005,
                linear_damping=0.1, angular_damping=0.5),
        }
        if articulated:
            addon['articulation_props'] = sim.ArticulationRootPropertiesCfg(
                enabled_self_collisions=True, solver_position_iteration_count=64,
                solver_velocity_iteration_count=16, sleep_threshold=0.005)
        obj = NativeObject(name=a.name, usd_path=str(here/'assets'/f'{a.name}.usda'),
                           object_type=ObjectType.ARTICULATION if articulated else ObjectType.RIGID,
                           spawn_cfg_addon=addon)
        obj.set_initial_pose(Pose(position_xyz=tuple(a.pos), rotation_xyzw=(0, 0, 0, 1)))
        return obj

    def collect(emb):
        env = emb._env.unwrapped
        origin = array(env.scene.env_origins)[0]
        bodies, joints = {}, {}
        for a in spec['assemblies']:
            asset = env.scene[a['name']]
            articulated = bool(a.get('joints')) or a.get('fixed', False)
            if articulated:
                poses = array(asset.data.body_link_pose_w)[0]
                velocities = array(asset.data.body_link_vel_w)[0]
                index = {n: i for i, n in enumerate(asset.body_names)}
                for b in a['bodies']:
                    i = index[b['name']]
                    bodies[b['name']] = {'pos': (poses[i, :3]-origin).tolist(), 'quat': poses[i, 3:7].tolist(),
                                         'linear': velocities[i, :3].tolist(), 'angular': velocities[i, 3:].tolist()}
                if a.get('joints'):
                    q = array(asset.data.joint_pos)[0]
                    for j in a['joints']:
                        joints[j['name']] = float(q[list(asset.joint_names).index(j['name'])])
            else:
                pose = array(asset.data.root_link_pose_w)[0]
                vel = array(asset.data.root_link_vel_w)[0]
                bodies[a['bodies'][0]['name']] = {'pos': (pose[:3]-origin).tolist(), 'quat': pose[3:].tolist(),
                                                 'linear': vel[:3].tolist(), 'angular': vel[3:].tolist()}
        robot_boxes = []
        for side in ('left', 'right'):
            robot = env.scene[f'{side}_robot']
            poses = array(robot.data.body_link_pose_w)[0]
            for i, name in enumerate(robot.body_names):
                centre_local, half = robot_bounds[(side, name)]
                state = {'pos': (poses[i, :3]-origin).tolist(), 'quat': poses[i, 3:].tolist()}
                robot_boxes.append(box(state, {'kind': 'box', 'pos': centre_local,
                                              'size': [2*v for v in half], 'quat': [0,0,0,1]}))
        clearance = robot_clearance(robot_boxes, spec, bodies)
        return {'schema': 1, 'time': float(emb._t), 'bodies': bodies, 'joints': joints,
                'robot_clearance': clearance, 'max_penetration': maximum_penetration(spec, bodies)}

    def cache_robot_bounds(emb):
        from isaaclab.sim.utils.stage import get_current_stage
        from pxr import UsdGeom
        stage = get_current_stage()
        cache = UsdGeom.BBoxCache(
            0, [UsdGeom.Tokens.default_, UsdGeom.Tokens.render, UsdGeom.Tokens.proxy,
                UsdGeom.Tokens.guide], False, True,
        )
        robot_bounds.clear()
        details = []
        for side in ('left', 'right'):
            asset = emb._env.unwrapped.scene[f'{side}_robot']
            for name in asset.body_names:
                # Arena scene keys are left_robot/right_robot, but the pinned
                # adapter spawns USD roots LeftArm/RightArm. Read the actual cfg.
                root_name=asset.cfg.prim_path.rstrip('/').rsplit('/',1)[-1]
                prim=collision_link(stage,root_name,name)
                points = []
                shapes = list(collision_shapes_for_link(prim))
                for child in shapes:
                    bound = cache.ComputeRelativeBound(child, prim).ComputeAlignedRange()
                    if bound.IsEmpty():
                        continue
                    points.extend(bound.GetCorner(corner) for corner in range(8))
                if not points:
                    raise RuntimeError(f'Collision geometry missing for {side}/{name}')
                lo = [min(p[i] for p in points) for i in range(3)]
                hi = [max(p[i] for p in points) for i in range(3)]
                centre = [(x+y)/2 for x, y in zip(lo, hi)]
                robot_bounds[(side, name)] = (centre, [(y-x)/2 for x,y in zip(lo,hi)])
                details.append({'side': side, 'link': name, 'prim': str(prim.GetPath()),
                                'owned_collider_count': len(shapes),
                                'local_center': centre, 'local_half_extent': robot_bounds[(side, name)][1]})
        trace = os.environ.get('ROBOCURVE_TRACE')
        if trace:
            target = Path(trace).parent / f'robot-collision-bounds-e{episode["number"]}.json'
            temporary = target.with_suffix('.tmp')
            temporary.write_text(json.dumps({'kind': 'NATIVE_OWNED_ROBOT_COLLISION_BOUNDS',
                                             'links': details}, indent=2, allow_nan=False) + '\n')
            temporary.replace(target)

    def patch_scene(module):
        original = module.task_object
        def task_object(obj):
            return arena_object(obj) if isinstance(obj, Assembly) else original(obj)
        module.task_object = task_object

        original_builder = module.build_task_environment
        def build_task_environment(embodiment, task, control_hz=None):
            environment = original_builder(embodiment, task, control_hz)
            if getattr(task.module, 'SPEC', None) is spec:
                previous_callback = environment.env_cfg_callback
                def configure(config):
                    config = previous_callback(config)
                    control_dt = config.sim.dt * config.decimation
                    config.sim.dt = 1.0 / 480
                    config.decimation = round(control_dt / config.sim.dt)
                    config.sim.render_interval = config.decimation
                    return config
                environment.env_cfg_callback = configure
            return environment
        module.build_task_environment = build_task_environment

    def patch_embodiment(module):
        cls = module.YamArenaEmbodiment
        original_reset, original_step = cls.reset, cls._task_step
        def ours(self):
            return self.task is not None and getattr(self.task.module, 'SPEC', None) is spec
        def reset(self, *args, **kwargs):
            obs = original_reset(self, *args, **kwargs)
            if ours(self):
                scorer.reset()
                episode['number'] += 1
                cache_robot_bounds(self)
                record(collect(self))
            return obs
        def record(frame):
            global LATEST
            LATEST = frame
            result = scorer.update(frame)
            destination = os.environ.get('ROBOCURVE_TRACE')
            if destination:
                from dataclasses import asdict
                with Path(destination).open('a', encoding='utf-8') as stream:
                    stream.write(json.dumps({'kind': 'NATIVE_SIMULATION_FRAME', 'episode': episode['number'],
                                             'frame': frame, 'result': asdict(result)}, allow_nan=False)+'\n')
        def task_step(self, *args, **kwargs):
            if not ours(self):
                return original_step(self, *args, **kwargs)
            # The adapter's default geometry helper accepts rigid objects only.
            # This scorer uses per-link articulation state collected after the real action.
            record(collect(self))
            result = scorer.result
            return module.StepResult(
                observation=self._observation(),
                terminated=result.success,
                termination_reason='success' if result.success else None,
                info={'success': result.success, 'score': result.score},
            )
        cls.reset, cls._task_step = reset, task_step

    patches = {'yam_arena.scene': patch_scene, 'yam_arena.inspect_embodiment': patch_embodiment}
    class Hook(importlib.abc.MetaPathFinder):
        def find_spec(self, fullname, path, target=None):
            if fullname not in patches:
                return None
            result = importlib.machinery.PathFinder.find_spec(fullname, path)
            if result is None or result.loader is None:
                return None
            loader = result.loader
            class Loader(importlib.abc.Loader):
                def create_module(self, spec):
                    return loader.create_module(spec) if hasattr(loader, 'create_module') else None
                def exec_module(self, module):
                    loader.exec_module(module)
                    patches[fullname](module)
            result.loader = Loader()
            return result
    sys.meta_path.insert(0, Hook())
    for name, patch in patches.items():
        if name in sys.modules:
            patch(sys.modules[name])
    return objects
