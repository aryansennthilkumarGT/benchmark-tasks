"""Externally meaningful local coupon score. No case name/installed flag input.
This score does NOT grade full assembly, axial retention or electrical function.
"""
import numpy as np

def physical_score(observations,ring_nodes,specification):
    shifts=np.array([r['foot_shift_mm'] for r in observations])
    b=shifts[0];moves=np.linalg.norm(shifts[1::2]-b,axis=1)
    returns=np.linalg.norm(shifts[2::2]-b,axis=1)
    q=np.array(ring_nodes)
    centers=np.mean(q,axis=1)-shifts[-1] if len(q) else np.empty((0,2))
    radii=np.linalg.norm(centers,axis=1)
    measured=dict(
        twelve_source_size_elements=(len(q)==12 and specification['tube_OD_mm']==6 and
                                    specification['tube_ID_mm']==4 and specification['tube_length_mm']==3),
        all_in_contact_band=bool(len(q) and np.all((radii>7.5)&(radii<11.5))),
        own_weight_centering=bool(np.linalg.norm(b)<.3),
        finite_reversible_travel=bool(len(moves) and np.all((moves>.1)&(moves<1.3))),
        passive_return=bool(len(returns) and np.all(returns<.1)),
        moves_mm=moves.tolist(),return_errors_mm=returns.tolist())
    measured['score']=float(all(v for k,v in measured.items() if k not in ['moves_mm','return_errors_mm']))
    return measured


def numerical_audit(observations):
    checks=dict(
        equilibrium_resolved=all(r['converged'] and r['gradient_residual_N']<.002 for r in observations),
        contact_resolved=all(r['max_contact_penetration_mm']<.05 for r in observations),
        no_numerical_stop=all(not r['numerical_domain_hit'] and not r['ring_node_domain_hit'] for r in observations))
    checks['passed']=all(checks.values())
    return checks
