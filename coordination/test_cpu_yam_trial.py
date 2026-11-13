"""Task source isolation, not a physics/evaluation success fixture."""
import sys
from pathlib import Path
import pytest
import cpu_yam_trial as trial


def test_one_process_cannot_silently_reuse_a_different_task_module(tmp_path,monkeypatch):
 names=['mechanism_cpu','feedback','scoring','audit_geometry','robot_clearance','source_identity']
 for name in names:
  monkeypatch.delitem(sys.modules,name,raising=False)
  (tmp_path/(name+'.py')).write_text('FORMAT_FIXTURE_ONLY=True\n')
 monkeypatch.setattr(trial,'_BOUND_FOLDER',None)
 previous=list(sys.path)
 try:
  modules=trial.load(tmp_path)
  assert all(m.FORMAT_FIXTURE_ONLY for m in modules.values())
  with pytest.raises(ValueError,match='one task per process'):trial.load(tmp_path/'different')
 finally:
  sys.path[:]=previous
  for name in names:sys.modules.pop(name,None)


def test_terminal_controller_cannot_certify_zero_partial_or_nonfinite_score():
 # An expert can terminate while the physical state fails the independent scorer.
 args=dict(completed=True,controller_done=True,stop_after_phase=None,error=None,
           warnings={},source_bound=True,maximum_velocity_ratio=.8)
 for score in (0.,.25,.75,None,float('nan'),float('inf')):
  result=trial.classify_result(score=score,**args)
  assert not result['passed'] and not result['full_task_passed']
 assert trial.classify_result(score=1.,**args)['full_task_passed']
 args['source_bound']=False
 assert not trial.classify_result(score=1.,**args)['passed']


def test_requested_prefix_never_promoted_to_full_task_evidence():
 args=dict(completed=True,controller_done=True,stop_after_phase=7,score=1.,
           error=None,warnings={},source_bound=True,maximum_velocity_ratio=.8)
 result=trial.classify_result(**args)
 assert result['passed'] and not result['full_task_passed']
 assert result['result_scope']=='REQUESTED_PREFIX_DIAGNOSTIC'
 args['warnings']={'mjWARN_BADQVEL':1}
 assert not trial.classify_result(**args)['passed']
