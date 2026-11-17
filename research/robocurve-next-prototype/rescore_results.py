"""Reapply the observation-only local score and separate numerical audit.
Never edits a simulated coordinate, force, parameter or equilibrium observation.
"""
from pathlib import Path
import sys,json
D=Path(__file__).resolve().parent
sys.path.insert(0,'/workspace/robocurve-cpu-deps');sys.path.insert(0,str(D/'odri'))
from scoring import physical_score,numerical_audit
for tag in ['CONTROLS','SENSITIVITY']:
 p=D/f'odri/results/{tag}.json';rows=json.loads(p.read_text())
 for row in rows:
  row['physical_score']=physical_score(row['observations'],row['ring_nodes_by_stage_mm'][-1],row['specification'])
  row['numerical_audit']=numerical_audit(row['observations'])
  row['experiment_pass']=bool(row['physical_score']['score']==1 and row['numerical_audit']['passed'])
 p.write_text(json.dumps(rows,indent=2)+'\n')
 print(tag,[(x['case'],x['modulus_MPa'],x['experiment_pass']) for x in rows])
