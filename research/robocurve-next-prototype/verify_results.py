"""Verify saved executed results, source invariants and observation-only grading."""
from pathlib import Path
import sys,json,numpy as np
D=Path(__file__).resolve().parent;sys.path.insert(0,str(D/'odri'))
from scoring import physical_score,numerical_audit
rows=json.loads((D/'odri/results/CONTROLS.json').read_text())
assert len(rows)==9 and rows[0]['experiment_pass']
assert all(r['physical_score']['score']==0 for r in rows[1:])
for r in rows:
 p=physical_score(r['observations'],r['ring_nodes_by_stage_mm'][-1],r['specification'])
 assert p==r['physical_score'] and numerical_audit(r['observations'])==r['numerical_audit']
 # Names cannot change the physical grade.
 changed=dict(r,case='correct');assert physical_score(changed['observations'],changed['ring_nodes_by_stage_mm'][-1],changed['specification'])==p
p=rows[0];obs=p['observations']
assert abs(obs[0]['force_on_foot_N'][1]-.009*9.80665)<.002
assert obs[0]['pin_contact_force_N']==0
assert max(abs(x['foot_shift_mm'][0]) for x in obs)<.45
assert any(abs(x['pin_contact_force_N'])>.05 for x in obs),'Guide pin must causally carry lateral load'
assert not any(x['numerical_domain_hit'] for x in obs)
audit=json.loads((D/'odri/results/SOURCE_AUDIT.json').read_text())
assert all(x['intersection_volume_mm3']<.01 for x in audit['source_STEP_overlap_tests'])
assert abs(audit['guide_pin_lateral_clearance_mm']-.4)<1e-6
assert audit['beam_gradient_max_error_N']<1e-5
poses=json.loads((D/'odri/results/POSE_AUDIT.json').read_text())
assert all(v<.01 for row in poses for v in row['foot_print_overlap_mm3'].values())
sens=json.loads((D/'odri/results/SENSITIVITY.json').read_text())
assert {x['modulus_MPa'] for x in sens}=={.5,2.}
for x in sens:assert x['numerical_audit']==numerical_audit(x['observations'])
y=json.loads((D/'odri/results/YAM_ACCESS.json').read_text());assert y['hulls_per_arm']==315 and len(y['cases'])==8
valid=[x for x in y['cases'] if x['support_IK']['valid'] and all(k['valid'] for k in x['tool_IK'])]
clear=[x for x in valid if all(not q['robot_obstacle'] and not q['self_collision'] and not q['tool_obstacle'] for q in x['samples'])]
assert len(valid)==2 and len(clear)==0
c=json.loads((D/'cello/results/LOAD_GATE.json').read_text());assert c['physical_gravity_torque_Nm'] is None
assert all(x['raw_frame_overlap_mm3']>1000 for x in c['overlap_tests'])
out=dict(nominal_source_section_coupon='PASS',negative_full_false_positives=0,negative_controls=8,
 material_range_passes=[x['modulus_MPa'] for x in sens if x['experiment_pass']],
 material_range_unresolved=[x['modulus_MPa'] for x in sens if not x['experiment_pass']],
 YAM_templates=len(y['cases']),YAM_valid_endpoint_templates=len(valid),YAM_complete_clear_paths=len(clear),
 full_YAM_acquisition='NOT DEMONSTRATED',full_assembly='NOT DEMONSTRATED',ready_for_full_implementation='NO')
(D/'VERIFICATION.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
