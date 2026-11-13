"""Force-driven SDS automatic capture/pull/release fixture; NOT robot evidence.

Only initial diagnostic placement writes qpos. Thereafter all changes are
integrated contacts under capped, explicitly authored external test-rig wrenches.
"""
import collections,hashlib,json,math
from pathlib import Path
import numpy as np,mujoco
from mechanism_cpu import export,initialize,observe
from cpu_native_cases import set_body
from interfaces import retained
from motion import rotate,multiply,conjugate,axis_quat,qangle
HERE=Path(__file__).resolve().parent

def rotation(q):return np.column_stack([rotate(q,v) for v in np.eye(3)])
def servo(m,d,spec,name,goal,quat,cap=12.,state=None):
 bid=mujoco.mj_name2id(m,mujoco.mjtObj.mjOBJ_BODY,name);state=state if state is not None else observe(m,d,spec)['bodies'][name];v=np.asarray(state['linear']);w=np.asarray(state['angular']);error=np.asarray(goal)-state['pos'];force=1500.*error-25.*v;force*=min(1.,cap/max(np.linalg.norm(force),1e-12));force+=np.array([0,0,m.body_mass[bid]*9.81])
 e=multiply(quat,conjugate(state['quat']));e=-e if e[3]<0 else e;n=np.linalg.norm(e[:3]);angle=2*math.atan2(n,e[3]);rv=e[:3]*angle/max(n,1e-12)
 R=rotation(state['quat'])@rotation([*m.body_iquat[bid][1:],m.body_iquat[bid][0]]);I=R@np.diag(m.body_inertia[bid])@R.T;torque=I@(1600.*rv-80.*w)+np.cross(w,I@w);torque*=min(1.,.060/max(np.linalg.norm(torque),1e-12));d.xfrc_applied[bid]=[*force,*torque];return state,float(np.linalg.norm(force-np.array([0,0,m.body_mass[bid]*9.81])))

def run(folder=HERE):
 s=json.loads((folder/'scene.json').read_text());xml=export(s);m=mujoco.MjModel.from_xml_string(xml);d=mujoco.MjData(m);initialize(m,d,s);mouth=np.array(s['parameters']['holder_mouth']);start=mouth+[-.015,0,0];set_body(m,d,'used_point_chisel',[.37,-.30,s['table_top']+.0102],[0,0,0,1]);set_body(m,d,'replacement_flat_chisel',start,axis_quat([1,0,0],math.pi/4));mujoco.mj_forward(m,d)
 stage='ALIGN';started=0.;stable=None;events=[];rows=[];peak=0.;first=None;complete=False;position_reference=start.copy();tug_start=None;window=collections.deque();maxforce=0.
 def change(name):
  nonlocal stage,started,stable
  stage=name;started=float(d.time);stable=None;events.append(dict(stage=name,time=started))
 def settled(condition,dwell=.25):
  nonlocal stable
  if not condition:stable=None;return False
  if stable is None:stable=float(d.time)
  return d.time-stable>=dwell
 for k in range(round(30/s['physics_dt'])):
  t=float(d.time);d.xfrc_applied[:]=0.;f=observe(m,d,s);b=f['bodies']['replacement_flat_chisel'];q=[0,0,0,1]
  if stage=='ALIGN':
   a=max(0.,math.pi/4-max(0.,t-.4)*.5);q=axis_quat([1,0,0],a);goal=start
   _,force=servo(m,d,s,'replacement_flat_chisel',goal,q,state=b);maxforce=max(maxforce,force)
   if settled(a==0 and np.linalg.norm(np.asarray(b['pos'])-start)<.0003 and qangle(b['quat'],[0,0,0,1])<.005):change('INSERT')
  elif stage=='INSERT':
   position_reference[0]=min(mouth[0]+.042,position_reference[0]+.0075*s['physics_dt']);_,force=servo(m,d,s,'replacement_flat_chisel',position_reference,q,state=b);maxforce=max(maxforce,force)
   if settled(position_reference[0]>=mouth[0]+.042-1e-9 and np.linalg.norm(np.asarray(b['pos'])-position_reference)<=.0006 and retained(s,f['bodies'],f['joints'])):tug_start=float(b['pos'][0]);change('TUG')
  elif stage=='TUG':
   goal=np.array(b['pos']);goal[0]-=.00030;_,force=servo(m,d,s,'replacement_flat_chisel',goal,q,state=b);maxforce=max(maxforce,force);x=float(b['pos'][0]);window.append((t,x))
   while len(window)>1 and window[1][0]<=t-.35:window.popleft()
   if tug_start-x>.0045:first=dict(reason='Pulled beyond bounded closed-slot retention',time=t);break
   if t-started>.8 and tug_start-x>=.0005 and t-window[0][0]>=.35-1e-8 and np.ptp([v for _,v in window])<=.0001 and retained(s,f['bodies'],f['joints']):change('RELEASE')
  elif stage=='RELEASE':
   if t-started>=3.:complete=True;break
  mujoco.mj_step(m,d);mujoco.mj_forward(m,d);depth=max([0.]+[-float(c.dist) for c in d.contact[:d.ncon]]);peak=max(peak,depth)
  if depth>s['penetration_limit']:
   first=dict(time=float(d.time),stage=stage,depth_m=depth,contacts=[dict(a=mujoco.mj_id2name(m,mujoco.mjtObj.mjOBJ_GEOM,c.geom1),b=mujoco.mj_id2name(m,mujoco.mjtObj.mjOBJ_GEOM,c.geom2),depth_m=-float(c.dist)) for c in d.contact[:d.ncon] if c.dist<-s['penetration_limit']]);break
  if k%round(.05/s['physics_dt'])==0:
   rows.append(observe(m,d,s))
   if k%round(.5/s['physics_dt'])==0 and __import__('os').getenv('SDS_PROBE_PROGRESS'):Path(__import__('os').environ['SDS_PROBE_PROGRESS']).write_text(json.dumps(dict(stage=stage,time=float(d.time),frame=rows[-1])))
 f=observe(m,d,s);result=dict(kind='SUPPLEMENTAL_CAPPED_WRENCH_SDS_AUTOMATIC_CAPTURE_CYCLE',engine=mujoco.__version__,isaac_executed=False,robot_executed=False,grasps_validated=False,initial_diagnostic_placement_only=True,external_force_cap_N=12.,gravity_compensation_separate=True,external_torque_cap_Nm=.060,max_servo_force_without_gravity_N=maxforce,stage=stage,events=events,completed=complete,peak_contact_depth_m=peak,first_violation=first,scene_sha256=hashlib.sha256((folder/'scene.json').read_bytes()).hexdigest(),probe_source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),export_sha256=hashlib.sha256(xml.encode()).hexdigest(),checks=rows,final=f,retained_after_release=retained(s,f['bodies'],f['joints']),passed=complete and first is None and retained(s,f['bodies'],f['joints']));print(json.dumps(result,indent=2));return result
if __name__=='__main__':raise SystemExit(0 if run()['passed'] else 1)
