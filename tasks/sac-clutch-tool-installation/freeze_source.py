"""Refresh hashes only after intentional reviewed source/asset changes.

Never run automatically to bypass a failed integrity check. This does not create
native evidence or qualify changed source against an older evaluation.
"""
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent


def freeze():
    files={}
    for p in sorted(HERE.rglob('*')):
        if not p.is_file():continue
        name=p.relative_to(HERE).as_posix()
        if name=='source_manifest.json' or name.startswith('offline-evidence/') or '__pycache__' in p.parts or '.pytest_cache' in p.parts or p.suffix=='.pyc':continue
        files[name]=hashlib.sha256(p.read_bytes().replace(b'\r\n',b'\n')).hexdigest()
    (HERE/'source_manifest.json').write_text(json.dumps(dict(schema=1,algorithm='sha256-lf-normalized',files=files),indent=2)+'\n')


if __name__=='__main__':freeze()
