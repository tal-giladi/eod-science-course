# P03 · Bayesian sensor fusion and information-driven scheduling (`bayesfusion`)

<div class="module-card">

**Lessons** [05.6 Sensor fusion](lessons/stage-05/lesson-06.md) (core) · [05.1 Detection theory](lessons/stage-05/lesson-01.md) (LLRs, ROC) · [05.7 Search theory & area clearance](lessons/stage-05/lesson-07.md) (where the map is used)

**Level** Advanced · **Estimated time** 10–12 h

**Builds on** [P02 Sensor-noise simulator](projects/p02-sensor-noise/README.md) · **Simulator** [Sim C · Sensor fusion](sims/sensor-fusion/index.html) · **Feeds** [P07 SLAM](projects/p07-slam/README.md) (same grid), [P12 HITL decisions](projects/p12-hitl-decision/README.md), Capstone C1

<p class="tags"><span>log-odds</span><span>occupancy grid</span><span>inverse sensor model</span><span>correlated errors</span><span>mutual information</span><span>greedy scheduling</span><span>calibration</span></p>
</div>

## Goal

Implement the fusion loop of 05.6 end to end: a log-odds grid that accumulates evidence from
several sensors through inverse sensor models; a demonstration — with numbers — that treating
correlated sensors as independent makes the map **overconfident**, and that the joint Gaussian
likelihood fixes it; expected information gain (mutual information) per sensor and cell; a greedy
information-per-cost scheduler under a budget; and an evaluation harness (Brier score, log-loss,
ROC and reliability diagram of the fused map).

<div class="callout boundary">

**Boundary.** The grid holds fictional "objects of interest" in a synthetic search area; sensors
are abstract $(P_d, P_f)$ or Gaussian-score models. The project is about reasoning under
uncertainty — how much to believe a map and where to look next — not about any real sensor, object
or procedure.

</div>

## Background

- Log-odds accumulation under conditional independence, inverse sensor models, clamping:
  [05.6](lessons/stage-05/lesson-06.md) §1 and §5.
- Correlated errors, the Gaussian copula, $N_\text{eff}=N/(1+(N-1)\rho)$: [05.6](lessons/stage-05/lesson-06.md) §2.
- Information gain vs value of information, submodularity and the greedy $(1-1/e)$ guarantee:
  [05.6](lessons/stage-05/lesson-06.md) §6.
- LLRs, ROC and why calibration matters for decisions: [05.1](lessons/stage-05/lesson-01.md);
  per-location persistent errors: [P02](projects/p02-sensor-noise/README.md).

Key relations:

$$
\ell_t(c)=\operatorname{clip}\big(\ell_{t-1}(c)+\lambda(z;c),\ \ell_{\min},\ \ell_{\max}\big),\qquad
\lambda_{\text{alarm}}=\ln\frac{P_d}{P_f},\quad \lambda_{\text{silence}}=\ln\frac{1-P_d}{1-P_f}
$$

$$
\Lambda_{\text{naive}}=\sum_i\frac{\mu_is_i-\mu_i^2/2}{\sigma_i^2},\qquad
\Lambda_{\text{joint}}=\boldsymbol\mu^\top C^{-1}\mathbf s-\tfrac12\boldsymbol\mu^\top C^{-1}\boldsymbol\mu,\qquad
\text{equicorrelated: }\ \Lambda_{\text{naive}}=\big(1+(N-1)\rho\big)\Lambda_{\text{joint}}
$$

$$
I(X;Z)=H_b\big(pP_d+(1-p)P_f\big)-\big[pH_b(P_d)+(1-p)H_b(P_f)\big],\qquad 0\le I\le H_b(p)
$$

## Requirements

1. `fuse_ci`, `llr_binary`, `llr_gaussian`, `footprint_llr` (inverse sensor model with a kernel of
   weights $w\in[0,1]$: $P(\text{alarm}\mid X_c=1)=P_f+w(P_d-P_f)$).
2. `LogOddsGrid.update` — full-grid or kernel-centred evidence (kernel clipped at the borders),
   clamped to $[\ell_{\min},\ell_{\max}]$.
3. `llr_naive` (diagonal only), `llr_joint` (full covariance, solve don't invert), `fuse_scores`,
   `overconfidence_factor`.
4. `info_gain_binary` (exact enumeration over $z\in\{0,1\}$, vectorised over $p$) and
   `info_gain_gaussian` (quadrature of $H_b(p)-\mathbb E_S[H_b(P(X{=}1\mid S))]$).
5. `run_schedule` with `policy="greedy"` (max gain / cost over affordable sensor × cell; stop when
   the best is ≤ `min_gain` or nothing is affordable) and `policy="random"` (the baseline).
6. `brier`, `log_loss`, `roc_auc`, `calibration_curve`.

**Provided** (not the learning goal): `logit`, `sigmoid`, `binary_entropy`, the `Sensor`
dataclass, `simulate_reading`, `simulate_correlated_scores`, `equicorr_cov`, and
`LogOddsGrid.__init__/posterior/entropy`.

## API

```python
logit(p); sigmoid(l); binary_entropy(p) -> bits                               # provided
Sensor(name, pd, pf, cost=1.0)                                                  # provided
simulate_reading(x, sensor, rng) -> bool                                        # provided
simulate_correlated_scores(truth, mu, cov, rng) -> (n, N)                       # provided
equicorr_cov(n, rho, sd=1.0) -> (n, n)                                          # provided
fuse_ci(p0, lrs) -> float
llr_binary(z, pd, pf); llr_gaussian(s, mu, sd=1.0); footprint_llr(z, pd, pf, kernel)
class LogOddsGrid(prior, lmin=-8.0, lmax=8.0):
    update(llr, center=None) -> self; posterior(); entropy(); .l
llr_naive(s, mu, cov); llr_joint(s, mu, cov)          # s: (N,) or (n, N)
fuse_scores(prior, S, mu, cov, method="joint" | "naive") -> (n,)
overconfidence_factor(n, rho) -> float
info_gain_binary(p, pd, pf) -> bits;  info_gain_gaussian(p, mu, sd=1.0, n_grid=4001) -> bits
run_schedule(prior, truth, sensors, budget, policy="greedy", rng=None,
             lmin=-8.0, lmax=8.0, min_gain=1e-9) -> dict(posterior, log, spent)
    # log entries: (sensor_name, cell_index, alarm, gain_bits, cost)
brier(p, y); log_loss(p, y, eps=1e-12); roc_auc(p, y)
calibration_curve(p, y, n_bins=10) -> (mean_predicted, observed_frequency, counts)
```

## Input / output

- **Input**: prior probability map (any shape, usually 2-D); sensor list (`Sensor` with
  $P_d, P_f$, cost) or Gaussian score model ($\boldsymbol\mu$, covariance $C$); a hidden ground
  truth (simulation only); a budget in abstract cost units; a seeded `numpy.random.Generator`.
- **Output**: posterior maps, fused posteriors per location, information gains in bits, the
  action log, and evaluation metrics.

## Constraints

- NumPy/SciPy only; deterministic seeds.
- Per-reading grid update in $O(\text{footprint})$; `info_gain_binary` vectorised over the whole
  map (the scheduler evaluates every cell for every sensor at each step).
- Log-odds clamped at ±8 nats by default. Whole test suite < 30 s.

## Expected behaviour

| Experiment | Expected |
|---|---|
| `fuse_ci(0.01, [5, 8, 3])` | 0.548 |
| 1-D strip, prior 0.02, MD then GPR footprints (05.6 §5) | posterior (0.020, 0.030, 0.155, 0.133, 0.030) |
| $N=3$, $\mu=1.5$, $\rho=0.6$, all $s_i=1.5$ | naive LLR 3.375, joint 1.534 (ratio $1+2\rho=2.2$) |
| 200 000 simulated cells, prior 0.05, same sensors | naive posteriors > 0.9 are right only ≈ 55 % of the time; joint posteriors lie on the diagonal within MC error; joint has lower log-loss and Brier |
| `info_gain_binary(0.2, .9, .1)` vs `(0.2, .95, .3)` | 0.358 vs 0.224 bit |
| Gaussian sensor | $I=0$ at $\mu=0$; increases with $\mu$; $\to H_b(p)$ as $\mu\to\infty$; matches Monte Carlo to 3e-3 bit |
| 15 × 15 field with two hot spots, budget 120, sensors A (0.9/0.1, cost 1) and B (0.75/0.25, cost 0.4), 6 seeds | greedy's mean log-loss ≈ 15–20 % below random and lower in ≥ 5 of 6 seeds |
| Budget 0 | no actions; posterior = prior |

## Test cases (`tests/test_bayesfusion.py`)

| Test | What it checks |
|---|---|
| `test_fuse_ci_lesson_value` | 05.6 value; LR = 1 changes nothing; order invariance |
| `test_single_binary_sensor_reproduces_bayes`, `test_single_gaussian_sensor_reproduces_bayes` | one reading through the grid equals Bayes' rule exactly; for one sensor joint = naive = scalar LLR |
| `test_grid_strip_example_and_kernel_placement`, `test_grid_clamping`, `test_footprint_llr` | 05.6 strip numbers; kernel centring and border clipping; clamps; footprint LLR limits and ordering |
| `test_equicorrelated_closed_form` | 3.375 vs 1.534; naive/joint ratio $=1+(N-1)\rho$ for arbitrary scores; equality at $\rho=0$ |
| `test_naive_fusion_is_overconfident_joint_is_calibrated` | reliability diagram: naive overconfident by > 0.25 in its top bin, joint within MC error in every populated bin; joint wins on log-loss and Brier |
| `test_info_gain_binary_values_and_enumeration`, `test_info_gain_bounds`, `test_info_gain_gaussian_matches_monte_carlo` | lesson values; $0\le I\le H_b(p)$ on 2000 random cases; limits; Gaussian quadrature vs MC |
| `test_budget_zero_takes_no_action`, `test_schedule_respects_budget_and_logs`, `test_greedy_first_choice_maximises_gain_per_cost` | budget accounting, log format, greedy picks the true arg-max |
| `test_greedy_beats_random` | seeded synthetic fields: greedy beats random on log-loss and Brier |
| `test_metrics` | Brier, log-loss (finite under clipping), AUC with ties, calibration bins |

## Milestones

1. Log-odds helpers and `fuse_ci`; `llr_binary`, `llr_gaussian`; the single-sensor Bayes tests.
2. `LogOddsGrid.update` with kernels; reproduce the 05.6 strip; add `footprint_llr` and draw a 2-D posterior after a few simulated sweeps.
3. `llr_naive`, `llr_joint`, `fuse_scores`; plot the two reliability diagrams side by side. This plot is the main result of the project.
4. `info_gain_binary`, `info_gain_gaussian`; plot $I$ vs $p$ for both sensors of 05.6 §6.
5. `run_schedule` and the metrics; plot log-loss vs budget spent for greedy vs random (mean over seeds).

## Extension challenges

1. **VOI scheduler**: replace information gain by value of information with losses $L_m$, $L_e$
   (05.6 §6) and stop when no VOI exceeds cost; show a case where VOI and information gain rank
   two sensors differently (`voi(0.2,.95,.3) > voi(0.2,.9,.1)`).
2. **Correlated repeats in the scheduler**: give each (sensor, cell) a persistent bias as in P02 so
   that repeated readings are correlated. Watch greedy-CI "hammer" one cell; fix it with a
   per-cell effective-looks correction or a tempered LLR.
3. **Gaussian copula with non-Gaussian marginals**: gamma-distributed thermal scores plus a
   Poisson count sensor; estimate $R$ on normal scores from a synthetic "blind trial" and fuse
   with the copula correction.
4. **Footprint-aware information gain**: for a kernel sensor the reading depends on several
   cells; compute EIG by Monte Carlo over the joint and compare with the single-cell approximation.
5. **Two-step lookahead** and a brute-force optimal schedule on a 3 × 3 grid with budget 4; measure
   how close greedy gets (the $(1-1/e)$ bound is for information gain, which is submodular).
6. Learn the fusion by logistic regression on stacked scores and compare its calibration with the
   joint Gaussian model under model misspecification (heavy-tailed noise).

## Hints

<details><summary>Hint 1 — stable log-odds</summary>

Use `np.log(p) - np.log1p(-p)` for logit and `np.exp(-np.logaddexp(0, -l))` for the sigmoid.
For a silent reading use `np.log1p(-pd) - np.log1p(-pf)`; it stays accurate when $P_d\to1$.

</details>

<details><summary>Hint 2 — the joint LLR without an inverse</summary>

`w = np.linalg.solve(C, mu)` once; then $\Lambda = S\,w - \tfrac12\,\mu\cdot w$ for a whole
$(n, N)$ score matrix in one line. Naive Bayes is the same formula with `C` replaced by `np.diag(np.diag(C))`.

</details>

<details><summary>Hint 3 — kernel placement at the border</summary>

For each axis compute the grid slice `max(0, c-h) : min(n, c+h+1)` and the matching kernel slice
by subtracting `c-h`. Build both as tuples of slices and add `kernel[ks]` into `l[gs]`.

</details>

<details><summary>Hint 4 — quadrature for the Gaussian information gain</summary>

Integrate over $s\in[\min(0,\mu)-10\sigma,\ \max(0,\mu)+10\sigma]$ with a few thousand points:
the mixture density $pf_1+(1-p)f_0$ times $H_b$ of the posterior. The integrand is smooth, so the
trapezoid rule is accurate to far better than the test's tolerance.

</details>

<details><summary>Hint 5 — why greedy wins, and when it would not</summary>

Greedy concentrates readings where the belief is most uncertain per unit cost — the hot spots —
while random spends most of its budget confirming the 5 % background. It would lose its edge if
repeated readings were correlated (extension 2), because it keeps returning to the same uncertain
cells.

</details>

## How to run

```bash
python -m pytest projects/p03-bayesian-fusion                  # your starter
EOD_SOLUTION=1 python -m pytest projects/p03-bayesian-fusion   # reference solution (bash)
```

On Windows `cmd`: `set EOD_SOLUTION=1 && py -m pytest projects/p03-bayesian-fusion`.
