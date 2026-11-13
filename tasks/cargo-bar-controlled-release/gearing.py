"""Original contact geometry: authored involute rack/pinion and ratchet teeth.

These parameters are benchmark design values, never measured OEM gear data.
The approximation uses overlapping radial/axial slices on one rigid body.
No joint motor, per-stroke update or virtual rack advancement is implemented.
"""
import math
from primitives import box,cylinder,quat

STEEL=[.48,.50,.52]
PITCH=.004
TEETH=20
PRESSURE=math.radians(20)
RADIUS=PITCH*TEETH/(2*math.pi)
MODULE=PITCH/math.pi
WIDTH=.014


def involute(angle):return math.tan(angle)-angle


def pinion(width=WIDTH,slices=20,phase=0.):
    """Axis X; individual convex teeth replace nonphysical staircase flanks."""
    from convex_primitives import prism_x
    base=RADIUS*math.cos(PRESSURE);root=RADIUS-1.25*MODULE;tip=RADIUS+MODULE
    shapes=[cylinder([0,0,0],root,width,STEEL,quat([0,1,0],math.pi/2))]
    points=[]
    for sign in (-1,1):
        for j in range(slices+1):
            r=root+(tip-root)*j/slices;alpha=math.acos(min(1.,base/r))
            half=(math.pi/(2*TEETH)+involute(PRESSURE)-involute(alpha))*.95
            points.append([sign*r*math.sin(half),r*math.cos(half)])
    for i in range(TEETH):
        angle=2*math.pi*i/TEETH+phase
        shapes.append(prism_x(points,width,q=quat([1,0,0],-angle)))
    return shapes


def rack(length=.100,pitch_plane=0.,phase=0.,width=WIDTH,slices=16):
    """Axis Y, exact trapezoidal flanks facing the pinion below the rack."""
    from convex_primitives import prism_x
    bottom=pitch_plane+1.25*MODULE;top=pitch_plane-MODULE
    shapes=[box([0,length/2,bottom+.002],[width,length,.004],STEEL)]
    topwidth=(PITCH/2+2*(top-pitch_plane)*math.tan(PRESSURE))*.95
    rootwidth=(PITCH/2+2*(bottom-pitch_plane)*math.tan(PRESSURE))*.95
    points=[[-topwidth/2,top],[topwidth/2,top],[rootwidth/2,bottom],[-rootwidth/2,bottom]]
    for i in range(math.ceil(length/PITCH)):
        shapes.append(prism_x(points,width,pos=[0,i*PITCH+phase,0]))
    return shapes


def ratchet_wheel(teeth=24,root=.017,tip=.020,width=.014,slices=12):
    """Axis X, convex radial locking faces and sloped return faces."""
    from convex_primitives import prism_x
    shapes=[cylinder([0,0,0],root,width,STEEL,quat([0,1,0],math.pi/2))]
    period=2*math.pi/teeth
    points=[[0,root],[0,tip],[root*math.sin(.70*period),root*math.cos(.70*period)]]
    for i in range(teeth):shapes.append(prism_x(points,width,q=quat([1,0,0],-i*period)))
    return shapes
