"""Launch an unchanged task trial and record actual SDK joint observations.

By default this wrapper changes no actions, observations, physics, rendering or scoring.
An explicit --device selects the supported native PhysX backend in SDK arguments.
Its trace is additional diagnostic evidence, never a substitute for validation.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

import numpy as np


def observed_joints(observation):
    joints = np.asarray(observation.state['joint_pos'], dtype=float)
    if joints.shape != (14,) or not np.isfinite(joints).all():
        raise ValueError('Actual SDK proprioception is incomplete or nonfinite')
    time = float(observation.state_time)
    if not np.isfinite(time):
        raise ValueError('Actual SDK observation time is nonfinite')
    return {'time': time, 'joint_pos': joints.tolist()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--folder', type=Path, required=True)
    parser.add_argument('--mode', choices=('expert', 'dream'), required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--commit', required=True)
    parser.add_argument('--evidence', type=Path)
    parser.add_argument('--device', choices=('cuda:0', 'cpu'),
                        help='Explicit supported PhysX backend, recorded in the actual SDK arguments')
    args = parser.parse_args()
    folder, output = args.folder.resolve(), args.output.resolve()
    if output.exists():
        raise ValueError('Trial output must not exist before the task launcher starts')
    from yam_arena.inspect_embodiment import YamArenaEmbodiment
    original_reset, original_step = YamArenaEmbodiment.reset, YamArenaEmbodiment.step
    episode = 0

    def record(observation):
        row = dict(episode=episode, **observed_joints(observation))
        with (output/'measured-joints.jsonl').open('a') as stream:
            stream.write(json.dumps(row, allow_nan=False)+'\n')

    def reset(embodiment, *values, **keywords):
        nonlocal episode
        observation = original_reset(embodiment, *values, **keywords)
        episode += 1
        record(observation)
        return observation

    def step(embodiment, *values, **keywords):
        result = original_step(embodiment, *values, **keywords)
        record(result.observation)
        return result

    context = {'kind': 'READ_ONLY_SDK_PROPRIOCEPTION_TRACE', 'commit': args.commit,
               'wrapper_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               'launcher_sha256': hashlib.sha256((folder/'run.py').read_bytes()).hexdigest(),
               'changes_to_actions_physics_rendering_scoring': False}
    if args.device:
        context['requested_physics_device'] = args.device
        context['changes_to_actions_physics_rendering_scoring'] = True
        context['change_scope'] = 'Explicit native physics device only; task parameters and actions unchanged'
    output.parent.mkdir(parents=True, exist_ok=True)
    output.with_name(output.name+'-trace-context.json').write_text(json.dumps(context, indent=2)+'\n')
    YamArenaEmbodiment.reset, YamArenaEmbodiment.step = reset, step
    sys.path.insert(0, str(folder))
    loader = importlib.util.spec_from_file_location('traced_task_launcher', folder/'run.py')
    module = importlib.util.module_from_spec(loader)
    loader.loader.exec_module(module)
    if args.device:
        original_command = module.command

        def command_with_explicit_device(*values, **keywords):
            return [*original_command(*values, **keywords), '-E', f'device={args.device}']

        module.command = command_with_explicit_device
    sys.argv = [str(folder/'run.py'), '--mode', args.mode, '--execute', '--commit', args.commit,
                '--output', str(output)]
    if args.evidence:
        sys.argv.extend(['--evidence', str(args.evidence.resolve())])
    return module.main()


if __name__ == '__main__':
    raise SystemExit(main())
