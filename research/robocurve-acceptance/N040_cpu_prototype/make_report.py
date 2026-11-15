"""Render tables and an explanatory plot from actual recorded runs; no simulation."""
import csv
import json
from pathlib import Path
import matplotlib.pyplot as plt
from mechanism import Coupon, Parameters
import numpy as np

ROOT=Path(__file__).resolve().parent
s=json.loads((ROOT/'results/summary.json').read_text())
base=s['correct']
lines=['# Parameter sensitivity — actual CPU results', '',
       '**Exploratory assumed-material study, not measured Hyundai uncertainty bounds.** All dimensions are mm, forces N. `valid` requires initial retention, resolved equilibrium, the numerical contact-domain checks, released/recovered retaining geometry and no modeled plastic set. It does not certify authentic clip fitment or YAM access.', '',
       'Each trace is in [results/traces](results/traces); complete inputs and diagnostics are in [summary.json](results/summary.json). `retention_released` is not complete stem withdrawal. All runs were executed on CPU; no empirical force curve was fitted.', '',
       '## Required controls', '',
       '| Run | Panel / clip final mm | Peak tool N | Released | Plastic damage | Domain valid | Valid success |',
       '|---|---:|---:|---|---|---|---|']
for n,x in s.items():
    if x['kind']!='control':continue
    f=x['final']
    lines.append(f"| {n} | {f['panel_mm']:.4f} / {f['clip_mm']:.4f} | {x['peak_tool_force_N']:.3f} | {f['retention_released']} | {f['modeled_plastic_damage']} | {x['contact_domain_ok']} | {x['valid_success']} |")
lines += ['', 'The nominal release ends with the stem still in the hole; only the oversized retaining shoulder is clear. Nearby tool contact is exactly zero. Wrong-face contact gives a large rigid-stop penalty reaction and 3.49 mm tool overclosure: it is **outside the model domain**, not a credible plastic-tool load prediction. Partial extraction retains an oversized shoulder below the seat. A soft carrier permits over 3 mm of panel motion with under 0.5 mm clip extraction. These observations defeat panel-motion and proximity shortcuts.', '',
          'Overdrive yields the assumed panel spring (48 N internal yield load), leaving permanent set. It is invalid even though all retaining geometry clears; that is a constitutive damage outcome, not a score-at-depth rule. Lower assumed leg yield strain also produces irreversible set. This does not establish which genuine clips are reusable.', '',
          '## Assumption sweep', '',
          'Baseline: E=1500 N/mm², t=1 mm, effective flexure L=7 mm, yield strain=0.04, friction=0.25, radius peak=5.3 mm, hole D=9 mm, sheet t=0.8 mm, carrier k=180 N/mm, panel k=8 N/mm, root height=6 mm. Changed values appear in each row name; all other parameters remain baseline except explicitly combined cases.', '',
          'These ranges are deliberate design hypotheses to expose failure, **not empirical tolerances or confidence intervals**. E=700–2500; leg t=0.7–1.4; L=5.5–8.5; yield strain=0.012–0.06; friction=0–0.6; peak radius=4.8–5.8; hole D=8.6–9.4; sheet t=0.6–1.5; carrier k=1–500; panel k=2–20; root height=5.5–6.5. No probability of success can be inferred.', '',
          '| Changed assumption | Peak tool N | Final clip mm | Max plastic set mm (leg / panel) | Released | Domain valid | Valid |',
          '|---|---:|---:|---:|---|---|---|']
for n,x in s.items():
    if x['kind']!='sensitivity':continue
    f=x['final']
    lines.append(f"| {n} | {x['peak_tool_force_N']:.3f} | {f['clip_mm']:.4f} | {max(f['left_plastic_mm'],f['right_plastic_mm']):.4f} / {f['panel_plastic_mm']:.4f} | {f['retention_released']} | {x['contact_domain_ok']} | {x['valid_success']} |")
lines += ['', 'Success is **property-dependent**. Low-yield legs damage; soft head coupling fails to extract the retainer despite panel travel. Large-barb cases can drive the one-mode leg radius negative; the domain guard rejects those runs. Their damage/force diagnostics are outside the admissible model and cannot support hardware conclusions. The high-stiffness/high-friction interaction raises force substantially even where release remains possible. No small isolated sweep validates all correlated material/shape combinations.', '',
          '## Numerical sensitivity, separate from material uncertainty', '',
          'All increment solves satisfy the reported projected-gradient stationarity criterion (<0.01 N) and optimizer success. That is local equilibrium of this reduced model, not global dynamic snap validation. L-BFGS-B follows warm-start local equilibria; inertia, rate effects and impact peaks are absent. Contact is midpoint quadrature with a sharp assumed shoulder. Peak force has not converged to a defensible hardware prediction.', '',
          '| Numerical change | Peak tool N | Max hole overlap mm | Max tool overclosure mm | Max projected gradient N | Release valid |',
          '|---|---:|---:|---:|---:|---|']
for n,x in [('correct',base)]+[(n,x) for n,x in s.items() if x['kind']=='numerical']:
    lines.append(f"| {n} | {x['peak_tool_force_N']:.3f} | {x['peak_hole_penetration_mm']:.6f} | {x['peak_tool_overclosure_mm']:.6f} | {x['max_projected_gradient_N']:.3g} | {x['valid_success']} |")
peaks=[x['peak_tool_force_N'] for x in s.values() if x['kind']=='numerical']
lines += ['',f"The numerical-only sweep spans **{min(peaks):.3f}–{max(peaks):.3f} N**, versus {base['peak_tool_force_N']:.3f} N nominal. All preserve nondestructive release and final clip travel (about {base['final']['clip_mm']:.3f} mm). The combined fine case uses 480 increments, 192 wall samples and 120,000 N/mm penalty. Discretization, sharp-profile transitions and lagged friction still affect peak reaction. Do not compare this force directly with a YAM gripper rating or call it an extraction-force specification.", '',
          'The domain guard requires maximum sampled hole penetration ≤0.05 mm, tool overclosure ≤0.25 mm, and nonnegative deformed leg radius. These are declared numerical admissibility limits, not OEM tolerances or material failure limits. The initial softer 300 N/mm hole model exceeded the fixed penetration limit (~0.224 mm) and failed the positive-control assertions; contact stiffness was increased, rather than loosening the limits. These failures informed the final implementation.']
(ROOT/'PARAMETER_SENSITIVITY.md').write_text('\n'.join(lines)+'\n')

fig, axes=plt.subplots(2,2,figsize=(12,8))
for n in ['correct','partial_extraction','panel_moves_clip_captured','excessive_panel_load']:
    with (ROOT/'results/traces'/f'{n}.csv').open() as f:rows=list(csv.DictReader(f))
    theta=[float(r['theta_rad']) for r in rows]
    axes[0,0].plot(theta,[float(r['clip_mm']) for r in rows],label=n)
    axes[0,1].plot(theta,[float(r['tool_force_N']) for r in rows],label=n)
with (ROOT/'results/traces/correct.csv').open() as f:rows=list(csv.DictReader(f))
theta=[float(r['theta_rad']) for r in rows]
for key in ['panel_mm','clip_mm','left_deflection_mm']:
    axes[1,0].plot(theta,[float(r[key]) for r in rows],label=key)
model=Coupon();p=Parameters();material_s=np.linspace(0,p.stem_length,801);r,_=model.profile(material_s);phi,_=model.mode(material_s)
for label,row in [('initial',rows[0]),('max bending',max(rows,key=lambda r:float(r['left_deflection_mm']))),('released',rows[-1])]:
    radius=r-phi*float(row['left_deflection_mm']);z=p.root_height+float(row['clip_mm'])-material_s
    axes[1,1].plot(radius,z,label=label)
    axes[1,1].plot(-radius,z,color=axes[1,1].lines[-1].get_color())
for side in [-1,1]:
    axes[1,1].plot([side*p.hole_diameter/2]*2,[-p.sheet_thickness,0],color='black',lw=5)
axes[1,1].axhline(0,color='gray',lw=.6)
axes[1,1].set(xlabel='radial position (mm)',ylabel='height above seat (mm)',title='ASSUMED opposed-leg section, not Hyundai CAD',xlim=(-7,7))
axes[0,0].set(xlabel='prescribed tool angle (rad)',ylabel='clip extraction (mm)',title='Motion is not the release score')
axes[0,1].set(xlabel='prescribed tool angle (rad)',ylabel='sampled tool reaction (N)',title='Quasistatic, uncalibrated force')
axes[1,0].set(xlabel='prescribed tool angle (rad)',ylabel='displacement (mm)',title='Nominal coupled deformation / recovery')
for ax in axes.flat:ax.legend(fontsize=7);ax.grid(alpha=.2)
fig.suptitle('N040 CPU coupon — exploratory assumed geometry/material, no full-door/YAM test')
fig.tight_layout()
fig.savefig(ROOT/'results/mechanism.png',dpi=150)
print('Wrote PARAMETER_SENSITIVITY.md and results/mechanism.png from recorded outputs.')
