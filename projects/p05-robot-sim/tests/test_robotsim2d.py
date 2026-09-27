"""Tests for P05 robotsim2d. Run: python -m pytest projects/p05-robot-sim  (EOD_SOLUTION=1 for the reference)."""
import os, sys, pathlib
_ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_ROOT / ("solution" if os.environ.get("EOD_SOLUTION") else "starter")))
import robotsim2d as mod  # noqa: E402

import math  # noqa: E402

import numpy as np  # noqa: E402
import pytest  # noqa: E402


# ---------------------------------------------------------------- kinematics
def test_straight_line_exact():
    p = np.array([1.0, 2.0, np.radians(30)])
    for _ in range(100):
        p = mod.unicycle_step(p, 0.5, 0.0, 0.1)
    expect = [1.0 + 5.0 * math.cos(np.radians(30)), 2.0 + 5.0 * math.sin(np.radians(30)), np.radians(30)]
    assert np.allclose(p, expect, atol=1e-12)


def test_circle_exact_any_step_size():
    v, w = 1.0, 0.5                     # radius 2 m, period 4*pi s
    R, T = v / w, 2 * np.pi / w
    for n in (1, 3, 7, 400):            # exact arc: step size must not matter
        p = np.zeros(3)
        for _ in range(n):
            p = mod.unicycle_step(p, v, w, (T / 2) / n)
        assert np.allclose(p[:2], [0.0, 2 * R], atol=1e-9)
        assert abs(abs(p[2]) - np.pi) < 1e-9
    p = np.zeros(3)
    for _ in range(40):
        p = mod.unicycle_step(p, v, w, T / 40)
    assert np.allclose(p, [0, 0, 0], atol=1e-9)


def test_body_twist_lateral_velocity():
    # pure lateral motion then pure rotation: compare with composing SE(2) transforms
    p = mod.body_twist_step(np.array([0.0, 0.0, np.pi / 2]), 0.0, 1.0, 0.0, 2.0)
    assert np.allclose(p, [-2.0, 0.0, np.pi / 2], atol=1e-12)
    p = mod.body_twist_step(np.zeros(3), 0.0, 0.0, 1.0, 0.5)
    assert np.allclose(p, [0.0, 0.0, 0.5], atol=1e-12)


def test_skid_steer_lesson_numbers():
    vx, vy, w = mod.skid_steer_twist(0.2, 0.6, 0.5, 1.0)
    assert np.allclose([vx, vy, w], [0.4, 0.0, 0.8])
    vx, vy, w = mod.skid_steer_twist(0.2, 0.6, 0.5, 1.6)
    assert np.allclose([vx, vy, w], [0.4, 0.0, 0.5])           # radius 0.8 m, lesson 06.4 §2
    vL, vR = mod.track_speeds(vx, w, 0.5, 1.6)
    assert np.allclose([vL, vR], [0.2, 0.6])
    _, vy, _ = mod.skid_steer_twist(0.2, 0.6, 0.5, 1.6, x_icr=0.1)
    assert np.isclose(vy, -0.05)


# ---------------------------------------------------------------- geometry & ray casting
def test_point_in_polygon_and_segments():
    sq = mod.box(0, 0, 2, 2)
    assert mod.point_in_polygon((1, 1), sq) and not mod.point_in_polygon((3, 1), sq)
    tri = np.array([[0, 0], [4, 0], [0, 4]])
    assert mod.point_in_polygon((1, 1), tri) and not mod.point_in_polygon((3, 3), tri)
    assert mod.segments_intersect((0, 0), (2, 2), (0, 2), (2, 0))
    assert not mod.segments_intersect((0, 0), (1, 0), (0, 1), (1, 1))
    assert mod.segments_intersect((0, 0), (2, 0), (1, 0), (3, 0))          # collinear overlap
    assert np.isclose(mod.point_segment_distance((1, 1), (0, 0), (2, 0)), 1.0)
    assert np.isclose(mod.point_segment_distance((3, 1), (0, 0), (2, 0)), math.sqrt(2))


def test_raycast_empty_room_analytic():
    world = mod.World(10.0, 6.0)
    o = np.array([3.0, 2.0])
    ang = np.linspace(-np.pi, np.pi, 721, endpoint=False)
    r = mod.raycast(world, o, ang, 100.0)
    c, s = np.cos(ang), np.sin(ang)
    with np.errstate(divide="ignore"):
        tx = np.where(c > 1e-12, (10 - o[0]) / c, np.where(c < -1e-12, -o[0] / c, np.inf))
        ty = np.where(s > 1e-12, (6 - o[1]) / s, np.where(s < -1e-12, -o[1] / s, np.inf))
    assert np.allclose(r, np.minimum(tx, ty), atol=1e-9)
    assert np.isclose(mod.raycast(world, o, 0.0, 100.0), 7.0)
    assert np.isclose(mod.raycast(world, o, 0.0, 5.0), 5.0)                # capped at max range


def test_raycast_polygon_obstacle():
    world = mod.World(20.0, 20.0, [mod.box(8, 8, 12, 12), mod.regular_polygon(15, 3, 1.0, 64)])
    assert np.isclose(mod.raycast(world, (2, 10), 0.0, 50), 6.0)
    assert np.isclose(mod.raycast(world, (10, 2), np.pi / 2, 50), 6.0)
    assert np.isclose(mod.raycast(world, (2, 2), np.pi / 4, 50), math.hypot(6, 6))   # hits corner
    r = mod.raycast(world, (10, 3), 0.0, 50)                                  # 64-gon ~ circle r=1
    assert 3.99 < r < 4.001


def test_lidar_noise_statistics():
    world = mod.World(10.0, 10.0)
    lid = mod.Lidar(n_beams=4, fov=2 * np.pi, max_range=20.0, sigma=0.05, rng=np.random.default_rng(3))
    assert np.allclose(lid.angles(), [-np.pi, -np.pi / 2, 0, np.pi / 2])
    scans = np.array([lid.scan(world, np.array([5.0, 5.0, 0.0])) for _ in range(4000)])
    assert np.allclose(scans.mean(axis=0), 5.0, atol=0.005)
    assert np.allclose(scans.std(axis=0), 0.05, rtol=0.06)
    lid2 = mod.Lidar(n_beams=10, fov=np.pi, max_range=3.0, sigma=0.0, rng=np.random.default_rng(0))
    assert np.all(lid2.scan(world, np.array([5.0, 5.0, 0.0])) <= 3.0)


def test_world_collision():
    world = mod.World(10.0, 10.0, [mod.box(4, 4, 6, 6)])
    assert world.collides((5, 5))
    assert not world.collides((2, 2), 0.5)
    assert world.collides((3.7, 5), 0.35)          # disc touches the box
    assert world.collides((0.2, 5), 0.35)          # disc touches the wall
    assert world.segment_free((1, 1), (9, 1)) and not world.segment_free((1, 5), (9, 5))


# ---------------------------------------------------------------- odometry
def test_odometry_noise_free_matches_truth_and_chi_mismatch():
    B = 0.5
    odo = mod.WheelOdometry(B, chi_model=1.6)
    truth = np.zeros(3)
    for _ in range(200):
        odo.update(0.2, 0.6, 0.05)
        truth = mod.body_twist_step(truth, *mod.skid_steer_twist(0.2, 0.6, B, 1.6), 0.05)
    assert np.allclose(odo.pose, truth, atol=1e-12)
    odo_wrong = mod.WheelOdometry(B, chi_model=1.3)            # lesson 06.4: wrong chi -> heading error
    for _ in range(200):
        odo_wrong.update(0.2, 0.6, 0.05)
    assert abs(float(mod.wrap_angle(odo_wrong.pose[2] - truth[2]))) > 0.5


def test_odometry_bias_drift():
    odo = mod.WheelOdometry(0.5, 1.0, scale_bias=(0.02, 0.0), sigma=0.0)
    for _ in range(1000):
        odo.update(0.5, 0.5, 0.05)
    # left track reads fast -> odometry believes the robot turned right
    assert odo.pose[2] < -0.05
    assert odo.pose[1] < -0.1


# ---------------------------------------------------------------- channel
def test_channel_delay_distribution_and_loss():
    ch = mod.Channel(latency=0.2, jitter=0.05, loss=0.1, rng=np.random.default_rng(7))
    n = 20000
    for k in range(n):
        ch.send(k * 0.01, k)
    d = np.array(ch.delays)
    assert abs(len(d) / n - 0.9) < 0.01
    assert d.min() >= 0.15 - 1e-12 and d.max() <= 0.25 + 1e-12
    assert abs(d.mean() - 0.2) < 0.002
    assert abs(d.std() - 0.05 / math.sqrt(3)) < 0.002          # uniform on [-j, j]
    got = ch.receive(1e9)
    assert len(got) == len(d)
    assert ch.dropped == n - len(d)


def test_channel_timing_and_fifo():
    ch = mod.Channel(latency=0.5, rng=np.random.default_rng(0))
    ch.send(0.0, "a")
    assert ch.receive(0.49) == []
    assert ch.receive(0.5) == [(0.0, "a")]
    fifo = mod.Channel(latency=0.3, jitter=0.25, fifo=True, rng=np.random.default_rng(1))
    for k in range(500):
        fifo.send(k * 0.01, k)
    order = [p for _, p in fifo.receive(1e9)]
    assert order == sorted(order)
    raw = mod.Channel(latency=0.3, jitter=0.25, fifo=False, rng=np.random.default_rng(1))
    for k in range(500):
        raw.send(k * 0.01, k)
    order = [p for _, p in raw.receive(1e9)]
    assert order != sorted(order)                                 # jitter > spacing -> reordering


# ---------------------------------------------------------------- control
def test_pid_heading_converges():
    dt = 0.02
    # yaw is an integrating plant: PD gives zero steady-state error (an I term adds a slow mode)
    pid = mod.PID(3.0, 0.0, 0.05, dt, -1.0, 1.0, angle=True)
    pose = np.array([0.0, 0.0, 0.0])
    target = 2.5
    for _ in range(int(6.0 / dt)):
        w = pid.update(target, pose[2])
        pose = mod.unicycle_step(pose, 0.0, w, dt)
    assert abs(float(mod.wrap_angle(target - pose[2]))) < 1e-3
    pid2 = mod.PID(3.0, 0.0, 0.0, dt, angle=True)                   # wrap: -3 rad is 3.28 rad "away"
    th = 3.0
    for _ in range(300):
        th = float(mod.wrap_angle(th + pid2.update(-3.0, th) * dt))
    assert abs(float(mod.wrap_angle(th + 3.0))) < 1e-3


def _speed_loop(anti_windup):
    dt, tau = 0.01, 0.3
    pid = mod.PID(2.0, 8.0, 0.0, dt, -1.0, 1.0, anti_windup=anti_windup)
    v, out = 0.0, []
    for k in range(int(8.0 / dt)):
        sp = 0.9 if k * dt < 4.0 else 0.5
        u = pid.update(sp, v)
        v += dt * (u - v) / tau               # first-order drive, saturated input
        out.append(v)
    return np.array(out)


def test_pi_speed_loop_zero_steady_state_and_antiwindup():
    v = _speed_loop(True)
    assert abs(v[399] - 0.9) < 1e-3 and abs(v[-1] - 0.5) < 1e-3
    # a setpoint the plant can only just reach saturates the actuator; windup causes overshoot
    dt, tau = 0.01, 0.3
    res = {}
    for aw in (True, False):
        pid = mod.PID(1.0, 6.0, 0.0, dt, -1.0, 1.0, anti_windup=aw)
        v, peak = 0.0, 0.0
        for _ in range(1500):
            v += dt * (pid.update(0.95, v) - v) / tau
            peak = max(peak, v)
        res[aw] = peak
    assert res[True] < 0.97 and res[False] > 0.99


# ---------------------------------------------------------------- simulator
def test_simulator_waypoints_logging_and_collision():
    world = mod.World(12.0, 8.0, [mod.box(4.0, 2.5, 6.0, 5.5)])
    sim = mod.Simulator(world, mod.RobotParams(), pose0=(1.0, 1.0, 0.0), dt=0.05,
                        odometry=mod.WheelOdometry(0.5, chi_model=1.6))
    ctl = mod.WaypointFollower([(3, 1), (7, 1.2), (8, 6)], mod.PID(2.0, 0.0, 0.1, 0.05, -1.5, 1.5, angle=True))
    tr = sim.run(ctl, 80.0)
    assert ctl.done and sim.collisions == 0
    assert np.hypot(*(tr["pose"][-1, :2] - [8, 6])) < 0.15
    assert tr["pose"].shape == (len(tr["t"]), 3) and tr["odom"].shape == tr["pose"].shape
    assert np.allclose(tr["odom"], tr["pose"], atol=1e-9)          # perfect odometry, chi matched
    # drive straight into the box: robot must stop outside it
    sim2 = mod.Simulator(world, mod.RobotParams(), pose0=(1.0, 4.0, 0.0), dt=0.05)
    for _ in range(200):
        sim2.step(0.5, 0.0)
    assert sim2.collisions > 0
    assert sim2.pose[0] <= 4.0 - 0.35 + 1e-9 and sim2.pose[0] > 3.0


def test_render_smoke(tmp_path):
    import matplotlib
    matplotlib.use("Agg")
    world = mod.World(5.0, 5.0, [mod.box(1, 1, 2, 2)])
    lid = mod.Lidar(n_beams=31, fov=np.pi, max_range=4.0, sigma=0.0)
    pose = np.array([3.0, 3.0, 0.5])
    ax = mod.render(world, trajectories=[np.array([[0.5, 0.5], [3, 3]])], pose=pose,
                    scan=lid.scan(world, pose), lidar=lid, labels=["demo"])
    ax.figure.savefig(tmp_path / "r.png")
    assert (tmp_path / "r.png").exists()
