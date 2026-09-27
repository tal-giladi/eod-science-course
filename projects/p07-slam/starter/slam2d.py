"""[STARTER -- every function that raises NotImplementedError is yours to write; helpers that are implemented are given.]

slam2d -- a small, readable 2D SLAM toolkit (Project P07).

Components
----------
* SE(2) helpers (implemented in the starter as well).
* A synthetic room, a 2D LiDAR ray-caster and a loop dataset generator (implemented in the starter).
* Occupancy-grid mapping with log-odds and an inverse sensor model, from known poses.
* ICP scan matching (point-to-point, closed-form SVD alignment).
* EKF-SLAM with range-bearing landmarks and known data association.
* 2D pose-graph optimisation with Gauss-Newton on SE(2) and sparse normal equations.
* A loop-closure demonstration that ties the pieces together.

Conventions
-----------
* A pose is ``np.array([x, y, theta])`` in metres and radians; angles are wrapped to [-pi, pi).
* Grid cells are addressed ``(i, j)`` = (column, row); the log-odds array is indexed ``L[j, i]``.
* A pose-graph edge is a tuple ``(i, j, z_ij, Omega_ij)`` where ``z_ij`` is the measured pose of
  node ``j`` expressed in the frame of node ``i`` and ``Omega_ij`` is its 3x3 information matrix.

Everything is fictional and purely geometric; see lesson 06.7.
"""
from __future__ import annotations

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
from scipy.spatial import cKDTree

# ---------------------------------------------------------------------------------------------
# SE(2) helpers (given)
# ---------------------------------------------------------------------------------------------


def wrap(a):
    """Wrap angle(s) to [-pi, pi)."""
    return (np.asarray(a) + np.pi) % (2 * np.pi) - np.pi


def rot2(th: float) -> np.ndarray:
    """2x2 rotation matrix R(theta)."""
    c, s = np.cos(th), np.sin(th)
    return np.array([[c, -s], [s, c]])


def compose(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """SE(2) composition a (+) b: pose b expressed in frame a, returned in a's parent frame."""
    return np.r_[a[:2] + rot2(a[2]) @ b[:2], wrap(a[2] + b[2])]


def inverse(a: np.ndarray) -> np.ndarray:
    """SE(2) inverse: the pose of the parent frame expressed in frame a."""
    R = rot2(a[2])
    return np.r_[-R.T @ a[:2], wrap(-a[2])]


def relative(xi: np.ndarray, xj: np.ndarray) -> np.ndarray:
    """Pose of xj expressed in the frame of xi, i.e. inverse(xi) (+) xj."""
    return np.r_[rot2(xi[2]).T @ (xj[:2] - xi[:2]), wrap(xj[2] - xi[2])]


def transform_points(pose: np.ndarray, pts: np.ndarray) -> np.ndarray:
    """Map (N, 2) points from the frame of ``pose`` into its parent frame."""
    return pts @ rot2(pose[2]).T + pose[:2]


def bresenham(x0: int, y0: int, x1: int, y1: int) -> list[tuple[int, int]]:
    """Integer cells on the segment (x0, y0) -> (x1, y1), both ends included, in order."""
    cells, dx, dy = [], abs(x1 - x0), -abs(y1 - y0)
    sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1)
    err = dx + dy
    while True:
        cells.append((x0, y0))
        if x0 == x1 and y0 == y1:
            return cells
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy


def logodds(p):
    """Probability -> log-odds."""
    p = np.asarray(p, float)
    return np.log(p / (1 - p))


def prob(L):
    """Log-odds -> probability."""
    return 1.0 - 1.0 / (1.0 + np.exp(L))


# ---------------------------------------------------------------------------------------------
# Synthetic world and sensors (given)
# ---------------------------------------------------------------------------------------------


def make_room() -> dict:
    """A fictional 8 m x 6 m room with a rectangular pillar and a wall stub.

    Returns a dict with ``segments`` (M, 4) array of wall segments (x1, y1, x2, y2),
    ``bounds`` (xmin, ymin, xmax, ymax) and ``solids`` (list of (xmin, ymin, xmax, ymax)
    rectangles that are not free space, i.e. the pillar).
    """
    outer = [(0, 0, 8, 0), (8, 0, 8, 6), (8, 6, 0, 6), (0, 6, 0, 0)]
    px0, py0, px1, py1 = 3.0, 2.2, 4.0, 3.2
    pillar = [(px0, py0, px1, py0), (px1, py0, px1, py1), (px1, py1, px0, py1), (px0, py1, px0, py0)]
    stub = [(6.0, 6.0, 6.0, 5.2), (0.0, 1.0, 0.6, 1.0)]
    return {"segments": np.array(outer + pillar + stub, float), "bounds": (0.0, 0.0, 8.0, 6.0),
            "solids": [(px0, py0, px1, py1)]}


def simulate_scan(pose: np.ndarray, segments: np.ndarray, n_beams: int = 360,
                  max_range: float = 12.0, noise_std: float = 0.0,
                  rng: np.random.Generator | None = None) -> tuple[np.ndarray, np.ndarray]:
    """Ray-cast a 2D LiDAR at ``pose`` against wall ``segments``.

    Returns ``(ranges, angles)``; angles are in the sensor (robot) frame, spanning [-pi, pi).
    Beams that hit nothing return ``max_range``. Gaussian range noise is added if requested.
    """
    angles = -np.pi + 2 * np.pi * np.arange(n_beams) / n_beams
    th = pose[2] + angles
    d = np.stack([np.cos(th), np.sin(th)], 1)                       # (B, 2)
    a, e = segments[:, :2], segments[:, 2:] - segments[:, :2]         # (M, 2)
    ao = a[None, :, :] - pose[None, None, :2]                          # (1, M, 2)
    cross = lambda u, v: u[..., 0] * v[..., 1] - u[..., 1] * v[..., 0]
    den = cross(d[:, None, :], e[None, :, :])                          # (B, M)
    with np.errstate(divide="ignore", invalid="ignore"):
        t = cross(ao, e[None]) / den
        u = cross(ao, d[:, None, :]) / den
    ok = (np.abs(den) > 1e-12) & (t > 1e-9) & (u >= 0) & (u <= 1)
    t = np.where(ok, t, np.inf).min(1)
    r = np.minimum(t, max_range)
    if noise_std > 0:
        rng = np.random.default_rng() if rng is None else rng
        hit = r < max_range
        r = np.where(hit, r + noise_std * rng.standard_normal(n_beams), r)
    return r, angles


def scan_to_points(ranges: np.ndarray, angles: np.ndarray, max_range: float = 12.0) -> np.ndarray:
    """Convert a scan to (N, 2) points in the sensor frame, dropping no-return beams."""
    keep = ranges < max_range - 1e-9
    return np.stack([ranges[keep] * np.cos(angles[keep]), ranges[keep] * np.sin(angles[keep])], 1)


def sample_walls(segments: np.ndarray, spacing: float = 0.03, rng: np.random.Generator | None = None) -> np.ndarray:
    """Points sampled uniformly by arc length along wall segments (about one per ``spacing`` m)."""
    rng = np.random.default_rng(0) if rng is None else rng
    pts = []
    for x1, y1, x2, y2 in segments:
        s = rng.uniform(0, 1, max(2, int(np.hypot(x2 - x1, y2 - y1) / spacing)))
        pts.append(np.c_[x1 + s * (x2 - x1), y1 + s * (y2 - y1)])
    return np.vstack(pts)


def make_loop_dataset(n_per_side: int = 10, width: float = 5.0, height: float = 3.0,
                      start=(1.5, 1.2), sigma=(0.02, 0.02, 0.01), heading_bias: float = 0.01,
                      closure_sigma=(0.02, 0.02, 0.005), seed: int = 0) -> dict:
    """A rectangular loop (counter-clockwise) inside :func:`make_room`, with noisy biased odometry.

    Returns a dict with
      ``truth`` (N, 3) true poses, ``odom`` (N, 3) dead-reckoned poses (initial guess),
      ``edges`` list of (i, j, z, Omega) including odometry and one loop closure (last -> first),
      ``odom_edges`` the odometry edges only.
    The odometry over-reports each heading change by ``heading_bias`` rad (a systematic error
    that a loop closure can correct) plus zero-mean Gaussian noise with std ``sigma``.
    """
    rng = np.random.default_rng(seed)
    truth = [np.r_[start[0], start[1], 0.0]]
    for side, length in enumerate([width, height, width, height]):
        step = length / n_per_side
        for k in range(n_per_side):
            turn = np.pi / 2 if k == n_per_side - 1 else 0.0
            truth.append(compose(truth[-1], np.r_[step, 0.0, turn]))
    truth = np.array(truth)
    Om = np.diag(1.0 / np.square(sigma))
    odom, edges = [truth[0].copy()], []
    for k in range(len(truth) - 1):
        z = relative(truth[k], truth[k + 1])
        z = z + np.r_[0, 0, heading_bias] + np.asarray(sigma) * rng.standard_normal(3)
        z[2] = wrap(z[2])
        edges.append((k, k + 1, z, Om))
        odom.append(compose(odom[-1], z))
    odom_edges = list(edges)
    n = len(truth)
    zc = relative(truth[n - 1], truth[0]) + np.asarray(closure_sigma) * rng.standard_normal(3)
    edges.append((n - 1, 0, zc, np.diag(1.0 / np.square(closure_sigma))))
    return {"truth": truth, "odom": np.array(odom), "edges": edges, "odom_edges": odom_edges}


def square_example() -> dict:
    """The lesson 06.7 example: 2 m square, odometry reports 92 deg per 90 deg turn."""
    odo, true = np.array([2.0, 0.0, np.radians(92)]), np.array([2.0, 0.0, np.pi / 2])
    X, T = [np.zeros(3)], [np.zeros(3)]
    for _ in range(4):
        X.append(compose(X[-1], odo))
        T.append(compose(T[-1], true))
    edges = [(k, k + 1, odo, np.diag([100.0, 100.0, 400.0])) for k in range(4)]
    edges.append((4, 0, np.zeros(3), np.diag([400.0, 400.0, 1600.0])))
    return {"odom": np.array(X), "truth": np.array(T), "edges": edges}


def simulate_landmark_run(landmarks: np.ndarray, n_steps: int = 400, dt: float = 0.1,
                          v: float = 1.0, w: float = 0.2, x0=(0.0, 0.0, 0.0),
                          control_std=(0.05, 0.02), meas_std=(0.1, 0.02),
                          max_range: float = 6.0, seed: int = 0) -> dict:
    """Drive a circle among point landmarks; return true poses, noisy controls and measurements.

    ``controls[k] = (v_meas, w_meas)`` is applied over ``dt`` to go from pose k to k+1.
    ``measurements[k]`` is a list of ``(landmark_id, range, bearing)`` taken at pose k+1.
    """
    rng = np.random.default_rng(seed)
    x = np.array(x0, float)
    poses, controls, meas = [x.copy()], [], []
    for _ in range(n_steps):
        x = unicycle_step(x, np.r_[v, w], dt)
        poses.append(x.copy())
        controls.append(np.r_[v, w] + np.asarray(control_std) * rng.standard_normal(2))
        zs = []
        for j, lm in enumerate(landmarks):
            r, b = range_bearing(x, lm)
            if r < max_range:
                zs.append((j, r + meas_std[0] * rng.standard_normal(),
                           wrap(b + meas_std[1] * rng.standard_normal())))
        meas.append(zs)
    return {"poses": np.array(poses), "controls": np.array(controls), "measurements": meas,
            "dt": dt, "control_std": np.asarray(control_std), "meas_std": np.asarray(meas_std)}


def unicycle_step(x: np.ndarray, u: np.ndarray, dt: float) -> np.ndarray:
    """Euler step of the unicycle: u = (v, w)."""
    return np.r_[x[0] + u[0] * dt * np.cos(x[2]), x[1] + u[0] * dt * np.sin(x[2]), wrap(x[2] + u[1] * dt)]


def range_bearing(x: np.ndarray, lm: np.ndarray) -> tuple[float, float]:
    """Range and bearing (robot frame) from pose x to landmark lm."""
    d = lm - x[:2]
    return float(np.hypot(*d)), float(wrap(np.arctan2(d[1], d[0]) - x[2]))


# ---------------------------------------------------------------------------------------------
# 1. Occupancy grid with log-odds
# ---------------------------------------------------------------------------------------------


class OccupancyGrid:
    """Log-odds occupancy grid over a rectangle, updated from range scans taken at known poses.

    Parameters
    ----------
    width, height : extent in metres.  resolution : cell size in metres.
    origin : world coordinates of the lower-left corner of cell (0, 0).
    p_occ, p_free : inverse-sensor-model probabilities for the return cell and traversed cells.
    l_min, l_max : clamping bounds on the log-odds (keep cells revisable).
    """

    def __init__(self, width: float, height: float, resolution: float = 0.1, origin=(0.0, 0.0),
                 p_occ: float = 0.7, p_free: float = 0.35, l_min: float = -2.0, l_max: float = 3.5):
        self.res = float(resolution)
        self.origin = np.asarray(origin, float)
        self.nx = int(np.ceil(width / resolution))
        self.ny = int(np.ceil(height / resolution))
        self.L = np.zeros((self.ny, self.nx))
        self.l_occ, self.l_free = float(logodds(p_occ)), float(logodds(p_free))
        self.l_min, self.l_max = l_min, l_max

    def world_to_cell(self, xy) -> tuple[int, int]:
        """World point (x, y) -> integer cell (i, j) = (column, row). May be out of bounds."""
        ij = np.floor((np.asarray(xy, float) - self.origin) / self.res).astype(int)
        return int(ij[0]), int(ij[1])

    def cell_centers(self) -> tuple[np.ndarray, np.ndarray]:
        """Arrays (X, Y) of shape (ny, nx) holding world coordinates of cell centres."""
        xs = self.origin[0] + (np.arange(self.nx) + 0.5) * self.res
        ys = self.origin[1] + (np.arange(self.ny) + 0.5) * self.res
        return np.meshgrid(xs, ys)

    def in_bounds(self, i: int, j: int) -> bool:
        return 0 <= i < self.nx and 0 <= j < self.ny

    def probabilities(self) -> np.ndarray:
        """Occupancy probabilities, shape (ny, nx)."""
        return prob(self.L)

    def integrate_beam(self, origin_cell: tuple[int, int], end_cell: tuple[int, int], hit: bool) -> None:
        """Apply the inverse sensor model along one beam.

        Every cell traversed from ``origin_cell`` up to (but excluding) ``end_cell`` receives
        ``l_free``; ``end_cell`` receives ``l_occ`` if ``hit`` else ``l_free`` (a max-range beam
        says the whole ray is free). Cells beyond the end are untouched. Out-of-bounds cells are
        skipped. Log-odds are clamped to [l_min, l_max] after each addition. Prior log-odds is 0.
        """
        raise NotImplementedError("TODO: implement OccupancyGrid.integrate_beam")

    def integrate_scan(self, pose: np.ndarray, ranges: np.ndarray, angles: np.ndarray,
                       max_range: float = 12.0) -> None:
        """Integrate a full scan taken at a *known* pose.

        A beam with ``range >= max_range`` is a no-return: mark the ray free up to ``max_range``
        without an occupied end cell. Beam end points are ``pose[:2] + r * (cos, sin)(theta+angle)``.
        """
        raise NotImplementedError("TODO: implement OccupancyGrid.integrate_scan")


# ---------------------------------------------------------------------------------------------
# 2. ICP scan matching
# ---------------------------------------------------------------------------------------------


def rigid_align(P: np.ndarray, Q: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Least-squares rigid transform (R, t) with ``R @ p_i + t ~= q_i`` for paired rows of P, Q.

    Closed form (Arun/Umeyama, no scale): centre both sets, SVD of the cross-covariance
    ``H = sum p_i' q_i'^T = U S V^T``, ``R = V diag(1, .., det(V U^T)) U^T``, ``t = qbar - R pbar``.
    The determinant correction guarantees a proper rotation (det R = +1), never a reflection.
    Works for any dimension d; P, Q are (N, d) with N >= d.
    """
    raise NotImplementedError("TODO: implement rigid_align")


def icp(source: np.ndarray, target: np.ndarray, R0: np.ndarray | None = None,
        t0: np.ndarray | None = None, max_iter: int = 60, tol: float = 1e-10,
        reject_dist: float | None = None) -> tuple[np.ndarray, np.ndarray, dict]:
    """Point-to-point ICP: find (R, t) such that ``source @ R.T + t`` aligns with ``target``.

    Each iteration: transform the source with the current estimate, associate every source point
    with its nearest target point (use ``scipy.spatial.cKDTree``), optionally discard pairs farther
    than ``reject_dist``, solve the pairs with :func:`rigid_align`, and compose the increment onto
    the current estimate. Stop when the mean squared pair distance changes by less than ``tol``.

    Returns ``(R, t, info)`` with ``info = {"iterations": int, "rmse": float, "converged": bool}``.
    """
    raise NotImplementedError("TODO: implement icp")


# ---------------------------------------------------------------------------------------------
# 3. EKF-SLAM
# ---------------------------------------------------------------------------------------------


class EKFSLAM:
    """EKF-SLAM with a unicycle motion model and range-bearing landmarks (known association).

    State ``mu = [x, y, theta, l1x, l1y, ..., lNx, lNy]`` with covariance ``Sigma`` (n x n,
    n = 3 + 2N). Landmarks are initialised on first sight; ``seen[j]`` tracks that.

    Parameters
    ----------
    n_landmarks : N.  x0 : initial pose.  P0 : initial 3x3 pose covariance.
    control_std : std of (v, w) control noise.  meas_std : std of (range, bearing) noise.
    """

    def __init__(self, n_landmarks: int, x0=(0.0, 0.0, 0.0), P0=None,
                 control_std=(0.05, 0.02), meas_std=(0.1, 0.02)):
        self.N = n_landmarks
        n = 3 + 2 * n_landmarks
        self.mu = np.zeros(n)
        self.mu[:3] = x0
        self.Sigma = np.zeros((n, n))
        self.Sigma[:3, :3] = np.eye(3) * 1e-6 if P0 is None else P0
        self.M = np.diag(np.square(control_std))
        self.R = np.diag(np.square(meas_std))
        self.seen = np.zeros(n_landmarks, bool)

    def landmark(self, j: int) -> np.ndarray:
        return self.mu[3 + 2 * j: 5 + 2 * j]

    def landmark_cov(self, j: int) -> np.ndarray:
        s = slice(3 + 2 * j, 5 + 2 * j)
        return self.Sigma[s, s]

    def predict(self, u: np.ndarray, dt: float) -> None:
        """EKF prediction with control u = (v, w) over dt.

        Motion: x' = x + v dt cos th, y' = y + v dt sin th, th' = th + w dt.
        Propagate ``Sigma_rr <- G Sigma_rr G^T + V M V^T`` and the robot-landmark cross terms
        ``Sigma_rl <- G Sigma_rl`` (O(n) work); landmark-landmark blocks are unchanged.
        G = d(motion)/d(pose), V = d(motion)/d(u), M = control noise covariance.
        """
        raise NotImplementedError("TODO: implement EKFSLAM.predict")

    def update(self, j: int, z: np.ndarray) -> None:
        """Process one range-bearing measurement ``z = (r, b)`` of landmark ``j``.

        First sight: initialise the landmark at ``p + r (cos, sin)(th + b)`` and fill its
        covariance ``Gp Sigma_rr Gp^T + Gz R Gz^T`` and cross-covariances ``Gp Sigma_r,:``
        (no measurement update). Otherwise: standard EKF update with the 2 x n Jacobian H
        (non-zero only in the robot and landmark-j columns), innovation with wrapped bearing,
        ``K = Sigma H^T S^-1`` and the Joseph form ``(I-KH) Sigma (I-KH)^T + K R K^T``.
        """
        raise NotImplementedError("TODO: implement EKFSLAM.update")


def run_ekf_slam(run: dict, n_landmarks: int) -> tuple[EKFSLAM, dict]:
    """Run :class:`EKFSLAM` over a dataset from :func:`simulate_landmark_run`.

    Returns the filter and a history dict with ``poses`` (estimated) and ``lm_trace`` (T x N
    array of landmark covariance traces, NaN before first sight).
    """
    ekf = EKFSLAM(n_landmarks, x0=run["poses"][0], control_std=run["control_std"], meas_std=run["meas_std"])
    poses, traces = [ekf.mu[:3].copy()], []
    for u, zs in zip(run["controls"], run["measurements"]):
        ekf.predict(u, run["dt"])
        for j, r, b in zs:
            ekf.update(j, np.array([r, b]))
        poses.append(ekf.mu[:3].copy())
        traces.append([np.trace(ekf.landmark_cov(j)) if ekf.seen[j] else np.nan for j in range(n_landmarks)])
    return ekf, {"poses": np.array(poses), "lm_trace": np.array(traces)}


# ---------------------------------------------------------------------------------------------
# 4. Pose-graph optimisation (Gauss-Newton on SE(2), sparse)
# ---------------------------------------------------------------------------------------------


def edge_error(xi: np.ndarray, xj: np.ndarray, z: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Residual and Jacobians of one relative-pose edge.

    ``e = [R_z^T (R_i^T (t_j - t_i) - t_z) ; wrap(th_j - th_i - th_z)]``,
    ``A = de/dx_i`` and ``B = de/dx_j`` (both 3x3), as in lesson 06.7 section 4.
    """
    raise NotImplementedError("TODO: implement edge_error")


def chi2(X: np.ndarray, edges: list) -> float:
    """Total weighted squared error sum e^T Omega e over all edges (given in terms of edge_error)."""
    total = 0.0
    for i, j, z, Om in edges:
        e = edge_error(X[i], X[j], z)[0]
        total += float(e @ Om @ e)
    return total


def build_normal_equations(X: np.ndarray, edges: list, anchor: int = 0,
                           anchor_weight: float = 1e8) -> tuple[sp.csc_matrix, np.ndarray]:
    """Assemble the sparse Gauss-Newton system ``H dx = -b``.

    ``H = sum J^T Omega J`` and ``b = sum J^T Omega e`` where each edge contributes the four 3x3
    blocks (ii, ij, ji, jj). Build it from COO triplets and return ``H`` as ``scipy.sparse`` CSC
    (shape 3n x 3n) and dense ``b``. Fix the gauge freedom by adding ``anchor_weight * I`` to the
    diagonal block of node ``anchor``.
    """
    raise NotImplementedError("TODO: implement build_normal_equations")


def optimize_pose_graph(X0: np.ndarray, edges: list, iters: int = 20, tol: float = 1e-9,
                        anchor: int = 0) -> tuple[np.ndarray, list[float]]:
    """Gauss-Newton on the pose graph.

    Repeat: build (H, b), solve ``H dx = -b`` with ``scipy.sparse.linalg.spsolve``, apply
    ``X += dx.reshape(n, 3)``, wrap angles; stop when ``max |dx| < tol``.
    Returns the optimised poses and the chi^2 history (initial value first, one per iteration).
    """
    raise NotImplementedError("TODO: implement optimize_pose_graph")


# ---------------------------------------------------------------------------------------------
# 5. Loop-closure demonstration
# ---------------------------------------------------------------------------------------------


def position_errors(X: np.ndarray, truth: np.ndarray) -> np.ndarray:
    """Per-pose Euclidean position error (no alignment; node 0 is anchored at the truth)."""
    return np.linalg.norm(X[:, :2] - truth[:, :2], axis=1)


def build_map(poses: np.ndarray, room: dict, resolution: float = 0.1, n_beams: int = 180,
              noise_std: float = 0.01, seed: int = 0, true_poses: np.ndarray | None = None) -> OccupancyGrid:
    """Occupancy grid of the room from scans taken at ``true_poses`` but placed at ``poses``.

    This is how pose error turns into map error: the sensor sees the world from the true pose, the
    mapper believes the estimated one.
    """
    rng = np.random.default_rng(seed)
    true_poses = poses if true_poses is None else true_poses
    x0, y0, x1, y1 = room["bounds"]
    g = OccupancyGrid(x1 - x0 + 1.0, y1 - y0 + 1.0, resolution,
                      origin=(x0 - 0.5 - resolution / 2, y0 - 0.5 - resolution / 2))
    for p, pt in zip(poses, true_poses):
        r, a = simulate_scan(pt, room["segments"], n_beams, noise_std=noise_std, rng=rng)
        g.integrate_scan(p, r, a)
    return g


def run_loop_demo(outdir: str | None = None, seed: int = 0) -> dict:
    """Odometry chain vs pose graph with loop closure on the synthetic loop; optional figure.

    Returns metrics ``{"max_err_odom", "max_err_opt", "chi2_hist"}``; if ``outdir`` is given,
    writes ``loop_closure.png`` (trajectories, chi^2, maps from odometry and optimised poses).
    """
    room = make_room()
    ds = make_loop_dataset(seed=seed)
    Xo, hist = optimize_pose_graph(ds["odom"], ds["edges"])
    out = {"max_err_odom": float(position_errors(ds["odom"], ds["truth"]).max()),
           "max_err_opt": float(position_errors(Xo, ds["truth"]).max()), "chi2_hist": hist}
    if outdir is not None:
        import os
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(1, 4, figsize=(20, 4.5))
        for s in room["segments"]:
            ax[0].plot(s[[0, 2]], s[[1, 3]], "k-", lw=1)
        ax[0].plot(*ds["truth"][:, :2].T, "g-", label="truth")
        ax[0].plot(*ds["odom"][:, :2].T, "r--", label="odometry")
        ax[0].plot(*Xo[:, :2].T, "b-", label="pose graph")
        ax[0].set_aspect("equal"); ax[0].legend(); ax[0].set_title("Trajectories")
        ax[1].semilogy(hist, "o-"); ax[1].set_title(r"$\chi^2$ per Gauss-Newton iteration")
        for k, (P, name) in enumerate([(ds["odom"], "map from odometry"), (Xo, "map from pose graph")]):
            g = build_map(P, room, true_poses=ds["truth"], seed=seed)
            ax[2 + k].imshow(g.probabilities(), origin="lower", cmap="gray_r", vmin=0, vmax=1)
            ax[2 + k].set_title(name)
        fig.tight_layout()
        os.makedirs(outdir, exist_ok=True)
        fig.savefig(os.path.join(outdir, "loop_closure.png"), dpi=110)
        plt.close(fig)
    return out


if __name__ == "__main__":
    m = run_loop_demo(outdir="p07_out")
    print(f"max position error: odometry {m['max_err_odom']:.3f} m -> pose graph {m['max_err_opt']:.3f} m")
    print("chi2:", " -> ".join(f"{c:.1f}" for c in m["chi2_hist"]))
