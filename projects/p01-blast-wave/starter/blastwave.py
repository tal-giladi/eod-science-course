"""blastwave — blast-wave physics library for Project P01.

STARTER. Implement every function whose body is `raise NotImplementedError`. Functions that
are already implemented are PROVIDED helpers (not the learning goal) — use them freely.

Everything here is standard, published ideal-gas shock physics (Rankine–Hugoniot), published
empirical free-air fits (Kinney & Graham, 1985) and a textbook finite-volume Euler solver.
Yields are ABSTRACT "yield units" (YU); scaled distance Z = R / W^(1/3) [m / YU^(1/3)].
The formulas mirror ``sims/common/blast.js`` (Sims D and I) so that Python and the simulators
agree number for number.

Units used throughout (unless a docstring says otherwise):
    pressure  kPa        time      ms        distance  m
    impulse   kPa·ms     yield     YU        speed     m/s
The Euler solver is non-dimensional.

Lessons: 01.3 (shocks, Euler equations), 01.4 (reflection, dynamic pressure), 01.5 (scaling),
04.1 (Friedlander waveform, Kinney–Graham fits, arrival time).
"""
from __future__ import annotations

import numpy as np

P0 = 101.325   # kPa, sea-level standard ambient pressure
A0 = 340.3     # m/s, sea-level standard speed of sound
GAMMA = 1.4    # ratio of specific heats for air


# ---------------------------------------------------------------------------------------------
# 1. Rankine–Hugoniot (lessons 01.3, 01.4)
# ---------------------------------------------------------------------------------------------
def shock_jump(M, gamma: float = GAMMA) -> dict:
    """Normal-shock jump ratios for an ideal gas, state 2 (behind) over state 1 (ahead).

    Parameters
    ----------
    M : float or ndarray
        Shock Mach number M_s = U_s / a_1 (must be >= 1).
    gamma : float
        Ratio of specific heats.

    Returns
    -------
    dict with keys
        ``"p"``          p2/p1 = 1 + 2γ/(γ+1) (M²−1)
        ``"rho"``        ρ2/ρ1 = (γ+1)M² / ((γ−1)M² + 2)
        ``"T"``          T2/T1 = (p2/p1)/(ρ2/ρ1)
        ``"u_over_a1"``  particle velocity behind the shock / a1 = 2/(γ+1) (M − 1/M)
        ``"M_down"``     downstream Mach number in the shock frame
                         sqrt(((γ−1)M² + 2) / (2γM² − (γ−1)))
    """
    raise NotImplementedError


def mach_from_overpressure(ps, p0: float = P0, gamma: float = GAMMA):
    """Shock Mach number from peak overpressure (inverse of the p2/p1 relation).

    M_s = sqrt(1 + (γ+1)/(2γ) · ps/p0).  ``ps`` and ``p0`` in the same unit (default kPa).
    """
    raise NotImplementedError


def dynamic_pressure(ps, p0: float = P0, gamma: float = GAMMA):
    """Peak dynamic pressure q = ½ ρ2 u2² behind a shock of overpressure ``ps``.

    General ideal gas: q = ps² / (2γ p0 + (γ−1) ps).
    For γ = 1.4 this is the familiar q = 5/2 · ps² / (7 p0 + ps)  (same unit as ps).
    """
    raise NotImplementedError


def reflected_overpressure(ps, p0: float = P0):
    """Normally reflected overpressure for air (γ = 1.4), closed form.

    p_r = 2 ps (7 p0 + 4 ps) / (7 p0 + ps).  Reflection factor p_r/ps → 2 (acoustic) as ps → 0
    and → 8 as ps → ∞.
    """
    raise NotImplementedError


def reflected_ratio(ps, p0: float = P0, gamma: float = GAMMA):
    """Reflection factor C_r = p_r/ps for general γ (normal reflection off a rigid wall).

    With y = ps/p0:  C_r = 2 + (γ+1) y / ((γ−1) y + 2γ).
    Limits: 2 as y → 0; (3γ−1)/(γ−1) as y → ∞ (8 for γ = 1.4).
    """
    raise NotImplementedError


# ---------------------------------------------------------------------------------------------
# 2. Kinney–Graham free-air fits and scaling (lessons 01.5, 04.1)
# ---------------------------------------------------------------------------------------------
def kg_overpressure_ratio(Z):
    """Kinney–Graham (1985) peak incident overpressure ratio ps/p0 at scaled distance Z [m/YU^(1/3)]."""
    raise NotImplementedError


def kg_duration_scaled(Z):
    """Kinney–Graham positive-phase duration per cube-root yield, t_d / W^(1/3) [ms/YU^(1/3)]."""
    raise NotImplementedError


def kg_impulse_scaled(Z):
    """Kinney–Graham positive-phase impulse per cube-root yield, i / W^(1/3) [bar·ms/YU^(1/3)].

    Multiply by 100 to convert bar·ms to kPa·ms.
    """
    raise NotImplementedError


def scaled_distance(R, W, p0: float = P0):
    """Sachs-scaled distance, expressed as its sea-level equivalent.

    Z = R / W^(1/3) · (p0/P0)^(1/3)   [m / YU^(1/3)].  At p0 = P0 this is Hopkinson–Cranz Z.
    """
    raise NotImplementedError


# ---------------------------------------------------------------------------------------------
# 3. Friedlander waveform (lesson 04.1)
# ---------------------------------------------------------------------------------------------
def friedlander(t, ps, td, b):
    """Friedlander overpressure p(t) = ps (1 − t/td) exp(−b t/td) for t >= 0, 0 for t < 0.

    ``t`` is time since arrival (same unit as ``td``); negative phase included for t > td.
    """
    raise NotImplementedError


def friedlander_impulse(ps, td, b):
    """Analytic positive-phase impulse ∫₀^td p dt = ps td [1/b − (1 − e^−b)/b²]."""
    raise NotImplementedError


def friedlander_impulse_numeric(ps, td, b, n: int = 2001):
    """Positive-phase impulse by composite Simpson's rule on ``n`` (odd) points over [0, td]."""
    raise NotImplementedError


def solve_decay(ps, td, i_target, lo: float = 1e-4, hi: float = 60.0):
    """Decay coefficient b such that friedlander_impulse(ps, td, b) == i_target (bisection).

    The impulse is monotonically decreasing in b. Targets outside the bracket return the
    bracket end (``lo`` if the target is too large, ``hi`` if too small), as in blast.js.
    """
    raise NotImplementedError


# ---------------------------------------------------------------------------------------------
# 4. Arrival time and full prediction (lesson 04.1)
# ---------------------------------------------------------------------------------------------
def arrival_time(R, W, a0: float = A0, p0: float = P0, n: int = 400):
    """Shock arrival time [ms] at range R [m] for yield W [YU]: t_a = ∫ dr / U(r).

    U(r) = a0 · M(ps(r)), ps from the Kinney–Graham fit at the Sachs-scaled distance.
    Midpoint rule with ``n`` intervals from r0 = 0.05 m/YU^(1/3) (scaled) to R; returns 0 if
    R <= r0. (blast.js uses an unscaled r0; identical at sea level, but scaling r0 makes the
    result exactly Sachs-invariant.)
    """
    raise NotImplementedError


def predict(W, R, p0: float = P0, a0: float = A0, surface_factor: float = 1.0) -> dict:
    """Free-air gauge prediction for yield W [YU] at range R [m] (port of ``predict`` in blast.js).

    Sachs scaling for non-standard ambient: distance scales with (W/p0)^(1/3), pressure with p0,
    time with (W/p0)^(1/3)/a0, impulse with p0^(2/3) W^(1/3)/a0.

    ``surface_factor`` multiplies the effective yield (1 = free air, ≈1.8 hemispherical surface).

    Returns dict with keys
        W, We, R, Z, ps [kPa], td [ms], i [kPa·ms] (impulse of the fitted Friedlander pulse),
        i_fit [kPa·ms] (Kinney–Graham impulse), b, ta [ms], M, U [m/s], q [kPa], pr [kPa],
        Cr, ir [kPa·ms].

    If the duration and impulse fits demand b < 0.5 (a pulse fuller than a triangle), b is
    floored at 0.5 and t_d stretched to honour the impulse fit, exactly as blast.js does.
    """
    raise NotImplementedError


def gauge_trace(W, R, t, **kwargs):
    """Overpressure history p(t) [kPa] at range R for yield W, t in ms since release.

    Friedlander pulse from :func:`predict`, delayed by the arrival time.
    """
    pr = predict(W, R, **kwargs)
    return friedlander(np.asarray(t, dtype=float) - pr["ta"], pr["ps"], pr["td"], pr["b"])


# ---------------------------------------------------------------------------------------------
# 5. 1D finite-volume Euler solver (lesson 01.3)
# ---------------------------------------------------------------------------------------------
def prim_to_cons(rho, u, p, gamma: float = GAMMA):
    """Primitive (ρ, u, p) → conservative U = [ρ, ρu, E], E = p/(γ−1) + ½ρu². Shape (3, N)."""
    rho, u, p = (np.asarray(a, dtype=float) for a in (rho, u, p))
    return np.array([rho, rho * u, p / (gamma - 1) + 0.5 * rho * u * u])


def cons_to_prim(U, gamma: float = GAMMA):
    """Conservative U (3, N) → primitive (ρ, u, p)."""
    rho = U[0]
    u = U[1] / rho
    p = (gamma - 1) * (U[2] - 0.5 * rho * u * u)
    return rho, u, p


def euler_flux(U, gamma: float = GAMMA):
    """Physical flux F(U) = [ρu, ρu² + p, u(E + p)]."""
    raise NotImplementedError


def hll_flux(UL, UR, gamma: float = GAMMA):
    """HLL numerical flux between left and right states (arrays of shape (3, M)).

    Wave-speed estimates (Davis): S_L = min(u_L − c_L, u_R − c_R), S_R = max(u_L + c_L, u_R + c_R).
    F = F_L if S_L >= 0; F_R if S_R <= 0; else (S_R F_L − S_L F_R + S_L S_R (U_R − U_L)) / (S_R − S_L).
    """
    raise NotImplementedError


def _pad(U, bc):
    if bc == "periodic":
        return np.concatenate([U[:, -1:], U, U[:, :1]], axis=1)
    if bc == "transmissive":
        return np.concatenate([U[:, :1], U, U[:, -1:]], axis=1)
    if bc == "reflective":
        left = U[:, :1] * np.array([[1.0], [-1.0], [1.0]])
        right = U[:, -1:] * np.array([[1.0], [-1.0], [1.0]])
        return np.concatenate([left, U, right], axis=1)
    raise ValueError(f"unknown boundary condition {bc!r}")


def euler_step(U, dx, dt, gamma: float = GAMMA, bc: str = "transmissive"):
    """One first-order conservative update U^{n+1}_i = U^n_i − dt/dx (F_{i+½} − F_{i−½}).

    ``bc`` ∈ {"transmissive", "periodic", "reflective"} (one ghost cell each side).
    """
    raise NotImplementedError


def max_wave_speed(U, gamma: float = GAMMA):
    """max_i (|u_i| + c_i), the fastest signal speed on the grid (for the CFL condition)."""
    raise NotImplementedError


def euler_solve(rho, u, p, dx, t_end, gamma: float = GAMMA, cfl: float = 0.5,
                bc: str = "transmissive"):
    """Integrate the 1D Euler equations from primitive initial data to ``t_end``.

    Time step dt = cfl · dx / max(|u| + c), with the last step shortened to land exactly on
    t_end. Returns ``(rho, u, p, nsteps)`` at t_end.
    """
    raise NotImplementedError


# ---------------------------------------------------------------------------------------------
# 6. Exact Riemann solver (PROVIDED HELPER — also implemented in the starter)
#    After Toro, "Riemann Solvers and Numerical Methods for Fluid Dynamics", ch. 4.
#    Mirrors sims/common/riemann.js. States are (rho, u, p) tuples.
# ---------------------------------------------------------------------------------------------
def exact_riemann(left, right, gamma: float = GAMMA, tol: float = 1e-12) -> dict:
    """Star-region solution of the Riemann problem with states ``left``/``right`` = (ρ, u, p).

    Returns dict: p_star, u_star, rho_star_L, rho_star_R, shock_L / shock_R speeds (None for a
    rarefaction), plus the inputs, for use with :func:`sample_riemann`.
    """
    rl, ul, pl = map(float, left)
    rr, ur, pr = map(float, right)
    g = gamma
    cl, cr = np.sqrt(g * pl / rl), np.sqrt(g * pr / rr)
    AL, BL = 2 / ((g + 1) * rl), (g - 1) / (g + 1) * pl
    AR, BR = 2 / ((g + 1) * rr), (g - 1) / (g + 1) * pr

    def fk(p, pk, rk, ck, A, B):
        if p > pk:
            q = np.sqrt(A / (p + B))
            return (p - pk) * q, q * (1 - 0.5 * (p - pk) / (B + p))
        pr_ = p / pk
        return (2 * ck / (g - 1) * (pr_ ** ((g - 1) / (2 * g)) - 1),
                1 / (rk * ck) * pr_ ** (-(g + 1) / (2 * g)))

    du = ur - ul
    e = (g - 1) / (2 * g)
    p = ((cl + cr - 0.5 * (g - 1) * du) / (cl / pl ** e + cr / pr ** e)) ** (1 / e)
    p = max(1e-10, p)
    for _ in range(100):
        fL, dL = fk(p, pl, rl, cl, AL, BL)
        fR, dR = fk(p, pr, rr, cr, AR, BR)
        pn = max(1e-10, p - (fL + fR + du) / (dL + dR))
        if abs(pn - p) / (0.5 * (pn + p)) < tol:
            p = pn
            break
        p = pn
    fL = fk(p, pl, rl, cl, AL, BL)[0]
    fR = fk(p, pr, rr, cr, AR, BR)[0]
    u = 0.5 * (ul + ur) + 0.5 * (fR - fL)
    k = (g - 1) / (g + 1)
    rsl = rl * ((p / pl + k) / (k * p / pl + 1)) if p > pl else rl * (p / pl) ** (1 / g)
    rsr = rr * ((p / pr + k) / (k * p / pr + 1)) if p > pr else rr * (p / pr) ** (1 / g)
    s = lambda pk: np.sqrt((g + 1) / (2 * g) * p / pk + (g - 1) / (2 * g))  # noqa: E731
    return {
        "p_star": p, "u_star": u, "rho_star_L": rsl, "rho_star_R": rsr,
        "shock_L": ul - cl * s(pl) if p > pl else None,
        "shock_R": ur + cr * s(pr) if p > pr else None,
        "left": (rl, ul, pl), "right": (rr, ur, pr), "gamma": g, "cL": cl, "cR": cr,
    }


def sample_riemann(sol: dict, xi):
    """Sample the exact solution at similarity coordinates xi = (x − x0)/t. Returns (ρ, u, p) arrays."""
    xi = np.atleast_1d(np.asarray(xi, dtype=float))
    g = sol["gamma"]
    rl, ul, pl = sol["left"]
    rr, ur, pr = sol["right"]
    cl, cr = sol["cL"], sol["cR"]
    ps, us = sol["p_star"], sol["u_star"]
    out = np.empty((3, xi.size))
    for j, x in enumerate(xi):
        if x <= us:
            if ps > pl:
                st = (rl, ul, pl) if x < sol["shock_L"] else (sol["rho_star_L"], us, ps)
            else:
                cls = cl * (ps / pl) ** ((g - 1) / (2 * g))
                if x <= ul - cl:
                    st = (rl, ul, pl)
                elif x >= us - cls:
                    st = (sol["rho_star_L"], us, ps)
                else:
                    uu = 2 / (g + 1) * (cl + (g - 1) / 2 * ul + x)
                    c = 2 / (g + 1) * (cl + (g - 1) / 2 * (ul - x))
                    st = (rl * (c / cl) ** (2 / (g - 1)), uu, pl * (c / cl) ** (2 * g / (g - 1)))
        else:
            if ps > pr:
                st = (rr, ur, pr) if x > sol["shock_R"] else (sol["rho_star_R"], us, ps)
            else:
                crs = cr * (ps / pr) ** ((g - 1) / (2 * g))
                if x >= ur + cr:
                    st = (rr, ur, pr)
                elif x <= us + crs:
                    st = (sol["rho_star_R"], us, ps)
                else:
                    uu = 2 / (g + 1) * (-cr + (g - 1) / 2 * ur + x)
                    c = 2 / (g + 1) * (cr - (g - 1) / 2 * (ur - x))
                    st = (rr * (c / cr) ** (2 / (g - 1)), uu, pr * (c / cr) ** (2 * g / (g - 1)))
        out[:, j] = st
    return out[0], out[1], out[2]


def sod_initial(n: int = 400, x0: float = 0.5):
    """Sod shock-tube initial data on [0, 1]: (ρ,u,p) = (1,0,1) | (0.125,0,0.1). Returns x, ρ, u, p, dx."""
    dx = 1.0 / n
    x = (np.arange(n) + 0.5) * dx
    left = x < x0
    rho = np.where(left, 1.0, 0.125)
    p = np.where(left, 1.0, 0.1)
    return x, rho, np.zeros(n), p, dx
