# P02 · Sensor-noise simulator (`sensornoise`)

<div class="module-card">

**Lessons** [05.1 Detection theory, ROC & T&E](lessons/stage-05/lesson-01.md) (core) · [05.2 EMI & GPR](lessons/stage-05/lesson-02.md) · [05.3 Penetrating radiation](lessons/stage-05/lesson-03.md) · [05.4 Trace & vapour](lessons/stage-05/lesson-04.md) · [05.5 Imaging & remote sensing](lessons/stage-05/lesson-05.md)

**Level** Intermediate · **Estimated time** 8–10 h

**Simulator** [Sim J · Detection theory](sims/detection-theory/index.html) · **Feeds** [P03 Bayesian fusion](projects/p03-bayesian-fusion/README.md)

<p class="tags"><span>stochastic sensor models</span><span>Poisson clutter</span><span>ROC</span><span>AUC</span><span>Monte Carlo</span><span>Clopper–Pearson</span><span>Wilson</span><span>trial planning</span></p>
</div>

## Goal

Build the statistics engine behind every detection claim in Stage 5: sensor models that produce
realistic scores (with the persistent, per-location errors that real sensors have), a spatial
false-alarm process, $P_d$ as a function of SNR and range, Monte-Carlo ROC curves with AUC, honest
confidence intervals for $P_d$ and $P_{fa}$ — including their actual coverage — and the number of
targets a blind trial needs.

The central lesson is uncomfortable and practical: looking again at the same spot does **not**
give you independent evidence. The bias that belongs to the place (soil, a buried nail, geometry)
survives every repeat. P03 then shows what that does to fusion.

<div class="callout boundary">

**Boundary.** Sensors, targets and clutter are generic and fictional; parameters are illustrative
and claim nothing about any real detector. The project teaches how performance is *measured and
reasoned about*, not how to defeat or evade detection.

</div>

## Background

- Hypothesis testing, Neyman–Pearson, ROC/AUC, base rates, costs, blind trials, Clopper–Pearson and
  Poisson intervals, zero-failure demonstration: [05.1](lessons/stage-05/lesson-01.md) §1–§7.
- Where the score distributions come from — induction and radar ([05.2](lessons/stage-05/lesson-02.md)),
  photon-counting noise ([05.3](lessons/stage-05/lesson-03.md)), trace-detector peaks and interferents
  ([05.4](lessons/stage-05/lesson-04.md)), thermal contrast versus clutter ([05.5](lessons/stage-05/lesson-05.md)).

Key relations:

$$
s_{jr}=\mu_H+k_H\,(b_j+e_{jr}),\quad b_j\sim\mathcal N(0,\sigma_b^2),\ e_{jr}\sim\mathcal N(0,\sigma_e^2)
\;\Rightarrow\;
\operatorname{Var}\Big[\tfrac1k\textstyle\sum_r s_{jr}\Big]=\sigma_b^2+\sigma_e^2/k\ \ge\ \sigma_b^2
$$

$$
\text{AUC}_{\text{binormal}}=\Phi\!\Big(\frac{d'}{\sqrt{1+\sigma^2}}\Big),\qquad
P_d=Q\big(Q^{-1}(P_{fa})-\sqrt{\text{SNR}}\big),\qquad
\text{SNR}(r)=\text{SNR}_\text{ref}-10n\log_{10}\frac{r}{r_\text{ref}}-\alpha(r-r_\text{ref})
$$

$$
n_{\text{demo}}=\Big\lceil\frac{\ln(1-C)}{\ln p_0}\Big\rceil\quad(\text{zero misses}),\qquad
N_{\text{clutter}}(A)\sim\text{Poisson}(\lambda A)
$$

## Requirements

1. `GaussianSensor` with persistent per-location bias and fresh per-look noise; `measure`,
   `sd0`, `d_prime`, `theoretical_auc`. Helpers `mean_of_repeats_variance` and `effective_looks`
   ($k_\text{eff}=k/(1+(k-1)\rho)$, $\rho=\sigma_b^2/(\sigma_b^2+\sigma_e^2)$).
2. `PoissonClutter` (homogeneous spatial Poisson process): `expected_count`, `sample`.
3. `threshold_for_pfa`, `pd_from_snr`, `snr_at_range`, `pd_at_range`.
4. `empirical_roc` (vectorised, ties handled, trapezoidal AUC), `auc_mann_whitney` (ranks),
   `binormal_auc`, `monte_carlo_roc`, `bootstrap_auc_ci`.
5. `wilson_interval`, `clopper_pearson`, `poisson_rate_ci`; `exact_coverage` (sum over the
   binomial pmf) and `simulate_coverage` (Monte Carlo); `empirical_rates`.
6. `n_for_demo` (closed form for zero misses, binomial search otherwise) and `demo_pass_probability`.

`wald_interval` is **provided** as the cautionary baseline — you will measure how badly it
covers at high $P_d$.

## API

```python
class GaussianSensor(mu0=0.0, mu1=2.0, noise_sd=1.0, bias_sd=0.0, h1_scale=1.0):
    sd0 -> float; d_prime -> float
    measure(truth: bool[n], n_repeats=1, rng=None) -> scores (n, n_repeats)
    theoretical_auc() -> float
mean_of_repeats_variance(bias_sd, noise_sd, k) -> float
effective_looks(bias_sd, noise_sd, k) -> float
class PoissonClutter(rate_per_m2): expected_count(area_m2); sample(width, height, rng) -> (N, 2)
threshold_for_pfa(pfa, mu0=0, sd0=1) -> float
pd_from_snr(snr_db, pfa) -> Pd
snr_at_range(r, snr_ref_db, r_ref=1, path_exponent=4, atten_db_per_m=0) -> dB
pd_at_range(r, pfa, snr_ref_db, r_ref=1, path_exponent=4, atten_db_per_m=0) -> Pd
empirical_roc(s0, s1) -> (pfa, pd, auc)
auc_mann_whitney(s0, s1) -> float;  binormal_auc(d_prime, sigma_ratio=1) -> float
monte_carlo_roc(sensor, n0, n1, rng=None, n_repeats=1) -> dict(s0, s1, pfa, pd, auc)
bootstrap_auc_ci(s0, s1, n_boot=500, conf=0.95, rng=None) -> (lo, hi)
wald_interval(k, n, conf=0.95)                                   # provided
wilson_interval(k, n, conf=0.95); clopper_pearson(k, n, conf=0.95) -> (lo, hi)
poisson_rate_ci(k, exposure, conf=0.95) -> (lo, hi)
exact_coverage(interval, p, n, conf=0.95) -> float
simulate_coverage(interval, p, n, conf=0.95, n_trials=2000, rng=None) -> float
empirical_rates(s0, s1, threshold, conf=0.95, method=clopper_pearson) -> dict(pd, pd_ci, pfa, pfa_ci, k1, n1, k0, n0)
n_for_demo(p0, conf=0.95, misses_allowed=0) -> int
demo_pass_probability(p_true, n, misses_allowed=0) -> float
```

## Input / output

- **Input**: model parameters (means, standard deviations, clutter intensity per m², SNR at a
  reference range, path exponent, attenuation), sample sizes, trial counts $(k, n)$, confidence
  levels, and a seeded `numpy.random.Generator`.
- **Output**: score arrays, clutter coordinates, ROC arrays and AUC, intervals as `(lo, hi)`
  tuples, coverage probabilities, sample sizes.

## Constraints

- NumPy/SciPy only; deterministic seeds everywhere (pass `rng` explicitly).
- `empirical_roc` must be vectorised: no Python loop over thresholds, $\le 2$ s for
  $n_0=n_1=10^5$ (sort + `searchsorted` is $O(n\log n)$).
- The whole test suite < 30 s.

## Expected behaviour

| Experiment | Expected |
|---|---|
| Equal-variance Gaussian, $d'=2$ | AUC $\Phi(2/\sqrt2)=0.921$; MC with 4000 + 4000 within 4 standard errors (Hanley–McNeil) |
| Unequal variance $d'=1.5$, $\sigma=1.5$ | AUC $0.797$ |
| Bias 0.5, noise 1.0, averaging $k$ looks | error variance $0.25+1/k$; never below 0.25; $k_\text{eff}\to 1/\rho = 5$ |
| $\mu_1=1$, bias 0.5, noise 1, mean of 50 looks | AUC ≈ 0.91, not the 0.99999 that independent looks would promise |
| `clopper_pearson(98, 100)` | (0.9296, 0.9976); Wilson (0.9300, 0.9945) |
| Coverage at $P_d=0.99$, $n=50$ | Wald ≈ 0.39, Wilson ≈ 0.91, Clopper–Pearson ≥ 0.95 (0.986) |
| `poisson_rate_ci(0, 1)` | upper bound 3.689 |
| `n_for_demo(0.99)`, 1 miss allowed, `n_for_demo(0.996)` | 299, 473, 748 |
| Doubling range, $n=4$ | SNR falls by 12.04 dB |

## Test cases (`tests/test_sensornoise.py`)

| Test | What it checks |
|---|---|
| `test_gaussian_sensor_moments`, `test_measure_is_reproducible` | means, standard deviations under both hypotheses; seeding |
| `test_correlated_repeats_do_not_beat_the_bias` | variance of the mean of $k$ looks $=\sigma_b^2+\sigma_e^2/k \ge \sigma_b^2$; within-location correlation; $k_\text{eff}\to1/\rho$ |
| `test_repeats_improve_auc_only_up_to_the_bias_limit` | ROC gain from repeats saturates at the bias-limited AUC |
| `test_poisson_clutter_counts_and_positions`, `test_poisson_rate_ci` | mean $\lambda A$, dispersion index ≈ 1, uniform positions; Garwood values and ≥ 95 % exact coverage |
| `test_pd_from_snr`, `test_snr_and_pd_vs_range` | $P_d=P_{fa}$ at zero SNR, monotone, agrees with Monte Carlo; spreading and attenuation loss; $P_d$ falls with range |
| `test_empirical_roc_structure_and_mann_whitney`, `test_empirical_roc_is_fast` | end points, monotone, AUC = brute-force Mann–Whitney with ties (1e-12); speed |
| `test_binormal_auc_by_monte_carlo`, `test_equal_variance_dprime_2`, `test_bootstrap_auc_ci_contains_truth` | $\Phi(d'/\sqrt{1+\sigma^2})$ within MC tolerance; bootstrap interval sanity |
| `test_interval_known_values`, `test_clopper_pearson_coverage_is_guaranteed`, `test_wilson_coverage_near_nominal_wald_fails_at_high_pd`, `test_simulated_coverage_matches_exact` | published values; exact coverage ≥ 95 % for CP over a $(p,n)$ grid; Wilson ≈ nominal on average; Wald collapses; MC coverage agrees with exact |
| `test_empirical_rates`, `test_n_for_demo` | counts and intervals at a threshold; 299/473/748; $n$ is the *smallest* sufficient trial |

## Milestones

1. `GaussianSensor.measure` and the repeat-variance helpers; convince yourself with a histogram.
2. `PoissonClutter` and `poisson_rate_ci`; simulate a 50 m × 40 m lane and report FAR per m² with its interval.
3. `pd_from_snr` and the range functions; plot $P_d(r)$ for two path exponents.
4. `empirical_roc`, `auc_mann_whitney`, `binormal_auc`, `monte_carlo_roc`; plot ROC curves for 1, 4 and 50 looks with bias.
5. Intervals and coverage; plot exact coverage vs $p$ for Wald, Wilson and CP at $n=50$ (the saw-tooth is the point).
6. Trial planning; write a paragraph: "we detected all 50 targets" supports what, at 95 %?

## Extension challenges

1. **Clutter as a marked process**: give each clutter object a score from a Gaussian mixture and a
   target a lognormal amplitude; produce a free-response ROC (FROC: $P_d$ vs false alarms per m²).
2. **Sensor classes from 05.2–05.5**: `EMISensor` (dipole fall-off, path exponent 6, soil bias),
   `GPRSensor` (attenuation in dB/m from soil conductivity), `XRaySensor` (Poisson photon counts →
   $-\ln T$), `TraceSensor` (Poisson-limited peak plus interferents). Keep the same `measure` API.
3. Fit a binormal ROC to rating data by maximum likelihood and compare its AUC CI with the bootstrap.
4. Power of McNemar's test for a paired comparison of two detectors on the same targets (05.1 exercise 6).
5. Partial AUC over $P_d\in[0.95,1]$ — the region that matters for clearance — with a bootstrap CI.
6. Replace the per-location Gaussian bias with a spatially correlated random field (Gaussian process
   on the lane) and measure how the correlation length changes $k_\text{eff}$ for a sweeping detector.

## Hints

<details><summary>Hint 1 — the bias is drawn once per location</summary>

Draw `bias` with shape `(n, 1)` and `noise` with shape `(n, n_repeats)` and add them; broadcasting
shares the bias across a row. Under $H_1$ multiply both by `h1_scale`.

</details>

<details><summary>Hint 2 — a vectorised ROC with ties</summary>

Take the distinct scores in descending order as thresholds. With `s0s = np.sort(s0)`,
`P(s0 >= t) = (n0 - np.searchsorted(s0s, t, side="left")) / n0`. Tied H0/H1 scores then move the
curve diagonally, and the trapezoid gives exactly the ½-credit Mann–Whitney statistic.

</details>

<details><summary>Hint 3 — exact coverage needs no simulation</summary>

For fixed $(p, n)$, only $k=0,\dots,n$ can occur. Coverage is
$\sum_k \binom nk p^k(1-p)^{n-k}\,\mathbf 1[\text{lo}(k)\le p\le\text{hi}(k)]$ — a dot product of the
binomial pmf with a boolean vector.

</details>

<details><summary>Hint 4 — floating point in the demonstration formula</summary>

$\ln 0.05/\ln 0.99 = 298.07$, so `ceil` gives 299. When the ratio is (mathematically) an integer,
round-off can push it just above; subtract a tiny epsilon before `ceil`, and check your answer with
`demo_pass_probability(p0, n) <= 1 - conf < demo_pass_probability(p0, n - 1)`.

</details>

## How to run

```bash
python -m pytest projects/p02-sensor-noise                     # your starter
EOD_SOLUTION=1 python -m pytest projects/p02-sensor-noise      # reference solution (bash)
```

On Windows `cmd`: `set EOD_SOLUTION=1 && py -m pytest projects/p02-sensor-noise`.
