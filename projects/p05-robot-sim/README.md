# P05 · 2D robot simulator (`robotsim2d`)

<div class="module-card">

**Lessons** [06.2 Spatial mathematics](lessons/stage-06/lesson-02.md) · [06.4 Mobile bases & control](lessons/stage-06/lesson-04.md) · [06.5 Teleoperation & HMI](lessons/stage-06/lesson-05.md) · [06.9 Communications & fail-safe](lessons/stage-06/lesson-09.md)

**Level** Intermediate · **Estimated time** 10–14 h

**Used by** [P04 Localisation](projects/p04-localization/README.md) · [P06 Path planning](projects/p06-path-planning/README.md) · [P07 SLAM](projects/p07-slam/README.md) · [P08 Manipulator](projects/p08-manipulator/README.md) · [P11 Teleoperation](projects/p11-teleoperation/README.md)

<p class="tags"><span>kinematics</span><span>ray casting</span><span>odometry</span><span>latency & loss</span><span>PID</span></p>
</div>

## Goal

Build the small, deterministic, dependency-light 2D simulator that later projects run on: a
tracked robot in a walled arena with polygon obstacles, driven through exact skid-steer
kinematics with ICR slip, sensing with a noisy lidar and biased wheel odometry, commanded over a
channel with latency, jitter and packet loss, and steered by a PID heading loop. Every piece is
validated against an analytic case, so later projects can trust it as ground truth.

The simulator is about **robot engineering only**: the arena contains generic obstacles and, in
later projects, fictional objects. Nothing in it models a device or any action on one.

## Background

- Frames, SE(2), and the exponential map that makes the arc update exact: [06.2](lessons/stage-06/lesson-02.md).
- Skid-steer kinematics and the ICR slip model $\omega = (v_R - v_L)/(\chi B)$, arc-exact
  odometry, PID with anti-windup: [06.4](lessons/stage-06/lesson-04.md) §2–§5.
- Delay, jitter and loss and why they destabilise a teleoperation loop: [06.5](lessons/stage-06/lesson-05.md).
- Link behaviour and loss-of-comms design: [06.9](lessons/stage-06/lesson-09.md).
- The browser counterpart is Sim G — [Robotics Engineering](sims/robotics-engineering/index.html)
  (obstacle course, comms, noisy sensors); Sim B — [EOD Robot](sims/eod-robot/index.html) runs the same
  kinematics and channel models in JavaScript.

## Requirements

1. **Geometry**: point-in-polygon (crossing number), closed-segment intersection (including
   collinear overlap), point–segment distance; `World.collides(p, radius)` for a disc robot and
   `World.segment_free(a, b)` for planners.
2. **Kinematics**: exact SE(2) integration of a constant body twist $(v_x, v_y, \omega)$;
   unicycle as the special case $v_y = 0$; skid-steer twist from track speeds with effective-gauge
   factor $\chi$ and longitudinal ICR offset; the inverse map (desired $(v,\omega)$ → track speeds).
3. **Lidar**: vectorised ray casting against all wall and obstacle edges; Gaussian range noise,
   clipping to $[0, r_{\max}]$, optional dropout.
4. **Wheel odometry**: per-track scale bias and white noise; integration with a *model* $\chi$
   that may differ from the terrain's.
5. **Channel**: delay $\max(0, \tau_0 + \mathcal U[-j, j])$, Bernoulli loss $p$, optional FIFO
   (no reordering); time-stamped packets.
6. **PID**: derivative on measurement, output limits, anti-windup by conditional integration,
   angle-wrapping mode.
7. **Simulator**: fixed step; commands → track speeds (nominal $\chi$) → saturation → truth
   motion (true $\chi$) → collision rejection → odometry → log; `render` with matplotlib.

## API

```python
wrap_angle(a) -> ndarray                                  # helper, provided
box(xmin, ymin, xmax, ymax) -> (4,2) ndarray              # helper, provided
regular_polygon(cx, cy, radius, n=8, phase=0.0)           # helper, provided
point_in_polygon(p, poly) -> bool
segments_intersect(a, b, c, d) -> bool
point_segment_distance(p, a, b) -> float
class World(width, height, obstacles=[]):                 # provided (uses the geometry above)
    segments() -> (M,4); collides(p, radius=0.0) -> bool; segment_free(a, b) -> bool
raycast(world, origin, angles, max_range) -> ndarray      # shape of `angles`
body_twist_step(pose, vx, vy, omega, dt) -> pose
unicycle_step(pose, v, omega, dt) -> pose                 # provided wrapper
skid_steer_twist(vL, vR, B, chi=1.0, x_icr=0.0) -> (vx, vy, omega)
track_speeds(v, omega, B, chi=1.0) -> (vL, vR)
class WheelOdometry(B, chi_model=1.0, scale_bias=(0,0), sigma=0.0, rng=None, pose0=(0,0,0)):
    measure(vL, vR) -> (vL_m, vR_m); update(vL_true, vR_true, dt) -> pose
class Lidar(n_beams=181, fov=pi, max_range=10.0, sigma=0.02, dropout=0.0, rng=None):
    angles() -> ndarray (provided); scan(world, pose) -> ndarray
class Channel(latency=0, jitter=0, loss=0, fifo=False, rng=None):
    send(t, payload) -> bool; receive(t) -> [(t_sent, payload), ...]; .delays; .dropped
class PID(kp, ki=0, kd=0, dt=0.05, u_min=-inf, u_max=inf, angle=False, anti_windup=True):
    update(setpoint, measurement) -> u; reset()
class WaypointFollower(waypoints, heading_pid, v_max=0.5, k_v=0.8, tol=0.15)   # provided
class RobotParams(B=0.5, chi_true=1.6, chi_nominal=1.6, radius=0.35, v_track_max=1.0)
class Simulator(world, params=None, pose0=(1,1,0), dt=0.05, odometry=None, lidar=None):  # provided
    step(v_cmd, omega_cmd) -> pose; scan(); run(controller, t_max) -> dict; trajectory() -> dict
render(world, ax=None, trajectories=None, pose=None, scan=None, lidar=None, labels=None)  # provided
```

The starter implements the helpers, `World`, `Simulator`, `WaypointFollower` and `render` (glue
and plotting are not the learning goal); the thirteen functions/methods that are the learning goal
raise `NotImplementedError`.

## Input / output

- **Input**: a `World` (arena size in metres, list of `(N,2)` vertex arrays), robot parameters,
  a controller or a command sequence $(v^\ast, \omega^\ast)$, noise/bias/channel parameters and a
  seeded `numpy.random.Generator`.
- **Output**: `Simulator.trajectory()` → `t (T,)`, `pose (T,3)`, `odom (T,3)`, `cmd (T,2)`,
  `collided (T,)`; lidar ranges `(n_beams,)`; channel delivery lists and realised delays; plots.

## Constraints

- NumPy (+ matplotlib for `render`) only; no external physics engine.
- Deterministic under a seed: every random draw uses a `Generator` passed in (default seed 0).
- Angles wrapped to $[-\pi, \pi)$; SI units throughout.
- The full test suite runs in well under 30 s; a 181-beam scan in a world with ~50 edges should
  take < 1 ms (vectorise over beams × segments).

## Expected behaviour

- The arc update is exact: a half circle integrated in 1 step or 400 steps lands on the same
  point to 1e-9 m. Euler integration would not.
- $(v_L, v_R) = (0.2, 0.6)$ m/s, $B = 0.5$ m: $\omega = 0.8$ rad/s without slip, $0.5$ rad/s with
  $\chi = 1.6$ (turn radius 0.8 m, not 0.5 m) — 06.4 §2.
- Odometry with the right $\chi$ and no noise reproduces the truth exactly; with $\chi_{\text{model}} = 1.3$
  on $\chi = 1.6$ terrain the heading error grows linearly with the turned angle.
- Delay samples are uniform on $[\tau_0 - j, \tau_0 + j]$: mean $\tau_0$, standard deviation
  $j/\sqrt3$; the delivered fraction is $1-p$; without FIFO, jitter larger than the send
  interval reorders packets.
- A PD heading loop on the integrating yaw plant converges with zero steady-state error; a PI
  speed loop with anti-windup overshoots far less after saturation than without.

## Test cases (`tests/test_robotsim2d.py`)

| Test | What it checks |
|---|---|
| `test_straight_line_exact`, `test_circle_exact_any_step_size`, `test_body_twist_lateral_velocity` | SE(2) integration against closed-form straight/circle/lateral motion |
| `test_skid_steer_lesson_numbers` | 06.4 §2 numbers; inverse map; ICR offset gives lateral velocity |
| `test_point_in_polygon_and_segments`, `test_world_collision` | geometry predicates, disc collision against walls/boxes |
| `test_raycast_empty_room_analytic`, `test_raycast_polygon_obstacle` | 721 rays vs the analytic room distance; box faces, corners, a 64-gon |
| `test_lidar_noise_statistics` | per-beam mean and standard deviation over 4000 scans; clipping |
| `test_odometry_*` | exactness with matched $\chi$; drift sign under scale bias; $\chi$ mismatch |
| `test_channel_delay_distribution_and_loss`, `test_channel_timing_and_fifo` | delay mean/std/bounds, loss rate, exact timing, FIFO order vs reordering |
| `test_pid_heading_converges`, `test_pi_speed_loop_zero_steady_state_and_antiwindup` | convergence, angle wrapping, zero steady-state error, windup overshoot |
| `test_simulator_waypoints_logging_and_collision`, `test_render_smoke` | end-to-end run, log shapes, collision rejection, plotting |

## Milestones

1. Geometry predicates → `World` works (tests `point_in_polygon…`, `world_collision`).
2. `body_twist_step`, `skid_steer_twist`, `track_speeds` → kinematics tests.
3. `raycast` (first a loop, then vectorise) → `Lidar.scan`.
4. `WheelOdometry` → odometry tests; run the `__main__` demo and compare truth and odometry.
5. `Channel` → delay statistics; `PID` → control tests and the end-to-end simulator test.

## Extension challenges

- Add a DC-motor + battery model per track (06.4 §5–§6) and log current and state of charge.
- Terrain patches with different $\chi$; estimate $\chi$ online by recursive least squares from a
  simulated IMU yaw rate.
- A Gilbert–Elliott (bursty) loss model and a link-quality map from a path-loss model (06.9);
  implement a loss-of-comms behaviour (stop, then retrace the logged path).
- Replace the brute-force ray cast with a uniform-grid or BVH acceleration structure; measure
  the speed-up for 10⁴ edges.
- Render an animation (`matplotlib.animation.FuncAnimation`) with the lidar scan and odometry ghost.

## Using `robotsim2d` from other projects

Module names are unique across the repository, so another project can import this one by
inserting its directory into `sys.path`:

```python
import pathlib, sys
P05 = pathlib.Path(__file__).resolve().parents[2] / "p05-robot-sim"   # from projects/pNN/<dir>/file.py
sys.path.insert(0, str(P05 / "solution"))   # or "starter" once your own P05 passes its tests
import robotsim2d
```

**Choice made in this course:** P04 (`localization`) and P06 (`planning`) are *self-contained*:
each carries a small, already-implemented copy of the helpers it needs (angle wrapping, the
unicycle motion used for data generation, segment/polygon collision checks), so their starters work
whether or not you have finished P05. Their test suites add `projects/p05-robot-sim/solution` to
`sys.path` for one optional cross-check against `robotsim2d` (skipped if P05 is absent). Later
projects (P07, P11) import `robotsim2d` directly.

## Hints

<details><summary>Hint 1 — exact arc update</summary>

For constant $(v_x, v_y, \omega)$ over $T$ the body displacement is
$\begin{bmatrix}\sin\omega T/\omega & -(1-\cos\omega T)/\omega\\ (1-\cos\omega T)/\omega & \sin\omega T/\omega\end{bmatrix}\begin{bmatrix}v_x\\v_y\end{bmatrix}$,
rotated by the *initial* heading. Near $\omega = 0$ use the series $\sin x/x \approx 1 - x^2/6$,
$(1-\cos x)/x \approx x/2$ to avoid cancellation.

</details>

<details><summary>Hint 2 — vectorised ray casting</summary>

With ray $o + t d$ and segment $p + s e$, $t = \frac{(p-o)\times e}{d\times e}$ and
$s = \frac{(p-o)\times d}{d\times e}$ (2D cross product). Build `denom` as a (beams × segments)
array, mask invalid hits with `np.inf`, and take the row minimum. Parallel rays have
`denom == 0`: mask them before dividing (or under `np.errstate`).

</details>

<details><summary>Hint 3 — anti-windup</summary>

Compute the unsaturated output with the *tentative* integral, clamp it, and only commit the
integral update if the output is not saturated or the error would pull it out of saturation.
Differentiating the measurement instead of the error removes the derivative kick at setpoint steps.

</details>

<details><summary>Hint 4 — FIFO channel</summary>

Keep a heap keyed by delivery time. For FIFO, a packet's delivery time is
`max(own_time, previous_delivery_time)` — it waits behind its predecessor (head-of-line blocking),
which is why TCP-like links show latency spikes under jitter.

</details>

## How to run

```bash
python -m pytest projects/p05-robot-sim                      # your starter
EOD_SOLUTION=1 python -m pytest projects/p05-robot-sim       # reference solution (bash)
python projects/p05-robot-sim/solution/robotsim2d.py         # demo plot
```

On Windows `cmd`: `set EOD_SOLUTION=1 && py -m pytest projects/p05-robot-sim`.
