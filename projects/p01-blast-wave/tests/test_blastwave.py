"""Tests for Project P01 — blast-wave physics library (`blastwave`).

Run against your starter:        python -m pytest projects/p01-blast-wave
Run against the reference:       EOD_SOLUTION=1 python -m pytest projects/p01-blast-wave
"""
import os, sys, pathlib
_ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_ROOT / ("solution" if os.environ.get("EOD_SOLUTION") else "starter")))
import blastwave as mod  # noqa: E402

import importlib.util  # noqa: E402

import numpy as np  # noqa: E402
import pytest  # noqa: E402
from scipy.optimize import brentq  # noqa: E402

G = 1.4


# ------------------------------------------------------------------ Rankine–Hugoniot
def test_shock_jump_lesson_example():
    # lesson 01.3 worked example: 100 kPa overpressure into sea-level air
    M = float(mod.mach_from_overpressure(100.0))
    assert M == pytest.approx(1.359, abs=1e-3)
    j = mod.shock_jump(M)
    assert float(j["p"]) == pytest.approx(1.987, abs=1e-3)
    assert float(j["rho"]) == pytest.approx(1.618, abs=1e-3)
    assert float(j["u_over_a1"]) * mod.A0 == pytest.approx(176.6, abs=0.5)
    assert float(j["T"]) * 288 == pytest.approx(354, abs=1)


def test_shock_jump_limits():
    j1 = mod.shock_jump(1.0)
    for k in ("p", "rho", "T", "M_down"):
        assert float(j1[k]) == pytest.approx(1.0, abs=1e-12)
    assert float(j1["u_over_a1"]) == pytest.approx(0.0, abs=1e-12)
    strong = mod.shock_jump(1e4)
    assert float(strong["rho"]) == pytest.approx((G + 1) / (G - 1), rel=1e-6)   # 6 for air
    assert float(strong["M_down"]) == pytest.approx(np.sqrt((G - 1) / (2 * G)), rel=1e-6)
    Ms = np.linspace(1.01, 8, 50)
    assert np.all(np.asarray(mod.shock_jump(Ms)["M_down"]) < 1)   # subsonic behind a shock


def test_mach_from_overpressure_inverts_jump():
    for M in (1.05, 1.5, 3.0, 7.0):
        for g in (1.4, 1.2, 5 / 3):
            dp = (float(mod.shock_jump(M, g)["p"]) - 1) * mod.P0
            assert float(mod.mach_from_overpressure(dp, mod.P0, g)) == pytest.approx(M, rel=1e-12)


def test_dynamic_pressure_equals_half_rho_u2():
    # q = ½ ρ2 u2² computed from the jump conditions with ρ1 = γ p1 / a1²
    p1 = 101.325e3
    a1 = 340.3
    rho1 = G * p1 / a1 ** 2
    for ps in (5.0, 50.0, 300.0, 2000.0):   # kPa
        M = float(mod.mach_from_overpressure(ps))
        j = mod.shock_jump(M)
        q = 0.5 * rho1 * float(j["rho"]) * (float(j["u_over_a1"]) * a1) ** 2 / 1e3
        assert float(mod.dynamic_pressure(ps)) == pytest.approx(q, rel=1e-9)
        assert float(mod.dynamic_pressure(ps)) == pytest.approx(2.5 * ps ** 2 / (7 * mod.P0 + ps), rel=1e-12)


def test_reflection_factor_limits():
    assert float(mod.reflected_overpressure(1e-6)) / 1e-6 == pytest.approx(2.0, rel=1e-6)
    assert float(mod.reflected_overpressure(1e9)) / 1e9 == pytest.approx(8.0, rel=1e-5)
    assert float(mod.reflected_ratio(1e-6)) == pytest.approx(2.0, rel=1e-6)
    for g in (1.2, 1.4, 5 / 3):
        assert float(mod.reflected_ratio(1e12, mod.P0, g)) == pytest.approx((3 * g - 1) / (g - 1), rel=1e-6)
    ps = np.logspace(-1, 4, 40)
    cr = np.asarray(mod.reflected_ratio(ps))
    assert np.all(np.diff(cr) > 0)
    assert np.allclose(cr, np.asarray(mod.reflected_overpressure(ps)) / ps, rtol=1e-12)


def test_reflected_ratio_matches_two_shock_calculation():
    """Independent check: solve the reflected shock that brings the gas behind the incident
    shock to rest at a rigid wall, then compare (p5 − p1)/(p2 − p1) with reflected_ratio."""
    for g in (1.4, 1.2):
        for M in (1.1, 1.6, 3.0):
            j = mod.shock_jump(M, g)
            p2, u2 = float(j["p"]), float(j["u_over_a1"])          # p1 = a1 = 1
            a2 = np.sqrt(float(j["T"]))
            MR = brentq(lambda m: a2 * 2 / (g + 1) * (m - 1 / m) - u2, 1.0 + 1e-12, 50)
            p5 = p2 * (1 + 2 * g / (g + 1) * (MR ** 2 - 1))
            ps = p2 - 1
            assert float(mod.reflected_ratio(ps, 1.0, g)) == pytest.approx((p5 - 1) / ps, rel=1e-8)


# ------------------------------------------------------------------ Kinney–Graham & scaling
def test_kinney_graham_values():
    # values of the published fits (same expressions as sims/common/blast.js)
    assert float(mod.kg_overpressure_ratio(1.0)) == pytest.approx(9.95598, rel=1e-5)
    assert float(mod.kg_overpressure_ratio(10.0)) == pytest.approx(0.0985479, rel=1e-5)
    assert float(mod.kg_duration_scaled(2.0)) == pytest.approx(1.169953, rel=1e-5)
    assert float(mod.kg_impulse_scaled(5.0)) == pytest.approx(0.388805, rel=1e-5)
    Z = np.logspace(-1, 2, 200)
    assert np.all(np.diff(np.asarray(mod.kg_overpressure_ratio(Z))) < 0)
    assert np.all(np.diff(np.asarray(mod.kg_impulse_scaled(Z))) < 0)


def test_predict_matches_lesson_01_4():
    r = mod.predict(10.0, 15.0)
    assert r["ps"] == pytest.approx(16.74, abs=0.01)
    assert r["pr"] == pytest.approx(35.8, abs=0.05)
    assert r["i"] == pytest.approx(60.5, abs=0.1)
    assert r["ir"] == pytest.approx(129.4, abs=0.2)
    assert r["i"] == pytest.approx(r["i_fit"], rel=1e-6)   # b is chosen to honour the impulse fit


def test_hopkinson_cranz_scaling():
    base = mod.predict(1.0, 4.0)
    for k in (0.1, 8.0, 1000.0):
        s = np.cbrt(k)
        r = mod.predict(k, 4.0 * s)
        assert r["Z"] == pytest.approx(base["Z"], rel=1e-12)
        assert r["ps"] == pytest.approx(base["ps"], rel=1e-10)
        assert r["td"] == pytest.approx(base["td"] * s, rel=1e-8)
        assert r["i"] == pytest.approx(base["i"] * s, rel=1e-8)
        assert r["ta"] == pytest.approx(base["ta"] * s, rel=1e-8)


def test_sachs_scaling():
    """At fixed Sachs-scaled distance: ps/p0, td a0 p0^(1/3)/W^(1/3), i a0/(p0^(2/3) W^(1/3))
    and ta a0 p0^(1/3)/W^(1/3) are invariant."""
    rng = np.random.default_rng(1)
    ref = None
    for _ in range(6):
        W = 10 ** rng.uniform(-1, 3)
        p0 = rng.uniform(50, 110)
        a0 = rng.uniform(300, 360)
        R = 3.0 * np.cbrt(W) / np.cbrt(p0 / mod.P0)            # Z = 3 in every case
        r = mod.predict(W, R, p0=p0, a0=a0)
        groups = np.array([r["ps"] / p0,
                           r["td"] * a0 * np.cbrt(p0) / np.cbrt(W),
                           r["i"] * a0 / (p0 ** (2 / 3) * np.cbrt(W)),
                           r["ta"] * a0 * np.cbrt(p0) / np.cbrt(W)])
        assert r["Z"] == pytest.approx(3.0, rel=1e-12)
        if ref is None:
            ref = groups
        assert np.allclose(groups, ref, rtol=1e-9)


# ------------------------------------------------------------------ Friedlander & arrival
def test_friedlander_shape():
    assert float(mod.friedlander(0.0, 20.0, 5.0, 1.3)) == pytest.approx(20.0)
    assert float(mod.friedlander(5.0, 20.0, 5.0, 1.3)) == pytest.approx(0.0, abs=1e-12)
    assert float(mod.friedlander(-1.0, 20.0, 5.0, 1.3)) == 0.0
    assert float(mod.friedlander(7.0, 20.0, 5.0, 1.3)) < 0          # negative phase


@pytest.mark.parametrize("b", [0.05, 0.5, 1.0, 3.0, 12.0])
def test_friedlander_impulse_numeric_vs_analytic(b):
    ana = float(mod.friedlander_impulse(30.0, 4.0, b))
    num = float(mod.friedlander_impulse_numeric(30.0, 4.0, b))
    assert num == pytest.approx(ana, rel=1e-8)
    # b → 0 tends to the triangle ps td / 2
    assert float(mod.friedlander_impulse(30.0, 4.0, 1e-3)) == pytest.approx(60.0, rel=5e-4)


def test_solve_decay_roundtrip():
    for b in (0.3, 1.0, 4.0, 20.0):
        i = float(mod.friedlander_impulse(50.0, 3.0, b))
        assert mod.solve_decay(50.0, 3.0, i) == pytest.approx(b, rel=1e-8)


def test_arrival_time_behaviour():
    R = np.linspace(2, 60, 30)
    ta = np.array([mod.arrival_time(r, 5.0) for r in R])
    assert np.all(np.diff(ta) > 0)
    # the shock is supersonic, so it arrives before sound would
    assert np.all(ta[1:] < R[1:] / mod.A0 * 1000)
    # far field: dt/dR → 1/a0
    slope = (mod.arrival_time(400.0, 5.0) - mod.arrival_time(300.0, 5.0)) / 100.0
    assert slope == pytest.approx(1000 / mod.A0, rel=0.01)
    assert mod.arrival_time(0.01, 5.0) == 0.0


# ------------------------------------------------------------------ Euler solver
def test_exact_riemann_sod_values():
    s = mod.exact_riemann((1.0, 0.0, 1.0), (0.125, 0.0, 0.1))
    assert s["p_star"] == pytest.approx(0.30313, abs=1e-5)
    assert s["u_star"] == pytest.approx(0.92745, abs=1e-5)
    assert s["shock_R"] == pytest.approx(1.75216, abs=1e-5)
    assert s["rho_star_L"] == pytest.approx(0.42632, abs=1e-5)
    assert s["rho_star_R"] == pytest.approx(0.26557, abs=1e-5)


def test_hll_flux_consistency():
    U = mod.prim_to_cons(np.array([1.0, 0.3]), np.array([0.5, -2.0]), np.array([1.0, 0.2]))
    assert np.allclose(mod.hll_flux(U, U), mod.euler_flux(U), rtol=1e-13, atol=1e-13)
    # supersonic to the right: upwind flux is the left flux
    UL = mod.prim_to_cons(np.array([1.0]), np.array([5.0]), np.array([1.0]))
    UR = mod.prim_to_cons(np.array([0.5]), np.array([5.0]), np.array([0.8]))
    assert np.allclose(mod.hll_flux(UL, UR), mod.euler_flux(UL))


def test_sod_against_exact():
    x, rho, u, p, dx = mod.sod_initial(400)
    r, v, pp, n = mod.euler_solve(rho, u, p, dx, 0.2, cfl=0.5)
    ex = mod.exact_riemann((1.0, 0.0, 1.0), (0.125, 0.0, 0.1))
    re, ue, pe = mod.sample_riemann(ex, (x - 0.5) / 0.2)
    assert np.mean(np.abs(r - re)) < 0.012        # first-order HLL, N = 400: ≈ 0.0075
    assert np.mean(np.abs(pp - pe)) < 0.010
    # star-region plateau values
    plateau = (x > 0.72) & (x < 0.80)
    assert np.median(pp[plateau]) == pytest.approx(0.30313, rel=0.01)
    assert np.median(v[plateau]) == pytest.approx(0.92745, rel=0.01)
    # shock located near 0.5 + 0.2·1.7522 = 0.850
    jump = x[np.argmin(np.diff(pp))]
    assert abs(jump - 0.850) < 0.01
    # CFL: roughly t·max speed/(cfl·dx) steps
    assert 250 < n < 500


def test_conservation_periodic():
    n = 256
    dx = 1.0 / n
    x = (np.arange(n) + 0.5) * dx
    rho = 1 + 0.5 * np.sin(2 * np.pi * x)
    u = 0.3 * np.cos(2 * np.pi * x)
    p = 1 + 0.8 * (x > 0.5)                      # includes a discontinuity
    U0 = mod.prim_to_cons(rho, u, p).sum(axis=1) * dx
    r, v, pp, _ = mod.euler_solve(rho, u, p, dx, 0.5, bc="periodic")
    U1 = mod.prim_to_cons(r, v, pp).sum(axis=1) * dx
    assert np.allclose(U1, U0, rtol=1e-12, atol=1e-13)
    assert np.all(r > 0) and np.all(pp > 0)


def test_weak_pulse_travels_at_sound_speed():
    n = 2000
    dx = 4.0 / n
    x = (np.arange(n) + 0.5) * dx
    p = 1 + 0.01 * np.exp(-((x - 1.0) / 0.1) ** 2)
    _, _, pp, _ = mod.euler_solve(np.ones(n), np.zeros(n), p, dx, 2.0)
    right = x > 1.5
    speed = (x[right][np.argmax(pp[right])] - 1.0) / 2.0
    assert speed == pytest.approx(np.sqrt(G), rel=0.01)


# ------------------------------------------------------------------ plotting script
def test_plot_script_writes_figures(tmp_path):
    pytest.importorskip("matplotlib")
    spec = importlib.util.spec_from_file_location("plot_blastwave", _ROOT / "plot_blastwave.py")
    plots = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(plots)
    files = plots.make_plots(mod, tmp_path, sod_cells=100)
    names = {pathlib.Path(f).name for f in files}
    assert {"p_t.png", "p_Z.png", "i_Z.png", "sod.png"} <= names
    for f in files:
        assert pathlib.Path(f).stat().st_size > 1000
