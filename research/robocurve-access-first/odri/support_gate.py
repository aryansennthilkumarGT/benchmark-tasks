"""Bounded necessary-condition access tests; never a grasp/carry demonstration.
All original hulls and known source solids remain. Missing tread geometry blocks
acceptance even if a conditional bare-rim target is clear.
"""
from pathlib import Path
import sys,json,importlib.util
sys.path.insert(0,'/workspace/robocurve-cpu-deps')
D=Path(__file__).resolve().parent;R=D.parents[2]
sys.path.insert(0,str(R/'research/robocurve-implementation'))
sys.path.insert(0,str(R/'research/robocurve-next-prototype/odri'))
import numpy as np,fcl
from functools import lru_cache
from scipy.spatial.transform import Rotation
from common.access import Access,mesh
from sections import source_mesh
sys.path.insert(0,str(D.parent/"common"))
from ordinary_tool import parts as tool_parts
A=Access();RT=np.array([[0,0,1],[0,-1,0],[1,0,0]],float)
ADJ={frozenset([j['parent'],j['child']]) for j in A.r.joints}

def ob(g,rot,pos):return fcl.CollisionObject(g,fcl.Transform(rot,pos))
def hit(a,b):return bool(fcl.collide(a,b,fcl.CollisionRequest(),fcl.CollisionResult()))
def robot(q,side):
 P=A.r.fk(q,side)[0]
 return [(h['link'],h['name'],ob(g,P[h['link']][:3,:3],P[h['link']][:3,3])) for h,g in zip(A.r.hulls,A.geoms)]
def manager(items):
 m=fcl.DynamicAABBTreeCollisionManager();m.registerObjects([x[-1] for x in items]);m.setup();return m

@lru_cache(maxsize=4096)
def self_pairs(q,side):
 items=robot(np.array(q),side);groups={}
 for link,name,body in items:groups.setdefault(link,[]).append((link,name,body))
 managers={link:manager(obs) for link,obs in groups.items()};out=[];links=list(groups)
 for i,la in enumerate(links):
  for lb in links[i+1:]:
   if frozenset([la,lb]) in ADJ:continue
   data=fcl.CollisionData();managers[la].collide(managers[lb],data,fcl.defaultCollisionCallback)
   if data.result.is_collision:out.append([side,la,lb])
 return out

def scene(origin):
 out=[]
 for name in ['lower_leg_structure_base.STL','foot_structure.STL','lower_leg_structure_fork.STL']:
  m=source_mesh(name);g=mesh(np.array(m.vertices)*.001,np.array(m.faces,np.int32))
  p=origin+(np.array([-.15,.12,-.12]) if 'fork' in name else 0)
  out.append((name,ob(g,np.eye(3),p)))
 top=.7475;height=float(origin[2]+.145-top)
 out += [('table',ob(fcl.Box(1.1,1.3,.06),np.eye(3),[.36,0,.7175])),
         ('proximal-support-post',ob(fcl.Box(.025,.04,height),np.eye(3),origin+[.045,0,-height/2+.145])),
         ('proximal-support-bracket',ob(fcl.Box(.06,.04,.02),np.eye(3),origin+[.025,0,.145])),
         ('annulus-tray',ob(fcl.Box(.05,.06,.012),np.eye(3),[.23,.18,.7535]))]
 # Ordinary unheld tweezers lie in a bench cradle. No gripper attachment exists.
 for label,g,local in tool_parts():out.append(('unheld-'+label,ob(g,RT,np.array([.25,-.18,.77])+RT@local)))
 out.append(('tool-cradle',ob(fcl.Box(.04,.025,.02),np.eye(3),[.25,-.18,.7575])))
 for x in [-.009,.009]:out.append(('uncertain-PCB-envelope',ob(fcl.Cylinder(.005,.0016),Rotation.from_euler('y',np.pi/2).as_matrix(),origin+[x,0,0])))
 out.append(('source-size-guide-pin',ob(fcl.Cylinder(.00075,.012),np.eye(3),origin+[0,0,.0159])))
 return out

def evaluate(ql,qr,obstacles,origin,allow_rim=False):
 L=robot(ql,'left');RR=robot(qr,'right');pairs=[];rim_contacts=0
 for side,rs in [('left',L),('right',RR)]:
  for link,name,body in rs:
   for label,other in obstacles:
    result=fcl.CollisionResult();n=fcl.collide(body,other,fcl.CollisionRequest(num_max_contacts=4,enable_contact=True),result)
    if not n:continue
    if side=='right' and link.startswith('tip') and label=='foot_structure.STL' and allow_rim:
     points=[(np.array(c.pos)-origin)*1000 for c in result.contacts]
     if points and all(np.hypot(p[1],p[2])>=12.5 and abs(p[0])<=8.4 for p in points):rim_contacts+=1;continue
    pairs.append([side,link,name,label])
 lm,rm=manager(L),manager(RR);data=fcl.CollisionData();lm.collide(rm,data,fcl.defaultCollisionCallback)
 arm_pair=[]
 if data.result.is_collision:
  # Identify an actual link/hull pair, independently of manager callback identity.
  for la,na,a in L:
   for lb,nb,b in RR:
    if hit(a,b):arm_pair=[la,na,lb,nb];break
   if arm_pair:break
 own=self_pairs(tuple(ql),'left')+self_pairs(tuple(qr),'right')
 return dict(robot_source_pairs=pairs,arm_arm_pair=arm_pair,self_collision_pairs=own,allowed_original_rim_contacts=rim_contacts)

if __name__=='__main__':
 outputs=[]
 for origin in [np.array([.43,0,.98]),np.array([.48,-.03,1.03])]:
  obstacles=scene(origin)
  for dx in [-.003,-.006]:
   for roll in range(0,360,45):
    rot=RT@Rotation.from_euler('z',np.deg2rad(roll)).as_matrix();target=origin+[dx,0,0]
    pre,ep=A.ik(target-.06*rot[:,2],rot,side='right',gap=.035)
    qr,et=A.ik(target,rot,side='right',seed=pre,gap=.027)
    qopen=qr.copy();qopen[6:]=-.035/2
    targetcheck=evaluate(A.qready,qr,obstacles,origin,allow_rim=True)
    first=None;sample_count=0
    if not ep['valid']:first=dict(stage='support_approach_IK',reason='numerical IK did not solve',detail=ep)
    elif not et['valid']:first=dict(stage='support_acquisition_IK',reason='numerical IK did not solve',detail=et)
    else:
     # Acquisition/approach first. Endpoint collision is a rigorous path rejection;
     # clear finite samples would still require continuous certification/purchase.
     for stage,start,end,allowed in [('support_approach',A.qready,pre,False),('support_precontact',pre,qopen,False),('support_close',qopen,qr,True),('support_release',qr,qopen,True),('support_withdraw',qopen,pre,False)]:
      for u in np.linspace(0,1,9):
       q=start*(1-u)+end*u;sample_count+=1;e=evaluate(A.qready,q,obstacles,origin,allowed)
       if e['robot_source_pairs'] or e['arm_arm_pair'] or e['self_collision_pairs']:
        first=dict(stage=stage,fraction=float(u),reason='observed stock-hull collision',detail=e);break
      if first:break
    # Separate counterexample for simultaneous tool/support poses. It is not
    # executed transport: purchase/geometry gates have not passed.
    tooltarget=origin+[-.002123,.00933,0];ql,el=A.ik(tooltarget-[.120,0,0],RT,gap=.005)
    simultaneous=evaluate(ql,qr,obstacles,origin,True)
    G=A.r.fk(ql,'left')[0]['gripper'];toolpairs=[]
    for label,g,local in tool_parts():
     t=G@np.r_[local+[0,0,.134],1];body=ob(g,G[:3,:3],t[:3])
     for name,other in obstacles:
      if hit(body,other):toolpairs.append([label,name])
     for link,name,other in robot(qr,'right'):
      if hit(body,other):toolpairs.append([label,'support-arm',link,name]);break
    row=dict(origin_m=origin.tolist(),axial_shift_mm=dx*1000,roll_deg=roll,support_q=qr.tolist(),support_pre_q=pre.tolist(),IK=dict(approach=ep,acquisition=et),target_check=targetcheck,first_blocking_stage=first,sampled_configs=sample_count,
      simultaneous_counterexample=dict(tool_IK=el,**simultaneous,tool_pairs=toolpairs),
      tool_acquisition='NOT RUN: source/purchase/access gate did not pass',annulus_placement='NOT RUN',annulus_release='NOT RUN',continuous_certificate='NOT ESTABLISHED',accepted_complete_access=False)
    outputs.append(row);print(origin.tolist(),dx,roll,'first',None if first is None else first['stage'],'target pairs',len(targetcheck['robot_source_pairs']),'tool/arm',bool(toolpairs),flush=True)
 out=dict(ready_self_collision_pairs=self_pairs(tuple(A.qready),'left')+self_pairs(tuple(A.qready),'right'),self_exemptions='same-link and direct source-URDF adjacent links only; no sibling-finger exemption',hulls_per_arm=len(A.r.hulls),tested_support_templates=len(outputs),cases=outputs,
  geometry_limit='Actual three STEP solids are retained, along with both complete stock arms, table, stand, unheld tool and tray. Bonded tread profile is not specified by these STEP parts; the publisher drawing shows it, but no decoded matching tread solid is available. These necessary-condition bare-rim tests cannot establish a purchase on the complete assembled foot.',
  pose_scope='Counterexample configurations, not object transport or loaded manipulation.',decision='PARK ODRI: no accepted complete source-scale access/purchase route in the bounded pass')
 (D/'results/SUPPORT_GATE.json').write_text(json.dumps(out,indent=2,default=lambda v:v.item() if isinstance(v,np.generic) else str(v))+'\n')
