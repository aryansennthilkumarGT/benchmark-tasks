"""Seal real standalone physics plus control assertions from complete experts.

No simulator is launched. A config names existing actual exit files, GPU
inventories and evidence directories. Control results retain their distinct
recorded-expert method; no standalone control episodes or reset counts are added.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile

from engine import artifacts, atomic, digest, fingerprint, utc
from verify_expert_control_prefixes import verify, require
from stage_gate import require_no_interruption


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def seal(config, verify_only=False):
    root = Path(config['root']).resolve()
    folder = Path(config['folder']).resolve()
    commit = config['commit']
    require(subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=folder,
                                    text=True).strip() == commit, 'Task revision changed')
    required_exits = {'qualification', 'first', 'first_validation', 'second',
                      'second_validation', 'physics', 'control'}
    require(set(config['exit_files']) == required_exits, 'Missing execution/validation exit paths')
    require_no_interruption(root)
    exits = {}
    for name, value in config['exit_files'].items():
        path = Path(value)
        require_no_interruption(path.parent)
        require(path.read_text().strip() == '0', 'Nonzero or incomplete actual stage: '+name)
        exits[name] = {'path': str(path), 'sha256': digest(path)}
    require(config['gpu_inventories'], 'Actual producer GPU inventories required')
    gpu = []
    for value in config['gpu_inventories']:
        path = Path(value)
        content = path.read_text()
        require('L40S' in content and '565.57.01' in content,
                'Inventory does not document this fixed-driver L40S environment')
        gpu.append({'path': str(path), 'sha256': digest(path),
                    'scope': 'Actual producer inventory, not a new CPU-verifier GPU run'})
    sys.path.insert(0, str(folder))
    validator = load(folder/'validate_rollout.py', '_sealed_prefix_rollout_validator')
    directories = {'physics': root/'final-physics',
                   'control': Path(config['control_directory']).resolve(),
                   'first': root/'first-trial', 'second': root/'second-trial'}
    results = {}
    for name in ['first', 'second']:
        directory = directories[name]
        result = validator.inspect_log(directory, 'expert', config['run_limit'], commit, folder, seed=0)
        require(result == json.loads((directory/'validated-rollout.json').read_text()),
                'Existing validated expert summary differs from actual revalidation')
        results[name] = result
    physics = json.loads((directories['physics']/'results.json').read_text())
    definitions = json.loads((folder/'native-cases.json').read_text())
    expected = {(case['name'], repeat) for case in definitions['physics'] for repeat in (0, 1)}
    observed = {(case['name'], case['repeat']) for case in physics['cases']
                if case['status'] == 'PASS'}
    require(physics['kind'] == 'NATIVE_PHYSX_TESTS' and physics['mode'] == 'physics'
            and physics['commit'] == commit and physics['status'] == 'PASS'
            and physics['failed'] == 0 and observed == expected
            and physics['passed'] == physics['reset_count'] == len(physics['cases']) == len(expected),
            'Separate native mechanism suite is incomplete or mismatched')
    require(physics.get('camera_coverage') is True, 'Native camera geometry coverage missing')
    results['physics'] = physics
    control = json.loads((directories['control']/'results.json').read_text())
    # Recompute every assertion from actual source traces. Never trust a green
    # report alone, or substitute a fixture-initialized diagnostic for a cold expert.
    parent = root/'evidence'
    parent.mkdir(exist_ok=True)
    scratch = Path(tempfile.mkdtemp(prefix='control-recheck-', dir=parent))
    recomputed = verify(folder, [directories['first'], directories['second']], commit, scratch/'control')
    require(recomputed == control, 'Stored control report differs from real trace assertion verification')
    results['control'] = control
    if verify_only:
        print('READ-ONLY proof validation passed; no feasibility proof or receipts published.')
        return
    for directory in directories.values():
        require(directory.resolve().is_relative_to(root), 'Evidence directory escapes canonical root')
    records = {}
    pending = []
    for name in ['physics', 'control', 'first', 'second']:
        directory = directories[name]
        inputs = {'commit': commit, 'mode': 'expert' if name in ['first', 'second'] else name,
                  'method': ('Exact control assertions on two complete real experts; no new control runs'
                             if name == 'control' else 'Verify completed real standalone native evidence'),
                  'actual_stage_exits': exits, 'actual_producer_gpu_inventories': gpu,
                  'control_verifier_sha256': digest(Path(__file__).with_name('verify_expert_control_prefixes.py'))}
        key = fingerprint(inputs)
        inventory = artifacts(directory)
        receipt = directory/'receipt.json'
        if receipt.exists():
            old = json.loads(receipt.read_text())
            require(old['status'] == 'PASS' and old['key'] == key and old['inputs'] == inputs
                    and old['artifacts'] == inventory and old['result'] == results[name],
                    'Existing immutable receipt differs; create a new attempt instead of overwriting')
            records[name] = old
        else:
            record = {'status': 'PASS', 'key': key, 'inputs': inputs, 'result': results[name],
                      'verification_completed_at': utc(), 'artifacts': inventory,
                      'receipt': receipt.relative_to(root).as_posix()}
            records[name] = record
            pending.append((receipt, record))
    for path, record in pending:
        atomic(path, record)
    proof = {'commit': commit, 'physics': records['physics'], 'control': records['control'],
             'experts': [records['first'], records['second']],
             'scope': 'Genuine independent native mechanism suite and two complete cold SDK experts; '
                      'control predicates checked on their recorded default-reset prefixes',
             'standalone_control_executions_claimed': False,
             'dream_evaluation': 'NOT_RUN', 'billing_evidence': 'Separate actual provider receipts'}
    path = parent/'feasibility.json'
    if path.exists():
        require(json.loads(path.read_text()) == proof, 'Existing feasibility proof differs')
    else:
        atomic(path, proof)
    launcher = load(folder/'run.py', '_sealed_prefix_task_launcher')
    launcher.feasible(path, commit)
    print('Sealed real evidence; exact task feasibility verifier passed.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, required=True)
    parser.add_argument('--verify-only', action='store_true')
    args = parser.parse_args()
    seal(json.loads(args.config.read_text()), args.verify_only)


if __name__ == '__main__':
    main()
