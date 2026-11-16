from pathlib import Path
import sys,json
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from common.cad import yubi_shapes,triangulate
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
D=Path(__file__).resolve().parent;shapes=yubi_shapes();rows=[]
fig,axs=plt.subplots(2,2,figsize=(14,14))
for ax,idx,dims in [(axs[0,0],16,(0,2)),(axs[0,1],16,(1,2)),(axs[1,0],2,(0,2)),(axs[1,1],16,(0,1))]:
 s=shapes[idx];v,f=triangulate(s);v*=1000
 ax.add_collection(PolyCollection(v[f][:,:,dims],facecolor='lightgrey',edgecolor='grey',lw=.08))
 for i,face in enumerate(s.Faces()):
  c=np.array(face.Center().toTuple());area=face.Area()
  if area<30 and (idx==2 and i<15 or idx==16 and (c[2]<960 or c[0]<-42)):
   ax.text(c[dims[0]],c[dims[1]],str(i),fontsize=6,color='red')
 ax.autoscale();ax.set_aspect('equal');ax.set_title(f'Occurrence{idx}, axes{dims} / mm')
fig.tight_layout();fig.savefig(D/'results/saddle_sections.png',dpi=150)
for i,face in enumerate(shapes[16].Faces()):
 b=face.BoundingBox();c=face.Center().toTuple()
 if c[2]<960 and face.Area()<50:rows.append(dict(face=i,area_mm2=face.Area(),center_mm=c,bounds_mm=[b.xmin,b.ymin,b.zmin,b.xmax,b.ymax,b.zmax],vertices_mm=[p.toTuple() for p in face.Vertices()]))
(D/'results/saddle_candidate_faces.json').write_text(json.dumps(rows,indent=2)+'\n')
print('Extracted',len(rows),'small faces at rear of original holder; render saddle_sections.png')

# Numerically check the candidate channel, without claiming an installed-band path.
import cadquery as cq
p=np.array([-37.540496996,5.13831255,954.5]);probe=[]
for dx in [0,-1,1]:
 vv=cq.Vector(*(p+[dx,0,0]));probe.append(dict(point_mm=vv.toTuple(),inside_material=shapes[16].isInside(vv,.00001),distance_to_material_mm=shapes[16].distance(cq.Vertex.makeVertex(*vv.toTuple()))))
(D/'results/SADDLE_OCCUPANCY_PROBES.json').write_text(json.dumps(dict(probes=probe,interpretation='Proposed band-centre point is in/on source material. This rejects that centreline proposal; exact saddle role/route remains unresolved.'),indent=2)+'\n')
