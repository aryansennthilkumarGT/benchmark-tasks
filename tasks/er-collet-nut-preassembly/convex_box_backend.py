"""Exact convex-box export and independent overlap for supplemental CPU diagnostics.

Not an Isaac backend or robot controller. The original primitive corner sets,
poses and scalar parameters remain unchanged.
"""
import itertools,xml.etree.ElementTree as ET
import mujoco,numpy as np

def geometric_overlap(model,data,body):
 # Independent OBB minimum-overlap SAT from the actual exported world geoms.
 # MuJoCo contact.dist is a solver manifold quantity and can be a very different
 # number for deeply crossing thin compound boxes. Keep both metrics visible.
 ids=np.flatnonzero((model.geom_type==mujoco.mjtGeom.mjGEOM_BOX)|(model.geom_type==mujoco.mjtGeom.mjGEOM_MESH))
 left=ids[model.geom_bodyid[ids]==body];right=ids[model.geom_bodyid[ids]!=body]
 center=data.geom_xpos;rotation=data.geom_xmat.reshape(-1,3,3);half=model.geom_size
 extent=np.einsum('nij,nj->ni',np.abs(rotation),half)
 lo=center-extent;hi=center+extent
 i,j=np.nonzero(np.all(hi[left,None,:]>lo[right],axis=2)&np.all(lo[left,None,:]<hi[right],axis=2))
 if not len(i):return 0.
 li=left[i];ri=right[j];A=rotation[li].transpose(0,2,1);B=rotation[ri].transpose(0,2,1)
 cross=np.cross(A[:,:,None,:],B[:,None,:,:]).reshape(-1,9,3);length=np.linalg.norm(cross,axis=2);valid=length>1e-8
 cross/=np.where(valid,length,1)[:,:,None];axes=np.concatenate((A,B,cross),axis=1)
 ra=(np.abs(axes@A.transpose(0,2,1))*half[li,None,:]).sum(axis=2)
 rb=(np.abs(axes@B.transpose(0,2,1))*half[ri,None,:]).sum(axis=2)
 gaps=np.abs(np.einsum('nki,ni->nk',axes,center[ri]-center[li]))-ra-rb
 gaps[:,6:]=np.where(valid,gaps[:,6:],-np.inf)
 return float(np.maximum(0,-gaps.max(axis=1)).max())


def mesh_boxes(xml):
 """Exact eight-corner convex equivalents avoid an observed box-box contact bug.

 No geometry is rounded, enlarged or disabled. All cube hulls retain original
 local transforms. MuJoCo's convex mesh backend replaces its primitive box-box
 routine; PhysX assets remain unchanged. This is an alternate-engine setting.
 """
 assets=ET.SubElement(xml,'asset')
 for geom in xml.findall('.//worldbody//geom'):
  if geom.get('type')!='box':continue
  half=np.fromstring(geom.attrib.pop('size'),sep=' ');name='mesh_'+geom.get('name')
  vertices=np.array(list(itertools.product(*[(-v,v) for v in half])))
  ET.SubElement(assets,'mesh',name=name,vertex=' '.join(format(float(v),'.17g') for v in vertices.ravel()))
  geom.set('type','mesh');geom.set('mesh',name)
 return xml


