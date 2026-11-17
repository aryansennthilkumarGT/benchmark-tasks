"""Geometrically nonlinear, free planar curved beam for a 6/4 x 3 mm tube.
Units: mm, N, MPa=N/mm². No node is attached to a target or rigid part.
Finite wall thickness has node/rigid and nonadjacent node self-contact.
This is a thin-wall beam approximation, NOT a calibrated 3-D silicone model.
"""
import numpy as np
from scipy.optimize import minimize

class Ring:
    def __init__(self, n=32, modulus=1.0):
        self.n=n;self.radius=2.5;self.thickness=1.;self.length=3.
        self.E=modulus;self.l0=2*self.radius*np.sin(np.pi/n)
        self.ks=modulus*self.length*self.thickness/self.l0
        self.kb=modulus*self.length*self.thickness**3/(12*self.l0)
        self.turn0=2*np.pi/n
        i,j=np.triu_indices(n,k=3);keep=(j-i)<n-2;self.i=i[keep];self.j=j[keep]
    def circle(self,center):
        a=np.arange(self.n)*2*np.pi/self.n
        return np.array(center)+self.radius*np.c_[np.cos(a),np.sin(a)]
    def energy(self,q):
        e=np.roll(q,-1,axis=0)-q;l=np.linalg.norm(e,axis=1);t=e/l[:,None]
        dl=l-self.l0;g=self.ks*dl[:,None]*t
        energy=.5*self.ks*np.sum(dl*dl)
        phi=np.arctan2(e[:,1],e[:,0]);turn=np.angle(np.exp(1j*(phi-np.roll(phi,1))))
        dt=turn-self.turn0;energy+=.5*self.kb*np.sum(dt*dt)
        dphi=self.kb*(dt-np.roll(dt,-1))
        g+=dphi[:,None]*np.c_[-e[:,1],e[:,0]]/(l*l)[:,None]
        grad=np.roll(g,1,axis=0)-g
        # A finite wall must not pass through the opposing wall during collapse.
        delta=q[self.i]-q[self.j];dist=np.linalg.norm(delta,axis=1)
        pen=np.minimum(dist-self.thickness,0);k=20.
        energy+=.5*k*np.sum(pen*pen)
        force=k*pen[:,None]*delta/np.maximum(dist[:,None],1e-9)
        np.add.at(grad,self.i,force);np.add.at(grad,self.j,-force)
        return float(energy),grad

class Field:
    """Cubic signed-distance regularization of unmodified section geometry."""
    def __init__(self,polygon,lo=-17.,hi=17.,spacing=.05):
        import shapely
        self.lo=lo;self.h=spacing
        self.axis=np.arange(lo,hi+spacing/2,spacing)
        y,z=np.meshgrid(self.axis,self.axis,indexing='ij')
        points=shapely.points(y,z)
        values=shapely.distance(points,polygon.boundary)
        values[shapely.contains_xy(polygon,y,z)]*=-1
        self.values=values
        from scipy.interpolate import RectBivariateSpline
        self.spline=RectBivariateSpline(self.axis,self.axis,values,kx=3,ky=3,s=0)
    def at(self,q):
        values=self.spline.ev(q[:,0],q[:,1])
        gradient=np.c_[self.spline.ev(q[:,0],q[:,1],dx=1),self.spline.ev(q[:,0],q[:,1],dy=1)]
        return values,gradient

def solve(rings,initial,foot,fixed,shift=(0,0),contact_k=20.,node_force=(0,0),
          maxiter=6000,free_foot=False,body_force=(0,0),foot_domain_mm=1.4,
          pin_clearance_mm=.4):
    """Free-ring/foot equilibrium. The real guide pin contacts its source slot.

    The slot cylinders are R.85 centered Y±.3; source pin R.75. At X=0,
    lateral center clearance is .3+.85-.75=.4mm. Beyond that gap a unilateral
    normal contact acts, rather than a joint limit/hold flag. Axial engagement
    of the source pin is an explicit preassembled-state assumption.
    Numerical domain limits only reject a trial; they never provide retention.
    """
    shift=np.array(shift,dtype=float);node_force=np.array(node_force)
    body_force=np.array(body_force);n=rings[0].n if rings else 32
    # Batch each original section field, retaining all free element coordinates.
    groups={}
    for i in range(len(rings)):
        f=foot[i] if isinstance(foot,list) else foot
        base=fixed[i] if isinstance(fixed,list) else fixed
        for field,moving in [(f,True),(base,False)]:
            key=(id(field),moving)
            if key not in groups:groups[key]=[field,moving,[]]
            groups[key][2].append(i)
    def fun(flat,details=False):
        qs=flat[:len(rings)*n*2].reshape(len(rings),n,2)
        displacement=flat[-2:] if free_foot else shift
        energy=-float(np.dot(body_force,displacement));grads=np.zeros_like(qs)
        force_foot=np.zeros(2);maxpen=0.
        for i,(r,q) in enumerate(zip(rings,qs)):
            E,g=r.energy(q);energy+=E-np.sum(q*node_force);grads[i]=g-node_force
        for field,moving,indices in groups.values():
            points=qs[indices].reshape(-1,2)
            val,normal=field.at(points-(displacement if moving else 0))
            pen=np.minimum(val-.5,0);energy+=.5*contact_k*np.sum(pen*pen)
            cg=contact_k*pen[:,None]*normal
            grads[indices]+=cg.reshape(len(indices),n,2)
            if moving:force_foot+=np.sum(cg,axis=0)
            maxpen=max(maxpen,float(-pen.min()))
        pinforce=0.;pinpen=0.
        if pin_clearance_mm is not None:
            pinpen=max(abs(float(displacement[0]))-pin_clearance_mm,0.)
            energy+=.5*contact_k*pinpen**2
            pinforce=-contact_k*pinpen*np.sign(displacement[0]);force_foot[0]+=pinforce
            maxpen=max(maxpen,pinpen)
        gradient=grads.ravel()
        if free_foot:gradient=np.r_[gradient,-force_foot-body_force]
        if details:return dict(energy_Nmm=float(energy),force_on_foot_N=force_foot.tolist(),
            pin_contact_force_N=float(pinforce),pin_contact_penetration_mm=float(pinpen),
            foot_shift_mm=displacement.tolist(),max_contact_penetration_mm=maxpen,
            gradient_residual_N=float(np.max(np.abs(gradient))) if len(gradient) else 0,
            numerical_domain_hit=bool(free_foot and np.max(np.abs(displacement))>foot_domain_mm-.001))
        return energy,gradient
    x0=np.array(initial).ravel();bounds=[(-16.5,16.5)]*len(x0)
    if free_foot:
        x0=np.r_[x0,shift];bounds=[(-16.5,16.5)]*(len(x0)-2)+[(-foot_domain_mm,foot_domain_mm)]*2
    result=minimize(fun,x0,jac=True,method='L-BFGS-B',bounds=bounds,
        options=dict(maxiter=maxiter,ftol=1e-15,gtol=2e-5,maxls=35,maxcor=20))
    detail=fun(result.x,True)
    detail['ring_node_domain_hit']=bool(len(rings) and np.max(np.abs(result.x[:len(rings)*n*2]))>16.499)
    detail.update(converged=bool(result.success),message=str(result.message),iterations=int(result.nit))
    return result.x[:len(rings)*n*2].reshape(len(rings),n,2),detail
