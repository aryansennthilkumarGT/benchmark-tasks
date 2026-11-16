"""CPU-only free tray/carrier with actual contact-driven input/output coupling.
No output actuator, gear-ratio equality, pose latch, grasp weld or state-triggered capture.
Dimensions are EXPLICIT representative parameters, not manufacturer CAD.
"""
from pathlib import Path
import argparse,json,sys,hashlib
sys.path.insert(0,'/workspace/robocurve-cpu-deps')
import numpy as np
from scipy.spatial import ConvexHull
import mujoco
from scoring import physical_score
D=Path(__file__).resolve().parent
P=json.loads((D/'parameters.json').read_text())

def build(case,mu=.4,mass=.70):
 meshes=[]
 def sector(name,r0,r1,a0,a1,z0,z1):
  # Each narrow annular trapezoid is convex. Concave annulus is never convex-hulled whole.
  v=[[r*np.cos(a),r*np.sin(a),z] for z in [z0,z1] for r,a in [(r0,a0),(r1,a0),(r1,a1),(r0,a1)]]
  meshes.append(f'<mesh name="{name}" vertex="'+ ' '.join(f'{q:.12g}' for x in v for q in x)+'"/>')
  return f'<geom name="{name}" type="mesh" mesh="{name}" mass=".0007"/>'
 def ring(name,r0,r1,z0,z1,n=24):return ''.join(sector(name+str(k),r0,r1,k*2*np.pi/n,(k+1)*2*np.pi/n,z0,z1) for k in range(n))
 floor='<geom name="floor" type="plane" size=".30 .25 .01" friction=".4 .0001 .00001"/>'
 floor+=ring('recesslip',P['floor_recess_radius_m'],.20,0,P['floor_recess_depth_m'],48)
 floor+='<geom name="left_wall" type="box" size=".20 .005 .12" pos="0 .18 .12"/><geom name="right_wall" type="box" size=".20 .005 .12" pos="0 -.18 .12"/><geom name="rear_wall" type="box" size=".005 .18 .12" pos=".20 0 .12"/>'
 drive='<body name="drive"><joint name="drive_axis" type="hinge" axis="0 0 1" damping=".00005"/>'
 drive+='<geom name="shaft" type="cylinder" size=".005 .004" pos="0 0 .004" mass=".005"/>'
 if case!='missing_drive':
  for k in range(3):
   center=k*2*np.pi/3
   for j in range(4):
    half=P['drive_arm_half_angle_deg'];a0=center+np.deg2rad(-half+j*half/2);a1=a0+np.deg2rad(half/2)
    drive+=sector(f'drivekey{k}_{j}',P['drive_arm_inner_radius_m'],P['drive_arm_outer_radius_m'],a0,a1,P['drive_arm_bottom_m'],P['drive_arm_top_m'])
 drive+='</body>'
 carrier=''
 if case!='missing_carrier':
  offset=.025 if case=='displaced_carrier' else 0
  carrier=f'<body name="carrier" pos="{offset} 0 {P["wheel_radius_m"]}"><freejoint name="carrier_free"/>'
  carrier+=ring('carrier_centre',.019,.024,-.002,.002,24)
  for k in range(3):
   a=2*np.pi*k/3;R=P['wheel_orbit_radius_m']
   carrier+=f'<geom name="carrier_arm{k}" type="box" size=".038 .0015 .002" pos="{.062*np.cos(a)} {.062*np.sin(a)} 0" euler="0 0 {a}" mass=".004"/>'
   if case=='missing_wheel' and k==0:continue
   wheeljoint='' if case=='seized_wheels' else f'<joint name="wheel_axis{k}" type="hinge" axis="1 0 0" damping=".000002" frictionloss=".000001"/>'
   carrier+=f'<body name="wheel{k}" pos="{R*np.cos(a)} {R*np.sin(a)} 0" euler="0 0 {a}">{wheeljoint}<geom name="wheel{k}" type="cylinder" size="{P["wheel_radius_m"]} {P["wheel_half_width_m"]}" euler="0 1.5707963267948966 0" mass=".005"/></body>'
  carrier+='</body>'
 yaw=np.pi/3 if case=='wrong_phase' else 0
 flip=np.pi if case=='inverted_tray' else 0
 # Initially unengaged and unsupported,30mm above the nominal seated tray centre.
 tray=f'<body name="tray" pos=".0006 -.0005 .0445" euler="{flip} 0 {yaw}"><freejoint name="tray_free"/><geom name="glass" type="cylinder" size="{P["tray_radius_m"]} {P["tray_thickness_m"]/2}" mass="{mass}"/>'
 for k in range(3):
  c=(k*120+60)*np.pi/180
  for j in range(4):
   half=P['glass_lug_half_angle_deg'];a0=c+np.deg2rad(-half+j*half/2);a1=a0+np.deg2rad(half/2)
   tray+=sector(f'glasslug{k}_{j}',P['glass_lug_inner_radius_m'],P['glass_lug_outer_radius_m'],a0,a1,-P['tray_thickness_m']/2-P['glass_lug_height_m'],-P['tray_thickness_m']/2)
 tray+='</body>'
 support=''
 if case=='held_proud':
  for k,y in enumerate([-.07,.07]):support+=f'<body name="external_hand{k}" pos="-.10 {y} .024"><geom name="external_hand{k}" type="box" size=".025 .015 .002"/></body>'
 xml=f'''<mujoco model="representative_microwave_contact"><compiler angle="radian"/><option timestep="{P['timestep_s']}" gravity="0 0 -9.80665" integrator="implicitfast" solver="Newton" iterations="80" tolerance="1e-10" cone="elliptic"/><size nconmax="2000" njmax="6000"/><default><geom condim="4" friction="{mu} .00001 .000001" solref=".004 1" solimp=".95 .99 .001"/></default><asset>{''.join(meshes)}</asset><worldbody>{floor}{drive}{carrier}{tray}{support}</worldbody><actuator><velocity name="drive_motor" joint="drive_axis" kv=".03" ctrllimited="true" ctrlrange="-2 2" forcelimited="true" forcerange="-.04 .04"/></actuator></mujoco>'''
 return xml

def measure(m,d):
 tid=mujoco.mj_name2id(m,mujoco.mjtObj.mjOBJ_BODY,'tray');R=d.xmat[tid].reshape(3,3)
 z=float(d.xpos[tid,2]);xy=float(np.linalg.norm(d.xpos[tid,:2]));tilt=np.arccos(np.clip(R[2,2],-1,1));angle=np.arctan2(R[1,0],R[0,0]);wheels=set();external=0;keycontacts=0;normals={}
 for i in range(d.ncon):
  c=d.contact[i];n1=mujoco.mj_id2name(m,mujoco.mjtObj.mjOBJ_GEOM,c.geom1) or '';n2=mujoco.mj_id2name(m,mujoco.mjtObj.mjOBJ_GEOM,c.geom2) or '';names=[n1,n2]
  force=np.zeros(6);mujoco.mj_contactForce(m,d,i,force)
  if 'glass' in names:
   for n in names:
    if n.startswith('wheel'):wheels.add(n);normals[n]=normals.get(n,0)+float(force[0])
    if n.startswith('external_hand'):external+=1
  if any(n.startswith('drivekey') for n in names) and any(n.startswith('glasslug') for n in names):keycontacts+=1
 wheelangles={}
 for k in range(3):
  ji=mujoco.mj_name2id(m,mujoco.mjtObj.mjOBJ_JOINT,'wheel_axis'+str(k))
  if ji>=0:wheelangles['wheel'+str(k)]=float(d.qpos[m.jnt_qposadr[ji]])
  elif mujoco.mj_name2id(m,mujoco.mjtObj.mjOBJ_BODY,'wheel'+str(k))>=0:wheelangles['wheel'+str(k)]=0.0 # fixed relative marker for physically jammed axle
 return dict(wheel_angles_rad=wheelangles,tray_center_z_m=z,radial_offset_m=xy,tilt_deg=float(np.rad2deg(tilt)),tray_yaw_rad=float(angle),wheel_contacts=sorted(wheels),wheel_normal_force_N=normals,external_support_contacts=external,key_contacts=keycontacts)

def run(case,mu=.4,mass=.7,save_xml=False):
 xml=build(case,mu,mass);m=mujoco.MjModel.from_xml_string(xml);d=mujoco.MjData(m)
 assert m.neq==0,'No equality constraints allowed'
 assert m.nmocap==0,'No kinematic output carrier allowed'
 drivejid=mujoco.mj_name2id(m,mujoco.mjtObj.mjOBJ_JOINT,'drive_axis')
 assert m.nu==1 and int(m.actuator_trnid[0,0])==drivejid,'Only input shaft may be actuated'
 trayjoint=mujoco.mj_name2id(m,mujoco.mjtObj.mjOBJ_JOINT,'tray_free');tv=m.jnt_dofadr[trayjoint]
 for _ in range(round(1.5/m.opt.timestep)):mujoco.mj_step(m,d)
 before=measure(m,d);trace=[];driveidx=mujoco.mj_name2id(m,mujoco.mjtObj.mjOBJ_JOINT,'drive_axis');qd=m.jnt_qposadr[driveidx]
 startdrive=float(d.qpos[qd]);last=before['tray_yaw_rad'];trayturn=0
 for k in range(round(20/m.opt.timestep)):
  d.ctrl[0]=.8;mujoco.mj_step(m,d)
  if np.any(d.qfrc_applied[tv:tv+6]):raise RuntimeError('No external tray force allowed')
  if k%100==0:
   obs=measure(m,d);a=obs['tray_yaw_rad'];delta=np.arctan2(np.sin(a-last),np.cos(a-last));trayturn+=delta;last=a;trace.append(dict(time_s=float(d.time),drive_rad=float(d.qpos[qd]),tray_unwrapped_rad=trayturn,**obs))
  if d.qpos[qd]-startdrive>=7.0:break
 after=measure(m,d);driveturn=float(d.qpos[qd]-startdrive)
 # Independent observable score: released seating is measured BEFORE drive so the
 # validation motor cannot repair an initially proud assembly and disguise it.
 measured=physical_score(before,after,driveturn,trayturn,2*P['wheel_radius_m']+P['tray_thickness_m']/2);score=measured.pop('score')
 out=dict(case=case,friction=mu,tray_mass_kg=mass,source_scope=P['scope'],initial_state=dict(tray_center_z_m=.0445,engaged=False,pose_is_initial_only=True),before_drive=before,after_drive=after,input_rotation_rad=driveturn,output_rotation_rad=trayturn,tracking_error_rad=trayturn-driveturn,physical_predicates=measured,score=score,model_checks=dict(equality_constraints=int(m.neq),tray_actuators=int(sum(int(j)==trayjoint for j in m.actuator_trnid[:,0])),mocap_bodies=int(m.nmocap),input_only_actuation=bool(m.nu==1 and int(m.actuator_trnid[0,0])==drivejid),no_external_tray_force=True),trace=trace)
 if save_xml:(D/'results'/f'{case}.xml').write_text(xml)
 return out

def main():
 cases=['correct','wrong_phase','missing_carrier','missing_drive','missing_wheel','inverted_tray','held_proud','displaced_carrier','seized_wheels'];results=[]
 for case in cases:
  r=run(case,save_xml=True);results.append(r);print(case,r['score'],r['before_drive']['tray_center_z_m'],r['output_rotation_rad'],r['tracking_error_rad'],flush=True)
 sens=[]
 for mu,mass in [(.2,.5),(.2,.9),(.6,.5),(.6,.9)]:
  r=run('correct',mu,mass);sens.append(r);print('sensitivity',mu,mass,r['score'],flush=True)
 out=dict(engine='MuJoCoCPU '+mujoco.mj_versionString(),parameter_sha256=hashlib.sha256((D/'parameters.json').read_bytes()).hexdigest(),cases=results,sensitivity=sens)
 geometry_sensitivity=[]
 original_top=P['drive_arm_top_m']
 for top in [.007,.009,.011]:
  P['drive_arm_top_m']=top;r=run('correct');r['authored_drive_top_m']=top;geometry_sensitivity.append(r);print('geometry_sensitivity',top,r['score'],flush=True)
 P['drive_arm_top_m']=original_top;out['geometry_sensitivity']=geometry_sensitivity
 (D/'results/CONTACT_RESULTS.json').write_text(json.dumps(out,indent=2,default=lambda v:v.item() if isinstance(v,np.generic) else str(v))+'\n')
 if not results[0]['score']==1:raise SystemExit('Correct case FAILED; debug physical geometry/solver, do not relabel success')
 for r in results[1:]:
  if r['score']==1:raise SystemExit('Negative control falsely passed: '+r['case'])
 print('CONTACT SUCCESS AND NEGATIVE CONTROLS PASS')
if __name__=='__main__':main()
