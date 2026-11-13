"""Independent engine transforms and OBB metrics, not a robot demo."""
import itertools,json,xml.etree.ElementTree as ET
from pathlib import Path
import mujoco,numpy as np
from cpu_contact_probe import model_xml
from probe_cam_path_cpu import mesh_boxes,geometric_overlap
from motion import rotate
HERE=Path(__file__).resolve().parent


def test_convex_backend_preserves_every_original_box_corner():
 s=json.loads((HERE/'scene.json').read_text());xml=mesh_boxes(ET.fromstring(model_xml(s,dict(dynamic_friction=.2))))
 m=mujoco.MjModel.from_xml_string(ET.tostring(xml,encoding='unicode'));d=mujoco.MjData(m);mujoco.mj_forward(m,d)
 checked=0
 for assembly in s['assemblies']:
  for b in assembly['bodies']:
   for i,shape in enumerate(b['shapes']):
    if not shape.get('collision',True):continue
    assert shape['kind']=='box'
    g=mujoco.mj_name2id(m,mujoco.mjtObj.mjOBJ_GEOM,b['name']+'_'+str(i));mesh=m.geom_dataid[g]
    vertices=m.mesh_vert[m.mesh_vertadr[mesh]:m.mesh_vertadr[mesh]+m.mesh_vertnum[mesh]]
    actual=vertices@d.geom_xmat[g].reshape(3,3).T+d.geom_xpos[g]
    expected=np.array([np.array(b['pos'])+rotate(b['quat'],np.array(shape['pos'])+rotate(shape['quat'],v)) for v in itertools.product(*[(-x/2,x/2) for x in shape['size']])])
    assert len(actual)==8
    assert np.max(np.min(np.linalg.norm(actual[:,None,:]-expected[None,:,:],axis=2),axis=1))<2e-8
    assert np.max(np.abs(np.max(np.abs(vertices),axis=0)-m.geom_size[g]))<2e-8
    checked+=1
 assert checked==1874


def test_overlap_is_minimum_obb_penetration_not_solver_manifold_distance():
 for position,expected in [(.15,.05),(.30,0.)]:
  text=f'<mujoco><worldbody><body name="part"><freejoint/><geom type="box" size=".1 .1 .1"/></body><geom type="box" size=".1 .1 .1" pos="{position} 0 0"/></worldbody></mujoco>'
  m=mujoco.MjModel.from_xml_string(text);d=mujoco.MjData(m);mujoco.mj_forward(m,d)
  assert abs(geometric_overlap(m,d,1)-expected)<1e-10


def test_convex_contact_backend_has_no_spurious_deep_contact_at_recorded_pose():
 s=json.loads((HERE/'scene.json').read_text());xml=mesh_boxes(ET.fromstring(model_xml(s,dict(dynamic_friction=.2))))
 m=mujoco.MjModel.from_xml_string(ET.tostring(xml,encoding='unicode'));d=mujoco.MjData(m)
 j=mujoco.mj_name2id(m,mujoco.mjtObj.mjOBJ_JOINT,'collet_free');i=m.jnt_qposadr[j]
 d.qpos[i:i+7]=[.2400343172996321,0.,.8096518013516683,.9999990910750027,0.,.0013482763693260403,0.]
 mujoco.mj_forward(m,d);body=mujoco.mj_name2id(m,mujoco.mjtObj.mjOBJ_BODY,'collet')
 assert geometric_overlap(m,d,body)<1e-6
 assert min([0.]+[float(c.dist) for c in d.contact[:d.ncon]])>=-.000035
