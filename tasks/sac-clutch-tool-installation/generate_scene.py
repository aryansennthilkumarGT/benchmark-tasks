"""Original BENCHMARK_AUTHORED SAC mounting fixture; never LuK measured geometry.

The native mechanism consists entirely of collision geometry and gravity. No
screw joint, attachment, pose trigger or hidden score-dependent drive is used.
"""
import copy
import json
import math
from pathlib import Path
from dimensions import validated
from primitives import box,cylinder,ring,body,assembly,quat

HERE=Path(__file__).resolve().parent
TABLE=.7475
CENTER=[.24,0.]
BASE_TOP=TABLE+.040
CARRIER_BOTTOM=TABLE+.070
CARRIER_Z=CARRIER_BOTTOM+.004
PICK=[.22,.205,CARRIER_Z]
STEEL=[.48,.5,.52]
BLUE=[.12,.34,.58]
BRASS=[.66,.46,.15]


def helix(z0,length,major,pitch,internal=False):
    """Same-handed square thread, 64 tangential prisms per turn.

    Root/crest radii, 0.20 mm flank relief and 0.20 mm radial relief are authored
    approximations, not an ISO profile. Male/female phases differ by half pitch.
    """
    radial=(major/2-.0013,major/2) if not internal else (major/2-.0011,major/2+.00035)
    r=sum(radial)/2;shapes=[]
    for i in range(math.ceil(length/pitch*64)):
        a=2*math.pi*i/64
        z=z0+pitch*i/64+(pitch/2 if internal else 0)
        half=(pitch/2-.0002)/2
        if z-half<z0 or z+half>z0+length:continue
        shapes.append(box([r*math.cos(a),r*math.sin(a),z],
            [radial[1]-radial[0],2*radial[1]*math.tan(math.pi/64),pitch/2-.0002],
            BRASS if internal else STEEL,quat([0,0,1],a)))
    return shapes


def rotate_shapes(shapes,angle):
    from motion import rotate,multiply
    q=quat([0,0,1],angle);out=[]
    for s in shapes:
        t=copy.deepcopy(s);t['pos']=rotate(q,t['pos']).tolist();t['quat']=multiply(q,t['quat']).tolist();out.append(t)
    return out


def make_scene():
    d=validated(json.loads((HERE/'fixture-profile.json').read_text()))
    radius=d['stud_circle_radius'];pitch=d['retainer_thread_pitch'];major=d['retainer_thread_major']
    height=d['retainer_height'];thick=d['carrier_thickness']
    carrier_z=CARRIER_BOTTOM+thick/2
    nut_bottom=CARRIER_BOTTOM+thick
    tip=TABLE+d['stud_tip_height']
    if abs(tip-(nut_bottom+height))>1e-9:raise ValueError('Retainer top must be flush with stud tip')
    sites=[[CENTER[0]+radius*math.cos(a),CENTER[1]+radius*math.sin(a)] for a in [0,2*math.pi/3,4*math.pi/3]]
    # This is a rigid prepared surrogate, not a simulated DMF/diaphragm spring.
    fixture_shapes=[cylinder([0,0,-.020],.108,.040,BLUE)]
    fixture_shapes+=ring(.018,.095,.006,z=.003,color=STEEL) # visible centered disc/cover stack
    fixture_shapes+=[cylinder([0,0,.030],.0075,.060,BRASS)] # benchmark centering mandrel
    # Three real locating dowels and concentric prepared cover rim are fixed into
    # one assembly: their upstream installation is outside the bounded operation.
    for a in [math.pi/3,math.pi,5*math.pi/3]:
        fixture_shapes.append(cylinder([.085*math.cos(a),.085*math.sin(a),.009],.003,.012,BRASS))
    local_sites=[]
    for x,y in sites:
        X,Y=x-CENTER[0],y-CENTER[1];local_sites.append([X,Y])
        fixture_shapes.append(cylinder([X,Y,(CARRIER_BOTTOM-BASE_TOP)/2],.0067,CARRIER_BOTTOM-BASE_TOP,BLUE))
        # Lower flywheel socket intentionally M8x1.25, an authored assembly choice.
        # The separate custom upper contact thread is 12 mm x 3 mm.
        fixture_shapes.append(cylinder([X,Y,(tip-BASE_TOP)/2],major/2-.0013,tip-BASE_TOP))
        for s in helix(tip-BASE_TOP-d['stud_thread_length'],d['stud_thread_length'],major,pitch):
            s['pos'][0]+=X;s['pos'][1]+=Y;fixture_shapes.append(s)
    fixture=body('fixture',[*CENTER,BASE_TOP],fixture_shapes,5.,True)
    carrier_shapes=ring(d['carrier_centre_bore']/2,.032,thick,color=BLUE)
    for a in [0,2*math.pi/3,4*math.pi/3]:
        rails=[box([.062,sign*.009,0],[.056,.004,thick],BLUE) for sign in (-1,1)]
        rails += [box([.034,0,0],[.020,.014,thick],BLUE),box([.085,0,0],[.010,.014,thick],BLUE),
                  box([.099,0,.006],[.020,.016,.012],BLUE)]
        carrier_shapes+=rotate_shapes(rails,a)
    # Retracted hollow spindle is integral and passive in this bounded fixture.
    # Its lower face remains above the prepared cover, never compressing it.
    carrier_shapes+=ring(d['retracted_spindle_inner_bore']/2,.016,.024,z=.020,color=BRASS)
    carrier=body('carrier',PICK.copy(),carrier_shapes,d['carrier_mass'])
    # A passive raised nest supports the carrier's three arms, not its bore.
    tray_shapes=[]
    for a in [0,2*math.pi/3,4*math.pi/3]:
        tray_shapes.append(box([.038*math.cos(a),.038*math.sin(a),-.035],[.018,.018,.070],BLUE))
    carrier_tray=body('carrier_tray',[PICK[0],PICK[1],CARRIER_BOTTOM],tray_shapes,1.,True)
    # Nuts start on three narrow pedestals; jaws can reach below the upper rim.
    nut_picks=[[.12,-.18],[.21,-.20],[.30,-.18]]
    pick_bottom=TABLE+.045
    tray_shapes=[];nuts=[]
    for i,(x,y) in enumerate(nut_picks):
        tray_shapes.append(cylinder([x-.21,y+.18,.0225],.009,.045,BLUE))
        shapes=ring(major/2+.00035,d['retainer_diameter']/2,height,color=BRASS)
        shapes+=helix(-height/2,d['retainer_thread_length'],major,pitch,True)
        # Knurled outer surface is explicit faceted collision geometry.
        for j in range(24):
            a=j*2*math.pi/24
            shapes.append(box([.0138*math.cos(a),.0138*math.sin(a),0],[.0007,.0018,height],BRASS,quat([0,0,1],a)))
        marker=box([.010,0,height/2+.00001],[.006,.002,.00002],BLUE)
        marker['collision']=False;shapes.append(marker) # visible painted turn witness
        nuts.append(body('nut'+str(i),[x,y,pick_bottom+height/2],shapes,d['retainer_mass']))
    nut_tray=body('retainer_tray',[.21,-.18,TABLE],tray_shapes,1.,True)
    bodies=[fixture,carrier_tray,nut_tray,carrier,*nuts]
    anchors={b['name']:dict(pos=b['pos'],quat=b['quat']) for b in bodies if b['anchor']}
    score=dict(studs=[dict(axis_xy=v,tip_z=tip,entry_z=tip+height/2,entry_yaw=0.,engagement_min_z=nut_bottom+height/2-.0005,
                  engagement_max_z=tip+height/2+.001,minimum_turns=height/pitch-.15) for v in sites],
        retainers=[b['name'] for b in nuts],carrier_slot_centres=[[*v,0.] for v in local_sites],
        carrier_seat_z=carrier_z,retainer_top_offset=height/2,pitch=pitch,
        lateral_tolerance=.00065,axial_tolerance=.00030,tilt_tolerance=.025,hold_seconds=2.,
        penetration_limit=.00035,thread_phase_tolerance=.35,fixture_tolerance=.001,control_hz=20,speed_limit=.008,spin_limit=.15,
        release_clearance=.020,loss_plane=TABLE-.020,anchors=anchors)
    return dict(slug='sac-clutch-tool-installation',title='Mount and retain a SAC installation-tool carrier',
        instruction='Lower the unloaded three-arm SAC carrier over the prepared studs and centering mandrel. Screw each of the three knurled retainers clockwise until its top is flush with its stud tip and the carrier rests on all three shoulders. Release the parts and withdraw both grippers. Keep the central pressure spindle retracted.',
        geometry_mode='BENCHMARK_AUTHORED',control_hz=20,physics_dt=1/480,gravity=[0,0,-9.81],run_limit=24000,
        table_top=TABLE,hold_seconds=2.,penetration_limit=.00035,assemblies=[assembly(b,b['anchor']) for b in bodies],
        collision_exclusions=[],score_spec=score,parameters=d,
        material=dict(static_friction=.65,dynamic_friction=.5,restitution=0.,steel_density=7850.,contact_offset=.00003,rest_offset=0.),
        limitations=['Original benchmark fixture, NOT measured LuK or Sealey tool geometry.',
            'Prepared disc, cover, dowels and lower stud installation are fixed initial conditions.',
            'Hollow central spindle is retracted and rigid; diaphragm compression and torque are outside this task.',
            'Custom 12 mm / 3 mm square upper thread, faceted at 64 segments per turn; not an ISO M12 claim.',
            'Authored mass/inertia/friction require native validation; no stress, torque or service certification.'])


def make_plan(spec):
    from yam_arena.demo import DOWN_GRIP
    from motion import multiply,axis_quat
    phases=[];states={b['name']:dict(pos=b['pos'].copy(),quat=b['quat'].copy()) for a in spec['assemblies'] for b in a['bodies']}
    down=DOWN_GRIP.tolist();angle=2*math.pi/3
    left_q=multiply(axis_quat([0,0,1],angle-math.pi),down).tolist()
    grip_offset=[.099*math.cos(angle),.099*math.sin(angle),.015]
    def phase(label,side,pos,q,opening,contact=None,width=0.,dwell=.15,speed=.05,mutate=None):
        if mutate:mutate()
        phases.append(dict(label=label,side=side,target=dict(pos=list(pos),quat=q),opening=opening,
            grasp_width=width,contact_body=contact,dwell=dwell,timeout=55.,speed=speed,
            position_tolerance=.00035,angle_tolerance=.025,nominal_bodies=copy.deepcopy(states)))
    def cp(pos):return [pos[i]+grip_offset[i] for i in range(3)]
    def carrier_at(pos):states['carrier']=dict(pos=list(pos),quat=[0,0,0,1])
    phase('Approach carrier handling tab','left',cp([*PICK[:2],.94]),left_q,1.)
    phase('Reach carrier handling tab','left',cp(PICK),left_q,.5)
    phase('Grip carrier tab','left',cp(PICK),left_q,.12,'carrier',.016,dwell=.5)
    phase('Lift carrier above studs and centering tool','left',cp([*PICK[:2],.94]),left_q,.12,'carrier',.016,mutate=lambda:carrier_at([*PICK[:2],.94]))
    phase('Transfer carrier over prepared clutch','left',cp([*CENTER,.94]),left_q,.12,'carrier',.016,mutate=lambda:carrier_at([*CENTER,.94]))
    seat=spec['score_spec']['carrier_seat_z']
    phase('Lower three slots over studs and mandrel','left',cp([*CENTER,seat]),left_q,.12,'carrier',.016,speed=.006,mutate=lambda:carrier_at([*CENTER,seat]))
    phase('Release seated unloaded carrier','left',cp([*CENTER,seat]),left_q,.5,'carrier')
    phase('Lift carrier gripper clear','left',cp([*CENTER,.95]),left_q,.5)
    phase('Park carrier arm','left',[.17,.23,.92],left_q,1.)
    phase('Initialize retainer arm above cradle','right',[.28,-.17,.90],down,1.)
    d=spec['parameters'];pitch=d['retainer_thread_pitch'];height=d['retainer_height'];strokes=round(height/pitch*8)
    for i,name in enumerate(spec['score_spec']['retainers']):
        x,y=spec['score_spec']['studs'][i]['axis_xy'];pick=states[name]['pos'].copy()
        tip=spec['score_spec']['studs'][i]['tip_z'];entry=tip+height/2
        def nut_at(pos,q=[0,0,0,1],name=name):states[name]=dict(pos=list(pos),quat=list(q))
        # TCP sits 9 mm above the nut midplane, avoiding the carrier arms.
        zoff=.012;opening=.20;wide=.50
        phase(f'Approach retainer {i+1}','right',[*pick[:2],.90],down,1.)
        phase(f'Reach retainer {i+1}','right',[*pick[:2],pick[2]+zoff],down,wide)
        phase(f'Grip retainer {i+1}','right',[*pick[:2],pick[2]+zoff],down,opening,name,.028,dwell=.5)
        phase(f'Lift retainer {i+1}','right',[*pick[:2],.90],down,opening,name,.028,mutate=lambda:nut_at([*pick[:2],.90-zoff]))
        phase(f'Transfer retainer {i+1}','right',[x,y,.905],down,opening,name,.028,mutate=lambda:nut_at([x,y,.905-zoff]))
        phase(f'Enter upper stud {i+1}','right',[x,y,entry+zoff],down,opening,name,.028,speed=.005,mutate=lambda:nut_at([x,y,entry]))
        rotated=multiply(axis_quat([0,0,1],-math.pi/4),down).tolist()
        for k in range(strokes):
            z=entry-(k+1)*pitch/8
            phase(f'Thread retainer {i+1} stroke {k+1}','right',[x,y,z+zoff],rotated,opening,name,.028,speed=.004,
                  mutate=lambda z=z,k=k:nut_at([x,y,z],quat([0,0,1],-(k+1)*math.pi/4)))
            if k==strokes-1:continue
            phase(f'Open retainer {i+1} stroke {k+1}','right',[x,y,z+zoff],rotated,wide,name)
            phase(f'Clear retainer {i+1} stroke {k+1}','right',[x,y,z+zoff+.020],rotated,wide)
            phase(f'Unwind retainer {i+1} stroke {k+1}','right',[x,y,z+zoff+.020],down,wide)
            phase(f'Return retainer {i+1} stroke {k+1}','right',[x,y,z+zoff],down,wide,speed=.025)
            phase(f'Regrasp retainer {i+1} stroke {k+1}','right',[x,y,z+zoff],down,opening,name,.028,dwell=.3)
        phase(f'Release flush retainer {i+1}','right',[x,y,z+zoff],rotated,wide,name)
        phase(f'Withdraw from retainer {i+1}','right',[x,y,.89],rotated,wide)
    phase('Park retainer arm','right',[.28,-.17,.93],down,1.)
    phase('Released assembly hold','right',[.28,-.17,.93],down,1.,dwell=2.5)
    return dict(schema=1,feedback='robot_proprioception_only',phases=phases)


if __name__=='__main__':
    spec=make_scene();plan=make_plan(spec)
    (HERE/'scene.json').write_text(json.dumps(spec,indent=2)+'\n')
    (HERE/'controller.json').write_text(json.dumps(plan,indent=2)+'\n')
    from build_assets import compile_assets
    compile_assets(spec,HERE/'assets')
