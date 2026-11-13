"""Self-contained CPU checks; never starts Isaac, CUDA, Dream or network services."""
import argparse,hashlib,json,os,subprocess,sys,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent
AUDITS=('provenance.py','verify_assets.py','audit_gearing.py','probe_gearing_cpu.py','probe_pawl_cpu.py','mechanism_cpu.py','cpu_native_cases.py','audit_control.py','audit_geometry.py','audit_robot.py','audit_sequence.py','audit_path.py')


def integrity():
 manifest=json.loads((HERE/'source_manifest.json').read_text())
 actual={p.relative_to(HERE).as_posix():hashlib.sha256(p.read_bytes().replace(b'\r\n',b'\n')).hexdigest()
         for p in HERE.rglob('*') if p.is_file() and p.name!='source_manifest.json' and 'offline-evidence' not in p.parts and
         '__pycache__' not in p.parts and '.pytest_cache' not in p.parts and p.suffix!='.pyc'}
 if actual!=manifest['files']:raise ValueError('Source changed; review intentional edits before refreshing manifest')


def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path);args=parser.parse_args()
 integrity()
 if args.output is None:args.output=Path(tempfile.mkdtemp(prefix='cargo-offline-'))
 else:args.output.mkdir(parents=True,exist_ok=False)
 env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
 rows=[];commands=[('pytest',[sys.executable,'-m','pytest','-q',str(HERE)])]+[(name,[sys.executable,str(HERE/name)]) for name in AUDITS]
 for name,cmd in commands:
  result=subprocess.run(cmd,cwd=HERE.parents[1],env=env,text=True,capture_output=True)
  path=args.output/(name+'.log');path.write_text(result.stdout+result.stderr)
  row=dict(check=name,returncode=result.returncode,passed=result.returncode==0,log=path.name)
  rows.append(row);print(json.dumps(row),flush=True)
 report=dict(kind='OFFLINE_CPU_ONLY_PACKAGE_CHECKS',physics_engine='Supplemental MuJoCo only for named probes; no Isaac',native_executed=False,checks=rows,passed=all(r['passed'] for r in rows))
 (args.output/'summary.json').write_text(json.dumps(report,indent=2)+'\n')
 return 0 if report['passed'] else 1
if __name__=='__main__':raise SystemExit(main())
