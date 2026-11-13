"""Render genuine stored observations with the official exporter; decode every output.

No annotations/identifying overlays are introduced. A contact sheet is saved for
review. Native camera-coverage checks are separate from pixel and codec checks.
"""
import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import numpy as np
from run_ledger import Incomplete, atomic, digest, execute, read
from validate_rollout import require, public_text


def video_check(ffmpeg, path, expected_frames, out):
    require(path.stat().st_size <= 50_000_000, 'Video exceeds 50 MB')
    result=subprocess.run([ffmpeg,'-hide_banner','-i',str(path),'-map','0:v:0','-f','null','-',
                           '-progress','pipe:1','-nostats'],capture_output=True,text=True,timeout=600)
    require(result.returncode==0,'Full video decode failed: '+result.stderr[-600:])
    require(re.search(r'Video: h264.*yuv420p',result.stderr),'Video must be H.264 yuv420p')
    frames=re.findall(r'^frame=(\d+)\s*$',result.stdout,re.M)
    require(frames and int(frames[-1])==expected_frames,'Decoded frame count differs from trajectory')
    (out/(path.stem+'-decode.log')).write_text(result.stderr+'\n'+result.stdout)
    return {'sha256':digest(path),'bytes':path.stat().st_size,'decoded_frames':int(frames[-1]),
            'codec':'h264','pixel_format':'yuv420p','full_decode':'PASS'}


def render(run, label, output, ffmpeg):
    from inspect_robots.frames import _parse_frame_filename
    frame_dir=Path(run['frames'])
    top=[]
    for path in frame_dir.glob('*.npy'):
        parsed=_parse_frame_filename(path.name)
        if parsed and parsed[1]=='top_cam':top.append((parsed[2],path))
    top.sort()
    require([step for step,_ in top]==list(range(run['steps']+1)),'Top camera is missing observations')
    # Use the documented official CLI, writing outside the immutable rollout directory.
    videos=output/(label+'-cameras')
    execute([str(Path(sys.executable).parent/'inspect-robots'),'video',run['log'],'--out',str(videos),
             '--ffmpeg',ffmpeg],output,output/(label+'-export.log'),900)
    candidates=[p for p in videos.glob('*.mp4') if '~top_cam' in p.name]
    require(len(candidates)==1,'Official exporter did not produce a unique top-camera video')
    target=output/(label+'.mp4');shutil.copyfile(candidates[0],target)
    # Per-frame checks cannot prove visual quality; they detect blank/truncated frames.
    sample_indices=sorted({0,len(top)//4,len(top)//2,3*len(top)//4,len(top)-1})
    samples=[]
    for i in sample_indices:
        frame=np.load(top[i][1],allow_pickle=False)
        require(frame.shape==(176,320,3) and frame.dtype==np.uint8,'Camera format mismatch')
        require(float(frame.std())>5 and np.unique(frame.reshape(-1,3),axis=0).shape[0]>100,
                'Blank or corrupt rendered view')
        samples.append(frame)
    import cv2
    require(cv2.imwrite(str(output/(label+'-contact-sheet.png')),cv2.cvtColor(np.concatenate(samples,axis=1),cv2.COLOR_RGB2BGR)),
            'Failed to write contact sheet')
    return video_check(ffmpeg,target,len(top),output),np.load(top[0][1],allow_pickle=False)


def main():
    p=argparse.ArgumentParser();p.add_argument('--inputs',type=Path,required=True)
    p.add_argument('--folder',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    args=p.parse_args();data=read(args.inputs);output=args.output.resolve();output.mkdir(parents=True,exist_ok=False)
    public_text(args.folder)
    import imageio_ffmpeg
    ffmpeg=imageio_ffmpeg.get_ffmpeg_exe()
    require(len(data['experts'])==2 and all(r['score']==1 for r in data['experts']),'Two validated expert rollouts required')
    require(len({r['record_id'] for r in data['experts']}|{data['dream']['record_id']})==3,'Reused rollout identity')
    media={}
    for name,run in [('demo',data['experts'][0]),('demo-repeat',data['experts'][1]),('model',data['dream'])]:
        result,initial=render(run,name,output,ffmpeg);media[name]=dict(result,record_id=run['record_id'],score=run['score'])
        if name=='demo':
            import cv2
            require(cv2.imwrite(str(output/'setup.png'),cv2.cvtColor(initial,cv2.COLOR_RGB2BGR)),'Screenshot write failed')
    screenshot=output/'setup.png'
    require(screenshot.stat().st_size<=10_000_000,'Screenshot exceeds 10 MB')
    # Native tests must project actual initial task geometry into the overhead image.
    # This report is attached to feasibility by the orchestrator, not a task's claim.
    require(data.get('camera_coverage') is True,'Native camera coverage was not verified')
    report={'status':'PASS','kind':'ACTUAL_ROLLOUT_MEDIA','files':media,
            'setup':{'sha256':digest(screenshot),'bytes':screenshot.stat().st_size},
            'blind_review':{'public_text_scan':'PASS','overlays_added':False,
                           'scene_assets':'Original primitive geometry; no imported identifying textures'},
            'visual_checks':['native projected geometry coverage','sampled nonblank frames','all frames decoded'],
            'human_visual_review':'NOT_PERFORMED_BY_THIS_SCRIPT; inspect contact sheets before official submission'}
    atomic(output/'media-validation.json',report)


if __name__=='__main__':main()
