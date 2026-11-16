import omni
from PIL import Image ,ImageDraw, ImageFont
import imageio
import numpy as np
import json
from pxr import UsdLux
from isaacsim.core.prims import Articulation
from isaacsim.storage.native import get_assets_root_path
from isaacsim.core.api.materials import OmniPBR
from omni.isaac.sensor import ContactSensor
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import mech_utils_class as mu

gt_parts={
    "Lid":"part_00",
    "Basket":"part_04",
    "Temperature Control Knob":"part_01",
    "Timer Control Knob":"part_03"
}

class model_status(mu.CountdownController):

    def __init__(self, articulation_prim,prim_path,screen_file = None):
        super().__init__(articulation_prim,prim_path)

    def auto_check(self,button_contact):
        self.knob_countdown(gt_parts["Timer Control Knob"],0.00002463)
        
    def evaluation(self,part,gt_times,times):
        return gt_times == times