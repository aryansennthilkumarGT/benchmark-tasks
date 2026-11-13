"""Calibrate supplemental grasp contact resolution from recorded physical poses.

This is static diagnostic initialization, not replay continuation or an expert
trial. State is never overwritten after integration starts. No real hardware,
Isaac, model evaluation, upload or compute service is used.
"""
from pathlib import Path
import argparse,gzip,json,hashlib,xml.etree.ElementTree as ET
import mujoco,numpy as np
from cpu_yam_dynamics import initialize_robot,command_robot,measured


def probe(recording,phase,side='left',seconds=2.,subdivisions=(1,2,4,8),empty_control_body=None):
 xml=(recording/'model.xml').read_bytes();report=json.loads((recording/'report.json').read_text())
 if hashlib.sha256(xml).hexdigest()!=report['model_sha256']:raise ValueError('Recorded model was changed')
 if not report.get('source_bound') or report.get('isaac_executed') is not False:raise ValueError('Not a source-bound supplemental diagnostic')
 row=None
 trace=recording/'frames.jsonl.gz'
 opener=gzip.open if trace.exists() else open
 if not trace.exists():trace=recording/'frames.jsonl'
 with opener(trace,'rt') as stream:
  for line in stream:
   r=json.loads(line)
   if r['phase']==phase:row=r;break
 if row is None:raise ValueError('Requested actual phase was not recorded')
 results=[]
 for sub in subdivisions:
  for empty in ([False,True] if empty_control_body else [False]):
   root=ET.fromstring(xml);base_dt=float(root.find('option').get('timestep'));dt=base_dt/sub;root.find('option').set('timestep',str(dt))
   for geom in root.findall('.//geom'):
    if geom.get('name','').startswith(('left_','right_')):geom.set('solref',f'{.0022/sub} 1');geom.set('solmix','1000000')
   if empty:
    parent=root.find('worldbody');child=next((b for b in parent.findall('body') if b.get('name')==empty_control_body),None)
    if child is None:raise ValueError('Empty control must name one independent free body')
    if child.find('freejoint') is None:raise ValueError('Cannot remove an articulated body for the empty control')
    parent.remove(child)
   exported=ET.tostring(root,encoding='unicode');m=mujoco.MjModel.from_xml_string(exported);d=mujoco.MjData(m)
   for name,value in row['frame']['joints'].items():
    jid=mujoco.mj_name2id(m,mujoco.mjtObj.mjOBJ_JOINT,name);d.qpos[m.jnt_qposadr[jid]]=value
   for name,b in row['frame']['bodies'].items():
    jid=mujoco.mj_name2id(m,mujoco.mjtObj.mjOBJ_JOINT,name+'_free')
    if jid>=0:
     a=m.jnt_qposadr[jid];q=b['quat'];d.qpos[a:a+7]=[*b['pos'],q[3],*q[:3]]
   initialize_robot(m,d,row['robot_q']);action=np.asarray(row['robot_q']);off=0 if side=='left' else 7;action[off+6]=0.;command_robot(m,d,action);peak=0.
   for _ in range(round(seconds/dt)):
    mujoco.mj_step(m,d)
    for contact in d.contact[:d.ncon]:
     names=[mujoco.mj_id2name(m,mujoco.mjtObj.mjOBJ_GEOM,int(g)) or '' for g in contact.geom]
     if any(n.startswith(('left_','right_')) for n in names):peak=max(peak,max(0.,-float(contact.dist)))
   warnings={mujoco.mjtWarning(i).name:int(v.number) for i,v in enumerate(d.warning) if v.number}
   results.append(dict(subdivision=sub,diagnostic_timestep=dt,robot_contact_timeconstant=.0022/sub,empty_control_body=empty_control_body if empty else None,final_joint_aperture_m=float(measured(m,d)[off+6]*.0939),peak_robot_contact_depth_m=peak,seconds=float(d.time),warnings=warnings,export_sha256=hashlib.sha256(exported.encode()).hexdigest()))
 return dict(kind='SUPPLEMENTAL_GRASP_CONTACT_REFINEMENT_CALIBRATION',isaac_executed=False,hardware_executed=False,expert_success=False,initialization_from_recorded_poses=True,exact_dynamic_state_continuation=False,pose_writes_after_initialization=False,recording_model_sha256=report['model_sha256'],recording_source_commit=report['source_commit'],recording_source_commit_is_exact=report.get('source_commit_is_exact',False),recording_runtime_inputs_sha256=report['runtime_inputs_sha256'],phase=phase,side=side,harness_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),checks=results)

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--recording',type=Path,required=True);p.add_argument('--phase',type=int,required=True);p.add_argument('--side',choices=['left','right'],default='left');p.add_argument('--seconds',type=float,default=2.);p.add_argument('--empty-control-body');p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 if not 0.<a.seconds<=5.:raise SystemExit('Calibration duration must be0..5seconds')
 r=probe(a.recording,a.phase,a.side,a.seconds,empty_control_body=a.empty_control_body);a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r['checks'],indent=2))
