"""Audit original task preservation when adding real CPU YAM articulations.

This is an exporter/initialization audit, not a full robot expert test. One task
per invocation. All scalar geometry and task joint parameters are compared with
its unmodified task-only supplemental model before any controller is run.
"""
import argparse,hashlib,json
from pathlib import Path
import mujoco,numpy as np
from cpu_yam_trial import load,export
from cpu_yam_dynamics import initialize_robot,measured


def audit(folder):
 folder=folder.resolve();spec=json.loads((folder/'scene.json').read_text());modules=load(folder);backend=modules['mechanism_cpu']
 hashes=modules['source_identity'].runtime_hashes(folder)
 original=mujoco.MjModel.from_xml_string(backend.export(spec));combined=mujoco.MjModel.from_xml_string(export(spec,backend))
 a=mujoco.MjData(original);b=mujoco.MjData(combined);backend.initialize(original,a,spec);backend.initialize(combined,b,spec);initialize_robot(combined,b)
 checks=[]
 def check(label,ok):
  checks.append(dict(label=label,passed=bool(ok)))
 def same(field,i,j):return np.allclose(getattr(original,field)[i],getattr(combined,field)[j],rtol=1e-12,atol=1e-12)
 task_names=[x['name'] for assembly in spec['assemblies'] for x in assembly['bodies']]
 for name in task_names:
  i=mujoco.mj_name2id(original,mujoco.mjtObj.mjOBJ_BODY,name);j=mujoco.mj_name2id(combined,mujoco.mjtObj.mjOBJ_BODY,name)
  check('body_exists:'+name,i>=0 and j>=0)
  if i<0 or j<0:continue
  for field in ('body_mass','body_inertia','body_ipos','body_iquat','body_pos','body_quat'):
   check(field+':'+name,same(field,i,j))
  gi=np.flatnonzero(original.geom_bodyid==i);gj=np.flatnonzero(combined.geom_bodyid==j)
  check('collider_count:'+name,len(gi)==len(gj))
  for x in gi:
   geom=mujoco.mj_id2name(original,mujoco.mjtObj.mjOBJ_GEOM,int(x));y=mujoco.mj_name2id(combined,mujoco.mjtObj.mjOBJ_GEOM,geom)
   check('geom_exists:'+geom,y>=0)
   if y<0:continue
   for field in ('geom_type','geom_size','geom_pos','geom_quat','geom_friction','geom_margin','geom_gap','geom_solref','geom_solimp'):
    check(field+':'+geom,same(field,int(x),y))
   if original.geom_type[x]==mujoco.mjtGeom.mjGEOM_MESH:
    mi=int(original.geom_dataid[x]);mj=int(combined.geom_dataid[y]);vi=original.mesh_vertadr[mi];vj=combined.mesh_vertadr[mj];ni=original.mesh_vertnum[mi];nj=combined.mesh_vertnum[mj]
    check('original_mesh_vertices:'+geom,ni==nj and np.allclose(original.mesh_vert[vi:vi+ni],combined.mesh_vert[vj:vj+nj],rtol=1e-12,atol=1e-12))
 for assembly in spec['assemblies']:
  for joint in assembly.get('joints',[]):
   name=joint['name'];i=mujoco.mj_name2id(original,mujoco.mjtObj.mjOBJ_JOINT,name);j=mujoco.mj_name2id(combined,mujoco.mjtObj.mjOBJ_JOINT,name)
   check('task_joint_exists:'+name,i>=0 and j>=0)
   if i<0 or j<0:continue
   for field in ('jnt_type','jnt_pos','jnt_axis','jnt_range','jnt_stiffness','jnt_solref','jnt_solimp'):
    check(field+':'+name,same(field,i,j))
   check('dof_damping:'+name,same('dof_damping',int(original.jnt_dofadr[i]),int(combined.jnt_dofadr[j])))
 check('no_original_task_actuators',original.nu==0)
 check('only_real_robot_actuators',combined.nu==16 and all(mujoco.mj_id2name(combined,mujoco.mjtObj.mjOBJ_ACTUATOR,i).startswith(('left_','right_')) for i in range(combined.nu)))
 before=backend.observe(original,a,spec);after=backend.observe(combined,b,spec)
 for name in task_names:
  for key in ('pos','quat','linear','angular'):check('initial_'+key+':'+name,np.allclose(before['bodies'][name][key],after['bodies'][name][key],rtol=0,atol=1e-12))
 check('actual_initial_joint_coordinates',before['joints']==after['joints']==spec.get('initial_joint_values',{}))
 # Two genuinely integrated, initially decoupled models: adding the parked
 # robot should not alter the original mechanism's first10physics steps.
 for _ in range(10):mujoco.mj_step(original,a);mujoco.mj_step(combined,b)
 before=backend.observe(original,a,spec);after=backend.observe(combined,b,spec)
 for name in task_names:
  check('initial_dynamics:'+name,np.allclose(before['bodies'][name]['pos'],after['bodies'][name]['pos'],rtol=0,atol=1e-7))
 g=modules['audit_geometry'].geometry_module(folder);frame=backend.observe(combined,b,spec)
 frame['max_penetration']=float(g.maximum_penetration(spec,frame['bodies']));frame['robot_clearance']=float(g.robot_clearance(modules['robot_clearance'].boxes(measured(combined,b),g),spec,frame['bodies']))
 # Initial-layout validation must start at the actual reset time.
 backend.initialize(combined,b,spec);initialize_robot(combined,b);frame=backend.observe(combined,b,spec)
 frame['max_penetration']=float(g.maximum_penetration(spec,frame['bodies']));frame['robot_clearance']=float(g.robot_clearance(modules['robot_clearance'].boxes(measured(combined,b),g),spec,frame['bodies']))
 result=modules['scoring'].Scorer(spec).update(frame);check('original_scorer_accepts_actual_initial_frame',result.failure is None)
 check('source_unchanged',modules['source_identity'].runtime_hashes(folder)==hashes)
 return dict(kind='SUPPLEMENTAL_CPU_TASK_ADAPTER_PRESERVATION_AUDIT',task=spec['slug'],engine=mujoco.__version__,isaac_executed=False,robot_expert_success=False,checks=checks,source_hashes=hashes,initial_score=result.score,initial_failure=result.failure,passed=all(c['passed'] for c in checks))

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--task-folder',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();r=audit(a.task_folder);a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(dict(task=r['task'],passed=r['passed'],checks=len(r['checks']),failures=[c for c in r['checks'] if not c['passed']])));raise SystemExit(0 if r['passed'] else 1)
