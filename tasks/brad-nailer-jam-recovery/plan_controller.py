"""Original bounded service plan. Nominal poses are offline assumptions only.

The executable controller acquires all grasps from live native body poses and
follows physical hinge circles. This file never writes simulator body state.
"""
import copy,json,math,hashlib
from pathlib import Path
import numpy as np
from yam_arena.demo import DOWN_GRIP
import dimensions as D
from motion import rotate,multiply,conjugate,axis_quat
from kinematics import reconstruct
HERE=Path(__file__).resolve().parent


def make_plan(spec):
 root=copy.deepcopy(spec['assemblies'][0]['bodies'][0]);js=spec['initial_joint_values'].copy()
 free={b['name']:dict(pos=b['pos'],quat=b['quat']) for a in spec['assemblies'][1:] for b in a['bodies']}
 ref=json.loads((HERE/'guided-cycle-reference.json').read_text())
 if ref['scene_sha256']!=hashlib.sha256((HERE/'scene.json').read_bytes()).hexdigest():raise ValueError('Stale fixture reference')
 opened=min(ref['checks'],key=lambda r:abs(r['time']-9))['joints']
 phases=[];down=np.array(DOWN_GRIP);side=np.array([-.5,-.5,-.5,.5]);base=np.array(root['quat'])
 right_pin=axis_quat([1,0,0],-(math.pi/2+.5))
 def states():return dict(**reconstruct(spec,root,js),**copy.deepcopy(free))
 def add(label,arm,target,opening=1.,body=None,width=0.,dwell=.15,speed=.05,**extra):
  phases.append(dict(label=label,side=arm,target=target,opening=opening,contact_body=body,grasp_width=width,
     dwell=dwell,speed=speed,timeout=45.,position_tolerance=.0004,angle_tolerance=.02,
     joint_checks=[],nominal_bodies=states(),nominal_joints=js.copy(),**extra))
 def grip(label,arm,body,local,tool,opening,width=0.,away=0.,dwell=.15,**extra):
  b=states()[body];rel=multiply(conjugate(b['quat']),tool);offset=np.asarray(local)+rotate(rel,[0,0,-away])
  target=dict(pos=(np.asarray(b['pos'])+rotate(b['quat'],offset)).tolist(),quat=list(tool))
  add(label,arm,target,opening,body,width,dwell=dwell,reference_body=body,reference_offset=offset.tolist(),reference_quat=rel.tolist(),**extra)
 def park(arm):add('Park '+arm+' arm',arm,dict(pos=[.23,.26 if arm=='left' else -.20,.97],quat=down.tolist()))
 def arc(label,arm,body,joint,target,opening,width,**extra):
  js[joint]=target;b=states()[body]
  add(label,arm,dict(pos=b['pos'],quat=b['quat']),opening,body,width,arc=dict(joint=joint,angle=target),**extra)
 def check(joint,lo,hi):return dict(name=joint,min=lo,max=hi)
 park('left');park('right')
 grip('Approach latch lever','right','latch_lever',D.LEVER_GRIP,down,.55,away=.015)
 grip('Reach latch lever','right','latch_lever',D.LEVER_GRIP,down,.35)
 grip('Grip latch lever','right','latch_lever',D.LEVER_GRIP,down,0.,.002,dwell=.35)
 arc('Lift jam-clear lever','right','latch_lever','lever_rotation',-2.1,0.,.002)
 js.update(opened);js['door_rotation']=0.
 lever_tool=multiply(states()['latch_lever']['quat'],multiply(conjugate(base),down))
 grip('Release lifted lever','right','latch_lever',D.LEVER_GRIP,lever_tool,.35)
 grip('Withdraw from lifted lever','right','latch_lever',D.LEVER_GRIP,lever_tool,.35,away=.010)
 park('right')
 grip('Approach nose door','left','nose_door',D.DOOR_GRIP,down,.55,away=.070)
 grip('Reach nose door','left','nose_door',D.DOOR_GRIP,down,.35)
 grip('Grip nose door','left','nose_door',D.DOOR_GRIP,down,0.,.003,dwell=.35)
 arc('Open nose door','left','nose_door','door_rotation',1.9,0.,.003)
 # The second hand removes the genuinely free brad; the first keeps the door.
 grip('Approach bent brad','right','bent_brad',[.018,.010,0],side,.35,away=.060)
 grip('Reach bent brad','right','bent_brad',[.018,.010,0],side,.20)
 grip('Grip bent brad','right','bent_brad',[.018,.010,0],side,0.,.0012,dwell=.35)
 free['bent_brad']['pos'][1]-=.10
 grip('Extract bent brad through open service face','right','bent_brad',[.018,.010,0],side,0.,.0012)
 for key in ('reference_body','reference_offset','reference_quat'):phases[-1].pop(key,None)
 # Transport target is a rigid TCP offset captured by the controller. It must
 # not depend on re-reading the moving brad as a new acquisition reference.
 add('Carry brad clear above tray','right',dict(pos=[.24,-.28,.94],quat=down.tolist()),0.,'bent_brad',.0012,transport=True)
 add('Lower brad inside tray','right',dict(pos=[.24,-.28,D.TABLE+.035],quat=down.tolist()),0.,'bent_brad',.0012,transport=True,speed=.02)
 add('Release brad into tray','right',dict(pos=[.24,-.28,D.TABLE+.035],quat=down.tolist()),.15,dwell=.35)
 add('Withdraw from tray','right',dict(pos=[.24,-.28,.94],quat=down.tolist()),.15)
 free['bent_brad']=dict(pos=[.24,-.28,D.TABLE+.005],quat=base.tolist())
 park('right')
 # Crosspin orientation follows the door during the two-TCP carry. Its center
 # is accessible while it is outboard of the fixed capture arms.
 tool=multiply(states()['nose_door']['quat'],multiply(conjugate(base),right_pin))
 local=rotate(multiply(conjugate(states()['bail_crosspin']['quat']),tool),[0,0,-.011])
 grip('Approach outboard crosspin','right','bail_crosspin',local,tool,.35,away=.015)
 grip('Reach outboard crosspin','right','bail_crosspin',local,tool,.20)
 grip('Grip outboard crosspin','right','bail_crosspin',local,tool,0.,.0022,dwell=.35)
 arc('Close door while carrying pin clear','left','nose_door','door_rotation',0.,0.,.003,coupled='rigid',follower='right')
 grip('Release reseated door','left','nose_door',D.DOOR_GRIP,down,.35)
 grip('Withdraw door hand','left','nose_door',D.DOOR_GRIP,down,.35,away=.080)
 # Top projection permits a real, spatially separated crosspin handoff.
 top_tool=down;top=np.array([0,0,-.025])+rotate(multiply(conjugate(states()['bail_crosspin']['quat']),top_tool),[0,0,-.011])
 grip('Approach crosspin top end','left','bail_crosspin',top,top_tool,.35,away=.010)
 grip('Reach crosspin top end','left','bail_crosspin',top,top_tool,.20)
 grip('Regrasp crosspin top end','left','bail_crosspin',top,top_tool,0.,.0022,dwell=.35)
 local=rotate(multiply(conjugate(states()['bail_crosspin']['quat']),right_pin),[0,0,-.011])
 grip('Release crosspin center','right','bail_crosspin',local,right_pin,.30)
 grip('Withdraw crosspin center hand','right','bail_crosspin',local,right_pin,.30,away=.015)
 park('right')
 lever_tool=multiply(states()['latch_lever']['quat'],multiply(conjugate(base),down))
 grip('Approach open lever again','right','latch_lever',D.LEVER_GRIP,lever_tool,.45,away=.010)
 grip('Reach open lever again','right','latch_lever',D.LEVER_GRIP,lever_tool,.30)
 grip('Regrasp open lever','right','latch_lever',D.LEVER_GRIP,lever_tool,0.,.002,dwell=.35)
 arc('Guide pin around front of both arms','left','bail_crosspin','bail_rotation',.30-js['lever_rotation'],0.,.0022)
 E=np.array(D.HINGE_POINT)+rotate(axis_quat([0,0,1],js['lever_rotation']),D.ECCENTRIC)
 beta=math.asin((D.NOMINAL_PIN_CLOSED[1]-E[1])/D.DRAW_REST)
 arc('Insert pin through open hook mouth','left','bail_crosspin','bail_rotation',beta-js['lever_rotation'],0.,.0022)
 arc('Draw latch past center with both pin ends captured','right','latch_lever','lever_rotation',0.,0.,.002,coupled='hook',follower='left')
 js.update(D.INITIAL)
 # Targets for releases are bound to the measured terminal grasp, not the
 # starting top-grasp orientation reused at the end of a rotating operation.
 add('Release captured crosspin','left',dict(pos=[0,0,0],quat=down.tolist()),.30,release_current=True)
 add('Withdraw crosspin top hand','left',dict(pos=[0,0,0],quat=down.tolist()),.30,withdraw_current=.010)
 park('left')
 add('Release secured lever','right',dict(pos=[0,0,0],quat=down.tolist()),.35,release_current=True)
 add('Withdraw secured lever hand','right',dict(pos=[0,0,0],quat=down.tolist()),.35,withdraw_current=.010)
 park('right')
 add('Released fixture hold','right',dict(pos=[.23,-.20,.97],quat=down.tolist()),1.,dwell=2.5,
     joint_checks_final=[check('door_rotation',-.005,.005),check('lever_rotation',-.06,.01),check('bail_extension',.0001,.0015)])
 return dict(schema=1,feedback='READ_ONLY_NATIVE_STATE_AND_ROBOT_PROPRIOCEPTION',nominal_pose_basis='Supplemental force-fixture opening; explicit ideal grasps only, no native robot result',phases=phases)

if __name__=='__main__':
 s=json.loads((HERE/'scene.json').read_text());(HERE/'controller.json').write_text(json.dumps(make_plan(s),indent=2)+'\n')
