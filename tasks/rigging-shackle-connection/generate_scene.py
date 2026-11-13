"""Author an original dimensional shackle/lug fixture, never a simulator result.

Published GPGHBB16 envelope: 16 mm bow, 19 mm pin, 27 mm inside eye gap,
64 mm inside length, 43 mm inside bow width, 40 mm eye, 3/4-10 UNC thread.
Faceted surfaces and square thread flanks are declared approximations.
"""
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
PITCH = .0254 / 10
CENTER = [.22, 0., .788]
SEAT = .0295
TURNS = 6.
STEEL = [.48, .5, .52]
GREEN = [.05, .48, .18]


def quat(axis, angle):
    return [*(v*math.sin(angle/2) for v in axis), math.cos(angle/2)]


def box(pos, size, color=STEEL, q=None):
    return dict(kind='box', pos=pos, size=size, quat=q or [0,0,0,1], color=color)


def cylinder(pos, radius, height, color=STEEL, q=None):
    return dict(kind='cylinder', pos=pos, radius=radius, height=height,
                quat=q or [0,0,0,1], color=color)


def ring(inner, outer, height, z=0., count=64, color=STEEL):
    # Tangential prisms give a through-hole, not an invisible solid cylinder.
    radius=(inner+outer)/2
    width=2*outer*math.tan(math.pi/count)
    return [box([radius*math.cos(a),radius*math.sin(a),z],
                [outer-inner,width,height],color,quat([0,0,1],a))
            for a in [2*math.pi*i/count for i in range(count)]]


def helix(z0, length, internal=False):
    n=64
    pieces=[]
    # Crest widths leave an explicit 0.14 mm axial assembly clearance.
    # Male/female faces are offset by half a pitch, with same handedness.
    radial=[.0081,.009525] if not internal else [.00825,.0101]
    r=sum(radial)/2
    for i in range(math.ceil(length/PITCH*n)):
        a=2*math.pi*i/n
        z=z0+PITCH*i/n+(PITCH/2 if internal else 0)
        if z>z0+length-(PITCH/4-.00007):break
        pieces.append(box([r*math.cos(a),r*math.sin(a),z],
                [radial[1]-radial[0],2*radial[1]*math.tan(math.pi/n),PITCH/2-.00014],
            STEEL if internal else GREEN,quat([0,0,1],a)))
    return pieces


def body(name, pos, shapes, mass, fixed=False):
    from motion import rotate
    low=[float('inf')]*3; high=[-float('inf')]*3
    for shape in shapes:
        half=[v/2 for v in shape['size']] if shape['kind']=='box' else [shape['radius']]*2+[shape['height']/2]
        for i in (-1,1):
            for j in (-1,1):
                for k in (-1,1):
                    point=rotate(shape['quat'],[half[0]*i,half[1]*j,half[2]*k])
                    for axis in range(3):
                        value=point[axis]+shape['pos'][axis]
                        low[axis]=min(low[axis],value);high[axis]=max(high[axis],value)
    extent=[b-a for a,b in zip(low,high)]
    inertia=[mass*(extent[(i+1)%3]**2+extent[(i+2)%3]**2)/12 for i in range(3)]
    return dict(name=name,pos=pos,quat=[0,0,0,1],mass=mass,shapes=shapes,
                bounds_min=low,bounds_max=high,anchor=fixed,diagonal_inertia=inertia,
                inertia_model='bounding-box equivalent, not a manufacturer mass tensor')


def assembly(b, fixed=False):
    return dict(name=b['name']+'_asset',origin=b['pos'],fixed=fixed,bodies=[b],joints=[])


def make_scene():
    # The two eyes are 43 mm centre-to-centre, leaving 27 mm clear.
    shapes=ring(.00985,.020,.016,z=.0215)
    shapes+=ring(.0101,.020,.016,z=-.0215)
    shapes+=helix(-.0295,.016,True)
    # Shoulder curves widen from the eyes to the 43 mm internal bow.
    # Legs join the *outside* of the eyes. Starting at the bore centre would
    # silently obstruct the matching through-pin despite visually round holes.
    points=[(.017,-.0215),(.032,-.0275),(.0425,-.0295)]
    points += [(.0425+.0295*math.sin(a),-.0295*math.cos(a))
               for a in [math.pi*i/28 for i in range(1,29)]]
    points += [(.032,.0275),(.017,.0215)]
    for (y,z),(Y,Z) in zip(points,points[1:]):
        dy,dz=Y-y,Z-z;length=math.hypot(dy,dz)
        shapes.append(cylinder([0,(y+Y)/2,(z+Z)/2],.008,length+.0004,
                     q=quat([1,0,0],-math.atan2(dy,dz))))
    bow=body('shackle',[CENTER[0],.006,CENTER[2]],shapes,.45)
    # 59 mm shank plus 30 mm collar/thumb tab envelope = 89 mm overall.
    pin_shapes=[cylinder([0,0,-.0215],.0095,.043,GREEN),
                cylinder([0,0,-.051],.0081,.016,GREEN),
                cylinder([0,0,.002],.01425,.004,GREEN),
                box([0,0,.017],[.024,.012,.026],GREEN)]
    pin_shapes+=helix(-.059,.016)
    pin=body('pin',[.28,-.17,.808],pin_shapes,.18)
    lug_shapes=ring(.0103,.025,.012)
    floor=.7475-CENTER[2]
    lug_shapes += [box([0,-.029,(floor+.010-.006)/2],[.032,.014,-.006-floor-.010]),
                   box([0,-.035,floor+.005],[.09,.09,.010])]
    lug=body('lifting_lug',CENTER.copy(),lug_shapes,2.,True)
    # An already threaded sling master link, bench-supported. Only the upper
    # branch of the bow crosses its aperture; the pin and lower branch do not.
    link_shapes=[]
    for i in range(48):
        a=2*math.pi*i/48;aa=2*math.pi*(i+1)/48
        x,z=.024*math.cos(a),.024*math.sin(a)
        X,Z=.024*math.cos(aa),.024*math.sin(aa)
        link_shapes.append(cylinder([(x+X)/2,0,(z+Z)/2],.004,
            math.hypot(X-x,Z-z)+.0003,q=quat([0,1,0],math.atan2(X-x,Z-z))))
    link_floor=.7475-(CENTER[2]+.025)
    link_shapes += [box([.064,.015,link_floor/2],[.018,.03,-link_floor]),
                    box([.052,.015,0],[.042,.025,.008]),
                    cylinder([.030,0,0],.003,.010,q=quat([0,1,0],math.pi/2))]
    link=body('sling_link',[CENTER[0],.034,CENTER[2]+.025],link_shapes,.7,True)
    cradle_shapes=ring(.0102,.018,.018)
    cradle_shapes += [box([.026,0,-.025],[.014,.06,.051])]
    cradle=body('pin_cradle',[.28,-.17,.798],cradle_shapes,.5,True)
    supports=[box([dx,.012,-.0345],[.006,.052,.010]) for dx in (-.0175,.0175)]
    supports += [box([0,.045,(floor-.0375)/2],[.018,.040,-.0375-floor]),
                 box([0,.040,floor+.0005],[.075,.11,.001])]
    nest=body('alignment_nest',CENTER.copy(),supports,1.,True)
    pose=lambda name,p,tol:dict(kind='pose',body=name,pos=p,quat=[0,0,0,1],tolerance=tol,angle=.04)
    goals=[dict(name='aligned',weight=.2,all=[pose('shackle',CENTER,.0008)]),
           dict(name='pin_through_lug',weight=.25,requires=['aligned'],all=[
               dict(kind='pose',body='pin',relative_to='shackle',pos=[0,0,SEAT+.004],
                    quat=[0,0,0,1],angle=math.pi,tolerance=.0045),
               dict(kind='turns',body='pin',min=4.)]),
           dict(name='collar_seated',weight=.55,requires=['pin_through_lug'],all=[
               dict(kind='pose',body='pin',relative_to='shackle',pos=[0,0,SEAT],
                    quat=[0,0,0,1],angle=math.pi,tolerance=.00035),
               dict(kind='axis',body='pin',relative_to='shackle',direction=[0,0,1],angle=.025),
               dict(kind='turns',body='pin',min=5.8)])]
    return dict(slug='rigging-shackle-connection',title='Fit and seat a screw-pin shackle through a lifting lug',
        instruction='Connect the supported sling to the lifting lug with its matching screw-pin shackle. Align the eyes, pass the pin through the lug, and screw it down until its collar is fully seated. Leave the pin in place and withdraw both grippers.',
        control_hz=20,physics_dt=1/480,gravity=[0,0,-9.81],run_limit=18000,table_top=.7475,hold_seconds=2.,penetration_limit=.0015,
        assemblies=[assembly(b,b['anchor']) for b in [lug,link,bow,pin,cradle,nest]],goals=goals,
        threads=[dict(body='pin',reference='shackle',xy=[0,0],radial_tolerance=.00065,
            z_min=.028,z_max=.047,pitch=PITCH,axial_slack=.0003)],
        invariants=[],collision_exclusions=[],
        geometry_parameters=dict(pitch=PITCH,seat=SEAT,turns=TURNS,shank_length=.059,
            inside_gap=.027,bow_stock_diameter=.016,eye_diameter=.040,pin_diameter=.019,
            inside_length=.064,inside_bow_width=.043),
        limitations=['Square-profile faceted contact threads approximate the published 3/4-10 UNC pitch, not its triangular flank stress.',
            'Steel parts are rigid; lifting strength, certification, fatigue and wrench torque are not predicted.',
            'Lug, sling support, pin cradle, friction and inertia tensors are authored bench fixtures/model choices.'])


def make_plan(spec):
    from yam_arena.demo import DOWN_GRIP
    from motion import multiply,axis_quat
    down=DOWN_GRIP.tolist()
    # Wrist yaw chosen and tested in the analytical IK audit.
    left_q=multiply(axis_quat([0,0,1],-math.pi/2),down).tolist()
    right_q=down
    phases=[]
    def phase(label,side,pos,q,opening,dwell=.15,speed=.06):
        phases.append(dict(label=label,side=side,target=dict(pos=pos,quat=q),opening=opening,
                           dwell=dwell,timeout=40.,speed=speed,position_tolerance=.00035,
                           angle_tolerance=.025))
    x,_,z=CENTER
    support=[x,.072,z]
    phase('Approach shackle support','left',[x,.078,z+.09],left_q,1.)
    phase('Reach outer bow','left',[x,.078,z],left_q,.32)
    phase('Grip outer bow','left',[x,.078,z],left_q,.012/.0939,.5)
    phase('Align shackle eyes with lug bore','left',support,left_q,.012/.0939,speed=.008)
    phase('Release aligned shackle into passive nest','left',support,left_q,.32)
    phase('Park support arm clear of pin tool','left',[.17,.23,.92],left_q,.32)
    pick=[.28,-.17,.835]
    phase('Approach matching pin','right',[.28,-.17,.90],right_q,1.)
    phase('Reach pin head','right',pick,right_q,1.)
    phase('Grip pin thumb tab','right',pick,right_q,.010/.0939,.5)
    phase('Lift pin clear of cradle','right',[.28,-.17,.910],right_q,.010/.0939)
    phase('Carry pin above aligned eyes','right',[x,0,.910],right_q,.010/.0939)
    entry=z+SEAT+TURNS*PITCH+.027
    phase('Insert through near eye and lifting lug','right',[x,0,entry],right_q,.010/.0939,speed=.006)
    # Eight 45-degree strokes per turn. Open, lift and unwind between strokes;
    # thread contact alone must support the pin while the gripper repositions.
    segments=int(TURNS*8)
    for i in range(segments):
        height=entry-(i+1)*PITCH/8
        rotated=multiply(axis_quat([0,0,1],-math.pi/4),right_q).tolist()
        phase(f'Tighten pin stroke {i+1}','right',[x,0,height],rotated,.010/.0939,speed=.004)
        if i!=segments-1:
            phase(f'Open for regrasp {i+1}','right',[x,0,height],rotated,.45)
            phase(f'Clear pin head {i+1}','right',[x,0,height+.020],rotated,.45)
            phase(f'Unwind wrist {i+1}','right',[x,0,height+.020],right_q,.45)
            phase(f'Lower around pin head {i+1}','right',[x,0,height],right_q,.45,speed=.025)
            phase(f'Regrasp pin {i+1}','right',[x,0,height],right_q,.010/.0939,.4)
    phase('Release seated pin','right',[x,0,entry-TURNS*PITCH],rotated,.45)
    phase('Lift clear after pin release','right',[x,0,entry-TURNS*PITCH+.020],rotated,.45)
    phase('Withdraw pin tool gripper','right',[.28,-.17,.93],right_q,1.)
    phase('Final clear hold','right',[.28,-.17,.93],right_q,1.,dwell=2.5)
    states={b['name']:dict(pos=b['pos'],quat=b['quat']) for a in spec['assemblies'] for b in a['bodies']}
    for p in phases:
        if p['label']=='Align shackle eyes with lug bore':states['shackle']=dict(pos=CENTER.copy(),quat=[0,0,0,1])
        if p['label'] in ('Lift pin clear of cradle','Carry pin above aligned eyes','Insert through near eye and lifting lug'):
            states['pin']=dict(pos=[*p['target']['pos'][:2],p['target']['pos'][2]-.027],quat=[0,0,0,1])
        if p['label'].startswith('Tighten pin stroke'):
            i=int(p['label'].split()[-1]);states['pin']=dict(pos=[x,0,p['target']['pos'][2]-.027],quat=quat([0,0,1],-i*math.pi/4))
        p['nominal_bodies']=json.loads(json.dumps(states))
        p['contact_body']='shackle' if p['side']=='left' else 'pin'
        p['grasp_width']=0.
        if p['opening']<.3:
            if p['side']=='left':p['grasp_width']=.016
            else:
                from motion import rotate
                import numpy as np
                jaw=rotate(p['target']['quat'],[1,0,0]);bq=p['nominal_bodies']['pin']['quat']
                p['grasp_width']=sum(abs(float(np.dot(jaw,rotate(bq,axis))))*length
                    for axis,length in [([1,0,0],.024),([0,1,0],.012)])
    return dict(schema=1,feedback='robot_proprioception_only',phases=phases)


if __name__=='__main__':
    spec=make_scene()
    (HERE/'scene.json').write_text(json.dumps(spec,indent=2)+'\n')
    (HERE/'controller.json').write_text(json.dumps(make_plan(spec),indent=2)+'\n')
    from build_assets import compile_assets
    compile_assets(spec,HERE/'assets')
