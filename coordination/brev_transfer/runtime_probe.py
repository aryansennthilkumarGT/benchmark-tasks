"""Read installed GPU/runtime state; no simulation, paid model or provisioning."""
import argparse,json,os,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from engine import Incomplete,read
from environment import hardware,launchable_runtime


def probe(root,stage):
    if sys.version_info[:2]!=(3,12):raise Incomplete('Pinned SDK Python must be3.12')
    observed=hardware()
    if observed['problems']:raise Incomplete('; '.join(observed['problems']))
    gpu=observed['selected_gpu']
    if 'L40S' not in gpu['name'] or gpu['driver']!='565.57.01':raise Incomplete('Expected existing L40S/565.57.01 profile; no driver changes will be attempted')
    native=stage=='diagnostic'
    runtime=launchable_runtime(root,read(Path(__file__).resolve().parents[1]/'stack-lock.json'),require_dream=not native)
    if not native and not all(observed['credentials_present'].get(k) for k in ('dream','robocurve')):raise Incomplete('Qualification needs existing secure Dream/upload credentials; never paste tokens into chat or Git')
    return {'gpu_uuid':gpu['uuid'],'gpu_name':gpu['name'],'driver':gpu['driver'],'runtime':runtime,
            'credential_availability':observed['credentials_present'],'dream_auth_required':not native,
            'native_executed':False,'driver_smoke':'REQUIRED_BY_QUALIFICATION; not claimed by this read-only probe'}
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,required=True);p.add_argument('--stage',choices=('diagnostic','qualification'),required=True);a=p.parse_args()
    try:print(json.dumps(probe(a.root,a.stage),indent=2))
    except (Incomplete,OSError,ValueError,KeyError) as exc:print(str(exc),file=sys.stderr);raise SystemExit(2)
