# P08 · Manipulator kinematics: Arm-5 library

**Level:** Advanced · **Estimated time:** 10–14 h · **Module:** `manipulator`

## Goal

Write a kinematics and statics library for **Arm-5**, the fictional 5-DOF arm on a turret that
recurs throughout stage 06. Use it to answer the questions an operator and a designer actually
ask:

- Can the tool reach this point, with which joint angles, and does the solver fail gracefully when
  it cannot?
- How close is the arm to a singularity?
- How much can it hold at this reach?
- Where must the camera pan-tilt unit point to see a marked item?

The library covers SO(3)/SE(3) utilities, DH and product-of-exponentials forward kinematics, the
geometric Jacobian, damped-least-squares IK with joint limits, Yoshikawa manipulability with a
reachability/singularity map, statics ($\tau = J^\top F$) with a payload-vs-reach curve, and a
pan-tilt look-at solver.

## Arm-5 definition (fictional)

| Joint | Motion | Limits | Screw axis at home $(\hat\omega, v)$ |
|---|---|---|---|
| 1 turret yaw | about $z_0$ | ±170° | $(0,0,1,\ 0,0,0)$ |
| 2 shoulder pitch | positive raises | −40° … 130° | $(0,-1,0,\ 0.35,0,0)$ |
| 3 elbow pitch | positive raises | ±160° | $(0,-1,0,\ 0.35,0,-0.80)$ |
| 4 wrist pitch | positive raises | ±120° | $(0,-1,0,\ 0.35,0,-1.50)$ |
| 5 wrist roll | about the approach axis | ±180° | $(1,0,0,\ 0,0.35,0)$ |

Dimensions: $d_1 = 0.35$ m (turret to shoulder), $a_2 = 0.80$ m (upper arm), $a_3 = 0.70$ m
(forearm), $d_5 = 0.25$ m (wrist to tool point). At $q = 0$ the arm is stretched horizontally
forward, with the tool point at $(1.75, 0, 0.35)$ m and the approach vector along $+x_0$.

Standard DH rows $(\theta_i, d_i, a_i, \alpha_i)$: $(q_1, 0.35, 0, 90°)$, $(q_2, 0, 0.80, 0)$,
$(q_3, 0, 0.70, 0)$, $(q_4 + 90°, 0, 0, 90°)$, $(q_5, 0.25, 0, 0)$.

Masses: upper arm 4 kg, forearm 3 kg, wrist + gripper 2 kg, each with its CoM at the link
mid-point. Holding-torque limits: 150, 200, 100, 40, 20 N m.

## Background

- [06.2 Spatial mathematics](lessons/stage-06/lesson-02.md): rotations, Rodrigues, exp/log maps
  (§2), SE(3) (§5), twists and screws (§6), pan-tilt kinematics (§8).
- [06.3 Manipulators](lessons/stage-06/lesson-03.md): DH and PoE (§1–2), analytic IK (§4), the
  Jacobian (§5), numerical IK (§6), manipulability (§7), statics and payload vs reach (§8). Its
  numbers are this project's test cases.
- Related: [P05 robot simulator](projects/p05-robot-sim/README.md),
  [P11 teleoperation](projects/p11-teleoperation/README.md). Simulator
  [Sim B](sims/eod-robot/index.html) and [Sim G](sims/robotics-engineering/index.html) let you
  feel reach and payload limits interactively.

## Requirements

- `exp_so3` (Rodrigues) and `log_so3` must be accurate for angles near 0 and near π.
- `exp_se3` and `log_se3` must be closed form. Do not call `scipy.linalg.expm` in the library;
  tests use it only as a reference.
- `fk_poe` must equal `fk_dh` to machine precision.
- `ik_dls` handles both a position task (3D) and a pose task (6D, only for poses the 5-DOF arm can
  reach). It respects joint limits, uses a step trust region, restarts deterministically, and
  returns `success=False` with the best-effort configuration for unreachable targets.
- `gravity_torque` must use CoM point Jacobians. It must not use hand-coded lever arms.

## API

```python
# given
hat(w); vee(W); se3_hat(xi); make_T(R, p); inv_T(T); rot_x/rot_y/rot_z(t); rodrigues(axis, angle)
D1, A2, A3, D5, DH_TABLE, S_LIST, M_HOME, JOINT_LIMITS, LINK_MASSES, TORQUE_LIMITS, G
fk_dh_frames(q) -> [T_00 .. T_05];  link_coms(q) -> [(com, n_active)];  condition_number(J)
reachability_map(n_samples=25, cell=0.1, extent=2.0) -> {"x_edges","z_edges","reachable","w_max"}
plot_reachability(path, n_samples=22)
@dataclass IKResult(q, success, iterations, error)

# yours
exp_so3(w) -> R;  log_so3(R) -> w;  exp_se3(xi) -> T;  log_se3(T) -> xi;  adjoint(T) -> 6x6
dh_transform(theta, d, a, alpha) -> 4x4;  fk_dh(q) -> 4x4;  fk_poe(q) -> 4x4
jacobian_space(q) -> 6x5;  point_jacobian(q, point=None, n_active=None) -> 3x5
ik_dls(target, q0=None, task="position"|"pose", lam=0.05, tol=1e-6, max_iter=300,
       limits=JOINT_LIMITS, restarts=5, seed=0, max_step=0.3) -> IKResult
ik_analytic(p, pitch, roll, elbow_up=True) -> q | None
manipulability(J) -> float
joint_torques(q, F) -> tau;  gravity_torque(q, payload=0.0, masses=LINK_MASSES) -> tau
payload_vs_reach(reaches, torque_limits=TORQUE_LIMITS, masses=LINK_MASSES) -> (payload_kg, limiting_joint_idx)
look_at_pan_tilt(T_wb, T_bp, o_t, P_w) -> (pan, tilt, range)
```

## Input / Output

Angles are in radians, lengths in metres, forces in N and torques in N m. Twists are ordered
$(\omega, v)$. Poses are 4×4 homogeneous matrices in the arm base frame. The world frame appears
only in the pan-tilt solver.

## Constraints

NumPy (SciPy only in tests), matplotlib for plots. Tests run in about 5 s (limit 30 s).
Deterministic: all randomness comes through `seed`.

## Expected behaviour

- `exp_so3` equals `expm(hat(w))` to 1e-12. `log_so3(exp_so3(w))` returns `w` for |w| < π and a
  valid equivalent at π.
- The §4 target $(1.1, 0.3, 0)$ with approach pitch −60° gives
  $q = (15.26°, 35.50°, −94.18°, −1.32°, 0)$. DLS from $(0, 20°, −60°, 0, 10°)$ finds the same
  pose.
- Point manipulability is 0 whenever the elbow and the wrist pitch are both straight: the three
  pitch axes and the tool point are then collinear.
- A 3 kg payload at the §4 pose needs $\tau = (0, 33.56, 14.39, 3.68, 0)$ N m. The payload curve
  is 15.3 kg (wrist-limited) out to about 1.0 m, then falls to 12.4 kg at 1.2 m and 6.9 kg at
  1.75 m (shoulder-limited).
- Pan-tilt, lesson 06.2 §8: pan 19.98°, tilt −18.87°, range 2.474 m.
- `python projects/p08-manipulator/solution/manipulator.py` writes
  `p08_out/reachability.png` and `p08_out/payload_vs_reach.png`. The map shows the dark
  low-manipulability band above the turret axis (the wrist-centre-on-axis singularity) and the
  reach boundary.

## Test cases (`tests/test_manipulator.py`)

| Test | What it checks |
|---|---|
| `test_rodrigues_matches_matrix_exponential` | Rodrigues vs `expm` |
| `test_so3_exp_log_round_trip` | round trip at 1e-10 … π, including the near-π regime |
| `test_se3_exp_log_round_trip_and_expm`, `test_adjoint_transforms_twists` | closed-form SE(3), adjoint identity $[\mathrm{Ad}_T V] = T[V]T^{-1}$ |
| `test_home_pose`, `test_poe_equals_dh`, `test_lesson_pose` | FK consistency on 100 random configurations |
| `test_point_jacobian_vs_finite_differences`, `test_space_jacobian_vs_finite_differences` | analytic vs numerical Jacobians |
| `test_ik_position_converges_for_reachable_targets` | 15 random reachable targets, within joint limits |
| `test_ik_pose_task_lesson_case` | 6D pose IK on the lesson pose |
| `test_ik_reports_failure_for_unreachable_target` | `success=False`, arm stretched toward the target |
| `test_analytic_ik_lesson_numbers` | §4 table, `None` when out of reach |
| `test_manipulability_zero_at_singularity` | w = 0 at straight elbow and wrist; 2R formula |
| `test_reachability_map_sane` | reachable inside, unreachable outside |
| `test_payload_torques_lesson_numbers`, `test_torque_power_balance`, `test_payload_vs_reach_lesson_table` | statics |
| `test_pan_tilt_lesson_numbers` | look-at solver and zenith convention |

## Milestones

1. SO(3)/SE(3): `exp_so3`, `log_so3`, `exp_se3`, `log_se3`, `adjoint`.
2. FK: `dh_transform`, `fk_dh`, `fk_poe`, and check that they agree.
3. Jacobians: `jacobian_space`, `point_jacobian`, and check them by finite differences.
4. IK: `ik_analytic`, then `ik_dls` (position task first, then pose, then limits and restarts).
5. `manipulability`, then run `plot_reachability`.
6. Statics: `joint_torques`, `gravity_torque`, `payload_vs_reach`.
7. `look_at_pan_tilt`.

## Extension challenges

- Return *all* analytic IK branches (elbow up/down × turret front/back) in a deterministic order.
- Add null-space joint-limit avoidance to DLS for the position task (the arm is redundant by 2).
- Selectively damped least squares (Buss & Kim) and a comparison of joint-velocity peaks along a
  path that passes near the stretched-arm singularity.
- Force ellipsoids: verify the duality with velocity ellipsoids.
- Tilted base: rotate gravity by an IMU attitude and recompute payload vs reach on a 15° slope
  (06.3 Exercise 6).
- Kinematic calibration: identify DH offsets from simulated noisy tool measurements, and check
  identifiability with the SVD of the regressor.

## Hints

<details><summary>log near π</summary>

`arccos((tr R − 1)/2)` has an infinite derivative at −1, so it returns θ with an error of about
$\sqrt{\epsilon}\approx 10^{-8}$. Use `atan2(|vee(R − Rᵀ)|/2, (tr R − 1)/2)`. For the axis near π,
take the largest-diagonal column of $(R + R^\top)/2 - \cos\theta\, I = (1-\cos\theta)\,\hat a\hat
a^\top$, and fix its sign with $\mathrm{vee}(R - R^\top)$.

</details>

<details><summary>Point Jacobian</summary>

A point $p$ fixed to the moving body has velocity $v_s + \omega_s\times p$, so
$J_p = J_{s,v} - [p]\,J_{s,\omega}$. For a link CoM, zero the columns of the joints distal to that
link.

</details>

<details><summary>DLS stability</summary>

Far targets produce huge error vectors, and an undamped or unscaled step flings the arm into its
limits, where it stays. Scale each step so that max |Δq| ≤ 0.3 rad. Clip to limits after each
step. The stretched home pose is singular for the position task. That is why restarts help.

</details>

<details><summary>Payload vs reach</summary>

Compute gravity torque at payload 0 and at 1 kg. The difference is the torque per kg (linear in
the payload). The maximum is $\min_j (\tau_{j,\max} - |\tau_{j,\text{self}}|)/|\tau_{j,\text{kg}}|$
over joints that feel the load.

</details>

## How to run

```bash
python -m pytest projects/p08-manipulator                  # starter: fails with NotImplementedError
EOD_SOLUTION=1 python -m pytest projects/p08-manipulator   # reference (bash)
set EOD_SOLUTION=1 && python -m pytest projects/p08-manipulator   # Windows cmd
python projects/p08-manipulator/solution/manipulator.py    # figures in ./p08_out
```
