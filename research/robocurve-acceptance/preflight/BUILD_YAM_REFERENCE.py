#!/usr/bin/env python3
"""Extract pinned existing YAM collision geometry for offline CPU preflight; no simulator."""
import argparse
import gzip
import hashlib
import io
import json
from pathlib import Path
import struct
import subprocess
import tarfile
import xml.etree.ElementTree as ET

import numpy as np

PIN = '0059d02a1a91bc6834c1d0846022891df0c78730'
PREFIX = 'yam_arena/assets/yam/'


def rpy_matrix(rpy):
    r, p, y = rpy
    cr, sr, cp, sp, cy, sy = np.cos(r), np.sin(r), np.cos(p), np.sin(p), np.cos(y), np.sin(y)
    return np.array([[cy*cp, cy*sp*sr-sy*cr, cy*sp*cr+sy*sr],
                     [sy*cp, sy*sp*sr+cy*cr, sy*sp*cr-cy*sr],
                     [-sp, cp*sr, cp*cr]])


def origin(element):
    e = element.find('origin')
    return ([float(x) for x in e.get('xyz', '0 0 0').split()],
            [float(x) for x in e.get('rpy', '0 0 0').split()]) if e is not None else ([0., 0., 0.], [0., 0., 0.])


def vertices(data):
    if len(data) >= 84 and len(data) == 84 + 50 * struct.unpack_from('<I', data, 80)[0]:
        dtype = np.dtype([('normal', '<f4', (3,)), ('vertices', '<f4', (3, 3)), ('attr', '<u2')])
        return np.frombuffer(data, dtype=dtype, offset=84)['vertices'].reshape(-1, 3).astype(float)
    lines = data.decode().splitlines()
    return np.array([[float(x) for x in line.split()[1:4]] for line in lines if line.strip().startswith('vertex')])


def build(repo, out):
    paths = [PREFIX + 'yam_arm.urdf', PREFIX + 'collision', PREFIX + 'SOURCE_COMMIT',
             PREFIX + 'LICENSE.i2rt', 'yam_arena/constants.py', 'yam_arena/station.py', 'yam_arena/robot.py']
    archive = subprocess.check_output(['git', '-C', str(repo), 'archive', PIN, *paths])
    with tarfile.open(fileobj=io.BytesIO(archive)) as tf:
        blobs = {m.name: tf.extractfile(m).read() for m in tf.getmembers() if m.isfile()}
    tree = ET.fromstring(blobs[PREFIX + 'yam_arm.urdf'])
    joints = []
    for j in tree.findall('joint'):
        xyz, rpy = origin(j)
        lim = j.find('limit')
        joints.append({'name': j.get('name'), 'type': j.get('type'), 'parent': j.find('parent').get('link'),
                       'child': j.find('child').get('link'), 'xyz_m': xyz, 'rpy_rad': rpy,
                       'axis': [float(x) for x in j.find('axis').get('xyz').split()],
                       'lower': float(lim.get('lower')), 'upper': float(lim.get('upper'))})
    links = {}
    used = set(paths) - {PREFIX + 'collision'}
    for link in tree.findall('link'):
        inertia = link.find('inertial')
        com, _ = origin(inertia)
        hulls = []
        for i, collision in enumerate(link.findall('collision')):
            mesh = collision.find('geometry/mesh')
            path = PREFIX + mesh.get('filename')
            used.add(path)
            xyz, rpy = origin(collision)
            scale = np.array([float(x) for x in mesh.get('scale', '1 1 1').split()])
            pts = (vertices(blobs[path]) * scale) @ rpy_matrix(rpy).T + xyz
            hulls.append({'name': f'{link.get("name")}:{i}', 'vertices_link_m': np.unique(pts, axis=0).tolist(),
                          'source_path': path, 'source_sha256': hashlib.sha256(blobs[path]).hexdigest()})
        links[link.get('name')] = {'mass_kg': float(inertia.find('mass').get('value')), 'com_m': com, 'hulls': hulls}
    # These values are read from the pinned constants.py/station.py, not hardware ratings.
    bundle = {'schema': 1, 'pin': PIN, 'repository': 'https://github.com/kairosiann/yam-isaac-lab-arena',
              'asset_source_commit': blobs[PREFIX + 'SOURCE_COMMIT'].decode().strip(),
              'units': 'metres, radians, kilograms', 'geometry': 'actual yam_arm.urdf CoACD collision hulls',
              'joints': joints, 'links': links, 'tcp_offset_m': [0., 0., .134],
              'ready_joint_radians': [0., 1., 1., -.6, 0., 0.],
              'station_bases_m': {'left': [0., .305, .75], 'right': [0., -.305, .75]},
              'station_table': {'size_m': [1.10, 1.30, .06], 'centre_m': [.36, 0., .7175], 'top_m': .7475},
              'actuator_effort_configuration': {'joint1': 27., 'joint2': 27., 'joint3': 27.,
                                                 'joint4': 7., 'joint5': 7., 'joint6': 7., 'finger': 50.},
              'claims': ['Simulator geometry/configuration, not hardware force certification.',
                         'No camera-housing or task geometry is inferred from a TCP or product photograph.'],
              'source_manifest': [{'path': p, 'sha256': hashlib.sha256(blobs[p]).hexdigest(), 'bytes': len(blobs[p])}
                                  for p in sorted(used)]}
    out.mkdir(parents=True, exist_ok=True)
    raw = json.dumps(bundle, separators=(',', ':'), allow_nan=False).encode()
    # Fixed gzip metadata makes rebuilding byte-for-byte reproducible.
    with (out / 'YAM_REFERENCE.json.gz').open('wb') as f:
        with gzip.GzipFile(filename='', fileobj=f, mode='wb', mtime=0) as g:
            g.write(raw)
    (out / 'LICENSE.i2rt').write_bytes(blobs[PREFIX + 'LICENSE.i2rt'])
    summary = {'pin': PIN, 'bundle_sha256': hashlib.sha256((out / 'YAM_REFERENCE.json.gz').read_bytes()).hexdigest(),
               'collision_hulls_per_link': {k: len(v['hulls']) for k, v in links.items()},
               'collision_vertices': sum(len(h['vertices_link_m']) for v in links.values() for h in v['hulls']),
               'source_manifest': bundle['source_manifest']}
    (out / 'YAM_SOURCE_MANIFEST.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps({k: v for k, v in summary.items() if k != 'source_manifest'}, indent=2))


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--robot-repo', required=True, type=Path)
    p.add_argument('--output', default=Path(__file__).parent / 'assets', type=Path)
    args = p.parse_args()
    build(args.robot_repo, args.output)
