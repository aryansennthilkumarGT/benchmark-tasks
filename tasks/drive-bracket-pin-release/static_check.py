"""Exact-source checks and actual CPU tests; never starts Isaac or Dream."""
import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

HERE=Path(__file__).resolve().parent


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.parse_args()
    for p in HERE.glob('*.py'):ast.parse(p.read_text(),filename=str(p))
    hashes=json.loads((HERE/'source_manifest.json').read_text())['files']
    assert hashes,'Source manifest empty'
    for name,expected in hashes.items():
        p=(HERE/name).resolve()
        assert p.is_relative_to(HERE)
        assert hashlib.sha256(p.read_bytes().replace(b'\r\n',b'\n')).hexdigest()==expected,name
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
    subprocess.run([sys.executable,'-m','pytest','-q','-p','no:cacheprovider',str(HERE)],check=True,env=env)
    scripts=['verify_assets.py','audit_control.py','audit_geometry.py','audit_sequence.py','audit_robot.py','audit_kinematic_release.py']
    for script in scripts:subprocess.run([sys.executable,str(HERE/script)],check=True,env=env)
    print('OFFLINE CHECKS PASSED; no native physics or full-score expert evidence.')


if __name__=='__main__':main()
