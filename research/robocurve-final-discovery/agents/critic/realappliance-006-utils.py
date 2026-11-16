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
    "Lid":"part_07",
    "Menu Button":"part_01",
    "Crust Color Button":"part_04",
    "Start/Pause Button":"part_06",
    "Loaf Size Button":"part_03",
    "Delay Timer up Button":"part_05",
    "Delay Timer down Button":"part_00"
}

class model_status(mu.ScreenController):
    timer = 0
    hour = 0
    min = 0
    mark_bool = {}
    appliance_status={
        "menu" : 0,
        "shade" : 0,
        "size" : 0,
        "process" : 0
    }


    def __init__(self, articulation_prim,prim_path,screen_file = None):
        super().__init__(articulation_prim,prim_path)
        self.screen_status.texture_path = screen_file['Texture']
        self.screen_status.bg_color= (200,200,200)
        self.screen_status.mark = {}
        self.number_str = "00:00"
        self.screen_path = f"{self.prim_path}/{screen_file['prim_name']}"
        self.screen_status.number = screen_file["Numbers"]
        for item in screen_file["Marks"].keys():
            self.mark_bool[item] = False
            self.screen_status.mark[item] = screen_file["Marks"][item]
        self.mark_bool['shade0'] = True
        self.mark_bool['size0'] = True
        self.update_screen()

        self.appliance_status['menu'] = 0
        self.appliance_status['shade'] = 0
        self.appliance_status['size'] = 0
        self.appliance_status['process'] = 0

        self.menu_sensor = ContactSensor(
            prim_path=f"{self.prim_path}/part_01/Contact_Sensor",
            name="Contact_Sensor",
            frequency=120,
            translation=np.array([0, 0, 0]),
            min_threshold=0.0001,
            max_threshold=10000000,
            radius=-0.5
        )
        self.shade_sensor = ContactSensor(
            prim_path=f"{self.prim_path}/part_04/Contact_Sensor",
            name="Contact_Sensor",
            frequency=120,
            translation=np.array([0, 0, 0]),
            min_threshold=0.0001,
            max_threshold=10000000,
            radius=-0.5
        )
        self.size_sensor = ContactSensor(
            prim_path=f"{self.prim_path}/part_03/Contact_Sensor",
            name="Contact_Sensor",
            frequency=120,
            translation=np.array([0, 0, 0]),
            min_threshold=0.0001,
            max_threshold=10000000,
            radius=-0.5
        )
        self.start_sensor = ContactSensor(
            prim_path=f"{self.prim_path}/part_06/Contact_Sensor",
            name="Contact_Sensor",
            frequency=120,
            translation=np.array([0, 0, 0]),
            min_threshold=0.0001,
            max_threshold=10000000,
            radius=-0.5
        )
        self.time_up_sensor = ContactSensor(
            prim_path=f"{self.prim_path}/part_05/Contact_Sensor",
            name="Contact_Sensor",
            frequency=120,
            translation=np.array([0, 0, 0]),
            min_threshold=0.0001,
            max_threshold=10000000,
            radius=-0.5
        )
        self.time_down_sensor = ContactSensor(
            prim_path=f"{self.prim_path}/part_00/Contact_Sensor",
            name="Contact_Sensor",
            frequency=120,
            translation=np.array([0, 0, 0]),
            min_threshold=0.0001,
            max_threshold=10000000,
            radius=-0.5
        )

    

    def auto_check(self,button_contact):
        if self.appliance_status["process"] == 1:
            self.timer =  self.timer+1
            if self.timer == 3600:
                self.timer = 0
                if self.hour == 0 and self.min == 1:
                    self.appliance_status["process"] = 0 
                    self.min = 0
                elif self.min == 0:
                    self.hour = self.hour-1
                    self.min = 59
                else :
                    self.min = self.min-1
                self.number_str = str(self.hour).zfill(2) + ":" + str(self.min).zfill(2)
                self.update_screen()

        start_value = self.start_sensor.get_current_frame()
        if start_value['in_contact'] == True or button_contact[gt_parts['Start/Pause Button']]:
            self.appliance_status["process"] = 1

        menu_value = self.menu_sensor.get_current_frame()
        if menu_value['in_contact'] == True or button_contact[gt_parts['Menu Button']]:
            self.appliance_status["menu"] = (self.appliance_status["menu"]+1)%12
        shade_value = self.shade_sensor.get_current_frame()
        if shade_value['in_contact'] == True or button_contact[gt_parts['Crust Color Button']]:
            self.appliance_status["shade"] = (self.appliance_status["shade"]+1)%3
            self.mark_bool['shade0'] = False
            self.mark_bool['shade1'] = False
            self.mark_bool['shade2'] = False
            self.mark_bool[f"shade{self.appliance_status['shade']}"] = True
            self.update_screen()
        size_value = self.size_sensor.get_current_frame()
        if size_value['in_contact'] == True or button_contact[gt_parts['Loaf Size Button']]:
            self.appliance_status["size"] = (self.appliance_status["size"]+1)%3
            self.mark_bool['size0'] = False
            self.mark_bool['size1'] = False
            self.mark_bool['size2'] = False
            self.mark_bool[f"size{self.appliance_status['size']}"] = True
            self.update_screen()

        time_up_value = self.time_up_sensor.get_current_frame()
        if time_up_value['in_contact'] == True or button_contact[gt_parts['Delay Timer up Button']]:
            hour = self.hour
            if hour != 15: 
                self.hour = hour+1
                self.number_str = str(hour).zfill(2) + ":" + str(min).zfill(2)
                self.update_screen()
        time_down_value = self.time_down_sensor.get_current_frame()
        if time_down_value['in_contact'] == True or button_contact[gt_parts['Delay Timer down Button']]:
            hour = self.hour
            if hour != 0: 
                self.hour = hour-1
                self.number_str = str(hour).zfill(2) + ":" + str(min).zfill(2)
                self.update_screen()

    def evaluation(self,part,gt_times,times):
        if part == gt_parts['Crust Color Button']:
            return (gt_times-times)%3 == 0
        if part == gt_parts['Loaf Size Button']:
            return (gt_times-times)%3 == 0
        if part == gt_parts['Menu Button']:
            return (gt_times-times)%12 == 0
        if part == gt_parts['Start/Pause Button']:
            return (gt_times-times)%2 == 0
        else:
            return gt_times == times