"""Offline analytical and contact-geometry samples, never physics evidence."""
import copy
import hashlib
import importlib
import json
import math
from pathlib import Path
import sys
import types


def geometry_module(folder):
    name='_sac_geometry_'+hashlib.sha256(str(folder).encode()).hexdigest()[:12]
    package=types.ModuleType(name);package.__path__=[str(folder)];sys.modules[name]=package
    return importlib.import_module(name+'.geometry')


def audit(folder):
    spec=json.loads((folder/'scene.json').read_text());g=geometry_module(folder)
    initial={b['name']:dict(pos=b['pos'],quat=b['quat']) for a in spec['assemblies'] for b in a['bodies']}
    states=[('initial',copy.deepcopy(initial))]
    s=spec['score_spec'];d=spec['parameters'];seated=copy.deepcopy(initial)
    seated['carrier']['pos']=[.24,0.,s['carrier_seat_z']]
    states.append(('carrier_seated',copy.deepcopy(seated)))
    for turns in (0.,.125,.5,1.,2.,3.,4.):
        f=copy.deepcopy(seated)
        for i,n in enumerate(s['retainers']):
            a=-2*math.pi*turns;st=s['studs'][i]
            f[n]=dict(pos=[*st['axis_xy'],st['tip_z']+d['retainer_height']/2-turns*s['pitch']],quat=[0,0,math.sin(a/2),math.cos(a/2)])
        states.append(('thread_turns_'+str(turns),f))
    checks=[]
    for label,state in states:
        penetration=g.maximum_penetration(spec,state)
        checks.append(dict(label=label,max_penetration_m=float(penetration),passed=bool(penetration<=spec['penetration_limit'])))
    result=dict(kind='OFFLINE_NOMINAL_GEOMETRY',physics_executed=False,checks=checks,passed=all(x['passed'] for x in checks))
    print(json.dumps(result,indent=2));return 0 if result['passed'] else 1


if __name__=='__main__':raise SystemExit(audit(Path(__file__).resolve().parent))
