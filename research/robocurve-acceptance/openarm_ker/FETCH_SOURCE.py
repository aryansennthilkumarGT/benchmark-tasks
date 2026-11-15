"""Fetch/check the official fixed-version CAD snapshot, extract selected files only."""
import argparse
import hashlib
import json
from pathlib import Path
import tarfile
import urllib.request

NAME='openarm-hardware-2.0.0.tar.gz'
URL='https://github.com/enactic/openarm_hardware/releases/download/2.0.0/'+NAME
EXPECTED='247ce0141a9be6ebbb5a6c206cf0557574929ea0b80e20dddbff7c0c0919db75'
PREFIX='openarm-hardware-2.0.0/'
SELECTED=['README.md','LICENSE.txt','OpenArm KER/README.pdf','OpenArm KER/OpenArm KER.STEP','OpenArm KER/OpenArm KER JIG BASE.STEP','OpenArm KER/OpenArm KER BOM.xlsx']

def digest(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  while b:=f.read(1024*1024):h.update(b)
 return h.hexdigest()

def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--archive',type=Path);a=p.parse_args();a.output.mkdir(parents=True,exist_ok=True)
 archive=a.archive or a.output/NAME
 if not archive.exists():
  with urllib.request.urlopen(URL,timeout=45) as r,archive.open('wb') as f:
   while b:=r.read(1024*1024):f.write(b)
 assert digest(archive)==EXPECTED,'Archive is not the inspected official2.0.0 snapshot'
 rows=[]
 with tarfile.open(archive,'r:gz') as tf:
  for name in SELECTED:
   m=tf.getmember(PREFIX+name);assert m.isfile() and not m.issym() and not m.islnk()
   data=tf.extractfile(m).read();dst=a.output/name;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(data)
   rows.append(dict(path=name,bytes=len(data),sha256=hashlib.sha256(data).hexdigest()))
 (a.output/'SOURCE_FILES.json').write_text(json.dumps(dict(url=URL,tag='2.0.0',tag_commit='08fd58364cb96b4841c601d87f5aba5557565de7',archive_sha256=EXPECTED,files=rows),indent=2)+'\n')
 print(json.dumps(dict(archive_sha256=EXPECTED,selected_files=len(rows),output=str(a.output)),indent=2))
if __name__=='__main__':main()
