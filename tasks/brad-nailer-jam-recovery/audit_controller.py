"""Execute actual robot commands against explicit ideal grasp assumptions."""
import hashlib,json,sys,os
from pathlib import Path
from feedback import Controller
from ideal_fixture import IdealFixture
from source_identity import runtime_hashes,require_same
HERE=Path(__file__).resolve().parent


def run(folder=HERE,record=False):
 identity=runtime_hashes(folder);f=IdealFixture(folder);c=Controller(f.plan,f.spec);samples=[];error=None;reported=None
 try:
  while not c.done:
   if reported!=c.index:
    reported=c.index;print(json.dumps(dict(phase=c.index,label=c.phases[c.index]['label'],actions=c.actions,seconds=f.time)),file=sys.stderr,flush=True)
   if os.environ.get('ROBOCURVE_IDEAL_PROGRESS') and c.actions%25==0:
    import numpy as np
    state=dict(kind='SYNTHETIC_IDEAL_DEBUG_CHECKPOINT',phase=c.index,actions=c.actions,q=f.q.tolist(),frame=f.frame(),held=f.held,context=c.context,events=c.events[-3:])
    Path(os.environ['ROBOCURVE_IDEAL_PROGRESS']).write_text(json.dumps(state,default=lambda x:x.tolist() if isinstance(x,np.ndarray) else x))
   frame=f.frame();index=c.index;command=c.step(f.q,frame)
   if record and (c.actions%5==0 or c.started is None or index==len(c.phases)-1):samples.append(dict(index=index,q=f.q.tolist(),frame=frame))
   f.advance(c,command,index)
 except Exception as exc:error=str(exc)
 try:require_same(folder,identity)
 except ValueError as exc:error=str(exc)
 result=dict(kind='IDEAL_TRACKING_WITH_SYNTHETIC_RIGID_GRASPS',physics_executed=False,isaac_executed=False,robot_hardware_executed=False,
   scene_sha256=hashlib.sha256((folder/'scene.json').read_bytes()).hexdigest(),controller_sha256=hashlib.sha256((folder/'controller.json').read_bytes()).hexdigest(),
   actions=c.actions,seconds=f.time,phase=c.index,total_phases=len(c.phases),error=error,maximum_grasp_constraint_residual_m=f.residual,events=c.events,final=f.frame(),
   runtime_inputs_sha256=identity,terminal_robot_q=f.q.tolist(),passed=bool(c.done and error is None and f.residual<.0003))
 if record:result['samples']=samples
 return result

if __name__=='__main__':
 r=run(record=True);print(json.dumps(r,indent=2));raise SystemExit(0 if r['passed'] else 1)
