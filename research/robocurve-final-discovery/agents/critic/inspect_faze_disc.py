"""Read author STEP cylindrical faces; static geometry only, never a fit/path pass.

Run from repository root. Requires OCP. Input is the author ZIP already downloaded
by robot_build. Output contains source hashes and unregistered native CAD frames.
"""
import hashlib
import json
from pathlib import Path
import tempfile
import zipfile

from OCP.BRepAdaptor import BRepAdaptor_Surface
from OCP.GeomAbs import GeomAbs_Cylinder
from OCP.STEPControl import STEPControl_Reader
from OCP.TopAbs import TopAbs_FACE
from OCP.TopExp import TopExp_Explorer
from OCP.TopoDS import TopoDS

ROOT = Path(__file__).resolve().parent
archive = ROOT.parent / 'robot_build/evidence/faze4/cyclo_disk_STEP_files.zip'
member = 'cyclo_disk_STEP_files/11_1 cyclo disc.STEP'
with zipfile.ZipFile(archive) as z:
    raw = z.read(member)
with tempfile.TemporaryDirectory(prefix='critic-faze-') as tmp:
    step = Path(tmp) / 'disc.STEP'
    step.write_bytes(raw)
    reader = STEPControl_Reader()
    reader.ReadFile(str(step))
    reader.TransferRoots()
    faces = TopExp_Explorer(reader.OneShape(), TopAbs_FACE)
    rows = []
    while faces.More():
        surface = BRepAdaptor_Surface(TopoDS.Face_s(faces.Current()))
        if surface.GetType() == GeomAbs_Cylinder:
            cylinder = surface.Cylinder()
            center = cylinder.Location()
            axis = cylinder.Axis().Direction()
            rows.append({
                'radius_mm': cylinder.Radius(),
                'center_native_mm': [center.X(), center.Y(), center.Z()],
                'axis_native': [axis.X(), axis.Y(), axis.Z()],
                'u_range_rad': [surface.FirstUParameter(), surface.LastUParameter()],
                'v_range_mm': [surface.FirstVParameter(), surface.LastVParameter()],
            })
        faces.Next()
result = {
    'source_archive_sha256': hashlib.sha256(archive.read_bytes()).hexdigest(),
    'source_member': member,
    'member_sha256': hashlib.sha256(raw).hexdigest(),
    'cylindrical_faces': rows,
    'limitation': 'Native unregistered faces only; seam halves repeat surfaces. No assembly registration, collision, dynamics, grasp or robot reach test.',
}
(ROOT / 'faze-disc-source-inspection.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'cylindrical_face_count': len(rows), 'status': 'SOURCE_FEATURE_EXTRACTION_ONLY'}))
