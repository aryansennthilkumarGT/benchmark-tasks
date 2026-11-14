import subprocess,xml.etree.ElementTree as ET,struct,numpy as np,json,hashlib,pathlib
repo='/workspace/yam-verification-source';pin='0059d02a1a91bc6834c1d0846022891df0c78730';root=pathlib.Path('/workspace/final-two-evidence')
def show(p):return subprocess.check_output(['git','-C',repo,'show',pin+':'+p])
def trans(origin):
 xyz=list(map(float,origin.attrib.get('xyz','0 0 0').split()));r,p,y=map(float,origin.attrib.get('rpy','0 0 0').split());cx,sx=np.cos(r),np.sin(r);cy,sy=np.cos(p),np.sin(p);cz,sz=np.cos(y),np.sin(y)
 rx=np.array([[1,0,0],[0,cx,-sx],[0,sx,cx]]);ry=np.array([[cy,0,sy],[0,1,0],[-sy,0,cy]]);rz=np.array([[cz,-sz,0],[sz,cz,0],[0,0,1]])
 m=np.eye(4);m[:3,:3]=rz@ry@rx;m[:3,3]=xyz;return m
urdf=show('yam_arena/assets/yam/yam.urdf');tree=ET.fromstring(urdf);rows=[]
for name in ['tip_left','tip_right']:
 link=tree.find("link[@name='%s']"%name);vis=link.find('visual');mesh=vis.find('geometry/mesh');path='yam_arena/assets/yam/'+mesh.attrib['filename'];b=show(path);n=struct.unpack_from('<I',b,80)[0];assert len(b)==84+50*n
 pts=[]
 for i in range(n):pts.extend(np.array(struct.unpack_from('<12fH',b,84+50*i)[3:12]).reshape(3,3))
 pts=np.array(pts);j=next(j for j in tree.findall('joint') if j.find('child').attrib['link']==name);m=trans(j.find('origin'))@trans(vis.find('origin'));pts=(np.c_[pts,np.ones(len(pts))]@m.T)[:,:3]-np.array([0,0,.134])
 rows.append({'link':name,'joint_position_m':0,'mesh_path':path,'mesh_sha256':hashlib.sha256(b).hexdigest(),'min_relative_TCP_mm':(pts.min(axis=0)*1000).round(3).tolist(),'max_relative_TCP_mm':(pts.max(axis=0)*1000).round(3).tolist(),'axis_extents_mm':(np.ptp(pts,axis=0)*1000).round(3).tolist()})
d={'pin':pin,'method':'Binary visual STL vertices transformed by URDF visual then closed finger-joint origin, in gripper frame minus TCP offset. Static envelope only; no robot or task was instantiated.','urdf_sha256':hashlib.sha256(urdf).hexdigest(),'fingers':rows,'limitation':'Visual CAD bounds are not measured pad contact surfaces or final imported collision hulls. Full palm/wrist and open/regrasp swept paths still required.'}
(root/'stock-finger-static-envelope.json').write_text(json.dumps(d,indent=2)+'\n');print(json.dumps(d,indent=2))
