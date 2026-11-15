# Parameter sensitivity — actual CPU results

**Exploratory assumed-material study, not measured Hyundai uncertainty bounds.** All dimensions are mm, forces N. `valid` requires initial retention, resolved equilibrium, the numerical contact-domain checks, released/recovered retaining geometry and no modeled plastic set. It does not certify authentic clip fitment or YAM access.

Each trace is in [results/traces](results/traces); complete inputs and diagnostics are in [summary.json](results/summary.json). `retention_released` is not complete stem withdrawal. All runs were executed on CPU; no empirical force curve was fitted.

## Required controls

| Run | Panel / clip final mm | Peak tool N | Released | Plastic damage | Domain valid | Valid success |
|---|---:|---:|---|---|---|---|
| correct | 3.8591 / 3.6590 | 46.126 | True | False | True | True |
| nearby_not_engaged | 0.0000 / 0.0000 | 0.000 | False | False | True | False |
| wrong_upper_surface | 0.0000 / 0.0000 | 3489.924 | False | False | False | False |
| partial_extraction | 1.5622 / 2.5387 | 53.510 | False | False | True | False |
| panel_moves_clip_captured | 3.8557 / 0.2945 | 34.207 | False | False | True | False |
| excessive_panel_load | 8.4889 / 8.2889 | 48.948 | True | True | True | False |
| yielding_legs | 3.8591 / 3.6590 | 30.873 | True | True | True | False |
| no_initial_retention | 3.8591 / 3.6590 | 30.873 | True | False | True | False |

The nominal release ends with the stem still in the hole; only the oversized retaining shoulder is clear. Nearby tool contact is exactly zero. Wrong-face contact gives a large rigid-stop penalty reaction and 3.49 mm tool overclosure: it is **outside the model domain**, not a credible plastic-tool load prediction. Partial extraction retains an oversized shoulder below the seat. A soft carrier permits over 3 mm of panel motion with under 0.5 mm clip extraction. These observations defeat panel-motion and proximity shortcuts.

Overdrive yields the assumed panel spring (48 N internal yield load), leaving permanent set. It is invalid even though all retaining geometry clears; that is a constitutive damage outcome, not a score-at-depth rule. Lower assumed leg yield strain also produces irreversible set. This does not establish which genuine clips are reusable.

## Assumption sweep

Baseline: E=1500 N/mm², t=1 mm, effective flexure L=7 mm, yield strain=0.04, friction=0.25, radius peak=5.3 mm, hole D=9 mm, sheet t=0.8 mm, carrier k=180 N/mm, panel k=8 N/mm, root height=6 mm. Changed values appear in each row name; all other parameters remain baseline except explicitly combined cases.

These ranges are deliberate design hypotheses to expose failure, **not empirical tolerances or confidence intervals**. E=700–2500; leg t=0.7–1.4; L=5.5–8.5; yield strain=0.012–0.06; friction=0–0.6; peak radius=4.8–5.8; hole D=8.6–9.4; sheet t=0.6–1.5; carrier k=1–500; panel k=2–20; root height=5.5–6.5. No probability of success can be inferred.

| Changed assumption | Peak tool N | Final clip mm | Max plastic set mm (leg / panel) | Released | Domain valid | Valid |
|---|---:|---:|---:|---|---|---|
| modulus_700 | 30.873 | 3.6590 | 0.0000 / 0.0000 | True | True | True |
| modulus_2500 | 74.890 | 3.6590 | 0.0000 / 0.0000 | True | True | True |
| leg_thickness_0.7 | 30.873 | 3.6590 | 0.0000 / 0.0000 | True | True | True |
| leg_thickness_1.4 | 121.034 | 3.6590 | 0.0000 / 0.0000 | True | True | True |
| flexure_length_5.5 | 46.716 | 3.6590 | 0.0000 / 0.0000 | True | True | True |
| flexure_length_8.5 | 46.334 | 3.6590 | 0.0000 / 0.0000 | True | True | True |
| yield_strain_0.012 | 30.873 | 3.6590 | 0.3464 / 0.0000 | True | True | False |
| yield_strain_0.025 | 46.126 | 3.6590 | 0.0000 / 0.0000 | True | True | True |
| yield_strain_0.06 | 46.126 | 3.6590 | 0.0000 / 0.0000 | True | True | True |
| friction_0 | 45.678 | 3.6590 | 0.0000 / 0.0000 | True | True | True |
| friction_0.1 | 49.603 | 3.6590 | 0.0000 / 0.0000 | True | True | True |
| friction_0.45 | 46.469 | 3.6590 | 0.0000 / 0.0000 | True | True | True |
| friction_0.6 | 46.717 | 3.6590 | 0.0000 / 0.0000 | True | True | True |
| peak_radius_4.8 | 30.873 | 3.6590 | 0.0000 / 0.0000 | True | True | True |
| peak_radius_5.8 | 86.478 | 3.6590 | 0.0000 / 0.0000 | True | False | False |
| hole_diameter_8.6 | 57.501 | 3.6590 | 0.0000 / 0.0000 | True | True | True |
| hole_diameter_9.4 | 34.688 | 3.6590 | 0.0000 / 0.0000 | True | True | True |
| sheet_thickness_0.6 | 50.060 | 3.6590 | 0.0000 / 0.0000 | True | True | True |
| sheet_thickness_1.5 | 30.873 | 3.6590 | 0.0000 / 0.0000 | True | True | True |
| head_carrier_stiffness_1 | 34.207 | 0.2945 | 0.0000 / 0.0000 | False | True | False |
| head_carrier_stiffness_30 | 58.104 | 3.6590 | 0.0000 / 0.0000 | True | True | True |
| head_carrier_stiffness_500 | 43.937 | 3.6590 | 0.0000 / 0.0000 | True | True | True |
| panel_stiffness_2 | 41.719 | 3.6822 | 0.0000 / 0.0000 | True | True | True |
| panel_stiffness_20 | 76.274 | 3.6136 | 0.0000 / 0.0000 | True | True | True |
| root_height_5.5 | 51.407 | 3.6590 | 0.0000 / 0.0000 | True | True | True |
| root_height_6.5 | 30.873 | 3.6590 | 0.0000 / 0.0000 | True | True | True |
| combined_stiff_high_friction | 196.634 | 3.6590 | 0.0000 / 0.0000 | True | True | True |
| combined_large_barb_small_hole | 61.639 | 3.6590 | 0.5789 / 0.0000 | True | False | False |

Success is **property-dependent**. Low-yield legs damage; soft head coupling fails to extract the retainer despite panel travel. Large-barb cases can drive the one-mode leg radius negative; the domain guard rejects those runs. Their damage/force diagnostics are outside the admissible model and cannot support hardware conclusions. The high-stiffness/high-friction interaction raises force substantially even where release remains possible. No small isolated sweep validates all correlated material/shape combinations.

## Numerical sensitivity, separate from material uncertainty

All increment solves satisfy the reported projected-gradient stationarity criterion (<0.01 N) and optimizer success. That is local equilibrium of this reduced model, not global dynamic snap validation. L-BFGS-B follows warm-start local equilibria; inertia, rate effects and impact peaks are absent. Contact is midpoint quadrature with a sharp assumed shoulder. Peak force has not converged to a defensible hardware prediction.

| Numerical change | Peak tool N | Max hole overlap mm | Max tool overclosure mm | Max projected gradient N | Release valid |
|---|---:|---:|---:|---:|---|
| correct | 46.126 | 0.004816 | 0.046126 | 0.000109 | True |
| numerical_steps_60 | 46.082 | 0.004828 | 0.046082 | 3.54e-05 | True |
| numerical_steps_240 | 52.474 | 0.005059 | 0.052474 | 3.77e-05 | True |
| numerical_steps_480 | 50.796 | 0.005111 | 0.050796 | 0.000138 | True |
| numerical_wall_samples_24 | 49.714 | 0.002491 | 0.049714 | 0.000109 | True |
| numerical_wall_samples_96 | 46.473 | 0.009718 | 0.046473 | 0.000109 | True |
| numerical_wall_samples_192 | 46.525 | 0.019462 | 0.046525 | 0.000109 | True |
| numerical_hole_penalty_7500 | 45.889 | 0.019144 | 0.045889 | 0.000109 | True |
| numerical_hole_penalty_15000 | 46.047 | 0.009611 | 0.046047 | 0.000109 | True |
| numerical_hole_penalty_60000 | 46.166 | 0.002410 | 0.046166 | 0.000109 | True |
| numerical_hole_penalty_120000 | 46.186 | 0.001206 | 0.046186 | 0.000109 | True |
| numerical_viscosity_0.002 | 46.123 | 0.004815 | 0.046123 | 0.000139 | True |
| numerical_viscosity_0.05 | 46.139 | 0.004817 | 0.046139 | 0.000123 | True |
| numerical_friction_regularizer_5e-05 | 46.126 | 0.004816 | 0.046126 | 0.000109 | True |
| numerical_friction_regularizer_0.0002 | 46.126 | 0.004816 | 0.046126 | 0.000109 | True |
| numerical_combined_fine | 47.810 | 0.005004 | 0.047810 | 0.000214 | True |

The numerical-only sweep spans **45.889–52.474 N**, versus 46.126 N nominal. All preserve nondestructive release and final clip travel (about 3.659 mm). The combined fine case uses 480 increments, 192 wall samples and 120,000 N/mm penalty. Discretization, sharp-profile transitions and lagged friction still affect peak reaction. Do not compare this force directly with a YAM gripper rating or call it an extraction-force specification.

The domain guard requires maximum sampled hole penetration ≤0.05 mm, tool overclosure ≤0.25 mm, and nonnegative deformed leg radius. These are declared numerical admissibility limits, not OEM tolerances or material failure limits. The initial softer 300 N/mm hole model exceeded the fixed penetration limit (~0.224 mm) and failed the positive-control assertions; contact stiffness was increased, rather than loosening the limits. These failures informed the final implementation.
