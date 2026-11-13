"""Repeated declared diagnostic contact cases, not native YAM/Isaac evidence."""
import copy,json,hashlib
from pathlib import Path
import mujoco,numpy as np
from mechanism_cpu import export,initialize,observe
from scoring import Scorer
from native_tests import checks
HERE=Path(__file__).resolve().parent

def set_body(m,d,body,pos,quat):
 i=mujoco.mj_name2id(m,mujoco.mjtObj.mjOBJ_JOINT,body+'_free');address=m.jnt_qposadr[i];d.qpos[address:address+7]=[*pos,quat[3],*quat[:3]]

def run(folder=HERE):
 spec=json.loads((folder/'scene.json').read_text());xml=export(spec);rows=[];cases=json.loads((folder/'native-cases.json').read_text())['physics']
 for repeat in (0,1):
  for case in cases:
   m=mujoco.MjModel.from_xml_string(xml);d=mujoco.MjData(m);initialize(m,d,spec);judge=Scorer(spec);judge.update(observe(m,d,spec));row=dict(name=case['name'],repeat=repeat,passed=False);peak=0.
   try:
    for setup in case.get('initialize_joints',[]):
     i=mujoco.mj_name2id(m,mujoco.mjtObj.mjOBJ_JOINT,setup['joint']);d.qpos[m.jnt_qposadr[i]]=setup['value']
    for setup in case.get('initialize_bodies',[]):set_body(m,d,setup['body'],setup['pos'],setup.get('quat',[0,0,0,1]))
    mujoco.mj_forward(m,d);initial=observe(m,d,spec);substeps=round(1/spec['control_hz']/spec['physics_dt']);count=case['steps']+case.get('settle_steps',20)
    for control in range(count):
     d.xfrc_applied[:]=0.
     if control<case['steps']:
      for force in case.get('forces',[]):
       i=mujoco.mj_name2id(m,mujoco.mjtObj.mjOBJ_BODY,force['body']);d.xfrc_applied[i]=[*force.get('force',[0,0,0]),*force.get('torque',[0,0,0])]
     for _ in range(substeps):
      mujoco.mj_step(m,d);mujoco.mj_forward(m,d);depth=max([0.]+[-float(c.dist) for c in d.contact[:d.ncon]]);peak=max(peak,depth)
      if depth>spec['penetration_limit']:raise AssertionError('Substep contact depth '+str(depth))
     f=observe(m,d,spec);r=judge.update(f);checks(case.get('continuous_assertions',[]),initial,f,r)
    checks(case['assertions'],initial,f,r);row.update(passed=True,final=f,result=r.__dict__)
   except Exception as e:row['error']=str(e)
   row['peak_contact_depth_m']=peak;rows.append(row)
 result=dict(kind='SUPPLEMENTAL_MUJOCO_SDS_CONTACT_PROTOCOL',engine=mujoco.__version__,isaac_executed=False,robot_executed=False,grasps_validated=False,scene_sha256=hashlib.sha256((folder/'scene.json').read_bytes()).hexdigest(),export_sha256=hashlib.sha256(xml.encode()).hexdigest(),cases=rows,passed=all(r['passed'] for r in rows));print(json.dumps(result,indent=2));return result
if __name__=='__main__':raise SystemExit(0 if run()['passed'] else 1)
