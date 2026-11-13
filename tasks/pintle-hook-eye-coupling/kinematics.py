"""Rigid joint reconstruction for QA only, never simulator actuation."""
import numpy as np
from motion import rotate,multiply,axis_quat

def reconstruct(spec,root,joints):
 a=next(a for a in spec['assemblies'] if a['name']=='pintle_hook_asset')
 poses={'hook_body':dict(pos=list(root['pos']),quat=list(root['quat']))};pending=list(a['joints'])
 while pending:
  progressed=False
  for j in pending[:]:
   if j['parent'] not in poses:continue
   p=poses[j['parent']];axis={'X':[1,0,0],'Y':[0,1,0],'Z':[0,0,1]}[j['axis']];v=joints[j['name']]
   q=multiply(p['quat'],axis_quat(axis,v)) if j['kind']=='revolute' else np.asarray(p['quat'])
   offset=np.asarray(j['pivot_parent'])+(np.asarray(axis)*v if j['kind']=='prismatic' else 0.)
   pos=np.asarray(p['pos'])+rotate(p['quat'],offset)-rotate(q,j['pivot_child'])
   poses[j['child']]=dict(pos=pos.tolist(),quat=q.tolist());pending.remove(j);progressed=True
  if not progressed:raise ValueError('Disconnected or cyclic hook assembly')
 return poses
