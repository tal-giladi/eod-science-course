# P04 · Robot localisation: EKF and particle filter (`localization`)

<div class="module-card">

**Lessons** [06.6 State estimation](lessons/stage-06/lesson-06.md) (core) · [06.4 Mobile bases & control](lessons/stage-06/lesson-04.md) (odometry, slip) · [05.6 Sensor fusion](lessons/stage-05/lesson-06.md) (Bayesian fusion)

**Level** Advanced · **Estimated time** 10–12 h

**Builds on** [P05 Robot simulator](projects/p05-robot-sim/README.md) (optional cross-check) · **Feeds** [P07 SLAM](projects/p07-slam/README.md)

<p class="tags"><span>EKF</span><span>particle filter</span><span>Jacobians</span><span>NEES / NIS</span><span>Monte Carlo</span></p>
</div>

## Goal

Implement landmark-based localisation for a tracked robot two ways — an extended Kalman filter
and a bootstrap particle filter — and prove *statistically* that the EKF is honest about its own
uncertainty (NEES/NIS over seeded Monte Carlo runs). Then compare both against dead reckoning.

Why it matters for EOD robotics: every standoff check, cordon overlay and planned route (06.8)
is only as trustworthy as the pose estimate *and its covariance*. An overconfident filter draws a
small ellipse around the wrong place; the NEES test is how you catch that before an operator
relies on it. The landmarks here are fictional surveyed fiducial markers in a basement (the 06.6
worked example).

## Background

- Bayes filter, KF as Gaussian conditioning, EKF, particle filter, NEES/NIS: [06.6](lessons/stage-06/lesson-06.md) §1–§7.
- Unicycle/skid-steer odometry and why $\chi$ mismatch makes heading drift: [06.4](lessons/stage-06/lesson-04.md) §2–§3.
- Sim B — [EOD Robot](sims/eod-robot/index.html) shows the pose-uncertainty ellipse live;
  Sim G — [Robotics Engineering](sims/robotics-engineering/index.html) has a noisy-sensor challenge.

## Models and Jacobians (derivation)

**State** $x = (x, y, \theta)$, **control** $u = (v, \omega)$ from odometry over step $\Delta t$.

**Motion model** (Euler on the unicycle; at 10 Hz and 0.2 rad/s the arc–chord difference is
$\sim v\Delta t\cdot\omega\Delta t/2 = 5\times10^{-4}$ m, far below the noise):

$$ f(x,u) = \begin{bmatrix} x + v\Delta t\cos\theta \\ y + v\Delta t\sin\theta \\ \theta + \omega\Delta t \end{bmatrix} + w,\qquad w\sim\mathcal N(0, Q). $$

Differentiate row by row. Only $\theta$ enters nonlinearly: $\partial(x + v\Delta t\cos\theta)/\partial\theta = -v\Delta t\sin\theta$ and
$\partial(y + v\Delta t\sin\theta)/\partial\theta = v\Delta t\cos\theta$, so

$$ F = \frac{\partial f}{\partial x} = \begin{bmatrix} 1 & 0 & -v\Delta t\sin\theta \\ 0 & 1 & v\Delta t\cos\theta \\ 0 & 0 & 1 \end{bmatrix}. $$

(If you model noise on $u$ instead of on the state, you also need
$V = \partial f/\partial u = \begin{bmatrix}\Delta t\cos\theta & 0\\ \Delta t\sin\theta & 0 \\ 0 & \Delta t\end{bmatrix}$ and
$Q_x = V M V^\top$; that is extension 1.)

**Measurement model** for landmark $\ell = (\ell_x, \ell_y)$, with $\delta_x = \ell_x - x$,
$\delta_y = \ell_y - y$, $q = \delta_x^2 + \delta_y^2$, $r = \sqrt q$:

$$ h(x) = \begin{bmatrix} r \\ \operatorname{atan2}(\delta_y, \delta_x) - \theta \end{bmatrix} + v,\qquad v\sim\mathcal N(0, R). $$

Range row: $\partial r/\partial x = \frac{1}{2r}\,\partial q/\partial x = \frac{1}{2r}\,2\delta_x\cdot(-1) = -\delta_x/r$;
likewise $\partial r/\partial y = -\delta_y/r$; $\partial r/\partial\theta = 0$.
Bearing row: with $\phi = \operatorname{atan2}(\delta_y, \delta_x)$,
$\mathrm d\phi = (\delta_x\,\mathrm d\delta_y - \delta_y\,\mathrm d\delta_x)/q$ and
$\mathrm d\delta_x = -\mathrm dx$, $\mathrm d\delta_y = -\mathrm dy$, so
$\partial\phi/\partial x = \delta_y/q$, $\partial\phi/\partial y = -\delta_x/q$; and
$\partial(\phi-\theta)/\partial\theta = -1$:

$$ H = \begin{bmatrix} -\delta_x/r & -\delta_y/r & 0 \\ \delta_y/q & -\delta_x/q & -1 \end{bmatrix}. $$

Check (06.6 §3): robot $(1, 2, 30°)$, landmark $(4, 6)$ gives $r = 5$, bearing $23.13°$,
$H = \begin{bmatrix}-0.6 & -0.8 & 0\\ 0.16 & -0.12 & -1\end{bmatrix}$ — a unit test.

**Filter equations** (Joseph form, innovations wrapped):
$\nu = z - h(\bar\mu)$ with $\nu_2 \leftarrow \operatorname{wrap}(\nu_2)$,
$S = HPH^\top + R$, $K = PH^\top S^{-1}$, $\mu \leftarrow \mu + K\nu$ (then wrap $\theta$),
$P \leftarrow (I-KH)P(I-KH)^\top + KRK^\top$, $\text{NIS} = \nu^\top S^{-1}\nu$.
With $f(x) = Ax + Bu$ and $h(x) = Cx$ these are exactly the KF equations — which is the first
correctness test.

**Consistency.** $\text{NEES}_t = e_t^\top P_t^{-1} e_t$, $e_t = x_t - \mu_t$ (heading wrapped).
For a consistent filter $\text{NEES}_t\sim\chi^2_3$; averaged over $N$ runs,
$N\bar\epsilon_t\sim\chi^2_{3N}$, so for $N = 50$ the 95 % band is $[2.36, 3.72]$. NIS
$\sim\chi^2_2$ per landmark update.

## Requirements

1. Motion and measurement models and their Jacobians (verified against finite differences).
2. Linear `kf_predict`/`kf_update` and generic `ekf_predict`/`ekf_update` (Joseph form, returns
   NIS, wraps the listed angular innovation components).
3. `EKF` class for the localisation problem (wrap $\theta$ after every update).
4. `systematic_resample` (single uniform offset) and a bootstrap `ParticleFilter` with
   log-weights, $N_\text{eff}$-triggered resampling, and a circular-mean estimate.
5. `nees` with a wrapped heading error.
6. Provided drivers: `simulate`, `run_ekf`, `run_pf`, `dead_reckoning`, `monte_carlo_nees`,
   `comparison_experiment`, and a `__main__` experiment producing the NEES and trajectory plots.

## API

```python
wrap_angle(a); chi2_band(dof, n_runs=1, alpha=0.05) -> (lo, hi)          # provided
motion_model(x, u, dt) -> (3,);     motion_jacobian(x, u, dt) -> (3,3)
measurement_model(x, landmark) -> (2,);  measurement_jacobian(x, landmark) -> (2,3)
kf_predict(mu, P, A, B, u, Q) -> (mu, P);   kf_update(mu, P, z, C, R) -> (mu, P, nis)
ekf_predict(mu, P, f, F, Q) -> (mu, P);     ekf_update(mu, P, z, h, H, R, angle_idx=()) -> (mu, P, nis)
class EKF(x0, P0, Q, R): predict(u, dt); update(z, landmark) -> nis; .x, .P
systematic_resample(weights, rng) -> indices (N,)
class ParticleFilter(particles, Q, R, rng, resample_threshold=0.5):
    predict(u, dt); update(z, landmark); estimate() -> (mu, cov); .weights (provided)
nees(x_true, x_est, P) -> float
# provided drivers
simulate(landmarks, controls, dt, Q, R, x0, rng, meas_every=5, max_range=inf) -> SimRun
run_ekf(run, x0, P0, Q, R, use_landmarks=True) -> {est, cov, nees, nis}
run_pf(run, particles, Q, R, rng) -> {est, cov};  dead_reckoning(run, x0) -> (T+1,3)
monte_carlo_nees(n_runs=50, n_steps=300, seed=0, q_scale=1.0) -> {mean_nees, band, fraction_inside, mean_nis}
comparison_experiment(seed=1, n_steps=600, n_particles=1000) -> {rmse: {dead_reckoning, ekf, pf}, ...}
```

## Input / output

- **Input**: landmark map `(L,2)`; control sequence `(T,2)`; `dt`; `Q` (3×3), `R` (2×2); initial
  mean/covariance or particle set; a seeded `numpy.random.Generator`. The lesson scenario is
  exported as `LESSON_LANDMARKS` = (5,0), (5,8), (−2,6) m, `LESSON_Q` (σ = 2 cm, 2 cm, 1° per 0.1 s
  step), `LESSON_R` (σ = 10 cm, 2°), `LESSON_P0`.
- **Output**: estimated trajectories and covariances, NEES per step, NIS per update, RMSE, plots.

## Constraints

- NumPy/SciPy only; all angles wrapped to $[-\pi,\pi)$; deterministic seeds.
- 50 Monte Carlo EKF runs of 300 steps in a few seconds; the whole test suite < 30 s.
- Vectorise the particle filter over particles (no Python loop over particles).

## Expected behaviour

| Experiment | Expected |
|---|---|
| EKF, correct $Q$, 50 runs | mean NEES ≈ 2.9–3.1 (lesson: 3.04), ≥ 85 % of steps inside $[2.36, 3.72]$ (≈ 95 % ideal), mean NIS ≈ 2 |
| EKF, $Q/20$ | mean NEES ≈ 27 (lesson: 27.5): ellipse ≈ 3× too small per axis |
| PF, 2000 particles, uniform prior over the room | starts > 1.5 m off, ends < 0.4 m and < 0.15 rad |
| 600 steps, known start | EKF and PF RMSE ≈ 0.08 m; dead reckoning ≈ 2 m |
| P05 cross-check | with slip ($\chi$ 1.6 vs model 1.4) and biased tracks, odometry drifts; the EKF stays < 0.3 m |

## Test cases (`tests/test_localization.py`)

| Test | What it checks |
|---|---|
| `test_motion_model_and_jacobian`, `test_measurement_model_lesson_example` | analytic values, angle wrapping, Jacobians vs central differences, lesson 06.6 §3 numbers |
| `test_ekf_equals_kf_on_linear_gaussian_model`, `test_kf_update_scalar_by_hand` | generic EKF reduces to the KF exactly (to 1e-12) on a constant-acceleration model; scalar update by hand |
| `test_ekf_noise_free_tracks_truth` | no noise → estimate equals truth |
| `test_nees_definition`, `test_monte_carlo_nees_within_chi2_bounds`, `test_understated_q_is_detected` | NEES/NIS chi-square consistency over seeded Monte Carlo runs, and detection of mis-tuning |
| `test_systematic_resample_counts`, `test_particle_filter_estimate_circular_mean`, `test_pf_converges_from_wide_prior` | resampling invariant $\lfloor Nw_i\rfloor \le n_i \le \lceil Nw_i\rceil$; circular mean across ±π; global localisation (3 seeds) |
| `test_landmarks_beat_dead_reckoning` | landmarks cut RMSE by > 4× vs odometry |
| `test_with_robotsim2d_if_available` | optional cross-check on P05 skid-steer truth and biased odometry |

## Milestones

1. Models and Jacobians (derive on paper first, then test against finite differences).
2. `kf_*` and `ekf_*`: pass the linear-Gaussian equivalence test.
3. `EKF` + `nees`: run `monte_carlo_nees`; plot mean NEES with the band (`python solution/localization.py` shows the target plot).
4. Particle filter: resampling, weights in log space, circular mean; global localisation.
5. Comparison experiment and a short write-up: RMSE table, NEES plot for $Q$ and $Q/20$.

## Extension challenges

1. Put the noise on the controls ($M = \mathrm{diag}(\sigma_v^2, \sigma_\omega^2)$, $Q_x = VMV^\top$) and rerun the NEES test; then deliberately use the wrong model and watch NEES.
2. Augment the state with the slip factor $\chi$ (or a gyro bias $b_g$) and estimate it online (06.6 §8).
3. Implement the UKF and compare NEES during aggressive turns (large heading uncertainty).
4. Unknown correspondences: NIS gating with $\chi^2_2(0.99) = 9.21$, nearest neighbour vs joint compatibility; inject reflections as outliers.
5. KLD-sampling to adapt the number of particles; measure particles vs time during global localisation.
6. Replace `simulate` with the P05 `Simulator` (lidar-extracted landmarks, channel-delayed measurements) and handle out-of-sequence measurements.

## Hints

<details><summary>Hint 1 — angle wrapping, three places</summary>

Wrap (i) the predicted heading, (ii) the bearing innovation before multiplying by $K$, and (iii)
the heading after the update. Also wrap the heading error inside NEES. Forgetting (ii) produces
occasional catastrophic corrections near $\pm\pi$ and a NEES spike.

</details>

<details><summary>Hint 2 — numerically safe gain and covariance</summary>

Use `np.linalg.solve(S, H @ P).T` instead of `P @ H.T @ inv(S)`, and the Joseph form
$(I-KH)P(I-KH)^\top + KRK^\top$ — it stays symmetric positive definite even with round-off.

</details>

<details><summary>Hint 3 — particle weights</summary>

Accumulate log-likelihoods, subtract the maximum before exponentiating, and resample only when
$N_\text{eff} = 1/\sum w_i^2 < N/2$. For global localisation, using a somewhat inflated $R$ in
the PF (here $4R$) prevents premature collapse when particles are sparse — a standard, honest
engineering trade-off (you trade a little precision for robustness).

</details>

<details><summary>Hint 4 — circular mean</summary>

$\bar\theta = \operatorname{atan2}(\sum w_i\sin\theta_i, \sum w_i\cos\theta_i)$. The arithmetic
mean of $\pi-0.1$ and $-\pi+0.1$ is 0 — pointing the wrong way.

</details>

## How to run

```bash
python -m pytest projects/p04-localization                     # your starter
EOD_SOLUTION=1 python -m pytest projects/p04-localization      # reference solution (bash)
python projects/p04-localization/solution/localization.py      # NEES + comparison plots
```

On Windows `cmd`: `set EOD_SOLUTION=1 && py -m pytest projects/p04-localization`.

The module is self-contained; the one P05 cross-check test adds `projects/p05-robot-sim/solution`
to `sys.path` and is skipped if P05 is absent (see the P05 README, "Using robotsim2d from other
projects").
