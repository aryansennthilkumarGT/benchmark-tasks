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
 desired_velocity=(np.asarray(target)-previous)/dt if previous is not None else np.zeros(3)
 force=kp*(np.asarray(target)-current['pos'])+kv*(desired_velocity-v[3:])+[0,0,model.body_mass[index]*9.81]
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
 prev_pin=prev_nail=None;peak=0.;first_violation=None;rows=[];released=False;rest=spec['parameters']['draw_rest'];nominal=spec['parameters']['closed_pin_local'];judge=Scorer(spec)
 for step in range(round(24/spec['physics_dt'])):
  t=d.time
  if t<9:
   d.ctrl[0]=-min(2.1,max(0.,t-1.)*.7);d.ctrl[1]=min(1.9,max(0.,t-4.5)*.7)
   if t>=8:m.actuator_gainprm[1,:]=0.;m.actuator_biasprm[1,:]=0.
  elif t<14:
   m.actuator_gainprm[1,:]=saved_gain[1];m.actuator_biasprm[1,:]=saved_bias[1]
   d.ctrl[1]=max(0.,1.9-(t-9.)*.5)
   if pin_offset is None:
    parent=pose(m,d,ids['nose_door']);pin=pose(m,d,ids['bail_crosspin'])
    pin_offset=rotate(conjugate(parent['quat']),pin['pos']-parent['pos']);pin_relative=multiply(conjugate(parent['quat']),pin['quat'])
    m.actuator_gainprm[0,:]=0.;m.actuator_biasprm[0,:]=0.
  elif t<20:
   d.ctrl[1]=0.
   if t>=19:
    m.actuator_gainprm[1,:]=0.;m.actuator_biasprm[1,:]=0.
  elif t<23:
   m.actuator_gainprm[0,:]=saved_gain[0];m.actuator_biasprm[0,:]=saved_bias[0];d.ctrl[:]=[min(0.,-.8+(t-20.)*.5),0.]
  elif not released:
   m.actuator_gainprm[:]=0.;m.actuator_biasprm[:]=0.;d.xfrc_applied[ids['bail_crosspin']]=0.;released=True
  if t>=8:
   # External low-force support for the removed brad, not a robot grasp.
   prev_nail=wrench(m,d,ids['bent_brad'],nail_target+[0,-min(.12,max(0.,t-8.7)*.12),0],nail0['quat'],.5,.015,.030,.0002,prev_nail,spec['physics_dt'])
  if 9<=t<18:
   if t<14:
    parent=pose(m,d,ids['nose_door']);point=parent['pos']+rotate(parent['quat'],pin_offset);tool=multiply(parent['quat'],pin_relative)
   else:
    eccentric=pose(m,d,ids['draw_bail'])['pos'];local=rotate(conjugate(root['quat']),eccentric-root['pos'])
    if t<15:
     actual=pose(m,d,ids['bail_crosspin']);vector=rotate(conjugate(root['quat']),actual['pos']-eccentric);angle=math.atan2(vector[1],vector[0])
     # The first segment follows the outboard half-circle toward the mouth.
     beta=.30
     beta=angle+float(np.clip(beta-angle,-.6*spec['physics_dt'],.6*spec['physics_dt']))
     local_pin=local+rotate(axis_quat([0,0,1],beta),[rest,0,0])
    else:
     dy=nominal[1]-local[1]
     if abs(dy)>=rest:raise ValueError('No real draw-circle/hook-mouth intersection')
     beta=math.asin(dy/rest)
     if t<16:
      actual=pose(m,d,ids['bail_crosspin']);vector=rotate(conjugate(root['quat']),actual['pos']-eccentric);angle=math.atan2(vector[1],vector[0])
      beta=angle+float(np.clip(beta-angle,-.6*spec['physics_dt'],.6*spec['physics_dt']))
      local_pin=local+rotate(axis_quat([0,0,1],beta),[rest,0,0])
     else:
      initial_x=local[0]+math.sqrt(rest*rest-dy*dy)
      desired_x=max(nominal[0],initial_x-(t-16.)*.004)
      local_pin=np.array([desired_x,nominal[1],0.])
      beta=math.atan2(local_pin[1]-local[1],local_pin[0]-local[0])
    point=root['pos']+rotate(root['quat'],local_pin);tool=multiply(root['quat'],axis_quat([0,0,1],beta))
   prev_pin=wrench(m,d,ids['bail_crosspin'],point,tool,500.,1.,.50,.002,prev_pin,spec['physics_dt'])
  if 18<=t<23:d.xfrc_applied[ids['bail_crosspin']]=0.
  if released:
   j=mujoco.mj_name2id(m,mujoco.mjtObj.mjOBJ_JOINT,'door_rotation');omega=d.qvel[m.jnt_dofadr[j]]
   d.xfrc_applied[ids['nose_door'],3:]=[0,0,-float(np.clip(.02-.01*omega,-.02,.02))]
  mujoco.mj_step(m,d)
  depth=max([0.]+[-float(c.dist) for c in d.contact[:d.ncon]]);peak=max(peak,depth)
  if depth>spec['penetration_limit'] and first_violation is None:first_violation=dict(time=float(d.time),depth_m=depth,contacts=[dict(a=mujoco.mj_id2name(m,mujoco.mjtObj.mjOBJ_GEOM,c.geom1),b=mujoco.mj_id2name(m,mujoco.mjtObj.mjOBJ_GEOM,c.geom2),depth=-float(c.dist)) for c in d.contact[:d.ncon] if c.dist<-.0002])
  if step%round(.25/spec['physics_dt'])==0:rows.append(observe(m,d,spec))
 final=observe(m,d,spec);capture=judge.captured(final['bodies']);past=judge.past_center(final['bodies'],final['joints'])
 result=dict(kind='SUPPLEMENTAL_MUJOCO_SEQUENTIAL_PIN_CAPTURE_THEN_LEVER_CLOSE',engine=mujoco.__version__,isaac_executed=False,robot_executed=False,grasps_validated=False,
             applied_test_rig_inputs=True,pin_force_cap_N=.50,pin_torque_cap_Nm=.002,door_torque_cap_Nm=.10,lever_torque_cap_Nm=.20,
             pin_guidance_removed_s=18.,door_guidance_removed_s=19.,lever_guidance_restored_s=20.,probe_source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
             scene_sha256=hashlib.sha256((folder/'scene.json').read_bytes()).hexdigest(),export_sha256=hashlib.sha256(xml.encode()).hexdigest(),
             peak_contact_depth_m=peak,first_integrity_violation=first_violation,checks=rows,final=final,
             pin_under_both_arms_after_rig_release=capture,past_center_after_rig_release=past,
             passed=bool(peak<=spec['penetration_limit'] and capture and past and abs(final['joints']['door_rotation'])<=.005))
 print(json.dumps(result,indent=2));return result
if __name__=='__main__':raise SystemExit(0 if probe()['passed'] else 1)
