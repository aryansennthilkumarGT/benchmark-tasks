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
    "Oven Door":"part_03",
    "Oven Racks":"part_02",
    "ON/OFF Oven Control/Timer":"part_01",
    "Function Dial":"part_05",
    "Temperature Dial":"part_04"
}

class model_status(mu.CountdownController,mu.LightController):

    def __init__(self, articulation_prim,prim_path,screen_file = None):
        super().__init__(articulation_prim,prim_path)

    def auto_check(self,button_contact):
        self.knob_countdown(gt_parts["ON/OFF Oven Control/Timer"],0.00000727)
        self.inner_light()

    def evaluation(self,part,gt_times,times):
        return gt_times == times