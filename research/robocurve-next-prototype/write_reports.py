"""Generate the final numerical report exclusively from executed saved data."""
from pathlib import Path
import sys,json,math
D=Path(__file__).resolve().parent
rows=json.loads((D/'odri/results/CONTROLS.json').read_text());sens=json.loads((D/'odri/results/SENSITIVITY.json').read_text());yam=json.loads((D/'odri/results/YAM_ACCESS.json').read_text());audit=json.loads((D/'odri/results/SOURCE_AUDIT.json').read_text());cello=json.loads((D/'cello/results/LOAD_GATE.json').read_text())
b=rows[0];obs=b['observations'];p=b['physical_score']
lines=['# Executed CPU results','','**ODRI local contact coupon: nominal PASS. Full implementation: NO.** These are restricted planar, quasistatic simulation results, not measured hardware or a completed robot assembly.','','## Source/earliest gates','']
for x in cello['overlap_tests']:lines.append(f'- CELLO raw {"/".join(x["parts"])} solid overlap: **{x["raw_frame_overlap_mm3"]:.6f} mm³**.')
lines+=['- CELLO gravity torque/sag/friction window: **NOT ESTABLISHED**; full chain registration/mass/stiction were not resolved. No nine-control brake suite was run.','- Chefman: original squeeze/prong/cuff instruction reread; researcher asset audited; genuine cuff section/wire force remains unknown. No YAM or contact/lift success claimed.','', '## Source-CAD ODRI mechanism','']
for x in audit['source_STEP_overlap_tests']:lines.append(f'- Registered foot versus {x["file"]}: **{x["intersection_volume_mm3"]:.9f} mm³** initial solid overlap.')
lines += [f'- Beam-gradient independent finite-difference error: **{audit["beam_gradient_max_error_N"]:.3g} N**; rigid translation/rotation energy errors below 1e-10 N·mm.',f'- Maximum sampled signed-distance interpolation error: **{max(x["max_error_mm"] for x in audit["SDF_checks"]):.6f} mm**, over 3000 points/body/bank. Tessellation/2D approximation error is separate.',f'- Source pin-center lateral clearance: **{audit["guide_pin_lateral_clearance_mm"]:.6f} mm**; actual pin/slot contact is included. Pin-omitted results are not canonical.','', '## Free-foot positive test','',f'- Designer-reported moving assembly approximately 10 g: 9 g body plus 1 g over 12 tube elements. Initial own-weight center **{obs[0]["foot_shift_mm"]} mm**, norm **{math.hypot(*obs[0]["foot_shift_mm"]):.6f} mm**.',f'- Three 1 N probe displacements from own-weight equilibrium: **{p["moves_mm"]} mm**.',f'- Return errors after removing probes: **{p["return_errors_mm"]} mm**.',f'- Maximum lateral foot-center travel **{max(abs(x["foot_shift_mm"][0]) for x in obs):.6f} mm**; maximum pin normal reaction **{max(abs(x["pin_contact_force_N"]) for x in obs):.6f} N**.',f'- Worst equilibrium residual **{max(x["gradient_residual_N"] for x in obs):.6g} N**; worst contact penetration **{max(x["max_contact_penetration_mm"] for x in obs):.6f} mm**. No numerical domain boundary supports the positive case.','- Full STEP pose checks also find zero foot/leg-half solid overlap at all seven nominal cycle positions. Small loaded pin intersections from the declared penalty-contact model are recorded separately in POSE_AUDIT.json; they are not treated as hard-solid compatibility.','- The foot displacement and all ring nodes are solved from energy/contact balance. Only gravity/probe forces are supplied. No installed flag, neutral-position spring, attachment latch or commanded foot pose is used.','', '## Executed wrong cases','','|Case|Physical local score|Numerical audit|Main failed physical predicates|','|---|---:|---|---|']
for x in rows[1:]:
 failed=[k for k,v in x['physical_score'].items() if isinstance(v,bool) and not v]
 lines.append(f'|{x["case"]}|{x["physical_score"]["score"]:.0f}|{"resolved" if x["numerical_audit"]["passed"] else "invalid/unresolved"}|{", ".join(failed)}|')
lines += ['','All eight wrong cases reject full local credit. **Missing one ring and missing one bank can still move and return**; their full-grade rejection depends on actual inventory, not fabricated loss of function. This is why an eventual closed-device inspection method is required.','', 'Escaped numerical-domain cases and excessive-contact/stiffness cases are invalid-model diagnostics, not accurate hard-stop positions, measured force thresholds or physical hardware disqualifications. Damage and time-dependent return are not modeled.','', '## Material uncertainty','']
for x in sens:
 lines.append(f'- Authored E={x["modulus_MPa"]} MPa: physical score {x["physical_score"]["score"]:.0f}; numerical audit {x["numerical_audit"]}; full local experiment {"PASS" if x["experiment_pass"] else "UNRESOLVED/FAIL"}; 1 N displacement {x["physical_score"]["moves_mm"]} mm; return {x["physical_score"]["return_errors_mm"]} mm.')
lines += ['','These are uncertainty experiments, not identification of the installed silicone. Friction, hysteresis and nonlinear material behavior remain uncalibrated. The mechanical return result does not establish the optical voltage response.','', '## Stock-YAM access','', 'Two source-scale fixture placements and four ordinary-tweezer angles each were tested. Every template has 39 finite path samples and all 315 collision hulls per arm. Expected fingertip/foot-rim support contact alone is exempted.','', '|Foot center,m|Tool angle,deg|IK failures|Robot-obstacle samples|Self/arm-arm samples|Tool-obstacle samples|','|---|---:|---:|---:|---:|---:|']
valid=0
for x in yam['cases']:
 fail=int(not x['support_IK']['valid'])+sum(not a['valid'] for a in x['tool_IK']);valid+=int(fail==0);z=x['summary']
 lines.append(f'|{x["foot_center_m"]}|{x["tool_angle_deg"]}|{fail}|{z["robot_obstacle_poses"]}/39|{z["self_collision_poses"]}/39|{z["tool_obstacle_poses"]}/39|')
lines += ['',f'Only **{valid}** templates solve every endpoint; neither has a clear sampled path. Collisions evaluated at unsolved IK results are diagnostics, not executed reachable paths. **No complete stock-YAM acquisition/placement or loaded tool motion is demonstrated.** Sampling is not continuous swept certification. The remaining test is a genuine support grasp plus one annulus seating/release with full surrounding hardware; see NEXT_GATE.md.','', '## Decision','','Local source-section contact mechanism is implemented and executed. Axial capture, finite-rotation coupling, actual twelve-piece assembly, fork closure, loaded YAM tooling and optical function remain unverified. **READY FOR FULL IMPLEMENTATION: NO.** No GPU, Brev, Dream, paid evaluation, purchase or official submission occurred.','']
(D/'EXECUTED_TEST_RESULTS.md').write_text('\n'.join(lines))
# Standard scientific plot, using actual final-run coordinates and source sections.
sys.path.insert(0,'/workspace/robocurve-cpu-deps')
import numpy as np,matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from shapely.geometry import shape
from shapely.affinity import translate
section=next(x for x in json.loads((D/'odri/results/SECTIONS.json').read_text()) if x['x_mm']==2.123)
fig,axes=plt.subplots(1,3,figsize=(12,4))
for ax,index,title in zip(axes,[0,1,2],['Own weight','Upward1 N probe','After release']):
 shift=obs[index]['foot_shift_mm']
 for key,color in [('foot','tab:red'),('fixed','tab:blue')]:
  poly=shape(section[key]);poly=translate(poly,*shift) if key=='foot' else poly
  for q in (poly.geoms if hasattr(poly,'geoms') else [poly]):
   if q.is_empty:continue
   ax.fill(*q.exterior.xy,color=color,alpha=.35)
   for hole in q.interiors:ax.fill(*hole.xy,color='white')
 for nodes in b['ring_nodes_by_stage_mm'][index][:6]:
  pts=np.array(nodes);pts=np.r_[pts,pts[:1]];ax.plot(*pts.T,color='black',lw=2)
 ax.set_aspect('equal');ax.set_xlim(-15,15);ax.set_ylim(-15,15);ax.set_title(title);ax.set_xlabel('Y / mm');ax.set_ylabel('Z / mm')
fig.tight_layout();fig.savefig(D/'odri/results/CONTACT_STATES.png',dpi=150)
print('Reports and plot rendered from canonical executed outputs')
