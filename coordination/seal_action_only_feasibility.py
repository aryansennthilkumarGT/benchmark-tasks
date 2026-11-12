"""Seal actual cold action-only experts with explicitly reused identical mechanics.

No simulation is launched. Raw source revisions and reset counts remain intact.
"""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess

from engine import artifacts, atomic, digest, fingerprint, utc
from stage_gate import require_no_interruption
from verify_action_only_experts import verify, require


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def same_components(checker, folder, target, source, names):
    slug = folder.name
    files = {}
    for name in sorted(names):
        relative = name.split('#', 1)[0]
        original = subprocess.check_output(['git', 'show', f'{source}:tasks/{slug}/{relative}'], cwd=folder)
        current = (folder/relative).read_bytes()
        expected = checker.component_hash(name, original)
        require(checker.component_hash(name, current) == expected,
                'Source implementation differs from real evidence: '+name)
        files[name] = expected
    return {'source_commit': source, 'target_commit': target, 'files': files,
            'method': 'Exact file bytes or explicitly named AST/JSON component; original source revisions and actual runs retained, no new physics run claimed.'}


def clone_evidence(source, target):
    # Completed immutable outputs only. Hard links preserve raw bytes without
    # duplicating gigabytes or inventing a new executed episode.
    shutil.copytree(source, target, copy_function=os.link,
                    ignore=lambda folder, names: ['receipt.json'] if 'receipt.json' in names else [])
    if (source/'receipt.json').is_file():
        shutil.copyfile(source/'receipt.json', target/'original-source-receipt.json')


def seal(config):
    require(__debug__, 'Native assertion checks require Python without optimization')
    root = Path(config['root']).resolve()
    target_folder = Path(config['target_folder']).resolve()
    expert_folder = Path(config['expert_folder']).resolve()
    target, source = config['target_commit'], config['expert_commit']
    require(subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=target_folder, text=True).strip() == target,
            'Target source revision changed')
    require(not subprocess.check_output(['git', 'status', '--porcelain', '--', '.'],
                                       cwd=target_folder, text=True).strip(), 'Target source is dirty')
    exits = {}
    for name, value in config['exit_files'].items():
        path = Path(value)
        require_no_interruption(path.parent)
        require(path.read_text().strip() == '0', 'Missing/nonzero actual stage: '+name)
        exits[name] = {'path': str(path), 'sha256': digest(path)}
    require(set(exits) == {'first', 'first_validation', 'second', 'second_validation',
                          'expert_producer', 'physics', 'physics_producer'}, 'Required actual exits omitted')
    inventories = []
    for value in config['gpu_inventories']:
        path = Path(value)
        require('L40S' in path.read_text() and '565.57.01' in path.read_text(),
                'Missing actual fixed-driver GPU evidence')
        inventories.append({'path': str(path), 'sha256': digest(path)})
    require(len(inventories) >= 2, 'Actual physics and expert inventories required')
    checker = load(target_folder/'feasibility_v2.py', '_action_only_target_checker')
    mechanics = same_components(checker, target_folder, target, config['physics_commit'],
                                 checker.mechanics_names(target_folder))
    expert = same_components(checker, target_folder, target, source,
                              {'expert.py', 'expert_joint_trajectory.json', 'run.py#excluding_feasible'})
    trials = [Path(config['first_trial']).resolve(), Path(config['second_trial']).resolve()]
    proofs = [json.loads((p/'validated-rollout.json').read_text()) for p in trials]
    require(all(p['score'] == 1 and p['mode'] == 'expert' and p['commit'] == source for p in proofs),
            'Two actual complete state-independent experts required')
    physics_directory = Path(config['physics_directory']).resolve()
    physics = json.loads((physics_directory/'results.json').read_text())
    expected = {(case['name'], repeat) for case in json.loads((target_folder/'native-cases.json').read_text())['physics']
                for repeat in (0, 1)}
    require(physics['kind'] == 'NATIVE_PHYSX_TESTS' and physics['mode'] == 'physics'
            and physics['commit'] == config['physics_commit'] and physics['status'] == 'PASS'
            and physics['failed'] == 0 and physics['passed'] == physics['reset_count'] == len(expected)
            and len(physics['cases']) == len(expected)
            and {(p['name'], p['repeat']) for p in physics['cases'] if p['status'] == 'PASS'} == expected,
            'Actual mechanism suite lacks full case/reset coverage')
    require_no_interruption(root)
    root.mkdir(parents=True, exist_ok=True)
    require(not (root/'evidence/feasibility.json').exists(), 'Proof already sealed; use its immutable receipt')
    control = verify(expert_folder, trials, source, root/'control')
    # verify() revalidates whole official SDK records, every executed action,
    # all three camera streams, native scorer replay and every actual predicate.
    directories = {'physics': root/'physics', 'control': root/'control',
                   'first': root/'first-trial', 'second': root/'second-trial'}
    clone_evidence(physics_directory, directories['physics'])
    for name, source_dir in zip(['first', 'second'], trials):
        clone_evidence(source_dir, directories[name])
    results = dict(physics=physics, control=control, first=proofs[0], second=proofs[1])
    records = {}
    for name, directory in directories.items():
        inputs = {'commit': target, 'source_commit': results[name]['commit'],
                  'method': 'Revalidate actual recorded source evidence against identical target implementation',
                  'actual_stage_exits': exits, 'actual_gpu_inventories': inventories,
                  'verifier_sha256': digest(Path(__file__)),
                  'control_verifier_sha256': digest(Path(__file__).with_name('verify_action_only_experts.py'))}
        record = {'status': 'PASS', 'key': fingerprint(inputs), 'inputs': inputs,
                  'result': results[name], 'verification_completed_at': utc(),
                  'artifacts': artifacts(directory), 'receipt': (directory/'receipt.json').relative_to(root).as_posix()}
        atomic(directory/'receipt.json', record)
        records[name] = record
    proof = {'format_version': 2, 'commit': target,
             'expert_interface': 'FIXED_ROBOT_JOINT_ACTION_TRAJECTORY',
             'checker_sha256': digest(target_folder/'feasibility_v2.py'),
             'components': dict(mechanics=mechanics, expert=expert),
             'physics': records['physics'], 'control': records['control'],
             'experts': [records['first'], records['second']],
             'scope': 'Actual independent cold robot-action experts; unchanged native mechanism evidence retains '
                      'its original revision/reset counts. Authored checkpoints are numeric assertions, '
                      'not measured phase completion or new standalone control runs.',
             'dream_evaluation': 'NOT_RUN'}
    path = root/'evidence/feasibility.json'
    atomic(path, proof)
    checker.check(path, target, target_folder)
    launcher = load(target_folder/'run.py', '_action_only_target_launcher')
    launcher.feasible(path, target)
    print('Sealed actual action-only evidence; exact target launcher gate passed:', path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', required=True, type=Path)
    args = parser.parse_args()
    seal(json.loads(args.config.read_text()))


if __name__ == '__main__':
    main()
