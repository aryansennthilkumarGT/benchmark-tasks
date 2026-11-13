"""Bind diagnostics to every runtime Python source, physical input and original USD."""
import hashlib
from pathlib import Path

def runtime_hashes(folder):
 folder=Path(folder);files=list(folder.glob('*.py'))+[folder/n for n in ['scene.json','controller.json','stack-lock.json','contact-reference.json'] if (folder/n).is_file()]+list((folder/'assets').glob('*.usda'))
 return {f.relative_to(folder).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(files)}
def require_same(folder,expected):
 if not isinstance(expected,dict) or runtime_hashes(folder)!=expected:raise ValueError('Runtime inputs changed; diagnostic is stale')
