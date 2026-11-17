"""Stock 630-hull YAM + ordinary tweezer approach to one real open-bank pocket.
Static held-tool/support hypotheses only; no loaded pickup/assembly certificate.
"""
from pathlib import Path
import sys,json
sys.path.insert(0,'/workspace/robocurve-cpu-deps')
D=Path(__file__).resolve().parent;R=D.parents[2]
sys.path.insert(0,str(R/'research/robocurve-implementation'))
import numpy as np,fcl
from scipy.spatial.transform import Rotation
from common.access import Access,mesh
from sections import source_mesh
A=Access()
# The original full-size leg is supported through its proximal base only.
# The right hand is hypothesized to support the source foot rim; no extra foot clamp.
fixtures=[(.43,0,.98),(.48,-.03,1.03)]
RT=np.array([[0,0,1],[0,-1,0],[1,0,0]],float)
# Authored ordinary120mm tweezer envelope, not custom robot fingers or OEM CAD.
# Handle 5x2.5mm, shafts 80mm, distal tips .5x1mm. Tool manipulation not proven.
tool=[('handle',fcl.Box(.005,.0025,.045),np.eye(3),np.array([0,0,.134])),
      ('shaft0',fcl.Box(.002,.001,.068),np.eye(3),np.array([0,-.001,.192])),
      ('shaft1',fcl.Box(.002,.001,.068),np.eye(3),np.array([0,.001,.192])),
      ('tip0',fcl.Box(.001,.0005,.028),np.eye(3),np.array([0,-.00075,.240])),
      ('tip1',fcl.Box(.001,.0005,.028),np.eye(3),np.array([0,.00075,.240]))]
# Tool tip is120mm beyond the existing gripper TCP134mm from gripper frame.
adj={frozenset([j['parent'],j['child']]) for j in A.r.joints};adj.add(frozenset(['tip_left','tip_right']))
def objs(q,side):
 poses=A.r.fk(q,side)[0];out=[]
 for h,g in zip(A.r.hulls,A.geoms):
  T=poses[h['link']];out.append((h['link'],fcl.CollisionObject(g,fcl.Transform(T[:3,:3],T[:3,3]))))
 return out

def collide(a,b):return bool(fcl.collide(a,b,fcl.CollisionRequest(),fcl.CollisionResult()))
def run(origin,tool_angle):
 Rt=Rotation.from_euler("y",-np.deg2rad(tool_angle)).as_matrix()@RT
 origin=np.array(origin);entries=[]
 for name in ['lower_leg_structure_base.STL','foot_structure.STL','lower_leg_structure_fork.STL']:
  m=source_mesh(name);v=np.array(m.vertices)*.001
  offset=origin+(np.array([-.15,.12,-.12]) if 'fork' in name else 0)
  entries.append((name,mesh(v,np.asarray(m.faces,np.int32)),np.eye(3),offset))
 entries += [('table',fcl.Box(1.1,1.3,.06),np.eye(3),np.array([.36,0,.7175])),
             ('proximal-leg-support',fcl.Box(.035,.035,.035),np.eye(3),origin+[.025,0,.145])]
 # Conservative source-role electronics/pin envelopes; positions/thickness are
 # not registered circuit CAD. Keep them as uncertain obstacles, not delete them.
 for x in [-.009,.009]:entries.append(('PCB-envelope',fcl.Cylinder(.005,.0016),Rotation.from_euler('y',np.pi/2).as_matrix(),origin+[x,0,0]))
 entries.append(('guide-pin',fcl.Cylinder(.00075,.012),np.eye(3),origin+[0,0,.015]))
 obstacles=[(name,fcl.CollisionObject(g,fcl.Transform(r,p))) for name,g,r,p in entries]
 # Support grasp of the27mm original foot, approaching from below.
 RR=RT
 qr,er=A.ik(origin,RR,side='right',gap=.027)
 target=origin+[-.002123,.00933,0]
 keys=[];ik=[];qprev=A.qready.copy()
 for label,dx in [('approach',-.080),('preinsert',-.020),('pocket',0),('withdraw',-.080)]:
  tcp=target+[dx,0,0]-.120*Rt[:,2];q,e=A.ik(tcp,Rt,seed=qprev,gap=.005);qprev=q
  keys.append((label,q));ik.append(dict(stage=label,**e))
 samples=[]
 for k in range(len(keys)-1):
  for u in np.linspace(0,1,13):
   q=keys[k][1]*(1-u)+keys[k+1][1]*u;left=objs(q,'left');right=objs(qr,'right');hits=[];selfhits=[];toolhits=[]
   for side,group in [('left',left),('right',right)]:
    for link,body in group:
     for name,other in obstacles:
      if side=='right' and link.startswith('tip') and name=='foot_structure.STL':continue # intended rim support only
      if collide(body,other):hits.append([side,link,name]);break
     if hits:break
    if hits:break
   if any(collide(a,b) for _,a in left for _,b in right):selfhits.append('arm-arm')
   # Source URDF adjacency only; no custom palms/wrists omitted.
   for side,group in [('left',left),('right',right)]:
    seen=False
    for ii,(la,a) in enumerate(group):
     for lb,b in group[ii+1:]:
      if la==lb or frozenset([la,lb]) in adj:continue
      if collide(a,b):selfhits.append(side+':'+la+'/'+lb);seen=True;break
     if seen:break
   G=A.r.fk(q,'left')[0]['gripper']
   for name,g,rot,p in tool:
    T=np.eye(4);T[:3,:3]=rot;T[:3,3]=p;T=G@T;ob=fcl.CollisionObject(g,fcl.Transform(T[:3,:3],T[:3,3]))
    for nn,other in obstacles:
     if collide(ob,other):toolhits.append([name,nn]);break
    if any(collide(ob,b) for _,b in right):toolhits.append([name,'support-arm'])
   samples.append(dict(segment=keys[k][0]+'->'+keys[k+1][0],fraction=float(u),robot_obstacle=hits[:1],self_collision=selfhits[:2],tool_obstacle=toolhits[:3]))
 return dict(tool_angle_deg=tool_angle,foot_center_m=origin.tolist(),support_IK=er,tool_IK=ik,
  left_keyframes=[dict(stage=n,q=q.tolist()) for n,q in keys],right_support_q=qr.tolist(),samples=samples,
  summary=dict(sampled_poses=len(samples),robot_obstacle_poses=sum(bool(x['robot_obstacle']) for x in samples),self_collision_poses=sum(bool(x['self_collision']) for x in samples),tool_obstacle_poses=sum(bool(x['tool_obstacle']) for x in samples)))

if __name__=='__main__':
 cases=[run(x,angle) for x in fixtures for angle in [0,15,30,40]]
 out=dict(robot_pin=A.r.data['pin'],hulls_per_arm=len(A.r.hulls),cases=cases,
  scope='One pocket approach/withdrawal with original source geometry and full stock hands. Static support and held-tool hypotheses, not continuous collision or loaded acquisition proof.',
  unknown=['Tool jaw-force/elastic response and stock-pad gripping wrench','Ring seating/release while squeezed; capture of both banks without extra support','Actual PCB axial registration and wire routing','Continuous sweeps between finite samples','Whole twelve-element assembly, fork closure and optical output'])
 (D/'results/YAM_ACCESS.json').write_text(json.dumps(out,indent=2,default=lambda v:v.item() if isinstance(v,np.generic) else str(v))+'\n')
 print(json.dumps([dict(IK_failures=sum(not x['valid'] for x in a['tool_IK'])+int(not a['support_IK']['valid']),**a['summary']) for a in cases],indent=2))
