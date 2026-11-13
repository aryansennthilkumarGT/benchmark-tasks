"""Synthetic clocks and actual local processes; no provider or GPU calls."""
import tempfile,time,sys
from pathlib import Path
import pytest
from engine import Incomplete,atomic,execute
from session_budget import session,Window


def receipt(p,now=1000,balance=100):
 atomic(p,dict(hourly_usd=2.,balance_usd=balance,spent_before_start_usd=0.,instance_started_unix=now,
               authorized_session_spend_usd=100.,authorization_reference='CPU_ONLY_AUTH_FORMAT_FIXTURE',
               balance_observed_unix=now,instance_id='CPU_TEST_FIXTURE',gpu_uuid='NOT_A_GPU',provider_evidence='SYNTHETIC_TEST'))

def test_stale_balance_and_protected_reserve_block_start(tmp_path):
 p=tmp_path/'budget.json';receipt(p)
 with pytest.raises(Incomplete,match='five minutes'):session(p,clock=lambda:1301)
 receipt(p,balance=29.60)
 with pytest.raises(Incomplete,match='reserve'):session(p,clock=lambda:1000)

def test_task_deadline_does_not_cancel_other_tasks_or_extend_session(tmp_path):
 now=[1000.];p=tmp_path/'b.json';receipt(p);b=session(p,clock=lambda:now[0]);task=b.task(60)
 now[0]=1061.
 with pytest.raises(Incomplete,match='deadline'):task.check()
 assert b.check()['remaining_seconds']==21479
 assert b.task(50000).deadline==b.deadline
 now[0]=22601.
 with pytest.raises(Incomplete):b.check()

def test_deadline_kills_owned_real_cpu_workload(tmp_path):
 p=tmp_path/'b.json';receipt(p,time.time());b=session(p);task=b.task(.3)
 with pytest.raises(Incomplete,match='deadline'):
  execute([sys.executable,'-c','import time;print("CPU_ONLY",flush=True);time.sleep(30)'],tmp_path,tmp_path/'log',20,budget=task)
 assert 'CPU_ONLY' in (tmp_path/'log').read_text()

def test_session_cannot_exceed_six_hours(tmp_path):
 p=tmp_path/'b.json';receipt(p)
 with pytest.raises(Incomplete,match='six hours'):session(p,deadline=22601,clock=lambda:1000)
