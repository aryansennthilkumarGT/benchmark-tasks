"""Long free-root hold and resolution check, not a robot/native demonstration.

No applied forces, root locks, object writes during stepping or receiving-cradle
support. The second case halves only the supplemental engine's timestep; the
native PhysX setting remains unchanged. Failing either case fails this probe.
"""
import copy,hashlib,json
from pathlib import Path
import mujoco,numpy as np
from mechanism_cpu import export,initialize
from cpu_contact import description
HERE=Path(__file__).resolve().parent


def probe(folder=HERE,duration=30.):
 spec=json.loads((folder/'scene.json').read_text());rows=[]
 for resolution in (1,2):
  current=copy.deepcopy(spec);current['physics_dt']/=resolution;xml=export(current)
  model=mujoco.MjModel.from_xml_string(xml);data=mujoco.MjData(model);initialize(model,data,current)
  body=mujoco.mj_name2id(model,mujoco.mjtObj.mjOBJ_BODY,'outer_tube')
  frame=mujoco.mj_name2id(model,mujoco.mjtObj.mjOBJ_BODY,'wall_frame')
  origin=data.xpos[body].copy();samples=[];peak=0.;maximum_displacement=0.;support_force_peak=0.
  for step in range(round(duration/current['physics_dt'])):
   mujoco.mj_step(model,data)
   displacement=float(np.linalg.norm(data.xpos[body]-origin));maximum_displacement=max(maximum_displacement,displacement)
   for i,contact in enumerate(data.contact[:data.ncon]):
    peak=max(peak,-float(contact.dist))
    for geom in (contact.geom1,contact.geom2):
     if model.geom_bodyid[geom]!=frame:continue
     name=mujoco.mj_id2name(model,mujoco.mjtObj.mjOBJ_GEOM,geom)
     if name not in ('wall_frame1','wall_frame2'):
      force=np.zeros(6);mujoco.mj_contactForce(model,data,i,force);support_force_peak=max(support_force_peak,abs(float(force[0])))
   if (step+1)%round(5/current['physics_dt'])==0:samples.append(dict(time=float(data.time),root_displacement_m=displacement))
  row=dict(resolution_factor=resolution,timestep_s=current['physics_dt'],duration_s=float(data.time),
           contact_export_sha256=hashlib.sha256(xml.encode()).hexdigest(),samples=samples,
           max_root_displacement_m=maximum_displacement,final_root_position_m=data.xpos[body].tolist(),
           peak_contact_depth_m=peak,receiving_frame_support_force_peak_N=support_force_peak,
           passed=maximum_displacement<=.003 and peak<=spec['penetration_limit'] and support_force_peak<.01)
  rows.append(row)
 difference=float(np.linalg.norm(np.array(rows[0]['final_root_position_m'])-rows[1]['final_root_position_m']))
 return dict(kind='SUPPLEMENTAL_MUJOCO_LONG_FREE_HOLD_AND_TIMESTEP_CHECK',engine=mujoco.__version__,
             isaac_executed=False,robot_executed=False,applied_test_rig_forces=False,
             scene_sha256=hashlib.sha256((folder/'scene.json').read_bytes()).hexdigest(),contact_model=description(spec['material']['contact_offset']),
             tests=rows,resolution_endpoint_difference_m=difference,resolution_difference_limit_m=.00005,
             passed=all(r['passed'] for r in rows) and difference<=.00005)

if __name__=='__main__':
 report=probe();print(json.dumps(report,indent=2));raise SystemExit(0 if report['passed'] else 1)
