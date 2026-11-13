"""Manufacturer-dimensional ER32 collet with original eccentric-cam bench nut.

Only unloaded nut/collet preassembly is modeled. No toolholder tightening,
compression, cutting-tool pullout or unsupported cam retention is claimed.
"""
import copy,json,math
from pathlib import Path
from primitives import box,cylinder,ring,body,quat
from motion import rotate,multiply,axis_quat
HERE=Path(__file__).resolve().parent
TABLE=.7475
CENTER=[.24,0,.8055]
PICK=[.28,-.17,.8055]
STEEL=[.48,.50,.52];BLUE=[.10,.34,.61];GOLD=[.72,.49,.14]
GROOVE=.0036;LENGTH=.040;HEAD=.0055
PIVOT=[-.0156,0,0]
ANGLE=-.25


def collet_shapes():
    # REGO-FIX dimensional sheet Drawing4, 8mm ER32: 40mm total,
    # D1=33 / D2=32 / D3=29.2, groove L2=3.6, nose L3=5.5, 8/30deg.
    shapes=ring(.004,.0146,GROOVE,count=64)
    for lo,hi,r0,slope,n in [(.0018,.0327,.016,-math.tan(math.radians(8)),24),
                             (-.0073,-.0018,.0165-HEAD*math.tan(math.radians(30)),math.tan(math.radians(30)),8)]:
        dz=(hi-lo)/n
        for i in range(n):
            a=lo+i*dz;b=a+dz
            r=max(r0+slope*(a-lo),r0+slope*(b-lo))
            # Original rigid contact approximants retain through-bore. Slots
            # are omitted because this unloaded operation never clamps a tool.
            shapes+=ring(.004,r,dz,z=(a+b)/2,count=48)
    return shapes


def eccentric_lip():
    shapes=[];offset=.0029;inner=.0185;outer=.0190;count=128
    for i in range(count):
        a=2*math.pi*i/count
        radius=offset*math.cos(a)+math.sqrt(inner**2-offset**2*math.sin(a)**2)
        if radius>=outer:continue
        shapes.append(box([(radius+outer)/2*math.cos(a),(radius+outer)/2*math.sin(a),0],
            [outer-radius,2*outer*math.tan(math.pi/count),.0006],GOLD,quat([0,0,1],a)))
    return shapes


def hook_pose(angle=ANGLE):
    q=axis_quat([0,1,0],angle).tolist()
    pos=(CENTER+(-rotate(q,PIVOT)+PIVOT)).tolist()
    return pos,q


def make_scene():
    # Fixed surrogate nut held by an original bench clamp. Its inner cam
    # geometry is explicitly authored, not an undocumented REGO-FIX drawing.
    nut_shapes=ring(.0202,.025,.020,z=.012,color=BLUE)
    nut_shapes+=ring(.0190,.025,.004,z=0,color=BLUE)
    nut_shapes+=eccentric_lip()
    # Three lower pads support the front face so final preassembly never
    # assumes the manufacturer cam can suspend an unsupported collet.
    foot=CENTER[2]-TABLE
    nut_shapes += [box([x,y,-foot/2],[.012,.012,foot],BLUE) for x,y in [(-.030,0),(.030,0),(0,.03)]]
    for a in [0,2*math.pi/3,4*math.pi/3]:
        nut_shapes.append(box([.010*math.cos(a),.010*math.sin(a),(-foot-.0073)/2],[.003,.003,foot-.0073],BLUE))
    nut=body('bench_nut',CENTER.copy(),nut_shapes,.30,True)
    collet=body('collet',PICK.copy(),collet_shapes(),.15)
    # Initial cradle supports the nose annulus only, clear of the bore and grip.
    tray=ring(.006,.018,.010,z=-.0123,color=BLUE)
    tray+=[box([.024,0,-foot/2],[.012,.05,foot],BLUE)]
    cradle=body('collet_cradle',PICK.copy(),tray,.10,True)
    assemblies=[dict(name=b['name']+'_asset',origin=b['pos'].copy(),fixed=b['anchor'],bodies=[b],joints=[]) for b in [nut,collet,cradle]]
    return dict(slug='er-collet-nut-preassembly',title='Engage an ER collet groove with an eccentric nut cam',
      instruction='Prepare the supported ER nut and collet for later toolholder installation. Pick up the collet, tilt it to engage its extraction groove at the marked eccentric-cam side, and rock it upright into the supported nut. Release and withdraw the grippers. Do not insert a cutting tool or tighten a holder.',
      control_hz=20,physics_dt=1/480,gravity=[0,0,-9.81],run_limit=2400,table_top=TABLE,hold_seconds=2.,penetration_limit=.00035,
      assemblies=assemblies,collision_exclusions=[],
      score_spec=dict(initial_collet=PICK.copy(),target=CENTER.copy(),hook_pivot=PIVOT,hook_angle=ANGLE,anchors={b['name']:dict(pos=b['pos'],quat=b['quat']) for b in [nut,cradle]},
        lateral_tolerance=.0006,axial_tolerance=.0003,angle_tolerance=.025,hook_position_tolerance=.001,hook_angle_tolerance=.06,
        hold_seconds=2.,control_hz=20,release_clearance=.020,speed_limit=.008,spin_limit=.15,penetration_limit=.00035,fixture_tolerance=.001,loss_plane=TABLE-.02),
      parameters=dict(grasp_offset_z=.036,collet_D1=.033,collet_D2=.032,collet_D3=.0292,collet_length=LENGTH,collet_groove_width=GROOVE,collet_nose_length=HEAD,collet_bore=.008,
        taper_angle=math.radians(8),nose_angle=math.radians(30),cam_inner_radius=.0185,cam_eccentricity=.0029,cam_thickness=.0006,
        nut_front_bore_radius=.0190,nut_upper_bore_radius=.0202,nut_outer_radius=.025,hook_angle=ANGLE,collet_mass=.15),
      material=dict(static_friction=.65,dynamic_friction=.5,restitution=0.,contact_offset=.00003,rest_offset=0.),
      limitations=['Collet nominal diameters/length/profile angles follow REGO-FIX Drawing4; rigid faceted unslotted approximation.',
        'Cam/nut/clamp/support geometry, mass, friction and alignment tolerances are benchmark-authored.',
        'Manufacturer notes eccentric cam is not guaranteed to hold an unsupported collet; final state is supported.',
        'No spindle/thread tightening, tool insertion, elastic collapse, runout or cutting-load retention is evaluated.'])


def make_plan(spec):
    from yam_arena.demo import DOWN_GRIP
    down=DOWN_GRIP.tolist();states={b['name']:dict(pos=b['pos'].copy(),quat=b['quat'].copy()) for a in spec['assemblies'] for b in a['bodies']};phases=[]
    def phase(label,pos,q=down,opening=1.,width=0.,dwell=.12,speed=.06,pose=None):
        if pose:states['collet']=dict(pos=list(pose[0]),quat=list(pose[1]))
        phases.append(dict(label=label,side='right',target=dict(pos=list(pos),quat=q),opening=opening,grasp_width=width,contact_body='collet' if width else None,
            dwell=dwell,speed=speed,timeout=40.,position_tolerance=.00025,angle_tolerance=.02,nominal_bodies=copy.deepcopy(states)))
    def tcp(pos,q):return (pos+rotate(q,[0,0,spec['parameters']['grasp_offset_z']])).tolist()
    identity=[0,0,0,1];width=.027
    phase('Initialize handling arm',[.28,-.17,.90])
    phase('Approach ER collet',[PICK[0],PICK[1],.90])
    phase('Reach collet tapered body',tcp(PICK,identity))
    phase('Grip collet tapered body',tcp(PICK,identity),opening=.22,width=width,dwell=.3)
    up=[*PICK[:2],.870]
    phase('Lift collet from cradle',tcp(up,identity),opening=.22,width=width,pose=(up,identity))
    high=[CENTER[0],CENTER[1],.870]
    phase('Transfer above supported nut',tcp(high,identity),opening=.22,width=width,pose=(high,identity))
    hook,q=hook_pose();tool=multiply(q,down).tolist()
    approach=[CENTER[0]+.0025,CENTER[1],.850]
    phase('Tilt for eccentric cam entry',tcp(approach,q),tool,.22,width,pose=(approach,q))
    prehook=[CENTER[0]+.0025,CENTER[1],hook[2]]
    phase('Lower tilted nose through eccentric opening',tcp(prehook,q),tool,.22,width,speed=.008,pose=(prehook,q))
    phase('Engage groove at eccentric hook',tcp(hook,q),tool,.22,width,speed=.006,pose=(hook,q))
    for i in range(1,21):
        p,q=hook_pose(ANGLE*(1-i/20));tool=multiply(q,down).tolist()
        phase(f'Rock groove onto cam increment {i}',tcp(p,q),tool,.22,width,speed=.008,pose=(p,q))
    phase('Release supported preassembly',tcp(CENTER,identity),opening=.65,dwell=.25)
    phase('Withdraw above preassembly',[CENTER[0],CENTER[1],.91],opening=.65)
    phase('Park handling arm',[.28,-.17,.90],opening=1.)
    phase('Supported preassembly hold',[.28,-.17,.90],opening=1.,dwell=2.2)
    return dict(schema=1,feedback='robot_proprioception_only',phases=phases)

if __name__=='__main__':
    spec=make_scene();(HERE/'scene.json').write_text(json.dumps(spec,indent=2)+'\n');(HERE/'controller.json').write_text(json.dumps(make_plan(spec),indent=2)+'\n')
    from build_assets import compile_assets
    compile_assets(spec,HERE/'assets')
