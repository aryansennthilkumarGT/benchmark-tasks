"""Read-only privileged telemetry contract; no simulator or robot execution."""
import json
import pytest
from native_feedback import NativeFrameReader


def row(t):return dict(kind='NATIVE_SIMULATION_FRAME',frame=dict(schema=1,time=t,bodies={},joints={}),result=dict(score=1.))

def test_partial_tail_is_not_consumed_and_only_physical_frame_is_returned(tmp_path):
 p=tmp_path/'trace.jsonl';a=json.dumps(row(0.));b=json.dumps(row(.05))
 p.write_text(a+'\n'+b[:20]);reader=NativeFrameReader(p)
 f=reader.read(0.);assert 'result' not in f and 'score' not in f
 with p.open('a') as stream:stream.write(b[20:]+'\n')
 assert reader.read(.05)['time']==.05
 with pytest.raises(ValueError,match='synchronized'):reader.read(.10)

def test_wrong_producer_and_missing_file_fail_closed(tmp_path):
 p=tmp_path/'trace.jsonl';reader=NativeFrameReader(p)
 with pytest.raises(FileNotFoundError):reader.read(0.)
 p.write_text(json.dumps(dict(kind='IDEAL_TRACKING',frame=row(0.)['frame']))+'\n')
 with pytest.raises(ValueError,match='producer'):reader.read(0.)

def test_permanent_invalidation_terminates_at_zero_and_full_success_stays_distinct():
 from types import SimpleNamespace
 from native_feedback import termination_for
 assert termination_for(SimpleNamespace(success=False,failure=None))==(False,None)
 assert termination_for(SimpleNamespace(success=False,failure='Solid interference'))==(True,'invalid_physical_state')
 assert termination_for(SimpleNamespace(success=True,failure=None))==(True,'success')
