# Physical setup

Bimanual YAM station; x forward, y left, z up; metres, kilograms and radians; XYZW quaternions. Tabletop z=0.7475m. Fixed seed0, object_jitter0. Each envelope is the exact body-local axis-aligned collision union; shape centres and rotations are in scene.json. Body origins are reference frames, not envelope centres.

| Body | Intended material surrogate | Mass kg | Collision envelope m | World origin m | XYZW |
|---|---|---:|---|---|---|
| `captive_shaft` | steel rigid surrogate | 1.2 | (0.052, 0.25, 0.101) | (0.33, 0, 0.8225) | (0, 0, 0, 1) |
| `lower_collar` | aluminium rigid surrogate | 0.12 | (0.119, 0.131, 0.03806497) | (0.185, 0, 0.7717) | (0, 0, 0, 1) |
| `upper_collar` | aluminium rigid surrogate | 0.1 | (0.10406497, 0.119, 0.051) | (0.185, 0, 0.7717) | (0, 0, 0, 1) |
| `collar_key` | steel rigid surrogate | 0.025 | (0.022, 0.093, 0.022) | (0.36, -0.24, 0.7587) | (0, 0, 0, 1) |

The steel shaft fixture is anchored and includes fixed end flanges, supports and a2.4x180x4mm locating rib. The lower and upper aluminium collar proxies have a passive Y-axis hinge at local(-0.03,0,0)m in each half, range[-1.35,0]rad, zero stiffness and0.002 damping. A free steel retaining key has an8mm square shaft,72mm length and an orange22x24x22mm handling head. It passes through three rectangular bores,10mm wide and9.6mm tall.

Lower handle centre is(-0.05,0.09,-0.01)m; upper centre is(0.07,-0.09,0.025)m. Their support bars are16x93x12mm centred(-0.05,0.0465,-0.018)m and16x90x12mm centred(0.07,-0.045,0.018)m. Handles belong to the fixture and are not commercial-product geometry.

All movable components use static/dynamic friction0.65/0.5 and zero restitution. Material names specify physical surrogates; masses and contact coefficients are estimates, not calibrated aluminium or steel data. Scene constraints, shape facets and inertial overrides are authoritative in scene.json. Native480Hz physics uses64 position and16 velocity iterations. Reset restores authored geometry and clears scorer history. Demonstrations must start from a genuine cold reset; initialized diagnostic fixtures are not demonstrations.
