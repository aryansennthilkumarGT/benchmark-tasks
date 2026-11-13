"""Contact-driven positive/negative mechanism controls; not robot demonstrations.

Initialized released-latch cases are disclosed diagnostic starts. Opened-nose
extraction instead executes the complete physical rig opening before applying a
bounded wrench. No qpos/root/pose writes occur after stepping begins.
"""
import hashlib,json
from pathlib import Path
import mujoco,numpy as np
from mechanism_cpu import export,initialize,observe
from motion import multiply,conjugate
HERE=Path(__file__).resolve().parent


def step(model,data,peak):
 mujoco.mj_step(model,data)
 mujoco.mj_forward(model,data)  # Refresh integrated poses/velocities before feedback and contact audit.
 return max(peak,max([0.]+[-float(c.dist) for c in data.contact[:data.ncon]]))


def protocol(folder=HERE):
 spec=json.loads((folder/'scene.json').read_text());rows=[]
 for repeat in (0,1):
  for name in ['latched_door_resists','released_door_opens','closed_nail_normal_retention','closed_nail_axial_retention','opened_nail_wrench_extraction','opened_door_free_hold']:
   rig=name in ('opened_nail_wrench_extraction','opened_door_free_hold');m=mujoco.MjModel.from_xml_string(export(spec,rig));d=mujoco.MjData(m);initialize(m,d,spec)
   if name=='released_door_opens':
    for joint,value in [('lever_rotation',-2.1),('bail_rotation',2.0),('bail_extension',0.)]:
     i=mujoco.mj_name2id(m,mujoco.mjtObj.mjOBJ_JOINT,joint);d.qpos[m.jnt_qposadr[i]]=value
    mujoco.mj_forward(m,d)
   initial=observe(m,d,spec);peak=0.;displacement_peak=0.
   nail=mujoco.mj_name2id(m,mujoco.mjtObj.mjOBJ_BODY,'bent_brad');door=mujoco.mj_name2id(m,mujoco.mjtObj.mjOBJ_BODY,'nose_door')
   origin=np.array(initial['bodies']['bent_brad']['pos']);target=origin+[0,-.040,0];target_q=initial['bodies']['bent_brad']['quat']
   duration=10. if name=='opened_door_free_hold' else 9. if rig else 1.
   for _ in range(round(duration/spec['physics_dt'])):
    if rig:
     d.ctrl[0]=-min(2.1,max(0.,d.time-1.)*.7);d.ctrl[1]=min(1.9,max(0.,d.time-4.)*.7)
     if name=='opened_door_free_hold' and d.time>=8.:m.actuator_gainprm[:]=0.;m.actuator_biasprm[:]=0.
     if name=='opened_nail_wrench_extraction' and d.time>=8.:
      v=np.zeros(6);mujoco.mj_objectVelocity(m,d,mujoco.mjtObj.mjOBJ_XBODY,nail,v,0)
      force=.5*(target-d.xpos[nail])-.015*v[3:]+[0,0,spec['gravity'][2]*(-m.body_mass[nail])]
      force*=min(1.,.030/max(np.linalg.norm(force),1e-12));d.xfrc_applied[nail,:3]=force
      q=d.xquat[nail];error=multiply(target_q,conjugate([*q[1:],q[0]]))
      if error[3]<0:error=-error
      torque=.001*2*error[:3]-.00002*v[:3];torque*=min(1.,.0002/max(np.linalg.norm(torque),1e-12));d.xfrc_applied[nail,3:]=torque
    elif name in ('latched_door_resists','released_door_opens'):
     j=mujoco.mj_name2id(m,mujoco.mjtObj.mjOBJ_JOINT,'door_rotation');omega=d.qvel[m.jnt_dofadr[j]]
     d.xfrc_applied[door,3:]=[0,0,-float(np.clip(.02-.01*omega,-.02,.02))]
    else:
     velocity=np.zeros(6);mujoco.mj_objectVelocity(m,d,mujoco.mjtObj.mjOBJ_XBODY,nail,velocity,0)
     if name=='closed_nail_normal_retention':d.xfrc_applied[nail,:3]=[0,float(np.clip(-.03-.5*velocity[4],-.03,.03)),0]
     else:d.xfrc_applied[nail,:3]=[float(np.clip(.03-.5*velocity[3],-.03,.03)),0,0]
    peak=step(m,d,peak);displacement_peak=max(displacement_peak,float(np.linalg.norm(d.xpos[nail]-origin)))
   final=observe(m,d,spec);angle=final['joints']['door_rotation'];delta=np.array(final['bodies']['bent_brad']['pos'])-origin
   if name=='latched_door_resists':condition=angle<=.03
   elif name=='released_door_opens':condition=angle>=.4
   elif name=='closed_nail_normal_retention':condition=displacement_peak<=.003
   elif name=='closed_nail_axial_retention':condition=displacement_peak<=.012
   elif name=='opened_door_free_hold':condition=1.85<=angle<=1.95 and displacement_peak<=.005
   else:condition=angle>=1.85 and delta[1]<=-.035 and np.linalg.norm(np.array(final['bodies']['bent_brad']['pos'])-target)<=.002
   rows.append(dict(name=name,repeat=repeat,passed=bool(condition and peak<=spec['penetration_limit']),peak_contact_depth_m=peak,peak_nail_displacement_m=displacement_peak,initialization_is_diagnostic=name=='released_door_opens',test_rig_actuation=rig,external_wrench_fixture=name!='opened_door_free_hold',force_input='Bounded force/torque with explicit velocity damping to prevent destructive diagnostic impact; no manufacturer force claim.',final_door_angle_rad=angle,final_nail_delta_m=delta.tolist()))
 report=dict(scene_sha256=hashlib.sha256((folder/'scene.json').read_bytes()).hexdigest(),passive_export_sha256=hashlib.sha256(export(spec).encode()).hexdigest(),kind='SUPPLEMENTAL_MUJOCO_NOSE_JAM_MECHANISM_PROTOCOL',isaac_executed=False,robot_executed=False,grasps_validated=False,cases=rows,passed=all(r['passed'] for r in rows))
 print(json.dumps(report,indent=2));return report
if __name__=='__main__':raise SystemExit(0 if protocol()['passed'] else 1)
