"""Actual robot controller with explicitly ideal/synthetic task feedback, not physics."""
import json
from pathlib import Path
from feedback import Controller,ControlFailure
from ideal_fixture import IdealFixture
from scoring import Scorer


def audit(folder):
 fixture=IdealFixture(folder);c=Controller(fixture.plan,fixture.spec);judge=Scorer(fixture.spec);error=None;result=None;first_failure=None;constraint_peak=None;old_residual=0.
 for step in range(fixture.spec['run_limit']):
  frame=fixture.frame();result=judge.update(frame);index=c.index
  if result.failure and first_failure is None:first_failure=dict(step=step,phase=index,label=c.phases[index]['label'],reason=result.failure,frame=frame)
  try:command=c.step(fixture.q,frame)
  except (ControlFailure,KeyError,ValueError) as exc:error=str(exc);break
  fixture.advance(c,command,index)
  if fixture.residual>old_residual:constraint_peak=dict(step=step,phase=index,label=c.phases[index]['label'],residual_m=fixture.residual);old_residual=fixture.residual
  if c.done:break
 report=dict(kind='OFFLINE_IDEAL_TRACKING_SYNTHETIC_PHYSICAL_FEEDBACK',physics_executed=False,native_feedback_synthetic=True,
             grasps_validated=False,released_support_assumed=True,actions=step+1,simulated_seconds=(step+1)/20,
             phases=c.index,phase_count=len(c.phases),max_grasp_constraint_residual_m=fixture.residual,
             synthetic_score=result.score if result else None,scorer_failure=result.failure if result else None,first_failure=first_failure,constraint_peak=constraint_peak,error=error,events=c.events,
             passed=bool(c.done and error is None and result and result.success and fixture.residual<.001))
 print(json.dumps(report,indent=2));return 0 if report['passed'] else 1
if __name__=='__main__':raise SystemExit(audit(Path(__file__).resolve().parent))
