#!/usr/bin/env python3
"""Validate saved execution/data/source evidence; not a task-feasibility test."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parent


def digest(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--verify-workspace-source-repos', action='store_true',
                    help='Additionally compare pinned original blobs in the existing /workspace clones.')
    args = ap.parse_args()
    run = json.loads((ROOT/'results/RUN_MANIFEST.json').read_text())
    assert run['all_commands_returned_expected_status']
    assert run['candidate_tests_blocked'] == 4 and run['candidate_partial_geometric_certificates'] == 0
    assert run['full_feasibility_passes'] == 0
    for row in run['commands']:
        assert row['returncode'] == row['expected_returncode']
        assert digest(ROOT/'results'/row['stdout_stderr_file']) == row['output_sha256']
    for name, expected in run['code_sha256'].items():
        assert digest(ROOT/name) == expected, ('code changed since execution', name)
    for name, expected in run['input_sha256'].items():
        assert digest(ROOT/'inputs'/name) == expected
    text = (ROOT/'results/UNIT_TEST_OUTPUT.txt').read_text()
    assert 'Ran 20 tests' in text and text.rstrip().endswith('OK')
    for name, count in [('N040', 19), ('N044', 16), ('N047', 14), ('N022', 15)]:
        d = json.loads((ROOT/'results'/f'{name}_ACCESS_RESULT.json').read_text())
        assert d['input_status'] == 'BLOCKED_MISSING_INPUTS' and d['access_decision'] == 'NOT_CLEARED'
        assert len(d['missing_inputs']) == count and not d['empirical_candidate_test']
        assert not d['physical_task_or_simulation_executed']
        assert d['robot_reference']['collision_hulls_per_arm'] == 315
        assert d['input_file_sha256'] == digest(ROOT/'inputs'/f'{name}.json')
    ref = json.loads((ROOT/'results/REFERENCE_FK_COMPARISON.json').read_text())
    assert ref['all_within_1e_minus_12'] and len(ref['cases']) == 6
    summary = json.loads((ROOT/'assets/YAM_SOURCE_MANIFEST.json').read_text())
    assert digest(ROOT/'assets/YAM_REFERENCE.json.gz') == summary['bundle_sha256']
    model = json.loads(gzip.decompress((ROOT/'assets/YAM_REFERENCE.json.gz').read_bytes()))
    assert sum(len(v['hulls']) for v in model['links'].values()) == 315
    assert model['pin'] == '0059d02a1a91bc6834c1d0846022891df0c78730'
    attempts = json.loads((ROOT/'sources/user-supplied-attempts.json').read_text())
    assert len(attempts) == 5 and all('403' in x.get('error', '') for x in attempts)
    current = json.loads((ROOT/'sources/pr-1986-current.json').read_text())
    assert current['embedded_PR_state'] == 'OPEN'
    decision = json.loads((ROOT/'results/FIRST_BUILD_DECISION.json').read_text())
    assert decision['first_small_CPU_prototype'] == 'N040' and not decision['native_GPU_authorized']
    for p in ROOT.glob('*.md'):
        assert all(line.rstrip() == line for line in p.read_text().splitlines())
        for link in re.findall(r'\]\(([^)]+)\)', p.read_text()):
            if link.startswith(('https://', 'http://', '#')):
                continue
            assert (p.parent/link.split('#')[0]).exists(), (p.name, link)
    verified = 0
    if args.verify_workspace_source_repos:
        locations = {'https://github.com/Kmberry1989/Elantra': '/workspace/final-two-evidence/hyundai-elantra',
                     'https://github.com/robocurve/benchmark-tasks': '/workspace/robocurve-official-research',
                     'https://github.com/MIT-Work-Analytics-Laboratory/US_AI_MAP': '/workspace/final-two-evidence/onet-mit',
                     'https://github.com/kairosiann/yam-isaac-lab-arena': '/workspace/yam-verification-source'}
        inspected = json.loads((ROOT/'sources/INSPECTED_SOURCE_MANIFEST.json').read_text())
        for x in inspected:
            blob = subprocess.check_output(['git', '-C', locations[x['repository']], 'show', x['commit']+':'+x['path']])
            assert hashlib.sha256(blob).hexdigest() == x['sha256']
            verified += 1
        for x in summary['source_manifest']:
            blob = subprocess.check_output(['git', '-C', '/workspace/yam-verification-source', 'show', model['pin']+':'+x['path']])
            assert hashlib.sha256(blob).hexdigest() == x['sha256']
            verified += 1
    out = {'execution_output_hashes_match': True, 'executed_code_and_input_hashes_match': True,
           'unit_controls_passed': 20, 'candidate_access_passes': 0, 'candidate_access_blocked': 4,
           'independent_FK_comparisons': 6, 'collision_hulls_per_arm': 315,
           'original_pinned_blob_hashes_rechecked': verified,
           'all_five_new_user_service_URLs_blocked_and_unread': True, 'local_document_links_resolve': True,
           'selected_small_CPU_prototype': 'N040', 'full_task_or_native_clearance': False,
           'scope': 'Evidence/data/logic validation only; no physical mechanism or candidate-specific complete path was tested.'}
    (ROOT/'results/VALIDATION_SUMMARY.json').write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
