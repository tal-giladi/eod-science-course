# Stage 4 assessment · Blast effects

<div class="module-card">

**Covers** [04.1](lessons/stage-04/lesson-01.md) · [04.2](lessons/stage-04/lesson-02.md) · [04.3](lessons/stage-04/lesson-03.md) · [04.4](lessons/stage-04/lesson-04.md) · **Time** 4–5 h · **Allowed** Python (your P01 library), Sim D, no lesson notes for problems 1–5.

**Pass standard** "Proficient" band ([assessment plan](curriculum/assessment-plan.md)): correct results *with* unit and sanity checks, main uncertainties named, and every assumption stated.

</div>

All scenarios are fictional; yields are abstract yield units (YU); Kinney–Graham free-air fits,
γ = 1.4, sea level ($p_0 = 101.325$ kPa, $a_0 = 340.3$ m/s) unless stated. Answers are hidden —
commit to yours first.

## Problem 1 · Friedlander waveform (mathematical)

A side-on record has $p_s = 120$ kPa, $t_d = 4.0$ ms and positive impulse $i_s = 180$ kPa·ms.
(a) Find the waveform coefficient $b$. (b) Using the extended Friedlander form, find the time and
value of the minimum pressure in the negative phase. (c) State one reason why (b) should not be
trusted quantitatively.

<details class="answer"><summary>Answer</summary>

(a) $\phi = 180/(120\times4) = 0.375$ ⇒ solving $1/b - (1-e^{-b})/b^2 = 0.375$ gives $b = 0.932$.
(b) Minimum at $\tau = 1 + 1/b = 2.07$ ⇒ $t = 8.3$ ms after arrival; $p_{\min} = -(p_s/b)e^{-(1+b)} = -18.6$ kPa.
(c) The positive-phase fit form was never constrained by negative-phase data; Rigby et al. (2014)
show the naive extension misrepresents the negative phase, so a dedicated negative-phase model or
measurement is needed.

</details>

## Problem 2 · Scaling and arrival time (mathematical)

For a free-air release of 27 YU, a gauge at 9 m records $t_a = 11.8$ ms and $t_d = 5.36$ ms (Sim D
values). (a) Without any fit evaluation, predict $Z$, $p_s$-equivalence and $(t_a, t_d)$ for a
216 YU release at 18 m. (b) Compute the average shock speed between the source and the gauge and
compare it with the speed at the gauge. What does the difference tell you?

<details class="answer"><summary>Answer</summary>

(a) $Z = 9/3 = 18/6 = 3$ in both cases ⇒ same $p_s$ (82.3 kPa); times scale by $6/3 = 2$:
$t_a = 23.5$ ms, $t_d = 10.7$ ms (Sim D reports 23.5 ms and, with its $b$-floor convention,
10.7 ms). (b) Mean speed $9/0.0118 = 763$ m/s vs local $U = a_0\sqrt{1+\tfrac67\cdot0.813} = 1.303\times340.3 = 443$ m/s.
The front decelerated strongly: most of the "time saved" relative to sound ($9/340.3 = 26.4$ ms)
was gained in the near field.

</details>

## Problem 3 · Inferring an equivalent yield from gauges (interpretation + computation)

Three side-on gauges on a fictional test range record peaks of 58.3, 14.1 and 6.5 kPa at 10, 20
and 40 m (free air). (a) Estimate $W$ from each gauge separately. (b) Estimate $W$ by least squares
in log-pressure. (c) Explain why the single-gauge estimates scatter so much more than the gauge
errors (≤ 10 %).

<details class="answer"><summary>Answer</summary>

(a) Invert the fit for $Z$ at each peak, then $W = (R/Z)^3$: 22.9, 16.8, 22.7 YU.
(b) Minimising $\sum(\ln p_{\text{obs}} - \ln p_{\text{fit}}(R/W^{1/3}))^2$ gives $W \approx 21.0$ YU
(the data were generated from 20 YU with ±10 % errors).
(c) $\delta W/W \approx 3\epsilon_p/n$ with $n\approx2.1$ (at $Z\approx3.6$) down to ≈ 1.2 (at
$Z\approx14.5$): a 10 % pressure error becomes a 14–25 % yield error. Far-field gauges ($n\to1$)
amplify most.

</details>

## Problem 4 · Confinement and venting (mathematical)

A fictional 80 m³ room contains a 2 YU release (fictional $\kappa_Y = 25$ m³/YU). Vents: 2 m²,
$C_d = 0.6$; vented gas sound speed 500 m/s. A wall of the room has natural period 30 ms.
(a) Ideal quasi-static overpressure. (b) Blow-down time constant and gas-phase impulse. (c) Regime
of the wall under the gas load and the approximate effective static load for design.

<details class="answer"><summary>Answer</summary>

(a) $\Delta p_{qs}/p_0 = 0.4\times25\times2/80 = 0.25$ ⇒ 25.3 kPa (upper bound). (b)
$\tau_v = 80/(0.6\times2\times500) = 133$ ms; $i_{qs}\approx 25.3\times133 = 3380$ kPa·ms.
(c) $\omega\tau_v = (2\pi/0.030)\times0.133 = 27.9$ — effectively quasi-static; a rapidly applied,
slowly decaying load gives a DLF approaching 2 ⇒ effective static ≈ 50 kPa (slightly less
because of the decay). The shock phase must be checked separately (impulsive regime).

</details>

## Problem 5 · P–I assessment of a wall (mathematical + interpretation)

A fictional EPP wall panel: $m = 150$ kg/m², $R_u = 30$ kPa, $x_e = 4$ mm, allowable ductility
$\mu = 4$. A predicted face-on load: $p_r = 60$ kPa, reflected impulse 250 kPa·ms, $t_d = 8$ ms.
(a) Compute $P^*$, $I^*$, the natural period and $\omega t_d$. (b) Is the allowable ductility
exceeded? Justify *without* running an SDOF solver. (c) What would you do if the answer were
borderline?

<details class="answer"><summary>Answer</summary>

(a) $P^* = 30(1 - 1/8) = 26.3$ kPa; $I^* = \sqrt{2\cdot150\cdot30\,000\cdot0.004\cdot3.5} = 355$ kPa·ms;
$k = R_u/x_e = 7.5\times10^6$ Pa/m ⇒ $T = 28.1$ ms; $\omega t_d = 1.79$ (dynamic).
(b) The iso-damage curve lies above and to the right of both asymptotes. The load impulse (250) is
*below* $I^*$ (355), so the load point is left of the curve regardless of its pressure ⇒ not
exceeded. (c) Run the SDOF with the actual Friedlander pulse; propagate uncertainty in $R_u$ and
$m$ (probabilistic P–I, 04.3 programming exercise); check direct shear separately.

</details>

## Problem 6 · Evacuation radius under uncertainty (programming)

Adapt your 04.4 Monte Carlo: yield median 10 YU with $\sigma_{\ln W} = 0.8$, surface burst
($\alpha = 1.8$), fit error $\sigma_{\ln p} = 0.25$, fictional threshold 5 kPa, exceedance target 1 %.
(a) Report $R_{50}$ (median yield, no fit error), $R_{99}$ with yield uncertainty only (analytic and
MC), and $R_{99}$ with both uncertainties (MC, seed 42, $2\times10^5$ samples). (b) Which
uncertainty would you spend effort reducing, and how would you estimate the value of doing so?

<details class="answer"><summary>Answer</summary>

(a) $Z^*(5) = 17.79$. $R_{50} = 17.79\times18^{1/3} = 46.6$ m. Yield only: $W_{99} = 10e^{2.326\times0.8} = 64.3$ YU
⇒ $R_{99} = 17.79\times(1.8\times64.3)^{1/3} = 86.7$ m (MC 87.1 m). Both: ≈ 105.8 m.
(b) Yield uncertainty dominates ($n\sigma_{\ln W}/3 \approx 0.30$ vs $\sigma_{\ln p} = 0.25$ in log-pressure
terms, and it is the one information-gathering can reduce). Value of information: compare the
expected cost (evacuation cost ∝ area $\propto R^2$ plus exceedance harm) with and without a
measurement that shrinks $\sigma_{\ln W}$ — the formal treatment is in [07.1](lessons/stage-07/lesson-01.md).

</details>

## Problem 7 · Quantity-distance (interpretation)

Fictional Regulation F: inter-store $K = 3$, inhabited building $K = 18$ m·YU⁻¹ᐟ³. Two stores
(150 YU and 400 YU) are 15 m apart; the nearest house is 140 m away. (a) Are the stores separated
by the inter-store distance? (b) What quantity must be used for the house distance, and is the
house compliant? (c) Propose two compliant changes.

<details class="answer"><summary>Answer</summary>

(a) Required $3\times400^{1/3} = 22.1$ m (governed by the larger store) > 15 m ⇒ not separated; an
event in one could propagate to the other.
(b) The quantities must be aggregated: 550 YU ⇒ $18\times550^{1/3} = 147.5$ m > 140 m ⇒ **not
compliant**. (If the stores were properly separated, the 400 YU store alone would need 132.6 m ⇒
compliant.)
(c) Increase store separation to ≥ 22.1 m (or add an approved barrier where the regulation allows a
reduced separation), or reduce total quantity to $\le (140/18)^3 = 470$ YU.

</details>

## Problem 8 · Protective-design critique of a fictional building (design)

"Harbour House" (fictional) is a five-storey reinforced-concrete office on a city street:

- fully glazed ground-floor atrium façade of annealed glass, 8 m from the kerb, no vehicle barriers;
- a transfer girder at level 2 carries four upper-storey columns over the atrium;
- the designated staff shelter area during alerts is the atrium lounge;
- a gas main enters the basement plant room below the atrium;
- the side street is a 9 m wide canyon between the building and a car park structure.

Write a one-page critique (≤ 400 words) identifying the hazards in priority order, the physics
behind each (cite the lesson section), and the most cost-effective mitigation for each, following
the "standoff first" philosophy. State what you would need to know to quantify the risk.

<details class="answer"><summary>Rubric (what a proficient answer contains)</summary>

- **Standoff:** 8 m with no barriers is the governing weakness; near-field load falls as $Z^{-2}$ or
  faster (04.1), so vehicle exclusion/bollards give the largest risk reduction per unit cost (04.3 §6).
- **Glazing:** annealed atrium glass fails at very low loads and long ranges (04.3 §1); secondary
  injury dominates for occupants (04.4 §1). Mitigate with laminated glazing or film plus anchored,
  balanced frames.
- **Shelter location:** the atrium is the worst shelter choice (facing glass, near façade). Move it
  to an interior core behind masonry/concrete walls away from the street side.
- **Progressive collapse:** the level-2 transfer girder is a single point of failure over the most
  exposed bay (04.3 §5, Oklahoma City). Provide alternate load paths/ties or protect the supporting
  columns; at minimum, assess column-loss scenarios.
- **Gas main:** secondary hazard — rupture could produce a subsequent confined gas explosion in the
  basement (04.2 §5, 04.4 §7); isolation valves and plant-room venting.
- **Side-street canyon:** channelling raises along-street loads (04.2 §7) and affects the car park
  and the building's side façade; include it in any cordon or design-basis assessment.
- **Needed information:** design-basis threat band (in YU) with its uncertainty, glazing and frame
  specifications, structural drawings (reinforcement continuity), occupancy, and a CFD or
  specialist assessment of the street geometry.
- **Expert-level additions:** quantified P–I checks for glazing and the transfer-girder columns;
  probability of exceedance vs standoff (04.3/04.4 programming exercises); explicit statement of
  what the SDOF models cannot capture (close-in shear, breaching).

</details>

## Simulator target

<div class="callout sim">

**Sim D challenge set at Advanced** (equations hidden): ≥ 4 of 5 within tolerance on two different
seeds, followed by a written debrief of any miss (which formula, which assumption). Then run the
*Room* and *Street canyon* scenes and submit a probe experiment (positions, predicted vs observed
peak and impulse ratios relative to *Open field*, and an explanation).

</div>

## Self-assessment

| Band | Evidence |
|---|---|
| Novice | Problems 1–2 correct only with notes; uncertainty not mentioned |
| Developing | 1–5 correct; 6–8 incomplete or without uncertainty |
| Proficient | all problems correct with stated assumptions; critique covers every item in the rubric |
| Expert | also quantifies uncertainty in 3–5, proposes a measurement plan that would reduce the dominant uncertainty, and identifies the limits of SDOF/P–I and of the Monte Carlo model |

Next: [Stage 5 · Detection](lessons/stage-05/README.md).
