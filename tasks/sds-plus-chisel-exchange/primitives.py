"""Original compound primitive authoring; all geometry is in metres."""
import math
STEEL=[.48,.5,.52]
def quat(axis, angle):
    return [*(v*math.sin(angle/2) for v in axis), math.cos(angle/2)]


def box(pos, size, color=STEEL, q=None):
    return dict(kind='box', pos=pos, size=size, quat=q or [0,0,0,1], color=color)


def cylinder(pos, radius, height, color=STEEL, q=None):
    return dict(kind='cylinder', pos=pos, radius=radius, height=height,
                quat=q or [0,0,0,1], color=color)


def ring(inner, outer, height, z=0., count=64, color=STEEL):
    # Tangential prisms give a through-hole, not an invisible solid cylinder.
    radius=(inner+outer)/2
    width=2*outer*math.tan(math.pi/count)
    return [box([radius*math.cos(a),radius*math.sin(a),z],
                [outer-inner,width,height],color,quat([0,0,1],a))
            for a in [2*math.pi*i/count for i in range(count)]]


def body(name, pos, shapes, mass, fixed=False):
    from motion import rotate
    low=[float('inf')]*3; high=[-float('inf')]*3
    for shape in shapes:
        half=[v/2 for v in shape['size']] if shape['kind'] in ('box','convex') else [shape['radius']]*3 if shape['kind']=='sphere' else [shape['radius']]*2+[shape['height']/2]
        for i in (-1,1):
            for j in (-1,1):
                for k in (-1,1):
                    point=rotate(shape['quat'],[half[0]*i,half[1]*j,half[2]*k])
                    for axis in range(3):
                        value=point[axis]+shape['pos'][axis]
                        low[axis]=min(low[axis],value);high[axis]=max(high[axis],value)
    from mass_properties import compound
    for shape in shapes:shape.setdefault('mass_density',2700.)
    values=compound(shapes,mass)
    return dict(name=name,pos=pos,quat=[0,0,0,1],mass=mass,shapes=shapes,
                bounds_min=low,bounds_max=high,anchor=fixed,**values)


def assembly(b, fixed=False):
    return dict(name=b['name']+'_asset',origin=b['pos'],fixed=fixed,bodies=[b],joints=[])
