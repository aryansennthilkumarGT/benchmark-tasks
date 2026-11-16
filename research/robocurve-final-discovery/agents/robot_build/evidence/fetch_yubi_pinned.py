"""Fetch only exact published YUBI inputs to a chosen output directory; no checkout."""
from pathlib import Path
import argparse, subprocess, tempfile, hashlib, json
parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,required=True);args=parser.parse_args()
pin='dd8bd13d2fd8e5003057243576f88be333d95fc5';repo='https://github.com/Toyota/yubi-hw.git'
files=['README.md','LICENSE','docs/AssemblyInstruction/YUBI Glove Assy_AssemblyGuide.pdf','docs/BOM/YUBI Glove Assy_BOM.md','STEP/glove/YUBI Glove Assy_ver2_R.STEP']
args.out.mkdir(parents=True,exist_ok=True);manifest=[]
with tempfile.TemporaryDirectory(prefix='yubi-source-') as temp:
 subprocess.run(['git','init','--quiet',temp],check=True)
 subprocess.run(['git','-C',temp,'fetch','--depth','1','--filter=blob:none','--no-write-fetch-head',repo,pin+':refs/heads/pinned'],check=True)
 for file in files:
  b=subprocess.check_output(['git','-C',temp,'show','refs/heads/pinned:'+file]);p=args.out/file;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b);manifest.append(dict(path=file,sha256=hashlib.sha256(b).hexdigest(),bytes=len(b)))
(args.out/'FETCH_MANIFEST.json').write_text(json.dumps(dict(repo=repo,pin=pin,files=manifest),indent=2)+'\n')
print(json.dumps(manifest,indent=2))
