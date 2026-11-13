"""Sample original gear flank geometry; not torque/contact-dynamics evidence."""
import hashlib,importlib,json,math,sys,types
from pathlib import Path
from gearing import pinion,rack,RADIUS,PITCH
from primitives import body,quat


def geometry_module(folder):
 name='_gear_audit_'+hashlib.sha256(str(folder).encode()).hexdigest()[:12]
 p=types.ModuleType(name);p.__path__=[str(folder)];sys.modules[name]=p
 return importlib.import_module(name+'.geometry')


def audit(folder):
 g=geometry_module(folder)
 a=body('pinion',[0,.04,0],pinion(),.04)
 b=body('rack',[0,0,0],rack(pitch_plane=RADIUS+.00005,phase=PITCH/2),.12)
 s=dict(assemblies=[dict(bodies=[a,b],joints=[])],collision_exclusions=[])
 checks=[]
 for i in range(41):
  angle=-math.pi*i/40;advance=-angle*RADIUS
  states=dict(pinion=dict(pos=a['pos'],quat=quat([1,0,0],angle)),rack=dict(pos=[0,advance,0],quat=[0,0,0,1]))
  depth=float(g.maximum_penetration(s,states))
  checks.append(dict(angle_rad=angle,rack_advance_m=advance,penetration_m=depth,passed=depth<=.00015))
 result=dict(kind='OFFLINE_AUTHORED_INVOLUTE_FLANK_SAMPLES',physics_executed=False,collision_pairs_excluded=False,
             pitch_m=PITCH,pitch_radius_m=RADIUS,checks=checks,passed=all(x['passed'] for x in checks))
 print(json.dumps(result,indent=2));return 0 if result['passed'] else 1
if __name__=='__main__':raise SystemExit(audit(Path(__file__).resolve().parent))
