"""CPU-only source-section contact equilibria with free deformable rings/foot.
Not a full foot assembly, insertion policy, dynamic return or axial capture model.
"""
from pathlib import Path
import sys,json,argparse
sys.path.insert(0,'/workspace/robocurve-cpu-deps')
import numpy as np
from shapely.geometry import shape
from elastic_ring import Ring,Field,solve
from contact_coupon import initial
from scoring import physical_score,numerical_audit
D=Path(__file__).resolve().parent
class NoContact:
    def at(self,q):return np.full(len(q),1000.),np.zeros_like(q)

def execute(case,fields,modulus=1.,full_cycle=False):
    count={'missing_all':0,'missing_one':11,'missing_bank':6}.get(case,12)
    modulus={'too_soft':.05,'stiff_wrong_material':100.}.get(case,modulus)
    rings=[Ring(modulus=modulus) for _ in range(count)]
    q=np.r_[initial([Ring()]*6),initial([Ring()]*6)][:count]
    if case=='misplaced_element':q[0]-=[9.5,0]  # genuine free central void, not a pocket
    spec=dict(tube_OD_mm=6,tube_ID_mm=4,tube_length_mm=3)
    if case=='wrong_size':
        for i,r in enumerate(rings):
            r.radius=2.;r.l0=2*r.radius*np.sin(np.pi/r.n)
            r.ks=r.E*r.length*r.thickness/r.l0;r.kb=r.E*r.length*r.thickness**3/(12*r.l0)
            q[i]=r.circle(np.mean(q[i],axis=0))
        spec.update(tube_OD_mm=5,tube_ID_mm=3)
    foot=[fields[0][0]]*min(count,6)+[fields[1][0]]*max(count-6,0)
    fixed=[fields[0][1]]*min(count,6)+[fields[1][1]]*max(count-6,0)
    if case=='missing_support_ring':fixed=[NoContact()]*count
    forces=[(0,0),(0,1),(0,0)]
    if full_cycle:forces += [(1,0),(0,0),(-1,0),(0,0)]
    shift=[0,0];rows=[];states=[]
    for force in forces:
        q,o=solve(rings,q,foot,fixed,shift=shift,free_foot=True,
            body_force=np.array(force)+[0,-.009*9.80665],
            node_force=[0,-.001*9.80665/(12*32)],
            pin_clearance_mm=None if case=='missing_support_ring' else .4)
        print(case,modulus,'load',force,'iterations',o['iterations'],'residual',o['gradient_residual_N'],flush=True)
        shift=o['foot_shift_mm'];o['probe_force_N']=list(force);rows.append(o);states.append(q.tolist())
    score=physical_score(rows,q,spec)
    out=dict(case=case,modulus_MPa=modulus,specification=spec,observations=rows,
             ring_nodes_by_stage_mm=states,physical_score=score,numerical_audit=numerical_audit(rows),
             experiment_pass=bool(score['score']==1 and numerical_audit(rows)['passed']))
    print(case,modulus,score,flush=True)
    return out

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--mode',choices=['controls','sensitivity'],default='controls');args=parser.parse_args()
    rows=json.loads((D/'results/SECTIONS.json').read_text());fields=[]
    for x in [2.123,-2.123]:
        row=next(r for r in rows if r['x_mm']==x)
        fields.append((Field(shape(row['foot'])),Field(shape(row['fixed']))))
    if args.mode=='controls':
        cases=['correct','missing_all','missing_one','missing_bank','misplaced_element','wrong_size','too_soft','stiff_wrong_material','missing_support_ring']
        out=[execute(case,fields,full_cycle=case=='correct') for case in cases]
    else:out=[execute('correct',fields,modulus=E) for E in [.5,2.]]
    (D/f'results/{args.mode.upper()}.json').write_text(json.dumps(out,indent=2)+'\n')
    if args.mode=='controls':
        assert out[0]['experiment_pass'],'Nominal source-section coupon FAILED'
        assert all(r['physical_score']['score']==0 for r in out[1:]),'False full positive'
    print('CPU',args.mode,'completed')
if __name__=='__main__':main()
