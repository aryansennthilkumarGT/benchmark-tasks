"""Real MuJoCo CPU contacts and exporter boundaries, never GPU evidence."""
import copy,json,math
import mujoco,numpy as np,pytest
from cpu_contact_probe import model_xml


def scene():
 b=dict(name='block',pos=[0,0,.1],quat=[0,0,0,1],mass=.1,diagonal_inertia=[.0001]*3,
        center_of_mass=[0,0,0],anchor=False,shapes=[dict(kind='box',pos=[0,0,0],quat=[0,0,0,1],size=[.02,.02,.02])])
 return dict(slug='CPU_CONTACT_TEST_FIXTURE',physics_dt=1/480,gravity=[0,0,-9.81],table_top=0.,
             material=dict(dynamic_friction=.5),assemblies=[dict(bodies=[b],joints=[])])

def test_exported_free_body_falls_and_is_physically_supported():
 m=mujoco.MjModel.from_xml_string(model_xml(scene()));d=mujoco.MjData(m)
 for _ in range(480):mujoco.mj_step(m,d)
 assert d.ncon>0 and abs(d.qpos[2]-.01)<.0002
 assert np.isfinite(d.qvel).all() and np.linalg.norm(d.qvel)<.001
 assert m.ngeom==2 and abs(m.body_mass[1]-.1)<1e-10

def test_articulations_and_unsupported_shapes_are_not_flattened():
 s=scene();s['assemblies'][0]['joints']=[dict(kind='gear')]
 with pytest.raises(ValueError,match='joint exporter'):model_xml(s)
 s=scene();s['assemblies'][0]['bodies'][0]['shapes'][0]['kind']='imaginary_mesh'
 with pytest.raises(ValueError,match='Unsupported'):model_xml(s)

def test_xyzw_rotation_and_half_extents_are_preserved():
 s=scene();b=s['assemblies'][0]['bodies'][0];b['quat']=[0,0,math.sin(.3),math.cos(.3)]
 b['shapes'][0]['size']=[.02,.03,.04]
 m=mujoco.MjModel.from_xml_string(model_xml(s));d=mujoco.MjData(m);mujoco.mj_forward(m,d)
 assert np.allclose(d.xquat[1],[math.cos(.3),0,0,math.sin(.3)])
 assert np.allclose(m.geom_size[1],[.01,.015,.02])

def test_missing_material_is_an_error_instead_of_an_invented_default():
 s=scene();s.pop('material')
 with pytest.raises(ValueError,match='Explicit authored'):model_xml(s)
