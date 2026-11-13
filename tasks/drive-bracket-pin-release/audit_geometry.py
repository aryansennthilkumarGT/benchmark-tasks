"""Nominal inter-part geometry, including retaining-pin negative controls."""
import copy,hashlib,importlib,json,sys,types
from pathlib import Path


def geometry_module(folder):
    name='_drive_geometry_'+hashlib.sha256(str(folder).encode()).hexdigest()[:12]
    package=types.ModuleType(name);package.__path__=[str(folder)];sys.modules[name]=package
    return importlib.import_module(name+'.geometry')


def audit(folder):
    spec=json.loads((folder/'scene.json').read_text());plan=json.loads((folder/'controller.json').read_text());g=geometry_module(folder)
    checks=[]
    for i,p in enumerate(plan['phases']):
        depth=float(g.maximum_penetration(spec,p['nominal_bodies']))
        checks.append(dict(phase=i,label=p['label'],max_penetration_m=depth,passed=depth<=spec['penetration_limit']))
    result=dict(kind='OFFLINE_NOMINAL_GEOMETRY',physics_executed=False,checks=checks,passed=all(x['passed'] for x in checks))
    print(json.dumps(result,indent=2));return 0 if result['passed'] else 1
if __name__=='__main__':raise SystemExit(audit(Path(__file__).resolve().parent))
