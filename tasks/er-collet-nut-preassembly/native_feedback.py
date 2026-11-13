"""Read-only privileged state for the scripted expert, never model observations.

The native collector's frame is already recorded for independent scoring/replay.
The expert reads its physical state only, not score/results, and outputs ordinary
robot joint/gripper actions. Missing/stale telemetry fails instead of substituting
nominal part poses. No simulator state is written.
"""
import json


def termination_for(result):
    """Permanent invalidation ends futile simulation/model spending at zero."""
    if result.success:return True,'success'
    if result.failure is not None:return True,'invalid_physical_state'
    return False,None
from pathlib import Path

class NativeFrameReader:
 def __init__(self,path):self.path=Path(path);self.offset=0;self.latest=None
 def read(self,observation_time):
  with self.path.open('r',encoding='utf-8') as stream:
   stream.seek(self.offset)
   while True:
    start=stream.tell();line=stream.readline()
    if not line or not line.endswith('\n'):stream.seek(start);break
    row=json.loads(line)
    if row.get('kind')!='NATIVE_SIMULATION_FRAME':raise ValueError('Wrong telemetry producer')
    frame=row.get('frame')
    if not isinstance(frame,dict) or frame.get('schema')!=1:raise ValueError('Invalid native state frame')
    self.latest=frame
   self.offset=stream.tell()
  if self.latest is None or abs(self.latest['time']-float(observation_time))>1e-4:raise ValueError('Native state and robot observation are not synchronized')
  return self.latest
