"""Exact source-bound supplemental integration checkpoints, not virtual grasps.

Only restore an actual saved mjSTATE_INTEGRATION at process initialization.
No pickle or arbitrary class loading; controller/scorer state remains complete.
This cannot create native Isaac or hardware evidence.
"""
from collections import deque
from dataclasses import asdict,is_dataclass
from pathlib import Path
import hashlib,json,math,os
import mujoco,numpy as np

STATE=mujoco.mjtState.mjSTATE_INTEGRATION


def encode(value):
 if isinstance(value,np.ndarray):return {'_type':'ndarray','dtype':value.dtype.str,'shape':list(value.shape),'values':value.ravel().tolist()}
 if isinstance(value,np.generic):return encode(value.item())
 if isinstance(value,deque):return {'_type':'deque','maxlen':value.maxlen,'values':[encode(v) for v in value]}
 if isinstance(value,tuple):return {'_type':'tuple','values':[encode(v) for v in value]}
 if isinstance(value,dict):return {'_type':'dict','pairs':[[encode(k),encode(v)] for k,v in value.items()]}
 if isinstance(value,list):return [encode(v) for v in value]
 if isinstance(value,float) and not math.isfinite(value):
  if math.isnan(value):raise ValueError('NaN cannot enter a computational checkpoint')
  return {'_type':'infinity','sign':1 if value>0 else -1}
 if value is None or isinstance(value,(str,bool,int,float)):return value
 raise TypeError('Unsupported computational state type: '+type(value).__name__)


def decode(value):
 if isinstance(value,list):return [decode(v) for v in value]
 if not isinstance(value,dict):return value
 kind=value['_type']
 if kind=='ndarray':
  dtype=np.dtype(value['dtype'])
  if dtype.hasobject:raise ValueError('Object arrays are not allowed')
  return np.asarray(value['values'],dtype=dtype).reshape(value['shape'])
 if kind=='dict':return {decode(k):decode(v) for k,v in value['pairs']}
 if kind=='tuple':return tuple(decode(v) for v in value['values'])
 if kind=='deque':return deque((decode(v) for v in value['values']),maxlen=value['maxlen'])
 if kind=='infinity':return float('inf')*value['sign']
 raise ValueError('Unknown computational state encoding')


def controller_state(c):
 return dict(fields={k:v for k,v in c.__dict__.items() if k not in ('spec','phases','motion')},motion={s:{k:v for k,v in m.__dict__.items() if k!='ik'} for s,m in c.motion.items()})


def scorer_state(s):
 values={k:v for k,v in s.__dict__.items() if k not in ('spec','defs','result')}
 if not is_dataclass(s.result):raise ValueError('Unreviewed scorer result type')
 return dict(fields=values,result=asdict(s.result))


def save(path,model,data,controller,scorer,binding,metadata):
 vector=np.empty(mujoco.mj_stateSize(model,STATE));mujoco.mj_getState(model,data,vector,STATE)
 if not np.isfinite(vector).all():raise ValueError('Nonfinite physical state cannot be checkpointed')
 payload=dict(schema=1,kind='SUPPLEMENTAL_TRUE_INTEGRATION_CHECKPOINT',engine=mujoco.__version__,binding=binding,metadata=metadata,controller=controller_state(controller),scorer=scorer_state(scorer),warnings={str(i):dict(number=int(v.number),lastinfo=int(v.lastinfo)) for i,v in enumerate(data.warning) if v.number})
 raw=json.dumps(encode(payload),separators=(',',':'),allow_nan=False).encode();temporary=path.with_name(path.name+'.tmp')
 with temporary.open('wb') as stream:
  np.savez_compressed(stream,integration=vector,payload=np.frombuffer(raw,dtype=np.uint8));stream.flush();os.fsync(stream.fileno())
 os.replace(temporary,path)


def restore(path,model,data,controller,scorer,expected_binding):
 with np.load(path,allow_pickle=False) as archive:
  vector=np.array(archive['integration'],copy=True);payload=decode(json.loads(archive['payload'].tobytes()))
 if payload.get('schema')!=1 or payload.get('kind')!='SUPPLEMENTAL_TRUE_INTEGRATION_CHECKPOINT' or payload.get('engine')!=mujoco.__version__:raise ValueError('Unsupported integration checkpoint')
 if payload.get('binding')!=expected_binding:raise ValueError('Checkpoint source, model or run configuration changed')
 if vector.shape!=(mujoco.mj_stateSize(model,STATE),) or not np.isfinite(vector).all():raise ValueError('Checkpoint physical state is malformed')
 cs=payload['controller'];ss=payload['scorer']
 if set(cs['fields'])!=set(controller.__dict__)-{'spec','phases','motion'}:raise ValueError('Controller computational fields changed')
 if set(ss['fields'])!=set(scorer.__dict__)-{'spec','defs','result'}:raise ValueError('Scorer computational fields changed')
 for side,state in cs['motion'].items():
  if set(state)!=set(controller.motion[side].__dict__)-{'ik'}:raise ValueError('Motion computational fields changed')
 # Validation finishes before any restored physical or policy state is applied.
 result=type(scorer.result)(**ss['result'])
 mujoco.mj_setState(model,data,vector,STATE)
 controller.__dict__.update(cs['fields'])
 for side,state in cs['motion'].items():controller.motion[side].__dict__.update(state)
 scorer.__dict__.update(ss['fields']);scorer.result=result
 return payload


def recover_trace(path,offset,expected_sha256):
 if offset<0 or not path.is_file() or path.stat().st_size<offset:raise ValueError('Checkpoint trace prefix is missing')
 digest=hashlib.sha256()
 with path.open('rb') as stream:
  remaining=offset
  while remaining:
   chunk=stream.read(min(1024*1024,remaining));digest.update(chunk);remaining-=len(chunk)
  tail=stream.read()
 if digest.hexdigest()!=expected_sha256:raise ValueError('Checkpoint trace prefix was changed')
 if tail:
  excluded=path.with_name('interrupted-tail-'+hashlib.sha256(tail).hexdigest()[:16]+'.jsonl')
  if excluded.exists() and excluded.read_bytes()!=tail:raise ValueError('Interrupted-tail preservation path collided')
  excluded.write_bytes(tail)
  with path.open('r+b') as stream:stream.truncate(offset)
 return digest
