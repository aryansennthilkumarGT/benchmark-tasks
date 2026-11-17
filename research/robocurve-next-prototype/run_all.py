"""Offline CPU reproduction; all source inputs are committed here or at the base."""
from pathlib import Path
import os,subprocess,sys
D=Path(__file__).resolve().parent
env=os.environ.copy();env.update(PYTHONPATH='/workspace/robocurve-cpu-deps'+os.pathsep+env.get('PYTHONPATH',''),MPLCONFIGDIR='/tmp/robocurve-next-mpl',OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1')
commands=[('cello/inspect_source.py',[],'cello/results/INSPECTION_EXECUTION.txt'),
 ('cello/load_gate.py',[],'cello/results/LOAD_EXECUTION.txt'),
 ('chefman/inspect_mesh.py',[],'chefman/results/MESH_EXECUTION.txt'),
 ('odri/inspect_source.py',[],'odri/results/INSPECTION_EXECUTION.txt'),
 ('odri/sections.py',[],'odri/results/SECTIONS_EXECUTION.txt'),
 ('odri/source_audit.py',[],'odri/results/SOURCE_AUDIT_EXECUTION.txt'),
 ('odri/mechanism_tests.py',[],'odri/results/CONTROLS_EXECUTION.txt'),
 ('odri/mechanism_tests.py',['--mode','sensitivity'],'odri/results/SENSITIVITY_EXECUTION.txt'),
 ('odri/yam_access.py',[],'odri/results/YAM_EXECUTION.txt'),
 ('rescore_results.py',[],'RESCORE_OUTPUT.txt'),('odri/pose_audit.py',[],'odri/results/POSE_AUDIT_EXECUTION.txt'),('verify_results.py',[],'VERIFICATION_OUTPUT.txt'),
 ('write_reports.py',[],'REPORT_OUTPUT.txt')]
for file,args,log in commands:
 print('CPU',file,*args,flush=True)
 with (D/log).open('w') as stream:result=subprocess.run([sys.executable,str(D/file),*args],env=env,stdout=stream,stderr=None)
 if result.returncode:raise SystemExit(f'{file} failed with exit {result.returncode}; inspect {log}')
print('CPU commands completed. Read limitations before interpreting any local PASS.')
