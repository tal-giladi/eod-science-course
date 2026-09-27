"""Tests for P04 localization. Run: python -m pytest projects/p04-localization  (EOD_SOLUTION=1 for the reference)."""
import os, sys, pathlib
_ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_ROOT / ("solution" if os.environ.get("EOD_SOLUTION") else "starter")))
import localization as mod  # noqa: E402

import numpy as np  # noqa: E402
import pytest  # noqa: E402


def _num_jac(fun, x, eps=1e-6):
    x = np.asarray(x, dtype=float)
    cols = []
    for i in range(len(x)):
        d = np.zeros_like(x)
        d[i] = eps
        diff = fun(x + d) - fun(x - d)
        diff[-1] = mod.wrap_angle(diff[-1])        # last component is an angle in both models
        cols.append(diff / (2 * eps))
    return np.column_stack(cols)


# ---------------------------------------------------------------- models
def test_motion_model_and_jacobian():
    x, u, dt = np.array([1.0, -2.0, 0.7]), np.array([0.5, 0.2]), 0.1
    fx = mod.motion_model(x, u, dt)
    assert np.allclose(fx, [1 + 0.05 * np.cos(0.7), -2 + 0.05 * np.sin(0.7), 0.72])
    assert np.isclose(mod.motion_model(np.array([0, 0, 3.1]), [0.0, 1.0], 0.1)[2], 3.2 - 2 * np.pi)
    F = mod.motion_jacobian(x, u, dt)
    assert np.allclose(F, _num_jac(lambda s: mod.motion_model(s, u, dt), x), atol=1e-7)


def test_measurement_model_lesson_example():
    # lesson 06.6 §3: robot (1, 2, 30 deg), landmark (4, 6): r = 5, bearing 23.13 deg
    x, lm = np.array([1.0, 2.0, np.radians(30)]), np.array([4.0, 6.0])
    z = mod.measurement_model(x, lm)
    assert np.allclose(z, [5.0, np.radians(53.130102354 - 30)], atol=1e-9)
    H = mod.measurement_jacobian(x, lm)
    assert np.allclose(H, [[-0.6, -0.8, 0.0], [0.16, -0.12, -1.0]])
    for x in (np.array([0.3, -1.0, 2.9]), np.array([6.0, 7.5, -3.0])):
        assert np.allclose(mod.measurement_jacobian(x, lm),
                           _num_jac(lambda s: mod.measurement_model(s, lm), x), atol=1e-6)


# ---------------------------------------------------------------- EKF == KF when linear
def test_ekf_equals_kf_on_linear_gaussian_model():
    rng = np.random.default_rng(4)
    dt = 0.1
    A = np.array([[1, 0, dt, 0], [0, 1, 0, dt], [0, 0, 1, 0], [0, 0, 0, 1.0]])
    B = np.array([[0.5 * dt * dt, 0], [0, 0.5 * dt * dt], [dt, 0], [0, dt]])
    C = np.array([[1.0, 0, 0, 0], [0, 1.0, 0, 0]])
    Q, R = 0.01 * np.eye(4), 0.25 * np.eye(2)
    m_kf = m_ekf = np.zeros(4)
    P_kf = P_ekf = np.eye(4)
    for _ in range(50):
        u, z = rng.normal(size=2), rng.normal(size=2)
        m_kf, P_kf = mod.kf_predict(m_kf, P_kf, A, B, u, Q)
        m_kf, P_kf, nis_kf = mod.kf_update(m_kf, P_kf, z, C, R)
        m_ekf, P_ekf = mod.ekf_predict(m_ekf, P_ekf, lambda m: A @ m + B @ u, A, Q)
        m_ekf, P_ekf, nis_ekf = mod.ekf_update(m_ekf, P_ekf, z, lambda m: C @ m, C, R)
        assert np.allclose(m_kf, m_ekf, atol=1e-12) and np.allclose(P_kf, P_ekf, atol=1e-12)
        assert np.isclose(nis_kf, nis_ekf)
    assert np.allclose(P_kf, P_kf.T) and np.all(np.linalg.eigvalsh(P_kf) > 0)


def test_kf_update_scalar_by_hand():
    mu, P, nis = mod.kf_update(np.array([0.0]), np.array([[4.0]]), np.array([2.0]), np.eye(1), np.array([[1.0]]))
    assert np.isclose(mu[0], 1.6) and np.isclose(P[0, 0], 0.8) and np.isclose(nis, 0.8)


def test_ekf_noise_free_tracks_truth():
    rng = np.random.default_rng(0)
    tiny = 1e-12
    run = mod.simulate(mod.LESSON_LANDMARKS, np.tile([0.5, 0.2], (200, 1)), 0.1, tiny * np.eye(3),
                       tiny * np.eye(2), np.zeros(3), rng)
    res = mod.run_ekf(run, np.zeros(3), 1e-9 * np.eye(3), 1e-9 * np.eye(3), 1e-9 * np.eye(2))
    err = res["est"] - run.truth
    err[:, 2] = mod.wrap_angle(err[:, 2])
    assert np.max(np.abs(err)) < 1e-5


# ---------------------------------------------------------------- consistency
def test_nees_definition():
    P = np.diag([4.0, 1.0, 0.25])
    assert np.isclose(mod.nees([2.0, 1.0, 0.5], [0, 0, 0], P), 1 + 1 + 1)
    assert np.isclose(mod.nees([0, 0, np.pi - 0.1], [0, 0, -np.pi + 0.1], np.eye(3)), 0.04)  # wrapped


def test_monte_carlo_nees_within_chi2_bounds():
    mc = mod.monte_carlo_nees(n_runs=50, n_steps=300, seed=0, q_scale=1.0)
    lo, hi = mc["band"]
    assert np.isclose(lo, 2.36, atol=0.01) and np.isclose(hi, 3.72, atol=0.01)
    assert lo < mc["mean_nees"].mean() < hi                  # lesson 06.6: 2.8-3.3
    assert mc["fraction_inside"] > 0.85                       # ~95 % expected
    assert 1.8 < mc["mean_nis"] < 2.2                         # NIS ~ chi2(2)


def test_understated_q_is_detected():
    mc = mod.monte_carlo_nees(n_runs=20, n_steps=200, seed=1, q_scale=1 / 20)
    assert mc["mean_nees"][20:].mean() > 10                  # lesson: ~27, grossly overconfident
    assert mc["fraction_inside"] < 0.2


# ---------------------------------------------------------------- particle filter
def test_systematic_resample_counts():
    rng = np.random.default_rng(2)
    w = rng.random(1000) ** 3
    w /= w.sum()
    idx = mod.systematic_resample(w, rng)
    assert idx.shape == (1000,) and idx.min() >= 0 and idx.max() < 1000
    counts = np.bincount(idx, minlength=1000)
    assert np.all(counts >= np.floor(1000 * w) - 1e-9) and np.all(counts <= np.ceil(1000 * w) + 1e-9)
    assert np.all(np.diff(idx) >= 0)


@pytest.mark.parametrize("seed", [0, 2, 4])
def test_pf_converges_from_wide_prior(seed):
    rng = np.random.default_rng(seed)
    run = mod.simulate(mod.LESSON_LANDMARKS, np.tile([0.5, 0.2], (200, 1)), 0.1, mod.LESSON_Q,
                       mod.LESSON_R, np.array([1.0, 2.0, 0.5]), rng)
    n = 2000                                                  # global localisation: uniform prior
    parts = np.column_stack([rng.uniform(-4, 10, n), rng.uniform(-3, 10, n), rng.uniform(-np.pi, np.pi, n)])
    res = mod.run_pf(run, parts, mod.LESSON_Q, 4 * mod.LESSON_R, rng)
    err = np.hypot(*(res["est"][:, :2] - run.truth[:, :2]).T)
    assert err[0] > 1.5                                       # starts lost
    assert err[-50:].max() < 0.4                              # ends localised
    head = np.abs(mod.wrap_angle(res["est"][-50:, 2] - run.truth[-50:, 2]))
    assert head.max() < 0.15


def test_particle_filter_estimate_circular_mean():
    parts = np.array([[0.0, 0.0, np.pi - 0.1], [2.0, 0.0, -np.pi + 0.1]])
    pf = mod.ParticleFilter(parts, 0.01 * np.eye(3), 0.01 * np.eye(2), np.random.default_rng(0))
    mu, cov = pf.estimate()
    assert np.isclose(mu[0], 1.0) and np.isclose(abs(mu[2]), np.pi)
    assert np.isclose(cov[0, 0], 1.0) and np.isclose(cov[2, 2], 0.01)


# ---------------------------------------------------------------- comparison
def test_landmarks_beat_dead_reckoning():
    out = mod.comparison_experiment(seed=1, n_steps=600, n_particles=1000)
    r = out["rmse"]
    assert r["ekf"] < 0.2 and r["pf"] < 0.2
    assert r["ekf"] < 0.25 * r["dead_reckoning"] and r["pf"] < 0.25 * r["dead_reckoning"]


def test_with_robotsim2d_if_available():
    """Optional cross-check with the P05 simulator: truth from skid-steer kinematics with slip and
    biased wheel odometry (model chi wrong), landmarks observed from the true pose."""
    p05 = _ROOT.parent / "p05-robot-sim" / "solution"
    if not (p05 / "robotsim2d.py").exists():
        pytest.skip("P05 not present")
    sys.path.insert(0, str(p05))
    rs = pytest.importorskip("robotsim2d")
    rng = np.random.default_rng(5)
    B, chi_true, chi_model, dt = 0.5, 1.6, 1.4, 0.05
    odo = rs.WheelOdometry(B, chi_model, scale_bias=(0.02, -0.01), sigma=0.005, rng=rng)
    truth, ekf = np.zeros(3), mod.EKF(np.zeros(3), 1e-4 * np.eye(3),
                                      np.diag([0.01 ** 2, 0.01 ** 2, np.radians(1.0) ** 2]), mod.LESSON_R)
    lms = mod.LESSON_LANDMARKS
    t_err, o_err = [], []
    for k in range(1200):
        vL, vR = rs.track_speeds(0.5, 0.2 * np.sin(0.01 * k) + 0.1, B, chi_true)
        truth = rs.body_twist_step(truth, *rs.skid_steer_twist(vL, vR, B, chi_true), dt)
        mL, mR = odo.measure(vL, vR)
        vx, _, w = rs.skid_steer_twist(mL, mR, B, chi_model)
        odo.pose = rs.body_twist_step(odo.pose, vx, 0.0, w, dt)
        ekf.predict((vx, w), dt)
        if k % 10 == 9:
            for lm in lms:
                z = mod.measurement_model(truth, lm) + rng.normal(0, [0.1, np.radians(2)])
                ekf.update(z, lm)
        t_err.append(np.hypot(*(ekf.x[:2] - truth[:2])))
        o_err.append(np.hypot(*(odo.pose[:2] - truth[:2])))
    assert np.mean(t_err[-200:]) < 0.3 < np.mean(o_err[-200:])
