"""Joint-frame reconstruction for consistency auditing, never native body writes."""
import numpy as np
try:
 from .motion import rotate,multiply,axis_quat
except ImportError:
 from motion import rotate,multiply,axis_quat

def reconstruct(spec,root,joints):
 a=next(a for a in spec['assemblies'] if a['name']=='sds_holder_asset');poses={'tool_holder':dict(pos=list(root['pos']),quat=list(root['quat']))};pending=list(a['joints'])
 while pending:
  for j in pending[:]:
   if j['parent'] not in poses:continue
   p=poses[j['parent']];axis={'X':[1,0,0],'Y':[0,1,0],'Z':[0,0,1]}[j['axis']];value=joints[j['name']];q=multiply(p['quat'],axis_quat(axis,value)) if j['kind']=='revolute' else p['quat'];offset=np.asarray(j['pivot_parent'])+np.asarray(axis)*value
   pos=np.asarray(p['pos'])+rotate(p['quat'],offset)-rotate(q,j['pivot_child']);poses[j['child']]=dict(pos=pos.tolist(),quat=list(q));pending.remove(j)
  if pending:raise ValueError('Disconnected or unsupported fixture joint tree')
 return poses
