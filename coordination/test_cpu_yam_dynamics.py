"""Real CPU dynamics/export checks, distinct from native Isaac qualification."""
import xml.etree.ElementTree as ET
import numpy as np,pytest,mujoco
from scipy.spatial import ConvexHull
import cpu_yam_dynamics as rig
from yam_arena import YAM_URDF,station
from yam_arena.constants import ARM_JOINTS,FINGER_JOINTS,FINGER_OPEN,SHOULDER,WRIST,GRIPPER
from yam_arena.urdf import forward_kinematics,rpy_matrix

@pytest.fixture(scope='module')
def compiled():return mujoco.MjModel.from_xml_string(rig.export_robot_only())


def test_all_actual_link_frames_match_independent_sdk_fk(compiled):
 m=compiled;d=mujoco.MjData(m)
 for arm in [[0,1,1,-.6,0,0],[.3,1.3,1.4,-.8,.2,-.2],[-.4,.6,1.8,-1.1,-.3,.5]]:
  action=np.tile(np.r_[arm,.37],2);rig.initialize_robot(m,d,action)
  config=dict(zip(ARM_JOINTS,arm));config.update({n:.37*FINGER_OPEN for n in FINGER_JOINTS});fk=forward_kinematics(YAM_URDF,config)
  for side in ('left','right'):
   for link,expected in fk.items():
    i=mujoco.mj_name2id(m,mujoco.mjtObj.mjOBJ_BODY,side+'_'+link)
    assert np.max(np.abs(d.xpos[i]-expected[:3,3]-station.BASES[side]))<1e-8
    assert np.max(np.abs(d.xmat[i].reshape(3,3)-expected[:3,:3]))<1e-8


def test_rotated_urdf_inertial_frames_and_full_tensors_are_preserved(compiled):
 m=compiled
 for link in ET.parse(YAM_URDF).getroot().findall('link'):
  inertial=link.find('inertial');o=inertial.find('origin');i=inertial.find('inertia');rotation=rpy_matrix(rig.xyz(o,'rpy'))
  tensor=np.array([[float(i.get('ixx')),float(i.get('ixy')),float(i.get('ixz'))],[float(i.get('ixy')),float(i.get('iyy')),float(i.get('iyz'))],[float(i.get('ixz')),float(i.get('iyz')),float(i.get('izz'))]])
  for side in ('left','right'):
   bid=mujoco.mj_name2id(m,mujoco.mjtObj.mjOBJ_BODY,side+'_'+link.get('name'));matrix=np.zeros(9);mujoco.mju_quat2Mat(matrix,m.body_iquat[bid]);r=matrix.reshape(3,3)
   assert np.allclose(m.body_ipos[bid],rig.xyz(o,'xyz'),atol=1e-12)
   assert np.allclose(r@np.diag(m.body_inertia[bid])@r.T,rotation@tensor@rotation.T,atol=1e-12)
   assert m.body_mass[bid]==pytest.approx(float(inertial.find('mass').get('value')))


def stl_vertices(path):
 data=path.read_bytes();import struct
 count=struct.unpack_from('<I',data,80)[0]
 assert len(data)==84+50*count
 dtype=np.dtype([('normal','<f4',(3,)),('vertices','<f4',(3,3)),('attribute','<u2')])
 return np.frombuffer(data,dtype=dtype,count=count,offset=84)['vertices'].reshape(-1,3).astype(float)


def test_every_original_collision_support_plane_survives_mjcf_compilation(compiled):
 m=compiled;d=mujoco.MjData(m);rig.initialize_robot(m,d)
 # Compare original link-local solids at q0, independent of mjcf mesh centering.
 for link in ET.parse(YAM_URDF).getroot().findall('link'):
  name=link.get('name')
  for index,c in enumerate(link.findall('collision')):
   mesh=c.find('geometry/mesh');points=stl_vertices((YAM_URDF.parent/mesh.get('filename')).resolve())*rig.xyz(mesh,'scale','1 1 1')
   o=c.find('origin');points=points@rpy_matrix(rig.xyz(o,'rpy')).T+rig.xyz(o,'xyz');hull=ConvexHull(points);normals=hull.equations[:,:3]
   for side in ('left','right'):
    gid=mujoco.mj_name2id(m,mujoco.mjtObj.mjOBJ_GEOM,side+'_'+name+'_'+str(index));mid=m.geom_dataid[gid];start=m.mesh_vertadr[mid];count=m.mesh_vertnum[mid];local=m.mesh_vert[start:start+count];world=local@d.geom_xmat[gid].reshape(3,3).T+d.geom_xpos[gid];bid=m.geom_bodyid[gid];r=d.xmat[bid].reshape(3,3);back=(world-d.xpos[bid])@r
    assert np.max(np.abs((back@normals.T).max(0)-(points@normals.T).max(0)))<3e-7


def test_native_overrides_replace_urdf_placeholder_effort_and_keep_asymmetric_collision_masks(compiled):
 m=compiled
 for side,ids in rig.indexes(m).items():
  for n,jid in zip(ARM_JOINTS+FINGER_JOINTS,ids):
   cfg=GRIPPER if n in FINGER_JOINTS else SHOULDER if n in ARM_JOINTS[:3] else WRIST
   aid=mujoco.mj_name2id(m,mujoco.mjtObj.mjOBJ_ACTUATOR,side+'_'+n+'_drive')
   assert np.allclose(m.actuator_forcerange[aid],[-cfg['effort'],cfg['effort']])
   assert m.actuator_gainprm[aid,0]==cfg['stiffness']
   assert m.actuator_biasprm[aid,2]==-cfg['damping']
   assert m.jnt_actgravcomp[jid]
 for gid in range(m.ngeom):
  name=mujoco.mj_id2name(m,mujoco.mjtObj.mjOBJ_GEOM,gid)
  if name.startswith('left_'):assert (m.geom_contype[gid],m.geom_conaffinity[gid])==(2,5)
  if name.startswith('right_'):assert (m.geom_contype[gid],m.geom_conaffinity[gid])==(4,3)


def test_gravity_hold_is_actual_dynamics_and_negative_control_falls(compiled):
 m=compiled;d=mujoco.MjData(m);rig.initialize_robot(m,d);q0=rig.measured(m,d)
 for _ in range(960):mujoco.mj_step(m,d)
 assert np.max(np.abs(rig.measured(m,d)-q0))<1e-6
 # A different model removes compensation. No state overwrite after initialization.
 unbalanced=mujoco.MjModel.from_xml_string(rig.export_robot_only());unbalanced.body_gravcomp[:]=0.;u=mujoco.MjData(unbalanced);rig.initialize_robot(unbalanced,u)
 for _ in range(960):mujoco.mj_step(unbalanced,u)
 assert np.max(np.abs(rig.measured(unbalanced,u)-q0))>.005


def test_invalid_or_out_of_range_actions_fail_before_simulation(compiled):
 m=compiled;d=mujoco.MjData(m);rig.initialize_robot(m,d)
 with pytest.raises(ValueError,match='14D'):rig.command_robot(m,d,np.zeros(13))
 q=rig.measured(m,d);q[0]=20.
 with pytest.raises(ValueError,match='range'):rig.command_robot(m,d,q)


def test_a_late_invalid_action_cannot_partially_change_either_robot(compiled):
 m=compiled;d=mujoco.MjData(m);rig.initialize_robot(m,d);before=d.ctrl.copy();q=rig.measured(m,d);q[0]=.2;q[13]=2.
 with pytest.raises(ValueError,match='range'):rig.command_robot(m,d,q)
 assert np.array_equal(d.ctrl,before)
