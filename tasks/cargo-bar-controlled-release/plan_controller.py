"""Original complete robot phase plan for controlled cargo-bar unloading.

Native states locate real interfaces and confirm release/retraction. Nominal body
poses are only offline geometry references, never simulator writes. Cam lift
references come from separately labelled, exact-scene MuJoCo fixture observations.
"""
import copy,hashlib,json,math
from pathlib import Path
import numpy as np
from yam_arena.demo import DOWN_GRIP
from motion import rotate,multiply,axis_quat,conjugate
from kinematics import reconstruct
HERE=Path(__file__).resolve().parent


def make_plan(spec,reference):
 if reference['scene_sha256']!=hashlib.sha256((HERE/'scene.json').read_bytes()).hexdigest():raise ValueError('Cam reference belongs to different scene geometry')
 root=next(b for a in spec['assemblies'] for b in a['bodies'] if b['name']=='outer_tube');root=copy.deepcopy(dict(pos=root['pos'],quat=root['quat']))
 frame=next(b for a in spec['assemblies'] for b in a['bodies'] if b['name']=='wall_frame');js=spec['initial_joint_values'].copy();phases=[]
 down=DOWN_GRIP.tolist();sideways=multiply(axis_quat([0,0,1],-math.pi/2),down).tolist();base=root['quat']
 def nominal():
  return dict(wall_frame=dict(pos=frame['pos'],quat=frame['quat']),**reconstruct(spec,root,js))
 def phase(label,side,target,tool,opening,contact=None,width=0.,dwell=.15,speed=.045,checks=None,
           reference_body=None,reference_offset=None,reference_quat=None,world_offset=None,live=False,**extra):
  p=dict(label=label,side=side,target=dict(pos=list(target),quat=list(tool)),opening=opening,contact_body=contact,
         grasp_width=width,contact_bodies=([contact,'release_trigger'] if contact=='handle' and width else [contact] if contact else []),dwell=dwell,speed=speed,timeout=45.,position_tolerance=.00035,angle_tolerance=.025,
         joint_checks=checks or [],nominal_bodies=nominal(),nominal_joints=js.copy(),reference_live=live,**extra)
  if reference_body:p.update(reference_body=reference_body,reference_offset=list(reference_offset),reference_quat=list(reference_quat),world_offset=list(world_offset or [0,0,0]))
  phases.append(p)
 def point(body,local,up):
  b=nominal()[body];return (np.array(b['pos'])+rotate(b['quat'],local)+[0,0,up]).tolist()
 local_side=multiply(conjugate(base),sideways).tolist()
 def inner(label,opening,width=0.,up=.010,dwell=.15,live=False,checks=None):
  phase(label,'left',point('inner_tube',[0,.24,0],up),sideways,opening,'inner_tube',width,dwell=dwell,
        reference_body='inner_tube',reference_offset=[0,.24,0],reference_quat=local_side,world_offset=[0,0,up],live=live,checks=checks)
 def handle(label,phi,opening=.20,width=.0255,dwell=.10,checks=None,live=True,**extra):
  local=np.array([0,0,-.032])+rotate(axis_quat([1,0,0],phi),[.054,.06325,0]);tool=multiply(axis_quat([0,0,1],phi),down)
  target=(np.array(root['pos'])+rotate(base,local)+[0,0,.024]).tolist()
  phase(label,'right',target,tool,opening,'handle',width,dwell=dwell,speed=.020,
        reference_body='outer_tube',reference_offset=local,reference_quat=multiply(conjugate(base),tool),world_offset=[0,0,.024],
        live=live,checks=checks,**extra)
 def check(name,lo,hi,angular=False):return dict(name=name,min=lo,max=hi,angular=angular)
 phase('Initialize support arm','left',[.24,.25,.92],sideways,1.)
 inner('Approach inner tube support',1.,up=.090)
 inner('Reach inner tube support',.55)
 inner('Grip loaded inner tube',.18,.025,dwell=.5)
 phase('Initialize release arm','right',[.23,-.16,.92],down,1.)
 handle('Approach latch and handle',0,opening=.55,width=0,dwell=.1)
 # Approach at vertical clearance first; keep exact target/reference consistent.
 phases[-1]['target']['pos'][0]-=.072;phases[-1]['reference_offset'][2]+=.072
 handle('Reach latch and handle',0,opening=.50,width=0)
 js['trigger_pull']=.0083
 handle('Squeeze latch release',0,dwell=.4,checks=[check('trigger_pull',.007,.0093)])
 rows=sorted(reference['checks'],key=lambda r:r['joints']['handle_rotation']);angles=np.array([r['joints']['handle_rotation'] for r in rows])
 phi=2.6;js['handle_rotation']=phi
 for name in ('holding_pawl_rotation','driving_pawl_rotation'):js[name]=float(np.interp(phi,angles,[r['joints'][name] for r in rows]))
 handle('Open handle on its physical circular path',phi,dwell=.1,
        arc=dict(angle=phi,pivot=[0,0,-.032],grip=[.054,.06325,0],world_offset=[0,0,.024],tool_zero=multiply(conjugate(base),down).tolist()),
        checks=[check('handle_rotation',2.55,2.63,True),check('trigger_pull',.007,.0093)])
 handle('Verify both physical pawls clear',2.6,dwell=.3,pawls_clear=True,checks=[check('handle_rotation',2.45,2.63,True)])
 handle('Hold outer tube through released handle',2.6,dwell=.2,live=False,pawls_clear=True)
 # Left hand feeds the real inner tube while the right hand anchors the outer
 # tube through its held handle. The pinion must backdrive through real contacts.
 js['telescope']=.003;js['pinion_rotation']=-.003/spec['parameters']['authored_pinion_pitch_radius'];js['right_compliance']=0.
 local=np.array([0,.24+.003,0]);tool=sideways
 phase('Retract controlled inner tube','left',(np.array(root['pos'])+rotate(base,local)+[0,0,.010]).tolist(),tool,.18,'inner_tube',.025,
       speed=.005,checks=[check('telescope',0.,.0045)],reference_body='outer_tube',reference_offset=local,
       reference_quat=local_side,world_offset=[0,0,.010],live=True)
 inner('Release shortened inner tube',.55)
 inner('Withdraw support fingers',.7,up=.090)
 phase('Park support arm','left',[.24,.25,.92],sideways,1.)
 # The inner tube is now free; one held handle translates/lowers the bar onto
 # the two diameter-matched cradles. This never sets a task pose in the simulator.
 root['pos'][1]=0.;js['left_compliance']=0.
 phi=2.6;local=np.array([0,0,-.032])+rotate(axis_quat([1,0,0],phi),[.054,.06325,0]);tool=multiply(axis_quat([0,0,1],phi),down)
 def place(label,root_target,speed=.010):
  root['pos']=list(root_target)
  phase(label,'right',(np.array(root_target)+rotate(base,local)+[0,0,.024]).tolist(),tool,.20,'handle',.0255,
        speed=speed,root_target=list(root_target),checks=[check('left_compliance',0.,.0005),check('right_compliance',-.0005,0.)])
 place('Clear both wall faces',[root['pos'][0],0.,root['pos'][2]])
 place('Lower unloaded bar onto cradles',spec['parameters']['authored_cradle_root'],speed=.004)
 js['trigger_pull']=0.
 phase('Release supported handle','right',(np.array(root['pos'])+rotate(base,local)+[0,0,.024]).tolist(),tool,.50,'handle',0.,dwell=.3)
 phase('Withdraw release fingers','right',(np.array(root['pos'])+rotate(base,local)+[0,0,.070]).tolist(),tool,.70)
 phase('Park release arm','right',[.23,-.16,.92],down,1.)
 phase('Released unloaded bar hold','right',[.23,-.16,.92],down,1.,dwell=2.5,require_still=True,
       checks=[check('telescope',0.,.006),check('left_compliance',0.,.0005),check('right_compliance',-.0005,0.)])
 return dict(schema=1,feedback='READ_ONLY_NATIVE_PHYSICAL_STATE_AND_ROBOT_PROPRIOCEPTION',
             nominal_pose_basis='Exact-scene MuJoCo fixture pawl observations and explicit ideal grasp/placement assumptions; no Isaac or robot demonstration.',phases=phases)

if __name__=='__main__':
 from mechanism_cpu import probe
 spec=json.loads((HERE/'scene.json').read_text());reference=probe(HERE)
 if not reference['passed']:raise SystemExit('CPU cam reference failed; do not author a nominal plan from it')
 reference['scene_sha256']=hashlib.sha256((HERE/'scene.json').read_bytes()).hexdigest()
 (HERE/'cam-reference.json').write_text(json.dumps(reference,indent=2)+'\n')
 (HERE/'controller.json').write_text(json.dumps(make_plan(spec,reference),indent=2)+'\n')
