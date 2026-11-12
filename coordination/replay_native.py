"""Diagnose a controller suffix from a recorded native fixture, without demo credit."""
from __future__ import annotations

import argparse
import hashlib
import importlib
import json
from pathlib import Path
import subprocess
import sys

import numpy as np

from engine import atomic


def native_contact_view(include_task_sensors=False):
    from isaaclab.sim.utils.stage import get_current_stage
    from isaaclab_physx.physics import PhysxManager
    from pxr import PhysxSchema, UsdPhysics

    sensor_paths, filter_paths = [], []
    for prim in get_current_stage().Traverse():
        path = str(prim.GetPath())
        if prim.HasAPI(UsdPhysics.RigidBodyAPI):
            filter_paths.append(path)
            if include_task_sensors or 'RightArm' in path or 'LeftArm' in path:
                PhysxSchema.PhysxContactReportAPI.Apply(prim).CreateThresholdAttr().Set(0.)
                sensor_paths.append(path)
        elif prim.HasAPI(UsdPhysics.CollisionAPI):
            ancestor = prim.GetParent()
            while ancestor and not ancestor.IsPseudoRoot() and not ancestor.HasAPI(UsdPhysics.RigidBodyAPI):
                ancestor = ancestor.GetParent()
            if not ancestor or ancestor.IsPseudoRoot():
                filter_paths.append(path)
    view = PhysxManager.get_physics_sim_view().create_rigid_contact_view(
        sensor_paths, filter_patterns=[filter_paths for _ in sensor_paths], max_contact_data_count=8192)
    return view, sensor_paths, filter_paths


def measured_contacts(view, sensor_paths, filter_paths, physics_dt):
    matrix = view.get_contact_force_matrix(dt=physics_dt).numpy()
    if matrix.shape != (len(sensor_paths), len(filter_paths), 3):
        raise ValueError('Native contact force dimensions differ from the configured bodies')
    return [{'sensor': sensor, 'other': path, 'force_N': force.tolist()}
            for sensor, forces in zip(sensor_paths, matrix)
            for path, force in zip(filter_paths, forces) if np.linalg.norm(force) > .01]


def controller_snapshot(controller, observation, frame):
    def array_data(value):
        if isinstance(value, (np.ndarray, np.generic)):
            return value.tolist()
        raise TypeError(f'Unsupported diagnostic state {type(value).__name__}')

    data = dict(phase_index=controller.index, thread_state=controller.thread,
                grasp_transforms=controller.grasps,
                motion_references={side: motion.reference for side, motion in controller.motion.items()},
                joint_pos=np.asarray(observation.state['joint_pos']), frame=frame)
    return json.loads(json.dumps(data, default=array_data, allow_nan=False))


def control_recorded_prefix(folder, source, label):
    sys.path.insert(0, str(folder))
    from feedback import Controller

    directory = source / 'control'
    report = json.loads((directory / 'results.json').read_text())
    if report.get('mode') != 'control' or not report.get('cases'):
        raise ValueError('Source must contain a completed native control case')
    receipt = json.loads((source / 'control-render-diagnostic.json').read_text())
    joints = np.asarray(receipt['resets'][0]['initial_robot_joint_pos'])
    if joints.shape != (14,):
        raise ValueError('Recorded initial robot state is incomplete')
    frame_lines = []
    frames = {}
    episode = None
    for line in (directory / 'physics-probes-not-demonstrations.jsonl').open():
        row = json.loads(line)
        if episode is None:
            episode = row['episode']
        if row['episode'] != episode:
            break
        frame_lines.append(line)
        frame = row['frame']
        frames[round(frame['time'] / .05)] = frame
    action_lines = []
    actions = []
    for line in (directory / 'robot-actions.jsonl').open():
        row = json.loads(line)
        if row['reset_index'] != 0:
            break
        action_lines.append(line)
        actions.append(row)
    plan = json.loads((folder / 'controller.json').read_text())
    specification = json.loads((folder / 'scene.json').read_text())
    selected = next(i for i, phase in enumerate(plan['phases']) if phase['label'] == label)
    controller = Controller(plan, specification)
    compared = 0
    previous = None
    frame = frames[0]
    for row in actions:
        if controller.index == selected:
            break
        if row['control_step'] != compared + 1:
            raise ValueError('Recorded control actions are discontinuous')
        expected = np.asarray(row['submitted_action'])
        actual = controller.step(joints, frame)
        if not np.allclose(actual, expected, rtol=0., atol=1e-9):
            raise ValueError(f'Controller prefix diverged at action {compared}')
        compared += 1
        previous = expected
        joints = np.asarray(row['measured_joint_pos'])
        frame = frames[round(row['time'] / .05)]
    if controller.index != selected or previous is None:
        raise ValueError('Recorded control prefix did not reach the requested phase')
    return controller, specification, frame, joints, previous, {
        'source_kind': 'NATIVE_CONTROL_PROBE_PREFIX_NOT_DEMONSTRATION',
        'compared_actions': compared,
        'absolute_action_tolerance': 1e-9,
        'source_first_reset_actions_sha256': hashlib.sha256(''.join(action_lines).encode()).hexdigest(),
        'source_first_reset_frames_sha256': hashlib.sha256(''.join(frame_lines).encode()).hexdigest(),
        'source_frame_time': frame['time'],
    }


def diagnostic_recorded_prefix(folder, source, label):
    """Reuse an initialized diagnostic prefix; never demonstration evidence."""
    descriptor = json.loads((source/'diagnostic-prefix.json').read_text())
    anchor = Path(descriptor['anchor_source']).resolve()
    if anchor == source.resolve():
        raise ValueError('Diagnostic prefix cannot reference itself')
    controller, specification, _, _, previous, proof = recorded_prefix(
        folder, anchor, descriptor['anchor_phase_label'])
    directory = source/'replay'
    before = json.loads((directory/'controller-state-before-actions.json').read_text())
    if before['phase_index'] != controller.index:
        raise ValueError('Diagnostic initial controller phase mismatch')
    frame, joints = before['frame'], np.asarray(before['joint_pos'])
    selected = next(i for i,p in enumerate(controller.phases) if p['label']==label)
    if selected < controller.index:
        raise ValueError('Requested diagnostic phase precedes anchor')
    compared = 0
    stream = directory/'native-actions.jsonl'
    for line in stream.open():
        if controller.index == selected:
            break
        row = json.loads(line)
        if row['step'] != compared:
            raise ValueError('Diagnostic actions are discontinuous')
        actual = controller.step(joints, frame)
        if not np.allclose(actual, row['action'], rtol=0., atol=1e-9):
            raise ValueError(f'Diagnostic prefix diverged at action {compared}')
        previous = np.asarray(row['action'])
        frame, joints = row['frame'], np.asarray(row['joint_pos'])
        compared += 1
    if controller.index != selected:
        raise ValueError('Diagnostic did not reach requested phase')
    return controller, specification, frame, joints, previous, {
        'source_kind':'INITIALIZED_DIAGNOSTIC_PREFIX_NOT_DEMONSTRATION',
        'demonstration_credit':False, 'compared_actions':compared,
        'absolute_action_tolerance':1e-9, 'anchor_prefix':proof,
        'source_actions_sha256':hashlib.sha256(stream.read_bytes()).hexdigest(),
        'source_initial_state_sha256':hashlib.sha256((directory/'controller-state-before-actions.json').read_bytes()).hexdigest()}


def recorded_prefix(folder, source, label):
    if (source/'diagnostic-prefix.json').is_file():
        return diagnostic_recorded_prefix(folder, source, label)
    if (source / 'control/robot-actions.jsonl').is_file():
        return control_recorded_prefix(folder, source, label)
    sys.path.insert(0, str(folder))
    from feedback import Controller

    plan = json.loads((folder / 'controller.json').read_text())
    specification = json.loads((folder / 'scene.json').read_text())
    selected = next(i for i, phase in enumerate(plan['phases']) if phase['label'] == label)
    controller = Controller(plan, specification)
    frames = {round(row['frame']['time'] / .05): row['frame'] for row in
              map(json.loads, (source / 'first-trial/native_frames.jsonl').read_text().splitlines())}
    proprio = {}
    proprio_file = source / 'first-trial/measured-joints.jsonl'
    if not proprio_file.is_file():
        proprio_file = source / 'measured-joints.jsonl'
    for row in map(json.loads, proprio_file.read_text().splitlines()):
        step = round(row['time'] / .05)
        if step == 0 and proprio:
            break
        if step in proprio:
            raise ValueError('Duplicate proprioception within the first source trial')
        proprio[step] = row['joint_pos']
    recordings = list((source / 'first-trial/records').glob('*/*/chunks.jsonl'))
    if len(recordings) != 1:
        raise ValueError('Expected exactly one source recording')
    chunks = [row for row in map(json.loads, recordings[0].read_text().splitlines()) if 't' in row]
    compared = 0
    previous = None
    for row in chunks:
        step = row['t']
        if controller.index == selected:
            break
        if step != compared or len(row['actions']) != 1:
            raise ValueError('Source actions are discontinuous or chunked unexpectedly')
        expected = np.asarray(row['actions'][0])
        actual = controller.step(proprio[step], frames[step])
        if not np.allclose(actual, expected, rtol=0., atol=1e-9):
            raise ValueError(f'Controller prefix diverged at action {step}')
        compared += 1
        previous = expected
    if controller.index != selected or previous is None:
        raise ValueError('Source prefix did not reach the requested phase')
    return controller, specification, frames[compared], proprio[compared], previous, {
        'compared_actions': compared,
        'absolute_action_tolerance': 1e-9,
        'source_chunks_sha256': hashlib.sha256(recordings[0].read_bytes()).hexdigest(),
        'source_proprio_sha256': hashlib.sha256(proprio_file.read_bytes()).hexdigest(),
        'source_frame_time': frames[compared]['time'],
    }


def initialize_fixture(embodiment, specification, frame, joints, free_articulation_roots=False, env_origin=None):
    from yam_arena.constants import ARM_JOINTS, FINGER_JOINTS, FINGER_OPEN

    base = embodiment._env.unwrapped
    torch = embodiment._torch
    pending_roots = []
    origin = np.zeros(3) if env_origin is None else np.asarray(env_origin)
    for assembly in specification['assemblies']:
        asset = base.scene[assembly['name']]
        if not assembly.get('fixed'):
            if len(assembly['bodies']) != 1 and not free_articulation_roots:
                raise ValueError('Free articulated replay roots require explicit fixture authorization')
            children = {joint['child'] for joint in assembly.get('joints', [])}
            roots = [body for body in assembly['bodies'] if body['name'] not in children]
            if len(roots) != 1:
                raise ValueError('Replay assembly must have exactly one rigid root')
            pose = frame['bodies'][roots[0]['name']]
            value = torch.tensor([[*(np.asarray(pose['pos'])+origin), *pose['quat']]],
                                 dtype=torch.float32, device=base.device)
            pending_roots.append((asset, value))
        for joint in assembly.get('joints', []):
            index = list(asset.joint_names).index(joint['name'])
            value = torch.tensor([[frame['joints'][joint['name']]]], device=base.device)
            asset.write_joint_position_to_sim_index(position=value, joint_ids=[index])
            asset.write_joint_velocity_to_sim_index(velocity=torch.zeros_like(value), joint_ids=[index])
    for side, offset in [('left', 0), ('right', 7)]:
        asset = base.scene[side + '_robot']
        names = list(ARM_JOINTS) + list(FINGER_JOINTS)
        indices = [list(asset.joint_names).index(name) for name in names]
        values = list(joints[offset:offset+6]) + [joints[offset+6] * FINGER_OPEN] * len(FINGER_JOINTS)
        value = torch.tensor([values], dtype=torch.float32, device=base.device)
        asset.write_joint_position_to_sim_index(position=value, joint_ids=indices)
        asset.write_joint_velocity_to_sim_index(velocity=torch.zeros_like(value), joint_ids=indices)
    # Restore free root transforms last, after all articulation/FK state writes.
    # This follows the successful native mechanism-fixture ordering and avoids
    # a later joint-state refresh invalidating the requested root transform.
    for asset, value in pending_roots:
        asset.write_root_velocity_to_sim_index(root_velocity=torch.zeros((1, 6), device=base.device))
        asset.write_root_pose_to_sim_index(root_pose=value)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--folder', type=Path, required=True)
    parser.add_argument('--source-run', type=Path, required=True)
    parser.add_argument('--phase-label', required=True)
    parser.add_argument('--through-label', required=True)
    parser.add_argument('--commit', required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--max-steps', type=int, default=1200)
    parser.add_argument('--initial-hold-steps', type=int, default=20, choices=range(1, 21),
                        help='Diagnostic motor hold before controller actions:1–20 actual control steps')
    parser.add_argument('--contact-pairs', action='store_true')
    parser.add_argument('--free-articulation-roots', action='store_true',
                        help='Explicitly initialize a recorded free articulated root for diagnostics')
    parser.add_argument('--snapshot', type=Path)
    parser.add_argument('--hold-steps', type=int, default=60)
    parser.add_argument('--worker', action='store_true')
    args = parser.parse_args()
    args.folder = args.folder.resolve()
    args.output = args.output.resolve()
    if args.max_steps < 1:
        parser.error('--max-steps must be positive')
    if args.snapshot and (not args.contact_pairs or not 1 <= args.hold_steps <= args.max_steps):
        parser.error('Recorded contact holds require contact pairs and a bounded hold duration')
    if not args.worker:
        result = subprocess.run([sys.executable, __file__, *sys.argv[1:], '--worker'])
        path = args.output / 'results.json'
        report = json.loads(path.read_text()) if path.is_file() else {}
        passed = (report.get('status') == 'PASS' and report.get('commit') == args.commit
                  and report.get('kind') == 'NATIVE_REPLAY_DIAGNOSTIC_NOT_DEMONSTRATION')
        return 0 if result.returncode == 0 and passed else 1

    args.output.mkdir(parents=True, exist_ok=False)
    report = {'kind': 'NATIVE_REPLAY_DIAGNOSTIC_NOT_DEMONSTRATION', 'status': 'RUNNING',
              'commit': args.commit, 'source_run': str(args.source_run),
              'fixture_initialization': 'Recorded poses and joints, zero velocities, explicitly recorded initial motor hold.',
              'initial_motor_hold_steps': args.initial_hold_steps,
              'initial_motor_hold_seconds': args.initial_hold_steps / 20,
              'demonstration_credit': False, 'scorer_history_restored': False,
              'free_articulation_roots_authorized': args.free_articulation_roots}
    atomic(args.output / 'results.json', report)
    embodiment = None
    controller = None
    observation = None
    runtime = None
    try:
        actual = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=args.folder, text=True).strip()
        if actual != args.commit:
            raise ValueError('Current source revision differs from the requested diagnostic')
        dirty = subprocess.check_output(['git', 'status', '--porcelain', '--', str(args.folder)],
                                        cwd=args.folder, text=True)
        if dirty.strip():
            raise ValueError('Replay diagnostics require a committed, clean task package')
        if args.snapshot:
            snapshot_path = args.snapshot.resolve()
            if not snapshot_path.is_relative_to(args.source_run.resolve()):
                raise ValueError('Snapshot must belong to the declared source run')
            source_report = json.loads((snapshot_path.parent / 'results.json').read_text())
            if source_report.get('commit') != args.commit:
                raise ValueError('Snapshot and current task revisions differ')
            data = snapshot_path.read_bytes()
            snapshot = json.loads(data.splitlines()[-1])
            specification = json.loads((args.folder / 'scene.json').read_text())
            frame = snapshot['frame']
            joints = snapshot['joint_pos']
            previous = np.asarray(snapshot['action'])
            controller = None
            prefix = {'source_kind': 'RECORDED_NATIVE_CONTACT_SNAPSHOT',
                      'source_sha256': hashlib.sha256(data).hexdigest(),
                      'source_frame_time': frame['time']}
            report.update(operation='RECORDED_CONTACT_HOLD', controller_suffix_completed=False)
        else:
            controller, specification, frame, joints, previous, prefix = recorded_prefix(
                args.folder, args.source_run, args.phase_label)
            through = next(i for i, phase in enumerate(controller.phases)
                           if phase['label'] == args.through_label)
            if through < controller.index:
                raise ValueError('Final diagnostic phase precedes its start')
        report['prefix_equivalence'] = prefix
        atomic(args.output / 'results.json', report)
        from inspect_robots import Scene
        from inspect_robots.types import Action
        from inspect_robots_yam.config import DEFAULT_CAMERAS
        from yam_arena.inspect_embodiment import YamArenaEmbodiment

        embodiment = YamArenaEmbodiment(task=str(args.folder / 'task.py'), object_jitter=0,
                                       control_hz=20, cam_width=320, cam_height=176)
        module = embodiment.task.module
        runtime = importlib.import_module(module._name + '.arena_runtime')
        observation = embodiment.reset(Scene(id='replay-diagnostic', instruction=specification['instruction']), seed=0)
        base = embodiment._env.unwrapped
        report['physics_hz'] = 1. / float(base.cfg.sim.dt)
        report['action_hz'] = 1. / float(base.step_dt)
        base.cfg.sim.render_interval = base.cfg.decimation * 4
        for name in DEFAULT_CAMERAS:
            base.scene[name].cfg.update_period = .2
        initialize_fixture(embodiment, specification, frame, joints, args.free_articulation_roots,
                           env_origin=runtime.array(base.scene.env_origins)[0])
        written_bodies = {}
        origin = runtime.array(base.scene.env_origins)[0]
        for assembly in specification['assemblies']:
            asset = base.scene[assembly['name']]
            if assembly.get('joints') or assembly.get('fixed'):
                poses = runtime.array(asset.data.body_link_pose_w)[0]
                for body in assembly['bodies']:
                    value = poses[list(asset.body_names).index(body['name'])]
                    written_bodies[body['name']] = dict(pos=(value[:3]-origin).tolist(), quat=value[3:].tolist())
            else:
                value = runtime.array(asset.data.root_link_pose_w)[0]
                written_bodies[assembly['bodies'][0]['name']] = dict(pos=(value[:3]-origin).tolist(), quat=value[3:].tolist())
        atomic(args.output/'immediate-fixture-state-write.json', dict(
            requested_frame=frame, actual_body_link_poses_before_physics=written_bodies,
            root_write_order='After all task/robot joint and velocity writes',
            scope='Fixture initialization diagnostic only; not a demonstration'))
        for _ in range(args.initial_hold_steps):
            observation = embodiment.step(Action(data=previous)).observation
        atomic(args.output / 'replay-initialized-state.json', {
            'requested_frame': frame,
            'actual_after_initial_motor_hold': runtime.LATEST,
            'initial_motor_hold_steps': args.initial_hold_steps,
            'initial_motor_hold_seconds': args.initial_hold_steps / 20,
            'actual_robot_joint_pos': np.asarray(observation.state['joint_pos']).tolist(),
            'free_articulation_roots_authorized': args.free_articulation_roots,
        })
        if controller is not None:
            atomic(args.output / 'controller-state-before-actions.json',
                   controller_snapshot(controller, observation, runtime.LATEST))
        contact_view = None
        sensor_paths = []
        filter_paths = []
        if args.contact_pairs:
            contact_view, sensor_paths, filter_paths = native_contact_view()
            report['native_contact_sensor_count'] = len(sensor_paths)
            atomic(args.output / 'results.json', report)
        with (args.output / 'native-actions.jsonl').open('w') as stream:
            for step in range(args.max_steps):
                action = (previous if args.snapshot else
                          controller.step(observation.state['joint_pos'], runtime.LATEST))
                observation = embodiment.step(Action(data=action)).observation
                phase_index = snapshot['phase_index'] if args.snapshot else controller.index
                sample = {'step': step, 'phase_index': phase_index,
                          'action': np.asarray(action).tolist(), 'frame': runtime.LATEST,
                          'joint_pos': np.asarray(observation.state['joint_pos']).tolist()}
                if contact_view is not None and step % 5 == 0:
                    sample['measured_native_contacts_N'] = measured_contacts(
                        contact_view, sensor_paths, filter_paths, float(base.cfg.sim.dt))
                stream.write(json.dumps(sample, allow_nan=False) + '\n')
                stream.flush()
                completed = (step+1 >= args.hold_steps if args.snapshot else controller.index > through)
                if completed:
                    break
            else:
                raise ValueError('Diagnostic action limit reached')
        report.update(status='PASS', control_steps=step+1, final_phase_index=phase_index,
                      final_native_frame=runtime.LATEST,
                      controller_events=[] if args.snapshot else controller.events)
        atomic(args.output / 'results.json', report)
    except Exception as exc:
        report.update(status='FAIL', error=f'{type(exc).__name__}: {exc}')
        if controller is not None and observation is not None and runtime is not None:
            try:
                atomic(args.output / 'controller-failure-state.json',
                       controller_snapshot(controller, observation, runtime.LATEST))
            except (TypeError, ValueError) as capture_error:
                report['failure_state_capture_error'] = str(capture_error)
        atomic(args.output / 'results.json', report)
        raise
    finally:
        if embodiment is not None:
            embodiment.close()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
