"""Render the actual source jig BRep; display mesh is never collision evidence."""
import argparse
from pathlib import Path
import numpy as np
import cadquery as cq
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

p=argparse.ArgumentParser();p.add_argument('--source-dir',type=Path,required=True);p.add_argument('--output',type=Path,default=Path(__file__).resolve().parent/'results/JIG_CAD.png');a=p.parse_args()
s=cq.importers.importStep(str(a.source_dir/'OpenArm KER/OpenArm KER JIG BASE.STEP')).val()
v,t=s.tessellate(.3,.15);vertices=np.array([x.toTuple() for x in v]);tri=vertices[np.asarray(t)]
fig=plt.figure(figsize=(10,8));ax=fig.add_subplot(111,projection='3d')
ax.add_collection3d(Poly3DCollection(tri,facecolors='#a5b4bf',shade=True))
lo=vertices.min(0);hi=vertices.max(0)
ax.set(xlim=(lo[0],hi[0]),ylim=(lo[1],hi[1]),zlim=(lo[2],hi[2]),xlabel='native X (mm)',ylabel='native Y (mm)',zlabel='native Z (mm)')
ax.set_box_aspect(hi-lo);ax.view_init(35,-65)
fig.suptitle('Official 2.0.0 KER_JIG_BASE — native millimetres\nDisplay tessellation only; no robot/contact simulation')
fig.tight_layout();a.output.parent.mkdir(exist_ok=True,parents=True);fig.savefig(a.output,dpi=150)
print('Rendered source BRep:',len(tri),'display triangles;',a.output)
