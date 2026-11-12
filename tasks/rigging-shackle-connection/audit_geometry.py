"""Nominal geometry audits only. No actor is created or moved in a simulator."""
import copy
import hashlib
import importlib
import json
from pathlib import Path
import sys
import types


def geometry_module(folder):
    name='_shackle_geometry_'+hashlib.sha256(str(folder).encode()).hexdigest()[:12]
    package=types.ModuleType(name);package.__path__=[str(folder)];sys.modules[name]=package
    return importlib.import_module(name+'.geometry')


def audit(folder):
    spec=json.loads((folder/'scene.json').read_text())
    g=geometry_module(folder)
    initial={b['name']:copy.deepcopy(b) for a in spec['assemblies'] for b in a['bodies']}
    states=[('initial',copy.deepcopy(initial))]
    for label,z in [('entry',.0295+6*.00254),('seated',.0295)]:
        f=copy.deepcopy(initial);f['shackle']['pos']=[.22,0,.788]
        f['pin']['pos']=[.22,0,.788+z]
        states.append((label,f))
    checks=[]
    for label,state in states:
        penetration=g.maximum_penetration(spec,state)
        checks.append(dict(label=label,max_penetration_m=float(penetration),passed=penetration<=spec['penetration_limit']))
    result=dict(kind='OFFLINE_NOMINAL_GEOMETRY',physics_executed=False,checks=checks,
                passed=all(x['passed'] for x in checks))
    print(json.dumps(result,indent=2));return 0 if result['passed'] else 1


if __name__=='__main__':raise SystemExit(audit(Path(__file__).resolve().parent))
