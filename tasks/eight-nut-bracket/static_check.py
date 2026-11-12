"""Run offline package checks. No simulator or model is launched."""
import ast
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent

def main():
    for path in HERE.glob('*.py'):ast.parse(path.read_text(encoding='utf8'),filename=path.name)
    manifest=json.loads((HERE/'source_manifest.json').read_text())
    for name,expected in manifest['files'].items():
        path=(HERE/name).resolve()
        if not path.is_relative_to(HERE):raise ValueError('Source hash path escapes task')
        if hashlib.sha256(path.read_bytes().replace(b'\r\n',b'\n')).hexdigest()!=expected:
            raise ValueError('Source hash differs: '+name)
    commands=[['-m','unittest','discover','-s',str(HERE),'-p','test_*.py','-v']]
    commands += [[str(HERE/name)] for name in ['verify_assets.py','audit_control.py','audit_geometry.py','audit_grasps.py','audit_motion.py','audit_threads.py']]
    for command in commands:
        subprocess.run([sys.executable,*command],cwd=HERE,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),check=True)
    print('STATIC CHECKS PASSED; native physics and physical feasibility are not established.')
if __name__=='__main__':main()
