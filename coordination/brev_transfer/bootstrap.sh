#!/usr/bin/env bash
set -euo pipefail
ops_ref=''
dry_run=0
refresh_from=''
while (($#)); do
  case "$1" in
    --ops-ref) ops_ref="${2:?Missing exact coordinator SHA}"; shift 2 ;;
    --dry-run) dry_run=1; shift ;;
    --refresh-from) refresh_from="${2:?Missing old coordinator SHA}"; shift 2 ;;
    *) printf 'Unknown option: %s\n' "$1" >&2; exit 2 ;;
  esac
done
[[ "$ops_ref" =~ ^[0-9a-f]{40}$ ]] || { printf 'Use --ops-ref with the exact published 40-character recovery commit.\n' >&2; exit 2; }
[[ -z "$refresh_from" || "$refresh_from" =~ ^[0-9a-f]{40}$ ]] || { printf 'Invalid --refresh-from SHA.\n' >&2; exit 2; }
if ((dry_run)); then
  printf 'DRY RUN: verify/create independent /data/robocurve-ops at %s and pinned /data/robocurve-task-cargo; preserve all existing data; no GPU or provider calls.\n' "$ops_ref"
  exit 0
fi
command -v git >/dev/null || { printf 'Missing git; install it before transfer.\n' >&2; exit 2; }
command -v python3 >/dev/null || { printf 'Missing python3; no Isaac installation will be attempted.\n' >&2; exit 2; }
repo='https://github.com/aryansennthilkumarGT/benchmark-tasks.git'
data_root='/data'
if [[ "${ROBOCURVE_TRANSFER_TEST_MODE:-}" == '1' ]]; then
  data_root="${ROBOCURVE_TRANSFER_TEST_ROOT:?Test root required}"
  repo="${ROBOCURVE_TRANSFER_TEST_REPO:?Local fixture repository required}"
fi
python3 - "$data_root" "$ops_ref" "$repo" "$refresh_from" <<'PY'
import os,subprocess,sys,tempfile
from pathlib import Path
root,sha,url=Path(sys.argv[1]),sys.argv[2],sys.argv[3]
refresh=sys.argv[4]
def git(path,*args):
 r=subprocess.run(['git','-c','credential.helper=','-c','credential.helper=!gh auth git-credential','-C',str(path),*args],text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=180)
 if r.returncode:raise SystemExit('Git operation failed; inspect local access/paths. No source was reset or deleted.')
 return r.stdout.strip()
def identity(value):
 if value.startswith('git@github.com:'):value='https://github.com/'+value.split(':',1)[1]
 return value.removesuffix('.git').rstrip('/')
def verify(path,expected=None):
 if git(path,'rev-parse','--show-toplevel')!=str(path.resolve()):raise SystemExit('Refusing nested or unrelated ops directory')
 if identity(git(path,'remote','get-url','origin'))!=identity(url):raise SystemExit('Existing ops repository identity differs')
 if git(path,'status','--porcelain','--untracked-files=all'):raise SystemExit('Existing ops checkout is dirty; preserve it and resolve before transfer')
 if git(path,'rev-parse','HEAD')!=(expected or sha):raise SystemExit('Existing ops commit differs; no checkout/reset/overwrite was attempted')
root.mkdir(parents=True,exist_ok=True);dest=root/'robocurve-ops'
if dest.exists():
 current=git(dest,'rev-parse','HEAD')
 verify(dest,current)
 if current!=sha:
  if not refresh or current!=refresh:raise SystemExit('Existing ops commit differs: use explicit --refresh-from ORIGINAL_SHA; no reset was attempted')
  git(dest,'fetch','origin',sha)
  git(dest,'merge-base','--is-ancestor',current,sha)
  git(dest,'checkout','--detach',sha)
 verify(dest)
else:
 pending=Path(tempfile.mkdtemp(prefix='robocurve-ops-transfer-',dir=root))
 git(root,'clone','--filter=blob:none','--no-checkout','--single-branch','--branch','recovery/cloud-cpu-engineering',url,str(pending))
 git(pending,'config','core.autocrlf','false')
 git(pending,'sparse-checkout','init','--cone');git(pending,'sparse-checkout','set','coordination','tools')
 git(pending,'checkout','--detach',sha);verify(pending)
 os.rename(pending,dest)
print('Coordinator source verified: '+sha)
PY
args=(bootstrap --ops-ref "$ops_ref")
[[ -z "$refresh_from" ]] || args+=(--refresh-from "$refresh_from")
exec python3 "$data_root/robocurve-ops/coordination/brev_transfer/transfer.py" "${args[@]}"
