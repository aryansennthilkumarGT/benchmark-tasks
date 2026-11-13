"""Force-limited second-engine cam-path fixture, not a robot demonstration.

Starts from the exact authored cradle reset. During the run the free
collet moves through MuJoCo contacts under explicit bounded PD wrench inputs.
No repeated pose writes, attachment, contact exclusions or virtual cam exist.
"""
import argparse,hashlib,json,math
from pathlib import Path
import xml.etree.ElementTree as ET
import mujoco,numpy as np
from cpu_contact_probe import model_xml
from motion import multiply,conjugate,interpolate,qangle
HERE=Path(__file__).resolve().parent


def clipped(v,limit):
 n=float(np.linalg.norm(v));return v*min(1.,limit/max(n,1e-12))


from convex_box_backend import geometric_overlap,mesh_boxes

def run(folder=HERE,speed=.003,strategy='tilted',refinement=1,box_backend='mesh'):
 from cpu_contact_probe import scorer
 spec=json.loads((folder/'scene.json').read_text());plan=json.loads((folder/'controller.json').read_text())
 from pxr import Usd,UsdPhysics
 stage=Usd.Stage.Open(str(folder/'assets/bench_nut_asset.usda'))
 material=UsdPhysics.MaterialAPI(stage.GetPrimAtPath('/Asset/Material'))
 xml=ET.fromstring(model_xml(spec,dict(dynamic_friction=material.GetDynamicFrictionAttr().Get())))
 xml.find('option').set('integrator','implicitfast');xml.find('option').set('timestep',str(spec['physics_dt']/refinement))
 if box_backend=='mesh':xml=mesh_boxes(xml)
 model=mujoco.MjModel.from_xml_string(ET.tostring(xml,encoding='unicode'));d=mujoco.MjData(model);mujoco.mj_forward(model,d)
 names=[b['name'] for a in spec['assemblies'] for b in a['bodies']]
 ids={n:mujoco.mj_name2id(model,mujoco.mjtObj.mjOBJ_BODY,n) for n in names};body=ids['collet']
 mass=model.body_mass[body];rows=[];peak=0.;maxforce=0.;maxtorque=0.;peak_state=None;geometry_peak=0.;geometry_samples=0
 judge=scorer(folder,spec);first_failure=None;frames=0;substep=0;last_frames=[];stride=round(.05/model.opt.timestep)
 def observe(released):
  nonlocal geometry_peak,geometry_samples,frames,first_failure
  overlap=geometric_overlap(model,d,body);geometry_peak=max(geometry_peak,overlap);geometry_samples+=1
  bodies={}
  for name,i in ids.items():
   v=np.zeros(6);mujoco.mj_objectVelocity(model,d,mujoco.mjtObj.mjOBJ_BODY,i,v,0);q=d.xquat[i]
   bodies[name]=dict(pos=d.xpos[i].tolist(),quat=[*q[1:],q[0]],linear=v[3:].tolist(),angular=v[:3].tolist())
  # No robot exists in this test rig. The fixture-contact sentinel prevents
  # hands-off credit while a diagnostic wrench is still actively applied.
  f=dict(schema=1,time=float(d.time),bodies=bodies,joints={},max_penetration=overlap,robot_clearance=.025 if released else 0.)
  result=judge.update(f);frames+=1
  last_frames.append(dict(time=float(d.time),released=released,score=result.score,stable_since=judge.stable,max_speed=max(float(np.linalg.norm(b['linear'])) for b in bodies.values()),max_spin=max(float(np.linalg.norm(b['angular'])) for b in bodies.values())))
  if len(last_frames)>20:last_frames.pop(0)
  if result.failure and first_failure is None:first_failure=dict(time=float(d.time),reason=result.failure,frame=f)
  return result
 result=observe(False);previous=plan['phases'][0]['nominal_bodies']['collet']
 indices=list(range(4,29)) if strategy=='tilted' else [4,5,28]
 for index in indices:
  target=plan['phases'][index]['nominal_bodies']['collet']
  stage_speed=speed if index>=7 else max(.02,plan['phases'][index]['speed'])
  duration=max(math.dist(previous['pos'],target['pos'])/stage_speed,qangle(previous['quat'],target['quat'])/.10,.10)
  for step in range(math.ceil((duration+.20)/model.opt.timestep)):
   fraction=min(1.,step*model.opt.timestep/duration)
   desired=(1-fraction)*np.array(previous['pos'])+fraction*np.array(target['pos']);desired_q=interpolate(previous['quat'],target['quat'],fraction)
   mujoco.mj_forward(model,d);velocity=np.zeros(6);mujoco.mj_objectVelocity(model,d,mujoco.mjtObj.mjOBJ_BODY,body,velocity,0)
   current_q=np.r_[d.xquat[body][1:],d.xquat[body][0]];dq=multiply(desired_q,conjugate(current_q))
   if dq[3]<0:dq=-dq
   length=np.linalg.norm(dq[:3]);rotation=dq[:3]*(2*math.atan2(length,dq[3])/length if length>1e-12 else 0.)
   force=clipped(900*(desired-d.xpos[body])-12*velocity[3:]-mass*np.array(spec['gravity']),5.)
   torque=clipped(.45*rotation-.004*velocity[:3],.10)
   d.xfrc_applied[body,:3]=force;d.xfrc_applied[body,3:]=torque
   maxforce=max(maxforce,float(np.linalg.norm(force)));maxtorque=max(maxtorque,float(np.linalg.norm(torque)))
   mujoco.mj_step(model,d);substep+=1;depth=max([0.]+[-float(c.dist) for c in d.contact[:d.ncon]])
   if depth>peak:
    contact=min(d.contact[:d.ncon],key=lambda c:c.dist);peak=depth
    peak_state=dict(time=float(d.time),pos=d.xpos[body].tolist(),quat_wxyz=d.xquat[body].tolist(),
                    contact_pair=[mujoco.mj_id2name(model,mujoco.mjtObj.mjOBJ_GEOM,int(i)) for i in contact.geom],
                    geometric_overlap_m=geometric_overlap(model,d,body))
   if substep%stride==0:
    mujoco.mj_forward(model,d);result=observe(False)
  mujoco.mj_forward(model,d);q=np.r_[d.xquat[body][1:],d.xquat[body][0]]
  rows.append(dict(phase=index,label=plan['phases'][index]['label'],time=float(d.time),
                   position_error_m=float(np.linalg.norm(d.xpos[body]-target['pos'])),rotation_error_rad=qangle(q,target['quat']),
                   pos=d.xpos[body].tolist(),quat=q.tolist()))
  previous=target
 d.xfrc_applied[:]=0.
 for _ in range(round(3./model.opt.timestep)):
  mujoco.mj_step(model,d);substep+=1
  if substep%stride==0:mujoco.mj_forward(model,d);result=observe(True)
 mujoco.mj_forward(model,d);q=np.r_[d.xquat[body][1:],d.xquat[body][0]];end=plan['phases'][28]['nominal_bodies']['collet']
 final_error=float(np.linalg.norm(d.xpos[body]-end['pos']));angle=qangle(q,end['quat'])
 positive=result.success and not result.failure and geometry_peak<=spec['penetration_limit'] and final_error<=.0006 and angle<=.025
 blocked=rows[-1]['position_error_m']>.001 and final_error>.001 and geometry_peak<=spec['penetration_limit']
 negative=(result.score==0. and result.failure=='penetration') or (blocked and not result.success and result.score<.75 and result.failure is None)
 return dict(kind='SUPPLEMENTAL_MUJOCO_FORCE_LIMITED_CAM_PATH_FIXTURE',engine=mujoco.__version__,isaac_executed=False,robot_executed=False,
             exact_scene_reset=True,pose_writes_during_run=False,force_cap_N=5.,torque_cap_Nm=.10,
             strategy=strategy,box_contact_backend=box_backend,geometry_identical_eight_corner_hulls=box_backend=='mesh',expected_outcome='valid_fixture_preassembly' if strategy=='tilted' else 'direct_entry_does_not_seat_validly',
             peak_force_N=maxforce,peak_torque_Nm=maxtorque,speed_m_s=speed,physics_dt_s=float(model.opt.timestep),
             input_sha256={n:hashlib.sha256((folder/n).read_bytes()).hexdigest() for n in ('scene.json','controller.json','probe_cam_path_cpu.py','cpu_contact_probe.py','scoring.py','convex_box_backend.py')},
             checks=rows,sampled_geometric_peak_overlap_m=geometry_peak,geometric_samples=geometry_samples,refinement_factor=refinement,
             peak_state=peak_state,peak_solver_contact_depth_m=peak,solver_contact_distance_is_not_obb_penetration=True,
             final_pos=d.xpos[body].tolist(),final_quat=q.tolist(),final_error_m=final_error,final_angle_rad=angle,
             diagnostic_scorer=dict(score=result.score,success=result.success,failure=result.failure,frames=frames,last_frames=last_frames),
             fixture_contact_sentinel_not_robot_clearance=True,first_failure=first_failure,
             physical_straight_entry_blocking_demonstrated=bool(blocked) if strategy=='straight' else None,
             limitations=['No YAM robot, grasp or actuation validation.','All wrench gains/caps are authored fixture inputs.','Geometry samples at20Hz; no continuous-overlap guarantee.','Primitive box backend produced false contact distances/crossing; exact convex-box backend is separately verified.'],
             passed=bool(positive if strategy=='tilted' else negative))
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--speed',type=float,default=.003)
 parser.add_argument('--strategy',choices=['tilted','straight'],default='tilted');parser.add_argument('--refinement',type=int,choices=[1,2,4,8],default=1);parser.add_argument('--box-backend',choices=['primitive','mesh'],default='mesh');args=parser.parse_args()
 if not math.isfinite(args.speed) or not 0<args.speed<=.02:raise SystemExit('Unsupported diagnostic speed')
 result=run(speed=args.speed,strategy=args.strategy,refinement=args.refinement,box_backend=args.box_backend);print(json.dumps(result,indent=2));raise SystemExit(0 if result['passed'] else 1)
