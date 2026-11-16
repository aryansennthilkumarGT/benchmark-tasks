"""Verify actual saved experiment results and physical/scoring invariants."""
from pathlib import Path
import json,sys
D=Path(__file__).resolve().parent
x=json.loads((D/'toshiba/results/CONTACT_RESULTS.json').read_text());by={a['case']:a for a in x['cases']}
assert by['correct']['score']==1
assert all(a['score']<1 for n,a in by.items() if n!='correct')
assert all(a['score']==1 for a in x['sensitivity'])
assert next(a for a in x['geometry_sensitivity'] if a['authored_drive_top_m']==.007)['score']<1
for a in x['cases']+x['sensitivity']+x['geometry_sensitivity']:
 c=a['model_checks'];assert c['equality_constraints']==0 and c['tray_actuators']==0 and c['mocap_bodies']==0 and c['input_only_actuation'] and c['no_external_tray_force']
assert by['missing_drive']['output_rotation_rad']<.001
assert abs(by['correct']['input_rotation_rad']-by['correct']['output_rotation_rad'])<.25
assert by['wrong_phase']['before_drive']['tray_center_z_m']-by['correct']['before_drive']['tray_center_z_m']>.0015
assert not by['seized_wheels']['physical_predicates']['all_three_wheels_roll']
y=json.loads((D/'toshiba/results/YAM_ACCESS.json').read_text());assert y['total_hulls']==630 and all(z['valid'] for z in y['ik'])
assert all(z['summary']['sampled_poses']==65 and z['summary']['obstacle_collision_poses']==65 for z in y['cases'])
assert all(z['undersized_aperture_negative_detected'] for z in y['cases'])
f=json.loads((D/'faze4/results/CLOSURE_GATE.json').read_text());assert all(z['worst_gap_mm']<-.3 for z in f['fits'])
ind=json.loads((D/'faze4/results/INDEPENDENT_CHECKS.json').read_text());assert ind['best_shared_carrier_at_ring_fits']['minimum_hole_clearance_mm']<-.4
assert not any(z['full_planar_gate'] for z in ind['negative_states'])
for v in ['DIRECT','RAISED_TRANSIT']:
 u=json.loads((D/f'yubi/results/ACCESS_{v}.json').read_text());assert u['summary']['attempts']==64 and u['summary']['sampled_clear_paths']==0
# Scorer accepts physical observations only; a case-name spoof cannot affect it.
sys.path.insert(0,str(D/'toshiba'));from scoring import physical_score
for a in x['cases']:
 r=physical_score(a['before_drive'],a['after_drive'],a['input_rotation_rad'],a['output_rotation_rad']);assert r['score']==a['score']
print(json.dumps({'contact_positive':'PASS','incorrect_full_successes':0,'negative_controls':len(by)-1,'material_parameter_cases_passed':len(x['sensitivity']),'critical_geometry_sensitivity_cases':len(x['geometry_sensitivity']),'YAM_IK_endpoints':len(y['ik']),'YAM_sampled_poses':sum(a['summary']['sampled_poses'] for a in y['cases']),'YAM_obstacle_collision_poses':sum(a['summary']['obstacle_collision_poses'] for a in y['cases']),'full_YAM_installation':'NOT_DEMONSTRATED','full_task_advance':'NO'},indent=2))
