"""Force-limited full fixture cycle; NOT a YAM expert or Isaac demonstration.

The door motor and guided crosspin wrench represent two diagnostic manipulators.
The pin is carried relative to the door, aligned through the actual hook mouth,
then guided while the lever draws the physical compliant bail past center. All
rig inputs have explicit caps. No task qpos/root pose is written after reset.
"""
import hashlib,json,math
from pathlib import Path
import mujoco,numpy as np
from mechanism_cpu import export,initialize,observe
from motion import rotate,conjugate,multiply,axis_quat
from scoring import Scorer
HERE=Path(__file__).resolve().parent


def limited(vector,cap):
 vector=np.asarray(vector,dtype=float);return vector*min(1.,cap/max(np.linalg.norm(vector),1e-12))


def pose(model,data,index):
 q=data.xquat[index];return dict(pos=data.xpos[index].copy(),quat=np.array([*q[1:],q[0]]))


def wrench(model,data,index,target,tool,kp,kv,force_cap,torque_cap,previous,dt):
 current=pose(model,data,index);v=np.zeros(6);mujoco.mj_objectVelocity(model,data,mujoco.mjtObj.mjOBJ_XBODY,index,v,0)
 # Dissipative measured-velocity damping. Finite-differencing a moving
 # passive parent reference feeds stiff-joint chatter back into the rig.
 force=kp*(np.asarray(target)-current['pos'])-kv*v[3:]+[0,0,model.body_mass[index]*9.81]
 error=multiply(tool,conjugate(current['quat']))
 if error[3]<0:error=-error
 data.xfrc_applied[index,:3]=limited(force,force_cap)
 data.xfrc_applied[index,3:]=limited(.01*2*error[:3]-.0002*v[:3],torque_cap)
 return np.asarray(target).copy()


def probe(folder=HERE):
 spec=json.loads((folder/'scene.json').read_text());xml=export(spec,True);m=mujoco.MjModel.from_xml_string(xml);d=mujoco.MjData(m);initialize(m,d,spec)
 ids={name:mujoco.mj_name2id(m,mujoco.mjtObj.mjOBJ_BODY,name) for name in ['nose_body','nose_door','latch_lever','draw_bail','bail_crosspin','bent_brad']}
 root=pose(m,d,ids['nose_body']);nail0=pose(m,d,ids['bent_brad']);nail_target=nail0['pos']+[0,-.04,0]
 saved_gain=m.actuator_gainprm.copy();saved_bias=m.actuator_biasprm.copy();pin_offset=pin_relative=None
 prev_pin=prev_nail=None;peak=0.;first_violation=None;rows=[];events=[];rest=spec['parameters']['draw_rest'];nominal=spec['parameters']['closed_pin_local'];judge=Scorer(spec)
 stage='OPEN_AND_CARRY';started=0.;stable=None;complete=False;lever_start=None;beta_reference=None
 def change(name):
  nonlocal stage,started,stable
  stage=name;started=float(d.time);stable=None;events.append(dict(stage=name,time=started))
 def settled(ok,seconds=.20):
  nonlocal stable
  if not ok:stable=None;return False
  if stable is None:stable=float(d.time)
  return d.time-stable>=seconds
 for step in range(round(32/spec['physics_dt'])):
  # mj_step integrates qpos/qvel after computing derived Cartesian arrays.
  # Refresh before external feedback; otherwise a stiff slider receives a
  # full-step delayed velocity/pose signal. Keep the implicitfast integrator.
  mujoco.mj_forward(m,d)
  t=d.time
  if t<9:
   d.ctrl[0]=-min(2.1,max(0.,t-1.)*.7);d.ctrl[1]=min(1.9,max(0.,t-4.5)*.7)
   if t>=8:m.actuator_gainprm[1,:]=0.;m.actuator_biasprm[1,:]=0.
  elif t<14:
   m.actuator_gainprm[1,:]=saved_gain[1];m.actuator_biasprm[1,:]=saved_bias[1];d.ctrl[1]=max(0.,1.9-(t-9.)*.5)
   if pin_offset is None:
    parent=pose(m,d,ids['nose_door']);pin=pose(m,d,ids['bail_crosspin']);pin_offset=rotate(conjugate(parent['quat']),pin['pos']-parent['pos']);pin_relative=multiply(conjugate(parent['quat']),pin['quat'])
    m.actuator_gainprm[0,:]=0.;m.actuator_biasprm[0,:]=0.
  else:
   if stage=='OPEN_AND_CARRY':change('PIN_OUTBOARD')
   if stage=='PIN_OUTBOARD' and t>=15:change('PIN_MOUTH')
   if stage=='PIN_RELEASED' and t-started>=1.:
    m.actuator_gainprm[1,:]=0.;m.actuator_biasprm[1,:]=0.;change('DOOR_RELEASED')
   if stage=='DOOR_RELEASED' and t-started>=1.:
    lever_start=observe(m,d,spec)['joints']['lever_rotation'];m.actuator_gainprm[0,:]=saved_gain[0];m.actuator_biasprm[0,:]=saved_bias[0];change('LEVER_CLOSE')
   if stage=='LEVER_CLOSE':
    d.ctrl[0]=min(0.,lever_start+(t-started)*.5);frame=observe(m,d,spec)
    good=abs(frame['joints']['lever_rotation'])<=.005 and judge.captured(frame['bodies']) and judge.past_center(frame['bodies'],frame['joints'])
    if settled(good,.25):
     m.actuator_gainprm[:]=0.;m.actuator_biasprm[:]=0.;change('RELEASED_RETENTION')
   if stage=='RELEASED_RETENTION':
    j=mujoco.mj_name2id(m,mujoco.mjtObj.mjOBJ_JOINT,'door_rotation');omega=d.qvel[m.jnt_dofadr[j]];d.xfrc_applied[ids['nose_door'],3:]=[0,0,-float(np.clip(.02-.01*omega,-.02,.02))]
    if t-started>=1.:complete=True;break
  if t>=8:
   prev_nail=wrench(m,d,ids['bent_brad'],nail_target+[0,-min(.12,max(0.,t-8.7)*.12),0],nail0['quat'],.5,.015,.030,.0002,prev_nail,spec['physics_dt'])
  if 9<=t<14:
   parent=pose(m,d,ids['nose_door']);point=parent['pos']+rotate(parent['quat'],pin_offset);tool=multiply(parent['quat'],pin_relative)
   prev_pin=wrench(m,d,ids['bail_crosspin'],point,tool,500.,1.,.50,.002,prev_pin,spec['physics_dt'])
  elif stage in ('PIN_OUTBOARD','PIN_MOUTH','PIN_SEAT'):
   eccentric=pose(m,d,ids['draw_bail'])['pos'];local=rotate(conjugate(root['quat']),eccentric-root['pos']);actual=pose(m,d,ids['bail_crosspin'])
   dy=nominal[1]-local[1]
   if abs(dy)>=rest:raise ValueError('Hook mouth outside draw-circle reach')
   beta_goal=.30 if stage=='PIN_OUTBOARD' else math.asin(dy/rest)
   if stage=='PIN_MOUTH':
    exact=local+rotate(axis_quat([0,0,1],beta_goal),[rest,0,0]);goal=root['pos']+rotate(root['quat'],exact);orientation=multiply(root['quat'],axis_quat([0,0,1],beta_goal))
    from motion import qangle
    if settled(np.linalg.norm(actual['pos']-goal)<=.00010 and qangle(actual['quat'],orientation)<=.003):change('PIN_SEAT')
   if stage=='PIN_SEAT':
    initial_x=local[0]+math.sqrt(rest*rest-dy*dy);point_local=np.array([max(nominal[0],initial_x-(t-started)*.004),nominal[1],0.]);beta=math.atan2(dy,point_local[0]-local[0])
   else:
    vector=rotate(conjugate(root['quat']),actual['pos']-eccentric);angle=math.atan2(vector[1],vector[0])
    if beta_reference is None:beta_reference=angle
    beta_reference+=float(np.clip(beta_goal-beta_reference,-.6*spec['physics_dt'],.6*spec['physics_dt']));beta=beta_reference;point_local=local+rotate(axis_quat([0,0,1],beta),[rest,0,0])
   point=root['pos']+rotate(root['quat'],point_local);tool=multiply(root['quat'],axis_quat([0,0,1],beta));prev_pin=wrench(m,d,ids['bail_crosspin'],point,tool,500.,1.,.50,.002,prev_pin,spec['physics_dt'])
   if stage=='PIN_SEAT':
    frame=observe(m,d,spec);goal=root['pos']+rotate(root['quat'],nominal)
    if settled(judge.captured(frame['bodies']) and np.linalg.norm(actual['pos']-goal)<=.00025):d.xfrc_applied[ids['bail_crosspin']]=0.;change('PIN_RELEASED')
  mujoco.mj_step(m,d)
  depth=max([0.]+[-float(c.dist) for c in d.contact[:d.ncon]]);peak=max(peak,depth)
  if depth>spec['penetration_limit'] and first_violation is None:first_violation=dict(time=float(d.time),depth_m=depth,contacts=[dict(a=mujoco.mj_id2name(m,mujoco.mjtObj.mjOBJ_GEOM,c.geom1),b=mujoco.mj_id2name(m,mujoco.mjtObj.mjOBJ_GEOM,c.geom2),depth=-float(c.dist)) for c in d.contact[:d.ncon] if c.dist<-spec['penetration_limit']])
  if step%round(.25/spec['physics_dt'])==0:rows.append(observe(m,d,spec))
 final=observe(m,d,spec);capture=judge.captured(final['bodies']);past=judge.past_center(final['bodies'],final['joints'])
 result=dict(kind='SUPPLEMENTAL_MUJOCO_FEEDBACK_GATED_SEQUENTIAL_NOSE_SERVICE',engine=mujoco.__version__,isaac_executed=False,robot_executed=False,grasps_validated=False,
  applied_test_rig_inputs=True,pin_force_cap_N=.50,pin_torque_cap_Nm=.002,door_torque_cap_Nm=.10,lever_torque_cap_Nm=.20,phase_events=events,final_stage=stage,completed=complete,
  probe_source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),scene_sha256=hashlib.sha256((folder/'scene.json').read_bytes()).hexdigest(),export_sha256=hashlib.sha256(xml.encode()).hexdigest(),
  peak_contact_depth_m=peak,first_integrity_violation=first_violation,checks=rows,final=final,pin_under_both_arms_after_rig_release=capture,past_center_after_rig_release=past,
  passed=bool(complete and peak<=spec['penetration_limit'] and capture and past and abs(final['joints']['door_rotation'])<=.005))
 print(json.dumps(result,indent=2));return result

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,help='Write normalized reference JSON only after a passing probe');args=p.parse_args();result=probe()
 if args.output and result['passed']:args.output.write_text(json.dumps(result,indent=2)+'\n')
 raise SystemExit(0 if result['passed'] else 1)
