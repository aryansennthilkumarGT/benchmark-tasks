"""Independently enumerate root-cause pairs in the previous ODRI support pose."""
from pathlib import Path
import sys,json,hashlib,copy
sys.path.insert(0,'/workspace/robocurve-cpu-deps')
D=Path(__file__).resolve().parent;R=D.parents[2]
sys.path.insert(0,str(R/'research/robocurve-implementation'))
sys.path.insert(0,str(R/'research/robocurve-next-prototype/odri'))
import numpy as np,fcl,cadquery as cq
from common.access import Access,mesh
from sections import source_mesh,S
A=Access()

def object_at(g,T):return fcl.CollisionObject(g,fcl.Transform(T[:3,:3],T[:3,3]))
def contact(a,b):
 result=fcl.CollisionResult();n=fcl.collide(a,b,fcl.CollisionRequest(num_max_contacts=10,enable_contact=True),result)
 return [dict(position_m=np.array(c.pos).tolist(),normal=np.array(c.normal).tolist(),penetration_mm=float(c.penetration_depth*1000)) for c in result.contacts] if n else []

if __name__=='__main__':
 prior=json.loads((R/'research/robocurve-next-prototype/odri/results/YAM_ACCESS.json').read_text())
 base=source_mesh('lower_leg_structure_base.STL');foot=source_mesh('foot_structure.STL')
 bg=mesh(np.array(base.vertices)*.001,np.array(base.faces,np.int32));fg=mesh(np.array(foot.vertices)*.001,np.array(foot.faces,np.int32))
 # Analytic original STEP, transformed once to the same foot-centre millimetre frame.
 solid=cq.importers.importStep(str(S/'lower_leg_structure_base.STEP')).val().translate((0,0,160))
 cases=[];identical_configurations={}
 for index,row in enumerate(prior['cases']):
  q=np.array(row['right_support_q']);origin=np.array(row['foot_center_m']);poses=A.r.fk(q,'right')[0]
  key=(tuple(q),tuple(origin))
  if key in identical_configurations:
   original=identical_configurations[key]
   result=copy.deepcopy(cases[original]);result['prior_layout']=index
   result['identical_configuration_reused_from']=original
   cases.append(result)
   print(index,'identical source/robot configuration; reuse analytic audit of layout',original,flush=True)
   continue
  identical_configurations[key]=index
  T=np.eye(4);T[:3,3]=origin;b=object_at(bg,T);f=object_at(fg,T);hits=[];dist={}
  for h,g in zip(A.r.hulls,A.geoms):
   ob=object_at(g,poses[h['link']]);cs=contact(ob,b)
   if cs:
    world=np.array(h['vertices'])@poses[h['link']][:3,:3].T+poses[h['link']][:3,3]
    local=(world-origin)*1000
    # An intrusion needs a witness, not a full census. Bound this expensive
    # analytic query and retain enough points for the boundary-distance audit.
    inside=[];probed=0
    for p in local:
     probed+=1
     if solid.isInside(cq.Vector(*p),1e-7):inside.append(p.tolist())
     if len(inside)==20:break
    hits.append(dict(link=h['link'],hull=h['name'],contacts=cs,
      analytic_vertices_probed=probed,source_base_contains_robot_hull_vertices_mm=inside))
   if h['link'].startswith('tip'):
    rr=fcl.DistanceResult();dd=fcl.distance(ob,f,fcl.DistanceRequest(enable_nearest_points=True),rr)
    dist[h['link']]=min(float(dd),dist.get(h['link'],1e9))
  cases.append(dict(prior_layout=index,origin_m=origin.tolist(),support_IK=row['support_IK'],actual_TCP_error_mm=float(np.linalg.norm(A.r.tcp(q,'right')-origin)*1000),base_collisions=hits,tip_to_foot_min_distance_m=dist))
  print(index,'hits',[(x['link'],x['hull'],len(x['source_base_contains_robot_hull_vertices_mm'])) for x in hits],flush=True)
 # Verify registered mesh/source bounds and SI conversion independently.
 bb=solid.BoundingBox();expected=np.array([[bb.xmin,bb.ymin,bb.zmin],[bb.xmax,bb.ymax,bb.zmax]])*.001
 errors=float(np.max(np.abs(base.bounds*.001-expected)))
 out=dict(robot_pin=A.r.data['pin'],hulls_per_arm=len(A.r.hulls),distinct_support_configurations=len(identical_configurations),registration_bounds_error_m=errors,mesh_bounds_m=(base.bounds*.001).tolist(),STEP_bounds_m=expected.tolist(),cases=cases,
  analytic_containment_scope='Up to 20 positive witnesses per intersecting hull, not a census of contained vertices. Identical full q/origin configurations reuse their exact analytic audit.',
  conclusion='Exact stock collision-hull/source-base intersection, not an allowed foot-rim contact. All source transforms and metre conversion agree. Hull/STEP vertex containment independently verifies genuine intrusions.')
 assert errors<1e-6
 assert all(any(x['link']=='tip_right' for x in c['base_collisions']) for c in cases)
 assert all(any(x['source_base_contains_robot_hull_vertices_mm'] for x in c['base_collisions']) for c in cases)
 (D/'results/ROOT_CAUSE.json').write_text(json.dumps(out,indent=2)+'\n')
 print('SOURCE_BASE_COLLISION_CONFIRMED')
