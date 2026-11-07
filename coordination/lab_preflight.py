#!/usr/bin/env python3
"""Read-only lab diagnostics. This does not run simulations or validate tasks.
Reports credential presence only; never reads their values or credential files.
Run in the target account's intended project directory after activating its environment.
"""
import argparse
import csv
import getpass
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import shutil
import socket
import subprocess
import sys

def command(args):
    try:
        p = subprocess.run(args, capture_output=True, text=True, timeout=20, check=False)
        return {"returncode": p.returncode, "stdout": p.stdout.strip(), "stderr": p.stderr.strip()}
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"returncode": None, "error": type(exc).__name__}

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--expected-host", required=True, help="Actual confirmed hostname; not an unverified SSH alias.")
    ap.add_argument("--expected-user", default="asenthil74")
    args = ap.parse_args()
    host = socket.gethostname()
    user = getpass.getuser()
    gpu = command(["nvidia-smi", "--query-gpu=name,driver_version,memory.total,memory.free,utilization.gpu", "--format=csv,noheader,nounits"])
    gpu_rows = []
    if gpu.get("returncode") == 0:
        for row in csv.reader(gpu["stdout"].splitlines()):
            if len(row) == 5:
                gpu_rows.append(dict(zip(["name","driver","total_mib","free_mib","utilization_percent"], [x.strip() for x in row])))
    mem = {}
    meminfo = Path("/proc/meminfo")
    if meminfo.exists():
        for line in meminfo.read_text().splitlines():
            key, _, value = line.partition(":")
            if key in {"MemTotal","MemAvailable"}:
                mem[key] = value.strip()
    disk = shutil.disk_usage(Path.cwd())
    packages = {}
    for name in ("isaacsim","isaaclab","isaaclab-arena","inspect-robots","inspect-robots-dream","dreamlabs","yam-arena"):
        try:
            packages[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            packages[name] = None
    checks = {
        "linux": platform.system() == "Linux",
        "expected_host": host.casefold() == args.expected_host.casefold(),
        "expected_user": user == args.expected_user,
        "rtx_4090_present": any("RTX 4090" in row["name"] for row in gpu_rows),
        "nvidia_driver_query": gpu.get("returncode") == 0,
    }
    report = {
        "kind":"READ_ONLY_PREFLIGHT_NOT_SIMULATION_EVIDENCE",
        "host":host, "user":user, "cwd":str(Path.cwd()), "os":platform.platform(),
        "python":sys.version.split()[0], "checks":checks,
        "gpu":gpu_rows, "gpu_query":gpu,
        "memory":mem, "disk_bytes":{"total":disk.total,"free":disk.free},
        "git":command(["git","--version"]), "packages":packages,
        "executables":{x:shutil.which(x) for x in ("python3","git","ffmpeg","inspect-robots","tmux","codex")},
        "credentials_present":{
            "ROBOCURVE_TOKEN":bool(os.environ.get("ROBOCURVE_TOKEN")),
            "DREAM_API_KEY":bool(os.environ.get("DREAM_API_KEY")),
            "dream_credentials_file":(Path.home()/".dreamlabs"/"credentials").is_file(),
        },
        "authentication_verified":False,
        "gpu_workload_started":False,
        "manual_review_required":[
            "Verify workload authorization and shared GPU utilization before launching.",
            "Review free VRAM/RAM/disk against the actual stack and scene.",
            "Verify network access and real service authentication separately.",
            "Inspect existing environment before installation or upgrade."
        ],
    }
    print(json.dumps(report, indent=2))
    return 0 if all(checks.values()) else 2

if __name__ == "__main__":
    raise SystemExit(main())
