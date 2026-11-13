"""Original DCN680-procedure service fixture, not OEM CAD or measured hardware.

External nose door, independent lever, compliant draw bail and pin captured
under two arms follow manufacturer p12/FigJ. Hidden linkage/elastic dimensions
are explicit benchmark approximations. No firing mechanism is simulated.
"""
import json,math
from pathlib import Path
import dimensions as D
from primitives import body,box,cylinder,ring,quat
from motion import rotate
from kinematics import reconstruct
HERE=Path(__file__).resolve().parent
STEEL=[.48,.50,.52];BLUE=[.10,.34,.61];ORANGE=[.85,.39,.10];DARK=[.15,.15,.16]


def fixed_shape(s,role='steel'):
 s['role']=role;s['mass_density']={'steel':7850.,'aluminium':2700.,'polymer':1200.}[role];return s


def boxes(entries,color=STEEL,role='steel'):
 return [fixed_shape(box(p,s,color),role) for p,s in entries]


def member(name,shapes,mass,anchor=False):
 for shape in shapes:shape.setdefault('mass_density',7850.)
 b=body(name,D.ROOT,shapes,mass,anchor);b['quat']=D.BASE_Q.copy();return b


def local_ring(pos,inner,outer,length,color=STEEL,axis='Z'):
 q=quat([0,1,0],math.pi/2) if axis=='X' else [0,0,0,1]
 result=[]
 for shape in ring(inner,outer,length,count=32,color=color):
  shape['pos']=(rotate(q,shape['pos'])+pos).tolist();shape['quat']=__import__('motion').multiply(q,shape['quat']).tolist();result.append(fixed_shape(shape))
 return result


def joint(name,kind,parent,child,parent_pivot,child_pivot,axis,lo,hi,k=0.,damping=.0002):
 return dict(name=name,kind=kind,parent=parent,child=child,pivot_parent=parent_pivot,pivot_child=child_pivot,
             axis=axis,lower=lo,upper=hi,stiffness=k,damping=damping,rest=0.,initial=D.INITIAL[name],collision_enabled=True)


def make_scene():
 D.validate_mode()
 # Base and stops are a visible benchmark workholding fixture, not an alleged
 # supplied DeWalt accessory. Rotating the service frame keeps the firing axis
 # pointing away from the robots while all work stays above the normal table.
 shapes=boxes([([0,-.08,.0865],[.26,.36,.012])],BLUE,'aluminium')
 shapes+=boxes([([-.06,-.08,.06075],[.025,.12,.0395]),([.065,-.14,.04725],[.020,.030,.0665])],BLUE,'aluminium')
 # Original unpowered tool-shell envelope with an empty battery bay. It is
 # static workholding/context; no trigger, power or driver actuation is claimed.
 shapes+=boxes([([-.050,-.085,0],[.18,.008,.070]),([-.050,-.150,0],[.18,.008,.070]),
                ([-.138,-.1175,0],[.008,.065,.070]),([.038,-.1175,0],[.008,.065,.070]),
                ([-.050,-.1175,-.038],[.18,.065,.006]),([-.050,-.1175,.038],[.18,.065,.006])],DARK,'polymer')
 # Empty magazine envelope, tied into the nose housing, without loaded nails.
 
 # Two preinstalled clamp bridges visibly secure the tool case to this stand.
 # Their rods/bridges touch external shell/base surfaces; no powered actuation
 # or alleged manufacturer fixture is introduced.
 for x in (-.100,0.):
  shapes+=boxes([([x,-.1175,-.043],[.012,.105,.004])],BLUE,'aluminium')
  for y in (-.170,-.065):
   shapes.append(fixed_shape(cylinder([x,y,.01625],.003,.1285,STEEL)))
   shapes+=boxes([([x,y,-.0465],[.009,.009,.003])])
 shapes+=boxes([([.065,-.1555,0],[.025,.30,.028]),([.065,-.0205,0],[.025,.030,.028])],STEEL,'aluminium')
 # Open service trough and narrow U-shaped muzzle; ordinary straight brads
 # fit the muzzle. The pre-bent head fits its rear pocket but cannot exit the
 # closed narrow muzzle; opening the door supplies the missing extraction DOF.
 # Rear side overhang remains accessible to the stock parallel gripper.
 shapes+=boxes([([.0425,-.0035,0],[.085,.004,.016]),([.095,-.0035,0],[.020,.004,.028])])
 for z in (-.007,.007):shapes+=boxes([([.0475,.00025,z],[.075,.0035,.002])])
 for z in (-.00215,.00215):shapes+=boxes([([.0925,.00025,z],[.015,.0035,.0017])])
 # Continuous outer shoulders prevent bypassing the narrow muzzle around its
 # cheeks. Only the U-slot opens when the service door is lifted.
 for z in (-.0055,.0055):shapes+=boxes([([.0925,.00025,z],[.015,.0035,.005])])
 shapes+=boxes([([.007,.00025,0],[.004,.0035,.014])])
 # Pin-capture arms: fixed rear abutment and retaining lip, with the mouth
 # opening toward the muzzle. Both ends of the real crosspin must engage.
 for z in (-.012,.012):
  shapes+=boxes([([.0925,.0037,z],[.002,.0104,.003]),([.09475,.0089,z],[.0065,.003,.003])],ORANGE)
 # Real door hinge shaft and connected supports, with mating open bores.
 shapes.append(fixed_shape(cylinder([0,.0035,0],.002,.060,STEEL)))
 for z in (-.026,.026):shapes+=boxes([([0,0,z],[.008,.011,.006])])
 root=member('nose_body',shapes,3.5,True)
 door_shapes=boxes([([.0445,0,0],[.081,.003,.026]),([.0925,0,0],[.015,.003,.018])],BLUE)
 # Authored5mm side overhang at the rear supplies a real stock-gripper edge;
 # the front remains narrow enough to clear both pin-capture arms.
 for z in (-.009,.009):door_shapes+=local_ring([0,0,z],.0022,.004,.004,BLUE)
 # Lever axle is on the door, above its service face; its end brackets are
 # outside the moving lever hub, so enabled parent contacts remain honest.
 door_shapes.append(fixed_shape(cylinder(D.LEVER_PIVOT,.0016,.028,STEEL)))
 for z in (-.012,.012):door_shapes+=boxes([([.055,.0025,z],[.004,.005,.003])])
 door_shapes+=boxes([([.010,.0047,0],[.006,.003,.018])],DARK)  # closed lever stop
 door=member('nose_door',door_shapes,.075)
 lever_shapes=boxes([([-.0285,.002,0],[.051,.002,.017])],BLUE)
 for z in (-.006,.006):lever_shapes+=local_ring([0,0,z],.0018,.003,.003,BLUE)
 lever_shapes.append(fixed_shape(cylinder(D.ECCENTRIC,.0009,.044,STEEL)))
 for z in (-.010,.010):lever_shapes+=boxes([([-.005,.0004,z],[.002,.004,.003])])
 lever=member('latch_lever',lever_shapes,.025)
 bail_shapes=[]
 for z in (-D.BAIL_HALF_SPAN,D.BAIL_HALF_SPAN):
  bail_shapes+=local_ring([0,0,z],.00105,.0018,.002)
  length=D.DRAW_REST-.010
  bail_shapes+=boxes([([(length+.0018)/2,0,z],[length-.0018,.002,.002])])
  bail_shapes+=local_ring([D.DRAW_REST-.006,0,z],.0011,.0016,.008,axis='X')
  bail_shapes.append(fixed_shape(cylinder([D.DRAW_REST-.0105,0,z],.0016,.001,STEEL,quat([0,1,0],math.pi/2))))
 bail=member('draw_bail',bail_shapes,.012)
 end_shapes=[fixed_shape(cylinder([0,0,0],D.PIN_RADIUS,D.PIN_LENGTH,ORANGE))]
 for z in (-D.BAIL_HALF_SPAN,D.BAIL_HALF_SPAN):
  end_shapes.append(fixed_shape(cylinder([-.0045,0,z],.001,.009,STEEL,quat([0,1,0],math.pi/2))))
 end=member('bail_crosspin',end_shapes,.003)
 joints=[joint('door_rotation','revolute','nose_body','nose_door',D.DOOR_PIVOT,[0,0,0],'Z',0.,2.05,damping=.001),
         joint('lever_rotation','revolute','nose_door','latch_lever',D.LEVER_PIVOT,[0,0,0],'Z',-2.15,0.,damping=.0004),
         joint('bail_rotation','revolute','latch_lever','draw_bail',D.ECCENTRIC,[0,0,0],'Z',-math.pi,math.pi,damping=.00005),
         joint('bail_extension','prismatic','draw_bail','bail_crosspin',[D.DRAW_REST,0,0],[0,0,0],'X',-.0003,.0015,D.SPRING,1.)]
 # A genuinely free original pre-bent fastener, not a fixture-attached marker.
 nail_shapes=boxes([([.0025,0,0],[.045,.0010,.0012]),([-.020,0,-.002],[.0012,.0010,.0052]),([-.020,0,-.0044],[.003,.0010,.0012])],ORANGE)
 nail=member('bent_brad',nail_shapes,.00050);nail['pos']=(__import__('numpy').array(D.ROOT)+rotate(D.BASE_Q,[.095,0,.0007])).tolist()
 tray_shapes=boxes([([0,0,0],[.080,.090,.004])],BLUE,'aluminium')
 for x in (-.039,.039):tray_shapes+=boxes([([x,0,.010],[.002,.090,.020])],BLUE,'aluminium')
 for y in (-.044,.044):tray_shapes+=boxes([([0,y,.010],[.080,.002,.020])],BLUE,'aluminium')
 # Tray uses world-up coordinates; other mechanism solids use local service axes.
 tray=body('parts_tray',[.24,-.28,D.TABLE+.002],tray_shapes,.2,True)
 spec=dict(slug='brad-nailer-jam-recovery',title='Clear a brad-nailer nose jam and secure its draw latch',
  instruction='The tool is unpowered and its driver is retracted. Open the nose, remove the bent brad into the tray, then close the nose and secure the latch pin under both arms. Leave the tool and both hands clear.',
  geometry_mode=D.MODE,control_hz=20,physics_dt=1/1920,gravity=[0,0,-9.81],run_limit=5000,table_top=D.TABLE,hold_seconds=2.,penetration_limit=.00020,
  assemblies=[dict(name='nose_service_asset',origin=D.ROOT,fixed=True,bodies=[root,door,lever,bail,end],joints=joints),
              dict(name='bent_brad_asset',origin=nail['pos'],fixed=False,bodies=[nail],joints=[]),
              dict(name='parts_tray_asset',origin=tray['pos'],fixed=True,bodies=[tray],joints=[])],
  initial_joint_values=D.INITIAL.copy(),collision_exclusions=[],material=dict(static_friction=.65,dynamic_friction=.50,restitution=0.,contact_offset=.00002,rest_offset=0.),materials={},
  parameters=dict(firing_axis_local=[1,0,0],service_normal_local=[0,1,0],closed_pin_local=D.NOMINAL_PIN_CLOSED,initial_contact_deflection_m=D.INITIAL_CONTACT_DEFLECTION,draw_length=D.DRAW_LENGTH,draw_rest=D.DRAW_REST,bail_preload_extension=D.END_PRELOAD,bail_stiffness=D.SPRING,preload_force_N=D.SPRING*D.END_PRELOAD,driver_already_retracted=True,battery_absent=True,magazine_empty=True),
  limitations=['Original authored service fixture, not OEM dimensional compatibility, measured force or full powered nailer.', 'Rigid pre-bent brad; no deformation or firing. Effective axial draw compliance approximates wire-bail bending.','Visible workholding bench mount is original, not a supplied DeWalt accessory.'])
 poses=reconstruct(spec,root,D.INITIAL)
 for b in spec['assemblies'][0]['bodies']:b.update(poses[b['name']])
 return spec

if __name__=='__main__':
 spec=make_scene();(HERE/'scene.json').write_text(json.dumps(spec,indent=2)+'\n')
 from build_assets import compile_assets
 compile_assets(spec,HERE/'assets')
