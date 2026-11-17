"""Audit dataset geometry for the documented spring/prong/cuff mechanism."""
from pathlib import Path
import json,sys,hashlib,gzip,io
sys.path.insert(0,'/workspace/robocurve-cpu-deps')
import trimesh
p=Path(__file__).resolve().parents[1]/'sources/Chefman_080_OBJ.obj.gz'
raw=gzip.decompress(p.read_bytes());s=trimesh.load(io.BytesIO(raw),file_type='obj',force='scene',process=False)
rows=[]
for name,m in s.geometry.items():
 r=dict(name=name,vertices=len(m.vertices),faces=len(m.faces),bounds=m.bounds.tolist(),watertight=m.is_watertight)
 rows.append(r);print(name,len(m.vertices),len(m.faces),m.bounds)
Path(__file__).with_name('results').joinpath('DATASET_MESH_AUDIT.json').write_text(json.dumps(dict(source='RealAppliance researcher asset; NOT manufacturer CAD',sha256=hashlib.sha256(raw).hexdigest(),geometry=rows),indent=2)+'\n')
