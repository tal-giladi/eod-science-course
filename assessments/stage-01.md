# Stage 1 gate · Physics foundations

<div class="module-card">

**Covers** [01.1](lessons/stage-01/lesson-01.md) · [01.2](lessons/stage-01/lesson-02.md) · [01.3](lessons/stage-01/lesson-03.md) · [01.4](lessons/stage-01/lesson-04.md) · [01.5](lessons/stage-01/lesson-05.md) · [01.6](lessons/stage-01/lesson-06.md) · [01.7](lessons/stage-01/lesson-07.md) · **Time** ≈ 3 h · **Pass** Proficient band on at least 7 of 8 problems: correct result, units and dimension check, a sanity check, and the governing assumption named.

**Simulator target** In [Sim I](sims/shock-tube/index.html), choose five shock Mach numbers between 1.1 and 3. For each, predict $p_2/p_1$, $\rho_2/\rho_1$, $T_2/T_1$ and $u_2$ *before* revealing, and get all five within 2 %.

</div>

Use $\gamma = 1.4$, $R = 287.05$ J kg⁻¹ K⁻¹, $p_0 = 101.325$ kPa, $T_0 = 288.15$ K and
$a_0 = 340.3$ m/s unless stated otherwise. Write your answer before revealing.

## Problem 1: impulse of a Friedlander pulse *(01.1, mathematical)*

A Friedlander positive phase with $p_m = 40$ kPa, $t_d = 10$ ms, $b = 1.5$ acts uniformly on a free,
rigid 1.0 m² panel of mass 20 kg. Compute the specific impulse, the panel's velocity and its
kinetic energy. Then state what would change if the panel were restrained by a spring with a
natural period of 2 ms.

<details class="answer"><summary>Model answer</summary>

$i = p_m t_d\left[\frac1b - \frac{1-e^{-b}}{b^2}\right] = 400\cdot0.3214 = 128.6$ Pa s ⇒
$J = 128.6$ N s ⇒ $v = 6.43$ m/s, $E_k = 413$ J. With $T_n = 2$ ms ≪ $t_d$ the response is
**quasi-static**. The panel follows the force, peak displacement ≈ $2F_{\max}/k$ (the dynamic load
factor of a suddenly applied load), and the *peak* pressure, not the impulse, governs (01.6).

</details>

## Problem 2: a gas cylinder, three energies *(01.2, mathematical + judgement)*

A 20 L nitrogen cylinder ($\gamma = 1.4$) at 300 bar (absolute, $p_0 = 1$ bar) fails in a few
milliseconds. Compute the Brode and isentropic energy estimates. Estimate the gas temperature after
isentropic expansion from 20 °C. Which estimate would you use in a hazard assessment, and why not
the isothermal one?

<details class="answer"><summary>Model answer</summary>

Brode: $(300-1)\times10^5\cdot0.02/0.4 = 1.50$ MJ. Isentropic: $\frac{300\times10^5\cdot0.02}{0.4}\left[1 - (1/300)^{0.2857}\right] = 1.21$ MJ.
$T_2 = 293.15\cdot(1/300)^{0.2857} = 57$ K (an ideal-gas limit). The thermal diffusion length in a
few ms is sub-millimetre, so the process is adiabatic and the isothermal model, which needs heat
input, is inappropriate. Use Brode as a conservative upper estimate and isentropic as a lower
estimate, and state which one you chose. Isothermal would give 3.4 MJ, an overestimate by more
than 2×.

</details>

## Problem 3: from overpressure to flow state *(01.3, mathematical)*

A shock with $\Delta p = 50$ kPa travels into sea-level air. Find $M_s$, $U_s$, $\rho_2/\rho_1$,
$T_2$ and the particle velocity $u_2$.

<details class="answer"><summary>Model answer</summary>

$M_s = \sqrt{1 + \frac{6}{7}\cdot\frac{50}{101.325}} = 1.193$; $U_s = 406$ m/s;
$p_2/p_1 = 1.493$; $\rho_2/\rho_1 = 1.329$; $T_2 = 288.15\cdot1.493/1.329 = 324$ K;
$u_2 = \frac{2}{2.4}\left(1.193 - \frac{1}{1.193}\right)\cdot340.3 = 101$ m/s. Sanity check:
between the acoustic limit ($u \approx \Delta p/\rho_0a_0 = 120$ m/s, which overestimates) and the
100 kPa example of 01.3 (177 m/s).

</details>

## Problem 4: reflection and dynamic pressure *(01.4, mathematical)*

The same 50 kPa shock strikes a large rigid wall head-on. Compute the normally reflected
overpressure and the peak dynamic pressure of the incident flow. Why is the reflection factor
greater than 2?

<details class="answer"><summary>Model answer</summary>

$\Delta p_r = 2\Delta p\,\frac{7p_0 + 4\Delta p}{7p_0 + \Delta p} = 100\cdot\frac{909.3}{759.3} = 119.8$ kPa
(factor 2.40). $q = \frac{5}{2}\frac{\Delta p^2}{7p_0 + \Delta p} = 2.5\cdot2500/759.3 = 8.2$ kPa.
The factor exceeds the acoustic value of 2 because the incident flow ($u_2 \approx 100$ m/s) must
be brought to rest at the wall. Its momentum adds to the reflected pressure, and the effect grows
with shock strength toward 8 for an ideal gas.

</details>

## Problem 5: scaling *(01.5, mathematical)*

In Sim D a source of 1 yield unit (YU) gives a peak overpressure $P^*$ at 10 m. (a) At what
distance does an 8 YU source give the same $P^*$ (Hopkinson–Cranz)? (b) At an altitude where
$p_z = 70$ kPa, by what factor must distances be scaled for the same *scaled* conditions (Sachs)?
(c) Give one physical situation in which cube-root scaling fails.

<details class="answer"><summary>Model answer</summary>

(a) $R = 10\cdot8^{1/3} = 20$ m. (b) $S_d = (p_0/p_z)^{1/3} = (101.33/70)^{1/3} = 1.131$.
(c) Any of: gravity-dominated effects (cratering and ejecta scale differently); strain-rate- or
size-dependent material response (structural failure does not scale geometrically); viscous and
thermal effects at very small scale; real-gas effects near very strong sources; scaled distances
outside a fit's validity range.

</details>

## Problem 6: which regime? *(01.6, mathematical + interpretation)*

A wall panel is modelled as an SDOF system with $m = 100$ kg and $k = 4\times10^5$ N/m. (a) Find its
natural period. (b) A load with impulse 200 N s and duration 5 ms: which regime applies, and what is
the peak displacement? (c) A load of 20 kN lasting 1 s: which regime, and what peak displacement?
(d) Sketch where (b) and (c) sit relative to the P–I curve's asymptotes.

<details class="answer"><summary>Model answer</summary>

(a) $\omega = \sqrt{k/m} = 63.2$ rad/s, $T_n = 99$ ms. (b) $t_d/T_n = 0.05 \ll 1$, so **impulsive**:
$x_{\max} = I/(m\omega) = 200/(100\cdot63.2) = 31.6$ mm. (c) $t_d/T_n \approx 10 \gg 1$, so
**quasi-static**: $x_{\max} \approx 2F/k = 100$ mm (a suddenly applied, long-duration load).
(d) (b) sits near the vertical (impulse) asymptote and (c) near the horizontal (pressure) asymptote.
The question the P–I diagram answers is on which side of the curve each point falls for a given
damage threshold.

</details>

## Problem 7: electricity and EM for technology *(01.7, mathematical)*

(a) The standard human-body model for electrostatic discharge is a 100 pF capacitance. How much
energy does it store at 10 kV? Compare with the energy needed to lift 1 g by 1 m. (b) A robot's
2.4 GHz link operates over 500 m in free space. Compute the free-space path loss, and the extra loss
if the range doubles. (c) Why do both numbers matter to an EOD technology designer? Answer at the
level of *safety concepts* and *link budget*.

<details class="answer"><summary>Model answer</summary>

(a) $E = \tfrac12CV^2 = \tfrac12\cdot10^{-10}\cdot10^8 = 5$ mJ. Lifting 1 g by 1 m takes 9.8 mJ, so
the charge is tiny as mechanical energy but delivered in nanoseconds through a small contact area.
(b) $\lambda = 0.125$ m; $\mathrm{FSPL} = 20\log_{10}(4\pi d/\lambda) = 94.0$ dB at 500 m and 100.0 dB
at 1 km (+6 dB per doubling). (c) ESD is why electrostatic control is a standard *safety concept*
around sensitive electronics and electro-explosive items (01.7, 02.3). Path loss sets range and
margin for teleoperation, and the loss-of-comms behaviour of robots (06.9) must be designed for the
link failing, not just for it working.

</details>

## Problem 8: choose the approximation *(design / judgement, all lessons)*

For each situation, choose the model and justify it with a *time or length scale* or a
*dimensionless number*: (a) air behind a shock front during its first millisecond (isentropic?
adiabatic? isothermal?); (b) a 5 Pa sound wave from a distant event (linear acoustics or
Rankine–Hugoniot?); (c) a 3 mm steel skin heated by a nearby fire (lumped or distributed?
$h_{\text{eff}} = 80$ W m⁻² K⁻¹); (d) a 150 bar propane vessel (ideal gas?); (e) a building
façade loaded for 2 ms (impulsive or quasi-static?); (f) a 1 YU and a 1000 YU source compared at the
same scaled distance (does cube-root scaling hold for fragment ranges?).

<details class="answer"><summary>Model answer</summary>

(a) Adiabatic, **not** isentropic, across the front (entropy jump). Isentropic along particle paths
behind it. Isothermal is ruled out because the thermal diffusion length is ~0.1 mm in 1 ms.
(b) Linear acoustics: $\Delta p/p_0 = 5\times10^{-5}$.
(c) Lumped: $\mathrm{Bi} = 80\cdot0.003/45 = 0.005 \ll 0.1$.
(d) No. Propane at room temperature is a liquid–vapour system, and the ideal-gas and Brode vapour
estimates miss the flash-evaporation energy (BLEVE, 01.2 Expert extension).
(e) Façade natural periods are typically tens of ms, so $t_d/T_n \ll 1$: impulsive. Check this
against the actual element.
(f) No. Blast parameters scale with $W^{1/3}$, but fragment ranges depend on fragment mass and drag
(ballistics with gravity), which do not scale geometrically. Scaling laws have validity domains
(01.5).

</details>

## Next

Passed? Continue to [02.1 Chemical energy](lessons/stage-02/lesson-01.md) (chemistry path) or
[04.1 Anatomy of a blast wave](lessons/stage-04/lesson-01.md) after 02.2, following the
[dependency graph](curriculum/course-outline.md).
