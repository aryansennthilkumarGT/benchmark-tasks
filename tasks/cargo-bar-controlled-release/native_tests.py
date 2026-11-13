"""Native PhysX probes, distinct from the two robot feasibility demonstrations.

Physics fixtures may initialize joint/body poses to isolate a mechanism and apply
known forces. Such probes are explicitly labelled and NEVER used as expert/model
video evidence. Control tests use only real 14-D robot actions after reset.
"""
import argparse
import copy
import importlib
import json
import os
from pathlib import Path
import subprocess
import sys
sys.dont_write_bytecode=True
import traceback
import numpy as np

HERE=Path(__file__).resolve().parent


def save(path,value):
    temporary = path.with_suffix('.tmp')
    temporary.write_text(json.dumps(value, indent=2, allow_nan=False) + '\n')
    temporary.replace(path)


def checks(assertions,initial,final,result=None):
    from feedback import qangle, rotate
    for item in assertions:
        kind=item['kind']
        if kind=='joint':
            value=final['joints'][item['joint']]
            assert item['min']<=value<=item['max'],(item,value)
        elif kind=='displacement':
            p=np.asarray(final['bodies'][item['body']]['pos'])-initial['bodies'][item['body']]['pos']
            value=float(np.dot(p,item['axis'])) if item.get('axis') else float(np.linalg.norm(p))
            assert item['min']<=value<=item['max'],(item,value)
        elif kind=='coordinate':
            value=final['bodies'][item['body']]['pos'][item['axis']]
            assert item['min']<=value<=item['max'],(item,value)
        elif kind=='pose':
            body=final['bodies'][item['body']]
            assert np.linalg.norm(np.asarray(body['pos'])-item['pos'])<=item['tolerance'],item
            if 'quat' in item:assert qangle(body['quat'],item['quat'])<=item.get('angle',0.05),item
        elif kind == 'axis':
            actual = rotate(final['bodies'][item['body']]['quat'], item['local_axis'])
            direction = np.asarray(item['direction'], dtype=float)
            cosine = np.dot(actual, direction) / (np.linalg.norm(actual) * np.linalg.norm(direction))
            assert cosine >= np.cos(item['angle']) - 1e-9, (item, cosine)
        elif kind=='penetration':
            assert final['max_penetration']<=item['max'],(item,final['max_penetration'])
        elif kind=='still':
            body=final['bodies'][item['body']]
            assert np.linalg.norm(body['linear'])<=item['speed'] and np.linalg.norm(body['angular'])<=item['spin'],item
        elif kind=='score':
            assert result is not None,'Native scorer result missing'
            assert item.get('min',0)<=result.score<=item.get('max',1),(item,result)
            if 'success' in item:assert result.success==item['success'],(item,result)
        elif kind=='goal':
            assert result is not None,'Native scorer result missing'
            assert (item['name'] in result.completed)==item['completed'],(item,result)
        elif kind=='valid':
            assert result is not None and result.failure is None,(item,result)
        else:raise ValueError('Unknown native assertion: '+kind)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--mode',choices=['physics','control'],required=True)
    parser.add_argument('--output',type=Path,required=True);parser.add_argument('--commit',required=True)
    parser.add_argument('--case', action='append',
                        help='Run a named diagnostic case only. Repeat this option to select multiple cases.')
    parser.add_argument('--worker', action='store_true', help=argparse.SUPPRESS)
    args=parser.parse_args()
    if not args.worker:
        # Keep the caller's exit status independent of Kit's interpreter shutdown.
        child = subprocess.run([sys.executable, str(__file__), *sys.argv[1:], '--worker'])
        if child.returncode:
            return child.returncode
        report_path = args.output/'results.json'
        if not report_path.is_file():
            print('Native worker produced no results.json', file=sys.stderr)
            return 1
        report = json.loads(report_path.read_text())
        return 0 if report.get('status') == 'PASS' else 1
    if sys.platform!='linux':raise SystemExit('Native tests require the official Linux GPU environment')
    current=subprocess.run(['git','rev-parse','HEAD'],cwd=HERE,text=True,capture_output=True,check=True).stdout.strip()
    if current!=args.commit:raise SystemExit('Test revision mismatch')
    cases = json.loads((HERE/'native-cases.json').read_text())[args.mode]
    if args.case:
        declared = {case['name'] for case in cases}
        if set(args.case) - declared:
            raise ValueError('Unknown native diagnostic case for ' + args.mode)
        cases = [case for case in cases if case['name'] in args.case]
    if not cases:
        raise ValueError('No mechanism/control test cases configured')
    args.output.mkdir(parents=True,exist_ok=False)
    os.environ['ROBOCURVE_TRACE']=str(args.output.resolve()/'physics-probes-not-demonstrations.jsonl')
    kind = 'NATIVE_PHYSX_DIAGNOSTIC_CASES' if args.case else 'NATIVE_PHYSX_TESTS'
    report={'kind':kind,'mode':args.mode,'commit':args.commit,'reset_count':0,
            'passed':0,'failed':0,'cases':[],'camera_coverage':False,
            'initialization_probes_are_not_demonstrations':True,'status':'RUNNING','active_case':None}
    results_path = args.output/'results.json'
    save(results_path, report)
    from inspect_robots import Scene
    from inspect_robots.types import Action
    from yam_arena.inspect_embodiment import YamArenaEmbodiment
    embodiment=YamArenaEmbodiment(task=str(HERE/'task.py'),object_jitter=0,control_hz=20,cam_width=320,cam_height=176)
    module=embodiment.task.module
    runtime=importlib.import_module(module._name+'.arena_runtime')
    controller_class=importlib.import_module(module._name+'.feedback').Controller
    from audit_control import camera_coverage
    initial_reference=None
    scene=Scene(id='native-test',instruction=module.SPEC['instruction'])
    try:
        for repeat in (0,1):
            for case in cases:
                row={'name':case['name'],'repeat':repeat,'status':'RUNNING'}
                report['active_case'] = {'name': case['name'], 'repeat': repeat}
                save(results_path, report)
                touched=[]
                controller=None
                try:
                    observation=embodiment.reset(scene,seed=0);report['reset_count']+=1
                    frame=copy.deepcopy(runtime.LATEST)
                    if initial_reference is None:initial_reference=frame
                    else:
                        for name,body in frame['bodies'].items():
                            delta=np.linalg.norm(np.asarray(body['pos'])-initial_reference['bodies'][name]['pos'])
                            assert delta<0.003,('reset drift',name,delta)
                    coverage=camera_coverage(module.SPEC,frame['bodies'])
                    assert all(v['visible'] for v in coverage.values()),'Initial task geometry out of view'
                    report['camera_coverage']=True
                    save(args.output/f'{case["name"]}-{repeat}-initial.json',frame)
                    ready=np.asarray(observation.state['joint_pos']).copy()
                    base=embodiment._env.unwrapped;torch=embodiment._torch
                    if args.mode=='physics':
                        # Fixture setup is allowed only here; expert.py has no state-write path.
                        for setup in case.get('initialize_joints',[]):
                            asset=base.scene[setup['assembly']]
                            index=list(asset.joint_names).index(setup['joint'])
                            asset.write_joint_position_to_sim_index(position=torch.tensor([[setup['value']]],device=base.device),joint_ids=[index])
                            asset.write_joint_velocity_to_sim_index(velocity=torch.zeros((1,1),device=base.device),joint_ids=[index])
                        for setup in case.get('initialize_bodies',[]):
                            asset=base.scene[setup['assembly']]
                            description=next(a for a in module.SPEC['assemblies'] if a['name']==setup['assembly'])
                            if description.get('fixed'):raise ValueError('Cannot move a fixed fixture root')
                            if description.get('joints') and not setup.get('free_articulation_root'):
                                raise ValueError('Free articulated root initialization must be explicit')
                            value=torch.tensor([[*setup['pos'],*setup.get('quat',[0,0,0,1])]],device=base.device)
                            asset.write_root_pose_to_sim_index(root_pose=value)
                            asset.write_root_velocity_to_sim_index(root_velocity=torch.zeros((1,6),device=base.device))
                        base.sim.forward()
                        initialized = {'joints': [], 'roots': []}
                        for setup in case.get('initialize_joints', []):
                            asset = base.scene[setup['assembly']]
                            index = list(asset.joint_names).index(setup['joint'])
                            actual = float(runtime.array(asset.data.joint_pos)[0, index])
                            assert abs(actual - setup['value']) < 1e-6, ('fixture joint write', setup, actual)
                            initialized['joints'].append(dict(setup, measured=actual))
                        for setup in case.get('initialize_bodies', []):
                            asset = base.scene[setup['assembly']]
                            actual = runtime.array(asset.data.root_link_pose_w)[0].tolist()
                            assert np.linalg.norm(np.asarray(actual[:3]) - setup['pos']) < 1e-6, ('fixture root write', setup, actual)
                            initialized['roots'].append(dict(setup, measured_pose=actual))
                        save(args.output/f'{case["name"]}-{repeat}-post-initialization.json', initialized)
                        for force in case.get('forces',[]):
                            asset=base.scene[force['assembly']]
                            index=list(asset.body_names).index(force['body'])
                            if not any(asset is other for other in touched):
                                asset.permanent_wrench_composer.reset();touched.append(asset)
                            asset.permanent_wrench_composer.add_forces_and_torques_index(
                                torch.tensor([[force.get('force',[0,0,0])]],dtype=torch.float32,device=base.device),
                                torch.tensor([[force.get('torque',[0,0,0])]],dtype=torch.float32,device=base.device),body_ids=[index],is_global=True)
                        for _ in range(case['steps']):embodiment.step(Action(data=ready))
                        for asset in touched:asset.permanent_wrench_composer.reset()
                        for _ in range(case.get('settle_steps',20)):embodiment.step(Action(data=ready))
                    else:
                        controller=controller_class(json.loads((HERE/'controller.json').read_text()),module.SPEC)
                        prefix=case['through_phase']
                        if controller.phases[prefix]['label']!=case['through_label']:
                            raise ValueError('Control probe phase/label mismatch; update the case for this revision')
                        for step in range(case['max_steps']):
                            action=controller.step(observation.state['joint_pos'],runtime.LATEST)
                            result=embodiment.step(Action(data=action));observation=result.observation
                            if controller.index>prefix:break
                        else:raise AssertionError('Robot control prefix exceeded test action limit')
                        save(args.output/f'{case["name"]}-{repeat}-events.json',controller.events)
                    final=copy.deepcopy(runtime.LATEST)
                    save(args.output/f'{case["name"]}-{repeat}-final.json',final)
                    checks(case['assertions'],frame,final,module.EVALUATOR.result)
                    from dataclasses import asdict
                    row['scoring']=asdict(module.EVALUATOR.result)
                    row['status']='PASS';report['passed']+=1
                except Exception as exc:
                    if controller is not None:
                        diagnostic = {
                            'phase_index': controller.index,
                            'phase': controller.phases[controller.index] if controller.index < len(controller.phases) else None,
                            'events': controller.events,
                            'robot_joint_pos': np.asarray(observation.state['joint_pos']).tolist(),
                            'motion_references': {
                                side: motion.reference.tolist() if motion.reference is not None else None
                                for side, motion in controller.motion.items()
                            },
                            'applied_joint_torques': {
                                side: runtime.array(base.scene[f'{side}_robot'].data.applied_torque)[0].tolist()
                                for side in ('left', 'right')
                            },
                            'thread_state': {
                                name: value.tolist() if isinstance(value, np.ndarray) else value
                                for name, value in (controller.thread or {}).items()
                            },
                            'grasp_transforms': {
                                side: {name: value.tolist() if isinstance(value, np.ndarray) else value
                                       for name, value in grasp.items()}
                                for side, grasp in getattr(controller,'grasps',{}).items()
                            },
                            'last_frame': copy.deepcopy(runtime.LATEST),
                        }
                        save(args.output/f'{case["name"]}-{repeat}-control-failure.json', diagnostic)
                    row.update(status='FAIL',error=str(exc),traceback=traceback.format_exc());report['failed']+=1
                finally:
                    # A failed probe must never leave its force active for the next reset.
                    for asset in touched:asset.permanent_wrench_composer.reset()
                report['cases'].append(row)
                report['active_case'] = None
                save(results_path, report)
    finally:
        embodiment.close()
    report['status'] = 'FAIL' if report['failed'] else 'PASS'
    save(results_path, report)
    return 1 if report['failed'] else 0


if __name__=='__main__':raise SystemExit(main())
