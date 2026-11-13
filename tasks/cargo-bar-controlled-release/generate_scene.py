"""Original contact-driven rack/pawl cargo-bar benchmark fixture.

Manufacturer-documented procedure and40–70in range identify the reference class;
unreported component geometry, masses, springs and contact parameters are explicit
benchmark-authored approximations. No per-stroke advancement or virtual clutch.
"""
import copy,json,math
from pathlib import Path
from primitives import box,cylinder,ring,body,quat
from motion import rotate,multiply,axis_quat
from gearing import pinion,rack,ratchet_wheel,RADIUS,PITCH
HERE=Path(__file__).resolve().parent
TABLE=.7475
CENTER=[.24,0,TABLE+.050]
BASEQ=quat([0,1,0],-math.pi/2)
GEAR=[0,0,-.032]
BLUE=[.10,.34,.61];STEEL=[.48,.50,.52];RUBBER=[.15,.15,.16];ORANGE=[.85,.39,.10]


def transformed(shapes,q,pos):
 result=[]
 for shape in shapes:
  s=copy.deepcopy(shape);s['pos']=(rotate(q,s['pos'])+pos).tolist();s['quat']=multiply(q,s['quat']).tolist();result.append(s)
 return result


def member(name,local,shapes,mass):
 for shape in shapes:
  if shape.get('role')=='protective_housing':density=1200.
  elif name in ('left_pad','right_pad'):density=580. if shape['kind']=='box' else 7850.
  elif shape.get('material')=='cam' or shape.get('role') in ('steel_rack','rack_guide'):density=7850.
  elif name in ('outer_tube','inner_tube'):density=2700.
  else:density=7850.
  shape['mass_density']=density
 b=body(name,(rotate(BASEQ,local)+CENTER).tolist(),shapes,mass);b['quat']=BASEQ.copy();return b


def pawl_shapes(release=None):
 # Pivot at(-Y,+Z) relative to the wheel. Return flank raises the tip; the
 # radial locking flank pushes it toward the mechanical lower stop.
 length=math.hypot(.0162,0.)
 # A bowed structural arm clears neighbouring tooth tips. The load-bearing
 # nose lies at pivot height, permitting release without driving into the flank.
 shapes=[box([0,.004,.003],[.004,.010,.0018],STEEL,quat([1,0,0],math.atan2(.006,.008))),
         box([0,.0162,0],[.004,.0024,.0020],ORANGE),
         box([0,.0121,.0045],[.004,math.hypot(.0082,.003),.0018],STEEL,quat([1,0,0],math.atan2(-.003,.0082))),
         box([0,.0162,.0015],[.004,.0018,.003],STEEL)]
 if release:
  x,y,z=release;length=math.hypot(y,z)
  shapes.append(box([0,y/2,z/2],[.004,length,.0025],STEEL,quat([1,0,0],math.atan2(z,y))))
  shapes.append(box([x/2,y,z],[abs(x)+.004,.004,.0025],ORANGE))
  shapes.append(box([x,y,z],[.006,.005,.0025],ORANGE))
 for shape in shapes[-2:] if release else []:shape['material']='cam'
 return shapes


def arc_cam(x,start,end,inner,radial,offset=(0,0,0),pieces=32):
 from convex_primitives import prism_x
 # One convex sector avoids artificial internal collision faces between cam
 # slices. The inner chord leaves a genuine open bearing clearance.
 points=[[inner*math.sin(start),inner*math.cos(start)],
         [inner*math.sin(end),inner*math.cos(end)]]
 for i in range(pieces+1):
  a=start+(end-start)*i/pieces;r=radial(a);points.append([r*math.sin(a),r*math.cos(a)])
 shape=prism_x(points,.006,pos=[x+offset[0],offset[1],offset[2]],color=ORANGE);shape['material']='cam'
 return [shape]


def joint(name,kind,parent,child,pivot_parent,pivot_child,axis,lower,upper,stiffness=0.,damping=.02,rest=0.):
 return dict(name=name,kind=kind,parent=parent,child=child,pivot_parent=pivot_parent,pivot_child=pivot_child,
             axis=axis,lower=lower,upper=upper,stiffness=stiffness,damping=damping,rest=rest,collision_enabled=True)


def housing_shapes():
 # Original rigid polycarbonate guard, not claimed OEM dimensions. Closed
 # sidewalls and close-fitting circular tube/hub ports prevent direct fingers
 # reaching the pawl followers while leaving the actual handle/trigger free.
 shapes=[]
 def panel(center,size):shapes.append(box(center,size,BLUE))
 low,high=-.035,.0505;mid=(low+high)/2;height=high-low
 zlo,zhi=GEAR[2]-.066,GEAR[2]+.066
 # Floor stops0.5mm before the shaft end and1mm above the frame base at rest.
 panel([-.03425,.0225,GEAR[2]],[.0015,.197,.132])
 # Two continuous long walls.
 for z in (zlo,zhi):panel([mid,.0225,z],[height,.197,.0015])
 # End panels with genuine circular tube clearances, not square corner holes.
 for y,radius,slot in [(-.075,.01875,.021),(.120,.01325,.015)]:
  for x0,x1 in [(low,-slot),(slot,high)]:
   panel([(x0+x1)/2,y,(zlo+zhi)/2],[x1-x0,.0015,zhi-zlo])
  for z0,z1 in [(zlo,-slot),(slot,zhi)]:
   panel([0,y,(z0+z1)/2],[2*slot,.0015,z1-z0])
  shapes+=transformed(ring(radius,slot*math.sqrt(2)+.001,.0015,count=64,color=BLUE),
                      quat([1,0,0],math.pi/2),[0,y,0])
 # Ceiling panels join an annular hub opening. The square panel opening is
 # completely covered by the overlapping ring, leaving only the circular bore.
 slot=.0105
 for y0,y1 in [(-.076,-slot),(slot,.121)]:
  panel([.050,(y0+y1)/2,GEAR[2]],[.001,y1-y0,.132])
 for z0,z1 in [(zlo,GEAR[2]-slot),(GEAR[2]+slot,zhi)]:
  panel([.050,0,(z0+z1)/2],[.001,2*slot,z1-z0])
 shapes+=transformed(ring(.008,.015,.001,count=64,color=BLUE),quat([0,1,0],math.pi/2),[.050,0,GEAR[2]])
 for shape in shapes:shape['role']='protective_housing'
 return shapes


def make_scene():
 # Original wall frame, plus two passive cradles that support weight only.
 frame_shapes=[box([0,0,.005],[.22,1.32,.010],BLUE)]
 for y in (-.611,.611):frame_shapes.append(box([0,y,.070],[.16,.022,.140],BLUE))
 for y in (-.30,.30):
  height=.028 if y<0 else .0335
  frame_shapes.append(box([0,y,height/2],[.040,.035,height],BLUE))
  for x in (-.026,.026):frame_shapes.append(box([x,y,.0325],[.008,.035,.065],BLUE))
 frame=body('wall_frame',[CENTER[0],0,TABLE],frame_shapes,11.,True)
 # Round hollow tube, not an undersized plate with a cosmetic bar label.
 outer_shapes=transformed(ring(.014,.018,.510,count=48,color=STEEL),quat([1,0,0],math.pi/2),[0,-.315,0])
 # Open service window for the rack and release link; the rear circular guide
 # remains full length. This is an explicit authored housing cutout.
 end_shapes=transformed(ring(.014,.018,.180,count=48,color=STEEL),quat([1,0,0],math.pi/2),[0,.030,0])
 outer_shapes += [shape for shape in end_shapes if shape['pos'][0]<=-.012]
 outer_shapes+=transformed(ring(.014,.018,.050,count=48,color=STEEL),quat([1,0,0],math.pi/2),[0,.145,0])
 # Rack edge guides prevent rotation of the real inner member. Their supports
 # pass below the rack outside the wheel envelope, not through moving solids.
 for x,width in [(-.0083,.002),(.008,.0014)]:
  shape=box([x,.045,-.0156],[width,.170,.004],STEEL);shape['role']='rack_guide';outer_shapes.append(shape)
 for y in (-.030,.030,.090):
  outer_shapes.append(box([-.0213,y,-.0156],[.026,.006,.004],BLUE))
  outer_shapes.append(box([-.012975,y,-.026],[.045,.006,.004],BLUE))
  outer_shapes.append(box([.0083,y,-.021],[.002,.006,.014],BLUE))
 # All moving pairs, including joined parent/child bodies, retain collisions.
 # Real open bearings and connected brackets, not solid plates across a shaft.
 for x in (-.024,.032):
  outer_shapes+=transformed(ring(.0067,.012,.006,count=40,color=BLUE),quat([0,1,0],math.pi/2),[x,GEAR[1],GEAR[2]])
  dy,dz=.026,.044;length=math.hypot(dy,dz);start=.010/length
  outer_shapes.append(box([x,dy*(1+start)/2,GEAR[2]+dz*(1+start)/2],[.006,length-.010,.006],BLUE,quat([1,0,0],math.atan2(dz,dy))))
  target=.018 if x>0 else -.018
  outer_shapes.append(box([(x+target)/2,.026,.012],[abs(x-target)+.006,.009,.008],BLUE))
 # A bridge above the inner tube joins both bearing supports to the retained
 # tube shell without filling the shaft bore or colliding with the rack.
 outer_shapes.append(box([0,.026,.022],[.062,.009,.006],BLUE))
 for x in (-.024,.032):outer_shapes.append(box([x,.026,.017],[.006,.009,.016],BLUE))
 # Connected closed-handle keeper, beyond the rotating carrier's axial plane.
 outer_shapes += [box([.065,.015,GEAR[2]+.0095],[.008,.008,.005],ORANGE),
                  box([.065,.010,GEAR[2]-.024],[.008,.004,.072],BLUE),
                  box([.0575,.010,GEAR[2]-.060],[.019,.004,.004],BLUE),
                  box([.03925,.026,.022],[.0225,.009,.006],BLUE)]
 outer_shapes+=arc_cam(.046,-3.15,-1.00,.0330,lambda a:.0345+.007*min(1.,max(0.,(-a-1.00)/1.45)),GEAR)
 outer_shapes+=transformed(ring(.008,.012,.006,count=40,color=BLUE),quat([0,1,0],math.pi/2),[.029,0,GEAR[2]])
 outer_shapes.append(box([.048,0,GEAR[2]-.040],[.006,.004,.004],BLUE))
 a=-3.15;outer_shapes.append(box([.046,.0255*math.sin(a),GEAR[2]+.0255*math.cos(a)],[.006,.002,.033],BLUE,quat([1,0,0],-a)))
 outer_shapes+=transformed(ring(.0054,.014,.008,count=40,color=STEEL),quat([1,0,0],math.pi/2),[0,-.566,0])
 outer_shapes+=housing_shapes()
 outer=member('outer_tube',[0,0,0],outer_shapes,1.05)
 inner_shapes=transformed(ring(.009,.0125,.600,count=40,color=STEEL),quat([1,0,0],math.pi/2),[0,.270,0])
 # Pinion is offset32mm from the tube axis. The rack pitch plane is exactly
 # one pitch radius from its centre, with50um radial design clearance.
 rack_shapes=transformed(rack(length=.10,pitch_plane=GEAR[2]+RADIUS+.00005,phase=PITCH/2),[0,0,0,1],[0,-.040,0])
 for shape in rack_shapes:shape['role']='steel_rack'
 inner_shapes+=rack_shapes
 for y in (-.025,.010,.045):inner_shapes.append(box([0,y,-.0125],[.010,.006,.004],STEEL))
 inner_shapes+=transformed(ring(.0054,.009,.008,count=40,color=STEEL),quat([1,0,0],math.pi/2),[0,.566,0])
 inner=member('inner_tube',[0,0,0],inner_shapes,.48)
 left=member('left_pad',[0,-.584,0],[box([0,0,0],[.0635,.012,.1016],RUBBER),cylinder([0,.012,0],.0048,.024,STEEL,quat([1,0,0],math.pi/2))],.06)
 right=member('right_pad',[0,.584,0],[box([0,0,0],[.0635,.012,.1016],RUBBER),cylinder([0,-.012,0],.0048,.024,STEEL,quat([1,0,0],math.pi/2))],.06)
 left['shapes'][0]['material']='pad';right['shapes'][0]['material']='pad'
 gears=pinion()+transformed(ratchet_wheel(),quat([1,0,0],.029),[.016,0,0])+[cylinder([0,0,0],.0048,.066,STEEL,quat([0,1,0],math.pi/2))]
 gear=member('gear_set',GEAR,gears,.16)
 # Hollow slide guide: the trigger stem is not embedded in a solid beam.
 handle_shapes=[box([.060,.070,0],[.012,.012,.010],BLUE),
                box([.05225,.034,0],[.003,.072,.0105],BLUE),
                box([.054,.070,0],[.002,.010,.010],BLUE)]
 for z in (-.0045,.0045):handle_shapes.append(box([.056,.0185,z],[.004,.041,.0015],BLUE))
 # Front cover with a real slot for the moving latch cross-link.
 for y0,y1 in [(-.002,.0135),(.0315,.039)]:
  handle_shapes.append(box([.0595,(y0+y1)/2,0],[.001,y1-y0,.0105],BLUE))
 for z0,z1 in [(-.00525,-.0015),(.0015,.00525)]:
  handle_shapes.append(box([.0595,.0225,(z0+z1)/2],[.001,.018,z1-z0],BLUE))
 for z in (-.0045,.0045):handle_shapes.append(box([.05725,.036,z],[.0065,.003,.0015],BLUE))
 handle_shapes+=transformed(ring(.0054,.0062,.040,count=40,color=BLUE),quat([0,1,0],math.pi/2),[.044,0,0])
 a=2.82;handle_shapes.append(box([.040,.017*math.sin(a),.017*math.cos(a)],[.006,.003,.028],BLUE,quat([1,0,0],-a)))
 handle_shapes+=arc_cam(.040,1.85,2.85,.0250,lambda a:.0275+.009*min(1.,max(0.,(a-1.85)/.70)))
 handle=member('handle',GEAR,handle_shapes,.07)
 trigger=member('release_trigger',GEAR,[box([.060,.045,0],[.012,.006,.010],ORANGE),
             box([.056,.027,0],[.004,.034,.004],ORANGE),
             box([.060,.018,0],[.008,.006,.002],ORANGE),
             box([.0625,.018,.002],[.004,.006,.004],ORANGE),
             box([.064,.018,.004],[.006,.006,.003],ORANGE)],.012)
 holding=member('holding_pawl',[.0155,-.018,GEAR[2]+.020],pawl_shapes((.0245,.020,.011)),.008)
 driving=member('driving_pawl',[.020,-.018,GEAR[2]+.020],pawl_shapes((.026,.010,.019)),.008)
 joints=[joint('telescope','prismatic','outer_tube','inner_tube',[0,0,0],[0,0,0],'Y',0,.05,damping=.05),
         joint('left_compliance','prismatic','outer_tube','left_pad',[0,-.584,0],[0,0,0],'Y',0,.004,12000.,12.),
         joint('right_compliance','prismatic','inner_tube','right_pad',[0,.584,0],[0,0,0],'Y',-.004,0,12000.,12.),
         joint('pinion_rotation','revolute','outer_tube','gear_set',GEAR,[0,0,0],'X',-8,8,damping=.00005),
         joint('handle_rotation','revolute','outer_tube','handle',GEAR,[0,0,0],'X',0,2.60,damping=.002),
         joint('trigger_pull','prismatic','handle','release_trigger',[0,0,0],[0,0,0],'Y',0,.009,80.,.2),
         joint('holding_pawl_rotation','revolute','outer_tube','holding_pawl',[.0155,-.018,GEAR[2]+.020],[0,0,0],'X',-.02,.8,.02,.0004),
         joint('driving_pawl_rotation','revolute','handle','driving_pawl',[.020,-.018,.020],[0,0,0],'X',-.02,.8,.02,.0004)]
 mechanism=[outer,inner,left,right,gear,handle,trigger,holding,driving]
 initial_extension=7*(2*math.pi/24)*RADIUS
 initial_pad=(initial_extension-.020)/2
 initial_root=dict(pos=[CENTER[0],-.010-initial_pad,CENTER[2]],quat=BASEQ)
 initial={'telescope':initial_extension,'pinion_rotation':-initial_extension/RADIUS,
          'left_compliance':initial_pad,'right_compliance':-initial_pad}
 for j in joints:j['initial']=initial.get(j['name'],0.)
 spec=dict(slug='cargo-bar-controlled-release',title='Release and shorten a clamped cargo load bar',
   instruction='Remove the clamping load and shorten the cargo bar until both feet clear the walls. Leave it unloaded on both cradles with both grippers clear.',
   control_hz=20,physics_dt=1/960,gravity=[0,0,-9.81],run_limit=5000,table_top=TABLE,hold_seconds=2.,penetration_limit=.00035,
   assemblies=[dict(name='wall_frame_asset',origin=frame['pos'],fixed=True,bodies=[frame],joints=[]),
               dict(name='cargo_bar_asset',origin=initial_root['pos'],fixed=False,bodies=mechanism,joints=joints)],
   collision_exclusions=[],material=dict(static_friction=.65,dynamic_friction=.5,restitution=0.,contact_offset=.00003,rest_offset=0.),
   materials=dict(cam=dict(static_friction=.12,dynamic_friction=.08,restitution=0.,classification='Benchmark-authored approximation; greased cam/follower contact, not measured OEM material'),
                  pad=dict(static_friction=.80,dynamic_friction=.65,restitution=0.,cpu_dynamic_against_default=.575,classification='Benchmark-authored dry elastomer/steel assumption. CPU .575 is the mean of pad .65 and default metal .50; no manufacturer measurement.')),
   parameters=dict(reference_minimum_length=1.016,reference_maximum_length=1.778,wall_span=1.200,
      authored_initial_foot_span=1.180,authored_pad_stiffness=12000.,authored_gear_pitch=PITCH,authored_pinion_pitch_radius=RADIUS,
      authored_gear_teeth=20,authored_ratchet_teeth=24,authored_ratchet_phase=.029,authored_fixture_geometry=True,authored_housing_hub_bore_radius=.008,authored_housing_outer_port_radius=.01875,authored_housing_inner_port_radius=.01325,authored_outer_tube_length=.740,authored_inner_tube_length=.600,authored_rack_side_clearance=.0003),
   limitations=['Original benchmark fixture, not OEM dimensional compatibility or measured cargo rating.',
       'Steel gear/rack/pawls and spring-pad surrogates preserve contact-driven advancement/retention. Pad compliance is authored, not measured rubber data.',
       'Bar starts clamped 4mm above the weight-support cradles. No vehicle, live cargo or load certification is simulated.'])

 from kinematics import reconstruct
 poses=reconstruct(spec,initial_root,{j['name']:j['initial'] for j in joints})
 for b in mechanism:b.update(poses[b['name']])
 spec['initial_joint_values']={j['name']:j['initial'] for j in joints}
 spec['parameters'].update(authored_initial_extension=initial_extension,authored_initial_pad_compression=initial_pad,
                           authored_neutral_root=CENTER,authored_cradle_root=[CENTER[0],0,TABLE+.046])
 return spec

if __name__=='__main__':
 spec=make_scene();(HERE/'scene.json').write_text(json.dumps(spec,indent=2)+'\n')
 from build_assets import compile_assets
 compile_assets(spec,HERE/'assets')
