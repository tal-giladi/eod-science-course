# P12 · Human-in-the-loop decision system

<div class="module-card">

**Lessons** [07.1 Decisions under uncertainty](lessons/stage-07/lesson-01.md) (expected loss, thresholds, EVPI/EVSI, Bellman lookahead) · [09.2 Uncertainty-aware ML](lessons/stage-09/lesson-02.md) (temperature scaling, split and Mondrian conformal, abstention) · [09.6 Trustworthy deployment](lessons/stage-09/lesson-06.md) (automation bias, alarm fatigue, cost-weighted thresholds)

**Simulators** [Sim F — incident command](sims/incident-command/index.html) · [Sim J — detection theory](sims/detection-theory/index.html) · [Sim C — sensor fusion](sims/sensor-fusion/index.html)

**Module** `hitl` · **Level** Expert · **Time** 10–14 h · **Builds on** [P03 Bayesian fusion](projects/p03-bayesian-fusion/README.md), [P09 CV detection](projects/p09-cv-detection/README.md) · **Feeds** capstone [C1](capstones/c1-autonomous-mission.md)

</div>

<div class="callout boundary">

**Fictional incidents, abstract actions.** Classes are "clutter", "benign item" and "hazard-like";
the two commit actions are the abstract *full response* and *release* of lesson 07.1; losses are in
abstract loss units (LU). The engine is a decision-theory exercise about calibration, guarantees and
the value of asking — it contains no procedure for handling any real object.

</div>

## Goal

Build the decision layer that sits between a perception model and an operator: turn raw classifier
scores into calibrated beliefs, attach distribution-free prediction sets, and choose — per incident —
whether to **declare**, **gather more data** (a costly second look with a known sensor model) or
**escalate to a human** (costly, near-perfect), under strongly asymmetric losses. Evaluate risk,
coverage, human workload and expected cost against the baselines *always ask* and *threshold only*.

## Background

- **Temperature scaling** (09.2 §3): $T^*=\arg\min_T \mathrm{NLL}(T)$; convex in $1/T$; accuracy invariant.
- **Split conformal** (09.2 §5): $\hat q$ = the $\lceil(n+1)(1-\alpha)\rceil$-th smallest LAC score
  $1-\hat p_y$; $1-\alpha\le P(y\in\mathcal C)\le 1-\alpha+\tfrac1{n+1}$. **Mondrian** (§5.1): per-class
  thresholds and budgets $\alpha_k$; needs $n_k\ge(1-\alpha_k)/\alpha_k$ calibration points per class.
- **Expected loss and VOI** (07.1 §3–4): $p^*=\frac{\ell(F,B)-\ell(R,B)}{(\ell(F,B)-\ell(R,B))+(\ell(R,H)-\ell(F,H))}$;
  $\text{EVPI}=\mathcal L_0-\mathcal L_{\text{PI}}\ge\text{EVSI}=\mathcal L_0-\mathcal L_{\text{SI}}\ge0$;
  gather iff EVSI > cost; finite-horizon Bellman recursion over beliefs.
- **Human factors** (09.6 §8–9): workload and alarm fatigue are part of the objective, and a risk
  *guarantee* ("at most $\alpha_h$ of hazards are auto-released") is a policy constraint, not an
  expected-loss consequence.

## Requirements

1. **Calibration.** `nll`, `fit_temperature` (bounded 1-D minimisation over $\log T$),
   `expected_calibration_error`.
2. **Conformal.** `conformal_threshold` (robust ceiling: subtract 1e-9; `+inf` and a
   `RuntimeWarning` when $k>n$), `min_calibration_size`, `lac_scores`, `fit_conformal` (marginal or
   class-conditional with per-class `alphas`), `prediction_sets`.
3. **Decision theory** (batched over beliefs `(n, K)`): `commit_losses`, `decision_threshold`,
   `obs_probability`, `posterior`, `evpi`, `evsi`, `human_value`, `q_values` / `value` / `decide`
   (exact Bellman recursion with `max_gathers` steps; ties → commit, then escalate, then gather).
4. **Simulator.** `IncidentSimulator` (given): Gaussian classes, over-confident logits
   $z = T_{\text{true}}\log p(y\mid x)$; `sample_observation` (given) draws sensor/human outputs from
   pre-drawn uniforms.
5. **Policies.** `simulate_policy` for `threshold`, `always_ask`, `voi`, `voi_guarded` (VOI, but a
   release without human review is replaced by escalation whenever the hazard class is in the
   conformal set). All policies must see the same world (common random numbers).
6. **Evaluation.** `summarize` (mean cost ± SE, hazard release and auto-release rates, false-alarm
   rate, workload, automation rate, mean gathers) and `run_pipeline` (fit / calibrate / test splits).

## API

```python
CLASSES = ("clutter", "benign_item", "hazard_like"); HAZARD = 2
ACTIONS = ("declare_hazard", "declare_benign"); DEFAULT_LOSS (2 x 3); COMMIT, ESCALATE = 0, 1
@dataclass Sensor(name, likelihood (n_obs, K), cost)
@dataclass DecisionProblem(loss, sensors, human, max_gathers);  default_problem()
softmax(z, T=1); log_softmax(z, T=1); nll(z, y, T=1); fit_temperature(z, y) -> T
expected_calibration_error(probs, y, n_bins=15)
conformal_threshold(scores, alpha); min_calibration_size(alpha); lac_scores(probs, y)
fit_conformal(probs, y, alpha=0.1, class_conditional=False, alphas=None) -> q (K,)
prediction_sets(probs, q) -> bool (n, K); coverage(sets, y); class_coverage(sets, y)
commit_losses(B, loss); decision_threshold(loss); obs_probability(B, lik); posterior(B, lik, o)
evpi(B, loss); evsi(B, loss, lik); human_value(B, prob)
q_values(B, prob, gathers_left) -> (n, 2 + n_sensors); value(...); decide(...) -> codes
IncidentSimulator(priors, dim, separation, temperature).sample(n, rng) -> (logits, y)
simulate_policy(policy, B0, y, prob, rng, sets=None) -> {cost, action, gathers, escalated}
summarize(run, y) -> dict;  run_pipeline(sim, prob, n_fit, n_cal, n_test, alpha, alpha_hazard, seed) -> dict
```

## Input / output

| | |
|---|---|
| **Input** | logits and labels (fit, calibration, test splits); loss matrix; sensor likelihoods and costs; human confusion matrix and cost; $\alpha$, per-class $\alpha_k$; gather budget; seed |
| **Output** | $T^*$; conformal thresholds; sets; per-incident decisions and realised costs; per-policy summary (cost, risk, workload, automation, gathers); coverage per class |

## Constraints

- NumPy + SciPy (`minimize_scalar` only); no conformal or decision libraries.
- Vectorised over incidents: the Bellman recursion runs on whole belief batches.
- Deterministic under seed; policies compared with common random numbers.
- Tests < 30 s.

## Expected behaviour

`python projects/p12-hitl-decision/solution/hitl.py` (defaults: priors 0.6/0.3/0.1, $T_{\text{true}}=2.5$,
second look 3 LU, human 30 LU, $\alpha=0.1$, $\alpha_{\text{hazard}}=0.02$, 5,000 test incidents):

| Quantity | Value |
|---|---|
| fitted $T$ | 2.47; test NLL 0.714 → 0.485 |
| conformal coverage (marginal / clutter / benign / hazard) | 0.910 / 0.905 / 0.896 / 0.980; mean set size 1.73 |

| Policy | Mean cost [LU] | Hazard release | False alarm | Workload | Gathers |
|---|---|---|---|---|---|
| threshold only | 14.4 ± 0.8 | 3.4 % | 47.3 % | 0 % | 0 |
| VOI | 10.5 ± 0.7 | 2.6 % | 14.9 % | 0 % | 0.90 |
| VOI + conformal guard | 21.7 ± 0.6 | 1.4 % (auto) | 15.5 % | 41 % | 0.90 |
| always ask | 34.5 ± 0.5 | 1.2 % (0 auto) | 4.3 % | 100 % | 0 |

Read it: the cheap second look is worth far more than its cost because it cuts false alarms by
two-thirds; with these losses the human is never worth 30 LU to the pure expected-loss policy. The
conformal guard buys a *guarantee* (hazard auto-release ≤ $\alpha_h$) at the price of 41 % workload
and double the expected cost — a policy choice (07.1 §3, risk constraint), not an optimisation result.

## Test cases (`tests/test_hitl.py`)

| Test | Checks |
|---|---|
| `test_temperature_scaling_reduces_nll_and_recovers_T`, `test_temperature_fit_on_underconfident_logits` | $T^*\approx T_{\text{true}}$ (±0.2), NLL and ECE fall, argmax unchanged |
| `test_conformal_threshold_hand_case` | `arange(10)/10`, α = 0.2 → 0.8; exact-integer $k$ not rounded up; $n<(1-\alpha)/\alpha$ → inf + warning |
| `test_split_conformal_marginal_coverage` | 200 random splits: mean coverage in $[1-\alpha,\,1-\alpha+\tfrac1{n+1}]$ ± 3 SE |
| `test_class_conditional_coverage_protects_rare_class` | per-class coverage ≥ $1-\alpha_k$ (MC tolerance); beats marginal on the hazard class |
| `test_evpi_evsi_lesson_numbers` | 07.1: EVPI 16.90, EVSI(A) = 0, EVSI(B) = 8.99 LU; $p^*=20/995$ |
| `test_evpi_ge_evsi_ge_zero`, `test_posterior_is_bayes` | $\text{EVPI}\ge\text{EVSI}\ge0$ on random problems; perfect sensor attains EVPI; useless sensor worth 0 |
| `test_bellman_values_consistent`, `test_free_information_is_always_gathered_when_useful` | $V\le$ commit loss; $V$ non-increasing in horizon; $h=0$ without human = one-shot rule; gather chosen only when strictly better |
| `test_voi_never_worse_than_threshold_only` | exact per-incident $V(b)\le\min_a\bar\ell(a)$ and realised mean cost within 2 SE |
| `test_baselines_behave`, `test_conformal_guard_bounds_hazard_auto_release` | workload 0/1 baselines; guarded auto-release ≤ $\alpha_h$ + 3 SE |
| `test_pipeline_reports_calibration`, `test_simulation_deterministic` | end-to-end sanity and reproducibility |

## Milestones

1. Calibration (`nll`, `fit_temperature`) and conformal thresholds; get the coverage tests green.
2. EVPI/EVSI on the lesson's two-state example, then batched posteriors.
3. Bellman `q_values`/`decide`; check $V\le$ commit on random beliefs before simulating.
4. Policy simulator with common random numbers; the guard; the pipeline and the comparison table.

## Extension challenges

- Feed **uncalibrated** beliefs ($T=1$) to the VOI policy and measure the extra realised cost —
  calibration as a decision-quality issue, not a cosmetic one.
- APS/RAPS scores; compare set sizes and the guard's workload.
- Human capacity: a queue with a review budget per hour; escalate only the highest-VOI incidents
  (09.2 programming exercise).
- Correlated second looks (shared nuisance variable) and a POMDP with two sensor types (07.1 §6).
- Distribution shift: calibrate on site A, test on a shifted site B; show the conformal guarantee
  failing and repair it with re-calibration or weighted conformal.

## Hints

<details class="answer"><summary>Hint 1 — robust conformal index</summary>

`k = ceil((n + 1) * (1 - alpha) - 1e-9)`. With $n=24$, $\alpha=0.44$, $(n+1)(1-\alpha)$ is exactly 14,
but `25 * (1 - 0.44)` evaluates to 14.000000000000002 in floating point; without the epsilon you get
$k=15$, a threshold one rank too high and sets that over-cover.

</details>

<details class="answer"><summary>Hint 2 — batched Bellman recursion</summary>

Write `value(B, h)` for a whole `(n, K)` batch: for each sensor and each observation $o$, compute the
posterior batch and recurse with `h - 1`; weight by `obs_probability`. The recursion tree has
$(\text{sensors}\times\text{observations})^h$ calls, each on the full batch — tiny for $h\le3$.

</details>

<details class="answer"><summary>Hint 3 — why VOI can never lose to threshold-only</summary>

"Commit now" is one of the options inside the minimum, so $V(b)\le\min_a\bar\ell_b(a)$ for every
belief. With calibrated beliefs, the expected realised cost of the policy equals $\mathbb E[V(b)]$.
If your simulation shows the opposite, check calibration first, then common random numbers.

</details>

## How to run

```bash
python -m pytest projects/p12-hitl-decision                  # your starter
EOD_SOLUTION=1 python -m pytest projects/p12-hitl-decision   # reference solution
python projects/p12-hitl-decision/solution/hitl.py           # comparison table
```
