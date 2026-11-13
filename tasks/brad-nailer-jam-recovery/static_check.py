"""Reusable complete affected CPU checks; no GPU, service, network or paid calls."""
import argparse,hashlib,json,os,subprocess,sys,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent

def integrity():
 manifest=json.loads((HERE/'source_manifest.json').read_text())
 actual={p.relative_to(HERE).as_posix():hashlib.sha256(p.read_bytes().replace(b'\r\n',b'\n')).hexdigest() for p in HERE.rglob('*') if p.is_file() and p.name not in ('source_manifest.json','MUJOCO_LOG.TXT') and 'offline-evidence' not in p.parts and '__pycache__' not in p.parts and '.pytest_cache' not in p.parts and p.suffix!='.pyc'}
 if actual!=manifest['files']:raise ValueError('Source changed; review intentional edits before refreshing manifest')

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path);a=p.parse_args();integrity()
 out=a.output.resolve() if a.output else Path(tempfile.mkdtemp(prefix='nailer-offline-'))
 if a.output:out.mkdir(parents=True,exist_ok=False)
 env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
 env.pop('ROBOCURVE_IDEAL_PROGRESS',None)
 commands=[('pytest',[sys.executable,'-m','pytest','-q',str(HERE)])]
 for name in ('provenance.py','verify_assets.py','audit_geometry.py','mechanism_cpu.py','cpu_native_cases.py','probe_cycle_cpu.py','audit_controller.py'):commands.append((name,[sys.executable,str(HERE/name)]))
 commands.append(('audit_path.py',[sys.executable,str(HERE/'audit_path.py'),str(out/'audit_controller.py.log')]))
 rows=[]
 for name,cmd in commands:
  result=subprocess.run(cmd,cwd=HERE,env=env,text=True,capture_output=True)
  (out/(name+'.log')).write_text(result.stdout);(out/(name+'.stderr.log')).write_text(result.stderr)
  row=dict(check=name,returncode=result.returncode,passed=result.returncode==0,log=name+'.log',stderr=name+'.stderr.log');rows.append(row);print(json.dumps(row),flush=True)
 report=dict(kind='CPU_ONLY_PACKAGE_CHECKS',native_isaac_executed=False,hardware_executed=False,supplemental_engine='MuJoCo3.3.7',source_manifest_sha256=hashlib.sha256((HERE/'source_manifest.json').read_bytes()).hexdigest(),checks=rows,passed=all(r['passed'] for r in rows))
 (out/'summary.json').write_text(json.dumps(report,indent=2)+'\n');return 0 if report['passed'] else 1
if __name__=='__main__':raise SystemExit(main())
