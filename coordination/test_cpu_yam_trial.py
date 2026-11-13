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
