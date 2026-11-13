"""Run a real task controller against supplemental MuJoCo YAM/task contacts.

This CPU-only diagnostic never loads Isaac, runs Dream, uploads or provisions.
Object state is initialized once; afterward only ordinary robot position actions
are applied. There are no virtual grasps, task actuators or phase pose setters.
All results retain this backend's friction/contact limitations.
"""
from __future__ import annotations
import argparse,gzip,hashlib,importlib,json,os,shutil,subprocess,sys,time
import cpu_physics_checkpoint as checkpoint
from pathlib import Path
import xml.etree.ElementTree as ET
import mujoco,numpy as np
from cpu_yam_dynamics import add_robots,initialize_robot,measured,command_robot,robot_sources,indexes
from yam_arena.constants import SHOULDER,WRIST,GRIPPER,ARM_JOINTS,FINGER_JOINTS


_BOUND_FOLDER=None

def load(folder):
 global _BOUND_FOLDER
 if _BOUND_FOLDER is not None:raise ValueError('Run exactly one task per process; task module caches cannot cross source bindings')
 _BOUND_FOLDER=folder.resolve()
 for name in ['mechanism_cpu','feedback','scoring','audit_geometry','robot_clearance','source_identity']:
  if name in sys.modules:raise ValueError('Task namespace already loaded; start a fresh process')
 sys.path.insert(0,str(folder))
 return {name:importlib.import_module(name) for name in ['mechanism_cpu','feedback','scoring','audit_geometry','robot_clearance','source_identity']}


def export(spec,backend,subdivision=1):
 if subdivision not in (1,2,4,8):raise ValueError('Supported CPU physics refinements are1,2,4,8')
 root=ET.fromstring(backend.export(spec));root.find('option').set('timestep',str(spec['physics_dt']/subdivision))
 if root.find('actuator') is not None:raise ValueError('Task export unexpectedly contains diagnostic actuators')
 for geom in root.findall('.//geom'):
  if geom.get('contype','1')!='0' and geom.get('conaffinity','1')!='0':geom.set('contype','1');geom.set('conaffinity','7')
 return ET.tostring(add_robots(root,contact_timeconstant=.0022/subdivision),encoding='unicode')


def run(folder,out,max_actions=100,stop_after_phase=None,wall_seconds=600,subdivision=1,resume=False,checkpoint_every=50):
 folder=folder.resolve();harness_paths=[Path(__file__),Path(__file__).with_name('cpu_yam_dynamics.py'),Path(checkpoint.__file__)];harness_hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in harness_paths};out.mkdir(parents=True,exist_ok=resume)
 if resume and (out/'report.json').exists():raise ValueError('Diagnostic already finalized; do not relabel a finished run as resumed')
 source_status=subprocess.check_output(['git','status','--porcelain','--','.'],cwd=folder,text=True)
 initial_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=folder,text=True).strip()
 modules=load(folder);backend=modules['mechanism_cpu'];spec=json.loads((folder/'scene.json').read_text());plan=json.loads((folder/'controller.json').read_text());source=modules['source_identity'].runtime_hashes(folder)
 if not 1<=max_actions<=spec['run_limit']:raise ValueError('Requested actions exceed declared task limit')
 if stop_after_phase is not None and not 1<=stop_after_phase<=len(plan['phases']):raise ValueError('Requested prefix must include actual controller phases')
 if not 0.<wall_seconds<=3600.:raise ValueError('Bounded CPU wall limit must be0..3600seconds')
 xml=export(spec,backend,subdivision)
 if resume and (out/'model.xml').read_text()!=xml:raise ValueError('Checkpoint model source changed')
 if not resume:(out/'model.xml').write_text(xml)
 m=mujoco.MjModel.from_xml_string(xml);d=mujoco.MjData(m);backend.initialize(m,d,spec);initialize_robot(m,d)
 g=modules['audit_geometry'].geometry_module(folder);control=modules['feedback'].Controller(plan,spec);judge=modules['scoring'].Scorer(spec)
 ticks=round(1/spec['control_hz']/m.opt.timestep)
 if abs(ticks*m.opt.timestep-1/spec['control_hz'])>1e-10:raise ValueError('Physics/control clocks are not integral')
 velocity_dofs=[];velocity_limits=[]
 for ids in indexes(m).values():
  for n,jid in zip(ARM_JOINTS+FINGER_JOINTS,ids):
   cfg=GRIPPER if n in FINGER_JOINTS else SHOULDER if n in ARM_JOINTS[:3] else WRIST
   velocity_dofs.append(m.jnt_dofadr[jid]);velocity_limits.append(cfg['velocity'])
 velocity_dofs=np.asarray(velocity_dofs);velocity_limits=np.asarray(velocity_limits)
 start=time.monotonic();phase=None;error=None;actions=0;peak_task_depth=0.;peak_robot_depth=0.;max_tracking=0.;maximum_velocity_ratio=0.;completed=False;result=None;last_scored_time=None
 elapsed_before=0.;resumptions=0;prior_warnings={};trace_path=out/'frames.jsonl';state_path=out/'integration-checkpoint.npz';trace_hasher=hashlib.sha256()
 binding=dict(model_sha256=hashlib.sha256(xml.encode()).hexdigest(),runtime_inputs=source,harness_sources=harness_hashes,robot_sources=robot_sources(),source_commit=initial_commit,source_status=source_status,max_actions=max_actions,stop_after_phase=stop_after_phase,subdivision=subdivision)
 if resume:
  restored=checkpoint.restore(state_path,m,d,control,judge,binding);saved=restored['metadata']
  trace_hasher=checkpoint.recover_trace(trace_path,saved['trace_offset'],saved['trace_sha256'])
  actions=saved['actions'];phase=saved['phase'];peak_task_depth=saved['peak_task_depth'];peak_robot_depth=saved['peak_robot_depth'];max_tracking=saved['max_tracking'];maximum_velocity_ratio=saved['maximum_velocity_ratio'];last_scored_time=saved['last_scored_time'];elapsed_before=saved['elapsed_wall_seconds'];resumptions=saved['resumptions']+1;prior_warnings=saved['prior_warnings']
  for key,value in restored['warnings'].items():
   label=mujoco.mjtWarning(int(key)).name;prior_warnings[label]=prior_warnings.get(label,0)+value['number']
  result=judge.result
 if not 1<=checkpoint_every<=1000:raise ValueError('Checkpoint interval must be1..1000actions')
 def frame():
  nonlocal peak_task_depth,peak_robot_depth
  f=backend.observe(m,d,spec);f['schema']=1;q=measured(m,d)
  # A pad's solver penetration is not substituted for task/task integrity.
  f['max_penetration']=float(g.maximum_penetration(spec,f['bodies']));f['robot_clearance']=float(g.robot_clearance(modules['robot_clearance'].boxes(q,g),spec,f['bodies']))
  peak_task_depth=max(peak_task_depth,f['max_penetration'])
  for contact in d.contact[:d.ncon]:
   names=[mujoco.mj_id2name(m,mujoco.mjtObj.mjOBJ_GEOM,int(k)) or '' for k in contact.geom]
   if any(n.startswith(('left_','right_')) for n in names):peak_robot_depth=max(peak_robot_depth,max(0.,-float(contact.dist)))
  return f,q
 with trace_path.open('ab' if resume else 'wb') as trace:
  try:
   for index in range(actions,max_actions):
    if elapsed_before+time.monotonic()-start>wall_seconds:raise TimeoutError('Bounded CPU diagnostic wall deadline reached')
    f,q=frame();result=judge.update(f);last_scored_time=f['time']
    if result.failure:raise ValueError('Physical integrity scorer: '+result.failure)
    if control.done:completed=True;break
    if stop_after_phase is not None and control.index>=stop_after_phase:completed=True;break
    if phase!=control.index:
     phase=control.index;print(json.dumps(dict(phase=phase,label=plan['phases'][phase]['label'],actions=actions,simulation_seconds=float(d.time))),flush=True)
    command=control.step(q,f);command_robot(m,d,command);max_tracking=max(max_tracking,float(np.abs(command[:6]-q[:6]).max()),float(np.abs(command[7:13]-q[7:13]).max()))
    contacts=[]
    for ci,contact in enumerate(d.contact[:d.ncon]):
     names=[mujoco.mj_id2name(m,mujoco.mjtObj.mjOBJ_GEOM,int(k)) or '' for k in contact.geom]
     if any(n.startswith(('left_','right_')) for n in names):
      force=np.zeros(6);mujoco.mj_contactForce(m,d,ci,force)
      contacts.append(dict(geoms=names,distance_m=float(contact.dist),force_contact_frame=force.tolist(),position=contact.pos.tolist()))
    line=(json.dumps(dict(kind='SUPPLEMENTAL_MUJOCO_ROBOT_FRAME',phase=control.index,action=command.tolist(),robot_q=q.tolist(),frame=f,robot_contacts=contacts))+'\n').encode();trace.write(line);trace_hasher.update(line)
    for _ in range(ticks):
     mujoco.mj_step(m,d)
     maximum_velocity_ratio=max(maximum_velocity_ratio,float(np.max(np.abs(d.qvel[velocity_dofs])/velocity_limits)))
    actions+=1
    if actions%checkpoint_every==0:
     trace.flush();os.fsync(trace.fileno())
     metadata=dict(actions=actions,phase=phase,peak_task_depth=peak_task_depth,peak_robot_depth=peak_robot_depth,max_tracking=max_tracking,maximum_velocity_ratio=maximum_velocity_ratio,last_scored_time=last_scored_time,elapsed_wall_seconds=elapsed_before+time.monotonic()-start,resumptions=resumptions,prior_warnings=prior_warnings,trace_offset=trace.tell(),trace_sha256=trace_hasher.hexdigest())
     checkpoint.save(state_path,m,d,control,judge,binding,metadata)
   f,q=frame()
   if last_scored_time is None or f['time']>last_scored_time:result=judge.update(f)
   completed=bool(control.done or stop_after_phase is not None and control.index>=stop_after_phase)
   if result.failure:raise ValueError('Terminal physical integrity scorer: '+result.failure)
  except Exception as exc:error=type(exc).__name__+': '+str(exc)
 warnings=prior_warnings.copy()
 for i,row in enumerate(d.warning):
  if row.number:
   label=mujoco.mjtWarning(i).name;warnings[label]=warnings.get(label,0)+int(row.number)
 with trace_path.open('rb') as raw,gzip.open(out/'frames.jsonl.gz','wb') as compressed:shutil.copyfileobj(raw,compressed)
 same=modules['source_identity'].runtime_hashes(folder)==source and harness_hashes=={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in harness_paths}
 if not same:error='Task sources changed during diagnostic; evidence is stale'
 source_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=folder,text=True).strip()
 if source_commit!=initial_commit or subprocess.check_output(['git','status','--porcelain','--','.'],cwd=folder,text=True)!=source_status:
  same=False;error='Task source commit or working tree changed during integration'
 report=dict(kind='SUPPLEMENTAL_MUJOCO_ACTUATED_YAM_TASK_DIAGNOSTIC',engine=mujoco.__version__,declared_task_timestep=spec['physics_dt'],diagnostic_timestep=float(m.opt.timestep),physics_subdivision=subdivision,robot_contact_timeconstant=.0022/subdivision,robot_contact_solmix=1e6,isaac_executed=False,hardware_executed=False,dream_executed=False,synthetic_grasps=False,task_pose_writes_after_initialization=False,resumed_integration=bool(resumptions),resume_count=resumptions,checkpoint_restores_only_at_process_initialization=True,task_actuators=False,virtual_constraints=False,source_commit=source_commit,source_tree_dirty=bool(source_status),source_commit_is_exact=not bool(source_status),source_binding='WORKING_TREE_HASHES_ONLY' if source_status else 'CLEAN_COMMIT_AND_RUNTIME_HASHES',source_bound=same,runtime_inputs_sha256=source,robot_sources=robot_sources(),harness_sources=harness_hashes,model_sha256=hashlib.sha256(xml.encode()).hexdigest(),max_actions=max_actions,stop_after_phase=stop_after_phase,actions=actions,phase=control.index,phases=len(plan['phases']),seconds=float(d.time),elapsed_wall_seconds=elapsed_before+time.monotonic()-start,error=error,warnings=warnings,maximum_task_interference_m=peak_task_depth,maximum_raw_robot_contact_depth_m=peak_robot_depth,maximum_action_tracking_delta_rad=max_tracking,maximum_measured_velocity_to_sdk_limit_ratio=maximum_velocity_ratio,velocity_limit_violated=maximum_velocity_ratio>1.001,score=result.score if result else None,controller_done=control.done,requested_prefix_complete=completed,events=control.events,limitations=['MuJoCo, not the native Isaac/PhysX backend.','Official joint friction coefficients are not converted into Nm; authored Coulomb joint loss0.','Robot collision friction0.5 is an explicit diagnostic assumption; PhysX combination/contact behavior may differ.','Table/robot/task geometry included; camera hardware/room/lighting not modeled.','This does not establish native expert, hardware, model or reviewer success.'],passed=bool(completed and error is None and not warnings and same and maximum_velocity_ratio<=1.001))
 (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');return report

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--task-folder',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--max-actions',type=int,default=100);p.add_argument('--stop-after-phase',type=int);p.add_argument('--wall-seconds',type=float,default=600);p.add_argument('--physics-subdivision',type=int,choices=[1,2,4,8],default=1);p.add_argument('--resume',action='store_true');p.add_argument('--checkpoint-every',type=int,default=50);a=p.parse_args()
 r=run(a.task_folder,a.output,a.max_actions,a.stop_after_phase,a.wall_seconds,a.physics_subdivision,a.resume,a.checkpoint_every);print(json.dumps({k:v for k,v in r.items() if k not in ['robot_sources','runtime_inputs_sha256','events']},indent=2));raise SystemExit(0 if r['passed'] else 1)
