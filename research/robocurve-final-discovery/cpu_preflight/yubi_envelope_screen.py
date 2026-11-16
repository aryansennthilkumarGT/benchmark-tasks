"""One bounded CPU geometry screen. No band physics, grasp proof or native simulator.
Actual YAM convex hulls vs conservative per-occurrence exact STEP bounding boxes.
Disjointness certifies separation of these envelopes; overlap is INCONCLUSIVE.
"""
from pathlib import Path
import datetime,hashlib,itertools,json,sys
import numpy as np
D=Path(__file__).resolve().parent; R=D.parent.parent/'robocurve-acceptance'/'preflight'
sys.path.insert(0,str(R))
from access_core import Robot,points_at,transform,convex_intersects,aabb_separated,aabb
P=D.parent/'agents/robot_build/evidence/yubi/assembly-occurrences.json'
source=json.loads(P.read_text());robot=Robot()
# Genuine hook face5 and repeated cylindrical pivot from analytic STEP inspection.
H=np.array([-22.055430442,9.919948188,1035.0])*1e-3
q=np.array(robot.data['ready_joint_radians']+[-.004,-.004])
poses,_=robot.fk(q,'left');tcp=robot.tcp(q,'left');gR=poses['gripper'][:3,:3]
hulls=robot.world_hulls(q,'left')+robot.world_hulls(q,'right')
for h in hulls:h['bounds']=aabb(h['world'])
parts=[]
for row in source['leaf_occurrences']:
 if row['name']=='MetaQuestTouchPlus_Right':continue # step12 follows band step11
 lo=np.array(row['bounds_mm'][:3])*1e-3;hi=np.array(row['bounds_mm'][3:])*1e-3
 v=np.array(list(itertools.product(*zip(lo,hi))))
 parts.append({'index':row['index'],'name':row['name'],'corners':v})
def check(Rm,t):
 hits=[];near=0
 for p in parts:
  v=p['corners']@Rm.T+t;bb=aabb(v)
  for h in hulls:
   if aabb_separated(h['bounds'],bb):continue
   near+=1
   if convex_intersects(h['world'],v):hits.append([p['index'],h['link'],h['name']])
 return {'conservatively_clear':not hits,'overlapping_envelope_pairs':len(hits),'broadphase_candidates':near,'first_pairs':hits[:8]}
# Keep pivot vertical; this is an ordinary supported assembly orientation and removes
# gravity as a potential source of falsely demonstrated spring return. No fixture
# geometry is modeled, so this is ONLY a hand/assembly separation screen.
C=np.array([[0.,0.,1.],[1.,0.,0.],[0.,1.,0.]])
rows=[]
for yaw in [-90,-60,-30,0,30,60,90]:
 T=transform(rpy=(0,0,np.deg2rad(yaw)));Rm=T[:3,:3]@C
 for standoff in [0.,.004,.012,.025]:
  # TCP is a target in the free approach volume, not a modeled band purchase.
  target=tcp+gR[:,2]*standoff;t=target-Rm@H
  zmin=min(float((p['corners']@Rm.T+t)[:,2].min()) for p in parts)
  r=check(Rm,t);r.update(yaw_deg=yaw,hook_ahead_of_tcp_mm=1000*standoff,source_assembly_lowest_world_z_m=zmin,source_to_world=np.vstack([np.c_[Rm,t],[0,0,0,1]]).tolist());rows.append(r)
# Controls exercise the same exact robot hulls and source occurrence envelopes.
far=check(C,np.array([2.,0.,2.])-C@H)
grip=next(p for p in parts if p['name']=='GRIP')['corners'].mean(0)
palm=(poses['gripper']@np.array([0,0,.025,1]))[:3]
bad=check(C,palm-C@grip)
assert far['conservatively_clear'],'Far separated control failed'
assert not bad['conservatively_clear'],'Palm-overlap negative control was missed'
out={'kind':'one bounded CPU source-envelope screen; not a contact or assembly simulation','source_pin':'dd8bd13d2fd8e5003057243576f88be333d95fc5','source_assembly_sha256':source['source_sha256'],'occurrence_manifest_sha256':hashlib.sha256(P.read_bytes()).hexdigest(),'robot_reference_sha256':robot.bundle_sha256,'robot_hulls_per_arm':len(robot.hulls),'total_robot_hulls_tested':len(hulls),'source_occurrences_tested':len(parts),'source_excluded':'MetaQuestTouchPlus_Right only, because original instruction installs it after band','units':'metres internally; original STEP mm converted once','source_hook_face5_mm':(H*1000).tolist(),'joint_coordinates_each_arm':q.tolist(),'left_TCP_m':tcp.tolist(),'cases':rows,'controls':{'far_separated':far,'source_grip_envelope_in_palm_negative':bad},'summary':{'sampled_static_placements':len(rows),'conservatively_clear':sum(x['conservatively_clear'] for x in rows),'overlapping_or_inconclusive':sum(not x['conservatively_clear'] for x in rows)},'not_tested':['No rubber band body, acquisition, slip, spring torque or retention','No holder-hook saddle identification: it remains unresolved in source interpretation','No continuous motion/fixture/table/arm-self collision certificate; only the two actual arms versus source assembly envelopes','No full bimanual route, tool manipulation, native expert or model evaluation'],'interpretation':'Clear rows prove only static empty-hand separation from conservative STEP occurrence envelopes at one actual source hook. Overlap is not proof of actual CAD collision. Gap8mm is a declared approach setting, not a verified loop grasp. Neither result establishes task success.'}
(D/'YUBI_ENVELOPE_RESULT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'summary':out['summary'],'controls':{k:v['conservatively_clear'] for k,v in out['controls'].items()},'hulls':len(hulls),'parts':len(parts)},indent=2))
