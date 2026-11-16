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
    "Jar Lid":"part_02",
    "Rotary Dial":"part_01"
}

class model_status(mu.BasicController):


    def __init__(self, articulation_prim,prim_path,screen_file = None):
        super().__init__(articulation_prim,prim_path)
    

    def auto_check(self,button_contact):
        return

    def evaluation(self,part,gt_times,times):
        return gt_times == times