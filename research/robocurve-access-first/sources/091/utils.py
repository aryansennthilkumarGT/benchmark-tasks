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
    "Lid":"part_08",
    "Power Button":"part_00",
    "Low Button":"part_02",
    "Medium Button":"part_04",
    "High Button":"part_01",
    "Pulse Button":"part_03"
}

class model_status(mu.BasicController):

    def __init__(self, articulation_prim,prim_path,screen_file = None):
        super().__init__(articulation_prim,prim_path)
        self.appliance_status['mode'] = "none"
        self.appliance_status['process'] = 0
        self.power_sensor = ContactSensor(
            prim_path=f"{self.prim_path}/part_00/Contact_Sensor",
            name="Contact_Sensor",
            frequency=120,
            translation=np.array([0, 0, 0]),
            min_threshold=0.0001,
            max_threshold=10000000,
            radius=-0.5
        )
        self.pulse_sensor = ContactSensor(
            prim_path=f"{self.prim_path}/part_03/Contact_Sensor",
            name="Contact_Sensor",
            frequency=120,
            translation=np.array([0, 0, 0]),
            min_threshold=0.0001,
            max_threshold=10000000,
            radius=-0.5
        )
        self.low_sensor = ContactSensor(
            prim_path=f"{self.prim_path}/part_02/Contact_Sensor",
            name="Contact_Sensor",
            frequency=120,
            translation=np.array([0, 0, 0]),
            min_threshold=0.0001,
            max_threshold=10000000,
            radius=-0.5
        )
        self.medium_sensor = ContactSensor(
            prim_path=f"{self.prim_path}/part_04/Contact_Sensor",
            name="Contact_Sensor",
            frequency=120,
            translation=np.array([0, 0, 0]),
            min_threshold=0.0001,
            max_threshold=10000000,
            radius=-0.5
        )
        self.high_sensor = ContactSensor(
            prim_path=f"{self.prim_path}/part_01/Contact_Sensor",
            name="Contact_Sensor",
            frequency=120,
            translation=np.array([0, 0, 0]),
            min_threshold=0.0001,
            max_threshold=10000000,
            radius=-0.5
        )

    

    def auto_check(self,button_contact):
        power_value = self.power_sensor.get_current_frame()
        if power_value['in_contact'] == True or button_contact[gt_parts['Power Button']]:
            self.appliance_status["process"] = (self.appliance_status["process"]+1)%2

        pulse_value = self.pulse_sensor.get_current_frame()
        if pulse_value['in_contact'] == True or button_contact[gt_parts['Pulse Button']]:
            if self.appliance_status["mode"] == "pulse":
                self.appliance_status["mode"] = "none"
            else:
                self.appliance_status["mode"] = "pulse"
        low_value = self.low_sensor.get_current_frame()
        if low_value['in_contact'] == True or button_contact[gt_parts['Low Button']]:
            if self.appliance_status["mode"] == "low":
                self.appliance_status["mode"] = "none"
            else:
                self.appliance_status["mode"] = "low"
        medium_value = self.medium_sensor.get_current_frame()
        if medium_value['in_contact'] == True or button_contact[gt_parts['Medium Button']]:
            if self.appliance_status["mode"] == "medium":
                self.appliance_status["mode"] = "none"
            else:
                self.appliance_status["mode"] = "medium"
        high_value = self.high_sensor.get_current_frame()
        if high_value['in_contact'] == True or button_contact[gt_parts['High Button']]:
            if self.appliance_status["mode"] == "high":
                self.appliance_status["mode"] = "none"
            else:
                self.appliance_status["mode"] = "high"

    def evaluation(self,part,gt_times,times):
        if part == gt_parts['Power Button']:
            return (gt_times-times)%2 == 0
        else:
            return gt_times == times