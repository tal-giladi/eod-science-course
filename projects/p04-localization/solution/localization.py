"""localization — EKF and particle-filter localisation with range–bearing landmarks (Project P04,
reference solution).

State x = (x, y, theta) in metres/radians. Control u = (v, omega): the forward speed and yaw rate
reported by odometry over a step dt. Process model (06.6 §3): x_t = f(x_{t-1}, u_t) + w_t,
w_t ~ N(0, Q) — the additive w_t lumps odometry error and slip. Measurement of a known landmark
l = (lx, ly): z = h(x, l) + v, v ~ N(0, R), z = (range, bearing), bearing relative to heading.
Data association is known (landmark ids).

The module is self-contained (NumPy/SciPy only). ``simulate`` generates ground truth with its own
private copy of the motion model, so a bug in your ``motion_model`` cannot hide itself.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.stats import chi2

__all__ = [
    "wrap_angle", "motion_model", "motion_jacobian", "measurement_model", "measurement_jacobian",
    "kf_predict", "kf_update", "ekf_predict", "ekf_update", "EKF",
    "systematic_resample", "ParticleFilter", "nees", "chi2_band",
    "SimRun", "simulate", "run_ekf", "run_pf", "dead_reckoning",
    "monte_carlo_nees", "comparison_experiment",
]


# ----------------------------------------------------------------------------------------------
# Helpers (provided in the starter)
# ----------------------------------------------------------------------------------------------
def wrap_angle(a):
    """Wrap angle(s) to [-pi, pi)."""
    return (np.asarray(a) + np.pi) % (2.0 * np.pi) - np.pi


def chi2_band(dof: int, n_runs: int = 1, alpha: float = 0.05):
    """Two-sided (1-alpha) acceptance band for the *run-averaged* NEES/NIS with ``dof`` degrees of
    freedom: N * mean ~ chi2(N * dof)  =>  band = chi2.ppf([a/2, 1-a/2], N*dof) / N."""
    lo, hi = chi2.ppf([alpha / 2, 1 - alpha / 2], n_runs * dof) / n_runs
    return float(lo), float(hi)


def _f_true(x, u, dt):  # private copy used only to generate ground truth
    return np.array([x[0] + u[0] * dt * np.cos(x[2]), x[1] + u[0] * dt * np.sin(x[2]),
                     float(wrap_angle(x[2] + u[1] * dt))])


def _h_true(x, lm):
    d = np.asarray(lm) - x[:2]
    return np.array([np.hypot(d[0], d[1]), float(wrap_angle(np.arctan2(d[1], d[0]) - x[2]))])


# ----------------------------------------------------------------------------------------------
# Models and Jacobians (learning goals)
# ----------------------------------------------------------------------------------------------
def motion_model(x, u, dt: float) -> np.ndarray:
    """f(x, u) = [x + v dt cos(theta), y + v dt sin(theta), wrap(theta + omega dt)]."""
    v, w = u
    return np.array([x[0] + v * dt * np.cos(x[2]), x[1] + v * dt * np.sin(x[2]),
                     float(wrap_angle(x[2] + w * dt))])


def motion_jacobian(x, u, dt: float) -> np.ndarray:
    """F = df/dx (3x3) evaluated at (x, u)."""
    v = u[0]
    return np.array([[1.0, 0.0, -v * dt * np.sin(x[2])],
                     [0.0, 1.0, v * dt * np.cos(x[2])],
                     [0.0, 0.0, 1.0]])


def measurement_model(x, landmark) -> np.ndarray:
    """h(x, l) = [sqrt(q), wrap(atan2(dy, dx) - theta)], (dx, dy) = l - (x, y), q = dx^2 + dy^2."""
    dx, dy = landmark[0] - x[0], landmark[1] - x[1]
    return np.array([np.hypot(dx, dy), float(wrap_angle(np.arctan2(dy, dx) - x[2]))])


def measurement_jacobian(x, landmark) -> np.ndarray:
    """H = dh/dx (2x3) = [[-dx/r, -dy/r, 0], [dy/q, -dx/q, -1]]."""
    dx, dy = landmark[0] - x[0], landmark[1] - x[1]
    q = dx * dx + dy * dy
    r = np.sqrt(q)
    return np.array([[-dx / r, -dy / r, 0.0], [dy / q, -dx / q, -1.0]])


# ----------------------------------------------------------------------------------------------
# Linear KF and generic EKF steps (learning goals)
# ----------------------------------------------------------------------------------------------
def kf_predict(mu, P, A, B, u, Q):
    """Linear KF prediction: mu' = A mu + B u, P' = A P A^T + Q."""
    return A @ mu + B @ u, A @ P @ A.T + Q


def kf_update(mu, P, z, C, R):
    """Linear KF update (Joseph form). Returns (mu, P, nis)."""
    nu = z - C @ mu
    S = C @ P @ C.T + R
    K = np.linalg.solve(S, C @ P).T          # K = P C^T S^-1 (S, P symmetric)
    I_KC = np.eye(len(mu)) - K @ C
    return mu + K @ nu, I_KC @ P @ I_KC.T + K @ R @ K.T, float(nu @ np.linalg.solve(S, nu))


def ekf_predict(mu, P, f, F, Q):
    """Generic EKF prediction. f: callable mu -> mean; F: Jacobian at mu (matrix). Returns (mu, P)."""
    return np.asarray(f(mu), dtype=float), F @ P @ F.T + Q


def ekf_update(mu, P, z, h, H, R, angle_idx=()):
    """Generic EKF update (Joseph form).

    h: callable mu -> predicted measurement; H: Jacobian at mu; angle_idx: indices of angular
    components of the innovation to wrap. Returns (mu, P, nis). Angle wrapping of the *state* is
    the caller's job.
    """
    nu = np.asarray(z, dtype=float) - np.asarray(h(mu), dtype=float)
    for i in angle_idx:
        nu[i] = wrap_angle(nu[i])
    S = H @ P @ H.T + R
    K = np.linalg.solve(S, H @ P).T
    I_KH = np.eye(len(mu)) - K @ H
    return mu + K @ nu, I_KH @ P @ I_KH.T + K @ R @ K.T, float(nu @ np.linalg.solve(S, nu))


class EKF:
    """EKF localiser for the unicycle + range–bearing landmark model."""

    def __init__(self, x0, P0, Q, R):
        self.x = np.asarray(x0, dtype=float).copy()
        self.P = np.asarray(P0, dtype=float).copy()
        self.Q, self.R = np.asarray(Q, dtype=float), np.asarray(R, dtype=float)

    def predict(self, u, dt: float):
        """Propagate mean and covariance through the motion model."""
        F = motion_jacobian(self.x, u, dt)
        self.x, self.P = ekf_predict(self.x, self.P, lambda m: motion_model(m, u, dt), F, self.Q)

    def update(self, z, landmark) -> float:
        """Fuse one range–bearing measurement of a known landmark; return its NIS."""
        H = measurement_jacobian(self.x, landmark)
        self.x, self.P, nis = ekf_update(self.x, self.P, z, lambda m: measurement_model(m, landmark),
                                         H, self.R, angle_idx=(1,))
        self.x[2] = wrap_angle(self.x[2])
        return nis


# ----------------------------------------------------------------------------------------------
# Particle filter (learning goals)
# ----------------------------------------------------------------------------------------------
def systematic_resample(weights, rng) -> np.ndarray:
    """Systematic resampling: indices for N particles using one uniform offset u ~ U[0, 1/N)."""
    w = np.asarray(weights, dtype=float)
    n = len(w)
    positions = (rng.random() + np.arange(n)) / n
    c = np.cumsum(w / w.sum())
    c[-1] = 1.0
    return np.searchsorted(c, positions, side="right")


class ParticleFilter:
    """Bootstrap particle filter for the same models.

    particles: (N, 3); log-weights are kept for numerical stability. Resample (systematically)
    when the effective sample size N_eff = 1 / sum(w^2) drops below ``resample_threshold * N``.
    """

    def __init__(self, particles, Q, R, rng, resample_threshold: float = 0.5):
        self.particles = np.asarray(particles, dtype=float).copy()
        self.n = len(self.particles)
        self.logw = np.full(self.n, -np.log(self.n))
        self.Q, self.R, self.rng = np.asarray(Q, dtype=float), np.asarray(R, dtype=float), rng
        self.resample_threshold = resample_threshold
        self._Lq = np.linalg.cholesky(self.Q)
        self._Rinv = np.linalg.inv(self.R)

    @property
    def weights(self) -> np.ndarray:
        """Normalised weights (N,)."""
        w = np.exp(self.logw - self.logw.max())
        return w / w.sum()

    def predict(self, u, dt: float):
        """Move every particle with the motion model plus a N(0, Q) sample."""
        p = self.particles
        v, w = u
        p[:, 0] += v * dt * np.cos(p[:, 2])
        p[:, 1] += v * dt * np.sin(p[:, 2])
        p[:, 2] += w * dt
        p += self.rng.standard_normal((self.n, 3)) @ self._Lq.T
        p[:, 2] = wrap_angle(p[:, 2])

    def update(self, z, landmark):
        """Multiply weights by the Gaussian likelihood of z (bearing residual wrapped); resample if
        N_eff is low."""
        p = self.particles
        dx, dy = landmark[0] - p[:, 0], landmark[1] - p[:, 1]
        nu = np.column_stack([z[0] - np.hypot(dx, dy), wrap_angle(z[1] - (np.arctan2(dy, dx) - p[:, 2]))])
        self.logw += -0.5 * np.einsum("ni,ij,nj->n", nu, self._Rinv, nu)
        self.logw -= self.logw.max()
        w = self.weights
        if 1.0 / np.sum(w * w) < self.resample_threshold * self.n:
            idx = systematic_resample(w, self.rng)
            self.particles = self.particles[idx]
            self.logw = np.full(self.n, -np.log(self.n))

    def estimate(self):
        """Weighted mean (circular mean for theta) and weighted covariance (3x3)."""
        w = self.weights
        p = self.particles
        th = np.arctan2(w @ np.sin(p[:, 2]), w @ np.cos(p[:, 2]))
        mu = np.array([w @ p[:, 0], w @ p[:, 1], th])
        d = p - mu
        d[:, 2] = wrap_angle(d[:, 2])
        return mu, (d * w[:, None]).T @ d


def nees(x_true, x_est, P) -> float:
    """Normalised estimation error squared e^T P^-1 e (heading error wrapped)."""
    e = np.asarray(x_true, dtype=float) - np.asarray(x_est, dtype=float)
    e[2] = wrap_angle(e[2])
    return float(e @ np.linalg.solve(P, e))


# ----------------------------------------------------------------------------------------------
# Simulation and experiment drivers (provided in the starter)
# ----------------------------------------------------------------------------------------------
@dataclass
class SimRun:
    """One simulated run. measurements[k] is a list of (landmark_index, z) available after step k."""
    dt: float
    landmarks: np.ndarray
    truth: np.ndarray          # (T+1, 3)
    controls: np.ndarray       # (T, 2) odometry-reported (v, omega)
    measurements: list         # length T


def simulate(landmarks, controls, dt, Q, R, x0, rng, meas_every: int = 5, max_range: float = np.inf) -> SimRun:
    """Ground truth x_k = f(x_{k-1}, u_k) + w_k, w ~ N(0, Q); every ``meas_every`` steps, a
    range–bearing measurement of each landmark within ``max_range`` with noise N(0, R)."""
    landmarks = np.asarray(landmarks, dtype=float).reshape(-1, 2)
    controls = np.asarray(controls, dtype=float)
    Lq, Lr = np.linalg.cholesky(Q), np.linalg.cholesky(R)
    x = np.asarray(x0, dtype=float).copy()
    truth, meas = [x.copy()], []
    for k, u in enumerate(controls):
        x = _f_true(x, u, dt) + Lq @ rng.standard_normal(3)
        x[2] = wrap_angle(x[2])
        truth.append(x.copy())
        zs = []
        if (k + 1) % meas_every == 0:
            for i, lm in enumerate(landmarks):
                z = _h_true(x, lm)
                if z[0] <= max_range:
                    z = z + Lr @ rng.standard_normal(2)
                    z[1] = wrap_angle(z[1])
                    zs.append((i, z))
        meas.append(zs)
    return SimRun(dt, landmarks, np.array(truth), controls, meas)


def run_ekf(run: SimRun, x0, P0, Q, R, use_landmarks: bool = True) -> dict:
    """Run the EKF over a SimRun. Returns est (T+1,3), cov (T+1,3,3), nees (T+1,), nis (list)."""
    ekf = EKF(x0, P0, Q, R)
    est, cov, nis = [ekf.x.copy()], [ekf.P.copy()], []
    for u, zs in zip(run.controls, run.measurements):
        ekf.predict(u, run.dt)
        if use_landmarks:
            for i, z in zs:
                nis.append(ekf.update(z, run.landmarks[i]))
        est.append(ekf.x.copy())
        cov.append(ekf.P.copy())
    est, cov = np.array(est), np.array(cov)
    ne = np.array([nees(t, e, P) for t, e, P in zip(run.truth, est, cov)])
    return {"est": est, "cov": cov, "nees": ne, "nis": np.array(nis)}


def run_pf(run: SimRun, particles, Q, R, rng) -> dict:
    """Run the particle filter over a SimRun. Returns est (T+1,3), cov (T+1,3,3)."""
    pf = ParticleFilter(particles, Q, R, rng)
    m, c = pf.estimate()
    est, cov = [m], [c]
    for u, zs in zip(run.controls, run.measurements):
        pf.predict(u, run.dt)
        for i, z in zs:
            pf.update(z, run.landmarks[i])
        m, c = pf.estimate()
        est.append(m)
        cov.append(c)
    return {"est": np.array(est), "cov": np.array(cov)}


def dead_reckoning(run: SimRun, x0) -> np.ndarray:
    """Integrate the odometry controls only (no landmarks). Returns (T+1, 3)."""
    x = np.asarray(x0, dtype=float).copy()
    out = [x.copy()]
    for u in run.controls:
        x = motion_model(x, u, run.dt)
        out.append(x.copy())
    return np.array(out)


def position_rmse(truth, est) -> float:
    """RMS position error over a trajectory."""
    return float(np.sqrt(np.mean(np.sum((truth[:, :2] - est[:, :2]) ** 2, axis=1))))


# Scenario of lesson 06.6 (worked example): three fiducials, an arc at 0.5 m/s and 0.2 rad/s.
LESSON_LANDMARKS = np.array([[5.0, 0.0], [5.0, 8.0], [-2.0, 6.0]])
LESSON_DT = 0.1
LESSON_Q = np.diag([0.02 ** 2, 0.02 ** 2, np.radians(1.0) ** 2])
LESSON_R = np.diag([0.10 ** 2, np.radians(2.0) ** 2])
LESSON_P0 = np.diag([0.1 ** 2, 0.1 ** 2, np.radians(3.0) ** 2])


def monte_carlo_nees(n_runs: int = 50, n_steps: int = 300, seed: int = 0, q_scale: float = 1.0) -> dict:
    """Lesson 06.6 scenario, ``n_runs`` seeded runs. The filter uses Q * q_scale (q_scale = 1 is
    correctly tuned). Returns mean NEES per step (n_steps+1,), mean NIS per update, the 95 %
    band for the run-average, and the fraction of steps inside it."""
    rng = np.random.default_rng(seed)
    controls = np.tile([0.5, 0.2], (n_steps, 1))
    x_nom = np.array([0.0, 0.0, 0.0])
    ne, nis = [], []
    for _ in range(n_runs):
        x0_true = x_nom + np.linalg.cholesky(LESSON_P0) @ rng.standard_normal(3)
        run = simulate(LESSON_LANDMARKS, controls, LESSON_DT, LESSON_Q, LESSON_R, x0_true, rng)
        res = run_ekf(run, x_nom, LESSON_P0, LESSON_Q * q_scale, LESSON_R)
        ne.append(res["nees"])
        nis.append(res["nis"])
    mean_nees = np.mean(ne, axis=0)
    band = chi2_band(3, n_runs)
    inside = float(np.mean((mean_nees >= band[0]) & (mean_nees <= band[1])))
    return {"mean_nees": mean_nees, "band": band, "fraction_inside": inside,
            "mean_nis": float(np.mean(np.concatenate(nis)))}


def comparison_experiment(seed: int = 1, n_steps: int = 600, n_particles: int = 1000) -> dict:
    """Dead reckoning vs EKF vs PF on one lesson-scenario run with a known start.
    Returns position RMSE for each and the trajectories."""
    rng = np.random.default_rng(seed)
    controls = np.tile([0.5, 0.2], (n_steps, 1))
    x0 = np.zeros(3)
    run = simulate(LESSON_LANDMARKS, controls, LESSON_DT, LESSON_Q, LESSON_R, x0, rng)
    dr = dead_reckoning(run, x0)
    ek = run_ekf(run, x0, LESSON_P0, LESSON_Q, LESSON_R)
    parts = x0 + rng.standard_normal((n_particles, 3)) @ np.linalg.cholesky(LESSON_P0).T
    pf = run_pf(run, parts, LESSON_Q, LESSON_R, rng)
    return {"run": run, "dr": dr, "ekf": ek["est"], "pf": pf["est"],
            "rmse": {"dead_reckoning": position_rmse(run.truth, dr),
                     "ekf": position_rmse(run.truth, ek["est"]),
                     "pf": position_rmse(run.truth, pf["est"])}}


if __name__ == "__main__":  # experiment: NEES consistency and filter comparison plots
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(1, 2, figsize=(12, 5))
    for qs, lab in ((1.0, "Q correct"), (1 / 20, "Q / 20")):
        mc = monte_carlo_nees(50, 300, seed=0, q_scale=qs)
        ax[0].plot(mc["mean_nees"], label=f"{lab}: {100 * mc['fraction_inside']:.0f} % inside")
    lo, hi = chi2_band(3, 50)
    ax[0].axhline(lo, ls="--", c="k")
    ax[0].axhline(hi, ls="--", c="k")
    ax[0].set(yscale="log", xlabel="step", ylabel="mean NEES (50 runs)", title="EKF consistency")
    ax[0].legend()
    cmp = comparison_experiment()
    tr = cmp["run"].truth
    for key, lab in (("dr", "dead reckoning"), ("ekf", "EKF"), ("pf", "PF")):
        ax[1].plot(cmp[key][:, 0], cmp[key][:, 1], label=f"{lab} (RMSE {cmp['rmse'][ {'dr': 'dead_reckoning'}.get(key, key)]:.2f} m)")
    ax[1].plot(tr[:, 0], tr[:, 1], "k-", lw=0.8, label="truth")
    ax[1].plot(*LESSON_LANDMARKS.T, "r^", ms=10, label="landmarks")
    ax[1].set(aspect="equal", xlabel="x [m]", ylabel="y [m]", title="Localisation comparison")
    ax[1].legend()
    plt.tight_layout()
    plt.show()
