#!/usr/bin/env python3
"""Compare our CPU FK to the independently pinned public URDF evaluator; no Isaac."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile

import numpy as np

from access_core import Robot, ROOT

PIN = '0059d02a1a91bc6834c1d0846022891df0c78730'


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--robot-repo', required=True, type=Path)
    a = p.parse_args()
    def blob(path):
        return subprocess.check_output(['git', '-C', str(a.robot_repo), 'show', PIN+':'+path])
    code = blob('yam_arena/urdf.py')
    urdf = blob('yam_arena/assets/yam/yam_arm.urdf')
    robot = Robot()
    cases = [robot.data['ready_joint_radians']+[-.04695, -.04695], [0.]*8,
             [.4, .7, 1.2, -.4, .2, .8, -.02, -.03]]
    results = []
    with tempfile.TemporaryDirectory(prefix='robocurve-reference-') as folder:
        file, xml = Path(folder)/'reference.py', Path(folder)/'robot.urdf'
        file.write_bytes(code)
        xml.write_bytes(urdf)
        spec = importlib.util.spec_from_file_location('pinned_reference_urdf', file)
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)  # Reviewed pure NumPy/xml module, no simulator imports.
        for q in cases:
            for side in ['left', 'right']:
                their = module.forward_kinematics(xml, dict(zip([f'joint{i}' for i in range(1, 9)], q)))
                ours, _ = robot.fk(q, side)
                error = max(float(np.max(np.abs(ours[k]-robot.base_poses[side]@v))) for k, v in their.items())
                results.append({'side': side, 'q': q, 'max_transform_element_error': error})
    output = {'reference_pin': PIN, 'reference_code_sha256': hashlib.sha256(code).hexdigest(),
              'reference_urdf_sha256': hashlib.sha256(urdf).hexdigest(), 'cases': results,
              'all_within_1e_minus_12': all(x['max_transform_element_error'] < 1e-12 for x in results),
              'scope': 'Independent source-parser/FK agreement on all links; not robot/task feasibility or physical calibration.'}
    (ROOT/'results/REFERENCE_FK_COMPARISON.json').write_text(json.dumps(output, indent=2)+'\n')
    print(json.dumps(output, indent=2))
    return 0 if output['all_within_1e_minus_12'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
