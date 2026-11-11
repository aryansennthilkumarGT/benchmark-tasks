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


def recorded_prefix(folder, source, label):
    sys.path.insert(0, str(folder))
    from feedback import Controller

    plan = json.loads((folder / 'controller.json').read_text())
    specification = json.loads((folder / 'scene.json').read_text())
    selected = next(i for i, phase in enumerate(plan['phases']) if phase['label'] == label)
    controller = Controller(plan, specification)
    frames = {round(row['frame']['time'] / .05): row['frame'] for row in
              map(json.loads, (source / 'first-trial/native_frames.jsonl').read_text().splitlines())}
    proprio = {}
    for row in map(json.loads, (source / 'measured-joints.jsonl').read_text().splitlines()):
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
        'source_frame_time': frames[compared]['time'],
    }


def initialize_fixture(embodiment, specification, frame, joints):
    from yam_arena.constants import ARM_JOINTS, FINGER_JOINTS, FINGER_OPEN

    base = embodiment._env.unwrapped
    torch = embodiment._torch
    for assembly in specification['assemblies']:
        asset = base.scene[assembly['name']]
        if not assembly.get('fixed'):
            if len(assembly['bodies']) != 1:
                raise ValueError('Free articulated replay roots require a dedicated fixture')
            pose = frame['bodies'][assembly['bodies'][0]['name']]
            value = torch.tensor([[*pose['pos'], *pose['quat']]], dtype=torch.float32,
                                 device=base.device)
            asset.write_root_pose_to_sim_index(root_pose=value)
            asset.write_root_velocity_to_sim_index(root_velocity=torch.zeros((1, 6), device=base.device))
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


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--folder', type=Path, required=True)
    parser.add_argument('--source-run', type=Path, required=True)
    parser.add_argument('--phase-label', required=True)
    parser.add_argument('--through-label', required=True)
    parser.add_argument('--commit', required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--max-steps', type=int, default=1200)
    parser.add_argument('--worker', action='store_true')
    args = parser.parse_args()
    args.folder = args.folder.resolve()
    args.output = args.output.resolve()
    if args.max_steps < 1:
        parser.error('--max-steps must be positive')
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
              'fixture_initialization': 'Recorded poses and joints, zero velocities, one-second motor hold.',
              'demonstration_credit': False, 'scorer_history_restored': False}
    atomic(args.output / 'results.json', report)
    embodiment = None
    try:
        actual = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=args.folder, text=True).strip()
        if actual != args.commit:
            raise ValueError('Current source revision differs from the requested diagnostic')
        dirty = subprocess.check_output(['git', 'status', '--porcelain', '--', str(args.folder)],
                                        cwd=args.folder, text=True)
        if dirty.strip():
            raise ValueError('Replay diagnostics require a committed, clean task package')
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
        initialize_fixture(embodiment, specification, frame, joints)
        for _ in range(20):
            observation = embodiment.step(Action(data=previous)).observation
        with (args.output / 'native-actions.jsonl').open('w') as stream:
            for step in range(args.max_steps):
                action = controller.step(observation.state['joint_pos'], runtime.LATEST)
                observation = embodiment.step(Action(data=action)).observation
                stream.write(json.dumps({'step': step, 'phase_index': controller.index,
                                         'action': np.asarray(action).tolist(), 'frame': runtime.LATEST,
                                         'joint_pos': np.asarray(observation.state['joint_pos']).tolist()}) + '\n')
                stream.flush()
                if controller.index > through:
                    break
            else:
                raise ValueError('Diagnostic action limit reached')
        report.update(status='PASS', control_steps=step+1, final_phase_index=controller.index,
                      final_native_frame=runtime.LATEST, controller_events=controller.events)
        atomic(args.output / 'results.json', report)
    except Exception as exc:
        report.update(status='FAIL', error=f'{type(exc).__name__}: {exc}')
        atomic(args.output / 'results.json', report)
        raise
    finally:
        if embodiment is not None:
            embodiment.close()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
