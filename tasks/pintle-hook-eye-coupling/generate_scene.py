"""Original full-size bench pintle/eye fixture, not OEM hardware or vehicle CAD."""
import json,math
from pathlib import Path
import numpy as np
import dimensions as D
from primitives import body,box,cylinder,quat,assembly
from cad import convex
from mass_properties import primitive
from motion import rotate,multiply
from kinematics import reconstruct
HERE=Path(__file__).resolve().parent
STEEL=[.45,.48,.51];BLUE=[.15,.34,.58];ORANGE=[.86,.43,.12]

def tagged(shapes,density=7850.):
 for s in shapes:s['mass_density']=density
 return shapes

def member(name,pos,shapes,fixed=False,mass=None):
 tagged(shapes)
 if mass is None:mass=sum(primitive(s)[0]*s['mass_density'] for s in shapes)
 return body(name,pos,shapes,mass,fixed)

def profile(points,y0,y1,color=STEEL):return convex([[x,y,z] for x,z in points for y in [y0,y1]],color)

def torus(major,minor,count=64,sides=16):
 result=[]
 for i in range(count):
  points=[]
  for a in [2*math.pi*i/count,2*math.pi*(i+1)/count]:
   for j in range(sides):
    t=2*math.pi*j/sides;r=major+minor*math.cos(t);points.append([r*math.cos(a),r*math.sin(a),minor*math.sin(t)])
  result.append(convex(points,ORANGE,'forged_eye_replica'))
 return result

def joint(name,parent,child,pivot,lo,hi,k=0.,damping=.002):
 return dict(name=name,kind='revolute',parent=parent,child=child,pivot_parent=pivot,pivot_child=[0,0,0],axis='Y',lower=lo,upper=hi,stiffness=k,damping=damping,rest=0.,initial=D.INITIAL[name],collision_enabled=True)

def make_scene():
 D.validate_mode()
 # Permanently mounted hook, actual full-size compatible eye. Bench pedestal is
 # not a toy trailer: no claim of vehicle motion, tongue lifting or roadworthiness.
 basez=D.TABLE-D.ROOT[2]
 root_shapes=[box([.025,0,basez+.005],[.22,.21,.010],BLUE),box([-.016,0,(basez+.010+.13)/2],[.018,D.MOUNT_WIDTH,.13-basez-.010],BLUE)]
 # U-shaped load path: back web, under-seat beam and upright horn. Shared faces
 # avoid same-body overlap in these structural members.
 root_shapes += [box([.0525,0.,-.0025],[.105,.038,.025]),box([.1125,0.,.041],[.015,.034,.102])]
 # Real bridge from mounting plate to hinge, two outside cheeks and axle.
 root_shapes += [box([.004,0.,.0545],[.008,.040,.089])]
 for y in [-.027,.027]:root_shapes.append(box([.015,y,.110],[.022,.010,.022]))
 root_shapes.append(cylinder(D.LATCH_PIVOT,.003,.062,STEEL,quat([1,0,0],math.pi/2)))
 # Original positive lock ledge. Hidden OEM dog/cam dimensions are unavailable;
 # this declared replica requires the same lifted handle/closed flush indication.
 root_shapes.append(box([.018,0.,.1181],[.014,.019,.004],ORANGE))
 # Bolt-head centers preserve the documented mounting spacing, already secured.
 for y in [-D.BOLT_SPAN_Y/2,D.BOLT_SPAN_Y/2]:
  for z in [.020,.020+D.BOLT_SPAN_Z]:root_shapes.append(cylinder([-.004,y,z],D.BOLT_DIAMETER*.8,.006,STEEL,quat([0,1,0],math.pi/2)))
 root=member('hook_body',D.ROOT,root_shapes,True,mass=4.)
 # Hinged upper jaw closes the loop above the horn; exact front gap .5mm.
 latch_shapes=[box([.049,0.,0.],[.114,.042,.014],BLUE),box([.094,0.,-.012],[.020,.034,.010],BLUE)]
 # Hollow boss surrounds the real fixed axle, rather than overlapping it.
 from cad import annular_slice
 for y0,y1 in [(-.021,-.013),(.013,.021)]:
  for s in annular_slice(y0,y1,.0032,.0032,.009,count=32,color=BLUE):
   # annular_slice axisX -> localY, radialY -> localX, radialZ ->localZ.
   s['pos']=[s['pos'][1],s['pos'][0],s['pos'][2]];s['vertices']=[[v[1],v[0],v[2]] for v in s['vertices']]
   # Axis swap reflects handedness: reverse each triangle for positive integration.
   s['faces']=[list(reversed(f)) for f in s['faces']];s['size']=[s['size'][1],s['size'][0],s['size'][2]];latch_shapes.append(s)
 # Remove center spine behind hinge where it would overlap its shaft.
 latch_shapes[0]=box([.069,0.,0.],[.074,.042,.014],BLUE)
 for y in [-.016,.016]:latch_shapes.append(box([.0175,y,0.],[.029,.010,.014],BLUE))
 # Independent handle pivot axle on the jaw, with hand access at the top.
 latch_shapes += [cylinder(D.LOCK_PIVOT,.0015,.034,STEEL,quat([1,0,0],math.pi/2))]
 for y in [-.016,.016]:latch_shapes.append(box([.015,y,.0095],[.008,.004,.010],BLUE))
 latch=member('upper_latch',D.ROOT,latch_shapes)
 # Flush lever forward of its pivot, rear dog below it. The spring is authored;
 # .14Nm/rad yields .091Nm at .65rad, not an OEM torque claim.
 handle_shapes=[box([.023,0.,.002],[.043,.020,.004],ORANGE),box([-.005,0.,-.017],[.006,.012,.022],ORANGE)]
 # Rear dog top at .114, below ledge .117; lifting the front rotates dog forward.
 for y0,y1 in [(-.012,-.009),(.009,.012)]:
  from cad import annular_slice
  for s in annular_slice(y0,y1,.0017,.0017,.003,count=24,color=ORANGE):
   s['pos']=[s['pos'][1],s['pos'][0],s['pos'][2]];s['vertices']=[[v[1],v[0],v[2]] for v in s['vertices']];s['faces']=[list(reversed(f)) for f in s['faces']];s['size']=[s['size'][1],s['size'][0],s['size'][2]];handle_shapes.append(s)
 handle=member('lock_handle',D.ROOT,handle_shapes)
 joints=[joint('latch_rotation','hook_body','upper_latch',D.LATCH_PIVOT,-1.7,0.,damping=.008),joint('lock_rotation','upper_latch','lock_handle',D.LOCK_PIVOT,-.75,0.,D.LOCK_SPRING,D.LOCK_DAMPING)]
 # Original one-piece eye, real toroidal wire section, no fictitious slide joint.
 # Short tangential fixture stem lies beyond the ring, enabling stock jaws; it
 # represents the unladen supported eye attachment, not a miniaturized trailer.
 eye_shapes=torus(D.EYE_MAJOR,D.EYE_MINOR,D.EYE_FACETS,D.BAR_FACETS)
 eye_shapes += [box([.095,0.,0.],[.064,.022,.022],ORANGE)]
 eye=member('drawbar_eye',D.EYE_START,eye_shapes)
 # Initial stool supports the ring at three actual contact patches. It does not
 # follow it, latch it, carry a hidden spring or touch the stem grip site.
 stool_shapes=[box([0,0,0.],[.15,.15,.006],BLUE)]
 top=D.EYE_START[2]-D.TABLE-.006-D.EYE_MINOR
 for x,y in [(-.045,0.),(.020,.040),(.020,-.040)]:stool_shapes.append(box([x,y,.003+top/2],[.012,.012,top],BLUE))
 stool=member('eye_start_stool',[D.EYE_START[0],D.EYE_START[1],D.TABLE+.003],stool_shapes,True,mass=.5)
 spec=dict(slug='pintle-hook-eye-coupling',title='Couple a full-size drawbar eye and secure the pintle latch',instruction='Fit the supported unloaded drawbar eye onto the horn and close the pintle latch with its lock handle flush. Leave both hands clear.',geometry_mode=D.MODE,control_hz=20,physics_dt=1/1920,gravity=[0,0,-9.81],run_limit=4000,table_top=D.TABLE,hold_seconds=2.,penetration_limit=.00020,assemblies=[dict(name='pintle_hook_asset',origin=D.ROOT,fixed=True,bodies=[root,latch,handle],joints=joints),assembly(eye),assembly(stool,True)],initial_joint_values=D.INITIAL.copy(),collision_exclusions=[],material=dict(static_friction=.65,dynamic_friction=.50,restitution=0.,contact_offset=.00002,rest_offset=0.),materials={},parameters=dict(eye_inner_diameter=D.EYE_ID,eye_bar_diameter=D.EYE_BAR,eye_major_radius=D.EYE_MAJOR,eye_minor_radius=D.EYE_MINOR,eye_goal_local=D.EYE_SEAT,horn_x=D.HORN_X,horn_top=D.HORN_TOP,horn_width=D.HORN_WIDTH,replica_lock_dog=True,manufacturer_inner_lock_geometry=False,vehicle_motion_excluded=True))
 poses=reconstruct(spec,root,D.INITIAL)
 for b in spec['assemblies'][0]['bodies']:b.update(poses[b['name']])
 return spec

if __name__=='__main__':
 spec=make_scene();(HERE/'scene.json').write_text(json.dumps(spec,indent=2)+'\n');from build_assets import compile_assets;compile_assets(spec,HERE/'assets')
