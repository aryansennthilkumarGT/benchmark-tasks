"""Supplemental MuJoCo CPU contact probes exported from exact scene primitives.

This is a second-engine diagnostic, NOT Isaac/PhysX qualification, robot control,
expert evidence, hardware validation, or proof of compatibility with native GPU
contacts. No rendering, CUDA, network or paid service is used. Flat scalar Coulomb
friction uses the authored dynamic coefficient; compliant-contact solver behavior
is engine-specific. Only independent rigid bodies are supported, never silently
flatten articulated mechanisms or suppress task collision pairs.
"""
import argparse,copy,hashlib,importlib,json,math,sys,types,subprocess,time
from pathlib import Path
import xml.etree.ElementTree as ET
import numpy as np


def numbers(values):return ' '.join(format(float(v),'.17g') for v in values)
def wxyz(q):return [q[3],*q[:3]]

def model_xml(scene,material=None):
 if any(a.get('joints') for a in scene['assemblies']):raise ValueError('Articulated scene requires an explicitly reviewed joint exporter')
 root=ET.Element('mujoco',model=scene['slug']+'-SUPPLEMENTAL-CPU')
 ET.SubElement(root,'compiler',angle='radian',inertiafromgeom='false')
 ET.SubElement(root,'option',timestep=str(scene['physics_dt']),gravity=numbers(scene['gravity']),iterations='50',tolerance='1e-10',solver='Newton')
 default=ET.SubElement(root,'default')
 material=material or scene.get('material')
 if not material or 'dynamic_friction' not in material:raise ValueError('Explicit authored material coefficients are required')
 friction=material['dynamic_friction']
 ET.SubElement(default,'geom',friction=numbers([friction,.005,.0001]),condim='3',margin='0.00003',solref='.0042 1',solimp='.99 .999 .0001',density='0')
 world=ET.SubElement(root,'worldbody');ET.SubElement(world,'geom',name='table',type='plane',size='2 2 .05',pos=numbers([0,0,scene['table_top']]))
 for assembly in scene['assemblies']:
  for b in assembly['bodies']:
   body=ET.SubElement(world,'body',name=b['name'],pos=numbers(b['pos']),quat=numbers(wxyz(b['quat'])))
   if not b.get('anchor'):
    ET.SubElement(body,'freejoint',name=b['name']+'_free')
    ET.SubElement(body,'inertial',pos=numbers(b.get('center_of_mass',[0,0,0])),mass=str(b['mass']),diaginertia=numbers(b['diagonal_inertia']))
   for i,s in enumerate(b['shapes']):
    if not s.get('collision',True):continue
    attrs=dict(name=b['name']+'_'+str(i),pos=numbers(s['pos']),quat=numbers(wxyz(s['quat'])))
    if s['kind']=='box':attrs.update(type='box',size=numbers(np.array(s['size'])/2))
    elif s['kind']=='cylinder':attrs.update(type='cylinder',size=numbers([s['radius'],s['height']/2]))
    else:raise ValueError('Unsupported contact primitive: '+s['kind'])
    ET.SubElement(body,'geom',**attrs)
 return ET.tostring(root,encoding='unicode')


def scorer(folder,spec):
 name='_cpu_probe_'+hashlib.sha256(str(folder).encode()).hexdigest()[:12]
 package=types.ModuleType(name);package.__path__=[str(folder)];sys.modules[name]=package
 return importlib.import_module(name+'.scoring').Scorer(spec)


def run(folder,output):
 import mujoco
 started=time.monotonic();folder=folder.resolve();spec=json.loads((folder/'scene.json').read_text());cases=json.loads((folder/'native-cases.json').read_text())['physics']
 material=spec.get('material')
 if material is None:
  from pxr import Usd,UsdPhysics
  coefficients=set()
  for a in spec['assemblies']:
   stage=Usd.Stage.Open(str(folder/'assets'/(a['name']+'.usda')))
   mat=UsdPhysics.MaterialAPI(stage.GetPrimAtPath('/Asset/Material'))
   coefficients.add((float(mat.GetStaticFrictionAttr().Get()),float(mat.GetDynamicFrictionAttr().Get())))
  if len(coefficients)!=1:raise ValueError('Mixed materials require an explicit per-collider exporter')
  static,dynamic=coefficients.pop();material=dict(static_friction=static,dynamic_friction=dynamic)
 output.mkdir(parents=True,exist_ok=False);xml=model_xml(spec,material);(output/'export.xml').write_text(xml)
 model=mujoco.MjModel.from_xml_string(xml);data=mujoco.MjData(model)
 names=[b['name'] for a in spec['assemblies'] for b in a['bodies']];ids={n:mujoco.mj_name2id(model,mujoco.mjtObj.mjOBJ_BODY,n) for n in names}
 assemblies={a['name']:a for a in spec['assemblies']}
 report=dict(kind='SUPPLEMENTAL_MUJOCO_CPU_CONTACT_DIAGNOSTIC',engine=mujoco.__version__,isaac_executed=False,robot_executed=False,
             source_scene_sha256=hashlib.sha256((folder/'scene.json').read_bytes()).hexdigest(),input_sha256={n:hashlib.sha256((folder/n).read_bytes()).hexdigest() for n in ('scene.json','native-cases.json','scoring.py','source_manifest.json')},exporter_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),cases=[],passed=False,
             material_mapping=material,penetration_assertion='Final frame, matching the declared native assertion; peak transient is separately recorded, never hidden.',limitations=['Different contact solver and friction model from PhysX.','No robot grasp or controller is simulated.','No Isaac, expert or model evidence can be inferred.'])
 substeps=round(1/spec['control_hz']/spec['physics_dt']);assert abs(substeps*spec['physics_dt']-1/spec['control_hz'])<1e-10
 for case in cases:
  for repeat in (0,1):
   mujoco.mj_resetData(model,data)
   for init in case.get('initialize_bodies',[]):
    a=assemblies[init['assembly']]
    if len(a['bodies'])!=1:raise ValueError('Initialization of multi-body assembly requires explicit exporter support')
    n=a['bodies'][0]['name'];j=mujoco.mj_name2id(model,mujoco.mjtObj.mjOBJ_JOINT,n+'_free');q=model.jnt_qposadr[j]
    data.qpos[q:q+3]=init['pos'];data.qpos[q+3:q+7]=wxyz(init['quat'])
   mujoco.mj_forward(model,data);initial={n:data.xpos[i].copy() for n,i in ids.items()};judge=scorer(folder,spec);worst=0.;result=None
   def observe(t):
    bodies={}
    for n,i in ids.items():
     vel=np.empty(6);mujoco.mj_objectVelocity(model,data,mujoco.mjtObj.mjOBJ_BODY,i,vel,0)
     q=data.xquat[i];bodies[n]=dict(pos=data.xpos[i].tolist(),quat=[*q[1:],q[0]],linear=vel[3:].tolist(),angular=vel[:3].tolist())
    depth=max([0.]+[-float(c.dist) for c in data.contact[:data.ncon]])
    return dict(schema=1,time=t,bodies=bodies,joints={},max_penetration=depth,robot_clearance=1.),depth
   frame,depth=observe(0.);worst=depth;result=judge.update(frame)
   # Native probes apply the force first, then remove it during settling.
   steps=case.get('settle_steps',20)+case.get('steps',0)
   for step in range(steps):
    data.xfrc_applied[:]=0
    if step<case.get('steps',0):
     for force in case.get('forces',[]):
      data.xfrc_applied[ids[force['body']],:3]=force.get('force',[0,0,0]);data.xfrc_applied[ids[force['body']],3:]=force.get('torque',[0,0,0])
    for _ in range(substeps):mujoco.mj_step(model,data)
    frame,depth=observe((step+1)/spec['control_hz']);worst=max(worst,depth);result=judge.update(frame)
   outcomes=[]
   for a in case['assertions']:
    k=a['kind'];n=a.get('body');value=None
    if k=='pose':
     value=math.dist(frame['bodies'][n]['pos'],a['pos']);ok=value<=a['tolerance']
     if 'quat' in a:
      dot=abs(float(np.dot(frame['bodies'][n]['quat'],a['quat'])));ok=ok and 2*math.acos(min(1.,dot))<=a.get('angle',.05)
    elif k=='coordinate':value=frame['bodies'][n]['pos'][a['axis']];ok=a['min']<=value<=a['max']
    elif k=='displacement':
     v=np.array(frame['bodies'][n]['pos'])-initial[n];value=float(np.dot(v,a['axis'])) if 'axis' in a else float(np.linalg.norm(v));ok=a['min']<=value<=a['max']
    elif k=='penetration':value=frame['max_penetration'];ok=value<=a['max']
    elif k=='score':value=result.score;ok=a.get('min',0)<=value<=a.get('max',1) and ('success' not in a or result.success==a['success'])
    elif k=='valid':value=result.failure;ok=value is None
    elif k=='goal':value=a['name'] in result.completed;ok=value==a['completed']
    else:raise ValueError('Unsupported assertion kind: '+k)
    outcomes.append(dict(assertion=a,value=value,passed=bool(ok)))
   report['cases'].append(dict(name=case['name'],repeat=repeat,assertions=outcomes,final_frame=frame,scorer_failure=result.failure,peak_contact_penetration_m=worst,peak_exceeds_scene_tolerance=worst>spec['penetration_limit'],passed=all(x['passed'] for x in outcomes)))
   (output/'results.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
 report['duration_seconds']=time.monotonic()-started;report['passed']=all(x['passed'] for x in report['cases']);(output/'results.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n');return report


def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--folder',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 d=run(a.folder,a.output);print(json.dumps(dict(kind=d['kind'],passed=d['passed'],cases=len(d['cases']),output=str(a.output)),indent=2));return 0 if d['passed'] else 1
if __name__=='__main__':raise SystemExit(main())
