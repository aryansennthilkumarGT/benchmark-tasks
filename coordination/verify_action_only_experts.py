"""Verify two complete fixed-action experts and their actual numeric control checkpoints.

This launches no simulator and does not claim standalone native-case executions.
Authored checkpoints do not claim measured phase completion. Mechanism fixtures still run
separately. Source expert logs, traces and events remain untouched.
"""
import argparse
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import subprocess
import sys


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def completion_tick(case, phases, events, program):
    allowed = {'name', 'through_phase', 'through_label', 'max_steps', 'assertions'}
    require(not set(case)-allowed, 'Case contains fixture/custom setup')
    phase = case['through_phase']
    require(phases[phase]['label'] == case['through_label'], 'Case phase/label mismatch')
    planned = [p for p in program['checkpoints'] if p['source_phase'] == phase
               and p['label'] == case['through_label']]
    require(len(planned) == 1, 'Missing/ambiguous authored checkpoint')
    tick = planned[0]['post_action_frame_index']
    require(isinstance(tick, int) and not isinstance(tick, bool) and 0 < tick <= case['max_steps'],
            'Authored checkpoint exceeds case action limit')
    actual = [e for e in events if e.get('event') == 'SCRIPTED_ACTION_CHECKPOINT'
              and e.get('source_phase') == phase and e.get('label') == case['through_label']]
    require(len(actual) == 1, 'Missing/ambiguous actual authored-checkpoint event')
    event = actual[0]
    require(event.get('post_action_frame_index') == tick and event.get('action_index') == tick-1
            and abs(event.get('state_time', -1)-(tick-1)/20) < 1e-6,
            'Authored checkpoint event is off the actual action timeline')
    return tick


def verify_actions(actions, program):
    planned = program['actions']
    require(planned and program['control_hz'] == 20 and program['action_dim'] == 14,
            'Invalid authored action program')
    require(len(actions) <= len(planned)+program['terminal_hold_actions'],
            'Executed actions exceed authored program and fixed hold')
    for tick, row in enumerate(actions):
        require(row['t'] == tick and row['action'] == planned[min(tick, len(planned)-1)],
                'Executed robot action differs from fixed authored trajectory')


def policy_audit(path):
    import ast
    tree = ast.parse(path.read_text())
    forbidden = {'LATEST', 'EVALUATOR', 'runtime', 'evaluator', 'SPEC', 'write_root_pose_to_sim_index',
                 'write_joint_position_to_sim_index'}
    require(not any(isinstance(n, ast.Attribute) and n.attr in forbidden for n in ast.walk(tree)),
            'Expert source accesses privileged task state')
    require(not any(isinstance(n, (ast.Import, ast.ImportFrom))
                    and any(x in ast.unparse(n) for x in ('arena_runtime', 'feedback', 'importlib'))
                    for n in ast.walk(tree)), 'Expert imports a privileged controller/runtime')
    require(not any(isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
                    and n.func.id in {'eval', 'exec', '__import__', 'getattr'} for n in ast.walk(tree)),
            'Dynamic expert state access requires separate review')
    return digest(path)


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def verify(folder, trials, commit, output):
    require(__debug__, 'Native assertion checks require Python without optimization')
    folder = folder.resolve()
    require(len(trials) == 2, 'Exactly two independent complete experts required')
    current = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=folder, text=True).strip()
    require(current == commit, 'Task source revision differs')
    require(not subprocess.check_output(['git', 'status', '--porcelain', '--', '.'],
                                       cwd=folder, text=True).strip(), 'Task source is dirty')
    sys.path.insert(0, str(folder))
    validator = load(folder/'validate_rollout.py', '_control_prefix_rollout_validator')
    native = load(folder/'native_tests.py', '_control_prefix_native_assertions')
    cases = json.loads((folder/'native-cases.json').read_text())['control']
    require(cases and len({c['name'] for c in cases}) == len(cases), 'Missing/duplicate control cases')
    phases = json.loads((folder/'controller.json').read_text())['phases']
    program = json.loads((folder/'expert_joint_trajectory.json').read_text())
    policy_sha = policy_audit(folder/'expert.py')
    rows, sources, identities, logs = [], [], set(), set()
    for repeat, trial in enumerate(trials):
        trial = trial.resolve()
        proof_file = trial/'validated-rollout.json'
        proof = json.loads(proof_file.read_text())
        require(proof['mode'] == 'expert' and proof['score'] == 1 and proof['commit'] == commit,
                'Expert is incomplete, failed, or from another revision')
        require(proof.get('native_failure') is None, 'Expert has a native failure')
        revalidated = validator.inspect_log(trial, 'expert', proof['run_limit'], commit, folder, seed=0)
        require(revalidated == proof, 'Existing expert summary differs from full revalidation')
        require(proof['record_id'] not in identities, 'Expert record reused')
        identities.add(proof['record_id'])
        log = Path(proof['log']).resolve()
        require(log.is_relative_to(trial), 'Expert log escapes its trial')
        require(digest(log) == proof['log_sha256'], 'Expert log changed after validation')
        require(proof['log_sha256'] not in logs, 'Expert log reused')
        logs.add(proof['log_sha256'])
        official = json.loads(log.read_text())
        require(official['status'] == 'success' and not official.get('error'),
                'Official expert record is not successful')
        require(official['eval']['policy'] == 'rc_expert'
                and official['eval']['environment_revision'] == commit,
                'Wrong recorded policy or environment revision')
        require(official['stats']['total_steps'] == proof['steps'], 'Official action count differs')
        require(len(official['samples']) == 1, 'Mixed official trials')
        sample = official['samples'][0]
        require(sample['status'] == 'success' and not sample.get('error')
                and len(sample['epochs']) == 1 and sample['epochs'][0]['task_score'] == 1,
                'Official expert sample did not reach full score')
        require(len(sample['record_dirs']) == 1, 'Missing or mixed full trial records')
        record_dir = (trial/sample['record_dirs'][0]).resolve()
        require(record_dir.is_relative_to(trial), 'Full trial record escapes its trial')
        record_file = record_dir/'record.json'
        require(json.loads(record_file.read_text())['record_id'] == proof['record_id'],
                'Validated identity differs from actual record')
        action_streams = list(trial.glob('actions/*/*.jsonl'))
        require(len(action_streams) == 1, 'Missing or ambiguous executed-action stream')
        actions_file = action_streams[0]
        actions = [json.loads(line) for line in actions_file.read_text().splitlines()]
        require(actions[0].get('action_dim') == 14 and len(actions) == proof['steps']+1,
                'Incomplete real robot action record')
        for tick, action in enumerate(actions[1:]):
            require(action['t'] == tick and len(action['action']) == 14
                    and all(isinstance(v, (int, float)) and math.isfinite(v)
                            for v in action['action']), 'Invalid recorded robot action')
        verify_actions(actions[1:], program)
        events_path = trial/'expert-events.jsonl'
        events = [json.loads(line) for line in events_path.read_text().splitlines()]
        pending = {}
        for case in cases:
            tick = completion_tick(case, phases, events, program)
            pending.setdefault(tick, []).append(case)
        scorer = validator.load_scorer(folder)
        trace_path = trial/'native_frames.jsonl'
        initial = None
        count = 0
        completed = set()
        for line in trace_path.open():
            record = json.loads(line)
            require(record.get('kind') == 'NATIVE_SIMULATION_FRAME' and record.get('episode') == 1,
                    'Nonnative or mixed-reset trace')
            frame = record['frame']
            require(abs(frame['time'] - count/20) < 1e-5, 'Incomplete native action timeline')
            if initial is None:
                initial = frame
            result = scorer.update(frame)
            require(abs(result.score - record['result']['score']) < 1e-9, 'Native scorer mismatch')
            for case in pending.get(count, []):
                native.checks(case['assertions'], initial, frame, result)
                rows.append({'name': case['name'], 'repeat': repeat, 'status': 'PASS',
                             'source_record_id': proof['record_id'], 'control_steps': count,
                             'authored_checkpoint_input_time': (count-1)/20,
                             'post_action_frame_time': frame['time'],
                             'assertions': case['assertions'],
                             'evidence_method': 'Numeric assertions at authored checkpoints in a complete cold action-only expert'})
                completed.add(case['name'])
            count += 1
        require(count > 0 and count == proof['steps']+1,
                'Trace and validated expert action counts differ')
        require(result.success and result.score == 1 and result.failure is None,
                'Full expert trace does not end in success')
        require(completed == {c['name'] for c in cases}, 'A control case has no actual frame')
        sources.append({'record_id': proof['record_id'], 'trial': str(trial),
                        'validated_rollout_sha256': digest(proof_file),
                        'log_sha256': digest(log), 'native_trace_sha256': digest(trace_path),
                        'events_sha256': digest(events_path), 'steps': proof['steps'],
                        'record_sha256': digest(record_file), 'actions_sha256': digest(actions_file)})
    expected = {(c['name'], repeat) for c in cases for repeat in (0, 1)}
    require({(r['name'], r['repeat']) for r in rows} == expected, 'Incomplete assertion coverage')
    report = {'kind': 'NATIVE_CONTROL_ASSERTIONS_FROM_ACTION_ONLY_EXPERTS', 'mode': 'control',
              'commit': commit, 'status': 'PASS', 'passed': len(rows), 'failed': 0,
              'independent_expert_resets': 2, 'standalone_native_case_runs_claimed': False,
              'cases': rows, 'sources': sources,
              'native_cases_sha256': digest(folder/'native-cases.json'),
              'assertion_implementation_sha256': digest(folder/'native_tests.py'),
              'policy_source_sha256': policy_sha,
              'joint_trajectory_sha256': digest(folder/'expert_joint_trajectory.json'),
              'every_executed_action_matches_authored_trajectory': True,
              'authored_checkpoints_are_not_measured_phase_completion': True,
              'scope': 'Actual numeric predicates on two complete independent cold action-only experts; '
                       'no new standalone control episodes and no measured phase-completion claim. '
                       'Mechanism fixtures and clean reproduction remain separate.'}
    output.mkdir(parents=True, exist_ok=False)
    (output/'results.json').write_text(json.dumps(report, indent=2)+'\n')
    print(f'Verified {len(rows)} control assertion sets from two complete real experts; no GPU run.')
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--folder', type=Path, required=True)
    parser.add_argument('--trial', type=Path, action='append', required=True)
    parser.add_argument('--commit', required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    verify(args.folder, args.trial, args.commit, args.output)


if __name__ == '__main__':
    main()
