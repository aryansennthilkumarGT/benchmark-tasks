"""Disclosed supplemental contact settings, not a PhysX-equivalent backend.

MuJoCo's active margin is margin-gap. Match a zero rest offset while retaining
the detection margin; using margin alone creates a positive separation target.
Elliptic friction avoids the four-edge Coulomb-pyramid approximation. High
friction impedance follows MuJoCo's documented grasp/slippage guidance. No
coefficient, geometry, gravity or integrity bound changes with these settings.
"""
import xml.etree.ElementTree as ET


def options(root, timestep, gravity, iterations=120):
    return ET.SubElement(root, 'option', timestep=str(timestep), gravity=gravity,
                         iterations=str(iterations), tolerance='1e-10',
                         solver='Newton', integrator='implicitfast',
                         cone='elliptic', impratio='100')


def solid_default(root, friction, detection_margin):
    default = ET.SubElement(root, 'default')
    return ET.SubElement(default, 'geom', density='0', friction=friction,
                         margin=str(detection_margin), gap=str(detection_margin),
                         solref='.0022 1', solimp='.99 .999 .0001')


def description(detection_margin):
    return dict(cone='elliptic', friction_impedance_ratio=100,
                detection_margin_m=detection_margin, active_rest_offset_m=0.,
                noslip_solver=False, native_equivalence_claimed=False,
                documentation='https://mujoco.readthedocs.io/en/3.3.7/modeling.html#preventing-slip')
