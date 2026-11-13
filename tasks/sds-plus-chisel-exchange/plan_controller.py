"""SDS-specific executable phase descriptors; body goals are mapped to TCP at acquisition."""
import hashlib,json,math
from pathlib import Path
try:
 from . import dimensions as D
except ImportError:
 import dimensions as D
from yam_arena.demo import DOWN_GRIP
HERE=Path(__file__).resolve().parent

def scene_digest(spec):return hashlib.sha256(json.dumps(spec,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()
def make_plan(spec):
 phases=[]
 def add(label,side,mode='world',opening=.2,width=0.,dwell=.15,speed=.055,timeout=25.,**kw):phases.append(dict(label=label,side=side,mode=mode,opening=opening,grasp_width=width,dwell=dwell,speed=speed,position_tolerance=.0004,angle_tolerance=.02,timeout=timeout,**kw))
 def park(side):add('Park '+side+' arm',side,target=dict(pos=[.23,.26 if side=='left' else -.26,.97],quat=list(DOWN_GRIP)),opening=.45)
 def grip(label,side,body,offset,opening,width=0.,away=0.):add(label,side,'grasp',body=body,offset=offset,tool_quat=list(DOWN_GRIP),away=away,opening=opening,width=width,dwell=.3 if width else .15)
 def move(label,side,body,pos,quat=None,opening=0.,width=.012,speed=.04,**kw):add(label,side,'body_goal',body=body,body_goal=dict(pos=pos,quat=quat),opening=opening,width=width,speed=speed,**kw)
 def release(label,side,opening):add(label,side,'release',opening=opening,dwell=.25)
 def withdraw(label,side,distance,opening):add(label,side,'withdraw',distance=distance,opening=opening)
 park('left');park('right')
 grip('Approach used chisel','right','used_point_chisel',D.OLD_GRIP,.20,away=.050)
 grip('Reach used chisel','right','used_point_chisel',D.OLD_GRIP,.18)
 grip('Grip used chisel','right','used_point_chisel',D.OLD_GRIP,0.,.0113)
 grip('Approach release sleeve','left','locking_sleeve',D.COLLAR_GRIP,.50,away=.050)
 grip('Reach release sleeve','left','locking_sleeve',D.COLLAR_GRIP,.45)
 grip('Grip release sleeve','left','locking_sleeve',D.COLLAR_GRIP,0.,.0356)
 move('Retract actual spring sleeve','left','locking_sleeve',[D.ROOT[0]+D.COLLAR_TRAVEL,*D.ROOT[1:]],[0,0,0,1],width=.0356,joint_checks=[dict(name='sleeve_retraction',min=.0075,max=.0081)],speed=.010)
 move('Withdraw used shank while sleeve stays back','right','used_point_chisel',[D.ROOT[0]-.008,*D.ROOT[1:]],[0,0,0,1],width=.0113,speed=.020)
 release('Release sleeve after chisel clears','left',.48)
 withdraw('Withdraw sleeve hand','left',.070,.48);park('left')
 move('Lift used chisel clear of holder','right','used_point_chisel',[D.ROOT[0]-.008,0.,.95],[0,0,0,1],width=.0113)
 move('Carry used chisel above tray','right','used_point_chisel',[.37,-.30,.95],[0,0,0,1],width=.0113)
 move('Lower used chisel into tray','right','used_point_chisel',[.37,-.30,D.TABLE+.026],[0,0,0,1],width=.0113,speed=.025)
 release('Release used chisel into tray','right',.20)
 withdraw('Withdraw tray hand','right',.10,.20);park('right')
 grip('Approach replacement chisel','left','replacement_flat_chisel',D.NEW_GRIP,.20,away=.070)
 grip('Reach replacement chisel','left','replacement_flat_chisel',D.NEW_GRIP,.18)
 grip('Grip replacement chisel','left','replacement_flat_chisel',D.NEW_GRIP,0.,.0113)
 move('Lift replacement from cradle','left','replacement_flat_chisel',[.37,.30,.95],width=.0113)
 move('Bring replacement to open holder mouth','left','replacement_flat_chisel',[D.ROOT[0]-.015,0.,D.ROOT[2]],width=.0113)
 move('Turn open drive grooves into alignment','left','replacement_flat_chisel',[D.ROOT[0]-.015,0.,D.ROOT[2]],[0,0,0,1],width=.0113,speed=.025)
 move('Insert shank until radial ball captures closed slot','left','replacement_flat_chisel',[D.ROOT[0]+.042,0.,D.ROOT[2]],[0,0,0,1],width=.0113,speed=.015,require_retained=True,dwell=.4)
 add('Pull check against actual retention stop','left','tug',body='replacement_flat_chisel',opening=0.,width=.0113,dwell=.35,speed=.006,maximum_withdrawal=.004,feedback_overtravel=.00030,timeout=6.)
 release('Release retained replacement','left',.24)
 withdraw('Withdraw replacement hand','left',.10,.24);park('left')
 add('Released secured-tool hold','left',target=dict(pos=[.23,.26,.97],quat=list(DOWN_GRIP)),opening=.45,dwell=2.5,require_retained=True)
 return dict(schema=1,scene_content_sha256=scene_digest(spec),feedback='READ_ONLY_NATIVE_BODY_JOINT_AND_ROBOT_STATE',phases=phases)
if __name__=='__main__':(HERE/'controller.json').write_text(json.dumps(make_plan(json.loads((HERE/'scene.json').read_text())),indent=2)+'\n')
