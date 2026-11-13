"""Original inert chisel-change scene with real groove/key/ball/sleeve contacts."""
import json,math
from pathlib import Path
import numpy as np
import dimensions as D
from motion import axis_quat,rotate
from primitives import box,cylinder,body,assembly
from cad import annular_slice,shank,faceted_ball,convex
HERE=Path(__file__).resolve().parent

def joint(name,parent,child,axis,pivot,lower,upper,initial=0.,stiffness=0.,damping=0.,rest=0.):
 return dict(name=name,kind='prismatic',parent=parent,child=child,axis=axis,pivot_parent=pivot,pivot_child=[0,0,0],lower=lower,upper=upper,initial=initial,stiffness=stiffness,damping=damping,rest=rest,collision_enabled=True)

def make_scene():
 D.validate();root=np.array(D.ROOT);shapes=[]
 # Tube surrounding the actual shank. A6.2mm port leaves an inward retaining lip;
 # its ball is a free body, not a radial joint or a virtual latch.
 for x0,x1 in [(0.,D.BALL_X-D.PORT_HALF),(D.BALL_X-D.PORT_HALF,D.BALL_X+.0045+D.PORT_HALF),(D.BALL_X+.0045+D.PORT_HALF,.055)]:
  port=x0<D.BALL_X<x1
  shapes+=annular_slice(x0,x1,D.HOLDER_INNER,D.HOLDER_INNER,D.HOLDER_OUTER,skip=(lambda a:math.sin(a)>.84) if port else None,role='holder_bore_with_real_ball_port')
 # Authored one-way ball race: front stop and a rear insertion relief.
 # The ball can roll/slide4.5mm rearward during insertion, while forward
 # withdrawal loads it against a positive fixed stop beneath the sleeve land.
 for x in (D.BALL_X-.00455,D.BALL_X+.00905):shapes.append(box([x,0,.0079],[.002,.0111,.0034]))
 for sign in (-1,1):
  shapes.append(box([D.BALL_X+.00225,sign*.00455,.0079],[.0116,.002,.0034]))
  # Actual sloping inner lips bias the free ball back to its locked forward
  # location under gravity. This is authored fixture engineering, not OEM CAD.
  pts=[]
  for x in (.0169,.0276):
   for y,z in [(sign*.0031,.0048),(sign*.00555,.0048),(sign*.00555,.0062+.10*(x-.020)),(sign*.0031,.0062+.10*(x-.020))]:pts.append([x,y,z])
  shapes.append(convex(pts,role='authored_gravity_return_lip'))
 # Two opposed drive keys occupy open-ended grooves; closed slots are90deg away.
 for s in (-1,1):shapes.append(box([.0085,s*.005,.0],[.007,.0024,.0014]))
 for shape in shapes:shape.update(material='lubricated',mass_density=7850.)
 # A real clear polycarbonate insert replaces the non-load-bearing positive-Y
 # guide wall; every collision face remains. It supports calibrated inspection.
 for shape in shapes:
  if shape['kind']=='box' and abs(shape['pos'][1]-.00455)<1e-9 and shape['size']==[.0116,.002,.0034]:shape.update(material='inspection_lubricated',mass_density=1200.,opacity=.12,color=[.72,.88,.98],role='physical_clear_ball_guide_window')

 # Rear mechanical stop prevents over-insertion; context casing and workholding.
 shapes.append(box([.047,0,0],[.004,.012,.012]))
 shapes.append(cylinder([.11,0,0],.032,.11,[.12,.25,.40],axis_quat([0,1,0],math.pi/2).tolist()))
 shapes.append(box([.14,0,-.05],[.036,.036,.065],[.12,.25,.40]))
 basez=D.TABLE+.006-root[2];shapes.append(box([.12,0,basez],[.19,.18,.012],[.24,.25,.27]))
 for x in (.073,.155):
  shapes.append(box([x,0,(basez+.006-.031)/2],[.014,.065,-.031-(basez+.006)],[.35,.37,.39]))
  # Visible clamps reach the case top and connect to the base through rods.
  shapes.append(box([x,0,.035],[.014,.09,.008],[.55,.57,.59]))
  for y in (-.038,.038):shapes.append(box([x,y,(basez+.006+.035)/2],[.008,.008,.035-(basez+.006)],[.55,.57,.59]))
 holder=body('tool_holder',D.ROOT,shapes,3.0,True)
 collarsh=[]
 for a,b,r0,r1 in [(-.002,.015,D.COLLAR_BORE_RELEASED,D.COLLAR_BORE_RELEASED),(.015,.017,D.COLLAR_BORE_RELEASED,D.COLLAR_BORE_CLOSED),(.017,.022,D.COLLAR_BORE_CLOSED,D.COLLAR_BORE_CLOSED),(.022,.024,D.COLLAR_BORE_CLOSED,D.COLLAR_BORE_RELEASED),(.024,.035,D.COLLAR_BORE_RELEASED,D.COLLAR_BORE_RELEASED)]:collarsh+=annular_slice(a,b,r0,r1,.014,color=[.15,.17,.19],role='positive_locking_land_and_front_rear_reliefs')
 for shape in collarsh:shape.update(material='lubricated',mass_density=7850.)
 # The roof over the ball remains steel. Clear side sectors allow a +Y photo
 # through the original inspection fixture without deleting any collider.
 for shape in collarsh:
  angle=math.atan2(shape['pos'][2],shape['pos'][1])
  if math.radians(20)<=angle<=math.radians(75):shape.update(material='inspection_lubricated',mass_density=2500.,opacity=.12,color=[.72,.88,.98],role='physical_glass_cam_side_window')

 collarsh+=annular_slice(-.002,.035,.014,.014,D.COLLAR_OUTER,color=[.15,.17,.19],role='dry_gripping_shell',inner_circumscribed=False)
 # Outer gripping shell is dry; only the inner cam is lightly lubricated.
 for shape in collarsh:
  if 'mass_density' not in shape:shape.update(mass_density=1200.,opacity=.12,color=[.72,.88,.98])
 from mass_properties import primitive
 collar_mass=sum(primitive(shape)[0]*shape['mass_density'] for shape in collarsh)
 collar=body('locking_sleeve',D.ROOT,collarsh,collar_mass)
 j=joint('sleeve_retraction','tool_holder','locking_sleeve','X',[0,0,0],0.,D.COLLAR_TRAVEL,0.,2000.,5.,-.001)
 ball=body('locking_ball',(root+[D.BALL_X,0,D.BALL_Z]).tolist(),[dict(kind='sphere',pos=[0.,0.,0.],quat=[0.,0.,0.,1.],radius=D.BALL_RADIUS,color=[.68,.70,.72],role='manufacturer_documented_7mm_sphere')],7850*4/3*math.pi*D.BALL_RADIUS**3)
 ball['shapes'][0].update(material='lubricated',mass_density=7850.)
 from mass_properties import compound
 ball.update(compound(ball['shapes'],ball['mass']))
 bitsh=shank()
 for shape in bitsh:shape.update(material='lubricated',mass_density=7850.)
 shaft=cylinder([-.1125,0,0],.006,.135,[.50,.52,.54],axis_quat([0,1,0],math.pi/2).tolist());shaft['role']='inert_chisel_stem';bitsh.append(shaft)
 def chisel(name,pos,flat,roll):
  import copy
  ss=copy.deepcopy(bitsh)
  # Blunt original tips: cutting/breaking concrete is outside this operation.
  if flat:ss.append(convex([[-.200,y,z] for y in (-.010,.010) for z in (-.001,.001)]+[[-.180,y,z] for y in (-.006,.006) for z in (-.006,.006)],[.58,.60,.62],'blunt_flat_chisel_tip'))
  else:ss.append(convex([[-.200,y,z] for y in (-.001,.001) for z in (-.001,.001)]+[[-.180,y,z] for y in (-.006,.006) for z in (-.006,.006)],[.48,.50,.52],'blunt_point_chisel_tip'))
  for shape in ss:shape['mass_density']=7850.
  bit_mass=sum(primitive(shape)[0]*7850. for shape in ss)
  b=body(name,pos,ss,bit_mass);b['quat']=axis_quat([1,0,0],roll).tolist();return b
 old=chisel('used_point_chisel',(root+[D.STEM_INSERTION,0,0]).tolist(),False,0.)
 new=chisel('replacement_flat_chisel',[.37,.30,D.TABLE+.025],True,math.pi/4)
 def tray(name,pos,supports=False):
  ss=[box([0,0,0],[.240,.080,.004],[.30,.38,.43])]
  for y in (-.038,.038):ss.append(box([0,y,.010],[.240,.004,.020],[.30,.38,.43]))
  for x in (-.118,.118):ss.append(box([x,0,.010],[.004,.072,.020],[.30,.38,.43]))
  if supports:
   # Original V cradles contact the12mm main stem, away from the grip.
   for x in (-.065,.020):
    z=.025-.002-.006*math.sqrt(2)
    for sign in (-1,1):ss.append(convex([[x+dx,y,z0] for dx in (-.006,.006) for y,z0 in [(0,0),(sign*.020,0),(sign*.020,z+.020),(0,z)]],[.48,.50,.52],'V_support'))
  return body(name,pos,ss,.450,True)
 oldtray=tray('used_chisel_tray',D.OLD_TRAY)
 newtray=tray('replacement_cradle',D.NEW_CRADLE,True)
 spec=dict(schema=1,task='sds-plus-chisel-exchange',geometry_mode=D.MODE.value,instruction='Replace the used point chisel with the flat chisel. Put the used chisel in its tray, secure the replacement in the unpowered holder, and leave both hands clear.',control_hz=20,physics_dt=1/1920,gravity=[0,0,-9.81],run_limit=3200,table_top=D.TABLE,hold_seconds=2.,penetration_limit=.00020,
 assemblies=[dict(name='sds_holder_asset',origin=D.ROOT,fixed=True,bodies=[holder,collar],joints=[j]),assembly(ball),assembly(old),assembly(new),assembly(oldtray,True),assembly(newtray,True)],initial_joint_values={'sleeve_retraction':0.},collision_exclusions=[],
 material=dict(static_friction=.65,dynamic_friction=.45,restitution=0.,contact_offset=.00002,rest_offset=0.),
 materials=dict(inspection_lubricated=dict(static_friction=.18,dynamic_friction=.12,restitution=0.,classification='Authored clear glass/polycarbonate inspection inserts; lightly lubricated0.12 assumption, not OEM hardware.'),lubricated=dict(static_friction=.18,dynamic_friction=.12,restitution=0.,classification='Benchmark-authored lightly greased steel interface assumption; manufacturer prescribes clean/lightly grease, not measured coefficient.')),
 parameters=dict(ball_diameter_manufacturer=D.BALL_DIAMETER,holder_mouth=D.ROOT,ball_port_x=D.BALL_X,shank_radius=D.SHAFT_RADIUS,closed_slot_rear=D.SLOT_REAR,closed_slot_front=D.SLOT_FRONT,closed_slot_floor_radius=D.SLOT_RADIUS,open_groove_floor_radius=D.OPEN_GROOVE_RADIUS,authored_closed_ball_radial_limit=D.COLLAR_BORE_CLOSED-D.BALL_RADIUS,authored_free_axial_play=True,authored_ball_race_x_min=.0194,authored_ball_race_x_max=.0251,authored_locked_ball_x_max=.0210,authored_gravity_return_lip_slope=.10,authored_clamped_inert_workholding=True),
 limitations=['Original authored benchmark fixture; not OEM dimensional compatibility or measured hardware. Only7mm retaining-ball diameter is manufacturer documented.','Groove profiles, gravity-biased axial ball race and sleeve locking land are engineered approximations preserving separate torque drive, radial ball retention, free axial play, automatic insertion and independent sleeve release.','Exact7mm sphere in both USD and supplemental CPU physics. No drilling, cutting, powered rotation, hammer action, grease flow or real dust seal is simulated.'])
 return spec

if __name__=='__main__':
 s=make_scene();(HERE/'scene.json').write_text(json.dumps(s,indent=2)+'\n')
 from build_assets import compile_assets
 compile_assets(s,HERE/'assets')
