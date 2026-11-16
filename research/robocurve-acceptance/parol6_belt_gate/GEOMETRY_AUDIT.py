"""CPU component measurements only; no assembled drive, belt dynamics or access pass.

Reads immutable publisher Git objects, measures their native STLs, and refuses
YAM access evaluation while the genuine installed axial stack is unavailable.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import struct
import subprocess
import sys

import numpy as np
from scipy.signal import find_peaks

HARDWARE_PIN='e2169c163244d647739cc34fc5da15c24b042a61'
DESCRIPTION_PIN='340171f3a5d5d2c751cb6f2a4fdef6467d301170'
HERE=Path(__file__).resolve().parent


def git_bytes(repo,pin,path):
    return subprocess.check_output(['git','-C',str(repo),'show',pin+':'+path])


def stl(data):
    n=struct.unpack_from('<I',data,80)[0] if len(data)>=84 else 0
    if len(data)==84+50*n:
        dtype=np.dtype([('normal','<f4',3),('v','<f4',(3,3)),('attr','<u2')])
        return np.frombuffer(data,offset=84,dtype=dtype,count=n)['v'].astype(float)
    v=np.array(re.findall(rb'vertex\s+([-+\deE.]+)\s+([-+\deE.]+)\s+([-+\deE.]+)',data),float)
    assert len(v)%3==0 and len(v)>0
    return v.reshape(-1,3,3)


def circle(vertices,seed,radius):
    """Seed selects a cylindrical surface; least squares independently refits XY.

    Seed/radius are feature-identification hypotheses, not source dimensions.
    Small residual and axial extent describe the actual selected source vertices.
    """
    xy=np.unique(vertices[np.abs(np.linalg.norm(vertices[:,:2]-seed,axis=1)-radius)<1e-4,:2],axis=0)
    assert len(xy)>30
    A=np.c_[2*xy,np.ones(len(xy))];b=(xy*xy).sum(1)
    x=np.linalg.lstsq(A,b,rcond=None)[0];c=x[:2];r=np.sqrt(x[2]+c@c)
    residual=np.linalg.norm(xy-c,axis=1)-r
    selected=vertices[np.abs(np.linalg.norm(vertices[:,:2]-c,axis=1)-r)<1e-4]
    return dict(center_xy_native=c.tolist(),radius_native=float(r),sample_xy_points=len(xy),
                rms_radial_error_native=float(np.sqrt(np.mean(residual**2))),
                max_radial_error_native=float(abs(residual).max()),
                selected_vertex_z_range_native=[float(selected[:,2].min()),float(selected[:,2].max())])


def radial_section(tri,z):
    points=[]
    for k in range(3):
        a,b=tri[:,k],tri[:,(k+1)%3]
        mask=((a[:,2]<z)&(b[:,2]>=z))|((b[:,2]<z)&(a[:,2]>=z))
        aa,bb=a[mask],b[mask];s=(z-aa[:,2])/(bb[:,2]-aa[:,2])
        points.append(aa[:,:2]+s[:,None]*(bb-aa)[:,:2])
    p=np.concatenate(points)-[22.5,22.5]
    r=np.linalg.norm(p,axis=1);a=np.arctan2(p[:,1],p[:,0]);n=4096
    bins=((a+np.pi)*n/(2*np.pi)).astype(int)%n;v=np.full(n,-np.inf)
    np.maximum.at(v,bins,r);ix=np.flatnonzero(np.isfinite(v))
    envelope=np.interp(np.arange(n),np.r_[ix-n,ix,ix+n],np.r_[v[ix],v[ix],v[ix]])
    peaks=find_peaks(np.tile(envelope,3),prominence=.3,distance=60)[0]
    count=int(((peaks>=n)&(peaks<2*n)).sum())
    return dict(z_native=z,radial_peaks=count,outer_envelope_range_native=[float(envelope.min()),float(envelope.max())],
                method='triangle-plane intersection,4096 angular bins,periodic outer envelope; peak prominence0.3mm, separation60 bins')


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--hardware-repo',type=Path,required=True)
    p.add_argument('--description-repo',type=Path,required=True)
    p.add_argument('--output-dir',type=Path,required=True)
    args=p.parse_args();args.output_dir.mkdir(parents=True,exist_ok=True)
    paths=['STL/ELBOW/Elbow_part.STL','STL/ELBOW/Elbow_lid_1.STL','STL/ELBOW/Elbow_lid_2.STL',
           'STL/ELBOW/J4_bearing_backplate.STL','STL/ELBOW/J4_limiter.STL',
           'STL/FOREARM/J4_output_pulley.STL','STL/FOREARM/J5_part.STL','STL/FOREARM/HTD3_48_J5_pulley.STL']
    rows=[];meshes={}
    for path in paths:
        b=git_bytes(args.hardware_repo,HARDWARE_PIN,path);t=stl(b);v=t.reshape(-1,3);meshes[Path(path).name]=t
        rows.append(dict(path=path,pin=HARDWARE_PIN,sha256=hashlib.sha256(b).hexdigest(),triangles=len(t),
                         bounds_native=[v.min(0).tolist(),v.max(0).tolist()],dimensions_native=np.ptp(v,axis=0).tolist()))
    for name in ['L3.STL','L4.STL']:
        path='urdf/parol6_description/meshes/arm/'+name;b=git_bytes(args.description_repo,DESCRIPTION_PIN,path);t=stl(b);v=t.reshape(-1,3)
        rows.append(dict(path=path,pin=DESCRIPTION_PIN,sha256=hashlib.sha256(b).hexdigest(),triangles=len(t),
                         bounds_native=[v.min(0).tolist(),v.max(0).tolist()],dimensions_native=np.ptp(v,axis=0).tolist()))
    elbow=meshes['Elbow_part.STL'].reshape(-1,3)
    features={name:circle(elbow,np.array(c),r) for name,c,r in [
        ('bearing_seat',[28.54,73.54],23.55),('motor_pilot',[28.54,21.04],11.5),
        ('motor_mount_1',[13.04,5.54],1.6),('motor_mount_2',[44.04,5.54],1.6),
        ('motor_mount_3',[13.04,36.54],1.6),('motor_mount_4',[44.04,36.54],1.6),
        ('candidate_tension_hole_left',[11.24,44.54],1.4),('candidate_tension_hole_right',[45.84,44.54],1.4) ]}
    C=float(np.linalg.norm(np.array(features['bearing_seat']['center_xy_native'])-features['motor_pilot']['center_xy_native']))
    sections=[radial_section(meshes['J4_output_pulley.STL'],z) for z in [51,53,55,57]]
    assert all(x['radial_peaks']==48 for x in sections)
    R=48*3/(2*np.pi);r=12*3/(2*np.pi);d=R-r
    length=float(2*np.sqrt(C*C-d*d)+np.pi*(R+r)+2*d*np.arcsin(d/C))
    sys.path.insert(0,str(HERE.parent/'preflight'))
    from access_core import Robot
    robot=Robot()
    guard=dict(status='NOT_RUN_MISSING_REGISTERED_J4_AXIAL_STACK',hulls_available_per_arm=len(robot.hulls),
        existing_bundle_sha256=robot.bundle_sha256,
        missing_input='One dimensioned J4 installation-stage axial-section/assembly record registering the commercial12T pulley/hub/flanges and motor shaft to the printed output pulley and elbow,including whether the motor pulley remains axially loose during loop fitting.',
        deliberately_absent=['invented pulley flange/hub dimensions','arbitrary axial pulley placement','cable-free route','guessed TCP/contact targets','insertion-path or grip-force claim'])
    result=dict(source_hardware_pin=HARDWARE_PIN,description_pin=DESCRIPTION_PIN,components=rows,features=features,
        units=dict(print_stl='unitless format; millimetres corroborated by actual NEMA mounting pattern and1000:1 exterior-dimension agreement with metre URDF meshes',
                   description_stl='metres in SI URDF; not a second mm-scale print mesh'),
        fitted_parallel_bore_center_distance_mm=C,printed_output_sections=sections,
        pitch_analysis=dict(assumptions='BOM HTD3 interpreted as3mm pitch,12T motor pulley, measured48-period printed pulley; inextensible ideal pitch line, no idlers, no flanges, no tooth contact or backing thickness',
                           large_pitch_radius_mm=float(R),small_pitch_radius_mm=float(r),ideal_two_pulley_pitch_length_mm=length,
                           nominal_belt_pitch_length_mm=201,nominal_length_minus_ideal_mm=201-length,
                           small_pulley_wrap_degrees=float(np.rad2deg(np.pi-2*np.arcsin(d/C)))),
        access_input_gate=guard,scope='Component/cross-section evidence and necessary nominal pitch geometry only. No assembled-route, elastic-belt or YAM access pass.')
    (args.output_dir/'COMPONENT_GEOMETRY.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(center_distance_mm=C,section_peak_counts=[x['radial_peaks'] for x in sections],ideal_pitch_length_mm=length,nominal_pitch_length_excess_mm=201-length,access=guard['status'],hulls=len(robot.hulls)),indent=2))

if __name__=='__main__':main()
