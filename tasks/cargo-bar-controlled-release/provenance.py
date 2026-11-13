"""Explicit inherited provenance for every numeric scene value, no measured claims.

JSON pointers use longest-prefix inheritance. Values remain fully specified in
scene.json; its hash prevents provenance silently following geometry changes.
"""
import hashlib,json,math
from pathlib import Path
HERE=Path(__file__).resolve().parent
CATEGORIES={'MANUFACTURER_DOCUMENTED','INDEPENDENTLY_MEASURED','BENCHMARK_AUTHORED','DERIVED'}


def numeric_paths(value,pointer=''):
 if isinstance(value,bool):return
 if isinstance(value,(float,int)):
  if not math.isfinite(value):raise ValueError('Nonfinite scene value')
  yield pointer
 elif isinstance(value,list):
  for i,item in enumerate(value):yield from numeric_paths(item,pointer+'/'+str(i))
 elif isinstance(value,dict):
  for name,item in value.items():yield from numeric_paths(item,pointer+'/'+name)


def validate(folder=HERE):
 spec=json.loads((folder/'scene.json').read_text());p=json.loads((folder/'parameter-provenance.json').read_text())
 if p['scene_sha256']!=hashlib.sha256((folder/'scene.json').read_bytes()).hexdigest():raise ValueError('Provenance source mismatch')
 entries=p['entries'];paths=list(numeric_paths(spec));counts={k:0 for k in CATEGORIES}
 for e in entries:
  if e['category'] not in CATEGORIES or not e.get('basis'):raise ValueError('Unjustified provenance')
  if e['category']=='MANUFACTURER_DOCUMENTED' and not (e.get('source_url') and e.get('source_sha256') and e.get('quote')):raise ValueError('Manufacturer evidence missing')
  if e['category']=='INDEPENDENTLY_MEASURED':
   evidence=e.get('measurement_evidence')
   if not evidence:raise ValueError('Genuine measurement evidence required')
   source=(folder/evidence['path']).resolve()
   if not source.is_relative_to(folder.resolve()) or not source.is_file():raise ValueError('Measurement evidence unavailable')
   if hashlib.sha256(source.read_bytes()).hexdigest()!=evidence['sha256']:raise ValueError('Measurement evidence changed')
  if e['category']=='DERIVED' and not e.get('derivation'):raise ValueError('Derivation missing')
 for path in paths:
  matches=[e for e in entries if path==e['pointer'] or path.startswith(e['pointer']+'/') or e['pointer']=='']
  if not matches:raise ValueError('Unclassified numeric field: '+path)
  entry=max(matches,key=lambda e:len(e['pointer']));counts[entry['category']]+=1
 if len({e['pointer'] for e in entries})!=len(entries):raise ValueError('Ambiguous provenance')
 return dict(kind='OFFLINE_PARAMETER_PROVENANCE',physics_executed=False,numeric_values=len(paths),counts=counts,passed=True)

if __name__=='__main__':print(json.dumps(validate(),indent=2))
