"""Tests for P08 (manipulator). Run from the repo root:  python -m pytest projects/p08-manipulator"""
import os, sys, pathlib
_ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_ROOT / ("solution" if os.environ.get("EOD_SOLUTION") else "starter")))
import manipulator as mod  # noqa: E402

import numpy as np  # noqa: E402
import pytest  # noqa: E402
from scipy.linalg import expm  # noqa: E402

RNG = np.random.default_rng(0)
Q_STAR = np.radians([15.26, 35.50, -94.18, -1.32, 0.0])


def random_q(n, rng=RNG, margin=0.05):
    lo, hi = mod.JOINT_LIMITS[:, 0] + margin, mod.JOINT_LIMITS[:, 1] - margin
    return rng.uniform(lo, hi, (n, 5))


# ------------------------------------------------------------------ SO(3) / SE(3)
def test_rodrigues_matches_matrix_exponential():
    for w in RNG.normal(size=(20, 3)):
        np.testing.assert_allclose(mod.exp_so3(w), expm(mod.hat(w)), atol=1e-12)
    np.testing.assert_allclose(mod.rodrigues([0, 0, 2], np.pi / 2), mod.rot_z(np.pi / 2), atol=1e-12)


@pytest.mark.parametrize("theta", [1e-10, 1e-5, 0.3, 1.5, 3.0, np.pi - 1e-4, np.pi - 1e-8, np.pi])
def test_so3_exp_log_round_trip(theta):
    for a in RNG.normal(size=(10, 3)):
        w = a / np.linalg.norm(a) * theta
        R = mod.exp_so3(w)
        w2 = mod.log_so3(R)
        np.testing.assert_allclose(mod.exp_so3(w2), R, atol=1e-9)
        if theta < np.pi - 1e-6:
            np.testing.assert_allclose(w2, w, atol=1e-7)


def test_se3_exp_log_round_trip_and_expm():
    for _ in range(20):
        a = RNG.normal(size=3)
        xi = np.r_[a / np.linalg.norm(a) * RNG.uniform(0, 3.0), RNG.normal(size=3)]   # |omega| < pi
        T = mod.exp_se3(xi)
        np.testing.assert_allclose(T, expm(mod.se3_hat(xi)), atol=1e-10)
        np.testing.assert_allclose(mod.log_se3(T), xi, atol=1e-9)
    xi = np.r_[0, 0, 0, 0.3, -0.2, 1.0]                      # pure translation
    np.testing.assert_allclose(mod.log_se3(mod.exp_se3(xi)), xi, atol=1e-12)


def test_adjoint_transforms_twists():
    T = mod.exp_se3(np.r_[0.3, -0.4, 0.8, 0.5, 1.0, -0.2])
    V = RNG.normal(size=6)
    lhs = mod.se3_hat(mod.adjoint(T) @ V)
    np.testing.assert_allclose(lhs, T @ mod.se3_hat(V) @ mod.inv_T(T), atol=1e-12)


# ------------------------------------------------------------------ FK
def test_home_pose():
    T = mod.fk_dh(np.zeros(5))
    np.testing.assert_allclose(T[:3, 3], [1.75, 0, 0.35], atol=1e-12)
    np.testing.assert_allclose(T[:3, 2], [1, 0, 0], atol=1e-12)        # approach along +x
    np.testing.assert_allclose(mod.fk_poe(np.zeros(5)), mod.M_HOME, atol=1e-12)


def test_poe_equals_dh():
    for q in RNG.uniform(-2.5, 2.5, (100, 5)):
        np.testing.assert_allclose(mod.fk_poe(q), mod.fk_dh(q), atol=1e-12)


def test_lesson_pose():
    T = mod.fk_poe(Q_STAR)
    np.testing.assert_allclose(T[:3, 3], [1.1, 0.3, 0.0], atol=2e-3)


# ------------------------------------------------------------------ Jacobians
def test_point_jacobian_vs_finite_differences():
    h = 1e-6
    for q in random_q(10):
        J = mod.point_jacobian(q)
        Jfd = np.column_stack([(mod.fk_poe(q + h * e)[:3, 3] - mod.fk_poe(q - h * e)[:3, 3]) / (2 * h)
                               for e in np.eye(5)])
        np.testing.assert_allclose(J, Jfd, atol=1e-7)


def test_space_jacobian_vs_finite_differences():
    h = 1e-6
    for q in random_q(5):
        Js = mod.jacobian_space(q)
        Tinv = mod.inv_T(mod.fk_poe(q))
        for i, e in enumerate(np.eye(5)):
            dT = (mod.fk_poe(q + h * e) - mod.fk_poe(q - h * e)) / (2 * h)
            W = dT @ Tinv
            np.testing.assert_allclose(np.r_[mod.vee(W[:3, :3]), W[:3, 3]], Js[:, i], atol=1e-7)


# ------------------------------------------------------------------ IK
def test_ik_position_converges_for_reachable_targets():
    for k, q in enumerate(random_q(15, np.random.default_rng(7))):
        p = mod.fk_poe(q)[:3, 3]
        res = mod.ik_dls(p, q0=np.zeros(5), task="position", seed=k)
        assert res.success, (q, res)
        np.testing.assert_allclose(mod.fk_poe(res.q)[:3, 3], p, atol=1e-5)
        assert np.all(res.q >= mod.JOINT_LIMITS[:, 0] - 1e-12) and np.all(res.q <= mod.JOINT_LIMITS[:, 1] + 1e-12)


def test_ik_pose_task_lesson_case():
    T_d = mod.fk_poe(Q_STAR)
    res = mod.ik_dls(T_d, q0=np.radians([0, 20, -60, 0, 10]), task="pose")
    assert res.success
    np.testing.assert_allclose(mod.fk_poe(res.q), T_d, atol=1e-5)


def test_ik_reports_failure_for_unreachable_target():
    res = mod.ik_dls(np.array([2.5, 0.8, 0.5]), q0=np.zeros(5), task="position", restarts=2)
    assert not res.success
    assert res.error > 0.5
    # the best effort points the stretched arm toward the target
    p = mod.fk_poe(res.q)[:3, 3]
    assert np.linalg.norm(p - [0, 0, mod.D1]) == pytest.approx(1.75, abs=0.02)


def test_analytic_ik_lesson_numbers():
    q = mod.ik_analytic(np.array([1.1, 0.3, 0.0]), np.radians(-60), 0.0)
    np.testing.assert_allclose(np.degrees(q), [15.26, 35.50, -94.18, -1.32, 0.0], atol=0.01)
    assert mod.ik_analytic(np.array([3.0, 0.0, 0.35]), 0.0, 0.0) is None


# ------------------------------------------------------------------ manipulability
def test_manipulability_zero_at_singularity():
    for q1, q2, q5 in [(0, 0, 0), (0.7, 0.4, 1.0), (-1.2, -0.3, 2.0)]:
        q = np.array([q1, q2, 0.0, 0.0, q5])                 # elbow and wrist straight
        assert mod.manipulability(mod.point_jacobian(q)) < 1e-10
    w = mod.manipulability(mod.point_jacobian(Q_STAR))
    assert w > 1e-2
    # 2R planar check: w = l1 l2 |sin q2|
    J2 = np.array([[-0.7 * np.sin(np.pi / 6), -0.7 * np.sin(np.pi / 6)],
                   [0.8 + 0.7 * np.cos(np.pi / 6), 0.7 * np.cos(np.pi / 6)]])
    assert mod.manipulability(J2) == pytest.approx(0.28, abs=1e-9)


def test_reachability_map_sane():
    m = mod.reachability_map(n_samples=8, cell=0.25)
    xe, ze = m["x_edges"], m["z_edges"]
    def cell(x, z):
        return m["reachable"][np.searchsorted(ze, z) - 1, np.searchsorted(xe, x) - 1]
    assert cell(1.0, 0.35)
    assert not cell(1.95, 1.95)
    assert np.nanmax(m["w_max"]) > 0


# ------------------------------------------------------------------ statics
def test_payload_torques_lesson_numbers():
    q = mod.ik_analytic(np.array([1.1, 0.3, 0.0]), np.radians(-60), 0.0)
    tau = mod.gravity_torque(q, payload=3.0, masses=(0.0, 0.0, 0.0))
    np.testing.assert_allclose(tau, [0, 33.56, 14.39, 3.68, 0], atol=0.01)
    np.testing.assert_allclose(mod.joint_torques(q, [0, 0, 3 * mod.G]), tau, atol=1e-9)


def test_torque_power_balance():
    q, F = random_q(1)[0], RNG.normal(size=3)
    qd = RNG.normal(size=5)
    assert mod.joint_torques(q, F) @ qd == pytest.approx(F @ (mod.point_jacobian(q) @ qd), rel=1e-12)


def test_payload_vs_reach_lesson_table():
    pl, lim = mod.payload_vs_reach([0.8, 1.2, 1.75])
    np.testing.assert_allclose(pl, [15.3, 12.4, 6.9], atol=0.06)
    assert list(lim) == [3, 1, 1]                            # wrist, shoulder, shoulder
    pl2, lim2 = mod.payload_vs_reach([2.0])
    assert np.isnan(pl2[0]) and lim2[0] == -1


# ------------------------------------------------------------------ pan-tilt
def test_pan_tilt_lesson_numbers():
    T_wb = mod.make_T(mod.rot_z(np.pi / 2), [5, 2, 0])
    T_bp = mod.make_T(np.eye(3), [0.3, 0, 0.8])
    pan, tilt, rng = mod.look_at_pan_tilt(T_wb, T_bp, [0, 0, 0.10], [4.2, 4.5, 0.1])
    assert np.degrees(pan) == pytest.approx(19.98, abs=0.01)
    assert np.degrees(tilt) == pytest.approx(-18.87, abs=0.01)
    assert rng == pytest.approx(2.474, abs=1e-3)
    pan0, tilt0, _ = mod.look_at_pan_tilt(np.eye(4), np.eye(4), [0, 0, 0], [0, 0, 5.0])
    assert pan0 == 0.0 and tilt0 == pytest.approx(np.pi / 2)
