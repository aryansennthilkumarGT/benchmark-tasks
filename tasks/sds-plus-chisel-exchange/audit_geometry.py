"""Unfiltered solid QA; no native or robot feasibility claim."""
import copy,hashlib,importlib,json,sys,types
from pathlib import Path


def geometry_module(folder):
 name='_sds_geometry_'+hashlib.sha256(str(folder).encode()).hexdigest()[:12]
 package=types.ModuleType(name);package.__path__=[str(folder)];sys.modules[name]=package
 return importlib.import_module(name+'.geometry')


def initial(folder):
 s=json.loads((folder/'scene.json').read_text());poses={b['name']:dict(pos=b['pos'],quat=b['quat']) for a in s['assemblies'] for b in a['bodies']}
 inspection=copy.deepcopy(s)
 for a in inspection['assemblies']:
  for b in a['bodies']:b['anchor']=False  # QA must inspect fixed/fixed pairs too.
 value=float(geometry_module(folder).maximum_penetration(inspection,poses))
 return dict(kind='OFFLINE_INITIAL_ALL_PAIR_SOLID_AUDIT',physics_executed=False,adjacency_filtered=False,fixed_pairs_skipped=False,penetration_m=value,passed=value<=.00005)

if __name__=='__main__':
 r=initial(Path(__file__).resolve().parent);print(json.dumps(r,indent=2));raise SystemExit(0 if r['passed'] else 1)
