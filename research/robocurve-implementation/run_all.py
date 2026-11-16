"""Reproduce finite CPU experiments only. No GPU/native/model/service invocation."""
from pathlib import Path
import os,subprocess,sys
D=Path(__file__).resolve().parent
commands=[('yubi/inspect_saddle.py',[],'yubi/results/SADDLE_EXECUTION.txt'),('yubi/access_gate.py',['--variant','direct'],'yubi/results/ACCESS_DIRECT_EXECUTION.txt'),('yubi/access_gate.py',['--variant','raised-transit'],'yubi/results/ACCESS_RAISED_TRANSIT_EXECUTION.txt'),('faze4/register_profile.py',[],'faze4/results/REGISTRATION_EXECUTION.txt'),('faze4/closure_gate.py',[],'faze4/results/CLOSURE_EXECUTION.txt'),('faze4/independent_checks.py',[],'faze4/results/INDEPENDENT_EXECUTION.txt'),('toshiba/contact_coupon.py',[],'toshiba/results/CONTACT_EXECUTION.txt'),('toshiba/yam_access.py',[],'toshiba/results/YAM_EXECUTION.txt'),('verify_results.py',[],'VERIFICATION_OUTPUT.txt'),('write_result_reports.py',[],'REPORT_GENERATION_OUTPUT.txt')]
env=os.environ.copy();env['PYTHONPATH']='/workspace/robocurve-cpu-deps'+os.pathsep+env.get('PYTHONPATH','');env['MPLCONFIGDIR']='/tmp/robocurve-impl-mpl'
for file,args,log in commands:
 print('CPU',file,*args,flush=True)
 with (D/log).open('w') as out:r=subprocess.run([sys.executable,str(D/file),*args],env=env,stdout=out,stderr=subprocess.STDOUT)
 if r.returncode:raise SystemExit(f'{file}: exit{r.returncode}; inspect{log}')
print('ALL CPU REPRODUCTION COMMANDS COMPLETED; inspect limitations before interpreting PASS')
