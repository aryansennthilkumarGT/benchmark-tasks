"""Rigid joint-frame reconstruction for audits; never runtime object writes."""
import numpy as np
from motion import rotate,multiply,axis_quat


def reconstruct(spec,root,joints):
 assembly=next(a for a in spec['assemblies'] if a['name']=='nose_service_asset')
 poses={'nose_body':dict(pos=list(root['pos']),quat=list(root['quat']))};pending=list(assembly['joints'])
 while pending:
  progress=False
  for joint in pending[:]:
   if joint['parent'] not in poses:continue
   p=poses[joint['parent']];axis={'X':[1,0,0],'Y':[0,1,0],'Z':[0,0,1]}[joint['axis']];value=joints[joint['name']]
   q=multiply(p['quat'],axis_quat(axis,value)) if joint['kind']=='revolute' else np.asarray(p['quat'])
   offset=np.asarray(joint['pivot_parent'])+(np.asarray(axis)*value if joint['kind']=='prismatic' else 0.)
   pos=np.asarray(p['pos'])+rotate(p['quat'],offset)-rotate(q,joint['pivot_child'])
   poses[joint['child']]=dict(pos=pos.tolist(),quat=q.tolist());pending.remove(joint);progress=True
  if not progress:raise ValueError('Disconnected or cyclic service-fixture joint tree')
 return poses
