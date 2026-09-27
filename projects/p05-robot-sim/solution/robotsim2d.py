"""robotsim2d — a small, deterministic 2D mobile-robot simulator (Project P05, reference solution).

Coordinates: world frame x right, y up, metres; heading theta in radians, counter-clockwise from +x.
Body frame: x forward, y left. A pose is a length-3 array (x, y, theta).

Contents
- geometry: polygons/boxes, point-in-polygon, segment tests, point–segment distance
- World: rectangular arena + polygon obstacles, collision checks
- ray casting and a noisy Lidar
- kinematics: exact SE(2) integration of a body twist, unicycle, skid-steer (ICR slip model)
- WheelOdometry with scale bias and noise
- Channel with latency, jitter, packet loss (optionally FIFO)
- PID with anti-windup, WaypointFollower
- Simulator with trajectory logging, and matplotlib rendering

Other projects (P04, P06, P07, P08, P11) can import this module by inserting
``projects/p05-robot-sim/solution`` (or ``starter``) into ``sys.path``; see the README.
"""
from __future__ import annotations

import heapq
import math
from dataclasses import dataclass, field

import numpy as np

__all__ = [
    "wrap_angle", "box", "regular_polygon", "World",
    "point_in_polygon", "segments_intersect", "point_segment_distance", "raycast",
    "body_twist_step", "unicycle_step", "skid_steer_twist", "track_speeds",
    "WheelOdometry", "Lidar", "Channel", "PID", "WaypointFollower",
    "RobotParams", "Simulator", "render",
]


# ----------------------------------------------------------------------------------------------
# Small helpers (implemented in the starter too)
# ----------------------------------------------------------------------------------------------
def wrap_angle(a):
    """Wrap angle(s) to [-pi, pi)."""
    return (np.asarray(a) + np.pi) % (2.0 * np.pi) - np.pi


def box(xmin: float, ymin: float, xmax: float, ymax: float) -> np.ndarray:
    """Axis-aligned rectangle as a (4, 2) counter-clockwise vertex array."""
    return np.array([[xmin, ymin], [xmax, ymin], [xmax, ymax], [xmin, ymax]], dtype=float)


def regular_polygon(cx: float, cy: float, radius: float, n: int = 8, phase: float = 0.0) -> np.ndarray:
    """Regular n-gon (counter-clockwise) inscribed in a circle of ``radius`` centred at (cx, cy)."""
    a = phase + 2.0 * np.pi * np.arange(n) / n
    return np.column_stack([cx + radius * np.cos(a), cy + radius * np.sin(a)])


def _cross2(a, b):
    return a[..., 0] * b[..., 1] - a[..., 1] * b[..., 0]


# ----------------------------------------------------------------------------------------------
# Geometry (learning goals)
# ----------------------------------------------------------------------------------------------
def point_in_polygon(p, poly) -> bool:
    """Even–odd (crossing-number) test. Points exactly on an edge may return either value.

    p: (2,) point; poly: (N, 2) vertices (either orientation, simple polygon).
    """
    x, y = float(p[0]), float(p[1])
    poly = np.asarray(poly, dtype=float)
    xi, yi = poly[:, 0], poly[:, 1]
    xj, yj = np.roll(xi, 1), np.roll(yi, 1)
    straddle = (yi > y) != (yj > y)
    with np.errstate(divide="ignore", invalid="ignore"):
        x_cross = xj + (y - yj) * (xi - xj) / (yi - yj)
    return bool(np.count_nonzero(straddle & (x < x_cross)) % 2)


def segments_intersect(a, b, c, d) -> bool:
    """True if closed segments ab and cd share at least one point (collinear overlap included)."""
    a, b, c, d = (np.asarray(v, dtype=float) for v in (a, b, c, d))

    def orient(p, q, r):
        v = (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
        return 0 if abs(v) < 1e-12 else (1 if v > 0 else -1)

    def on_seg(p, q, r):  # r collinear with pq: is it within the bounding box?
        return (min(p[0], q[0]) - 1e-12 <= r[0] <= max(p[0], q[0]) + 1e-12 and
                min(p[1], q[1]) - 1e-12 <= r[1] <= max(p[1], q[1]) + 1e-12)

    o1, o2, o3, o4 = orient(a, b, c), orient(a, b, d), orient(c, d, a), orient(c, d, b)
    if o1 != o2 and o3 != o4:
        return True
    return ((o1 == 0 and on_seg(a, b, c)) or (o2 == 0 and on_seg(a, b, d)) or
            (o3 == 0 and on_seg(c, d, a)) or (o4 == 0 and on_seg(c, d, b)))


def point_segment_distance(p, a, b) -> float:
    """Euclidean distance from point p to the closed segment ab."""
    p, a, b = (np.asarray(v, dtype=float) for v in (p, a, b))
    ab = b - a
    L2 = float(ab @ ab)
    t = 0.0 if L2 == 0.0 else float(np.clip((p - a) @ ab / L2, 0.0, 1.0))
    return float(np.linalg.norm(p - (a + t * ab)))


# ----------------------------------------------------------------------------------------------
# World
# ----------------------------------------------------------------------------------------------
@dataclass
class World:
    """Rectangular arena [0, width] x [0, height] with polygon obstacles.

    The arena boundary is a wall: rays hit it, and robots collide with it.
    """
    width: float
    height: float
    obstacles: list = field(default_factory=list)

    def __post_init__(self):
        self.obstacles = [np.asarray(o, dtype=float) for o in self.obstacles]

    def segments(self) -> np.ndarray:
        """All wall and obstacle edges as an (M, 4) array of [x1, y1, x2, y2]."""
        polys = [box(0.0, 0.0, self.width, self.height)] + list(self.obstacles)
        segs = [np.hstack([P, np.roll(P, -1, axis=0)]) for P in polys]
        return np.vstack(segs)

    def collides(self, p, radius: float = 0.0) -> bool:
        """True if a disc of ``radius`` centred at p overlaps a wall or obstacle."""
        x, y = float(p[0]), float(p[1])
        if x - radius < 0 or y - radius < 0 or x + radius > self.width or y + radius > self.height:
            return True
        for P in self.obstacles:
            if point_in_polygon((x, y), P):
                return True
            if radius > 0:
                Q = np.roll(P, -1, axis=0)
                if any(point_segment_distance((x, y), P[i], Q[i]) < radius for i in range(len(P))):
                    return True
        return False

    def segment_free(self, a, b) -> bool:
        """True if the segment ab stays inside the arena and touches no obstacle."""
        for q in (a, b):
            if not (0 <= q[0] <= self.width and 0 <= q[1] <= self.height):
                return False
        for P in self.obstacles:
            if point_in_polygon(a, P) or point_in_polygon(b, P):
                return False
            Q = np.roll(P, -1, axis=0)
            if any(segments_intersect(a, b, P[i], Q[i]) for i in range(len(P))):
                return False
        return True


def raycast(world: World, origin, angles, max_range: float) -> np.ndarray:
    """Distance along each ray (world-frame angle) to the first wall/obstacle hit, capped at max_range.

    Vectorised: every ray against every segment. Returns an array with the shape of ``angles``.
    Ray o + t d, segment p + s e:  t = (p - o) x e / (d x e),  s = (p - o) x d / (d x e),
    a hit needs t >= 0 and 0 <= s <= 1.
    """
    ang = np.atleast_1d(np.asarray(angles, dtype=float))
    o = np.asarray(origin, dtype=float)[:2]
    S = world.segments()
    p, e = S[:, :2], S[:, 2:] - S[:, :2]                           # (M, 2)
    d = np.column_stack([np.cos(ang), np.sin(ang)])                # (B, 2)
    denom = d[:, None, 0] * e[None, :, 1] - d[:, None, 1] * e[None, :, 0]   # (B, M)
    w = p - o                                                      # (M, 2)
    num_t = _cross2(w, e)[None, :]                                 # (1, M)
    num_s = w[None, :, 0] * d[:, None, 1] - w[None, :, 1] * d[:, None, 0]   # (B, M)
    with np.errstate(divide="ignore", invalid="ignore"):
        t = num_t / denom
        s = num_s / denom
    ok = (np.abs(denom) > 1e-12) & (t >= 0) & (s >= -1e-12) & (s <= 1 + 1e-12)
    t = np.where(ok, t, np.inf)
    r = np.minimum(t.min(axis=1), max_range)
    return r.reshape(np.shape(angles)) if np.ndim(angles) else r[0]


# ----------------------------------------------------------------------------------------------
# Kinematics
# ----------------------------------------------------------------------------------------------
def body_twist_step(pose, vx: float, vy: float, omega: float, dt: float) -> np.ndarray:
    """Integrate a constant body twist (vx, vy, omega) for dt **exactly** (SE(2) exponential).

    For omega != 0 the body-frame displacement is
    [[sin(wT)/w, -(1-cos(wT))/w], [(1-cos(wT))/w, sin(wT)/w]] @ [vx, vy];
    it is rotated into the world by the initial heading. Heading is wrapped.
    """
    x, y, th = (float(v) for v in pose)
    wt = omega * dt
    if abs(wt) < 1e-9:  # second-order series avoids cancellation near omega = 0
        a, b = dt * (1 - wt * wt / 6.0), dt * (wt / 2.0)
    else:
        a, b = math.sin(wt) / omega, (1.0 - math.cos(wt)) / omega
    dxb = a * vx - b * vy
    dyb = b * vx + a * vy
    c, s = math.cos(th), math.sin(th)
    return np.array([x + c * dxb - s * dyb, y + s * dxb + c * dyb, float(wrap_angle(th + wt))])


def unicycle_step(pose, v: float, omega: float, dt: float) -> np.ndarray:
    """Exact arc integration of the unicycle (forward speed v, yaw rate omega)."""
    return body_twist_step(pose, v, 0.0, omega, dt)


def skid_steer_twist(vL: float, vR: float, B: float, chi: float = 1.0, x_icr: float = 0.0):
    """Body twist (vx, vy, omega) of a skid-steer base from track speeds (symmetric ICR model).

    y_L = -y_R = chi*B/2 ; vx = (vL+vR)/2 ; omega = (vR-vL)/(chi*B) ; vy = -omega*x_icr.
    """
    omega = (vR - vL) / (chi * B)
    return 0.5 * (vL + vR), -omega * x_icr, omega


def track_speeds(v: float, omega: float, B: float, chi: float = 1.0):
    """Inverse of :func:`skid_steer_twist` (with x_icr = 0): (vL, vR) for a desired (v, omega)."""
    half = 0.5 * omega * chi * B
    return v - half, v + half


# ----------------------------------------------------------------------------------------------
# Sensors
# ----------------------------------------------------------------------------------------------
class WheelOdometry:
    """Dead-reckoning from measured track speeds.

    measured v_i = (1 + scale_bias_i) * v_i_true + N(0, sigma^2)   (i = L, R), per update.
    Integration uses the *model* effective-gauge factor ``chi_model`` (which may differ from the
    terrain's true chi) and the exact arc update.
    """

    def __init__(self, B: float, chi_model: float = 1.0, scale_bias=(0.0, 0.0), sigma: float = 0.0,
                 rng=None, pose0=(0.0, 0.0, 0.0)):
        self.B, self.chi_model = float(B), float(chi_model)
        self.scale_bias = np.asarray(scale_bias, dtype=float)
        self.sigma = float(sigma)
        self.rng = rng if rng is not None else np.random.default_rng(0)
        self.pose = np.asarray(pose0, dtype=float).copy()

    def measure(self, vL: float, vR: float):
        """Return the measured (vL, vR) track speeds."""
        v = (1.0 + self.scale_bias) * np.array([vL, vR], dtype=float)
        if self.sigma > 0:
            v = v + self.rng.normal(0.0, self.sigma, 2)
        return float(v[0]), float(v[1])

    def update(self, vL_true: float, vR_true: float, dt: float) -> np.ndarray:
        """Measure the true track speeds, integrate one step, return the odometry pose."""
        mL, mR = self.measure(vL_true, vR_true)
        vx, vy, w = skid_steer_twist(mL, mR, self.B, self.chi_model)
        self.pose = body_twist_step(self.pose, vx, vy, w, dt)
        return self.pose.copy()


class Lidar:
    """Planar scanning range finder.

    Beams at body-frame angles linspace(-fov/2, fov/2, n_beams) (fov = 2*pi: endpoint excluded).
    Each range = true range + N(0, sigma^2), clipped to [0, max_range]; with probability
    ``dropout`` a beam returns max_range (no return).
    """

    def __init__(self, n_beams: int = 181, fov: float = np.pi, max_range: float = 10.0,
                 sigma: float = 0.02, dropout: float = 0.0, rng=None):
        self.n_beams, self.fov, self.max_range = int(n_beams), float(fov), float(max_range)
        self.sigma, self.dropout = float(sigma), float(dropout)
        self.rng = rng if rng is not None else np.random.default_rng(0)

    def angles(self) -> np.ndarray:
        full = abs(self.fov - 2 * np.pi) < 1e-9
        return np.linspace(-self.fov / 2, self.fov / 2, self.n_beams, endpoint=not full)

    def scan(self, world: World, pose) -> np.ndarray:
        """Noisy ranges (n_beams,) from ``pose``."""
        r = raycast(world, pose[:2], pose[2] + self.angles(), self.max_range)
        if self.sigma > 0:
            r = r + self.rng.normal(0.0, self.sigma, r.shape)
        r = np.clip(r, 0.0, self.max_range)
        if self.dropout > 0:
            r = np.where(self.rng.random(r.shape) < self.dropout, self.max_range, r)
        return r


# ----------------------------------------------------------------------------------------------
# Communications
# ----------------------------------------------------------------------------------------------
class Channel:
    """One-way packet channel with latency, uniform jitter and Bernoulli loss.

    delay = max(0, latency + U[-jitter, +jitter]); each packet is lost with probability ``loss``.
    With ``fifo=True`` packets are never reordered (a packet is held until its predecessor is
    delivered), as on a TCP-like or serial link; otherwise reordering is possible (UDP-like).
    """

    def __init__(self, latency: float = 0.0, jitter: float = 0.0, loss: float = 0.0,
                 fifo: bool = False, rng=None):
        self.latency, self.jitter, self.loss, self.fifo = float(latency), float(jitter), float(loss), fifo
        self.rng = rng if rng is not None else np.random.default_rng(0)
        self._queue: list = []
        self._seq = 0
        self._last_delivery = -np.inf
        self.sent = 0
        self.dropped = 0
        self.delays: list = []   # realised delays of packets that will be delivered

    def send(self, t: float, payload) -> bool:
        """Offer a packet at time t. Returns False if it was lost."""
        self.sent += 1
        if self.loss > 0 and self.rng.random() < self.loss:
            self.dropped += 1
            return False
        d = self.latency + (self.rng.uniform(-self.jitter, self.jitter) if self.jitter > 0 else 0.0)
        t_del = t + max(0.0, d)
        if self.fifo:
            t_del = max(t_del, self._last_delivery)
            self._last_delivery = t_del
        self.delays.append(t_del - t)
        heapq.heappush(self._queue, (t_del, self._seq, t, payload))
        self._seq += 1
        return True

    def receive(self, t: float) -> list:
        """All packets with delivery time <= t, in delivery order, as (t_sent, payload) tuples."""
        out = []
        while self._queue and self._queue[0][0] <= t + 1e-12:
            _, _, ts, payload = heapq.heappop(self._queue)
            out.append((ts, payload))
        return out


# ----------------------------------------------------------------------------------------------
# Control
# ----------------------------------------------------------------------------------------------
class PID:
    """Discrete PID, u = kp e + ki * integral(e) + kd * de/dt, with output limits.

    - derivative on the measurement (no derivative kick on setpoint steps);
    - anti-windup by conditional integration: the integrator is frozen while the output is
      saturated and the error would drive it further into saturation;
    - ``angle=True`` wraps errors and measurement differences to [-pi, pi).
    """

    def __init__(self, kp: float, ki: float = 0.0, kd: float = 0.0, dt: float = 0.05,
                 u_min: float = -np.inf, u_max: float = np.inf, angle: bool = False,
                 anti_windup: bool = True):
        self.kp, self.ki, self.kd, self.dt = kp, ki, kd, dt
        self.u_min, self.u_max, self.angle, self.anti_windup = u_min, u_max, angle, anti_windup
        self.reset()

    def reset(self):
        self.integral = 0.0
        self._prev_meas = None

    def update(self, setpoint: float, measurement: float) -> float:
        e = setpoint - measurement
        if self.angle:
            e = float(wrap_angle(e))
        if self._prev_meas is None:
            dmeas = 0.0
        else:
            dm = measurement - self._prev_meas
            dmeas = (float(wrap_angle(dm)) if self.angle else dm) / self.dt
        self._prev_meas = measurement
        u_unsat = self.kp * e + self.ki * (self.integral + e * self.dt) - self.kd * dmeas
        u = min(max(u_unsat, self.u_min), self.u_max)
        saturated = u != u_unsat
        if not (self.anti_windup and saturated and np.sign(e) == np.sign(u_unsat)):
            self.integral += e * self.dt
        return u


class WaypointFollower:
    """Go-to-waypoint controller: heading PID for omega, distance-proportional speed.

    v = min(v_max, k_v * distance) * max(0, cos(heading_error)); a waypoint is reached within ``tol``.
    """

    def __init__(self, waypoints, heading_pid: PID, v_max: float = 0.5, k_v: float = 0.8,
                 tol: float = 0.15):
        self.waypoints = [np.asarray(w, dtype=float) for w in waypoints]
        self.pid, self.v_max, self.k_v, self.tol = heading_pid, v_max, k_v, tol
        self.index = 0

    @property
    def done(self) -> bool:
        return self.index >= len(self.waypoints)

    def command(self, pose):
        """Return (v, omega) for the current pose."""
        while not self.done and np.hypot(*(self.waypoints[self.index] - pose[:2])) < self.tol:
            self.index += 1
            self.pid.reset()
        if self.done:
            return 0.0, 0.0
        d = self.waypoints[self.index] - pose[:2]
        bearing = math.atan2(d[1], d[0])
        omega = self.pid.update(bearing, float(pose[2]))
        err = float(wrap_angle(bearing - pose[2]))
        v = min(self.v_max, self.k_v * float(np.hypot(*d))) * max(0.0, math.cos(err))
        return v, omega


# ----------------------------------------------------------------------------------------------
# Simulator
# ----------------------------------------------------------------------------------------------
@dataclass
class RobotParams:
    """Tracked-robot parameters (illustrative values for a mid-size EOD-class platform)."""
    B: float = 0.5              # track gauge, m
    chi_true: float = 1.6       # terrain effective-gauge factor (truth)
    chi_nominal: float = 1.6    # value the controller/odometry assume
    radius: float = 0.35        # collision radius, m
    v_track_max: float = 1.0    # track speed limit, m/s


class Simulator:
    """Fixed-step simulation of a skid-steer robot in a :class:`World`.

    ``step(v_cmd, omega_cmd)`` converts the command to track speeds with the nominal chi, saturates
    them, moves the robot with the true chi (exact arc), rejects moves that collide (the robot
    stays put and ``collisions`` increments), updates odometry, logs everything.
    """

    def __init__(self, world: World, params: RobotParams | None = None, pose0=(1.0, 1.0, 0.0),
                 dt: float = 0.05, odometry: WheelOdometry | None = None, lidar: Lidar | None = None):
        self.world = world
        self.params = params or RobotParams()
        self.pose = np.asarray(pose0, dtype=float).copy()
        self.dt, self.t = float(dt), 0.0
        self.odometry = odometry
        if self.odometry is not None:
            self.odometry.pose = self.pose.copy()
        self.lidar = lidar
        self.collisions = 0
        self.log = {"t": [0.0], "pose": [self.pose.copy()],
                    "odom": [self.pose.copy() if odometry is not None else np.full(3, np.nan)],
                    "cmd": [np.zeros(2)], "collided": [False]}

    def step(self, v_cmd: float, omega_cmd: float) -> np.ndarray:
        p = self.params
        vL, vR = track_speeds(v_cmd, omega_cmd, p.B, p.chi_nominal)
        vL = float(np.clip(vL, -p.v_track_max, p.v_track_max))
        vR = float(np.clip(vR, -p.v_track_max, p.v_track_max))
        vx, vy, w = skid_steer_twist(vL, vR, p.B, p.chi_true)
        new_pose = body_twist_step(self.pose, vx, vy, w, self.dt)
        collided = self.world.collides(new_pose[:2], p.radius)
        if collided:
            self.collisions += 1
            vL = vR = 0.0
        else:
            self.pose = new_pose
        odom = self.odometry.update(vL, vR, self.dt) if self.odometry is not None else np.full(3, np.nan)
        self.t += self.dt
        for k, v in (("t", self.t), ("pose", self.pose.copy()), ("odom", odom),
                     ("cmd", np.array([v_cmd, omega_cmd])), ("collided", collided)):
            self.log[k].append(v)
        return self.pose.copy()

    def scan(self) -> np.ndarray:
        if self.lidar is None:
            raise ValueError("no lidar attached")
        return self.lidar.scan(self.world, self.pose)

    def trajectory(self) -> dict:
        """Log as numpy arrays: t (T,), pose (T,3), odom (T,3), cmd (T,2), collided (T,)."""
        return {k: np.asarray(v) for k, v in self.log.items()}

    def run(self, controller, t_max: float) -> dict:
        """Step with ``controller.command(pose) -> (v, omega)`` until done or t_max."""
        while self.t < t_max - 1e-12 and not getattr(controller, "done", False):
            self.step(*controller.command(self.pose))
        return self.trajectory()


# ----------------------------------------------------------------------------------------------
# Rendering (implemented in the starter too)
# ----------------------------------------------------------------------------------------------
def render(world: World, ax=None, trajectories=None, pose=None, scan=None, lidar: Lidar | None = None,
           labels=None):
    """Draw the arena, obstacles, trajectories ((T, >=2) arrays), a robot pose and a lidar scan."""
    import matplotlib.pyplot as plt
    from matplotlib.patches import Polygon as MplPolygon

    if ax is None:
        _, ax = plt.subplots(figsize=(6, 6 * world.height / max(world.width, 1e-9)))
    ax.plot([0, world.width, world.width, 0, 0], [0, 0, world.height, world.height, 0], "k-", lw=1.5)
    for P in world.obstacles:
        ax.add_patch(MplPolygon(P, closed=True, fc="0.6", ec="0.2"))
    for i, tr in enumerate(trajectories or []):
        tr = np.asarray(tr)
        ax.plot(tr[:, 0], tr[:, 1], lw=1.5, label=(labels[i] if labels else None))
    if pose is not None:
        ax.plot(pose[0], pose[1], "o", color="C3")
        ax.arrow(pose[0], pose[1], 0.4 * math.cos(pose[2]), 0.4 * math.sin(pose[2]),
                 head_width=0.12, color="C3")
        if scan is not None and lidar is not None:
            a = pose[2] + lidar.angles()
            pts = np.column_stack([pose[0] + scan * np.cos(a), pose[1] + scan * np.sin(a)])
            ax.plot(pts[:, 0], pts[:, 1], ".", ms=2, color="C2")
    ax.set_aspect("equal")
    ax.set_xlabel("x [m]")
    ax.set_ylabel("y [m]")
    if labels:
        ax.legend()
    return ax


if __name__ == "__main__":  # demo: follow waypoints around an obstacle, plot truth vs odometry
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(1)
    world = World(12.0, 8.0, [box(4.0, 2.5, 6.0, 5.5), regular_polygon(9.0, 2.0, 0.8, 6)])
    odo = WheelOdometry(0.5, chi_model=1.5, scale_bias=(0.01, -0.01), sigma=0.01, rng=rng)
    sim = Simulator(world, RobotParams(), pose0=(1.0, 1.0, 0.0), odometry=odo,
                    lidar=Lidar(181, np.pi, 8.0, 0.02, rng=rng))
    ctl = WaypointFollower([(3, 1), (7, 1.2), (10.5, 4), (7, 6.8), (2, 6)],
                           PID(2.0, 0.1, 0.1, sim.dt, -1.5, 1.5, angle=True))
    tr = sim.run(ctl, 120.0)
    ax = render(world, trajectories=[tr["pose"], tr["odom"]], pose=sim.pose, scan=sim.scan(),
                lidar=sim.lidar, labels=["truth", "odometry"])
    ax.set_title(f"robotsim2d demo — {sim.t:.1f} s, collisions: {sim.collisions}")
    plt.show()
