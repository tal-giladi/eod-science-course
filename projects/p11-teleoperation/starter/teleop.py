"""teleop -- delayed teleoperation experiment harness (Project P11).

STARTER -- implement every function that raises NotImplementedError
(the helpers that are already implemented are not the learning goal). A simulated operator (noisy proportional controller with a reaction time)
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
MODES = ('continuous', 'move_and_wait', 'predictive')


def wrap_angle(a):
    """Wrap an angle (or array) to (-pi, pi]."""
    return (np.asarray(a) + np.pi) % (2 * np.pi) - np.pi if np.ndim(a) else (a + math.pi) % (2 * math.pi) - math.pi


def unicycle_step(x: float, y: float, th: float, v: float, w: float, dt: float):
    """Midpoint-heading unicycle integration over ``dt``. Returns (x, y, th)."""
    thm = th + 0.5 * w * dt
    return (x + v * math.cos(thm) * dt, y + v * math.sin(thm) * dt, th + w * dt)


def polyline_distance(px: np.ndarray, py: np.ndarray, pts: np.ndarray) -> np.ndarray:
    """Distance from each point (px, py) to the polyline through ``pts`` (M, 2)."""
    best = np.full(np.shape(px), np.inf)
    for a, b in zip(pts[:-1], pts[1:]):
        ab = b - a
        L2 = float(ab @ ab)
        s = np.clip(((px - a[0]) * ab[0] + (py - a[1]) * ab[1]) / L2, 0, 1) if L2 > 0 else 0.0
        best = np.minimum(best, np.hypot(px - (a[0] + s * ab[0]), py - (a[1] + s * ab[1])))
    return best


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
    k_v: float = 1.0
    k_w: float = 2.0
    reaction_time: float = 0.2
    noise: float = 0.05
    pass_radius: float = 0.3
    tolerance: float = 0.1
    settle_speed: float = 0.02
    hold_time: float = 0.3
    mw_speed: float = 0.5
    mw_turn_rate: float = 1.0
    mw_error: float = 0.1


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
        return {k: getattr(self, k) for k in ('completed', 'completion_time', 'final_error', 'overshoot', 'path_error_rms', 'path_length_ratio', 'collisions', 'n_commands', 'n_moves')}


class Channel:
    """One-way packet link: delay + U(-jitter, +jitter) (never negative), i.i.d. loss.

    ``send(t, seq, payload)`` returns False if the packet was lost. ``receive(t)`` returns the
    packets that have arrived by time ``t`` (in arrival order) and removes them from the link.
    Random draws happen only for features that are enabled (jitter > 0, loss > 0)."""

    def __init__(self, delay: float, jitter: float=0.0, loss: float=0.0, rng=None):
        self.delay, self.jitter, self.loss = (float(delay), float(jitter), float(loss))
        self.rng = rng if rng is not None else np.random.default_rng(0)
        self._heap: list = []
        self._n = 0
        self.sent = self.lost = 0

    def send(self, t: float, seq: int, payload) -> bool:
        raise NotImplementedError('TODO: implement Channel.send')

    def receive(self, t: float) -> list:
        raise NotImplementedError('TODO: implement Channel.receive')


class Robot:
    """Unicycle executing the newest command plan it has received.

    A plan is a list of segments (v, w, duration); duration may be ``inf`` (hold until
    replaced). Packets with a sequence number not newer than the current plan are ignored
    (reordering under jitter). Speeds are clipped to the robot's limits."""

    def __init__(self, pose, params: RobotParams=RobotParams()):
        self.x, self.y, self.th = map(float, pose)
        self.p = params
        self.plan: list = []
        self.seq = 0
        self.v = 0.0

    def accept(self, packets: list) -> None:
        raise NotImplementedError('TODO: implement Robot.accept')

    def step(self, dt: float) -> None:
        raise NotImplementedError('TODO: implement Robot.step')

    @property
    def busy(self) -> bool:
        raise NotImplementedError('TODO: implement Robot.busy')


def p_command(pose, target, op: OperatorParams, rp: RobotParams, extra_along: float=0.0):
    """Proportional operator law on the displayed pose.

    Heading error e = wrap(bearing - theta); if |e| > pi/2 the operator reverses (heading error
    wrapped by pi). Along-track error = dist * cos(bearing - theta) + ``extra_along`` (remaining
    course length after this waypoint, so intermediate waypoints are passed at speed).
    v = k_v * along (clipped), w = k_w * e (clipped). Returns (v, w)."""
    raise NotImplementedError('TODO: implement p_command')


def predict_ghost(pose, applied_seq: int, sent: dict, dt: float, model_gain: float=1.0):
    """Dead-reckoned ghost: integrate every sent command with seq > ``applied_seq`` for one
    command period ``dt`` from the telemetry ``pose``, scaling speeds by ``model_gain``
    (1.0 = perfect model). ``sent`` maps seq -> (v, w)."""
    raise NotImplementedError('TODO: implement predict_ghost')


def plan_move(pose, target, op: OperatorParams, rng) -> list:
    """Move-and-wait open-loop plan: turn in place, then drive straight. The operator's judgement
    error per move: the turn angle is off by N(0, mw_error) rad and the drive distance is scaled by
    (1 + N(0, mw_error)), so the residual error after a move is about mw_error * sqrt(2) * distance."""
    raise NotImplementedError('TODO: implement plan_move')


def run_episode(course: Course, mode: str='continuous', round_trip: float=0.0, jitter: float=0.0, loss: float=0.0, op: OperatorParams | None=None, robot: RobotParams | None=None, dt: float=0.02, t_max: float=120.0, seed: int=0, model_gain: float=1.0) -> EpisodeResult:
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
    raise NotImplementedError('TODO: implement run_episode')


def sweep_latency(course: Course, round_trips, modes=MODES, seeds=(0, 1, 2), **kwargs) -> list[dict]:
    """Run every (round_trip, mode, seed) and return one row per (round_trip, mode) with the mean
    of each numeric metric, the completion rate and the number of seeds."""
    raise NotImplementedError('TODO: implement sweep_latency')


def format_table(rows: list[dict]) -> str:
    """Plain-text table of sweep rows."""
    cols = ('round_trip', 'mode', 'completion_rate', 'completion_time', 'final_error', 'overshoot', 'path_error_rms', 'collisions')
    lines = [' | '.join((f'{c:>15s}' for c in cols))]
    for r in rows:
        lines.append(' | '.join((f'{r[c]:>15.3f}' if isinstance(r[c], float) else f'{str(r[c]):>15s}' for c in cols)))
    return '\n'.join(lines)


def plot_sweep(rows: list[dict], path=None):
    """Completion time and overshoot vs round-trip delay, one line per mode."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 2, figsize=(10, 4))
    for mode in sorted({r['mode'] for r in rows}):
        rr = [r for r in rows if r['mode'] == mode]
        ax[0].plot([r['round_trip'] for r in rr], [r['completion_time'] for r in rr], 'o-', label=mode)
        ax[1].plot([r['round_trip'] for r in rr], [r['overshoot'] for r in rr], 'o-', label=mode)
    ax[0].set(xlabel='round-trip delay [s]', ylabel='completion time [s]')
    ax[1].set(xlabel='round-trip delay [s]', ylabel='overshoot [m]')
    ax[0].legend()
    fig.tight_layout()
    if path:
        fig.savefig(path, dpi=120)
    return fig


def critical_gain(tau: float) -> float:
    """Stability limit of K e^{-s tau} / s: K tau = pi / 2."""
    raise NotImplementedError('TODO: implement critical_gain')


def phase_margin(K: float, tau: float) -> float:
    """PM = pi/2 - K tau [rad] (crossover at omega_c = K)."""
    raise NotImplementedError('TODO: implement phase_margin')


def simulate_p_loop(K: float, tau: float, T: float=10.0, dt: float=0.001, r: float=1.0, smith: bool=False, tau_model: float | None=None):
    """Euler simulation of x' = u(t - tau), u = K (r - y) with y = x (plain) or, with a Smith
    predictor, y = x + x_m(t) - x_m(t - tau_model) where x_m' = u is the delay-free model.
    Returns (t, x)."""
    raise NotImplementedError('TODO: implement simulate_p_loop')


def envelope_growth(t: np.ndarray, x: np.ndarray, r: float=1.0) -> float:
    """Ratio of max |r - x| over the last third of the record to that over the middle third
    (> 1: growing oscillation / unstable; < 1: decaying)."""
    e = np.abs(r - x)
    n = len(e)
    mid, last = (e[n // 3:2 * n // 3].max(), e[2 * n // 3:].max())
    return float(last / max(mid, 1e-300))


def find_stability_limit(tau: float, K_lo: float | None=None, K_hi: float | None=None, rel_tol: float=0.002, periods: float=60.0) -> float:
    """Bisection on K for the boundary between decaying and growing oscillation of the simulated
    loop (dt = tau/200, record length ``periods`` x tau)."""
    raise NotImplementedError('TODO: implement find_stability_limit')


def oscillation_frequency(t: np.ndarray, x: np.ndarray, r: float=1.0) -> float:
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
