"""Contact-only planar source-pocket/silicone centering coupon; not full assembly."""
from pathlib import Path
import sys,json
sys.path.insert(0,'/workspace/robocurve-cpu-deps')
import numpy as np
from shapely.geometry import shape
from elastic_ring import Ring,Field,solve
D=Path(__file__).resolve().parent

def fields(x=2.123):
    row=next(r for r in json.loads((D/'results/SECTIONS.json').read_text()) if r['x_mm']==x)
    return Field(shape(row['foot'])),Field(shape(row['fixed']))

def initial(rings):
    a=np.arange(len(rings))*np.pi/3
    centers=9.5*np.c_[np.cos(a),np.sin(a)]
    return np.array([r.circle(c) for r,c in zip(rings,centers)])

def main():
    foot,fixed=fields();rings=[Ring() for _ in range(6)]
    qs=initial(rings)
    # A finite-difference check independently verifies the nonlinear beam gradient.
    r=rings[0];q=qs[0].copy();q[3]+=[.07,-.1];en,g=r.energy(q);eps=1e-6
    check=[]
    for i,j in [(3,0),(3,1),(4,0),(2,1)]:
        z=q.copy();z[i,j]+=eps;hi=r.energy(z)[0];z[i,j]-=2*eps;lo=r.energy(z)[0]
        check.append(abs((hi-lo)/(2*eps)-g[i,j]))
    assert max(check)<1e-5
    rows=[]
    for z in [0,.2,.4,.8,.4,0,-.4,0]:
        qs,o=solve(rings,qs,foot,fixed,shift=(0,z))
        o.update(foot_shift_mm=[0,z],ring_centers_mm=np.mean(qs,axis=1).tolist())
        rows.append(o);print(z,o,flush=True)
    np.save(D.parent/'debug/DEFORMED_RING_NODES.npy',qs)
    out=dict(scope='Single source section; six free elastic ring cross-sections. No axial capture, full 12-element assembly or optical circuit validation.',section_x_mm=2.123,beam_gradient_error_N=max(check),cases=rows)
    (D.parent/'debug/CONTACT_TRIAL.json').write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
