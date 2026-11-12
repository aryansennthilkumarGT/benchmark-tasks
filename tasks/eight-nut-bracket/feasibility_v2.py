"""Self-contained receipts for genuine action-only experts and native mechanics.

Source revisions remain explicit. Reused native traces are never described as
new simulator runs; authored control checkpoints are not completion events.
"""
import ast
import hashlib
import json
from pathlib import Path


def require(value, message):
    if not value:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def component_hash(name, raw):
    if name == 'scene.json#excluding_instruction':
        # Only human/model wording differs. Every physical/scoring field remains exact.
        value=json.loads(raw)
        require('instruction' in value, 'Scene instruction is missing')
        value.pop('instruction')
        raw=json.dumps(value,sort_keys=True,separators=(',', ':')).encode()
    elif name.endswith('#phases'):
        value = json.loads(raw)['phases']
        raw = json.dumps(value, sort_keys=True, separators=(',', ':')).encode()
    elif name.endswith('#excluding_feasible'):
        tree = ast.parse(raw)
        tree.body = [n for n in tree.body if not isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
                     or n.name != 'feasible']
        raw = ast.dump(tree, include_attributes=False).encode()
    return hashlib.sha256(raw).hexdigest()


def mechanics_names(here):
    names = set()
    for path in here.rglob('*'):
        if not path.is_file():
            continue
        relative = path.relative_to(here).as_posix()
        if path.suffix in {'.usd', '.usda'} or (path.suffix == '.py'
                and path.name not in {'expert.py', 'run.py', 'feasibility_v2.py', 'cpu_launcher.py'}
                and not path.name.startswith('test_')):
            names.add(relative)
    names.update({'scene.json#excluding_instruction', 'native-cases.json', 'stack-lock.json',
                  'controller.json#phases', 'run.py#excluding_feasible'})
    return names


def verify_components(here, component):
    require(component.get('files'), 'Missing implementation fingerprints')
    for name, expected in component['files'].items():
        relative = name.split('#', 1)[0]
        path = (here/relative).resolve()
        require(path.is_relative_to(here), 'Implementation fingerprint escapes task folder')
        require(component_hash(name, path.read_bytes()) == expected,
                'Implementation differs from actual evidence: '+name)


def check(path, commit, here):
    require(__debug__, 'Native assertion checks require Python without optimization')
    path, here = Path(path).resolve(), Path(here).resolve()
    data = json.loads(path.read_text())
    require(data.get('format_version') == 2 and data['commit'] == commit,
            'Wrong feasibility format or target revision')
    require(data.get('expert_interface') == 'FIXED_ROBOT_JOINT_ACTION_TRAJECTORY',
            'State-independent full-score experts required')
    require(data['checker_sha256'] == sha(here/'feasibility_v2.py'), 'Proof checker changed')
    root = path.parent.parent
    records = [data['physics'], data['control'], *data['experts']]
    require(len(records) == 4, 'Two independent full-score experts required')
    for record in records:
        require(record['status'] == 'PASS' and record['inputs']['commit'] == commit,
                'Failed or mismatched verification receipt')
        receipt = (root/record['receipt']).resolve()
        require(receipt.is_relative_to(root), 'Receipt escapes proof root')
        require(json.loads(receipt.read_text()) == record, 'Immutable receipt changed')
        directory = receipt.parent
        inventory = {p.relative_to(directory).as_posix(): sha(p) for p in directory.rglob('*')
                     if p.is_file() and p.name != 'receipt.json'}
        require(inventory == record['artifacts'], 'Raw evidence changed or is missing')
    mechanics, expert = data['components']['mechanics'], data['components']['expert']
    require(set(mechanics['files']) == mechanics_names(here), 'Incomplete physical implementation fingerprints')
    require(set(expert['files']) == {'expert.py', 'expert_joint_trajectory.json', 'run.py#excluding_feasible'},
            'Incomplete expert implementation fingerprints')
    verify_components(here, mechanics)
    verify_components(here, expert)
    physics = data['physics']['result']
    require(physics['kind'] == 'NATIVE_PHYSX_TESTS' and physics['mode'] == 'physics'
            and physics['commit'] == mechanics['source_commit']
            and physics['status'] == 'PASS' and physics['failed'] == 0,
            'Actual native mechanism evidence is incomplete')
    definitions = json.loads((here/'native-cases.json').read_text())
    expected = {(case['name'], repeat) for case in definitions['physics'] for repeat in (0, 1)}
    observed = {(case['name'], case['repeat']) for case in physics['cases'] if case['status'] == 'PASS'}
    require(observed == expected and len(physics['cases']) == len(expected)
            and physics['passed'] == physics['reset_count'] == len(expected)
            and physics.get('camera_coverage') is True,
            'Native mechanism case/reset coverage is incomplete')
    identities = []
    for receipt in data['experts']:
        result = receipt['result']
        require(result['kind'] == 'REAL_INSPECT_ROLLOUT' and result['mode'] == 'expert'
                and result['score'] == 1 and result.get('native_failure') is None
                and result['commit'] == expert['source_commit'],
                'Actual action-only expert is incomplete or from another implementation')
        identities.append(result['record_id'])
    require(len(set(identities)) == 2, 'Independent expert identity reused')
    control = data['control']['result']
    require(control['kind'] == 'NATIVE_CONTROL_ASSERTIONS_FROM_ACTION_ONLY_EXPERTS'
            and control['commit'] == expert['source_commit'] and control['status'] == 'PASS'
            and control['failed'] == 0 and control['independent_expert_resets'] == 2
            and control['standalone_native_case_runs_claimed'] is False
            and control['every_executed_action_matches_authored_trajectory'] is True
            and control['authored_checkpoints_are_not_measured_phase_completion'] is True,
            'Unqualified control assertion method')
    require(control['policy_source_sha256'] == sha(here/'expert.py')
            and control['joint_trajectory_sha256'] == sha(here/'expert_joint_trajectory.json'),
            'Expert policy/program differs from actual executed actions')
    require([source['record_id'] for source in control['sources']] == identities,
            'Control predicates refer to other expert episodes')
    cases = {case['name']: case for case in definitions['control']}
    expected = {(name, repeat) for name in cases for repeat in (0, 1)}
    observed = set()
    for case in control['cases']:
        key = (case['name'], case['repeat'])
        require(key in expected and case['status'] == 'PASS', 'Wrong/failed control predicate set')
        require(case['source_record_id'] == identities[case['repeat']]
                and case['assertions'] == cases[case['name']]['assertions']
                and 0 < case['control_steps'] <= min(cases[case['name']]['max_steps'],
                    data['experts'][case['repeat']]['result']['steps']),
                'Control assertion provenance or numeric coverage differs')
        observed.add(key)
    require(observed == expected and len(control['cases']) == control['passed'] == len(expected),
            'Incomplete control predicate coverage')
    return data
