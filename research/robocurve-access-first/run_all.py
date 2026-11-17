"""Run offline CPU diagnostics in dependency order, preserving individual logs."""
from pathlib import Path
import os
import subprocess
import sys

D = Path(__file__).resolve().parent
R = D.parents[1]
jobs = [
    ('odri/diagnose.py', 'odri/results/ROOT_CAUSE_EXECUTION.txt'),
    ('odri/solid_witness.py', 'odri/results/SOLID_WITNESS_EXECUTION.txt'),
    ('odri/kinematic_facts.py', 'odri/results/KINEMATIC_EXECUTION.txt'),
    ('odri/support_gate.py', 'odri/results/SUPPORT_EXECUTION.txt'),
    ('odri/closure_contacts.py', 'odri/results/CLOSURE_EXECUTION.txt'),
    ('odri/one_annulus_stage_gate.py', 'odri/results/ONE_ANNULUS_EXECUTION.txt'),
    ('candidates/input_gate.py', 'candidates/results/INPUT_GATE_EXECUTION.txt'),
    ('candidates/opentrons_access.py', 'candidates/results/OPENTRONS_EXECUTION.txt'),
    ('write_reports.py', 'REPORT_OUTPUT.txt'),
    ('verify_results.py', 'VERIFICATION.txt'),
]
env = dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1')
for script, logfile in jobs:
    print(f'RUN {script}', flush=True)
    with (D / logfile).open('w') as output:
        subprocess.run([sys.executable, str(D / script)], cwd=R, env=env,
                       stdout=output, check=True)
print('All CPU diagnostics completed. No physics, purchase or complete-path claim.')
