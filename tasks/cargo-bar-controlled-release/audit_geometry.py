"""Original articulated endpoint and CPU-reference geometry, not native physics."""
import hashlib,importlib,json,sys,types
from pathlib import Path


def geometry_module(folder):
 name='_cargo_geometry_'+hashlib.sha256(str(folder).encode()).hexdigest()[:12]
 package=types.ModuleType(name);package.__path__=[str(folder)];sys.modules[name]=package
 return importlib.import_module(name+'.geometry')


def audit(folder):
 s=json.loads((folder/'scene.json').read_text());p=json.loads((folder/'controller.json').read_text());g=geometry_module(folder);rows=[]
 for i,phase in enumerate(p['phases']):
  depth=float(g.maximum_penetration(s,phase['nominal_bodies']))
  rows.append(dict(phase=i,label=phase['label'],penetration_m=depth,passed=depth<=s['penetration_limit']))
 report=dict(kind='OFFLINE_ARTICULATED_NOMINAL_GEOMETRY',physics_executed=False,checks=rows,passed=all(r['passed'] for r in rows))
 print(json.dumps(report,indent=2));return 0 if report['passed'] else 1
if __name__=='__main__':raise SystemExit(audit(Path(__file__).resolve().parent))
