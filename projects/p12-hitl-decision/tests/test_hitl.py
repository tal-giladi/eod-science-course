"""Tests for P12 -- human-in-the-loop decision engine. Run from the repo root:

    python -m pytest projects/p12-hitl-decision             (your starter)
    EOD_SOLUTION=1 python -m pytest projects/p12-hitl-decision   (reference solution)
"""
import os, sys, pathlib
_ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_ROOT / ("solution" if os.environ.get("EOD_SOLUTION") else "starter")))
import hitl as mod  # noqa: E402

import math

import numpy as np
import pytest

# Lesson 07.1 section 4 (two states B/H, actions F/R) -- hand-checked numbers.
L2 = np.array([[20.0, 25.0], [0.0, 1000.0]])
TEST_A = np.array([[0.80, 0.10], [0.20, 0.90]])     # rows o = (-, +); P_fa = 0.2, P_d = 0.90
TEST_B = np.array([[0.80, 0.03], [0.20, 0.97]])     # P_d = 0.97


def _data(n, seed, **kw):
    return mod.IncidentSimulator(**kw).sample(n, np.random.default_rng(seed))


# ---------------------------------------------------------------- calibration
def test_temperature_scaling_reduces_nll_and_recovers_T():
    z, y = _data(6000, 0)
    T = mod.fit_temperature(z, y)
    assert T == pytest.approx(2.5, abs=0.2)
    assert mod.nll(z, y, T) < mod.nll(z, y, 1.0) - 0.05
    zt, yt = _data(6000, 1)                           # held-out data improves as well
    assert mod.nll(zt, yt, T) < mod.nll(zt, yt, 1.0)
    assert (mod.softmax(zt, T).argmax(1) == mod.softmax(zt).argmax(1)).all()   # accuracy invariant
    assert mod.expected_calibration_error(mod.softmax(zt, T), yt) < mod.expected_calibration_error(mod.softmax(zt), yt)


def test_temperature_fit_on_underconfident_logits():
    z, y = _data(6000, 2, temperature=0.5)
    assert mod.fit_temperature(z, y) == pytest.approx(0.5, abs=0.05)


# ---------------------------------------------------------------- conformal
def test_conformal_threshold_hand_case():
    assert mod.conformal_threshold(np.arange(10) / 10, 0.2) == pytest.approx(0.8)   # k = ceil(8.8) = 9
    # exact integer (n+1)(1-alpha) must not be rounded up by floating-point error
    assert mod.conformal_threshold(np.arange(19) / 19, 0.05) == pytest.approx(18 / 19)
    assert mod.min_calibration_size(0.01) == 99 and mod.min_calibration_size(0.05) == 19
    with pytest.warns(RuntimeWarning):
        assert mod.conformal_threshold(np.arange(23) / 23, 0.01) == math.inf


def test_split_conformal_marginal_coverage():
    alpha, n_cal = 0.1, 500
    z, y = _data(20_000, 3)
    P = mod.softmax(z, 2.5)
    rng = np.random.default_rng(4)
    covs = []
    for _ in range(200):
        idx = rng.permutation(len(y))[: 2 * n_cal]
        c, t = idx[:n_cal], idx[n_cal:]
        q = mod.fit_conformal(P[c], y[c], alpha)
        covs.append(mod.coverage(mod.prediction_sets(P[t], q), y[t]))
    mean, se = np.mean(covs), np.std(covs) / math.sqrt(len(covs))
    assert mean >= 1 - alpha - 3 * se
    assert mean <= 1 - alpha + 1 / (n_cal + 1) + 3 * se


def test_class_conditional_coverage_protects_rare_class():
    z, y = _data(40_000, 5)
    P = mod.softmax(z, 2.5)
    c, t = slice(0, 20_000), slice(20_000, None)
    alphas = np.array([0.1, 0.1, 0.02])
    marg = mod.prediction_sets(P[t], mod.fit_conformal(P[c], y[c], 0.1))
    mond = mod.prediction_sets(P[t], mod.fit_conformal(P[c], y[c], class_conditional=True, alphas=alphas))
    cc = mod.class_coverage(mond, y[t])
    n_k = np.bincount(y[t], minlength=3)
    for k in range(3):
        assert cc[k] >= 1 - alphas[k] - 3 * math.sqrt(alphas[k] * (1 - alphas[k]) / n_k[k])
    assert cc[mod.HAZARD] > mod.class_coverage(marg, y[t])[mod.HAZARD]


# ---------------------------------------------------------------- value of information
def test_evpi_evsi_lesson_numbers():
    b = np.array([0.845, 0.155])
    assert mod.evpi(b, L2)[0] == pytest.approx(16.90, abs=0.01)
    assert mod.evsi(b, L2, TEST_A)[0] == pytest.approx(0.0, abs=1e-9)
    assert mod.evsi(b, L2, TEST_B)[0] == pytest.approx(8.99, abs=0.01)
    assert mod.decision_threshold(np.array([[20.0, 20.0, 25.0], [0.0, 0.0, 1000.0]])) == pytest.approx(20 / 995)


def test_evpi_ge_evsi_ge_zero():
    rng = np.random.default_rng(6)
    for _ in range(300):
        K, A, O = rng.integers(2, 5), rng.integers(2, 4), rng.integers(2, 5)
        b = rng.dirichlet(np.ones(K), size=4)
        loss = rng.uniform(0, 100, size=(A, K))
        lik = rng.dirichlet(np.ones(O), size=K).T                # (O, K), columns sum to 1
        vpi, vsi = mod.evpi(b, loss), mod.evsi(b, loss, lik)
        assert (vsi >= -1e-9).all() and (vpi >= vsi - 1e-9).all()
    # a perfect sensor attains EVPI; an uninformative one is worth nothing
    b = rng.dirichlet(np.ones(3), size=5)
    loss = rng.uniform(0, 100, size=(2, 3))
    assert np.allclose(mod.evsi(b, loss, np.eye(3)), mod.evpi(b, loss))
    assert np.allclose(mod.evsi(b, loss, np.full((2, 3), 0.5)), 0.0)


def test_posterior_is_bayes():
    b = np.array([0.845, 0.155])
    post = mod.posterior(b, TEST_B, 1)[0]
    assert post[1] == pytest.approx(0.97 * 0.155 / (0.97 * 0.155 + 0.2 * 0.845))


def test_bellman_values_consistent():
    prob = mod.default_problem()
    B = mod.softmax(_data(500, 7)[0], 2.5)
    commit = mod.commit_losses(B, prob.loss).min(axis=1)
    v0, v1, v2 = (mod.value(B, prob, h) for h in (0, 1, 2))
    assert (v0 <= commit + 1e-9).all()
    assert (v1 <= v0 + 1e-9).all() and (v2 <= v1 + 1e-9).all()      # more options never hurt
    no_human = mod.DecisionProblem(prob.loss, prob.sensors, None, 0)
    assert np.allclose(mod.value(B, no_human, 0), commit)            # h = 0, no human -> one-shot rule
    d = mod.decide(B, prob, 2)
    assert set(np.unique(d)) <= {mod.COMMIT, mod.ESCALATE, 2}
    # gathering is chosen only where it beats both committing and escalating
    Q = mod.q_values(B, prob, 2)
    g = d == 2
    assert (Q[g, 2] < Q[g, mod.COMMIT]).all() and (Q[g, 2] < Q[g, mod.ESCALATE]).all()


def test_free_information_is_always_gathered_when_useful():
    prob = mod.default_problem()
    prob.sensors[0].cost = 0.0
    b = np.array([[0.6, 0.3, 0.1]])
    if mod.evsi(b, prob.loss, prob.sensors[0].likelihood)[0] > 0:
        assert mod.decide(b, prob, 1)[0] == 2


# ---------------------------------------------------------------- policies on the simulator
@pytest.fixture(scope="module")
def pipeline():
    return mod.run_pipeline(n_fit=3000, n_cal=3000, n_test=6000, alpha=0.1, alpha_hazard=0.02, seed=0)


def test_voi_never_worse_than_threshold_only(pipeline):
    prob = mod.default_problem()
    z, y = _data(4000, 8)
    B = mod.softmax(z, 2.5)
    # exact, per incident: the Bellman value never exceeds the one-shot threshold rule
    assert (mod.value(B, prob, prob.max_gathers) <= mod.commit_losses(B, prob.loss).min(1) + 1e-9).all()
    # realised on the simulator (common random numbers)
    res = pipeline["policies"]
    voi, thr = res["voi"], res["threshold"]
    assert voi["mean_cost"] <= thr["mean_cost"] + 2 * math.hypot(voi["se_cost"], thr["se_cost"])
    assert voi["mean_cost"] <= res["always_ask"]["mean_cost"]


def test_baselines_behave(pipeline):
    res = pipeline["policies"]
    assert res["always_ask"]["workload"] == 1.0 and res["threshold"]["workload"] == 0.0
    assert res["threshold"]["mean_gathers"] == 0.0
    assert res["voi"]["workload"] < 1.0
    assert res["always_ask"]["hazard_auto_release_rate"] == 0.0


def test_conformal_guard_bounds_hazard_auto_release(pipeline):
    res = pipeline["policies"]["voi_guarded"]
    n_haz = 6000 * 0.1
    a_h = 0.02
    assert res["hazard_auto_release_rate"] <= a_h + 3 * math.sqrt(a_h * (1 - a_h) / n_haz)
    assert res["workload"] >= pipeline["policies"]["voi"]["workload"]   # the guarantee costs reviews
    assert pipeline["class_coverage"][mod.HAZARD] >= 1 - a_h - 3 * math.sqrt(a_h * (1 - a_h) / n_haz)


def test_pipeline_reports_calibration(pipeline):
    assert pipeline["T"] == pytest.approx(2.5, abs=0.2)
    assert pipeline["nll_calibrated"] < pipeline["nll_raw"]
    assert 1.0 <= pipeline["mean_set_size"] <= 3.0


def test_simulation_deterministic():
    kw = dict(n_fit=500, n_cal=1000, n_test=500, alpha_hazard=0.05, seed=3)
    a, b = mod.run_pipeline(**kw), mod.run_pipeline(**kw)
    assert a["policies"] == b["policies"] and a["T"] == b["T"]
