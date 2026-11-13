"""Dell-grounded bracket pin release with an original compliant-rail fixture.

Only the Samsung external case envelope is manufacturer-dimensional. Bracket,
pin/bore clearances and lumped compliance are explicit benchmark approximations.
"""
import copy,json,math
from pathlib import Path
from primitives import box,cylinder,ring,body,quat
from motion import rotate,multiply,axis_quat
HERE=Path(__file__).resolve().parent
TABLE=.7475
BASE=[.24,0,TABLE+.050]
SIZE=[.100,.06985,.0068]
DRIVE=[BASE[0],0,BASE[2]+.003+SIZE[2]/2]
RAIL_TRAVEL=.006
BLUE=[.10,.35,.65];GREY=[.42,.44,.48];ORANGE=[.78,.38,.10]


def transform(shapes,q,offset):
    result=[]
    for shape in shapes:
        s=copy.deepcopy(shape);s['pos']=(rotate(q,s['pos'])+offset).tolist();s['quat']=multiply(q,s['quat']).tolist();result.append(s)
    return result


def make_scene():
    floor=box([0,0,-.005],[.12,.09,.01],GREY)
    fixed=[floor,box([.006,-.039,.008],[.078,.004,.016],BLUE)]
    for x in (-.030,.030):
        fixed.append(cylinder([x,-.035,.0064],.0015,.006,GREY,quat([1,0,0],math.pi/2)))
    for x in (-.04,.04):fixed.append(box([x,0,.0015],[.012,.05,.003],BLUE))
    bracket=body('bracket',BASE.copy(),fixed,.30,True)
    rail_shapes=[box([.006,.039,.008],[.078,.004,.016],BLUE),
                 box([.050,.039,.008],[.020,.004,.016],BLUE),
                 box([.064,.039,.008],[.020,.004,.016],BLUE)]
    for x in (-.030,.030):rail_shapes.append(cylinder([x,.035,.0064],.0015,.006,GREY,quat([1,0,0],math.pi/2)))
    rail=body('release_rail',BASE.copy(),rail_shapes,.016)
    joint=dict(name='rail_flexure',kind='prismatic',parent='bracket',child='release_rail',
        pivot_parent=[0,0,0],pivot_child=[0,0,0],axis='Y',lower=0.,upper=.007,
        rest=0.,stiffness=180.,damping=1.)
    # Real side bores: a central core plus four annular side-wall regions,
    # never a solid cube with painted holes. Positions are benchmark-authored.
    L,W,H=SIZE;strip=.006;bore=.0024;outer=H/2
    shapes=[box([0,0,0],[L,W-2*strip,H],GREY)]
    intervals=[(-L/2,-.030-outer),(-.030+outer,.030-outer),(.030+outer,L/2)]
    for sign in (-1,1):
        y=sign*(W/2-strip/2)
        for lo,hi in intervals:shapes.append(box([(lo+hi)/2,y,0],[hi-lo,strip,H],GREY))
        for x in (-.030,.030):
            shapes+=transform(ring(bore,outer,strip,color=GREY),quat([1,0,0],math.pi/2),[x,y,0])
    # Visible connector outline is disconnected and unscored: this is removal
    # from an already-extracted bracket, never an electrical insertion task.
    marker=box([-.045,0,H/2+.00002],[.007,.025,.00004],ORANGE);marker['collision']=False;shapes.append(marker)
    drive=body('drive',DRIVE.copy(),shapes,.045)
    tray_pos=[.25,-.19,TABLE]
    tray_shapes=[box([0,0,.0015],[.12,.09,.003],BLUE)]
    for x in (-.04,.04):
        for y in (-.025,.025):tray_shapes.append(box([x,y,.014],[.012,.012,.022],BLUE))
    tray=body('staging_tray',tray_pos,tray_shapes,.12,True)
    assemblies=[dict(name='bracket_asset',origin=BASE.copy(),fixed=True,bodies=[bracket,rail],joints=[joint]),
        dict(name='drive_asset',origin=DRIVE.copy(),fixed=False,bodies=[drive],joints=[]),
        dict(name='staging_tray_asset',origin=tray_pos,fixed=True,bodies=[tray],joints=[])]
    anchors={b['name']:dict(pos=b['pos'],quat=b['quat']) for b in [bracket,tray]}
    target=[tray_pos[0],tray_pos[1],TABLE+.025+H/2]
    return dict(slug='drive-bracket-pin-release',title='Release a 2.5-inch drive from its pinned service bracket',
        instruction='Remove the disconnected drive from the pinned bracket and place it on the staging supports. Release the compliant rail and withdraw both grippers. The assembly is already removed from the computer.',
        control_hz=20,physics_dt=1/480,gravity=[0,0,-9.81],run_limit=6500,table_top=TABLE,hold_seconds=2.,penetration_limit=.00035,
        assemblies=assemblies,collision_exclusions=[],
        score_spec=dict(anchors=anchors,initial_drive=DRIVE.copy(),target_drive=target,rail_origin=BASE.copy(),rail_joint='rail_flexure',
            rail_release=.0045,rail_return=.0005,rail_limit=.007,hold_seconds=2.,release_clearance=.020,
            speed_limit=.008,spin_limit=.15,position_tolerance=.0015,axial_tolerance=.0005,tilt_tolerance=.025,
            loss_plane=TABLE-.020,penetration_limit=.00035,fixture_tolerance=.001,control_hz=20),
        parameters=dict(drive_length=L,drive_width=W,drive_height=H,drive_mass=.045,pin_radius=.0015,pin_length=.006,
            pin_x_spacing=.060,pin_centres_y=[-.035,.035],bore_radius=bore,bore_depth=strip,
            rail_travel=RAIL_TRAVEL,rail_limit=.007,rail_stiffness=180.,rail_damping=1.,
            rail_mass=.016,tilt_angle=.25,opposite_pin_release_translation=.0045),
        material=dict(static_friction=.65,dynamic_friction=.5,restitution=0.,contact_offset=.00003,rest_offset=0.),
        limitations=['Samsung external case dimensions are documented; all bracket, bores, pins, compliance, masses and fixture dimensions are authored approximations.',
            'Lumped prismatic rail approximates plastic flexure, not actual Dell force or material stress.',
            'SATA/power are already disconnected and the assembly removed from chassis; electrical mating and front-door access are not evaluated.',
            'Bracket base is held by an authored bench fixture; the removal skill concerns rail release, opposed pins and drive extraction.'])


def make_plan(spec):
    from yam_arena.demo import DOWN_GRIP
    down=DOWN_GRIP.tolist();left_q=down
    phases=[];states={b['name']:dict(pos=b['pos'].copy(),quat=b['quat'].copy()) for a in spec['assemblies'] for b in a['bodies']}
    def phase(label,side,pos,q,opening,contact=None,width=0.,dwell=.2,speed=.04,mutate=None):
        if mutate:mutate()
        phases.append(dict(label=label,side=side,target=dict(pos=list(pos),quat=q),opening=opening,contact_body=contact,
            grasp_width=width,dwell=dwell,speed=speed,timeout=45.,position_tolerance=.00035,angle_tolerance=.025,
            nominal_bodies=copy.deepcopy(states)))
    phase('Initialize rail arm','left',[.17,.23,.92],left_q,1.)
    tab=[BASE[0]+.064,.039,BASE[2]+.017]
    phase('Approach compliant rail tab','left',[tab[0],tab[1],.90],left_q,1.)
    phase('Reach compliant rail tab','left',tab,left_q,.5)
    phase('Grip compliant rail tab','left',tab,left_q,.015,'release_rail',.004,dwell=.5)
    def rail_at(q):states['release_rail']['pos']=[BASE[0],q,BASE[2]]
    phase('Pull rail to release two pins','left',[tab[0],tab[1]+RAIL_TRAVEL,tab[2]],left_q,.015,'release_rail',.004,speed=.004,mutate=lambda:rail_at(RAIL_TRAVEL))
    phase('Initialize extraction arm','right',[.28,-.17,.90],down,1.)
    offset=[-.047,0,.014]
    def tcp(pos,q):return (rotate(q,offset)+pos).tolist()
    def drive_at(pos,q):states['drive']=dict(pos=list(pos),quat=list(q))
    phase('Descend in extraction approach corridor','right',[DRIVE[0]+offset[0],-.10,.835],down,1.)
    phase('Approach drive leading edge','right',[DRIVE[0]+offset[0],0,.835],down,1.)
    phase('Reach drive leading edge','right',tcp(DRIVE,[0,0,0,1]),down,1.)
    phase('Grip drive case across its width','right',tcp(DRIVE,[0,0,0,1]),down,.66,'drive',SIZE[1],dwell=.5)
    pivot=[DRIVE[0],-SIZE[1]/2,DRIVE[2]];tilt=axis_quat([1,0,0],.25).tolist()
    tilted=(rotate(tilt,[0,SIZE[1]/2,0])+pivot).tolist();tool=multiply(tilt,down).tolist()
    for step in range(1,11):
        angle=.25*step/10;q=axis_quat([1,0,0],angle).tolist()
        arc=(rotate(q,[0,SIZE[1]/2,0])+pivot).tolist();qt=multiply(q,down).tolist()
        phase('Tilt released edge off its pins' if step==10 else f'Tilt pin-release increment {step}',
            'right',tcp(arc,q),qt,.66,'drive',SIZE[1],speed=.004,mutate=lambda arc=arc,q=q:drive_at(arc,q))
    unpinned=[tilted[0],tilted[1]+.0045,tilted[2]]
    phase('Slide away from opposite locating pins','right',tcp(unpinned,tilt),tool,.66,'drive',SIZE[1],speed=.004,mutate=lambda:drive_at(unpinned,tilt))
    phase('Release compliant rail','left',[tab[0],tab[1]+RAIL_TRAVEL,tab[2]],left_q,.5,'release_rail',mutate=lambda:rail_at(0.))
    phase('Lift released rail fingers clear','left',[tab[0],tab[1]+RAIL_TRAVEL,tab[2]+.020],left_q,.5)
    phase('Withdraw rail gripper','left',[tab[0],.16,tab[2]+.020],left_q,1.)
    phase('Park rail arm','left',[.17,.23,.92],left_q,1.)
    lifted=[unpinned[0],unpinned[1],.90]
    phase('Lift drive clear of bracket','right',tcp(lifted,tilt),tool,.66,'drive',SIZE[1],mutate=lambda:drive_at(lifted,tilt))
    phase('Level extracted drive','right',tcp(lifted,[0,0,0,1]),down,.66,'drive',SIZE[1],mutate=lambda:drive_at(lifted,[0,0,0,1]))
    dest=spec['score_spec']['target_drive']
    above=[dest[0],dest[1],.90]
    phase('Carry drive above staging supports','right',tcp(above,[0,0,0,1]),down,.66,'drive',SIZE[1],mutate=lambda:drive_at(above,[0,0,0,1]))
    phase('Lower drive onto staging supports','right',tcp(dest,[0,0,0,1]),down,.66,'drive',SIZE[1],speed=.005,mutate=lambda:drive_at(dest,[0,0,0,1]))
    phase('Release staged drive','right',tcp(dest,[0,0,0,1]),down,1.,'drive')
    phase('Withdraw extraction gripper','right',[dest[0]+offset[0],dest[1],.90],down,1.)
    phase('Released staged-drive hold','right',[.28,-.17,.90],down,1.,dwell=2.5)
    return dict(schema=1,feedback='robot_proprioception_only',phases=phases)


if __name__=='__main__':
    spec=make_scene();(HERE/'scene.json').write_text(json.dumps(spec,indent=2)+'\n');(HERE/'controller.json').write_text(json.dumps(make_plan(spec),indent=2)+'\n')
    from build_assets import compile_assets
    compile_assets(spec,HERE/'assets')
