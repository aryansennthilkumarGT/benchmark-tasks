"""Check recorded evidence and reporting boundaries; no new physics trials."""
from collections import Counter
from pathlib import Path
import gzip
import hashlib
import json

D = Path(__file__).resolve().parent


def read(name):
    return json.loads((D / name).read_text())


root = read('odri/results/ROOT_CAUSE.json')
assert root['hulls_per_arm'] == 315 and len(root['cases']) == 8
assert root['distinct_support_configurations'] == 2
assert [r.get('identical_configuration_reused_from') for r in root['cases']] == [None, 0, 0, 0, None, 4, 4, 4]
assert root['registration_bounds_error_m'] < 1e-8
for case in root['cases']:
    hits = {r['hull']: r for r in case['base_collisions']}
    for name in ['tip_right:5', 'tip_right:8']:
        assert hits[name]['source_base_contains_robot_hull_vertices_mm']
for witness in read('odri/results/STRICT_SOLID_WITNESSES.json'):
    assert witness['strict_inside_witness']['distance_to_any_STEP_boundary_mm'] > .001
for facts in read('odri/results/KINEMATIC_FACTS.json'):
    for direction in facts['opening_travel_direction_world'].values():
        assert abs(direction[2]) > .999

support = read('odri/results/SUPPORT_GATE.json')
assert support['hulls_per_arm'] == 315
assert support['ready_self_collision_pairs'] == []
assert len(support['cases']) == support['tested_support_templates'] == 32
assert {r['axial_shift_mm'] for r in support['cases']} == {-3., -6.}
assert {r['roll_deg'] for r in support['cases']} == set(range(0, 360, 45))
assert len({tuple(r['origin_m']) for r in support['cases']}) == 2
counts = Counter(r['first_blocking_stage']['stage'] if r['first_blocking_stage']
                 else 'finite_support_samples_clear' for r in support['cases'])
assert counts == {'support_precontact': 16, 'support_approach_IK': 12,
                  'finite_support_samples_clear': 4}
for row in support['cases']:
    assert not row['accepted_complete_access']
    if row['first_blocking_stage'] is None:
        assert row['roll_deg'] == 90 and row['sampled_configs'] == 45
        assert row['IK']['approach']['valid'] and row['IK']['acquisition']['valid']
        assert row['target_check']['allowed_original_rim_contacts'] == 0

closure = read('odri/results/CLOSURE_CONTACTS.json')
assert len(closure) == 4
for row in closure:
    event = row['first_contact']
    assert 26.93 < event['first_collision_gap_mm'] < event['last_clear_gap_mm'] < 26.95
    assert event['contacts']['robot_source_pairs'] == [
        ['right', 'tip_left', 'tip_left:14', 'foot_structure.STL']]
    assert row['physical_purchase'].startswith('NOT PROVEN')

stages = read('odri/results/ONE_ANNULUS_STAGE_GATE.json')
assert not stages['source_scale_complete'] and len(stages['cases']) == 4
for row in stages['cases']:
    assert row['first_blocking_stage']['stage'] == 'tool_pregrasp'
    assert row['first_blocking_stage']['reason'] == 'IK not solved'
    place = row['placement_required_configuration']
    assert place['tool_IK']['valid']
    assert place['arm_arm_pair'] == ['gripper', 'gripper:0', 'link3', 'link3:1']
    assert len(place['tool_pairs']) == 3
    assert row['physical_tool_purchase'] == 'NOT PROVEN'
    assert row['physical_annulus_installation'] == 'NOT RUN'
    assert not row['complete_manipulation']

household = read('candidates/results/SOURCE_SCALE_GATES.json')
assert {r['id'] for r in household} == {'055', '091'}
for row in household:
    assert not row['complete_access'] and not row['real_scale_manufacturer_calibration']
    assert row['robot_reference']['total_hulls'] == 630
    assert len(row['asset_geometry']) == 2 and row['missing']
    assert row['access_stages']['acquisition'].startswith('NOT RUN')

roof = read('candidates/results/OPENTRONS_ACCESS.json')
assert len(roof['cases']) == 216 and roof['hulls_per_arm'] == 315
assert Counter(r['status'] for r in roof['cases']) == roof['survey_summary'] == {
    'OUTSIDE NECESSARY TCP SPHERE': 168, 'IK UNRESOLVED': 43, 'IK SOLVED': 5}
for row in roof['cases']:
    if row['status'] == 'IK SOLVED':
        check = row['known_geometry_collision_check']
        assert not (check['robot_source_pairs'] or check['arm_arm_pair'] or check['self_collision_pairs'])
assert not roof['complete_access'] and roof['physical_purchase'] == 'NOT PROVEN'

for item in read('sources/INPUTS.json'):
    raw = (D / 'sources' / item['local']).read_bytes()
    if 'decompressed_sha256' in item:
        raw = gzip.decompress(raw)
    assert hashlib.sha256(raw).hexdigest() == item.get('sha256', item.get('decompressed_sha256'))
for item in read('sources/official/MANIFEST.json'):
    assert hashlib.sha256((D / 'sources/official' / item['local']).read_bytes()).hexdigest() == item['sha256']

summary = read('SUMMARY.json')
assert summary['outcome'] == 'B' and summary['recommendation'] == 'STOP'
assert summary['complete_manipulation_paths'] == summary['new_contact_models'] == summary['new_physical_negative_controls'] == 0
assert not summary['physical_gripper_or_tool_purchase_proven']
assert not summary['stiffness_sweep_rerun']
print('PASS: recorded geometry/source/IK counts and STOP reporting boundaries agree.')
print('These assertions check evidence integrity, not physical negative controls.')
