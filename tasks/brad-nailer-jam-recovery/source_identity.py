"""Runtime input hashes for real source-bound offline evidence."""
import hashlib

def runtime_hashes(folder):
 files=list(folder.glob('*.py'))+[folder/n for n in ['scene.json','controller.json','guided-cycle-reference.json','stack-lock.json']]+list((folder/'assets').glob('*.usda'))+list((folder/'test_fixtures').glob('*.json'))
 return {p.relative_to(folder).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)}

def require_same(folder,expected):
 if not expected or runtime_hashes(folder)!=expected:raise ValueError('Runtime inputs changed; stale trace cannot qualify this source')
