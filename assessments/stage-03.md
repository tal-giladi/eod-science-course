# Stage 3 gate · Explosive hazards and ordnance recognition

Attempt every problem without the lessons open; then check. Proficient = correct answers with
justification, main unknowns identified. All items, numbers and scenarios are fictional; yields
are abstract YU. Lessons: [03.1](lessons/stage-03/lesson-01.md) ·
[03.2](lessons/stage-03/lesson-02.md) · [03.3](lessons/stage-03/lesson-03.md) ·
[03.4](lessons/stage-03/lesson-04.md).

<div class="callout sim">

**Simulator target.** [Sim H · Recognition Trainer](sims/recognition-trainer/index.html): score
**≥ 85 % at Advanced** on both category *and* response-category, with a Brier score on your
stated confidences below 0.15 (the debrief's Calibration score is $100(1-2\,\text{Brier})$, so this
means Calibration above 70). Record the seed of your qualifying run.

</div>

## Problem 1 — category posterior with a noisy observer *(mathematical)*

Rural post-conflict context, four categories with prior PR 0.35, SM 0.30, MN 0.30, IM 0.05.
Likelihoods: $P(\text{small}\mid c) = (0.3, 0.9, 0.6, 0.4)$; $P(\text{irregular appearance}\mid c)
= (0.05, 0.05, 0.05, 0.85)$. A reporter states the item is small and "looks home-made"; that
reporter's appearance judgements are correct with probability 0.8 (and flip otherwise).
(a) Compute the posterior. (b) With losses $\ell(a_1,\text{IM})=20$, $\ell(a_2,\neg\text{IM})=1$,
choose the response. (c) How would the posterior differ if the observation were perfectly
reliable, and what does that say about the value of better observation?

<details class="answer"><summary>Answer</summary>

(a) Effective likelihood of the report $=0.8P+0.2(1-P)$: (0.23, 0.23, 0.23, 0.71). Unnormalised:
PR $0.35\cdot0.3\cdot0.23=0.02415$; SM 0.0621; MN 0.0414; IM $0.05\cdot0.4\cdot0.71=0.0142$;
posterior ≈ **PR 0.170, SM 0.438, MN 0.292, IM 0.100.**
(b) $E[\ell\mid a_1]=20\cdot0.100=2.00$; $E[\ell\mid a_2]=0.90$ ⇒ **$a_2$ (improvised-capable
response)**, although SM is most probable; threshold $1/21=0.048$.
(c) Perfect report: IM 0.380. Observer noise *halves* the diagnosticity of the strongest
indicator here; the decision is the same, but a better observation (e.g. a remote image) would
matter wherever $P(\text{IM})$ sits near the threshold.

</details>

## Problem 2 — independent safety features and common cause *(mathematical / design)*

A fictional S&A has two safety features, each with lifetime release-without-environment
probability $p=2\times10^{-3}$. Compare: design A, β = 0.05; design B, same features but made
diverse so β = 0.005; design C, design A plus a third, fully independent feature with
$p_3=10^{-2}$. Rank them and explain which engineering lever each uses.

<details class="answer"><summary>Answer</summary>

$P = (1-\beta)^2p^2+\beta p$. A: $0.9025\cdot4\times10^{-6}+10^{-4}=1.04\times10^{-4}$.
B: $0.990\cdot4\times10^{-6}+10^{-5}=1.40\times10^{-5}$. C: $1.04\times10^{-4}\cdot10^{-2}=1.04\times10^{-6}$.
Ranking C < B < A. B uses **diversity** (reduces common cause); C uses an additional
**independent** layer — a mediocre feature (1 %) is valuable *because* it is independent. Both
beat improving the original features' $p$, since the common-cause term dominates A.

</details>

## Problem 3 — contamination and residual hazard *(mathematical)*

A fictional strike dispersed 1,200 submunitions over 1.5 ha with field failure rate 0.08.
(a) Expected duds and binomial SD. (b) Probability that a 1 m × 300 m footpath through the
footprint intersects at least one item. (c) After clearance with $P_d=0.995$: probability the
footprint still holds at least one item, and the footpath probability. (d) Name one reason the
binomial SD understates real uncertainty.

<details class="answer"><summary>Answer</summary>

(a) $\lambda=96$, SD $=\sqrt{1200\cdot0.08\cdot0.92}=9.4$. (b) $\rho=96/15\,000=0.0064$ m⁻²;
$1-e^{-0.0064\cdot300}=1-e^{-1.92}=0.853$. (c) Residual $\lambda_r=0.48$ ⇒ $1-e^{-0.48}=0.38$;
path: $1-e^{-0.0064\cdot0.005\cdot300}=0.0096$. (d) Failure rate varies between strikes and lots
(overdispersion — beta-binomial), items are clustered rather than Poisson, and the "1,200" is
itself an estimate.

</details>

## Problem 4 — reading the statistics *(interpretation)*

Landmine Monitor 2025 reported 6,279 mine/ERW casualties for 2024 — the highest since 2020 — with
about 90 % civilians. A colleague concludes that "contamination worsened in 2024". Give three
alternative or contributing explanations, state what data would distinguish them, and say what the
figure is a lower bound *of*.

<details class="answer"><summary>Answer</summary>

Contributors: new use in active conflicts (new contamination, not worsening of old); greater
exposure through displacement, return or economic pressure; improved recording; reduced clearance
or risk-education funding. Discriminating data: casualties by country and item type, date of
contamination, recording-system coverage notes, land-release and funding trends. It is a lower
bound of *actual* casualties, since recording is incomplete — especially in active conflicts and
remote areas.

</details>

## Problem 5 — base rates, decision and value of information *(decision analysis)*

Base rate among reports $3\times10^{-4}$; HOT screen sensitivity 0.85, FPR 0.03. Options (cost if
benign, harm if device): none (0, 8000), cordon (1, 1200), evacuate (6, 150). (a) Posterior after a
positive screen. (b) Optimal option and the two thresholds. (c) An assessment step with
sensitivity 0.9 and specificity 0.85 is available before choosing: compute the EVSI.
(d) Name two costs this model omits.

<details class="answer"><summary>Answer</summary>

(a) $0.85\cdot3\times10^{-4}/(2.55\times10^{-4}+0.03\cdot0.9997)=0.00843$.
(b) Thresholds: none/cordon $1/6800=1.47\times10^{-4}$; cordon/evacuate $5/1050=4.76\times10^{-3}$.
$p=0.00843$ ⇒ **evacuate** (loss $6+0.00843\cdot150=7.26$).
(c) $P(T^+)=0.156$; $P(D\mid T^+)=0.0485$ ⇒ evacuate (13.28); $P(D\mid T^-)=0.0010$ ⇒ cordon
(2.20). With information: $0.156\cdot13.28+0.844\cdot2.20=3.93$. **EVSI ≈ 3.33.**
(d) Exposure and time consumed by the assessment itself; erosion of public compliance from
repeated evacuations (cry-wolf); secondary hazards of crowd movement; dependence between
successive reports.

</details>

## Problem 6 — mixed scene: response-category reasoning *(design / case)*

Fictional scenario. A construction project in a city that saw heavy fighting 30 years ago and
bombing 80 years ago. In one morning: (i) the excavator uncovers a rotted wooden crate containing
several identical, heavily corroded cylindrical items; (ii) a fin-stabilised-looking, bent item is
found in the spoil heap, 40 m away; (iii) an hour later, a new holdall is noticed just inside the
site gate, and the site office receives a call saying "you will regret building here".

For each item give: IMAS category (and uncertainty), likely state (03.2), lead organisation type,
priority, and the public/site-level actions. Then write the single consolidated instruction to
site staff (≤ 30 words), and explain how the three items interact.

<details class="answer"><summary>Model answer</summary>

| Item | Category | State reasoning | Lead | Priority |
|---|---|---|---|---|
| (i) crate | conventional, **AXO** (never used), fill unknown | S&A never exposed to enabling environments, but decades of ageing and corrosion ⇒ hazardous, sensitivity uncertain; CBRN "cannot exclude" if markings illegible | military EOD / state ordnance-disposal service | high |
| (ii) bent item | conventional, **UXO** (used, failed) | unknown S&A state ⇒ treat as armed; impact damage | same | high (per-item hazard highest of the conventional items) |
| (iii) holdall + threat call | **suspicious**: HOT (not typical, placement) *plus* a threat call — two indicators; treat as **possible IED** | no design authority, unknown category of functioning | police bomb squad / IEDD | **highest**: combined likelihood ratio and loss asymmetry; possible secondary-device logic |

Interactions: the threat call changes the interpretation of the whole site — it raises the
probability that (iii) is deliberate and makes a *secondary hazard* near the obvious assembly
points credible; the legacy items (i, ii) constrain where people can be moved. Responsibility
must be coordinated between police (lead, because of the possible IED and crime scene) and the
military/state disposal service (legacy items). Evacuation distances follow published stand-off
principles for the largest credible threat (04.4), with assembly away from the gate and not in
line of sight.

Instruction to staff: "Stop all work. Touch nothing. Leave the site now by the far exit, move well
away, do not gather at the gate, and follow police directions. Report anything else you saw."

</details>
