from pathlib import Path
import subprocess,json,hashlib,struct,re,datetime
base=Path(__file__).parent
spec={
 'openflexure-source':['README.md','docs/0_printing.md','docs/0_bill_of_materials.md','docs/1_actuator_assembly.md','docs/2a_basic_optics_module.md','docs/2b_high_resolution_optics_module.md','docs/3_illumination.md','docs/4_clips_and_wiring.md','docs/5_motors.md','docs/parts/fixings/viton_o_ring_30mm_inner_diameter_2mm_cross_section.md','docs/parts/electronics/raspberry_pi_camera.md','openscad/actuator_assembly_tools.scad','openscad/compact_nut_seat.scad','openscad/feet.scad','openscad/main_body.scad','openscad/microscope_parameters.scad','openscad/cameras/picamera_2.scad','openscad/cameras/picamera_2_gripper.scad','openscad/cameras/picamera_2_lens_gripper.scad','builds/actuator_assembly_tools.stl','builds/main_body_LS65-M.stl','builds/feet.stl','builds/gears.stl','builds/picamera_2_gripper.stl','builds/picamera_2_lens_gripper.stl','builds/optics_picamera_2_rms_f50d13_LS65.stl','builds/lens_tool.stl','docs/images/band_insertion_body_1.jpg','docs/images/band_insertion_body_2.jpg','docs/images/band_insertion_finished_bottom.jpg','docs/images/picam2_lens_removal.jpg'],
 'opentrons-source':['README.md','LICENSE','docs/flex/docs/installation/instruments.md','docs/flex/docs/installation/unboxing.md','docs/flex/docs/system-description/gripper.md','docs/flex/docs/system-description/pipettes.md','docs/flex/docs/system-description/robot.md','docs/flex/docs/system-description/e-stop.md','docs/flex/docs/maintenance/cleaning.md','docs/flex/docs/maintenance/service.md','docs/flex/docs/modules/caddy.md','docs/stacker/docs/installation.md','docs/flex/docs/images/o-ring-removal-tool.png','docs/flex/docs/images/o-ring-attachment-tool.png','docs/flex/docs/images/gripper-components.png'],
 'gello-mechanical':['README.md','LICENSE','franka_fr3/README.md','ar4/README.md','gripper/handle.STL','gripper/trigger.STL','franka_fr3/20_TRIGGER_BODY.STL','franka_fr3/21_TRIGGER_FINGER.STL','franka_fr3/LICENSE'],
 'gello-source':['README.md'],
 'robotis-manual':['docs/en/platform/openmanipulator_x/assembly.md','docs/en/platform/openmanipulator_x/overview.md','docs/en/platform/openmanipulator_x/specification.md'],
 'openmanipulator-source':['README.md','LICENSE','open_manipulator_description/urdf/open_manipulator_x/open_manipulator_x_arm.urdf.xacro','open_manipulator_description/meshes/open_manipulator_x/gripper_left_palm.stl','open_manipulator_description/meshes/open_manipulator_x/gripper_right_palm.stl'],
 'umi-source':['README.md'],
 'umi-site':['index.html']}
manifest=[];geo=[]
for repo,paths in spec.items():
 rp=base/repo; sha=subprocess.check_output(['git','-C',str(rp),'rev-parse','HEAD'],text=True).strip();remote=subprocess.check_output(['git','-C',str(rp),'remote','get-url','origin'],text=True).strip().removesuffix('.git');owner='/'.join(remote.split('/')[-2:])
 for p in paths:
  try:b=subprocess.check_output(['git','-C',str(rp),'show',sha+':'+p],stderr=subprocess.DEVNULL)
  except subprocess.CalledProcessError:manifest.append({'repo':remote,'commit':sha,'source_path':p,'error':'not present at pin'});continue
  dst=base/'sources'/repo/p;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(b)
  manifest.append({'repo':remote,'commit':sha,'source_path':p,'url':f'https://raw.githubusercontent.com/{owner}/{sha}/{p}','local':str(dst),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)})
  if p.lower().endswith('.stl'):
   if len(b)>=84 and 84+50*struct.unpack('<I',b[80:84])[0]==len(b):
    pts=[];n=struct.unpack('<I',b[80:84])[0]
    for i in range(n):
     v=struct.unpack('<12fH',b[84+i*50:134+i*50]);pts.extend([v[3:6],v[6:9],v[9:12]])
   else:
    pts=[tuple(map(float,m)) for m in re.findall(rb'vertex\s+([-\d.eE+]+)\s+([-\d.eE+]+)\s+([-\d.eE+]+)',b)];n=len(pts)//3
   if pts:
    lo=[min(q[i] for q in pts) for i in range(3)];hi=[max(q[i] for q in pts) for i in range(3)];geo.append({'repo':repo,'source_path':p,'commit':sha,'triangles':n,'units':'mm per source SCAD/URDF scale for OpenFlexure/ROBOTIS; GELLO STL units inferred mm, not separately certified','bbox_min':lo,'bbox_max':hi,'bbox_extent':[hi[i]-lo[i] for i in range(3)],'limitation':'Bounding extent only; no grasp, clearance, watertightness or contact test'})
(base/'source-manifest.json').write_text(json.dumps(manifest,indent=2));(base/'geometry-inspection.json').write_text(json.dumps(geo,indent=2));print(json.dumps(geo,indent=2))
