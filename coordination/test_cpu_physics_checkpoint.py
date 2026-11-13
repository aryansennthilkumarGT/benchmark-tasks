"""Actual simulator continuation and complete policy-state serialization tests."""
from collections import deque
from dataclasses import dataclass
import types,hashlib
import numpy as np,pytest,mujoco
import cpu_physics_checkpoint as checkpoint
from cpu_yam_dynamics import export_robot_only,initialize_robot,command_robot,measured

@dataclass
class Result:
 score:float=0.
 success:bool=False
 failure:str|None=None


def policy_fixture():
 c=types.SimpleNamespace(spec={'fixture':'serialization only'},phases=[],index=7,last_time=.1,attempts={3:2},context={'array':np.array([1.,2.]),'tuple':(False,None)},targets={},best=float('inf'),motion={'left':types.SimpleNamespace(ik=object(),reference=np.arange(6,dtype=float),base=(0.,.305,.75),dt=.05)})
 s=types.SimpleNamespace(spec={},defs={},previous_time=.1,failed=None,window=deque([(0.,np.eye(3))]),result=Result(score=.25))
 return c,s


def test_true_integration_resume_matches_uninterrupted_robot_dynamics(tmp_path):
 model=mujoco.MjModel.from_xml_string(export_robot_only());a=mujoco.MjData(model);initialize_robot(model,a);q=measured(model,a);q[0]=.15;command_robot(model,a,q)
 for _ in range(200):mujoco.mj_step(model,a)
 c,s=policy_fixture();path=tmp_path/'state.npz';binding={'model':'EXACT_TEST_FIXTURE','sources':{'x':'a'*64}};checkpoint.save(path,model,a,c,s,binding,{'actions':17})
 b=mujoco.MjData(model);other,judge=policy_fixture();other.attempts={};judge.window.clear();payload=checkpoint.restore(path,model,b,other,judge,binding)
 assert other.attempts=={3:2} and np.array_equal(other.context['array'],[1.,2.]) and other.context['tuple']==(False,None)
 assert len(judge.window)==1 and judge.result.score==.25 and payload['metadata']['actions']==17
 for _ in range(300):mujoco.mj_step(model,a);mujoco.mj_step(model,b)
 assert a.time==b.time and np.allclose(a.qpos,b.qpos,atol=1e-12,rtol=0) and np.allclose(a.qvel,b.qvel,atol=1e-12,rtol=0)


def test_source_change_is_rejected_before_any_physics_or_policy_restore(tmp_path):
 m=mujoco.MjModel.from_xml_string(export_robot_only());d=mujoco.MjData(m);initialize_robot(m,d);c,s=policy_fixture();p=tmp_path/'c.npz';checkpoint.save(p,m,d,c,s,{'source':'a'},{});q=d.qpos.copy();c.index=99
 with pytest.raises(ValueError,match='configuration changed'):checkpoint.restore(p,m,d,c,s,{'source':'b'})
 assert np.array_equal(d.qpos,q) and c.index==99


def test_interrupted_trace_tail_is_preserved_and_committed_prefix_is_verified(tmp_path):
 p=tmp_path/'frames.jsonl';prefix=b'{"t":0}\n';tail=b'{"t":.05}\nPARTIAL';p.write_bytes(prefix+tail)
 h=checkpoint.recover_trace(p,len(prefix),hashlib.sha256(prefix).hexdigest());assert p.read_bytes()==prefix and h.hexdigest()==hashlib.sha256(prefix).hexdigest()
 assert next(tmp_path.glob('interrupted-tail-*.jsonl')).read_bytes()==tail
 p.write_bytes(b'CHANGED\n')
 with pytest.raises(ValueError,match='changed'):checkpoint.recover_trace(p,len(prefix),hashlib.sha256(prefix).hexdigest())
