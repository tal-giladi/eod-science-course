"""Tests for Project P02 — sensor-noise simulator (`sensornoise`).

Run against your starter:        python -m pytest projects/p02-sensor-noise
Run against the reference:       EOD_SOLUTION=1 python -m pytest projects/p02-sensor-noise
"""
import os, sys, pathlib
_ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_ROOT / ("solution" if os.environ.get("EOD_SOLUTION") else "starter")))
import sensornoise as mod  # noqa: E402

import numpy as np  # noqa: E402
import pytest  # noqa: E402
from scipy import stats  # noqa: E402


def hanley_mcneil_se(auc, n0, n1):
    q1 = auc / (2 - auc)
    q2 = 2 * auc ** 2 / (1 + auc)
    return np.sqrt((auc * (1 - auc) + (n1 - 1) * (q1 - auc ** 2) + (n0 - 1) * (q2 - auc ** 2)) / (n0 * n1))


# ------------------------------------------------------------------ sensor models
def test_gaussian_sensor_moments():
    rng = np.random.default_rng(0)
    s = mod.GaussianSensor(mu0=0.0, mu1=2.0, noise_sd=0.8, bias_sd=0.6, h1_scale=1.5)
    assert s.sd0 == pytest.approx(1.0)
    assert s.d_prime == pytest.approx(2.0)
    truth = np.r_[np.zeros(20000, bool), np.ones(20000, bool)]
    z = s.measure(truth, n_repeats=1, rng=rng)
    assert z.shape == (40000, 1)
    z0, z1 = z[~truth, 0], z[truth, 0]
    assert z0.mean() == pytest.approx(0.0, abs=0.03)
    assert z1.mean() == pytest.approx(2.0, abs=0.04)
    assert z0.std() == pytest.approx(1.0, rel=0.03)
    assert z1.std() == pytest.approx(1.5, rel=0.03)


def test_measure_is_reproducible():
    s = mod.GaussianSensor(bias_sd=0.5)
    t = np.array([True, False, True])
    a = s.measure(t, 4, np.random.default_rng(7))
    b = s.measure(t, 4, np.random.default_rng(7))
    assert np.array_equal(a, b)


def test_correlated_repeats_do_not_beat_the_bias():
    """Averaging k looks at one place removes noise but not the persistent bias."""
    rng = np.random.default_rng(3)
    bias_sd, noise_sd = 0.5, 1.0
    s = mod.GaussianSensor(mu0=0.0, noise_sd=noise_sd, bias_sd=bias_sd)
    n_loc = 20000
    for k in (1, 4, 50):
        err = s.measure(np.zeros(n_loc, bool), k, rng).mean(axis=1)
        v = err.var()
        v_theory = mod.mean_of_repeats_variance(bias_sd, noise_sd, k)
        assert v_theory == pytest.approx(bias_sd ** 2 + noise_sd ** 2 / k)
        assert v == pytest.approx(v_theory, rel=0.05)
        assert v > 0.9 * bias_sd ** 2
    # repeats are correlated: within-location correlation = bias²/(bias²+noise²) = 0.2
    z = s.measure(np.zeros(n_loc, bool), 2, rng)
    assert np.corrcoef(z[:, 0], z[:, 1])[0, 1] == pytest.approx(0.2, abs=0.03)
    # effective looks saturate at 1/ρ = 5
    assert mod.effective_looks(bias_sd, noise_sd, 1) == pytest.approx(1.0)
    assert mod.effective_looks(bias_sd, noise_sd, 10 ** 6) == pytest.approx(5.0, rel=1e-4)
    # with no bias, repeats are independent
    assert mod.effective_looks(0.0, 1.0, 7) == pytest.approx(7.0)


def test_repeats_improve_auc_only_up_to_the_bias_limit():
    rng = np.random.default_rng(11)
    s = mod.GaussianSensor(mu1=1.0, noise_sd=1.0, bias_sd=0.5)
    auc1 = mod.monte_carlo_roc(s, 3000, 3000, rng, n_repeats=1)["auc"]
    auc50 = mod.monte_carlo_roc(s, 3000, 3000, rng, n_repeats=50)["auc"]
    # limit: d' = 1 / sqrt(bias² + noise²/50)  → AUC = Φ(d'/√2)
    lim = mod.binormal_auc(1.0 / np.sqrt(0.25 + 1 / 50))
    never = mod.binormal_auc(1.0 / np.sqrt(1 / 50))     # what independent looks would promise
    assert auc50 > auc1 + 0.1
    assert auc50 == pytest.approx(lim, abs=0.02)
    assert auc50 < never - 0.05


def test_poisson_clutter_counts_and_positions():
    rng = np.random.default_rng(5)
    c = mod.PoissonClutter(0.02)
    W, H = 50.0, 40.0
    assert c.expected_count(W * H) == pytest.approx(40.0)
    counts = []
    xs = []
    for _ in range(1500):
        pts = c.sample(W, H, rng)
        assert pts.ndim == 2 and pts.shape[1] == 2
        counts.append(len(pts))
        xs.append(pts[:, 0])
    counts = np.array(counts)
    xs = np.concatenate(xs)
    se = np.sqrt(40.0 / counts.size)
    assert abs(counts.mean() - 40.0) < 4 * se
    assert counts.var() / counts.mean() == pytest.approx(1.0, abs=0.12)    # Poisson dispersion
    assert xs.min() >= 0 and xs.max() <= W
    assert xs.mean() == pytest.approx(W / 2, rel=0.01)


def test_poisson_rate_ci():
    lo, hi = mod.poisson_rate_ci(0, 1.0)
    assert lo == 0.0 and hi == pytest.approx(3.689, abs=1e-3)
    lo, hi = mod.poisson_rate_ci(12, 200.0)
    assert (lo, hi) == pytest.approx((0.0310, 0.1048), abs=2e-4)
    # Garwood interval is conservative: exact coverage >= 95 % for a range of true means
    for mu in (0.5, 2.0, 7.5, 20.0):
        ks = np.arange(0, int(mu * 5 + 30))
        cov = sum(stats.poisson.pmf(k, mu) for k in ks
                  if mod.poisson_rate_ci(int(k), 1.0)[0] <= mu <= mod.poisson_rate_ci(int(k), 1.0)[1])
        assert cov >= 0.95 - 1e-9


# ------------------------------------------------------------------ Pd vs SNR and range
def test_pd_from_snr():
    assert float(mod.pd_from_snr(-80.0, 0.01)) == pytest.approx(0.01, rel=1e-3)
    assert float(mod.pd_from_snr(30.0, 1e-3)) > 0.9999
    snr = np.linspace(-10, 20, 31)
    assert np.all(np.diff(mod.pd_from_snr(snr, 1e-2)) > 0)
    # Monte-Carlo check: d' = sqrt(SNR), threshold at Pfa
    rng = np.random.default_rng(2)
    snr_db = 10 * np.log10(4.0)              # d' = 2
    thr = mod.threshold_for_pfa(0.05)
    assert thr == pytest.approx(1.6449, abs=1e-4)
    pd_mc = np.mean(rng.normal(2.0, 1.0, 200000) >= thr)
    assert float(mod.pd_from_snr(snr_db, 0.05)) == pytest.approx(pd_mc, abs=0.005)


def test_snr_and_pd_vs_range():
    assert float(mod.snr_at_range(1.0, 20.0)) == pytest.approx(20.0)
    assert float(mod.snr_at_range(2.0, 20.0, path_exponent=4)) == pytest.approx(20 - 12.0412, abs=1e-3)
    assert float(mod.snr_at_range(3.0, 20.0, path_exponent=0, atten_db_per_m=2.0)) == pytest.approx(16.0)
    r = np.linspace(0.5, 6, 40)
    pd = mod.pd_at_range(r, 1e-3, 25.0, r_ref=1.0, path_exponent=4)
    assert np.all(np.diff(pd) <= 1e-15)
    assert pd[-1] < 0.05 and pd[0] > 0.999


# ------------------------------------------------------------------ ROC / AUC
def test_empirical_roc_structure_and_mann_whitney():
    rng = np.random.default_rng(9)
    s0 = np.round(rng.normal(0, 1, 700), 1)      # rounding creates ties
    s1 = np.round(rng.normal(1.2, 1.3, 300), 1)
    pfa, pd, auc = mod.empirical_roc(s0, s1)
    assert pfa[0] == 0 and pd[0] == 0 and pfa[-1] == pytest.approx(1) and pd[-1] == pytest.approx(1)
    assert np.all(np.diff(pfa) >= 0) and np.all(np.diff(pd) >= 0)
    brute = np.mean(s1[:, None] > s0[None, :]) + 0.5 * np.mean(s1[:, None] == s0[None, :])
    assert auc == pytest.approx(brute, abs=1e-12)
    assert mod.auc_mann_whitney(s0, s1) == pytest.approx(brute, abs=1e-12)


def test_empirical_roc_is_fast():
    import time
    rng = np.random.default_rng(1)
    t = time.perf_counter()
    mod.empirical_roc(rng.normal(size=100000), rng.normal(1, 1, 100000))
    assert time.perf_counter() - t < 2.0


@pytest.mark.parametrize("d, sigma", [(2.0, 1.0), (1.5, 1.5), (1.0, 0.7)])
def test_binormal_auc_by_monte_carlo(d, sigma):
    sensor = mod.GaussianSensor(mu0=0.0, mu1=d, noise_sd=0.6, bias_sd=0.8, h1_scale=sigma)
    theory = mod.binormal_auc(d, sigma)
    assert theory == pytest.approx(stats.norm.cdf(d / np.sqrt(1 + sigma ** 2)))
    assert sensor.theoretical_auc() == pytest.approx(theory)
    n0 = n1 = 4000
    r = mod.monte_carlo_roc(sensor, n0, n1, np.random.default_rng(123))
    assert abs(r["auc"] - theory) < 4 * hanley_mcneil_se(theory, n0, n1)


def test_equal_variance_dprime_2():
    assert mod.binormal_auc(2.0) == pytest.approx(0.9214, abs=1e-4)


def test_bootstrap_auc_ci_contains_truth():
    rng = np.random.default_rng(4)
    s0, s1 = rng.normal(0, 1, 800), rng.normal(1.0, 1, 800)
    lo, hi = mod.bootstrap_auc_ci(s0, s1, n_boot=300, rng=rng)
    assert lo < mod.binormal_auc(1.0) < hi
    assert 0.02 < hi - lo < 0.08


# ------------------------------------------------------------------ intervals & coverage
def test_interval_known_values():
    assert mod.clopper_pearson(98, 100) == pytest.approx((0.9296, 0.9976), abs=1e-4)
    assert mod.wilson_interval(98, 100) == pytest.approx((0.9300, 0.9945), abs=1e-4)
    assert mod.clopper_pearson(0, 30)[0] == 0.0 and mod.clopper_pearson(30, 30)[1] == 1.0
    # 50/50 detected: one-sided 95 % lower bound (= two-sided 90 %) is 0.05^(1/50) = 0.942
    assert mod.clopper_pearson(50, 50, conf=0.90)[0] == pytest.approx(0.05 ** (1 / 50), abs=1e-9)


def test_clopper_pearson_coverage_is_guaranteed():
    for n in (20, 50, 200):
        for p in np.linspace(0.02, 0.98, 25):
            assert mod.exact_coverage(mod.clopper_pearson, p, n) >= 0.95 - 1e-9


def test_wilson_coverage_near_nominal_wald_fails_at_high_pd():
    ps = np.linspace(0.05, 0.95, 19)
    wil = [mod.exact_coverage(mod.wilson_interval, p, 50) for p in ps]
    assert np.mean(wil) == pytest.approx(0.95, abs=0.01)
    assert mod.exact_coverage(mod.wald_interval, 0.99, 50) < 0.5          # ≈ 0.39
    assert mod.exact_coverage(mod.clopper_pearson, 0.99, 50) >= 0.95


def test_simulated_coverage_matches_exact():
    rng = np.random.default_rng(8)
    for method in (mod.wilson_interval, mod.clopper_pearson, mod.wald_interval):
        ex = mod.exact_coverage(method, 0.97, 60)
        mc = mod.simulate_coverage(method, 0.97, 60, n_trials=4000, rng=rng)
        assert mc == pytest.approx(ex, abs=4 * np.sqrt(ex * (1 - ex) / 4000) + 1e-3)


def test_empirical_rates():
    s0 = np.array([0.1, 0.5, 0.9, 1.2, -0.3])
    s1 = np.array([1.5, 0.8, 2.2, 1.0])
    r = mod.empirical_rates(s0, s1, 1.0)
    assert (r["k1"], r["n1"], r["k0"], r["n0"]) == (3, 4, 1, 5)
    assert r["pd"] == pytest.approx(0.75) and r["pfa"] == pytest.approx(0.2)
    assert r["pd_ci"] == pytest.approx(mod.clopper_pearson(3, 4))
    assert mod.empirical_rates(s0, s1, 1.0, method=mod.wilson_interval)["pfa_ci"] == \
        pytest.approx(mod.wilson_interval(1, 5))


# ------------------------------------------------------------------ trial planning
def test_n_for_demo():
    assert mod.n_for_demo(0.99) == 299
    assert mod.n_for_demo(0.99, misses_allowed=1) == 473
    assert mod.n_for_demo(0.996) == 748
    assert mod.n_for_demo(0.9) == 29
    for p0 in (0.9, 0.95, 0.99):
        n = mod.n_for_demo(p0)
        assert n == int(np.ceil(np.log(0.05) / np.log(p0)))
        # passing is unlikely (≤ 5 %) if Pd were only p0, but n − 1 would not be enough
        assert mod.demo_pass_probability(p0, n) <= 0.05
        assert mod.demo_pass_probability(p0, n - 1) > 0.05
