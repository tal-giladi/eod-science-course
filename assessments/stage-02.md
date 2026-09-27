# Stage 2 assessment · Chemistry & energetic materials (science)

Covers [02.1](lessons/stage-02/lesson-01.md), [02.2](lessons/stage-02/lesson-02.md) and
[02.3](lessons/stage-02/lesson-03.md). Target: solve every problem without looking back at the
lessons, and be able to explain every step, including units and a sanity check. All materials are
either ordinary fuels or explicitly **fictional**. Python (NumPy/SciPy) is allowed and expected.

Suggested time: 2–3 h. Rubric bands are those of the [assessment plan](curriculum/assessment-plan.md):
*proficient* means correct answers with justification and the main unknowns identified; *expert*
also quantifies uncertainty and proposes a better experiment or model.

---

## Problem 1 — Thermochemistry (mathematical)

Butane burns as $\mathrm{C_4H_{10} + 6.5\,O_2 \to 4\,CO_2 + 5\,H_2O}$. Take
$\Delta_f H^\circ(\mathrm{C_4H_{10}}) = -125.7$ kJ/mol and the formation enthalpies from 02.1.

(a) Compute the lower heating value in kJ/mol and MJ/kg of fuel.
(b) Compute the energy per kg of stoichiometric butane–air mixture (air = O₂ + 3.76 N₂).
(c) Check the result against Thornton's rule and state, in one sentence, why hydrocarbon–air
mixtures all land near the same value.

<details class="answer"><summary>Answer 1</summary>

(a) $\Delta H = 4(-393.51) + 5(-241.82) - (-125.7) = -2657.4$ kJ/mol; LHV = 2657.4/58.12 = **45.7 MJ/kg**.
(b) Mixture mass per mol fuel: $58.12 + 6.5(32.00 + 3.76\times28.01) = 950.8$ g ⇒ 2657.4/0.9508 =
**2.80 MJ/kg of mixture**.
(c) Per mol O₂: 2657.4/6.5 = 409 kJ — inside the ≈ 400–420 kJ band. The energy is essentially a
property of the oxygen consumed, and air carries a fixed fraction of oxygen, so every hydrocarbon–air
mixture yields ≈ 2.8 MJ/kg.

</details>

## Problem 2 — Kinetics and power (mathematical + conceptual)

A fictional slow decomposition has $E_a = 80$ kJ/mol.

(a) By what factor does its rate increase when a warehouse warms from 20 °C to 40 °C?
(b) What activation energy would make the "doubles every 10 K" rule exact over that interval?
(c) A colleague argues that because this material stores only a quarter of the energy per kilogram
of diesel fuel, it is "less hazardous than diesel". Give the counter-argument in terms of power, and
say what additional information you would need to rank the two hazards.

<details class="answer"><summary>Answer 2</summary>

(a) $\exp[80\,000/8.3145\,(1/293.15 - 1/313.15)] = e^{2.096} = $ **8.1**.
(b) Factor 4 over 20 K: $E_a = R_u\ln4/(1/293.15 - 1/313.15) = 8.3145\times1.386/2.179\times10^{-4}
\approx 52.9$ kJ/mol (same as 02.1's 298→308 K value to within rounding, because $T^2$ barely changes).
(c) Hazard depends on the *rate* at which energy is released relative to the time the surroundings
need to relieve pressure (acoustic time) or remove heat. Diesel needs atmospheric oxygen and burns
at a rate limited by evaporation and mixing; a material that decomposes without external oxygen can,
in principle, release its energy far faster. Needed: the propagation mode (does it burn, deflagrate
or detonate, 02.2), its hazard division (02.3), quantity and confinement.

</details>

## Problem 3 — Chapman–Jouguet (mathematical)

Fictional ideal-gas mixture H: $\gamma = 1.25$ (reactants and products), $W = 0.025$ kg/mol,
$q = 2.5$ MJ/kg, $T_1 = 300$ K, $p_1 = 100$ kPa.

(a) Compute $a_1$, $\mathcal H$, $M_{CJ}$, $D_{CJ}$.
(b) Compute $p_{CJ}$, $\rho_{CJ}/\rho_1$, $T_{CJ}$ and verify the sonic condition numerically.
(c) Compute the von Neumann spike pressure and temperature.
(d) How good is the strong-detonation approximation here?

<details class="answer"><summary>Answer 3</summary>

(a) $R = 8.3145/0.025 = 332.6$ J/(kg K); $a_1 = \sqrt{1.25\cdot332.6\cdot300} = 353.2$ m/s;
$\mathcal H = (1.5625-1)(2.5\times10^6)/(2\cdot353.2^2) = 5.638$;
$M_{CJ} = \sqrt{6.638}+\sqrt{5.638} = 4.951$; $D_{CJ} = $ **1748 m/s**.
(b) $p_{CJ} = 100(1 + 1.25\cdot24.51)/2.25 = $ **1.41 MPa** (14.1 $p_1$); $\rho_{CJ}/\rho_1 = 1.743$;
$\rho_1 = 1.002$ kg/m³ ⇒ $T_{CJ} = p/(\rho R) = $ **2420 K**; $u_{CJ} = 745$ m/s,
$a_{CJ} = 1003$ m/s, $u + a = 1748$ m/s ✓.
(c) $p_{vN} = 100[1 + \frac{2.5}{2.25}(24.51 - 1)] = $ **2.71 MPa**; $T_{vN} \approx 1199$ K.
(d) $\sqrt{2(\gamma^2-1)q} = 1677$ m/s — 4 % low; $\mathcal H \approx 5.6$ is not yet "strong".

</details>

## Problem 4 — Interpretation: what kind of event? (interpretation)

In a long (fictional) duct filled with mixture H, two pressure gauges 2.00 m apart record:

- **Test A:** fronts 1.14 ms apart; each trace shows a µs rise to ≈ 2.7 MPa followed within
  tens of µs by a plateau near 1.4 MPa, then a slow decay.
- **Test B:** fronts 0.30 s apart; each trace shows a smooth rise over ≈ 50 ms to ≈ 0.2 bar
  overpressure.

Classify each test, name the features in the traces, and state one thing each record *cannot*
tell you.

<details class="answer"><summary>Answer 4</summary>

**A:** $D = 2.00/0.00114 = 1754$ m/s ≈ $D_{CJ} = 1748$ m/s (within timing error): a CJ detonation.
The spike ≈ $p_{vN}$ (2.71 MPa), the plateau ≈ $p_{CJ}$ (1.41 MPa), then the Taylor expansion. It
cannot tell you the induction length or cell size directly (gauge rise time and size smear the
µs-scale structure), nor whether the wave was slightly overdriven earlier.
**B:** 6.7 m/s, ms rise, sub-bar: a (possibly turbulent) deflagration with quasi-static pressure
build-up. It cannot tell you the local burning velocity without knowing the flow ahead of the flame
(the lab-frame speed includes the expansion-driven flow, $\sigma S$), nor whether the flame was
accelerating towards DDT further down the duct.

</details>

## Problem 5 — Sensitivity statistics (mathematical + interpretation)

An up-and-down series on a fictional material, step $d = 1$ SU, gives the less frequent outcome
(no-go) at levels 20, 21, 22 SU with counts 3, 6, 2.

(a) Compute the Dixon–Mood $\hat\mu$ and $\hat\sigma$ and check the validity condition.
(b) A report quotes "the material does not respond below 17 SU". Using the tail argument of 02.3,
explain why no series of this kind can support that statement, and what evidence could.

<details class="answer"><summary>Answer 5</summary>

(a) $y_0 = 20$, $N = 11$, $A = 0 + 6 + 4 = 10$, $B = 0 + 6 + 8 = 14$.
$\hat\mu = 20 + (10/11 + 0.5) = $ **21.41 SU**. $(NB - A^2)/N^2 = (154 - 100)/121 = 0.446 > 0.3$ ✓;
$\hat\sigma = 1.620(0.446 + 0.029) = $ **0.77 SU**.
(b) 17 SU is ≈ 5.7 $\hat\sigma$ below $\hat\mu$. With ≈ 20–30 trials concentrated near the median, the
probability of response there depends almost entirely on the assumed tail shape (logistic vs normal
differ by orders of magnitude), and $\hat\sigma$ itself is uncertain by ≈ ±45 %. "Does not respond" is
a probability statement about a tail that was never sampled. Evidence: many trials *at* 17 SU (e.g.
zero responses in $n$ trials bounds $P$ at ≈ $3/n$ at 95 %), a mechanistic argument about hot-spot
formation at that stimulus, and a design margin.

</details>

## Problem 6 — Thermal runaway and size (mathematical + design)

Fictional material W: $\rho = 900$ kg/m³, $Q = 1.5$ MJ/kg, $A = 5\times10^{11}$ s⁻¹,
$E = 110$ kJ/mol, $k = 0.15$ W/(m K). It is stored as flat layers (treat as an infinite slab,
$\delta_c = 0.878$).

(a) Write the Frank-Kamenetskii parameter and find the critical ambient temperature for layers of
total thickness 0.2 m, 0.4 m and 0.8 m.
(b) The store reaches 25 °C in summer. Which layer thicknesses are acceptable, and with what margin?
(c) By what factor must the thickness change to raise the critical temperature by ≈ 10 K, and why is
the answer nearly independent of the starting thickness?

<details class="answer"><summary>Answer 6</summary>

(a) $\delta = \rho QAE r^2 e^{-E/R_uT_a}/(kR_uT_a^2)$ with $r$ the *half*-thickness. Solving
$\delta = 0.878$: $r = 0.1$ m ⇒ **31.4 °C**; $r = 0.2$ m ⇒ **21.6 °C**; $r = 0.4$ m ⇒ **12.4 °C**.
(b) Only the 0.2 m layer ($r = 0.1$ m), with a ≈ 6 K margin — thin, given uncertainty in $E$.
The 0.4 m and 0.8 m layers are super-critical at 25 °C.
(c) Each halving of $r$ divides $\delta$ by 4; the critical temperature rises by roughly
$R_uT^2\ln4/E \approx 9$–10 K per halving (seen in the table: 12.4 → 21.6 → 31.4 °C). Because the
temperature enters exponentially and the size only as $r^2$, the shift per halving depends only
weakly (through $T^2$) on where you start.

</details>

---

## Simulator target — Sim I, CJ mode

Open [Sim I](sims/shock-tube/index.html) in CJ mode. For five settings of your choice spanning
$\gamma \in [1.15, 1.4]$ and $q \in [0.5, 5]$ MJ/kg (include mixtures G and H), **write down your
predicted $D_{CJ}$ and $p_{CJ}/p_1$ before revealing**. Target: all five within 3 %. Then set $D$
10 % above $D_{CJ}$ and identify the strong and weak intersection points; explain which one a
piston-supported wave reaches and why (ZND path from the von Neumann point).

## Design / case question — an ageing-related hazard from first principles

A (fictional) consignment of propellant-containing items has been stored for 12 years in a coastal
depot with no temperature control; no surveillance records exist. A newly installed logger shows
daily cycling between 18 °C and 48 °C in summer. Several containers show corrosion and some items
show residue around joints.

Write a one-page technical note, for a non-specialist manager, that explains **from first
principles** why this consignment should be treated as a higher hazard than the same items new, and
what information would reduce the uncertainty. Your note must use, quantitatively where possible:
Arrhenius kinetics and the kinetic mean temperature; stabiliser depletion followed by autocatalysis;
the Semenov/Frank-Kamenetskii link between self-heating, size and ambient temperature; the
statistical nature of sensitivity and why tail probabilities cannot be estimated for items of unknown
history; and the role of the IATG 07.10 surveillance concept. It must **not** contain any handling,
disposal or render-safe procedure — the decision framework for that is Stage 7.

<details class="answer"><summary>What a proficient answer contains</summary>

- **Ageing rate.** Convex $k(T)$ ⇒ cycling 18–48 °C ages the material faster than its mean
  (33 °C) suggests; with a fictional $E_a \approx 100$ kJ/mol and a two-level approximation of the
  cycle, the summer kinetic mean temperature is ≈ 42 °C — about 9 times the rate at 25 °C and
  3 times the rate at the 33 °C mean. Twelve uncontrolled years may correspond to many
  decades of "book" life.
- **Mechanism.** Stabiliser is consumed; once depleted, decomposition becomes autocatalytic with a
  long quiet induction period and a fast transition — so the absence of visible change is not
  evidence of safety.
- **Thermal stability.** Increased heat generation lowers the critical ambient temperature
  (Semenov); large, tightly packed stacks are worse ($r^2$ in the FK parameter); hot summer peaks
  approach or exceed critical conditions for degraded material.
- **Sensitivity.** Corrosion, residue (possible exudation) and cracking create additional hot-spot
  sites; the $P(\text{go}\mid x)$ curve may have shifted towards lower stimulus. No data-supported
  tail probability exists for items of unknown history.
- **Information that reduces uncertainty.** Chemical stability testing of samples (remaining
  stabiliser) under a surveillance system, the full temperature record, inspection by qualified
  ammunition technical staff, lot identification; decisions made by specialists using an
  exposure-minimising framework.
- **Expert band additionally:** quantifies the effective age with explicit $E_a$ uncertainty
  (e.g. 80–120 kJ/mol ⇒ a range of effective ages), and proposes an immediate low-cost
  mitigation (shading/ventilation to cut peak temperature) justified by the Arrhenius sensitivity.

</details>

Next: [Stage 3 · Explosive hazards & ordnance recognition](lessons/stage-03/lesson-01.md).
