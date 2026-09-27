"""teleop -- delayed teleoperation experiment harness (Project P11).

Reference solution. A simulated operator (noisy proportional controller with a reaction time)
drives a unicycle robot to waypoints through an uplink/downlink channel with delay, jitter and
packet loss. Three operating modes are compared:

* ``continuous``    -- the operator steers continuously on the (delayed) telemetry display;
* ``move_and_wait`` -- Ferrell's strategy: open-loop move, wait for the display to settle, repeat;
* ``predictive``    -- the operator steers a dead-reckoned "ghost" (a Smith predictor for the
  human): last telemetry pose + commands sent but not yet reflected in telemetry.

All packets are sequence-numbered and time-stamped by their sender; the operator never reads the
robot's true state (no global-clock cheating). Everything is deterministic given ``seed``.

Also included: the 1-D proportional loop with pure delay, x' = K (r - x(t - tau)), whose
stability limit is K tau < pi/2 (lesson 06.5 section 3), a numeric limit finder and a Smith
predictor for comparison.
"""
from __future__ import annotations

import heapq
import math
from dataclasses import dataclass, field

import numpy as np

MODES = ("continuous", "move_and_wait", "predictive")


# ----------------------------------------------------------------------------- helpers (given)
def wrap_angle(a):
    """Wrap an angle (or array) to (-pi, pi]."""
    return (np.asarray(a) + np.pi) % (2 * np.pi) - np.pi if np.ndim(a) else (a + math.pi) % (2 * math.pi) - math.pi


def unicycle_step(x: float, y: float, th: float, v: float, w: float, dt: float):
    """Midpoint-heading unicycle integration over ``dt``. Returns (x, y, th)."""
    thm = th + 0.5 * w * dt
    return x + v * math.cos(thm) * dt, y + v * math.sin(thm) * dt, th + w * dt


def polyline_distance(px: np.ndarray, py: np.ndarray, pts: np.ndarray) -> np.ndarray:
    """Distance from each point (px, py) to the polyline through ``pts`` (M, 2)."""
    best = np.full(np.shape(px), np.inf)
    for a, b in zip(pts[:-1], pts[1:]):
        ab = b - a
        L2 = float(ab @ ab)
        s = np.clip(((px - a[0]) * ab[0] + (py - a[1]) * ab[1]) / L2, 0, 1) if L2 > 0 else 0.0
        best = np.minimum(best, np.hypot(px - (a[0] + s * ab[0]), py - (a[1] + s * ab[1])))
    return best


# ----------------------------------------------------------------------------- data classes
@dataclass
class Course:
    """Start pose (x, y, theta), waypoints [(x, y), ...] and circular obstacles [(x, y, r)]."""
    start: tuple = (0.0, 0.0, 0.0)
    waypoints: tuple = ((4.0, 0.0),)
    obstacles: tuple = ()

    def polyline(self) -> np.ndarray:
        return np.array([self.start[:2], *self.waypoints], dtype=float)


@dataclass
class OperatorParams:
    """Synthetic operator. Gains in 1/s; times in s; distances in m."""
    k_v: float = 1.0              # speed per metre of along-track error
    k_w: float = 2.0              # turn rate per radian of heading error
    reaction_time: float = 0.2    # perception-to-action latency (NOT compensated by any display)
    noise: float = 0.05           # relative (multiplicative) command noise std
    pass_radius: float = 0.3      # intermediate waypoints count as passed inside this radius
    tolerance: float = 0.1        # final-waypoint tolerance
    settle_speed: float = 0.02    # displayed speed below which the robot "has stopped"
    hold_time: float = 0.3        # final waypoint must be held this long on the display
    mw_speed: float = 0.5         # move-and-wait drive speed
    mw_turn_rate: float = 1.0     # move-and-wait turn rate
    mw_error: float = 0.1         # open-loop error per move: heading std [rad] and distance std [fraction]


@dataclass
class RobotParams:
    v_max: float = 1.0
    w_max: float = 1.5
    radius: float = 0.25


@dataclass
class EpisodeResult:
    completed: bool
    completion_time: float
    final_error: float
    overshoot: float
    path_error_rms: float
    path_length_ratio: float
    collisions: int
    n_commands: int
    n_moves: int
    t: np.ndarray = field(repr=False, default=None)
    xy: np.ndarray = field(repr=False, default=None)
    ghost: np.ndarray = field(repr=False, default=None)

    def metrics(self) -> dict:
        return {k: getattr(self, k) for k in ("completed", "completion_time", "final_error", "overshoot",
                                               "path_error_rms", "path_length_ratio", "collisions",
                                               "n_commands", "n_moves")}


# ----------------------------------------------------------------------------- channel
class Channel:
    """One-way packet link: delay + U(-jitter, +jitter) (never negative), i.i.d. loss.

    ``send(t, seq, payload)`` returns False if the packet was lost. ``receive(t)`` returns the
    packets that have arrived by time ``t`` (in arrival order) and removes them from the link.
    Random draws happen only for features that are enabled (jitter > 0, loss > 0)."""

    def __init__(self, delay: float, jitter: float = 0.0, loss: float = 0.0, rng=None):
        self.delay, self.jitter, self.loss = float(delay), float(jitter), float(loss)
        self.rng = rng if rng is not None else np.random.default_rng(0)
        self._heap: list = []
        self._n = 0
        self.sent = self.lost = 0

    def send(self, t: float, seq: int, payload) -> bool:
        self.sent += 1
        if self.loss > 0 and self.rng.uniform() < self.loss:
            self.lost += 1
            return False
        d = self.delay + (self.rng.uniform(-self.jitter, self.jitter) if self.jitter > 0 else 0.0)
        heapq.heappush(self._heap, (t + max(d, 0.0), self._n, seq, t, payload))
        self._n += 1
        return True

    def receive(self, t: float) -> list:
        out = []
        while self._heap and self._heap[0][0] <= t + 1e-9:
            arr, _, seq, ts, payload = heapq.heappop(self._heap)
            out.append((seq, ts, payload))
        return out


# ----------------------------------------------------------------------------- robot
class Robot:
    """Unicycle executing the newest command plan it has received.

    A plan is a list of segments (v, w, duration); duration may be ``inf`` (hold until
    replaced). Packets with a sequence number not newer than the current plan are ignored
    (reordering under jitter). Speeds are clipped to the robot's limits."""

    def __init__(self, pose, params: RobotParams = RobotParams()):
        self.x, self.y, self.th = map(float, pose)
        self.p = params
        self.plan: list = []
        self.seq = 0
        self.v = 0.0

    def accept(self, packets: list) -> None:
        for seq, _, plan in packets:
            if seq > self.seq:
                self.seq = seq
                self.plan = [list(s) for s in plan]

    def step(self, dt: float) -> None:
        rem, v_used = dt, 0.0
        while rem > 1e-12 and self.plan:
            v, w, dur = self.plan[0]
            v = float(np.clip(v, -self.p.v_max, self.p.v_max))
            w = float(np.clip(w, -self.p.w_max, self.p.w_max))
            h = min(rem, dur)
            self.x, self.y, self.th = unicycle_step(self.x, self.y, self.th, v, w, h)
            v_used = v
            rem -= h
            self.plan[0][2] = dur - h
            if self.plan[0][2] <= 1e-12:
                self.plan.pop(0)
        self.v = v_used if rem < dt else 0.0

    @property
    def busy(self) -> bool:
        return bool(self.plan) and any(abs(s[0]) > 0 or abs(s[1]) > 0 for s in self.plan)


# ----------------------------------------------------------------------------- operator
def p_command(pose, target, op: OperatorParams, rp: RobotParams, extra_along: float = 0.0):
    """Proportional operator law on the displayed pose.

    Heading error e = wrap(bearing - theta); if |e| > pi/2 the operator reverses (heading error
    wrapped by pi). Along-track error = dist * cos(bearing - theta) + ``extra_along`` (remaining
    course length after this waypoint, so intermediate waypoints are passed at speed).
    v = k_v * along (clipped), w = k_w * e (clipped). Returns (v, w)."""
    x, y, th = pose
    dx, dy = target[0] - x, target[1] - y
    dist = math.hypot(dx, dy)
    if dist < 1e-9:
        return 0.0, 0.0
    brg = math.atan2(dy, dx)
    e = wrap_angle(brg - th)
    along = dist * math.cos(brg - th)
    if abs(e) > math.pi / 2:
        e = wrap_angle(e - math.pi)
    else:
        along += extra_along
    v = float(np.clip(op.k_v * along, -rp.v_max, rp.v_max))
    w = float(np.clip(op.k_w * e, -rp.w_max, rp.w_max))
    return v, w


def predict_ghost(pose, applied_seq: int, sent: dict, dt: float, model_gain: float = 1.0):
    """Dead-reckoned ghost: integrate every sent command with seq > ``applied_seq`` for one
    command period ``dt`` from the telemetry ``pose``, scaling speeds by ``model_gain``
    (1.0 = perfect model). ``sent`` maps seq -> (v, w)."""
    x, y, th = pose
    for s in sorted(k for k in sent if k > applied_seq):
        v, w = sent[s]
        x, y, th = unicycle_step(x, y, th, model_gain * v, model_gain * w, dt)
    return x, y, th


def plan_move(pose, target, op: OperatorParams, rng) -> list:
    """Move-and-wait open-loop plan: turn in place, then drive straight. The operator's judgement
    error per move: the turn angle is off by N(0, mw_error) rad and the drive distance is scaled by
    (1 + N(0, mw_error)), so the residual error after a move is about mw_error * sqrt(2) * distance."""
    x, y, th = pose
    dx, dy = target[0] - x, target[1] - y
    dist = math.hypot(dx, dy)
    dth = wrap_angle(math.atan2(dy, dx) - th)
    e1, e2 = rng.normal(0.0, op.mw_error, 2)
    plan = []
    dth += e1
    if abs(dth) > 1e-6:
        plan.append((0.0, math.copysign(op.mw_turn_rate, dth), abs(dth) / op.mw_turn_rate))
    plan.append((op.mw_speed, 0.0, dist / op.mw_speed * max(1 + e2, 0.0)))
    return plan


# ----------------------------------------------------------------------------- episode
def run_episode(course: Course, mode: str = "continuous", round_trip: float = 0.0, jitter: float = 0.0,
                loss: float = 0.0, op: OperatorParams | None = None, robot: RobotParams | None = None,
                dt: float = 0.02, t_max: float = 120.0, seed: int = 0, model_gain: float = 1.0) -> EpisodeResult:
    """Simulate one run and return its metrics.

    The round-trip delay is split equally between uplink and downlink (``jitter`` applies to
    each). Step order at time t = k dt: (1) operator reads telemetry arrived by t and decides;
    decisions enter the reaction pipeline and are sent ``reaction_time`` later; (2) robot applies
    the newest plan received by t, integrates over dt and sends telemetry stamped t + dt.

    * continuous / predictive: one hold-command per step; the control pose is the telemetry pose
      (continuous) or the ghost (predictive). Intermediate waypoints switch on the control pose;
      the run ends when *telemetry* shows the final waypoint within tolerance, below
      ``settle_speed``, for ``hold_time``.
    * move_and_wait: when the display shows the last plan finished and the robot at rest, the
      operator either advances the waypoint (inside pass_radius / tolerance for the final one,
      which ends the run) or sends a new open-loop plan. Lost plans are re-planned after a timeout.

    Metrics: completion time (declaration time), final error (true distance at declaration),
    overshoot (max along-track travel past the final waypoint, >= 0), RMS distance from the
    course polyline, path-length ratio, collisions (entries into an obstacle inflated by the
    robot radius), number of commands and of move-and-wait moves.
    """
    if mode not in MODES:
        raise ValueError(mode)
    op = op or OperatorParams()
    rp = robot or RobotParams()
    rng = np.random.default_rng(seed)
    up = Channel(round_trip / 2, jitter, loss, np.random.default_rng(rng.integers(2 ** 32)))
    down = Channel(round_trip / 2, jitter, loss, np.random.default_rng(rng.integers(2 ** 32)))
    op_rng = np.random.default_rng(rng.integers(2 ** 32))
    bot = Robot(course.start, rp)
    wps = [tuple(map(float, w)) for w in course.waypoints]
    poly = course.polyline()
    seg_len = np.hypot(*np.diff(poly, axis=0).T)
    remaining_after = [float(seg_len[i + 1:].sum()) for i in range(len(wps))]

    disp = {"t": 0.0, "pose": tuple(map(float, course.start)), "seq": 0, "busy": False, "v": 0.0}
    sent: dict = {}
    pipeline: list = []          # (release_time, plan)
    seq = 0
    active = 0
    hold_since = None
    done_t = None
    n_moves = 0
    mw_wait_until = -1.0
    mw_last_seq = 0
    nsteps = int(round(t_max / dt))
    T = np.empty(nsteps + 1); XY = np.empty((nsteps + 1, 2)); G = np.empty((nsteps + 1, 2))
    T[0], XY[0], G[0] = 0.0, course.start[:2], course.start[:2]
    k_end = nsteps
    for k in range(nsteps):
        t = k * dt
        # ---- operator: read display
        for _, ts, tel in down.receive(t):
            if ts >= disp["t"]:
                disp = tel
        tel_pose = disp["pose"]
        if mode == "predictive":
            ctrl = predict_ghost(tel_pose, disp["seq"], sent, dt, model_gain)
        else:
            ctrl = tel_pose
        G[k] = ctrl[:2]
        final = active == len(wps) - 1
        # ---- operator: decide
        decision = None
        if mode in ("continuous", "predictive"):
            tgt = wps[active]
            if not final and math.dist(ctrl[:2], tgt) < op.pass_radius:
                active += 1
                final = active == len(wps) - 1
                tgt = wps[active]
            v, w = p_command(ctrl, tgt, op, rp, remaining_after[active])
            v *= 1 + op.noise * op_rng.standard_normal()
            w *= 1 + op.noise * op_rng.standard_normal()
            decision = [(v, w, math.inf)]
            if final and math.dist(tel_pose[:2], wps[-1]) < op.tolerance and abs(disp["v"]) < op.settle_speed:
                hold_since = t if hold_since is None else hold_since
                if t - hold_since >= op.hold_time - 1e-9:
                    done_t = t
            else:
                hold_since = None
        else:  # move_and_wait
            settled = disp["seq"] >= mw_last_seq and not disp["busy"] and not pipeline
            timed_out = mw_last_seq > 0 and t > mw_wait_until and not pipeline
            if settled or timed_out:
                tgt = wps[active]
                tol = op.tolerance if final else op.pass_radius
                if math.dist(tel_pose[:2], tgt) < tol and settled:
                    if final:
                        done_t = t
                    else:
                        active += 1
                        tgt = wps[active]
                if done_t is None:
                    decision = plan_move(tel_pose, tgt, op, op_rng)
                    n_moves += 1
                    dur = sum(s[2] for s in decision)
                    mw_wait_until = t + op.reaction_time + dur + 2 * (round_trip + 2 * jitter) + 1.0
                    mw_last_seq = seq + 1 + sum(1 for _ in pipeline)
        if done_t is not None:
            k_end = k
            break
        if decision is not None:
            pipeline.append((t + op.reaction_time, decision))
        while pipeline and pipeline[0][0] <= t + 1e-9:
            _, plan = pipeline.pop(0)
            seq += 1
            if plan[0][2] == math.inf:
                sent[seq] = (plan[0][0], plan[0][1])
            up.send(t, seq, plan)
        # prune ghost history that telemetry has confirmed
        if mode == "predictive" and len(sent) > 2000:
            for s in [s for s in sent if s <= disp["seq"]]:
                del sent[s]
        # ---- robot
        bot.accept(up.receive(t))
        bot.step(dt)
        tel = {"t": t + dt, "pose": (bot.x, bot.y, bot.th), "seq": bot.seq, "busy": bot.busy, "v": bot.v}
        down.send(t + dt, bot.seq, tel)
        T[k + 1], XY[k + 1] = t + dt, (bot.x, bot.y)
        G[k + 1] = G[k]
    T, XY, G = T[:k_end + 1], XY[:k_end + 1], G[:k_end + 1]
    completed = done_t is not None
    ct = done_t if completed else t_max
    goal = np.array(wps[-1])
    direction = poly[-1] - poly[-2]
    direction = direction / (np.linalg.norm(direction) or 1.0)
    overshoot = float(max(((XY - goal) @ direction).max(), 0.0))
    perr = polyline_distance(XY[:, 0], XY[:, 1], poly)
    travelled = float(np.hypot(*np.diff(XY, axis=0).T).sum())
    collisions = 0
    for ox, oy, r in course.obstacles:
        inside = np.hypot(XY[:, 0] - ox, XY[:, 1] - oy) < r + rp.radius
        collisions += int(inside[0]) + int(np.sum(inside[1:] & ~inside[:-1]))
    return EpisodeResult(completed, float(ct), float(np.hypot(*(XY[-1] - goal))), overshoot,
                         float(np.sqrt(np.mean(perr ** 2))), travelled / float(seg_len.sum()),
                         collisions, seq, n_moves, T, XY, G)


# ----------------------------------------------------------------------------- experiment harness
def sweep_latency(course: Course, round_trips, modes=MODES, seeds=(0, 1, 2), **kwargs) -> list[dict]:
    """Run every (round_trip, mode, seed) and return one row per (round_trip, mode) with the mean
    of each numeric metric, the completion rate and the number of seeds."""
    rows = []
    for tau in round_trips:
        for mode in modes:
            ms = [run_episode(course, mode, tau, seed=s, **kwargs).metrics() for s in seeds]
            row = {"round_trip": float(tau), "mode": mode, "n": len(ms),
                   "completion_rate": float(np.mean([m["completed"] for m in ms]))}
            for key in ("completion_time", "final_error", "overshoot", "path_error_rms",
                        "path_length_ratio", "collisions", "n_moves"):
                row[key] = float(np.mean([m[key] for m in ms]))
            rows.append(row)
    return rows


def format_table(rows: list[dict]) -> str:
    """Plain-text table of sweep rows."""
    cols = ("round_trip", "mode", "completion_rate", "completion_time", "final_error", "overshoot",
            "path_error_rms", "collisions")
    lines = [" | ".join(f"{c:>15s}" for c in cols)]
    for r in rows:
        lines.append(" | ".join(f"{r[c]:>15.3f}" if isinstance(r[c], float) else f"{str(r[c]):>15s}" for c in cols))
    return "\n".join(lines)


def plot_sweep(rows: list[dict], path=None):  # pragma: no cover - plotting
    """Completion time and overshoot vs round-trip delay, one line per mode."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 2, figsize=(10, 4))
    for mode in sorted({r["mode"] for r in rows}):
        rr = [r for r in rows if r["mode"] == mode]
        ax[0].plot([r["round_trip"] for r in rr], [r["completion_time"] for r in rr], "o-", label=mode)
        ax[1].plot([r["round_trip"] for r in rr], [r["overshoot"] for r in rr], "o-", label=mode)
    ax[0].set(xlabel="round-trip delay [s]", ylabel="completion time [s]")
    ax[1].set(xlabel="round-trip delay [s]", ylabel="overshoot [m]")
    ax[0].legend()
    fig.tight_layout()
    if path:
        fig.savefig(path, dpi=120)
    return fig


# ----------------------------------------------------------------------------- 1-D delay loop theory
def critical_gain(tau: float) -> float:
    """Stability limit of K e^{-s tau} / s: K tau = pi / 2."""
    return math.pi / (2 * tau)


def phase_margin(K: float, tau: float) -> float:
    """PM = pi/2 - K tau [rad] (crossover at omega_c = K)."""
    return math.pi / 2 - K * tau


def simulate_p_loop(K: float, tau: float, T: float = 10.0, dt: float = 1e-3, r: float = 1.0,
                    smith: bool = False, tau_model: float | None = None):
    """Euler simulation of x' = u(t - tau), u = K (r - y) with y = x (plain) or, with a Smith
    predictor, y = x + x_m(t) - x_m(t - tau_model) where x_m' = u is the delay-free model.
    Returns (t, x)."""
    N, d = int(round(T / dt)), int(round(tau / dt))
    dm = int(round((tau if tau_model is None else tau_model) / dt))
    u = np.zeros(N); x = np.zeros(N); xm = np.zeros(N)
    for k in range(1, N):
        y = x[k - 1]
        if smith:
            y += xm[k - 1] - (xm[k - 1 - dm] if k - 1 - dm >= 0 else 0.0)
        u[k - 1] = K * (r - y)
        xm[k] = xm[k - 1] + u[k - 1] * dt
        x[k] = x[k - 1] + (u[k - 1 - d] if k - 1 - d >= 0 else 0.0) * dt
    return np.arange(N) * dt, x


def envelope_growth(t: np.ndarray, x: np.ndarray, r: float = 1.0) -> float:
    """Ratio of max |r - x| over the last third of the record to that over the middle third
    (> 1: growing oscillation / unstable; < 1: decaying)."""
    e = np.abs(r - x)
    n = len(e)
    mid, last = e[n // 3: 2 * n // 3].max(), e[2 * n // 3:].max()
    return float(last / max(mid, 1e-300))


def find_stability_limit(tau: float, K_lo: float | None = None, K_hi: float | None = None,
                         rel_tol: float = 2e-3, periods: float = 60.0) -> float:
    """Bisection on K for the boundary between decaying and growing oscillation of the simulated
    loop (dt = tau/200, record length ``periods`` x tau)."""
    K_lo = 0.5 / tau if K_lo is None else K_lo
    K_hi = 3.0 / tau if K_hi is None else K_hi
    dt = tau / 200
    while (K_hi - K_lo) / K_lo > rel_tol:
        K = 0.5 * (K_lo + K_hi)
        t, x = simulate_p_loop(K, tau, T=periods * tau, dt=dt)
        if envelope_growth(t, x) > 1.0:
            K_hi = K
        else:
            K_lo = K
    return 0.5 * (K_lo + K_hi)


def oscillation_frequency(t: np.ndarray, x: np.ndarray, r: float = 1.0) -> float:
    """Angular frequency [rad/s] from the mean spacing of zero crossings of r - x in the second
    half of the record."""
    h = len(t) // 2
    e = r - x[h:]
    tt = t[h:]
    idx = np.nonzero(np.signbit(e[1:]) != np.signbit(e[:-1]))[0]
    if len(idx) < 3:
        return 0.0
    tc = tt[idx] - e[idx] * (tt[idx + 1] - tt[idx]) / (e[idx + 1] - e[idx])
    return float(math.pi / np.mean(np.diff(tc)))


if __name__ == "__main__":  # pragma: no cover
    c = Course(start=(0, 0, 0), waypoints=((3, 0), (3, 3), (0, 3)))
    print(format_table(sweep_latency(c, (0.0, 0.5, 1.0, 2.0))))
    print("K_crit(0.5) numeric", find_stability_limit(0.5), "theory", critical_gain(0.5))
