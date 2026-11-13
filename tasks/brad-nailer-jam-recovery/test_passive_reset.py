"""CPU SDK-call contract only; recording doubles are never physics evidence."""
from types import SimpleNamespace
import torch
from passive_reset import configure_passive_targets

class CommandRecorder:
 def __init__(self):self.position=None;self.velocity=None
 def set_position_index(self,**kwargs):self.position=kwargs
 def set_velocity_index(self,**kwargs):self.velocity=kwargs

def test_preloaded_start_does_not_become_spring_equilibrium():
 command=CommandRecorder();asset=SimpleNamespace(joint_names=['gear','pad'],actuators=SimpleNamespace(target_command=command))
 env=SimpleNamespace(device='cpu',scene={'fixture':asset});ids=torch.tensor([0,2]);cfg=SimpleNamespace(name='fixture')
 configure_passive_targets(env,ids,cfg,[dict(name='pad',initial=.002,rest=0.),dict(name='gear',initial=-1.8,rest=0.)])
 assert command.position['joint_ids']==[1,0]
 assert command.position['value'].shape==(2,2)
 assert torch.equal(command.position['value'],torch.zeros(2,2))
 assert torch.equal(command.velocity['value'],torch.zeros(2,2))
 assert command.position['env_ids'] is ids

def test_no_selected_environments_does_not_touch_asset():
 configure_passive_targets(SimpleNamespace(),None,SimpleNamespace(),[])
