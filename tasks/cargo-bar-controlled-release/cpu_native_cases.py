"""Second-engine articulated diagnostic cases. No robot or Isaac executed.

Reuses declared native physics fixtures/forces/assertions, preserving distinction
between initialization probes and ordinary robot-action demonstrations. MuJoCo
Coulomb/constraint/contact dynamics differ from PhysX; no evidence transfers.
"""
import json
from pathlib import Path
import mujoco,numpy as np
from mechanism_cpu import export,initialize,observe
from native_tests import checks


def frame(model,data,spec):
 row=observe(model,data,spec)
 for name,b in row['bodies'].items():
  i=mujoco.mj_name2id(model,mujoco.mjtObj.mjOBJ_BODY,name);velocity=np.zeros(6)
  # Poses above use the ordinary link frame. BODY queries the inertial COM
  # frame; XBODY keeps linear velocity at the same datum as the scored pose.
  mujoco.mj_objectVelocity(model,data,mujoco.mjtObj.mjOBJ_XBODY,i,velocity,0)
  b.update(linear=velocity[3:].tolist(),angular=velocity[:3].tolist())
 return dict(schema=1,time=row['time'],bodies=row['bodies'],joints=row['joints'],max_penetration=row['contact_depth_m'],robot_clearance=None)


def probe(folder):
 spec=json.loads((folder/'scene.json').read_text());cases=json.loads((folder/'native-cases.json').read_text())['physics']
 model=mujoco.MjModel.from_xml_string(export(spec));rows=[];substeps=round(1/spec['control_hz']/spec['physics_dt'])
 for repeat in (0,1):
  for case in cases:
   d=mujoco.MjData(model);initialize(model,d,spec);initial=frame(model,d,spec)
   for setup in case.get('initialize_joints',[]):
    i=mujoco.mj_name2id(model,mujoco.mjtObj.mjOBJ_JOINT,setup['joint']);d.qpos[model.jnt_qposadr[i]]=setup['value']
   for setup in case.get('initialize_bodies',[]):
    body=next(b for a in spec['assemblies'] if a['name']==setup['assembly'] for b in a['bodies'] if not b.get('anchor'))
    i=mujoco.mj_name2id(model,mujoco.mjtObj.mjOBJ_JOINT,body['name']+'_free');offset=model.jnt_qposadr[i];q=setup.get('quat',body['quat'])
    d.qpos[offset:offset+7]=[*setup['pos'],q[3],*q[:3]]
   for force in case.get('forces',[]):
    i=mujoco.mj_name2id(model,mujoco.mjtObj.mjOBJ_BODY,force['body']);d.xfrc_applied[i,:3]=force.get('force',[0,0,0]);d.xfrc_applied[i,3:]=force.get('torque',[0,0,0])
   peak=0.;samples=[]
   for control in range(case['steps']+case.get('settle_steps',20)):
    if control==case['steps']:d.xfrc_applied[:]=0.
    for _ in range(substeps):
     mujoco.mj_step(model,d);peak=max(peak,max([0.]+[-float(c.dist) for c in d.contact[:d.ncon]]))
    samples.append(frame(model,d,spec))
   final=samples[-1];error=None;first_continuous_failure=None
   try:
    for sample in samples:
     try:checks(case.get('continuous_assertions',[]),initial,sample)
     except AssertionError as exc:
      first_continuous_failure=dict(time=sample['time'],error=str(exc));raise
    checks(case['assertions'],initial,final)
   except AssertionError as exc:error=str(exc)
   if peak>spec['penetration_limit'] and error is None:error='Physics-substep penetration exceeded integrity bound'
   rows.append(dict(name=case['name'],repeat=repeat,passed=error is None,error=error,initial=initial,final=final,peak_contact_depth_m=peak,first_continuous_failure=first_continuous_failure))
 report=dict(kind='SUPPLEMENTAL_MUJOCO_ARTICULATED_NATIVE_CASE_PROTOCOL',engine=mujoco.__version__,isaac_executed=False,
             robot_executed=False,initialization_is_not_demonstration=True,cases=rows,passed=all(r['passed'] for r in rows))
 print(json.dumps(report,indent=2));return 0 if report['passed'] else 1
if __name__=='__main__':raise SystemExit(probe(Path(__file__).resolve().parent))
