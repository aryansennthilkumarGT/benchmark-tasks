"""Run native mechanism/control probes with explicitly recorded render decimation."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import runpy
import subprocess
import sys

import numpy as np

from engine import atomic


def completed_report(path, mode, commit):
    if not path.is_file():
        return False
    report = json.loads(path.read_text())
    return (report.get('status') == 'PASS'
            and report.get('mode') == mode
            and report.get('commit') == commit
            and report.get('passed', 0) > 0
            and report.get('failed') == 0)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--folder', type=Path, required=True)
    parser.add_argument('--mode', choices=('physics', 'control'), required=True)
    parser.add_argument('--commit', required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--case', action='append', default=[])
    parser.add_argument('--render-every', type=int, choices=(1, 4), default=4)
    parser.add_argument('--expected-physics-hz', type=int, choices=(240, 480), default=240)
    parser.add_argument('--worker', action='store_true', help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.render_every < 1:
        parser.error('--render-every must be positive')
    args.folder = args.folder.resolve()
    args.output = args.output.resolve()
    script = args.folder / 'native_tests.py'
    receipt = args.output.parent / (args.output.name + '-render-diagnostic.json')
    if not args.worker:
        result = subprocess.run([sys.executable, __file__, *sys.argv[1:], '--worker'])
        passed = completed_report(args.output / 'results.json', args.mode, args.commit)
        metadata = json.loads(receipt.read_text()) if receipt.is_file() else {}
        resets = metadata.get('resets', [])
        observed = bool(resets) and all(record.get('camera_samples') for record in resets)
        return 0 if result.returncode == 0 and passed and observed else 1

    from yam_arena.inspect_embodiment import YamArenaEmbodiment
    from inspect_robots_yam.config import DEFAULT_CAMERAS

    metadata = {
        'kind': 'NATIVE_PROBE_WITH_DIAGNOSTIC_RENDER_CADENCE',
        'scope': 'Mechanism/control probes with fixture initialization where declared. No demonstration.',
        'commit': args.commit,
        'mode': args.mode,
        'render_every_control_steps': args.render_every,
        'wrapper_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'native_script_sha256': hashlib.sha256(script.read_bytes()).hexdigest(),
        'resets': [],
    }
    atomic(receipt, metadata)
    original_reset = YamArenaEmbodiment.reset
    original_step = YamArenaEmbodiment.step
    control_steps = 0

    def camera_frames(base):
        counts = {}
        for name in DEFAULT_CAMERAS:
            frame = base.scene[name].frame
            frame = frame.torch if hasattr(frame, 'torch') else frame
            counts[name] = int(frame[0].item())
        return counts

    def reset_with_diagnostic_rendering(embodiment, *reset_args, **reset_kwargs):
        nonlocal control_steps
        observation = original_reset(embodiment, *reset_args, **reset_kwargs)
        base = embodiment._env.unwrapped
        physics_dt = float(base.cfg.sim.dt)
        control_dt = float(base.step_dt)
        decimation = int(base.cfg.decimation)
        if not math.isclose(control_dt, .05) or not math.isclose(physics_dt, 1 / args.expected_physics_hz):
            raise ValueError('Unexpected native physics/control timing')
        if not math.isclose(physics_dt * decimation, control_dt):
            raise ValueError('Native control decimation mismatch')
        base.cfg.sim.render_interval = decimation * args.render_every
        for name in DEFAULT_CAMERAS:
            base.scene[name].cfg.update_period = control_dt * args.render_every
        control_steps = 0
        metadata['resets'].append({
            'physics_dt_s': physics_dt,
            'control_dt_s': control_dt,
            'render_interval_physics_steps': base.cfg.sim.render_interval,
            'diagnostic_render_hz': 1 / (physics_dt * base.cfg.sim.render_interval),
            'camera_frame_start': camera_frames(base),
            'camera_samples': [],
        })
        atomic(receipt, metadata)
        return observation

    def step_with_cadence_verification(embodiment, *step_args, **step_kwargs):
        nonlocal control_steps
        submitted = step_args[0] if step_args else step_kwargs['action']
        submitted_action = np.asarray(submitted.data).tolist()
        result = original_step(embodiment, *step_args, **step_kwargs)
        control_steps += 1
        if args.mode == 'control':
            observation = result.observation
            with (args.output / 'robot-actions.jsonl').open('a') as stream:
                stream.write(json.dumps({
                    'reset_index': len(metadata['resets'])-1,
                    'control_step': control_steps,
                    'time': float(observation.state_time),
                    'submitted_action': submitted_action,
                    'measured_joint_pos': np.asarray(observation.state['joint_pos']).tolist(),
                }, allow_nan=False) + '\n')
        if control_steps % 20 == 0:
            record = metadata['resets'][-1]
            current = camera_frames(embodiment._env.unwrapped)
            previous = (record['camera_samples'][-1]['frames'] if record['camera_samples']
                        else record['camera_frame_start'])
            increments = {name: current[name] - previous[name] for name in DEFAULT_CAMERAS}
            record['camera_samples'].append({'control_steps': control_steps, 'frames': current,
                                             'frames_per_control_second': increments})
            atomic(receipt, metadata)
            maximum = math.ceil(20 / args.render_every) + 1
            if any(value < 1 or value > maximum for value in increments.values()):
                raise ValueError('Observed camera cadence differs from diagnostic configuration')
        return result

    YamArenaEmbodiment.reset = reset_with_diagnostic_rendering
    YamArenaEmbodiment.step = step_with_cadence_verification
    sys.path.insert(0, str(args.folder))
    sys.argv = [str(script), '--mode', args.mode, '--commit', args.commit,
                '--output', str(args.output), '--worker']
    for name in args.case:
        sys.argv.extend(['--case', name])
    runpy.run_path(str(script), run_name='__main__')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
