"""Tests for P07 (slam2d). Run from the repo root:  python -m pytest projects/p07-slam"""
import os, sys, pathlib
_ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_ROOT / ("solution" if os.environ.get("EOD_SOLUTION") else "starter")))
import slam2d as mod  # noqa: E402

import numpy as np  # noqa: E402
import scipy.sparse as sp  # noqa: E402
import pytest  # noqa: E402


def angle_of(R):
    return np.arctan2(R[1, 0], R[0, 0])


# ------------------------------------------------------------------ occupancy grid
def test_log_odds_lesson_numbers():
    g = mod.OccupancyGrid(2.0, 2.0, 0.1)
    for _ in range(3):
        g.integrate_beam((0, 0), (10, 5), hit=True)
    assert g.probabilities()[5, 10] == pytest.approx(0.927, abs=1e-3)
    g.integrate_beam((0, 0), (12, 6), hit=True)          # passes through (10, 5) once
    assert g.probabilities()[5, 10] == pytest.approx(0.872, abs=1e-3)
    # traversed cells are free, cells beyond the return are untouched
    assert g.probabilities()[0, 0] < 0.5
    assert g.L[5, 15] == 0.0


def test_log_odds_clamped():
    g = mod.OccupancyGrid(2.0, 2.0, 0.1)
    for _ in range(50):
        g.integrate_beam((0, 0), (6, 3), hit=True)
    assert g.L.max() <= g.l_max + 1e-12 and g.L.min() >= g.l_min - 1e-12


def _truth_masks(g, room):
    X, Y = g.cell_centers()
    occ = np.zeros(X.shape, bool)
    for x1, y1, x2, y2 in room["segments"]:
        for s in np.linspace(0, 1, int(np.hypot(x2 - x1, y2 - y1) / (g.res / 4)) + 2):
            i, j = g.world_to_cell((x1 + s * (x2 - x1), y1 + s * (y2 - y1)))
            if g.in_bounds(i, j):
                occ[j, i] = True
    # free: inside the room, outside solids, and at least 1.5 cells from any wall
    x0, y0, x1, y1 = room["bounds"]
    free = (X > x0) & (X < x1) & (Y > y0) & (Y < y1)
    for a, b, c, d in room["solids"]:
        free &= ~((X > a) & (X < c) & (Y > b) & (Y < d))
    from scipy.ndimage import binary_dilation
    free &= ~binary_dilation(occ, iterations=1)
    return occ, free


def test_occupancy_grid_converges_on_room():
    room = mod.make_room()
    rng = np.random.default_rng(1)
    g = mod.OccupancyGrid(9.0, 7.0, 0.1, origin=(-0.55, -0.55))
    occ, free = _truth_masks(g, room)
    poses = [np.r_[1.5, 1.5, 0.0], np.r_[6.5, 1.5, 1.0], np.r_[6.5, 4.5, 2.0], np.r_[1.5, 4.5, -1.0],
             np.r_[5.0, 2.7, 0.3], np.r_[2.0, 3.0, -2.0], np.r_[4.8, 5.3, 0.0], np.r_[1.0, 0.5, 0.5]]
    accuracy = []
    for p in poses:
        r, a = mod.simulate_scan(p, room["segments"], n_beams=360, noise_std=0.01, rng=rng)
        g.integrate_scan(p, r, a)
        P = g.probabilities()
        correct = np.sum(P[occ] > 0.5) + np.sum(P[free] < 0.5)
        accuracy.append(correct / (occ.sum() + free.sum()))
    assert all(b >= a - 1e-9 for a, b in zip(accuracy, accuracy[1:])), accuracy   # monotone
    assert accuracy[-1] > 0.95
    P = g.probabilities()
    assert np.mean(P[free] < 0.5) > 0.98
    assert np.mean(P[occ] > 0.5) > 0.85


# ------------------------------------------------------------------ ICP
def test_rigid_align_exact_and_proper_rotation():
    rng = np.random.default_rng(0)
    P = rng.uniform(-3, 3, (40, 2))
    th, t = np.radians(30), np.array([1.0, 0.5])
    Q = P @ mod.rot2(th).T + t
    R, tt = mod.rigid_align(P, Q)
    assert angle_of(R) == pytest.approx(th, abs=1e-10)
    np.testing.assert_allclose(tt, t, atol=1e-10)
    # reflection-prone: target is a mirror image -> result must still be a rotation
    R2, _ = mod.rigid_align(P, P * np.array([1.0, -1.0]))
    assert np.linalg.det(R2) == pytest.approx(1.0)
    # 3D works too
    P3 = rng.normal(size=(30, 3))
    from scipy.spatial.transform import Rotation
    R3 = Rotation.from_rotvec([0.3, -0.2, 0.5]).as_matrix()
    R3e, t3e = mod.rigid_align(P3, P3 @ R3.T + [1, 2, 3])
    np.testing.assert_allclose(R3e, R3, atol=1e-10)
    np.testing.assert_allclose(t3e, [1, 2, 3], atol=1e-10)


def test_icp_recovers_known_rigid_transform():
    room = mod.make_room()
    r, a = mod.simulate_scan(np.r_[2.0, 1.5, 0.0], room["segments"], n_beams=720)
    target = mod.scan_to_points(r, a)
    th, t = np.radians(8.0), np.array([0.25, -0.15])
    R_true = mod.rot2(th)
    # source = target moved by the inverse transform, shuffled, so that R_true*src + t = target
    src = (target - t) @ R_true
    src = src[np.random.default_rng(3).permutation(len(src))]
    R, tt, info = mod.icp(src, target)
    assert angle_of(R) == pytest.approx(th, abs=1e-6)
    np.testing.assert_allclose(tt, t, atol=1e-6)
    assert info["rmse"] < 1e-6


def test_icp_between_two_real_scans():
    room = mod.make_room()
    rng = np.random.default_rng(5)
    xa, xb = np.r_[2.0, 1.5, 0.1], np.r_[2.35, 1.6, 0.22]
    Pa = mod.scan_to_points(*mod.simulate_scan(xa, room["segments"], 720, noise_std=0.005, rng=rng))
    Pb = mod.scan_to_points(*mod.simulate_scan(xb, room["segments"], 720, noise_std=0.005, rng=rng))
    z_true = mod.relative(xa, xb)                 # pose of b in frame a: maps b-points into a-frame
    z0 = z_true + np.r_[0.08, -0.06, 0.05]        # odometry-like initial guess
    R, t, info = mod.icp(Pb, Pa, R0=mod.rot2(z0[2]), t0=z0[:2], reject_dist=0.3)
    assert abs(mod.wrap(angle_of(R) - z_true[2])) < np.radians(1.0)
    assert np.linalg.norm(t - z_true[:2]) < 0.05


# ------------------------------------------------------------------ EKF-SLAM
LMS = np.array([[3, 1], [-2, 3], [0, 6], [4, 5], [-3, 8], [2, 9], [5, 3], [-1, 1.5]], float)


def test_ekf_slam_landmark_covariances_shrink():
    run = mod.simulate_landmark_run(LMS, n_steps=400, seed=0)
    ekf, hist = mod.run_ekf_slam(run, len(LMS))
    assert ekf.seen.all()
    tr = hist["lm_trace"]
    for j in range(len(LMS)):
        col = tr[~np.isnan(tr[:, j]), j]
        assert np.all(np.diff(col) <= 1e-9), f"landmark {j} covariance grew"
        assert col[-1] < 0.25 * col[0]
    assert np.allclose(ekf.Sigma, ekf.Sigma.T)
    assert np.linalg.eigvalsh(ekf.Sigma).min() > -1e-12
    err = np.linalg.norm(ekf.mu[3:].reshape(-1, 2) - LMS, axis=1)
    assert err.max() < 0.3


def test_ekf_predict_only_touches_robot_block():
    ekf = mod.EKFSLAM(2, x0=(0, 0, 0))
    ekf.update(0, np.array([2.0, 0.3]))
    lm_before = ekf.landmark_cov(0).copy()
    ekf.predict(np.array([1.0, 0.1]), 0.1)
    np.testing.assert_allclose(ekf.landmark_cov(0), lm_before)
    assert ekf.Sigma[0, 0] > 0


# ------------------------------------------------------------------ pose graph
def test_edge_jacobians_match_finite_differences():
    rng = np.random.default_rng(2)
    xi, xj, z = rng.normal(size=3), rng.normal(size=3), rng.normal(size=3)
    e, A, B = mod.edge_error(xi, xj, z)
    h = 1e-6
    for k in range(3):
        d = np.eye(3)[k] * h
        np.testing.assert_allclose((mod.edge_error(xi + d, xj, z)[0] - mod.edge_error(xi - d, xj, z)[0]) / (2 * h),
                                   A[:, k], atol=1e-6)
        np.testing.assert_allclose((mod.edge_error(xi, xj + d, z)[0] - mod.edge_error(xi, xj - d, z)[0]) / (2 * h),
                                   B[:, k], atol=1e-6)


def test_normal_equations_are_sparse():
    ds = mod.make_loop_dataset()
    H, b = mod.build_normal_equations(ds["odom"], ds["edges"])
    assert sp.issparse(H) and H.shape == (3 * len(ds["odom"]),) * 2
    assert H.nnz <= 9 * (len(ds["odom"]) + 2 * len(ds["edges"]))
    np.testing.assert_allclose((H - H.T).toarray(), 0, atol=1e-6)


def test_square_example_from_lesson():
    ex = mod.square_example()
    X, hist = mod.optimize_pose_graph(ex["odom"], ex["edges"])
    before = mod.position_errors(ex["odom"], ex["truth"]).max()
    after = mod.position_errors(X, ex["truth"]).max()
    assert before == pytest.approx(0.194, abs=1e-3)
    assert after < 0.01
    assert hist[0] == pytest.approx(46.2, abs=0.1) and hist[-1] == pytest.approx(1.84, abs=0.01)


def test_loop_closure_reduces_error_vs_odometry():
    ds = mod.make_loop_dataset(seed=0)
    X, hist = mod.optimize_pose_graph(ds["odom"], ds["edges"])
    e_odo = mod.position_errors(ds["odom"], ds["truth"])
    e_opt = mod.position_errors(X, ds["truth"])
    assert e_opt.max() < 0.25 * e_odo.max()
    assert e_opt.mean() < 0.25 * e_odo.mean()
    assert hist[-1] < 0.01 * hist[0]
    np.testing.assert_allclose(X[0], ds["truth"][0], atol=1e-6)     # anchored
    # without the loop closure, the optimum is the odometry chain itself (lesson Exercise 4)
    X2, _ = mod.optimize_pose_graph(ds["odom"], ds["odom_edges"])
    np.testing.assert_allclose(X2, ds["odom"], atol=1e-6)
