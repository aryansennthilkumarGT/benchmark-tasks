"""CPU API-call ordering only; no native simulation is claimed."""
from types import SimpleNamespace
import unittest
import numpy as np
import torch
from replay_native import initialize_fixture
from yam_arena.constants import ARM_JOINTS,FINGER_JOINTS


class FixtureOrder(unittest.TestCase):
    def test_free_root_is_written_after_all_articulation_and_robot_joints(self):
        events=[];poses=[]
        class Asset:
            def __init__(self,name,names):self.name=name;self.joint_names=names
            def write_joint_position_to_sim_index(self,**kw):events.append(self.name+'/joint')
            def write_joint_velocity_to_sim_index(self,**kw):events.append(self.name+'/velocity')
            def write_root_velocity_to_sim_index(self,**kw):events.append(self.name+'/root_velocity')
            def write_root_pose_to_sim_index(self,**kw):events.append(self.name+'/root');poses.append(kw['root_pose'])
        scene={'collar':Asset('collar',['hinge'])}
        for side in ['left','right']:scene[side+'_robot']=Asset(side,list(ARM_JOINTS)+list(FINGER_JOINTS))
        emb=SimpleNamespace(_torch=torch,_env=SimpleNamespace(unwrapped=SimpleNamespace(scene=scene,device='cpu')))
        spec=dict(assemblies=[dict(name='collar',fixed=False,bodies=[dict(name='lower'),dict(name='upper')],
                    joints=[dict(name='hinge',parent='lower',child='upper')])])
        frame=dict(bodies={'lower':dict(pos=[.3,0,.8],quat=[0,0,0,1])},joints={'hinge':-1.3})
        initialize_fixture(emb,spec,frame,np.tile([0,1,1,-.6,0,0,1.],2),True,env_origin=[1,2,3])
        self.assertEqual(events[-1],'collar/root')
        for name in ['collar/joint','left/joint','right/joint','collar/root_velocity']:
            self.assertLess(events.index(name),events.index('collar/root'))
        np.testing.assert_allclose(poses[0][0,:3].numpy(),[1.3,2,3.8],atol=1e-6)


if __name__=='__main__':unittest.main()
