"""Tests for Project P03 — Bayesian sensor fusion (`bayesfusion`).

Run against your starter:        python -m pytest projects/p03-bayesian-fusion
Run against the reference:       EOD_SOLUTION=1 python -m pytest projects/p03-bayesian-fusion
"""
import os, sys, pathlib
_ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_ROOT / ("solution" if os.environ.get("EOD_SOLUTION") else "starter")))
import bayesfusion as mod  # noqa: E402

import numpy as np  # noqa: E402
import pytest  # noqa: E402
from scipy import stats  # noqa: E402


# ------------------------------------------------------------------ Bayes & inverse sensor models
def test_fuse_ci_lesson_value():
    assert mod.fuse_ci(0.01, [5, 8, 3]) == pytest.approx(0.548, abs=1e-3)
    assert mod.fuse_ci(0.3, [1, 1, 1]) == pytest.approx(0.3)
    # order does not matter
    assert mod.fuse_ci(0.01, [3, 5, 8]) == pytest.approx(mod.fuse_ci(0.01, [8, 3, 5]))


@pytest.mark.parametrize("p, pd, pf", [(0.02, 0.9, 0.1), (0.3, 0.95, 0.3), (0.7, 0.6, 0.4)])
def test_single_binary_sensor_reproduces_bayes(p, pd, pf):
    for z in (True, False):
        g = mod.LogOddsGrid(np.full((3, 4), p))
        delta = np.zeros((3, 4))
        delta[1, 2] = mod.llr_binary(z, pd, pf)
        post = g.update(delta).posterior()
        like1, like0 = (pd, pf) if z else (1 - pd, 1 - pf)
        bayes = p * like1 / (p * like1 + (1 - p) * like0)
        assert post[1, 2] == pytest.approx(bayes, rel=1e-12)
        assert post[0, 0] == pytest.approx(p, rel=1e-12)


def test_single_gaussian_sensor_reproduces_bayes():
    p, mu, sd = 0.1, 1.7, 0.8
    s = np.linspace(-3, 5, 17)
    post = mod.sigmoid(mod.logit(p) + mod.llr_gaussian(s, mu, sd))
    f1, f0 = stats.norm.pdf(s, mu, sd), stats.norm.pdf(s, 0, sd)
    assert np.allclose(post, p * f1 / (p * f1 + (1 - p) * f0), rtol=1e-12)
    # a single sensor: joint and naive coincide and equal the scalar LLR
    C = np.array([[sd ** 2]])
    assert np.allclose(mod.llr_joint(s[:, None], [mu], C), mod.llr_gaussian(s, mu, sd))
    assert np.allclose(mod.llr_naive(s[:, None], [mu], C), mod.llr_gaussian(s, mu, sd))


def test_grid_strip_example_and_kernel_placement():
    # lesson 05.6 §5: 1-D strip, prior 0.02, full-strip footprint LRs
    g = mod.LogOddsGrid(np.full(5, 0.02))
    g.update(np.log([1, 1.5, 6, 1.5, 1]))
    g.update(np.log([1, 1, 1.5, 5, 1.5]))
    assert np.allclose(g.posterior(), [0.02, 0.03, 0.155, 0.133, 0.03], atol=1e-3)
    # the same second reading as a 3-wide kernel centred on cell index 3
    h = mod.LogOddsGrid(np.full(5, 0.02))
    h.update(np.log([1, 1.5, 6, 1.5, 1]))
    h.update(np.log([1.5, 5, 1.5]), center=(3,))
    assert np.allclose(h.posterior(), g.posterior(), rtol=1e-12)
    # kernels are clipped at the border
    k = mod.LogOddsGrid(np.full((4, 4), 0.1))
    k.update(np.ones((3, 3)), center=(0, 0))
    l = mod.logit(k.posterior())
    assert np.allclose(l[:2, :2], mod.logit(0.1) + 1)
    assert np.allclose(l[2:, :], mod.logit(0.1)) and np.allclose(l[:, 2:], mod.logit(0.1))


def test_grid_clamping():
    g = mod.LogOddsGrid(np.full(3, 0.02), lmin=-8, lmax=3)
    for _ in range(10):
        g.update(np.array([np.log(6), 0, -5.0]))
    l = mod.logit(g.posterior())
    assert l[0] == pytest.approx(3.0)
    assert l[2] == pytest.approx(-8.0)


def test_footprint_llr():
    k = np.array([0.0, 0.5, 1.0])
    a = mod.footprint_llr(True, 0.9, 0.1, k)
    s = mod.footprint_llr(False, 0.9, 0.1, k)
    assert a[0] == pytest.approx(0.0) and s[0] == pytest.approx(0.0)
    assert a[2] == pytest.approx(np.log(9.0))
    assert s[2] == pytest.approx(np.log(0.1 / 0.9))
    assert a[1] == pytest.approx(np.log(0.5 / 0.1))
    assert 0 < a[1] < a[2] and s[2] < s[1] < 0


# ------------------------------------------------------------------ correlated errors
def test_equicorrelated_closed_form():
    s = np.full(3, 1.5)
    C = mod.equicorr_cov(3, 0.6)
    assert mod.llr_naive(s, s, C) == pytest.approx(3.375)
    assert mod.llr_joint(s, s, C) == pytest.approx(1.534, abs=1e-3)
    rng = np.random.default_rng(0)
    for n, rho in ((2, 0.3), (5, 0.3), (4, 0.8)):
        C = mod.equicorr_cov(n, rho)
        S = rng.normal(0.7, 1.2, size=(50, n))
        mu = np.full(n, 1.2)
        ratio = mod.llr_naive(S, mu, C) / mod.llr_joint(S, mu, C)
        assert np.allclose(ratio, mod.overconfidence_factor(n, rho), rtol=1e-10)
    # ρ = 0: identical
    C0 = mod.equicorr_cov(4, 0.0)
    S = rng.normal(size=(20, 4))
    assert np.allclose(mod.llr_naive(S, np.ones(4), C0), mod.llr_joint(S, np.ones(4), C0))


def test_naive_fusion_is_overconfident_joint_is_calibrated():
    rng = np.random.default_rng(1)
    n, prior, mu = 200000, 0.05, np.full(3, 1.5)
    C = mod.equicorr_cov(3, 0.6)
    truth = rng.random(n) < prior
    S = mod.simulate_correlated_scores(truth, mu, C, rng)
    pn = mod.fuse_scores(prior, S, mu, C, "naive")
    pj = mod.fuse_scores(prior, S, mu, C, "joint")
    # naive: cells it calls > 0.9 are hazardous far less often than claimed
    hi = pn > 0.9
    assert hi.sum() > 1000
    assert truth[hi].mean() < pn[hi].mean() - 0.25
    # joint: reliability within Monte-Carlo error in every well-populated bin
    mp, fr, cnt = mod.calibration_curve(pj, truth, 10)
    for m_, f_, c_ in zip(mp, fr, cnt):
        if c_ >= 200:
            assert abs(m_ - f_) < 4 * np.sqrt(m_ * (1 - m_) / c_) + 0.01
    # and the correctly specified model scores better
    assert mod.log_loss(pj, truth) < mod.log_loss(pn, truth)
    assert mod.brier(pj, truth) < mod.brier(pn, truth)


# ------------------------------------------------------------------ information gain
def test_info_gain_binary_values_and_enumeration():
    assert float(mod.info_gain_binary(0.2, 0.9, 0.1)) == pytest.approx(0.358, abs=1e-3)
    assert float(mod.info_gain_binary(0.2, 0.95, 0.3)) == pytest.approx(0.224, abs=1e-3)
    # check against H(X) − E_Z[H(X|Z)] by enumerating z
    for p, pd, pf in ((0.1, 0.8, 0.2), (0.5, 0.99, 0.4), (0.9, 0.3, 0.1)):
        pz1 = p * pd + (1 - p) * pf
        post1 = p * pd / pz1
        post0 = p * (1 - pd) / (1 - pz1)
        ref = mod.binary_entropy(p) - (pz1 * mod.binary_entropy(post1) + (1 - pz1) * mod.binary_entropy(post0))
        assert float(mod.info_gain_binary(p, pd, pf)) == pytest.approx(float(ref), abs=1e-12)


def test_info_gain_bounds():
    rng = np.random.default_rng(2)
    p = rng.uniform(0.001, 0.999, 2000)
    pd = rng.uniform(0.01, 0.99, 2000)
    pf = rng.uniform(0.01, 0.99, 2000)
    ig = mod.info_gain_binary(p, pd, pf)
    assert np.all(ig >= -1e-12)
    assert np.all(ig <= mod.binary_entropy(p) + 1e-12)
    assert float(mod.info_gain_binary(0.3, 0.6, 0.6)) == pytest.approx(0.0, abs=1e-12)
    assert float(mod.info_gain_binary(0.3, 1.0, 0.0)) == pytest.approx(float(mod.binary_entropy(0.3)), abs=1e-9)
    for p_, mu in ((0.05, 0.5), (0.3, 1.5), (0.5, 3.0), (0.8, 0.2)):
        g = mod.info_gain_gaussian(p_, mu)
        assert 0 <= g <= float(mod.binary_entropy(p_)) + 1e-12
    assert mod.info_gain_gaussian(0.3, 0.0) == pytest.approx(0.0, abs=1e-9)
    assert mod.info_gain_gaussian(0.3, 20.0) == pytest.approx(float(mod.binary_entropy(0.3)), abs=1e-6)
    gs = [mod.info_gain_gaussian(0.3, m) for m in (0.5, 1.0, 2.0, 4.0)]
    assert np.all(np.diff(gs) > 0)


def test_info_gain_gaussian_matches_monte_carlo():
    rng = np.random.default_rng(3)
    p, mu, sd = 0.25, 1.3, 1.0
    n = 400000
    x = rng.random(n) < p
    s = rng.normal(mu * x, sd)
    post = mod.sigmoid(mod.logit(p) + mod.llr_gaussian(s, mu, sd))
    mc = float(mod.binary_entropy(p)) - np.mean(mod.binary_entropy(post))
    assert mod.info_gain_gaussian(p, mu, sd) == pytest.approx(mc, abs=3e-3)


# ------------------------------------------------------------------ scheduling
def _field(seed):
    rng = np.random.default_rng(seed)
    prior = np.full((15, 15), 0.05)
    prior[3:6, 3:6] = 0.3
    prior[10:13, 8:12] = 0.25
    return prior, rng.random(prior.shape) < prior


SENSORS = [mod.Sensor("A", 0.9, 0.1, 1.0), mod.Sensor("B", 0.75, 0.25, 0.4)]


def test_budget_zero_takes_no_action():
    prior, truth = _field(0)
    out = mod.run_schedule(prior, truth, SENSORS, 0.0, "greedy", np.random.default_rng(0))
    assert out["log"] == [] and out["spent"] == 0.0
    assert np.allclose(out["posterior"], prior)


def test_schedule_respects_budget_and_logs():
    prior, truth = _field(1)
    for policy in ("greedy", "random"):
        out = mod.run_schedule(prior, truth, SENSORS, 25.0, policy, np.random.default_rng(5))
        assert out["spent"] <= 25.0 + 1e-9
        assert out["spent"] == pytest.approx(sum(e[4] for e in out["log"]))
        assert out["spent"] > 25.0 - 1.0          # nothing affordable left (or no useful action)
        for name, idx, z, gain, cost in out["log"]:
            assert name in {"A", "B"} and len(idx) == 2 and gain >= -1e-12


def test_greedy_first_choice_maximises_gain_per_cost():
    prior, truth = _field(2)
    out = mod.run_schedule(prior, truth, SENSORS, 1.0, "greedy", np.random.default_rng(0))
    name, idx, z, gain, cost = out["log"][0]
    best = max(float(np.max(mod.info_gain_binary(prior, s.pd, s.pf))) / s.cost for s in SENSORS)
    assert gain / cost == pytest.approx(best)
    assert prior[idx] == pytest.approx(0.3)


def test_greedy_beats_random():
    ll = {"greedy": [], "random": []}
    br = {"greedy": [], "random": []}
    for seed in range(6):
        prior, truth = _field(seed)
        for policy in ll:
            out = mod.run_schedule(prior, truth, SENSORS, 120.0, policy, np.random.default_rng(100 + seed))
            ll[policy].append(mod.log_loss(out["posterior"], truth))
            br[policy].append(mod.brier(out["posterior"], truth))
    assert np.mean(ll["greedy"]) < 0.9 * np.mean(ll["random"])
    assert np.mean(br["greedy"]) < np.mean(br["random"])
    assert sum(g <= r for g, r in zip(ll["greedy"], ll["random"])) >= 5


# ------------------------------------------------------------------ evaluation metrics
def test_metrics():
    y = np.array([0, 0, 1, 1, 0, 1])
    p = np.array([0.1, 0.4, 0.35, 0.8, 0.2, 0.9])
    assert mod.brier(p, y) == pytest.approx(np.mean((p - y) ** 2))
    assert mod.log_loss(p, y) == pytest.approx(-np.mean(y * np.log(p) + (1 - y) * np.log(1 - p)))
    assert mod.roc_auc(p, y) == pytest.approx(8 / 9)
    assert mod.roc_auc(np.array([0.5, 0.5]), np.array([0, 1])) == pytest.approx(0.5)
    assert mod.log_loss(np.array([0.0, 1.0]), np.array([1, 0])) < 30   # clipped, finite
    mp, fr, cnt = mod.calibration_curve(np.array([0.05, 0.07, 0.95, 1.0]), np.array([0, 1, 1, 1]), 10)
    assert np.allclose(mp, [0.06, 0.975]) and np.allclose(fr, [0.5, 1.0]) and list(cnt) == [2, 2]
