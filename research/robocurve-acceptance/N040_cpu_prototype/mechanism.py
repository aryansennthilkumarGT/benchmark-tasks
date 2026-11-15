"""Exploratory CPU quasistatic contact coupon. Units: mm, N, N mm.

NOT measured Hyundai geometry. No latch state changes the equations. A rotating
nose loads a local panel, its captured-head carrier pulls a compliant retainer,
and fixed hole-wall contact bends two hypothetical legs. See SOURCE_AND_GEOMETRY.
"""
from dataclasses import dataclass, asdict
import numpy as np
from scipy.optimize import minimize


@dataclass(frozen=True)
class Parameters:
    hole_diameter: float = 9.0  # user-attributed supplier nominal, not re-read
    head_diameter: float = 13.0  # envelope only; not used as measured carrier
    stem_length: float = 13.0
    overall_length: float = 19.0  # envelope only
    sheet_thickness: float = 0.8  # EVERYTHING below is an exploratory assumption
    root_height: float = 6.0
    shoulder_start: float = 6.8
    shoulder_peak: float = 7.2
    neck_radius: float = 2.7
    peak_radius: float = 5.3
    tip_radius: float = 2.4
    flexure_length: float = 7.0
    leg_width: float = 4.0
    leg_thickness: float = 1.0
    modulus: float = 1500.0
    yield_strain: float = 0.04
    hardening_fraction: float = 0.05
    panel_stiffness: float = 8.0
    panel_yield_displacement: float = 6.0
    head_carrier_stiffness: float = 180.0
    head_clearance: float = 0.2
    hole_penalty: float = 30000.0  # force per penetration, numerical regularization
    tool_penalty: float = 1000.0
    friction: float = 0.25
    friction_regularizer: float = 0.0001
    viscosity: float = 0.01  # numerical continuation only, not material damping
    wall_samples: int = 48
    steps: int = 120
    tool_pivot_x: float = -10.0
    tool_pivot_z: float = -1.0
    handle_length: float = 100.0
    panel_half_patch_min: float = -9.0
    panel_half_patch_max: float = 4.0
    panel_thickness: float = 2.0

    @property
    def leg_k(self):
        return self.modulus * self.leg_width * self.leg_thickness**3 / (4*self.flexure_length**3)

    @property
    def leg_yield(self):
        return self.yield_strain*self.flexure_length**2/(1.5*self.leg_thickness)


def positive(v):
    return np.maximum(v, 0.)


def plastic_spring(q, previous, k, yield_displacement, hardening):
    """Monotone inward/pull plastic set; energy is incremental return mapping.

    Irreversibility a>=a_previous; yield force k*q_y. Not fracture prediction.
    """
    fy, h = k*yield_displacement, k*hardening
    a = np.maximum(previous, (k*np.asarray(q)-fy)/(k+h))
    elastic = np.asarray(q)-a
    energy = .5*k*elastic**2 + .5*h*a**2 + fy*(a-previous)
    return energy, k*elastic, a


class Coupon:
    def __init__(self, params=Parameters(), pose="under", offset=0.):
        self.p = params
        self.pose, self.offset = pose, offset
        # Midpoint quadrature integrates the finite-thickness hole wall.
        self.wall_z = -(np.arange(params.wall_samples)+.5)*params.sheet_thickness/params.wall_samples
        self.wall_weights = np.full(params.wall_samples, 1/params.wall_samples)
        self.nose_x = np.linspace(8., 10., 9)
        self.nose_z = np.linspace(.8, .6, 9)  # tapered plastic top surface

    def profile(self, s):
        p = self.p
        nodes = np.array([0., p.shoulder_start, p.shoulder_peak, p.stem_length])
        radii = np.array([p.neck_radius, p.neck_radius, p.peak_radius, p.tip_radius])
        idx = np.clip(np.searchsorted(nodes, s, side="right")-1, 0, 2)
        slope = np.diff(radii)[idx]/np.diff(nodes)[idx]
        r = radii[idx]+slope*(s-nodes[idx])
        inside = (s >= 0)&(s <= p.stem_length)
        return np.where(inside, r, 0.), np.where(inside, slope, 0.)

    def mode(self, s):
        xi = np.maximum(s/self.p.flexure_length, 0.)
        phi = np.where(xi <= 1, (3*xi**2-xi**3)/2, 1+1.5*(xi-1))
        derivative = np.where(xi <= 1, (3*xi-1.5*xi**2)/self.p.flexure_length, 1.5/self.p.flexure_length)
        return phi, derivative

    def nose(self, theta):
        """Actual rotated surface geometry; no 'engagement' flag or release command."""
        p = self.p
        x = p.tool_pivot_x+self.offset+self.nose_x*np.cos(theta)-self.nose_z*np.sin(theta)
        z = p.tool_pivot_z+self.nose_x*np.sin(theta)+self.nose_z*np.cos(theta)
        dz = self.nose_x*np.cos(theta)-self.nose_z*np.sin(theta)
        valid = (x >= p.panel_half_patch_min)&(x <= p.panel_half_patch_max)
        if not np.any(valid):
            return None, 0.
        i = np.argmax(np.where(valid, z, -np.inf))
        return float(z[i]), float(dz[i])

    def hole(self, c, q):
        p = self.p
        s = p.root_height+c-self.wall_z
        r, dr = self.profile(s)
        phi, dphi = self.mode(s)
        penetration = positive(r[None, :]-np.asarray(q)[:, None]*phi-p.hole_diameter/2)
        normals = p.hole_penalty*penetration*self.wall_weights
        energy = .5*p.hole_penalty*np.sum(penetration**2*self.wall_weights)
        gc = np.sum(normals*(dr-np.asarray(q)[:, None]*dphi))
        gq = -np.sum(normals*phi, axis=1)
        return energy, gc, gq, float(normals.sum()), float(penetration.max())

    def objective(self, x, theta, previous, plastic, previous_normal, detail=False):
        p = self.p
        panel, clip, left, right = x
        q = np.array([left, right])
        el, fl, al = plastic_spring(q, plastic[1:], p.leg_k, p.leg_yield, p.hardening_fraction)
        ep, fp, ap = plastic_spring(panel, plastic[0], p.panel_stiffness, p.panel_yield_displacement, p.hardening_fraction)
        energy = float(el.sum()+ep)
        grad = np.array([fp, 0., fl[0], fl[1]])
        # Undercut head/carrier clearance: transmits uplift but is not a welded panel.
        head_gap = max(panel-clip-p.head_clearance, 0.)
        head_force = p.head_carrier_stiffness*head_gap
        energy += .5*p.head_carrier_stiffness*head_gap**2
        grad += np.array([head_force, -head_force, 0., 0.])
        eh, gc, gq, normal, penetration = self.hole(clip, q)
        energy += eh
        grad[1] += gc
        grad[2:] += gq
        # Friction is axial, regularized Coulomb, lagging normal one load increment.
        dc = clip-previous[1]
        norm = np.sqrt(dc*dc+p.friction_regularizer**2)
        friction_force = p.friction*previous_normal*dc/norm
        energy += p.friction*previous_normal*(norm-p.friction_regularizer)
        grad[1] += friction_force
        height, dh = self.nose(theta)
        tool_force, gap = 0., 0.
        if height is not None:
            if self.pose == "under":
                gap, sign = max(height-panel, 0.), -1.
            elif self.pose == "upper":
                # Mirrored same nose, descending onto the panel's upper face.
                upper_surface = p.panel_thickness+.4-height
                gap, sign = max(panel+p.panel_thickness-upper_surface, 0.), 1.
            else:
                raise ValueError(self.pose)
            tool_force = p.tool_penalty*gap
            energy += .5*p.tool_penalty*gap**2
            grad[0] += sign*tool_force
        energy += .5*p.viscosity*np.sum((x-previous)**2)
        grad += p.viscosity*(x-previous)
        if not detail:
            return energy, grad
        return dict(energy_Nmm=energy, plastic=np.r_[ap, al], hole_normal_N=normal,
                    max_hole_penetration_mm=penetration, tool_force_N=tool_force,
                    head_force_N=head_force, friction_force_N=friction_force, tool_overclosure_mm=gap,
                    tool_torque_Nmm=tool_force*abs(dh),
                    estimated_handle_force_N=tool_force*abs(dh)/p.handle_length)

    def audit(self, x, plastic):
        """Read-only material-clearance audit, never used by the solver.

        Free recovered shape (including irreversible set), not current bent shape,
        is checked for all oversized portions still below the receiving upper face.
        """
        p = self.p
        s = np.linspace(0., p.stem_length, 5201)
        r, _ = self.profile(s)
        phi, _ = self.mode(s)
        free_r = r[None, :]-plastic[1:, None]*phi
        below = p.root_height+x[1]-s <= 0.
        captured = bool(np.any((free_r > p.hole_diameter/2+.002)&below))
        _, _, _, normal, penetration = self.hole(x[1], x[2:])
        damage = bool(np.max(plastic) > .001)
        elastic_recovered = bool(np.max(np.abs(x[2:]-plastic[1:])) < .02)
        retention_released = not captured and normal < .05 and elastic_recovered
        return dict(oversized_retaining_material_below_seat=captured,
                    retention_released=bool(retention_released),
                    fully_withdrawn=bool(p.root_height+x[1] > p.stem_length),
                    modeled_plastic_damage=damage,
                    valid_nondestructive_release=bool(retention_released and not damage),
                    residual_hole_normal_N=normal, residual_penetration_mm=penetration)

    def run(self, theta_max=.45):
        p = self.p
        x, plastic, normal = np.zeros(4), np.zeros(3), 0.
        rows = []
        initial = self.audit(x, plastic)
        for step, theta in enumerate(np.linspace(0., theta_max, p.steps+1)):
            previous = x.copy()
            result = minimize(self.objective, x, args=(theta, previous, plastic, normal),
                              method="L-BFGS-B", jac=True,
                              bounds=[(0., 20.), (0., 20.), (0., 2.4), (0., 2.4)],
                              options=dict(ftol=1e-13, gtol=2e-6, maxiter=400, maxls=60))
            x = result.x
            d = self.objective(x, theta, previous, plastic, normal, detail=True)
            plastic = d.pop("plastic")
            normal = d["hole_normal_N"]
            # Report stationarity of the actual solved increment (not re-evaluated
            # with its newly updated friction/plastic history).
            projected = result.jac.copy()
            projected[(x < 1e-8)&(projected > 0.)] = 0.
            projected[(x > np.array([20.,20.,2.4,2.4])-1e-8)&(projected < 0.)] = 0.
            row = dict(step=step, theta_rad=float(theta), panel_mm=float(x[0]),
                       clip_mm=float(x[1]), left_deflection_mm=float(x[2]),
                       right_deflection_mm=float(x[3]), panel_plastic_mm=float(plastic[0]),
                       left_plastic_mm=float(plastic[1]), right_plastic_mm=float(plastic[2]),
                       solver_success=bool(result.success), solver_message=str(result.message),
                       projected_gradient_N=float(np.max(abs(projected))), **d)
            row.update(self.audit(x, plastic))
            rows.append(row)
        summary = dict(parameters=asdict(p), pose=self.pose, offset_mm=self.offset,
                       theta_max_rad=theta_max, initial=initial, final=rows[-1],
                       peak_tool_force_N=max(r["tool_force_N"] for r in rows),
                       peak_head_force_N=max(r["head_force_N"] for r in rows),
                       peak_hole_normal_N=max(r["hole_normal_N"] for r in rows),
                       peak_tool_torque_Nmm=max(r["tool_torque_Nmm"] for r in rows),
                       peak_handle_force_N=max(r["estimated_handle_force_N"] for r in rows),
                       peak_leg_deflection_mm=max(r["left_deflection_mm"] for r in rows),
                       peak_hole_penetration_mm=max(r["max_hole_penetration_mm"] for r in rows),
                       peak_tool_overclosure_mm=max(r["tool_overclosure_mm"] for r in rows),
                       max_projected_gradient_N=max(r["projected_gradient_N"] for r in rows),
                       optimizer_failed_steps=sum(not r["solver_success"] for r in rows),
                       nonstationary_steps=sum(r["projected_gradient_N"] > .01 for r in rows))
        summary["numerically_resolved"] = summary["nonstationary_steps"] == 0 and summary["optimizer_failed_steps"] == 0
        # An explicit numerical-domain guard; not a measured tool failure limit.
        grid = np.linspace(0., p.stem_length, 521)
        radius, _ = self.profile(grid)
        phi, _ = self.mode(grid)
        summary["minimum_deformed_radius_mm"] = float(np.min(radius-phi*summary["peak_leg_deflection_mm"]))
        summary["contact_domain_ok"] = bool(summary["minimum_deformed_radius_mm"] >= 0. and summary["peak_tool_overclosure_mm"] <= .25 and
                                            summary["peak_hole_penetration_mm"] <= .05)
        summary["valid_success"] = bool(summary["contact_domain_ok"] and initial["oversized_retaining_material_below_seat"] and
                                         summary["numerically_resolved"] and rows[-1]["valid_nondestructive_release"])
        return rows, summary
