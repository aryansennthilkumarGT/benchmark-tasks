"""Restore passive spring rest targets without changing any body/joint state.

Uses the target_command API in pinned yam-arena0059d02/IsaacLab3.0. The official
Arena reset event separately restores authored initial poses/coordinates. Initial
compression is not the spring's equilibrium, and prior diagnostic targets must
never leak into a fresh episode. No expert or per-step task logic calls this.
"""

def configure_passive_targets(env,env_ids,asset_cfg,joints):
 if env_ids is None:return
 import torch
 asset=env.scene[asset_cfg.name];names=list(asset.joint_names)
 ids=[names.index(j['name']) for j in joints]
 if len(set(ids))!=len(ids):raise ValueError('Duplicate passive joint mapping')
 target=torch.tensor([[j.get('rest',0.) for j in joints]],device=env.device,dtype=torch.float32).expand(len(env_ids),-1).contiguous()
 command=asset.actuators.target_command
 command.set_position_index(value=target,env_ids=env_ids,joint_ids=ids)
 command.set_velocity_index(value=torch.zeros_like(target),env_ids=env_ids,joint_ids=ids)
