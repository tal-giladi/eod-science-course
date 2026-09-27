# Stage 5 assessment · Detection

<div class="module-card">

**Covers** [05.1](lessons/stage-05/lesson-01.md) – [05.7](lessons/stage-05/lesson-07.md) · **Time** ≈ 4 h (problems) + simulator targets · **Pass standard** "Proficient" band (see [assessment plan](curriculum/assessment-plan.md)): correct results with units, justification, and the main unknowns and limits named.

<p class="tags"><span>stage gate</span><span>computation</span><span>interpretation</span><span>design</span><span>Sim C</span><span>Sim J</span></p>
</div>

Work without the lessons open. Show units, and for every number state one thing that could make it
wrong in the field. All objects, compounds and sites are fictional.

## Problem 1 · Operating point, base rate and cost (mathematical)

A detector's scores follow the equal-variance Gaussian model with $d'=2.5$.
(a) At the Neyman–Pearson threshold for $P_{fa}=0.05$, what is $P_d$?
(b) At that operating point, with prevalence $\pi=0.002$ per opportunity, what fraction of alarms is real?
(c) If a miss costs 500 times a false alarm, where is the Bayes-optimal threshold (with $\mu_0=0$, $\sigma=1$), and what are $P_d$ and $P_{fa}$ there?

<details class="answer"><summary>Answer</summary>

(a) $\lambda = Q^{-1}(0.05) = 1.645$; $P_d = Q(1.645-2.5) = Q(-0.855) = 0.804$.
(b) PPV $= 0.804\cdot0.002/(0.804\cdot0.002 + 0.05\cdot0.998) = 0.031$ — about 3 %.
(c) $\eta^* = 0.998/(500\cdot0.002) = 0.998$; $x^* = 1.25 + \ln(0.998)/2.5 = 1.249$;
$P_d = Q(-1.251) = 0.894$, $P_{fa} = Q(1.249) = 0.106$. At this prior and cost ratio the Bayes
point lies close to the midpoint threshold, because $C_M\pi \approx C_{FA}(1-\pi)$.

</details>

## Problem 2 · Reading a trial report (interpretation + statistics)

A blind trial reports 236 detections in 240 target encounters and 30 false alarms on 400 m² of
target-free lane. (a) Give 95 % intervals for $P_d$ (Clopper–Pearson) and FAR (Poisson).
(b) The customer requires $P_d \ge 0.995$. How many targets, all detected, would be needed to
demonstrate it at 95 % confidence? (c) Name two trial-design weaknesses that the headline numbers
could hide.

<details class="answer"><summary>Answer</summary>

(a) $P_d \in [0.958, 0.995]$; FAR $= 0.075$ m⁻², 95 % CI $[0.051, 0.107]$ m⁻².
(b) $n \ge \ln 0.05/\ln 0.995 = 597.6 \Rightarrow 598$.
(c) Any two of: pooling across target types, depths or soils (Simpson-type masking); repeated
passes over the same targets treated as independent; operators not truly blind; FAR measured on a
cleaner lane than the deployment area; no temperature or moisture stratification.

</details>

## Problem 3 · Induction physics (computation)

(a) Compute the slowest eddy-current decay constant of fictional 3 mm-radius spheres of aluminium
($\sigma = 3.5\times10^7$ S/m) and stainless steel ($\sigma = 1.4\times10^6$ S/m).
(b) A pulse-induction detector's first sample is at 10 µs. What fraction of each sphere's signal remains?
(c) In the far field, by what factor does the received signal fall if the burial depth doubles from 8 to 16 cm?
(d) Explain why the steel sphere is the harder target even at equal depth, and why a magnetically
viscous soil makes it harder still.

<details class="answer"><summary>Answer</summary>

(a) $\tau = \mu_0\sigma a^2/\pi^2$: Al 40.1 µs; stainless 1.60 µs.
(b) Al $e^{-10/40.1} = 0.78$; stainless $e^{-10/1.60} = 0.0019$.
(c) $2^6 = 64$ (far-field $z^{-6}$; less in the near field where $z \sim$ coil radius).
(d) Its signal has almost gone by the first sample. The early-time window is where soil ($1/t$
viscous decay) and switch-off transients dominate. Raising gain to recover it also admits every
larger metal fragment as a false alarm.

</details>

## Problem 4 · GPR hyperbola (interpretation + computation)

Picked apex-region points from a B-scan (x in m, t in ns): (0.0, 7.21), (0.1, 6.32), (0.2, 6.00),
(0.3, 6.32), (0.4, 7.21). (a) Estimate $x_0$, $v$, $\varepsilon_r$ and depth. (b) With a 1.5 GHz
antenna, what is the $\lambda/4$ depth resolution in this soil? (c) The same site after heavy rain
shows the apex at 9.0 ns. Assuming the object has not moved, what is the new $\varepsilon_r$, and what
would you expect to happen to the soil's attenuation?

<details class="answer"><summary>Answer</summary>

(a) Symmetry gives $x_0 = 0.2$ m and $t_0 = 6.00$ ns. From the 0.2 m offset:
$c = (7.21^2-36)/0.04 = 399.6$ ns²/m², so $v = 2/\sqrt{c} = 0.100$ m/ns and
$\varepsilon_r = (0.2998/0.100)^2 = 9.0$. Depth $d = v t_0/2 = 0.30$ m.
(b) $\lambda = 0.100/1.5 = 0.0667$ m; $\lambda/4 = 1.7$ cm.
(c) $v = 2(0.30)/9.0 = 0.0667$ m/ns, so $\varepsilon_r = 20.2$. Wetter soil usually has higher
conductivity. Attenuation ($\propto \sigma/\sqrt{\varepsilon_r}$) typically rises, and the stronger
surface reflection adds clutter.

</details>

## Problem 5 · Dual energy and dose (interpretation + computation)

(a) An idealised dual-energy pixel shows $T_L = 0.30$ and $T_H = 0.45$. With reference ratios water
1.21, aluminium 1.63 and iron 3.24, what can and cannot be concluded?
(b) A fictional generator delivers 25 µSv per exposure at 1 m. Twelve exposures are planned. What
dose does an operator receive at 6 m? What unshielded distance keeps the total below 2 µSv?
(c) Give one reason why "stand further back" and "use fewer photons" are not interchangeable
dose-reduction strategies.

<details class="answer"><summary>Answer</summary>

(a) $R = \ln 0.30/\ln 0.45 = 1.51$. This lies between the water-like and aluminium-like classes.
It is consistent with a light inorganic material, and equally with an organic/metal overlap on the
same ray. One ratio cannot separate two unknown thicknesses; more views (CT) or more energy bins are
needed.
(b) $12\times25/36 = 8.3$ µSv. For ≤ 2 µSv: $r \ge \sqrt{300/2} = 12.2$ m.
(c) Distance reduces the *operator's* dose without changing the image. Fewer photons reduce the
object's exposure *and* the image quality: CNR scales as $\sqrt{N_0}$, so detectability degrades.

</details>

## Problem 6 · Trace detection (computation + interpretation)

An IMS runs at 110 °C and 101.3 kPa with $L = 7$ cm and $E = 250$ V/cm. A calibrant with
$K_0 = 1.80$ cm²/(V s) appears at 11.09 ms. (a) A peak appears at 13.31 ms; what is its $K_0$?
(b) A fictional interferent has $K_0 = 1.46$. At resolving power 30, is it resolved from the
peak in (a)? (c) The operator proposes raising the detection threshold from $4\sigma$ to $6\sigma$ to
stop the interferent alarms. Evaluate the proposal. (d) A fictional compound has
$\Delta H_{sub} = 110$ kJ/mol. By what factor does its equilibrium vapour change between 30 °C and
10 °C?

<details class="answer"><summary>Answer</summary>

(a) $K_0 = 1.80\times11.09/13.31 = 1.50$ cm²/(V s).
(b) $t_d(1.46) = 13.31\times1.50/1.46 = 13.67$ ms, a separation of 0.36 ms. The FWHM at $R = 30$
is $13.31/30 = 0.44$ ms, larger than the separation, so the peaks are **not** resolved.
(c) It will not work. The interferent produces a real peak comparable to a target peak, so a higher
threshold mainly costs $P_d$ on weak targets. What helps is resolution (higher $R$, dopants, a
second polarity), an orthogonal method such as MS, or confirmatory sampling.
(d) $\exp\!\big(110\,000/8.314\,(1/283.15 - 1/303.15)\big) = e^{3.08} \approx 22$: about 22× less vapour at 10 °C.

</details>

## Problem 7 · Combining two sensors (previews 05.6)

An EMI detector has $P_d = 0.98$, $P_{fa} = 0.20$ per cell. A GPR has $P_d = 0.90$, $P_{fa} = 0.10$.
(a) Assuming conditional independence, compute $P_d$ and $P_{fa}$ for the AND rule (alarm if both
alarm) and the OR rule (alarm if either alarms). (b) Which rule fits a humanitarian requirement, and
what does it cost? (c) Give a physical reason why the independence assumption may fail for false
alarms, and say which way the failure biases the AND-rule $P_{fa}$.

<details class="answer"><summary>Answer</summary>

(a) AND: $P_d = 0.882$, $P_{fa} = 0.020$. OR: $P_d = 0.998$, $P_{fa} = 0.28$.
(b) Neither rule is good enough on its own. AND loses about 10 % of targets, which is unacceptable.
OR keeps $P_d$ but raises false alarms by 40 % over EMI alone. Likelihood-ratio fusion of the
*scores*, rather than the binary decisions, generally dominates both (05.6).
(c) Some clutter excites both sensors, for example a metal fragment in a disturbed-soil pocket.
Positively correlated false alarms make the true AND-rule $P_{fa}$ **higher** than the independent
product of 0.02.

</details>

## Problem 8 · Design: sensor suite for a fictional clearance task (system design)

A fictional 5 ha agricultural site in a seasonally wet, iron-rich lateritic region is suspected to
contain legacy low-metal-content hazards and abundant metal scrap from past fighting. Survey
suggests about 40 items, concentrated along two former field boundaries. The client requires
demonstrated $P_d \ge 0.99$, and the budget covers about 1500 team-hours.

Write a one-page design that:
1. selects sensors (and deployment: handheld, vehicle, UAV, animal) and justifies each from its
   physics and its false-positive and false-negative mechanisms in *this* soil and season;
2. estimates the false-alarm burden and investigation hours for your chosen operating point, using
   stated assumptions for $d'$ or $P_{fa}$ and time per alarm;
3. shows how survey (raising $\pi$ along the boundaries) changes PPV and total effort;
4. specifies a blind verification trial (targets, strata, sample size) that could demonstrate the
   requirement;
5. names the two failure modes you consider most likely, and the evidence that would reveal them.

<details class="answer"><summary>What a proficient answer contains</summary>

- EMI chosen with explicit ground-compensation reasoning for viscous lateritic soil. Its weakness on
  low-metal targets is acknowledged, and GPR (or another non-metal modality) is added for
  discrimination. The wet-season GPR attenuation and surface clutter are quantified with $\alpha$
  and $v$.
- A numerical false-alarm budget, for example $P_{fa}$ per m² × area × minutes per alarm, compared
  with 1500 h, showing that blanket clearance at the required $P_d$ probably does not fit. Survey
  and land release (05.7) are used to focus the effort.
- PPV recomputed for the boundary strips against the rest of the site.
- A trial with per-stratum targets (soil state × target class × depth). About 300 per stratum are
  needed for 99 % with zero misses, which forces a choice of which strata really matter. Paired
  designs for detector comparison.
- Failure modes such as seasonal soil change (domain shift), operator fatigue under high false-alarm
  load, or correlated clutter reducing fusion gains, each paired with a monitoring metric.

</details>

## Simulator targets

<div class="callout sim">

- **Sim J** — in clearance mode, find the cost-minimising operating point for three prevalence and
  cost settings, each within 2 % of the minimum. Then find the operating point that meets
  $P_d \ge 0.99$ and report its investigation-hours per hectare.
- **Sim C** — reach the "proficient" band at Advanced difficulty: declare all cells with a
  calibrated posterior, using no more than the sensor budget, and write a debrief explaining one
  case where a sensor's false alarm was correctly overridden.

</div>

<a class="sim-link" href="sims/detection-theory/index.html" target="_blank">Open Sim J ↗</a> ·
<a class="sim-link" href="sims/sensor-fusion/index.html" target="_blank">Open Sim C ↗</a>

Back to the [Stage 5 overview](lessons/stage-05/README.md).
