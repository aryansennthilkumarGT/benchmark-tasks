"""Rigid joint-frame reconstruction for consistency/audits, never simulator writes."""
import numpy as np
from motion import rotate,multiply,axis_quat


def reconstruct(spec,root,joints):
 assembly=next(a for a in spec['assemblies'] if a['name']=='cargo_bar_asset')
 poses={'outer_tube':dict(pos=list(root['pos']),quat=list(root['quat']))}
 pending=list(assembly['joints'])
 while pending:
  progress=False
  for j in pending[:]:
   if j['parent'] not in poses:continue
   p=poses[j['parent']];axis={'X':[1,0,0],'Y':[0,1,0],'Z':[0,0,1]}[j['axis']];value=joints[j['name']]
   q=multiply(p['quat'],axis_quat(axis,value)) if j['kind']=='revolute' else np.array(p['quat'])
   offset=np.array(j['pivot_parent'])
   if j['kind']=='prismatic':offset=offset+np.array(axis)*value
   pos=np.array(p['pos'])+rotate(p['quat'],offset)-rotate(q,j['pivot_child'])
   poses[j['child']]=dict(pos=pos.tolist(),quat=q.tolist());pending.remove(j);progress=True
  if not progress:raise ValueError('Joint tree is cyclic or disconnected')
 return poses
