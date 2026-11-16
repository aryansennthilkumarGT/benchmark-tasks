from omni.isaac.kit import SimulationApp
simulation_app = SimulationApp({"headless": True})

from openai import OpenAI
import os
import math
import re
import numpy as np
import json
from PIL import Image, ImageFont, ImageDraw
from tqdm import tqdm
import base64
from typing import List
from argparse import ArgumentParser
import importlib
import omni
import requests
import imageio
from pxr import UsdPhysics, PhysxSchema,UsdLux,Gf, UsdGeom, Usd, UsdShade
from isaacsim.core.prims import Articulation
from isaacsim.core.utils.stage import add_reference_to_stage
from isaacsim.storage.native import get_assets_root_path
from isaacsim.core.api.objects.ground_plane import GroundPlane
from isaacsim.core.api.materials import OmniPBR,VisualMaterial
from omni.isaac.core.utils.stage import open_stage
from omni.isaac.core import World
from omni.isaac.sensor import Camera

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
    
def llm_response(messages, model_version):
        #put api here
        #ccurrent one not in use
        pass
        
#Predict next step
def next_step(history,current_img,task_prompt,planning,llm):
    content = []
    his = ""
    for history_steps in history:
        his += f'{history_steps},'
    content.append({"type": "text", "text":  f"Conduct History: {his}"})
    plan = ""
    for plan_steps in planning:
        plan += f'{plan_steps},'
    content.append({"type": "text", "text":  f"Complete Conduction: {plan}"})
    image_encoded = encode_image(f"{current_img}")
    content.append({"type": "image_url", "image_url":  {"url": f"data:image/jpeg;base64,{image_encoded}", "detail": "low"}})

    messages = [
        {"role": "system", "content": task_prompt},
        {"role": "user", "content": content},
    ]
    answer = llm_response(messages,llm)
    return answer

#Get mesh normal direction for camera orientation
def get_mesh_normal(screen_prim):
    """
    获取mesh的平均法线方向
    """
    try:
        mesh = UsdGeom.Mesh(screen_prim)
        if mesh:
            
            normals = mesh.GetNormalsAttr().Get()
            if normals:
                
                avg_normal = Gf.Vec3f(0, 0, 0)
                for normal in normals:
                    avg_normal += normal
                avg_normal /= len(normals)
                avg_normal.Normalize()
                return avg_normal
    except:
        pass
    
    
    return Gf.Vec3f(0, 0, 1)

#initialize camera position and orientation based on screen position and normal
def set_camera(screen,manual_subdir,camera,stage,camera_distance=2.0):
    if not screen:
        '''
        camera_path = f"/World/Camera"
        camera_prim = stage.GetPrimAtPath(camera_path)
        
        if not camera_prim.IsValid():
            camera_prim = UsdGeom.Camera.Define(stage, camera_path)
            print(f"创建新摄像头: {camera_path}")
        else:
            camera_prim = UsdGeom.Camera(camera_prim)
            print(f"更新现有摄像头: {camera_path}")

        camera_prim = UsdGeom.Camera(camera_prim)
        camera_xform = UsdGeom.Xformable(camera_prim)
        camera_xform.ClearXformOpOrder()
        
        pos_vec = Gf.Vec3f(1,0,2)
        camera_xform.AddTranslateOp().Set(pos_vec)

        quat_obj = Gf.Quatf(1.0,0.0,0.0,0.0)  # (w, x, y, z)
        camera_xform.AddOrientOp(UsdGeom.XformOp.PrecisionFloat).Set(quat_obj)
        '''
        camera.set_world_pose(
            position=[0,-2.2,0.6],
            orientation=[0.8,0.6,0,0],
            camera_axes="usd"
        )
        return None
    
    with open(f"./manuals_pdfs/{manual_subdir}/screen.json", 'r', encoding='utf-8') as file:
        screen_json = json.load(file)
    screen_prim_path = screen_json["mesh_path"]
    screen_prim = stage.GetPrimAtPath(screen_prim_path)
    if not screen_prim.IsValid():
        print(f"!ERROR: No Prim Path at {screen_prim_path}")
        return None
    
    
    screen_xform = UsdGeom.Xformable(screen_prim)
    screen_time = Usd.TimeCode.Default()
    screen_transform = screen_xform.ComputeLocalToWorldTransform(screen_time)
    
    local_normal = get_mesh_normal(screen_prim)
    world_normal = screen_transform.TransformDir(local_normal)
    world_normal.Normalize()

    screen_position = screen_transform.ExtractTranslation()
    world_normal_d = Gf.Vec3d(world_normal[0], world_normal[1], world_normal[2])

    camera_position = screen_position + world_normal_d * camera_distance
    xyz_position =[
        float(camera_position[0]),
        float(camera_position[1]), 
        float(camera_position[2])
    ]

    up_vector = Gf.Vec3d(0, 0, 1) 

    look_at_matrix = Gf.Matrix4d().SetLookAt(
        Gf.Vec3d(camera_position),  
        Gf.Vec3d(screen_position),    
        up_vector                   
    )

    rotation = look_at_matrix.ExtractRotation()
    quat = rotation.GetQuat()
    wxyz_quat =[
        float(quat.GetReal()),      # w
        -float(quat.GetImaginary()[0]),  # x
        -float(quat.GetImaginary()[1]),  # y  
        -float(quat.GetImaginary()[2])   # z
    ]
    if world_normal == (0,0,1):
        wxyz_quat=[1,0,0,0]
    #print(rotation)
    #print(screen_position,quat)
    camera.set_world_pose(
        position=xyz_position,
        orientation=wxyz_quat,
        camera_axes="usd"
    )

    print(f"Camera Set at: {camera_position}")
    print(f"Normal Direction: {world_normal}")
    return screen_json

def set_joint_status(pos,part,articulation_prim):
    index = articulation_prim.get_dof_index(part)
    articulation_prim.set_joint_positions(pos,[0],[index])
    #print("Success set",pos,part,index)

def get_joint_limit(part,articulation_prim):
    index = articulation_prim.get_dof_index(part)
    limit1 = articulation_prim.get_dof_limits()[0][index][1]
    limit0 = articulation_prim.get_dof_limits()[0][index][0]
    if abs(limit1) > abs(limit0):
        return limit1
    else:
        return limit0

#Conduct step based on instruction, return button contact status for evaluation and auto check
def conduct_step(articulation_prim,gt_parts,counter,instruction,button_contact):
    dof_list = articulation_prim.dof_names

    if "press" in instruction:
        ins = instruction.replace("press","")
        ins = ins.replace("(","")
        ins = ins.replace(")","")
        part_name,_,times = ins.split(",")
        part_name = part_name.strip().lower()
        times = re.sub(r'\D', '', times)
        times = int(times)

        if part_name not in gt_parts.keys():
            print(part_name,"Not in dict")
            return button_contact
        part_name = gt_parts[part_name]

        if counter < times :
            if part_name in dof_list:
                limit = get_joint_limit(part_name,articulation_prim)
                set_joint_status(limit,part_name,articulation_prim)
                button_contact[part_name] = True
            else:
                button_contact[part_name] = True
        if counter == times:
            if part_name in dof_list:
                set_joint_status(0,part_name,articulation_prim)
                button_contact[part_name] = False
            else:
                button_contact[part_name] = False

    elif "push" in instruction:
        ins = instruction.replace("push","")
        ins = ins.replace("(","")
        ins = ins.replace(")","")
        part_name,_ = ins.split(",")
        part_name = part_name.strip().lower()

        if part_name not in gt_parts.keys():
            print(part_name,"Not in dict")
            return button_contact
        part_name = gt_parts[part_name]

        if counter == 0 :
            if part_name in dof_list:
                limit = get_joint_limit(part_name,articulation_prim)
                set_joint_status(limit,part_name,articulation_prim)
            else:
                print(part_name,"Not in dof list")
    
    elif "rotate" in instruction:
        ins = instruction.replace("rotate","")
        ins = ins.replace("(","")
        ins = ins.replace(")","")
        part_name,_,degrees = ins.split(",")
        part_name = part_name.strip().lower()
        degrees = re.sub(r'\D', '', degrees)
        degrees = int(degrees)

        if part_name not in gt_parts.keys():
            print(part_name,"Not in dict")
            return button_contact
        part_name = gt_parts[part_name]

        if counter == 0 :
            if part_name in dof_list:
                pos = degrees * math.pi / 180
                limit = get_joint_limit(part_name,articulation_prim)
                if limit > 0:
                    set_joint_status(pos,part_name,articulation_prim)
                else:
                    set_joint_status(-pos,part_name,articulation_prim)
            else:
                print(part_name,"Not in dof list")

    elif "open" in instruction:
        ins = instruction.replace("open","")
        ins = ins.replace("(","")
        ins = ins.replace(")","")
        part_name = ins.strip().lower()

        if part_name not in gt_parts.keys():
            print(part_name,"Not in dict")
            return button_contact
        part_name = gt_parts[part_name]

        if counter == 0 :
            if part_name in dof_list:
                limit = get_joint_limit(part_name,articulation_prim)
                set_joint_status(limit,part_name,articulation_prim)
            else:
                print(part_name,"Not in dof list")

    elif "close" in instruction:
        ins = instruction.replace("close","")
        ins = ins.replace("(","")
        ins = ins.replace(")","")
        part_name = ins.strip().lower()

        if part_name not in gt_parts.keys():
            print(part_name,"Not in dict")
            return button_contact
        part_name = gt_parts[part_name]

        if counter == 0 :
            if part_name in dof_list:
                set_joint_status(0,part_name,articulation_prim)
            else:
                print(part_name,"Not in dof list")
    return button_contact

def save_log(out_dir,log,new_log,plan_length,success_length,result_dict,manual_subdir):
    success_rate = success_length/plan_length
    log.append(new_log)
    with open(os.path.join(out_dir, f"detailed_results.json"), 'w', encoding='utf-8') as file:
        json.dump(log, file, ensure_ascii=False, indent=4)
    result_dict[manual_subdir]["success_rate"].append(success_rate)
    with open(f"./benchmark_closeloop_{args.llm_model}.json", 'w', encoding='utf-8') as file:
        json.dump(result_dict, file, ensure_ascii=False, indent=4)
    return result_dict
    
def benchmark(manual_dir,manual_subdir, result_dict,out_dir,llm):
    log = []
    current_dir = os.path.dirname(os.path.abspath(__file__))
    target_path = os.path.join(
        current_dir, 
        "model", 
        manual_subdir[:3], 
        "utils.py"
    )
    # normalize the path and check if it exists
    target_path = os.path.abspath(target_path)
    if not os.path.exists(target_path):
        print(f"文件不存在: {target_path}")
        return None
    # import utils.py as a module
    module_name = f"model_{manual_subdir[:3]}_utils"
    spec = importlib.util.spec_from_file_location(module_name, target_path)
    utils = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(utils)

    #utils = importlib.import_module(f"..manual.{manual_subdir}.utils")

    subdir_path = os.path.join(manual_dir,manual_subdir)
    file_list = os.listdir(subdir_path)
    english = False
    screen = False
    for file in file_list:
        if file.endswith("EN.pdf"):
            english = True
            pdf_name = file
        elif file.endswith("CH.pdf") or file.endswith("RU.pdf"):
            pdf_name = file

        if file == "screen.json":
            screen = True

    # Prefer reading tasks from the merged closeloop file created in the script directory.
    merged_tasks_path = os.path.join(current_dir, "task_4_closeloop.json")
    if not os.path.exists(merged_tasks_path):
        print(f"任务文件不存在: {merged_tasks_path}")
        return None
    tasks = []
    with open(merged_tasks_path, 'r', encoding='utf-8') as f:
        for item in json.load(f):
            if item['id'].startswith(manual_subdir):
                tasks.append(item)

    #pdf_path = os.path.join(manual_dir,manual_subdir,pdf_name)
    #pdf_images = pdf_to_images(pdf_path,f"./cache/{manual_subdir}")

    with open(f"./model/{manual_subdir[:3]}/gt_part.json", 'r', encoding='utf-8') as file:
        gt_parts = json.load(file)

    file_path = f"{current_dir}/model/{manual_subdir[:3]}/Aligned.usd"
    add_reference_to_stage(usd_path=file_path, prim_path="/World")
    # add world
    world = World(stage_units_in_meters=1.0)
    cur_stage=omni.usd.get_context().get_stage()
    dome_light= UsdLux.DomeLight.Define(cur_stage,"/World/DemoLight")
    dome_light.CreateIntensityAttr().Set(500.0)

    world.reset()

    camera_prim_path = "/World/Camera"
    camera = Camera(camera_prim_path,resolution=(1920,1080),frequency=30)
    camera.initialize()
    screen_file = set_camera(screen,manual_subdir,camera,cur_stage)

    articulation_prim = Articulation('/World')
    button_contact = {}
    for item in gt_parts.keys():
        button_contact[gt_parts[item]] = False

    reset_needed = True
    task_count = 0
    step_count = 0
    
    result_dict[manual_subdir] = {"total_tasks": [], "success_rate": []}

    while simulation_app.is_running():
        if reset_needed:
            if task_count >= len(tasks):
                return
            world.reset()
            model = utils.init_model(articulation_prim,screen_file)
            world.reset()
            task = tasks[task_count]
            task_prompt = task["conversations"][0]['value']
            history = task['history']
            conduct_history = task['conduct']
            replanning = task['gt_planning']
            gt_steps = task["conversations"][1]['value']
            result_dict[manual_subdir]["total_tasks"].append(task_prompt)
            task_count = task_count + 1
            step_count = 0
            current_steps = 0
            success_length = 0
            counter = 0
            retry = 0
            sum_step = 0
            skip = False
            reset_needed = False
            new_log = {'task_prompt':task_prompt,"gt_plan":[],"predict":[]}
            new_log["gt_plan"] = gt_steps
        if(step_count == 0):
            for next_predict in conduct_history:
                for i in range(20):
                    world.step(render=True)
                    button_contact = conduct_step(articulation_prim,gt_parts,counter,next_predict,button_contact)
                    utils.auto_check(model,articulation_prim,cur_stage,button_contact)

        step_count += 1
        world.step(render=True)

        if counter == 0:
            if current_steps == len(gt_steps):
                new_log['result'] = success_length/len(gt_steps)
                save_log(out_dir,log,new_log,len(gt_steps),success_length,result_dict,manual_subdir)
                reset_needed = True
                continue
            if not skip:
                img_name = f"cache_gpt.png"
                img_array = camera.get_rgb()
                img_rgba = Image.fromarray(img_array, 'RGB')
                img_rgba.save(img_name)

                next_predict = next_step(history,img_name,task_prompt,replanning,llm)
                print(next_predict)
                history.append(next_predict)
                new_log["predict"].append(next_predict)
            else:
                skip = False

            gt_step = gt_steps[current_steps]
            if "press" in gt_step:
                gt_ins = gt_step.replace("press","")
                gt_ins = gt_ins.replace("(","")
                gt_ins = gt_ins.replace(")","")
                gt_part_name,_,gt_times = gt_ins.split(",")
                gt_part_name = gt_part_name.strip().lower()
                gt_times = re.sub(r'\D', '', gt_times)
                gt_times = int(gt_times)
                ins = next_predict.replace("press","")
                ins = ins.replace("(","")
                ins = ins.replace(")","")
                part_name = ins.split(",")[0]
                part_name = part_name.strip().lower()
                if gt_part_name not in gt_parts.keys():
                    if next_predict.lower() == gt_step.lower():
                        print("Planning Success")
                        success_length = success_length+1
                        current_steps = current_steps+1
                    else:
                        print("Mistake on Planning")
                        new_log['result'] = success_length/len(gt_steps)
                        save_log(out_dir,log,new_log,len(gt_steps),success_length,result_dict,manual_subdir)
                        reset_needed = True
                        continue
                else:
                    if part_name != gt_part_name or retry == 10:
                        if utils.evaluation(gt_parts[gt_part_name],gt_times,sum_step):
                            print(gt_times,sum_step)
                            print("Press Planning Success")
                            success_length = success_length+1
                            current_steps = current_steps+1
                            retry = 0
                            sum_step = 0
                            skip = True
                        else:
                            print("Mistake on Press Planning")
                            new_log['result'] = success_length/len(gt_steps)
                            save_log(out_dir,log,new_log,len(gt_steps),success_length,result_dict,manual_subdir)
                            reset_needed = True
                            continue
                    else:
                        if len(ins.split(",")) < 3:
                            new_log['result'] = success_length/len(gt_steps)
                            save_log(out_dir,log,new_log,len(gt_steps),success_length,result_dict,manual_subdir)
                            reset_needed = True
                            continue
                        times = ins.split(",")[2]
                        times = re.sub(r'\D', '', times)
                        if times == '':
                            new_log['result'] = success_length/len(gt_steps)
                            save_log(out_dir,log,new_log,len(gt_steps),success_length,result_dict,manual_subdir)
                            reset_needed = True
                            continue
                        times = int(times)
                        sum_step = sum_step+times
                        retry = retry+1
            elif "rotate" in gt_step:
                gt_ins = gt_step.replace("rotate","")
                gt_ins = gt_ins.replace("(","")
                gt_ins = gt_ins.replace(")","")
                gt_part_name,_,gt_degrees = gt_ins.split(",")
                gt_part_name = gt_part_name.strip().lower()
                gt_degrees = re.sub(r'\D', '', gt_degrees)
                gt_degrees = int(gt_degrees)
                ins = next_predict.replace("rotate","")
                ins = ins.replace("(","")
                ins = ins.replace(")","")
                part_name = ins.split(",")[0]
                part_name = part_name.strip().lower()
                if part_name != gt_part_name or retry == 10:
                    if sum_step == gt_degrees:
                        print("Rotate Planning Success")
                        success_length = success_length+1
                        current_steps = current_steps+1
                        retry = 0
                        sum_step = 0
                        skip = True
                    else:
                        print("Mistake on Rotate Planning")
                        new_log['result'] = success_length/len(gt_steps)
                        save_log(out_dir,log,new_log,len(gt_steps),success_length,result_dict,manual_subdir)
                        reset_needed = True
                        continue
                else:
                    if len(ins.split(",")) < 3:
                        new_log['result'] = success_length/len(gt_steps)
                        save_log(out_dir,log,new_log,len(gt_steps),success_length,result_dict,manual_subdir)
                        reset_needed = True
                        continue
                    degrees = ins.split(",")[2]
                    degrees = re.sub(r'\D', '', degrees)
                    if degrees == '':
                        new_log['result'] = success_length/len(gt_steps)
                        save_log(out_dir,log,new_log,len(gt_steps),success_length,result_dict,manual_subdir)
                        reset_needed = True
                        continue
                    degrees = int(degrees)
                    sum_step = sum_step+degrees
                    retry = retry+1
            else:
                if next_predict.lower() == gt_step.lower():
                    print("Planning Success")
                    success_length = success_length+1
                    current_steps = current_steps+1
                else:
                    print("Mistake on Planning")
                    new_log['result'] = success_length/len(gt_steps)
                    save_log(out_dir,log,new_log,len(gt_steps),success_length,result_dict,manual_subdir)
                    reset_needed = True
                    continue
        if not skip:
            button_contact = conduct_step(articulation_prim,gt_parts,counter,next_predict,button_contact)
            utils.auto_check(model,articulation_prim,cur_stage,button_contact)
            counter= counter+1

        if counter == 60:
            counter = 0
    
if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('--manual_id', default='006', type=str)
    parser.add_argument('--llm_model',default='gpt-5-mini', type=str)
    args = parser.parse_args()
    manual_dir = "./manuals_pdfs"
    manual_subdirs = os.listdir(manual_dir)
    manual_subdirs = [subdir for subdir in manual_subdirs if "." not in subdir]

    if os.path.exists(f"./benchmark_closeloop_{args.llm_model}.json"):
        with open(f"./benchmark_closeloop_{args.llm_model}.json", 'r', encoding='utf-8') as file:
            result_dict = json.load(file)
    else:
        result_dict = {}

    out_dir = f"./result/{args.llm_model}_closeloop/"
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
        
    manual_subdir = ""
    for subdir in manual_subdirs:
        if args.manual_id in subdir:
            manual_subdir = subdir
            break
    if manual_subdirs == "":
        print("!ERROR No manual directory as ",args.manual_id)
        exit()

    if os.path.join(manual_subdir) in result_dict.keys(): 
        exit()
        #pass
    
    out_dir = f"./result/{args.llm_model}_closeloop/{manual_subdir}"
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    result_dict = benchmark(manual_dir,manual_subdir, result_dict,out_dir,args.llm_model)

    simulation_app.close()