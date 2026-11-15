"""Run bounded CPU controls and assumption sweeps; writes all actual traces."""
import argparse
import csv
from dataclasses import replace, asdict
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import time
import sys
import numpy as np
import scipy
from mechanism import Coupon, Parameters

ROOT = Path(__file__).resolve().parent

def write_csv(path, rows):
    with path.open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator='\n')
        w.writeheader(); w.writerows(rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=ROOT/'results')
    args = parser.parse_args()
    out = args.output
    out.mkdir(parents=True, exist_ok=True)
    (out/'traces').mkdir(exist_ok=True)
    base = Parameters()
    cases = [
        ('correct', base, 'under', 0., .45, 'control'),
        ('nearby_not_engaged', base, 'under', 20., .45, 'control'),
        ('wrong_upper_surface', base, 'upper', 0., .45, 'control'),
        ('partial_extraction', base, 'under', 0., .20, 'control'),
        ('panel_moves_clip_captured', replace(base, head_carrier_stiffness=1.), 'under', 0., .45, 'control'),
        ('excessive_panel_load', replace(base, steps=320), 'under', 0., 1.20, 'control'),
        ('yielding_legs', replace(base, yield_strain=.012), 'under', 0., .45, 'control'),
    ]
    # These are hypotheses, NOT confidence intervals for any actual plastic part.
    sweeps = dict(modulus=[700.,2500.], leg_thickness=[.7,1.4],
                  flexure_length=[5.5,8.5], yield_strain=[.012,.025,.06],
                  friction=[0.,.1,.45,.6], peak_radius=[4.8,5.8],
                  hole_diameter=[8.6,9.4], sheet_thickness=[.6,1.5],
                  head_carrier_stiffness=[1.,30.,500.], panel_stiffness=[2.,20.],
                  root_height=[5.5,6.5])
    for field, values in sweeps.items():
        for value in values:
            cases.append((f'{field}_{value:g}', replace(base, **{field:value}), 'under', 0., .45, 'sensitivity'))
    # Interactions can fail even when isolated variations pass.
    cases += [
        ('combined_stiff_high_friction', replace(base, modulus=2500., leg_thickness=1.4, friction=.6), 'under', 0., .45, 'sensitivity'),
        ('combined_large_barb_small_hole', replace(base, peak_radius=5.8, hole_diameter=8.6, yield_strain=.025), 'under', 0., .45, 'sensitivity'),
        ('no_initial_retention', replace(base, hole_diameter=12.), 'under', 0., .45, 'control'),
    ]
    for field, values in dict(steps=[60,240,480], wall_samples=[24,96,192],
                              hole_penalty=[7500.,15000.,60000.,120000.], viscosity=[.002,.05],
                              friction_regularizer=[.00005,.0002]).items():
        for value in values:
            cases.append((f'numerical_{field}_{value:g}', replace(base, **{field:value}), 'under', 0., .45, 'numerical'))
    cases.append(('numerical_combined_fine', replace(base, steps=480, wall_samples=192, hole_penalty=120000.), 'under', 0., .45, 'numerical'))
    started = time.perf_counter()
    summaries, table = {}, []
    for name,p,pose,offset,angle,kind in cases:
        rows, s = Coupon(p,pose,offset).run(angle)
        s.update(name=name, kind=kind)
        summaries[name] = s
        write_csv(out/'traces'/f'{name}.csv', rows)
        f = s['final']
        table.append(dict(name=name, kind=kind, valid_success=s['valid_success'],
                          numerically_resolved=s['numerically_resolved'], contact_domain_ok=s['contact_domain_ok'],
                          retention_released=f['retention_released'],
                          damage=f['modeled_plastic_damage'], initial_captured=s['initial']['oversized_retaining_material_below_seat'],
                          panel_mm=f['panel_mm'], clip_mm=f['clip_mm'],
                          peak_tool_N=s['peak_tool_force_N'], peak_hole_normal_N=s['peak_hole_normal_N'],
                          peak_leg_mm=s['peak_leg_deflection_mm'],
                          panel_plastic_mm=f['panel_plastic_mm'], leg_plastic_mm=max(f['left_plastic_mm'],f['right_plastic_mm']),
                          peak_hole_overlap_mm=s['peak_hole_penetration_mm'], peak_tool_overclosure_mm=s['peak_tool_overclosure_mm'],
                          max_gradient_N=s['max_projected_gradient_N'], failed_steps=s['optimizer_failed_steps']))
        print(f"{name}: valid={s['valid_success']} released={f['retention_released']} damage={f['modeled_plastic_damage']} "
              f"panel={f['panel_mm']:.4f} clip={f['clip_mm']:.4f} tool_peak={s['peak_tool_force_N']:.3f}N "
              f"unresolved={s['nonstationary_steps']} failures={s['optimizer_failed_steps']}", flush=True)
    (out/'summary.json').write_text(json.dumps(summaries, indent=2)+'\n')
    write_csv(out/'summary.csv', table)
    manifest = dict(executed_utc=datetime.now(timezone.utc).isoformat(), python=sys.version, platform=platform.platform(), numpy=np.__version__, scipy=scipy.__version__,
                    cpu_only=True, experiment_count=len(cases), wall_seconds=time.perf_counter()-started,
                    default_parameters=asdict(base),
                    code_sha256={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in ['mechanism.py','run_experiments.py']})
    (out/'RUN_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')

if __name__ == '__main__':
    main()
