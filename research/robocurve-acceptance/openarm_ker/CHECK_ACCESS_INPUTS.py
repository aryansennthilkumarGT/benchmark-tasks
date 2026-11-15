"""Reuse the established full-YAM input gate; missing articulation never passes.
This is a source/input audit, not a collision path or mechanical trial.
"""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/'preflight'))
from access_core import Robot,evaluate

def main():
 p=argparse.ArgumentParser();p.add_argument('--results',type=Path,default=ROOT/'results');a=p.parse_args()
 summary=json.loads((a.results/'CAD_SUMMARY.json').read_text())
 geometry={}
 for item,key in zip(summary['files'],['static_KER_509_occurrences','actual_jig_BRep']):
  bounds=item['root_bounds_mm'][0]
  geometry[key]=dict(status='source_bound',source_ref='official-release2.0.0:'+item['sha256'],value=dict(units='m',bounds=dict(min=[x*.001 for x in bounds['min']],max=[x*.001 for x in bounds['max']]),scope='Native exported pose only; bounds are metadata, not collision proxies. Real BRep is retained externally.'))
 missing=['registered_articulated_KER_link_joint_definition_and_calibration_ready_pose','actual_M2_tool_shape_grasp_and_drive_interface']
 for key in missing:geometry[key]=dict(status='missing',source_ref=None,value=None)
 phases=['acquire_and_support_articulated_KER','seat_P1_both_sites','seat_J8_both_sites','rear_body_datum','actual_body_lock','M2_tool_approaches_and_fastening','release_hands_retained','left_right_completion']
 data=dict(candidate='OPENARM_KER',essential_phases=phases,required_geometry=list(geometry),geometry_inputs=geometry,
           required_force_inputs=['KER_mass_CG_joint_resistance_and_support','actual_jig_elastic_lock_contact','M2_driver_wrench_grip_and_friction'],force_inputs={},
           requires_site_inventory=True,required_sites=['P1_negative_X','P1_positive_X','J8_negative_X_pair','J8_positive_X_pair','rear_body_lock'],
           path=None,targets=None,static_obstacles=None,moving_body_sweep_envelopes=None,declared_contact_interfaces=[])
 robot=Robot();assert len(robot.hulls)==315
 result=evaluate(data,robot)
 result.update(input_gate_only=True,actual_candidate_phase_access_runs=0,full_robot_geometry_preserved=True,CAD_contact_diagnostics_are_not_a_path_test=True)
 assert result['input_status']=='BLOCKED_MISSING_INPUTS' and result['access_decision']=='NOT_CLEARED'
 (a.results/'ACCESS_INPUTS.json').write_text(json.dumps(data,indent=2)+'\n')
 (a.results/'ACCESS_INPUT_GATE.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(dict(input_status=result['input_status'],access_decision=result['access_decision'],robot_hulls_per_arm=len(robot.hulls),missing_inputs=len(result['missing_inputs']),force_groups_unbound=result['force_inputs_missing'],phase_access_runs=0),indent=2))
 return 2
if __name__=='__main__':raise SystemExit(main())
