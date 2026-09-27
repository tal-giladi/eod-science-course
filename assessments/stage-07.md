# Stage 7 gate · EOD decision-making

Covers [07.1](lessons/stage-07/lesson-01.md) and [07.2](lessons/stage-07/lesson-02.md). Work
without the lessons open; show units, state assumptions, and say what your answer *cannot* tell
you. All incidents, numbers and items are fictional; losses are in loss units (LU) and yields in
abstract yield units (YU).

<div class="callout boundary">

This gate assesses reasoning about information, risk and organisation. No question asks — and no
answer should contain — anything about how an item is approached, diagnosed or dealt with.

</div>

## Problem 1 · Value of information (mathematical)

A fictional call class has base rate $P(H)=0.04$. Loss matrix (rows: actions, columns: states
benign $B$ / hazardous $H$):

| $\ell$ [LU] | $B$ | $H$ |
|---|---|---|
| full response F | 30 | 35 |
| release R | 0 | 1500 |

(a) Compute $p^{*}$ and the optimal action. (b) Compute EVPI. (c) An information action has
$P_d=0.95$, $P_{fa}=0.25$ and costs 5 LU. Compute its EVSI and decide whether to use it.
(d) Explain in one sentence why the answer to (c) would change if $P_d$ were 0.90.

<details class="answer"><summary>Answer — then reveal</summary>

(a) $p^{*} = 30/(30+1465) = 0.0201$; $p=0.04>p^{*}$ → F. $\bar\ell(F) = 30+5\cdot0.04 = 30.2$,
$\bar\ell(R)=60$.
(b) $\mathcal L_{\text{PI}} = 0.04\cdot35 = 1.4$ → EVPI $= 28.8$ LU.
(c) $P(+) = 0.95\cdot0.04 + 0.25\cdot0.96 = 0.038+0.24=0.278$; $P(H\mid+) = 0.1367$;
$P(H\mid-) = 0.002/0.722 = 0.00277 < p^{*}$ → release on negative.
$\mathcal L_{\text{SI}} = 0.278\cdot(30+5\cdot0.1367) + 0.722\cdot(1500\cdot0.00277) = 0.278\cdot30.68 + 0.722\cdot4.155 = 8.53+3.00 = 11.53$.
EVSI $= 30.2-11.53 = 18.67$ LU $>5$ → use it (net 13.7 LU).
(d) With $P_d=0.90$: $P(H\mid-) = 0.004/(0.004+0.72) = 0.0055$ — still below $p^{*}$, so it
would *not* change in kind; EVSI falls to ≈ 15.7 LU. It would change only once
$P(H\mid-)$ exceeded 0.0201, i.e. for $P_d < 0.64$ approximately — the point is to check
threshold crossing, not ROC quality.

</details>

## Problem 2 · Cordon under uncertainty (mathematical + interpretation)

Illustrative threshold 7 kPa ($Z_{\text{th}} = 13.3$ m YU⁻¹ᐟ³, free air). Yield belief lognormal,
$W_{50}=10$ YU, $\sigma=0.8$. (a) Compute $R$ for $\alpha=0.01$. (b) New imagery narrows the belief
to $W_{50}=6$ YU, $\sigma=0.4$. Recompute and give the fractional reduction in cordon *area*.
(c) Name two hazards that could make both radii irrelevant, and where the governing number
should come from.

<details class="answer"><summary>Answer — then reveal</summary>

(a) $W_{0.99}=10e^{0.8\cdot2.326}=64.3$; $R=13.3\cdot4.006=53.2$ m.
(b) $W_{0.99}=6e^{0.4\cdot2.326}=15.2$; $R=13.3\cdot2.478=33.0$ m. Area ratio
$(33.0/53.2)^2=0.383$ → 62 % reduction.
(c) Fragments (density $\propto R^{-2}$, often governing) and glazing failure beyond the blast
radius; also channelling in streets. The governing distances come from published stand-off
tables and doctrine for the identified class; the calculation explains their structure.

</details>

## Problem 3 · Belief-state policy (programming + conceptual)

Using the 07.1 simulation (loss matrix of 07.1, sensor $P_d=0.85$, $P_{fa}=0.15$, 1 LU per look),
(a) explain why the myopic rule never looks at the prior 0.155; (b) modify the code so the
hazard can *change state* during the incident (with probability 0.02 per look a benign situation
becomes hazardous — e.g. a second item is placed), updating the belief with a transition
$T$ before each observation; (c) report how the optimal mean number of looks and the mean loss
change, and explain why.

<details class="answer"><summary>Answer — then reveal</summary>

(a) After one observation the belief is either ≈ 0.51 or ≈ 0.031; both exceed $p^{*}=0.0201$, so
the action does not change and one-step EVSI $=0 < 1$. Two or more negatives can cross the
threshold, which only non-myopic lookahead sees.
(b) Predict step $b \leftarrow b + 0.02(1-b)$ before each Bayes update; the belief index is no
longer an integer count, so use a belief grid (e.g. 2001 points with interpolation) for the
Bellman recursion.
(c) The belief is pushed up every step, so long look sequences can never drive it far below
$p^{*}$: the looking band shrinks, the optimal number of looks falls, and the mean loss rises.
In a non-stationary world, information decays — commit earlier, and protect against the
possibility you cannot rule out.

</details>

## Problem 4 · Decision-log critique (case question)

Read this fictional log from an unattended-item incident at a stadium exit.

> 18:02 Report of a rucksack by gate 4; steward says "probably forgotten". Cordon 30 m.
> 18:10 Standoff sensor inconclusive. Crowd leaving through gates 3 and 5 as normal.
> 18:18 Second report, a similar bag at gate 9. Logged.
> 18:25 Control point established at the main car-park entrance (usual location).
> 18:40 Robot delayed by crowd. "We've set everything up for this plan; continue."
> 19:05 Item assessed as benign; scene released. Gate 9 bag found to be benign at 19:30.

(a) Identify at least four reasoning errors, naming the bias or principle each violates.
(b) Rewrite the 18:18 and 18:25 entries as they should have read, including an explicit decision
trigger. (c) Explain why the benign outcome does not vindicate the log.

<details class="answer"><summary>Answer — then reveal</summary>

(a) Anchoring on the steward's frame (18:02); 30 m cordon apparently from habit, not a
tolerance-quantile or a published table, with crowds passing adjacent gates (exposure,
07.2 §1–3); "inconclusive" not converted into a belief or VOI decision (07.1 §4); second report
merely "logged" — a hypothesis-space change ignored (secondary hazards, 07.2 §6); control point at
a habitual location — responder exposure not considered; 18:40 sunk-cost and plan-continuation
reasoning; no escalation or re-plan criterion recorded.
(b) "18:18 Second similar item at gate 9 → TRIGGER: re-plan both cordons, halt egress via gates
3/5/9, reassess control-point location, notify command of possible coordinated or hoax pattern;
consider escalation per criteria." "18:25 Control point selected at a location checked and
shielded from both items, not the usual entrance; rationale recorded."
(c) Outcome bias: decisions must be judged on the belief and information available at the time.
With $p$ above threshold and a second report, the exposure accepted was not justified; a benign
outcome is what happens most of the time even with poor decisions (07.1 §3).

</details>

## Simulator target

- **Sim F · Incident Command** — complete an *Expert* scenario at "Proficient" band or better
  (≥ 70) on *information quality*, *uncertainty reduction* and *recognition of unknowns*, with the
  escalation trigger you wrote down beforehand recorded in your log.
- **Sim A · Scene Assessment** — complete an *Expert* scene with the *Avoiding exposure* score in
  the Proficient band (in practice: no person sent forward) and the control point searched, so
  that any secondary item is found.

Record both debriefs; for each, write three sentences: what you would decide differently, which
information action had the highest value, and which trigger you set that fired (or should have).

## Self-assessment rubric

| Band | Evidence |
|---|---|
| Novice | computes posteriors but cannot say when information is worthless |
| Developing | correct VOI numbers; cordon from median; treats second reports as updates, not model changes |
| Proficient | threshold-crossing reasoning, tolerance quantiles, explicit triggers, critiques logs without outcome bias |
| Expert | quantifies sensitivity to value judgements, handles non-stationarity, designs decision support that respects command/technical split |
