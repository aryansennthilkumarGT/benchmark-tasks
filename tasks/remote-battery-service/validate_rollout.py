"""Cross-check Inspect logs, native telemetry, actions, and every recorded camera frame."""
from __future__ import annotations
import importlib.util
import json
import math
from pathlib import Path
import re
import sys
from run_ledger import Incomplete, atomic, digest, within, read


def require(condition, message):
    if not condition:
        raise Incomplete(message)


def load_scorer(folder):
    spec = importlib.util.spec_from_file_location('evidence_task_scoring', Path(folder)/'scoring.py')
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module.Scorer(read(Path(folder)/'scene.json'))


def one_log(directory):
    logs = []
    for path in Path(directory).glob('*.json'):
        data = read(path)
        if 'eval' in data and 'samples' in data:
            logs.append((path, data))
    require(len(logs) == 1, f'Expected one finalized Inspect log, found {len(logs)}')
    return logs[0]


def inspect_log(directory, mode, run_limit, commit, folder=None, seed=0):
    directory = Path(directory).resolve()
    path, data = one_log(directory)
    require(data.get('version') == 3, 'Unsupported Inspect log schema; review adapter before accepting evidence')
    require(data['status'] == 'success' and not data.get('error'), 'Inspect evaluation did not finish successfully')
    spec, results, stats = data['eval'], data['results'], data['stats']
    require(spec['embodiment'] == 'yam_arena', 'Wrong embodiment')
    require(spec['seed'] == seed and spec['max_steps'] == run_limit, 'Seed/run limit mismatch')
    require(spec['environment_revision'] == commit, 'Evaluated task revision mismatch')
    policy = {'expert': 'rc_expert', 'dream': 'dream', 'smoke': 'yam_scripted'}[mode]
    require(spec['policy'] == policy, 'Wrong policy')
    require(results['total_trials'] == 1 and results['total_scenes'] == 1 and not results.get('errored_trials'),
            'Expected exactly one error-free trial')
    require(len(data['samples']) == 1, 'Unexpected scene count')
    sample = data['samples'][0]
    require(sample['status'] == 'success' and not sample.get('error'), 'Trial failed')
    require(len(sample['epochs']) == 1, 'Unexpected epoch count')
    score_name = 'success_at_end' if mode == 'smoke' else 'task_score'
    score = sample['epochs'][0].get(score_name)
    require(isinstance(score,(int,float)) and not isinstance(score,bool) and math.isfinite(score) and 0 <= score <= 1,
            'Missing finite numeric score')
    if mode in ('expert','smoke'):
        require(score == 1.0 and sample['termination_reasons'] == ['success'], 'Full-score physical success required')
    else:
        require(not spec['policy_config'].get('dry_run'), 'A model dry-run is not an evaluation')
    steps = stats['total_steps']
    require(isinstance(steps,int) and 0 < steps <= run_limit, 'Action count out of budget')
    record_dirs = sample.get('record_dirs',[])
    require(len(record_dirs) == 1 and record_dirs[0], 'Full trial record missing')
    record_dir = within(directory,directory/record_dirs[0])
    record = read(record_dir/'record.json')
    from inspect_robots.rollout import derive_seed
    configuration = record['configuration']
    if mode == 'dream':
        policy_record = configuration.get('policy', {})
        transcripts = sample.get('policy_transcripts', [])
        require(isinstance(policy_record, dict) and isinstance(transcripts, list),
                'Invalid recorded Dream metadata')
        require(policy_record.get('name', 'dream') == 'dream', 'Wrong recorded Dream policy')
        models = [value for value in (spec['policy_config'].get('model'),
                                      policy_record.get('checkpoint')) if value is not None]
        for transcript in transcripts:
            require(isinstance(transcript, dict), 'Invalid Dream transcript metadata')
            require(not transcript.get('dry_run'), 'A model dry-run is not an evaluation')
            if transcript.get('model') is not None:models.append(transcript['model'])
        require(models and all(model == 'dreamlabs/dream-1-beta' for model in models),
                'Unexpected or inconsistent Dream model')
    scene = configuration['scene']
    require(record['epoch'] == 0 and scene['id'] == sample['scene_id'], 'Record scene or epoch mismatch')
    reset_seed = derive_seed(seed, scene['init_seed'], record['epoch'])
    require(record['steps'] == steps and configuration['seed'] == seed, 'Record and log disagree')
    require(record['seed'] == configuration['trial_seed'] == reset_seed, 'Derived reset seed mismatch')
    require(record['record_id'] == sample['record_ids'][0], 'Record identity mismatch')
    actions = list(directory.glob('actions/*/*.jsonl'))
    require(len(actions) == 1, 'Executed-action stream missing or ambiguous')
    rows = [json.loads(line) for line in actions[0].read_text().splitlines()]
    require(rows[0].get('action_dim') == 14 and len(rows)-1 == steps, 'Action dimensions/count mismatch')
    for index, row in enumerate(rows[1:]):
        require(row['t'] == index and len(row['action']) == 14, 'Noncontiguous action timeline')
        require(all(isinstance(x,(int,float)) and math.isfinite(x) for x in row['action']), 'Nonfinite action')
    require((record_dir/'chunks.jsonl').is_file(), 'Policy chunk stream missing')
    if mode == 'dream':
        chunks = [json.loads(line) for line in (record_dir/'chunks.jsonl').read_text().splitlines()][1:]
        require(chunks and any(c.get('actions') for c in chunks), 'Dream action chunks missing')
        require(len(chunks)==record['chunks'], 'Record and policy chunk stream disagree')
        for chunk in chunks:
            for action in chunk.get('actions',[]):
                require(len(action)==14 and all(isinstance(x,(int,float)) and math.isfinite(x) for x in action),
                        'Invalid Dream action chunk')
        # A transcript is provider-dependent. Persist the full official record and chunks;
        # never manufacture a transcript if the pinned plugin does not expose one.
    frames = within(directory, directory/'frames'/Path(stats['frames_dir']).name)
    require(frames.is_dir(), 'Recorded observation frames missing')
    import numpy as np
    camera_counts = {}
    from inspect_robots.frames import _parse_frame_filename
    for file in frames.glob('*.npy'):
        ident = _parse_frame_filename(file.name)
        require(ident is not None, 'Unrecognized frame identity')
        trial, camera, step = ident
        camera_counts.setdefault((trial,camera),set()).add(step)
        array = np.load(file,allow_pickle=False)
        require(array.dtype == np.uint8 and array.shape == (176,320,3), 'Empty/wrong-size camera frame')
    require(len(camera_counts) == 3 and {k[1] for k in camera_counts} == {'top_cam','left_cam','right_cam'},
            'Missing or additional camera streams')
    require(all(indices == set(range(steps+1)) for indices in camera_counts.values()), 'Camera frames dropped')
    terminal = None
    if folder is not None:
        scorer = load_scorer(folder)
        trace_path = directory/'native_frames.jsonl'
        require(trace_path.is_file(), 'Native telemetry missing')
        count, previous = 0, None
        with trace_path.open(encoding='utf-8') as trace_stream:
            for line in trace_stream:
                row = json.loads(line)
                require(row.get('kind') == 'NATIVE_SIMULATION_FRAME' and row.get('episode') == 1,
                        'Mixed reset episodes or nonnative trace')
                frame = row['frame']
                if previous is not None:
                    require(abs(frame['time']-previous-0.05)<1e-5, 'Native frame timeline discontinuity')
                else:
                    require(abs(frame['time']) < 1e-8, 'Trace lacks reset frame')
                previous = frame['time']; count += 1
                terminal = scorer.update(frame)
                require(abs(terminal.score-row['result']['score']) < 1e-9, 'Scorer replay mismatch')
        require(count == steps+1, 'Native trace and actions disagree')
        require(terminal is not None and abs(terminal.score-score)<1e-9, 'Native terminal score disagrees with Inspect')
        if mode == 'expert':
            require(terminal.success and not terminal.failure, 'Expert failed native terminal conditions')
    summary = {'kind':'REAL_INSPECT_ROLLOUT', 'mode':mode, 'score':score, 'steps':steps, 'run_limit':run_limit,
               'seed':seed, 'reset_seed':reset_seed, 'commit':commit, 'record_id':record['record_id'], 'log':str(path),
               'log_sha256':digest(path), 'simulated_seconds':steps/20, 'duration_s':stats['duration_s'],
               'frames':str(frames), 'camera_streams':3, 'native_failure':getattr(terminal,'failure',None)}
    return summary


def public_text(folder):
    folder = Path(folder)
    task = read(folder/'task.json')
    required = {'title','category','instruction','setup','scoring','run_limit','fidelity','scores','media'}
    require(required <= task.keys(),'Missing required task.json fields')
    require(len(task['fidelity'])<=500,'Fidelity field exceeds the task-board 500-character limit')
    require(task['category'] in {'Impact on jobs','Impact on AI timelines','Safety and alignment','Societal relevance','Other'},
            'Unknown category')
    text = '\n'.join(str(v) for v in task.values())
    require(not re.search(r'(?i)aryan|senthil|georgia\s*tech|doubling\s*time|T-06|[A-Z]:[\\/]|/home/|/Users/',text),
            'Public task metadata contains identifying text/path')
    return {'required_fields':'PASS','public_text_scan':'PASS','visual_review':'REQUIRED_AFTER_RENDER'}


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--directory',required=True,type=Path)
    parser.add_argument('--mode',required=True,choices=['smoke','expert','dream'])
    parser.add_argument('--limit',required=True,type=int)
    parser.add_argument('--commit',required=True)
    parser.add_argument('--folder',type=Path)
    parser.add_argument('--seed',type=int,default=0)
    args=parser.parse_args()
    atomic(args.directory/'validated-rollout.json',inspect_log(args.directory,args.mode,args.limit,args.commit,args.folder,args.seed))
