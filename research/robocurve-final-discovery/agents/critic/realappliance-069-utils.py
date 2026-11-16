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
    "Power Button":"part_05",
    "Grind Amount Dial":"part_01",
    "Filter Size Button":"part_02",
    "1 Cup Button":"part_06",
    "2 Cup Button":"part_00",
    "Steam/Hot Water Dial":"part_12",
    "Program Button":"part_03"
}

class model_status(mu.BasicController):

    def __init__(self, articulation_prim,prim_path,screen_file = None):
        super().__init__(articulation_prim,prim_path)
    
        self.appliance_status['power'] = 0
        self.appliance_status['filter'] = 0
        self.appliance_status['brew'] = 0

    def auto_check(self,button_contact):
        if self.get_button_status(gt_parts['Power Button']):
            self.appliance_status['power'] = (self.appliance_status['power']+1)%2
        if self.get_button_status(gt_parts['Filter Size Button']):
            self.appliance_status['fliter'] = (self.appliance_status['fliter']+1)%2
        if self.get_button_status(gt_parts['1 Cup Button']):
            self.appliance_status['brew'] = 1
        if self.get_button_status(gt_parts['2 Cup Button']):
            self.appliance_status['brew'] = 2


    def evaluation(self,part,gt_times,times):
        if part == gt_parts['Power Button']:
            return (gt_times-times)%2 == 0
        if part == gt_parts['Filter Size Button']:
            return (gt_times-times)%2 == 0
        else:
            return gt_times == times