"""Reusable isolated CPU-only setup; never installs Isaac or starts a service."""
import argparse
from pathlib import Path
import subprocess
import sys
import venv

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--venv',type=Path,required=True);a=p.parse_args()
    if sys.version_info[:2]!=(3,12):raise SystemExit('Use Python 3.12, the tested interpreter')
    venv.EnvBuilder(with_pip=True).create(a.venv)
    python=a.venv.resolve()/'bin/python'
    subprocess.run([str(python),'-m','pip','install','torch==2.7.1+cpu','--index-url','https://download.pytorch.org/whl/cpu'],check=True)
    subprocess.run([str(python),'-m','pip','install','-r',str(Path(__file__).with_name('requirements-cpu.txt'))],check=True)
    subprocess.run([str(python),'-m','pip','check'],check=True)
    print('CPU tools ready; run static_check.py. No native physics qualification performed.')
