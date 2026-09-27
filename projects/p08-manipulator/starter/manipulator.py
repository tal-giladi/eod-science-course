"""[STARTER -- every function that raises NotImplementedError is yours to write; helpers that are implemented are given.]

manipulator -- kinematics, Jacobians, IK and statics for a fictional 5-DOF EOD-style arm (P08).

The arm ("Arm-5", lesson 06.3) sits on a turret on a mobile base:
turret yaw q1, shoulder pitch q2, elbow pitch q3, wrist pitch q4, wrist roll q5.
D1 = 0.35 m (turret to shoulder), A2 = 0.80 m (upper arm), A3 = 0.70 m (forearm),
D5 = 0.25 m (wrist to tool point). At q = 0 the arm is stretched horizontally forward and the tool
point is at (1.75, 0, 0.35). Positive pitch raises the arm. All dimensions are fictional.

Contents
--------
* SO(3)/SE(3): hat/vee, Rodrigues exp, log, closed-form SE(3) exp/log, adjoint.
* Forward kinematics by standard DH and by product of exponentials (PoE).
* Space Jacobian and point (linear-velocity) Jacobian.
* Damped-least-squares numerical IK with joint limits; analytic IK for Arm-5.
* Yoshikawa manipulability; reachability / singularity map in the vertical plane.
* Statics: tau = J^T F, gravity torques, payload-vs-reach curve.
* Pan-tilt "look-at" solver for a camera unit.

Twists are ordered (omega, v) as in Lynch & Park.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

# ---------------------------------------------------------------------------------------------
# Small helpers (given)
# ---------------------------------------------------------------------------------------------


def hat(w) -> np.ndarray:
    """so(3) hat: 3-vector -> 3x3 skew-symmetric matrix with hat(w) @ x == cross(w, x)."""
    return np.array([[0.0, -w[2], w[1]], [w[2], 0.0, -w[0]], [-w[1], w[0], 0.0]])


def vee(W: np.ndarray) -> np.ndarray:
    """Inverse of :func:`hat`."""
    return np.array([W[2, 1], W[0, 2], W[1, 0]])


def se3_hat(xi) -> np.ndarray:
    """6-vector twist (omega, v) -> 4x4 matrix in se(3)."""
    M = np.zeros((4, 4))
    M[:3, :3] = hat(xi[:3])
    M[:3, 3] = xi[3:]
    return M


def make_T(R, p) -> np.ndarray:
    """Homogeneous transform from rotation R and translation p."""
    T = np.eye(4)
    T[:3, :3] = R
    T[:3, 3] = p
    return T


def inv_T(T: np.ndarray) -> np.ndarray:
    """Inverse of a homogeneous transform (uses R^T, no general matrix inverse)."""
    R, p = T[:3, :3], T[:3, 3]
    return make_T(R.T, -R.T @ p)


def rot_x(t: float) -> np.ndarray:
    c, s = np.cos(t), np.sin(t)
    return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])


def rot_y(t: float) -> np.ndarray:
    c, s = np.cos(t), np.sin(t)
    return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])


def rot_z(t: float) -> np.ndarray:
    c, s = np.cos(t), np.sin(t)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])


# ---------------------------------------------------------------------------------------------
# 1. SO(3) / SE(3)
# ---------------------------------------------------------------------------------------------


def exp_so3(w) -> np.ndarray:
    """Rodrigues' formula: rotation vector w = theta * axis -> R in SO(3).

    ``R = I + sin(th) K + (1 - cos(th)) K^2`` with ``K = hat(axis)``. Must be accurate for
    ``|w| -> 0`` (use the Taylor series ``I + hat(w) + hat(w)^2 / 2`` below ~1e-8).
    """
    raise NotImplementedError("TODO: implement exp_so3")


def rodrigues(axis, angle: float) -> np.ndarray:
    """Rotation by ``angle`` about ``axis`` (need not be unit length)."""
    axis = np.asarray(axis, float)
    return exp_so3(axis / np.linalg.norm(axis) * angle)


def log_so3(R: np.ndarray) -> np.ndarray:
    """Matrix log of SO(3): returns rotation vector w with |w| in [0, pi] and exp_so3(w) == R.

    Compute theta with ``atan2(|vee(R - R^T)|/2, (tr R - 1)/2)``: ``arccos`` alone loses half the
    digits near pi. Robust in three regimes: theta ~ 0 (first-order formula), generic, and theta ~ pi (where
    ``R - R^T`` vanishes and the axis must come from the symmetric part ``(R + R^T)/2 - cos(th) I
    = (1 - cos th) a a^T``, with the sign taken from ``vee(R - R^T)``).
    """
    raise NotImplementedError("TODO: implement log_so3")


def exp_se3(xi) -> np.ndarray:
    """Closed-form exponential of a twist times angle, ``xi = (omega, v) * theta`` -> 4x4 T.

    For omega != 0 (theta = |omega part|, unit axis w, unit-speed v/theta):
    ``R = exp_so3(w th)``, ``p = (I th + (1 - cos th) [w] + (th - sin th) [w]^2) v``.
    For omega == 0: pure translation ``p = v``.
    """
    raise NotImplementedError("TODO: implement exp_se3")


def log_se3(T: np.ndarray) -> np.ndarray:
    """Inverse of :func:`exp_se3`: 4x4 T -> twist*angle 6-vector (omega*th, v*th).

    ``omega*th = log_so3(R)``; for th != 0, ``v = G^{-1}(th) p`` with
    ``G^{-1} = I/th - [w]/2 + (1/th - cot(th/2)/2) [w]^2`` (then multiply by th).
    """
    raise NotImplementedError("TODO: implement log_se3")


def adjoint(T: np.ndarray) -> np.ndarray:
    """6x6 adjoint ``[[R, 0], [[p] R, R]]`` mapping twists (omega, v) between frames."""
    raise NotImplementedError("TODO: implement adjoint")


# ---------------------------------------------------------------------------------------------
# 2. Arm-5 definition (given)
# ---------------------------------------------------------------------------------------------

D1, A2, A3, D5 = 0.35, 0.80, 0.70, 0.25
N_JOINTS = 5
#: standard DH rows (theta_offset, d, a, alpha); theta_i = q_i + theta_offset
DH_TABLE = [(0.0, D1, 0.0, np.pi / 2), (0.0, 0.0, A2, 0.0), (0.0, 0.0, A3, 0.0),
            (np.pi / 2, 0.0, 0.0, np.pi / 2), (0.0, D5, 0.0, 0.0)]
#: space screw axes at home, (omega, v) with v = -omega x q_point
S_LIST = np.array([[0, 0, 1, 0, 0, 0],
                   [0, -1, 0, D1, 0, 0],
                   [0, -1, 0, D1, 0, -A2],
                   [0, -1, 0, D1, 0, -(A2 + A3)],
                   [1, 0, 0, 0, D1, 0]], float)
M_HOME = make_T(np.array([[0, 0, 1], [0, -1, 0], [1, 0, 0]], float), [A2 + A3 + D5, 0, D1])
#: joint limits [rad], rows (low, high)
JOINT_LIMITS = np.radians([[-170, 170], [-40, 130], [-160, 160], [-120, 120], [-180, 180]])
#: link masses [kg]: upper arm, forearm, wrist + gripper (CoMs at link mid-points)
LINK_MASSES = (4.0, 3.0, 2.0)
#: holding-torque limits [N m] per joint (turret, shoulder, elbow, wrist pitch, roll)
TORQUE_LIMITS = np.array([150.0, 200.0, 100.0, 40.0, 20.0])
G = 9.81


# ---------------------------------------------------------------------------------------------
# 3. Forward kinematics
# ---------------------------------------------------------------------------------------------


def dh_transform(theta: float, d: float, a: float, alpha: float) -> np.ndarray:
    """Standard DH link transform ``Rz(theta) Tz(d) Tx(a) Rx(alpha)`` (4x4)."""
    raise NotImplementedError("TODO: implement dh_transform")


def fk_dh_frames(q) -> list[np.ndarray]:
    """All DH frames ``[T_00 = I, T_01, ..., T_05]`` (given; uses :func:`dh_transform`)."""
    Ts = [np.eye(4)]
    for (off, d, a, al), qi in zip(DH_TABLE, q):
        Ts.append(Ts[-1] @ dh_transform(qi + off, d, a, al))
    return Ts


def fk_dh(q) -> np.ndarray:
    """Tool pose T_05(q) from the DH table ``DH_TABLE``."""
    raise NotImplementedError("TODO: implement fk_dh")


def fk_poe(q) -> np.ndarray:
    """Tool pose by product of exponentials ``exp([S1] q1) ... exp([S5] q5) M_HOME``.

    Use the closed-form :func:`exp_se3` (no ``scipy.linalg.expm``).
    """
    raise NotImplementedError("TODO: implement fk_poe")


# ---------------------------------------------------------------------------------------------
# 4. Jacobians
# ---------------------------------------------------------------------------------------------


def jacobian_space(q) -> np.ndarray:
    """6x5 space Jacobian: column i = Ad(exp([S1]q1)...exp([S_{i-1}]q_{i-1})) S_i.

    Satisfies ``[V_s] = dT/dt T^{-1}`` with ``V_s = J_s(q) qdot``.
    """
    raise NotImplementedError("TODO: implement jacobian_space")


def point_jacobian(q, point=None, n_active: int | None = None) -> np.ndarray:
    """3xN Jacobian of the linear velocity of a point rigidly attached to the chain.

    ``point`` (base frame, current configuration) defaults to the tool point. Only the first
    ``n_active`` joints move the point (the other columns are zero) -- use this for link centres
    of mass. Formula: ``J_v - [p] J_omega`` from the space Jacobian.
    """
    raise NotImplementedError("TODO: implement point_jacobian")


# ---------------------------------------------------------------------------------------------
# 5. Inverse kinematics
# ---------------------------------------------------------------------------------------------


@dataclass
class IKResult:
    q: np.ndarray
    success: bool
    iterations: int
    error: float


def ik_dls(target, q0=None, task: str = "position", lam: float = 0.05, tol: float = 1e-6,
           max_iter: int = 300, limits: np.ndarray | None = JOINT_LIMITS, restarts: int = 5,
           seed: int = 0, max_step: float = 0.3) -> IKResult:
    """Damped-least-squares IK with joint limits.

    ``task="position"``: target is a 3-vector tool position; error ``e = p_d - p(q)`` and the
    3x5 :func:`point_jacobian`. ``task="pose"``: target is a 4x4 pose; error twist
    ``V_e = Ad(T) log_se3(T^{-1} T_d)`` and :func:`jacobian_space` (only poses a 5-DOF arm can
    reach will converge). Step: ``dq = J^T (J J^T + lam^2 I)^{-1} e``, scaled down so that
    ``max |dq| <= max_step`` (a trust region: far targets otherwise fling the arm into its limits);
    after every step clip ``q`` to ``limits``. Success iff ``|e| < tol``. If a run fails, retry from up to ``restarts`` random
    configurations inside the limits (deterministic ``seed``) and return the best result.
    Unreachable targets must return ``success=False`` together with the least-error configuration.
    """
    raise NotImplementedError("TODO: implement ik_dls")


def ik_analytic(p, pitch: float, roll: float, elbow_up: bool = True):
    """Closed-form Arm-5 IK (lesson 06.3 section 4) for tool position ``p``, approach pitch and roll.

    Returns q (5,) or ``None`` if the wrist centre is out of reach (|c3| > 1 beyond 1e-12).
    """
    raise NotImplementedError("TODO: implement ik_analytic")


# ---------------------------------------------------------------------------------------------
# 6. Manipulability and workspace maps
# ---------------------------------------------------------------------------------------------


def manipulability(J: np.ndarray) -> float:
    """Yoshikawa measure ``w = sqrt(det(J J^T))`` = product of the singular values of J (m x n, m <= n)."""
    raise NotImplementedError("TODO: implement manipulability")


def condition_number(J: np.ndarray) -> float:
    """sigma_max / sigma_min (inf at a singularity)."""
    s = np.linalg.svd(J, compute_uv=False)
    return float(s[0] / s[-1]) if s[-1] > 0 else np.inf


def reachability_map(n_samples: int = 25, cell: float = 0.1, extent: float = 2.0) -> dict:
    """Sample (q2, q3, q4) on a grid within limits (q1 = q5 = 0) and bin tool positions in the
    vertical x-z plane. Returns ``{"x_edges", "z_edges", "reachable" (bool grid [z, x]),
    "w_max" (max point-Jacobian manipulability per cell, NaN if unreachable)}``. (Given; it calls
    your :func:`fk_poe`, :func:`point_jacobian` and :func:`manipulability`.)
    """
    xe = np.arange(-extent, extent + cell, cell)
    ze = np.arange(-extent + D1, extent + D1 + cell, cell)
    wmax = np.full((len(ze) - 1, len(xe) - 1), np.nan)
    grids = [np.linspace(lo, hi, n_samples) for lo, hi in JOINT_LIMITS[1:4]]
    for q2 in grids[0]:
        for q3 in grids[1]:
            for q4 in grids[2]:
                q = np.array([0.0, q2, q3, q4, 0.0])
                p = fk_poe(q)[:3, 3]
                i, j = np.searchsorted(xe, p[0]) - 1, np.searchsorted(ze, p[2]) - 1
                if 0 <= i < wmax.shape[1] and 0 <= j < wmax.shape[0]:
                    w = manipulability(point_jacobian(q))
                    wmax[j, i] = w if np.isnan(wmax[j, i]) else max(wmax[j, i], w)
    return {"x_edges": xe, "z_edges": ze, "reachable": ~np.isnan(wmax), "w_max": wmax}


def plot_reachability(path: str, n_samples: int = 22) -> None:
    """Save a reachability / manipulability heat map of the x-z plane to ``path`` (given)."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    m = reachability_map(n_samples)
    fig, ax = plt.subplots(figsize=(7, 6))
    im = ax.pcolormesh(m["x_edges"], m["z_edges"], m["w_max"], cmap="viridis", shading="flat")
    fig.colorbar(im, label="max Yoshikawa manipulability (point Jacobian) [m^3]")
    ax.plot(0, D1, "r^", label="shoulder")
    ax.add_patch(plt.Circle((0, D1), A2 + A3 + D5, fill=False, ls="--", color="w", label="max reach"))
    ax.set_xlabel("x [m]"); ax.set_ylabel("z [m]"); ax.set_aspect("equal"); ax.legend(loc="lower left")
    ax.set_title("Arm-5 reachability and manipulability (q1 = 0)")
    fig.tight_layout(); fig.savefig(path, dpi=110); plt.close(fig)


# ---------------------------------------------------------------------------------------------
# 7. Statics
# ---------------------------------------------------------------------------------------------


def joint_torques(q, F) -> np.ndarray:
    """Joint torques balancing a force F (N, base frame) applied at the tool point: ``tau = J_p^T F``."""
    raise NotImplementedError("TODO: implement joint_torques")


def link_coms(q) -> list[tuple[np.ndarray, int]]:
    """Centres of mass (base frame) of upper arm, forearm, wrist+gripper, each with the number of
    joints that move it (given; mid-points of shoulder-elbow, elbow-wrist, wrist-tool)."""
    Ts = fk_dh_frames(q)
    sh, el, wr, tl = Ts[1][:3, 3], Ts[2][:3, 3], Ts[3][:3, 3], Ts[5][:3, 3]
    return [((sh + el) / 2, 2), ((el + wr) / 2, 3), ((wr + tl) / 2, 5)]


def gravity_torque(q, payload: float = 0.0, masses=LINK_MASSES) -> np.ndarray:
    """Motor torques needed to hold the arm and a payload (kg, at the tool point) statically.

    ``tau = sum_k J_{c_k}^T (m_k g z_hat) + J_p^T (m_payload g z_hat)``, using
    :func:`point_jacobian` with ``n_active`` for each link CoM from :func:`link_coms`.
    """
    raise NotImplementedError("TODO: implement gravity_torque")


def payload_vs_reach(reaches, torque_limits=TORQUE_LIMITS, masses=LINK_MASSES) -> tuple[np.ndarray, np.ndarray]:
    """Maximum static payload at each horizontal reach (tool at shoulder height, horizontal
    approach, elbow up), and the index of the limiting joint.

    For each reach: q from :func:`ik_analytic`; ``tau_self = gravity_torque(q, 0)``,
    ``tau_kg = gravity_torque(q, 1) - tau_self``; payload = ``min_j (limit_j - |tau_self_j|) / |tau_kg_j|``
    over joints with ``|tau_kg_j| > 1e-9``. Unreachable reaches give NaN and index -1.
    """
    raise NotImplementedError("TODO: implement payload_vs_reach")


# ---------------------------------------------------------------------------------------------
# 8. Pan-tilt look-at
# ---------------------------------------------------------------------------------------------


def look_at_pan_tilt(T_wb: np.ndarray, T_bp: np.ndarray, o_t, P_w) -> tuple[float, float, float]:
    """Pan and tilt (rad; pan positive left about z, tilt positive up) and range (m) that point a
    pan-tilt unit at world point ``P_w``.

    ``d = (T_wb T_bp)^{-1} P_w - o_t`` in the PTU base frame, ``pan = atan2(d_y, d_x)``,
    ``tilt = atan2(d_z, hypot(d_x, d_y))``. At the zenith singularity (``hypot < 1e-9``) return pan = 0.
    """
    raise NotImplementedError("TODO: implement look_at_pan_tilt")


if __name__ == "__main__":
    import os
    os.makedirs("p08_out", exist_ok=True)
    plot_reachability("p08_out/reachability.png")
    reaches = np.arange(0.3, 1.76, 0.05)
    pl, lim = payload_vs_reach(reaches)
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(reaches, pl, "o-")
    ax.set_xlabel("horizontal reach at shoulder height [m]"); ax.set_ylabel("max payload [kg]")
    ax.set_title("Arm-5 payload vs reach"); fig.tight_layout(); fig.savefig("p08_out/payload_vs_reach.png", dpi=110)
    for r, p, j in zip(reaches, pl, lim):
        print(f"reach {r:.2f} m  payload {p:5.1f} kg  limited by joint {j + 1}")
