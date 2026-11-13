"""Strict value/path/class validation; authored mode never creates measured claims."""
import json
from pathlib import Path
from document_parameters import numbers,CLASSES
import dimensions as D
HERE=Path(__file__).resolve().parent

def validate(folder=HERE):
 D.validate();s=json.loads((folder/'scene.json').read_text());p=json.loads((folder/'parameter-provenance.json').read_text());actual=dict(numbers(s));rows=p['records'];assert len(rows)==len({r['path'] for r in rows})
 assert {r['path']:r['value'] for r in rows}==actual
 assert p['geometry_mode']==s['geometry_mode']==D.MODE.value
 for r in rows:
  if r['classification'] not in CLASSES or not r['source']:raise ValueError('Missing provenance')
  if r['classification']=='Independently measured, with genuine measurement evidence':raise ValueError('No genuine measurement records supplied for this authored fixture')
  if r['classification']=='Manufacturer-documented' and r['path']!='/parameters/ball_diameter_manufacturer':raise ValueError('Unsupported manufacturer dimension claim')
 return dict(kind='COMPLETE_EXPLICIT_PARAMETER_PROVENANCE',passed=True,numeric_values=len(rows),manufacturer_documented_values=1,measured_values=0)
if __name__=='__main__':print(json.dumps(validate(),indent=2))
