"""Run native mechanism/control probes with explicitly recorded render decimation."""
from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import math
from pathlib import Path
import runpy
import subprocess
import sys

import numpy as np

from engine import atomic


def diagnostic_controller_state(controller):
    index = controller.index
    value = dict(
        phase_index=index,
        phase_label=(controller.phases[index]['label'] if index < len(controller.phases) else 'complete'),
        thread_state=getattr(controller,'thread',None),
        context=getattr(controller,'context',None),
    )
    return json.loads(json.dumps(value, default=lambda value: np.asarray(value).tolist(), allow_nan=False))


def sdk_sample(names, velocities, efforts, settings):
    """SI actuator samples, preserving SDK finger force/linear-speed units."""
    if len(names)!=len(set(names)) or set(names)!=set(settings):
        raise ValueError('Native robot joints differ from the pinned SDK')
    velocities=np.asarray(velocities,dtype=float);efforts=np.asarray(efforts,dtype=float)
    if velocities.shape!=(len(names),) or efforts.shape!=velocities.shape or not np.isfinite(velocities).all() or not np.isfinite(efforts).all():
        raise ValueError('Nonfinite or malformed native actuator telemetry')
    limits=np.array([[settings[n]['velocity'],settings[n]['effort']] for n in names],dtype=float)
    if not np.isfinite(limits).all() or np.any(limits<=0):raise ValueError('Invalid SDK limits')
    velocity_ratio=float(np.max(np.abs(velocities)/limits[:,0]));effort_ratio=float(np.max(np.abs(efforts)/limits[:,1]))
    return dict(joint_names=list(names),joint_vel_SI=velocities.tolist(),applied_effort_SI=efforts.tolist(),
                sdk_limits_SI=limits.tolist(),maximum_velocity_ratio=velocity_ratio,maximum_effort_ratio=effort_ratio,
                passed=velocity_ratio<=1.001 and effort_ratio<=1.001)


def completed_report(path, mode, commit):
    if not path.is_file():
        return False
    report = json.loads(path.read_text())
    return (report.get('status') == 'PASS'
            and report.get('mode') == mode
            and report.get('commit') == commit
            and report.get('passed', 0) > 0
            and report.get('failed') == 0)


def observed_cadence(metadata):
    resets = metadata.get('resets', [])
    if not resets:
        return False
    for record in resets:
        if record.get('camera_samples'):
            continue
        steps = record.get('control_steps_completed')
        start = record.get('camera_frame_start', {})
        end = record.get('camera_frame_end', {})
        if not isinstance(steps, int) or not 0 < steps < 20 or not start or start.keys() != end.keys():
            return False
        maximum = math.ceil(steps / metadata['render_every_control_steps']) + 1
        if any(not 0 <= end[name]-value <= maximum for name, value in start.items()):
            return False
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--folder', type=Path, required=True)
    parser.add_argument('--mode', choices=('physics', 'control'), required=True)
    parser.add_argument('--commit', required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--case', action='append', default=[])
    parser.add_argument('--render-every', type=int, choices=(1, 4), default=4)
    parser.add_argument('--expected-physics-hz', type=int, choices=(240, 480, 960, 1920), default=240)
    parser.add_argument('--contact-pairs', action='store_true',
                        help='Record actual robot and task-body native contact forces every five controls')
    parser.add_argument('--fail-fast', action='store_true', help='Forward first-failure stop to the frozen native runner')
    parser.add_argument('--sdk-limits', action='store_true', help='Record SI velocity/effort and stop observed SDK violations at20Hz; not substep certification')
    parser.add_argument('--worker', action='store_true', help=argparse.SUPPRESS)
    parser.add_argument('--device', choices=('cuda:0', 'cpu'), default='cuda:0',
                        help='Explicit supported native PhysX device; RTX rendering remains enabled')
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
        metadata['worker_exit_code'] = result.returncode
        atomic(receipt, metadata)
        return 0 if result.returncode == 0 and passed and observed_cadence(metadata) else 1

    from yam_arena.inspect_embodiment import YamArenaEmbodiment
    from inspect_robots_yam.config import DEFAULT_CAMERAS
    original_init = YamArenaEmbodiment.__init__

    def init_with_explicit_device(embodiment, *values, **keywords):
        keywords['device'] = args.device
        return original_init(embodiment, *values, **keywords)

    YamArenaEmbodiment.__init__ = init_with_explicit_device

    metadata = {
        'kind': 'NATIVE_PROBE_WITH_DIAGNOSTIC_RENDER_CADENCE',
        'scope': 'Mechanism/control probes with fixture initialization where declared. No demonstration.',
        'commit': args.commit,
        'mode': args.mode,
        'requested_physics_device': args.device,
        'render_every_control_steps': args.render_every,
        'wrapper_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'native_script_sha256': hashlib.sha256(script.read_bytes()).hexdigest(),
        'sdk_sampling_hz':20 if args.sdk_limits else None,
        'sdk_continuous_substep_monitor':False,
        'sdk_maximum_velocity_ratio':0.,'sdk_maximum_effort_ratio':0.,
        'resets': [],
    }
    atomic(receipt, metadata)
    original_reset = YamArenaEmbodiment.reset
    original_step = YamArenaEmbodiment.step
    control_steps = 0
    controller_state = {}
    contacts = None
    traced_controller_classes = set()

    def trace_controller_class(controller_class):
        if controller_class in traced_controller_classes:
            return
        original_controller_step = controller_class.step

        def step_with_phase_trace(controller, *values, **keywords):
            action = original_controller_step(controller, *values, **keywords)
            controller_state.update(diagnostic_controller_state(controller))
            return action

        controller_class.step = step_with_phase_trace
        traced_controller_classes.add(controller_class)

    def camera_frames(base):
        counts = {}
        for name in DEFAULT_CAMERAS:
            frame = base.scene[name].frame
            frame = frame.torch if hasattr(frame, 'torch') else frame
            counts[name] = int(frame[0].item())
        return counts

    def reset_with_diagnostic_rendering(embodiment, *reset_args, **reset_kwargs):
        nonlocal control_steps, contacts
        atomic(receipt, metadata)
        observation = original_reset(embodiment, *reset_args, **reset_kwargs)
        if args.mode == 'control':
            feedback = importlib.import_module(embodiment.task.module._name + '.feedback')
            trace_controller_class(feedback.Controller)
            controller_state.clear()
        base = embodiment._env.unwrapped
        from isaaclab_physx.physics import PhysxManager
        actual_device = str(PhysxManager.get_physics_sim_device())
        if actual_device != args.device:
            raise ValueError(f'Actual PhysX device {actual_device} differs from requested {args.device}')
        metadata['actual_physics_device'] = actual_device
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
        if args.contact_pairs:
            from replay_native import native_contact_view
            contacts = native_contact_view(include_task_sensors=True)
        metadata['resets'].append({
            'initial_robot_joint_pos': np.asarray(observation.state['joint_pos']).tolist(),
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
        if args.sdk_limits:
            from yam_arena.constants import ARM_JOINTS,FINGER_JOINTS,SHOULDER,WRIST,GRIPPER
            settings={n:(SHOULDER if i<3 else WRIST) for i,n in enumerate(ARM_JOINTS)}
            settings.update({n:GRIPPER for n in FINGER_JOINTS})
            runtime=importlib.import_module(embodiment.task.module._name+'.arena_runtime')
            base=embodiment._env.unwrapped
            records={}
            for side in ('left','right'):
                asset=base.scene[side+'_robot']
                records[side]=sdk_sample(list(asset.joint_names),runtime.array(asset.data.joint_vel)[0],
                                         runtime.array(asset.data.applied_torque)[0],settings)
            row={'reset_index':len(metadata['resets'])-1,'control_step':control_steps,
                 'time':float(result.observation.state_time),'robot_sdk_samples':records}
            with (args.output/'native-sdk-samples.jsonl').open('a') as stream:stream.write(json.dumps(row,allow_nan=False)+'\n')
            metadata['sdk_maximum_velocity_ratio']=max(metadata['sdk_maximum_velocity_ratio'],*(v['maximum_velocity_ratio'] for v in records.values()))
            metadata['sdk_maximum_effort_ratio']=max(metadata['sdk_maximum_effort_ratio'],*(v['maximum_effort_ratio'] for v in records.values()))
            if not all(v['passed'] for v in records.values()):
                metadata['sdk_violation']=row;atomic(receipt,metadata)
                raise ValueError('Observed native actuator velocity/effort exceeds SDK limit; see native-sdk-samples.jsonl')
        metadata['resets'][-1]['control_steps_completed'] = control_steps
        if control_steps < 20:
            metadata['resets'][-1]['camera_frame_end'] = camera_frames(embodiment._env.unwrapped)
        if args.mode == 'control':
            observation = result.observation
            with (args.output / 'robot-actions.jsonl').open('a') as stream:
                stream.write(json.dumps({
                    'reset_index': len(metadata['resets'])-1,
                    'control_step': control_steps,
                    'time': float(observation.state_time),
                    'controller': controller_state.copy(),
                    'submitted_action': submitted_action,
                    'measured_joint_pos': np.asarray(observation.state['joint_pos']).tolist(),
                }, allow_nan=False) + '\n')
        if args.contact_pairs and control_steps % 5 == 0:
            from replay_native import measured_contacts
            view, sensors, filters = contacts
            record = dict(reset_index=len(metadata['resets'])-1, control_step=control_steps,
                          time=float(embodiment._t), physics_dt=float(embodiment._env.unwrapped.cfg.sim.dt),
                          contacts_N=measured_contacts(view, sensors, filters,
                                                      float(embodiment._env.unwrapped.cfg.sim.dt)))
            with (args.output/'native-contacts.jsonl').open('a') as stream:
                stream.write(json.dumps(record, allow_nan=False)+'\n')
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
    if args.fail_fast:sys.argv.append('--fail-fast')
    try:
        runpy.run_path(str(script), run_name='__main__')
    finally:
        atomic(receipt, metadata)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
