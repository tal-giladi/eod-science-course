# Stage 9 gate · AI and computer vision for EOD

Covers [09.1](lessons/stage-09/lesson-01.md)–[09.6](lessons/stage-09/lesson-06.md). Work without
the lessons open; show every step, state assumptions, and say what your answer *cannot* tell you.
All datasets, detectors, items and programmes are fictional; objects are fictional surrogates.

<div class="callout boundary">

This gate assesses perception, uncertainty and evaluation reasoning. No question asks — and no
answer should contain — anything about how an item functions, how to render one safe, or how to
defeat a fielded detection system.

</div>

## Problem 1 · Operating point and evidence (mathematical + interpretation)

A drone detector is scored on a blind 3 ha lane seeded with 60 surrogate items (0.5 m halo).
At the chosen threshold it records 57 hits and 150 false alarms.

(a) Compute $P_D$, FA/ha and the two-sided 95 % Clopper–Pearson interval for $P_D$.
(b) The vendor claims "$P_D\ge0.95$". Is that supported at one-sided 95 % confidence?
(c) How many zero-miss presentations would demonstrate $P_D\ge0.98$ at 95 % confidence?
(d) The same detector reports mAP@0.5 = 0.91 on the vendor's test set. Give two reasons this
number does not bear on (a)–(c).

<details class="answer"><summary>Answer — then reveal</summary>

(a) $P_D=0.95$; FA/ha $=50$; CI $[0.861, 0.990]$.
(b) No. The one-sided 95 % lower bound is 0.876: the data are *consistent* with 0.95 but do not
demonstrate it. Claims should be stated as lower bounds.
(c) $n\ge\ln0.05/\ln0.98=148.3$ → 149.
(d) mAP depends on the test set's prevalence (precision changes with targets per image, not with
detector quality), uses IoU thresholds irrelevant to point-like hazards, averages over classes and
operating points you will not use, and — if the split was random over video frames — may be
inflated by leakage. None of it measures $P_D$ at an affordable FA/ha on representative ground.

</details>

## Problem 2 · Conformal guarantees for the hazard class (mathematical + design)

A robot-camera classifier outputs {clutter, benign debris, hazard-like}. Your calibration set has
2,000 labelled views with 4 % hazard-like (80 items).

(a) Show that Mondrian conformal with $\alpha_{\text{hazard}}=0.01$ is uninformative with this
set. What is the smallest $\alpha_{\text{hazard}}$ that gives a finite threshold?
(b) With $\alpha_{\text{hazard}}=0.02$, compute $k$ and the exact class-conditional coverage
$k/(n+1)$ implied by the rank argument, and the upper bound $1-\alpha+1/(n+1)$.
(c) Marginal 90 % conformal on the same model gives 0.90 overall coverage. Explain why this is
no evidence about hazard coverage, and describe the diagnostic you would run.
(d) Map each possible Mondrian set to an operator action.

<details class="answer"><summary>Answer — then reveal</summary>

(a) Finite threshold needs $n_k\ge(1-\alpha)/\alpha$, i.e. $80\ge 99$ — false; $\hat q=\infty$, so
every set contains "hazard". Equivalently $\alpha\ge1/(n_k+1)=1/81=0.0123$.
(b) $k=\lceil 81\cdot0.98\rceil=\lceil79.38\rceil=80$; coverage $80/81=0.9877$; upper bound
$0.98+1/81=0.9923$. (Guarantee is in expectation over calibration draws; any single calibration
set's realised coverage fluctuates with spread $\sim\sqrt{\alpha(1-\alpha)/n}$.)
(c) Marginal coverage averages over classes; with 96 % non-hazard inputs the majority class can be
over-covered while the hazard class is badly under-covered (09.2 lab: 0.90 marginal, 0.32 on the
hazard class). Diagnostic: report class-conditional coverage on held-out data with CIs.
(d) {clutter} / {debris} / {clutter, debris} → auto-label benign; {hazard} → declare, alert;
any set containing hazard plus another label → abstain to human with the set displayed; empty set
→ OOD, request another view or modality.

</details>

## Problem 3 · Calibration under prior shift (mathematical)

A binary hazard classifier was trained on data with 20 % hazard prevalence. Its raw logit for an
input is 3.0; temperature scaling fitted on in-distribution calibration data gives $T=2$. The
deployment prevalence is 0.5 %, and the programme sets $C_{FN}/C_{FP}=500$.

(a) Compute the temperature-scaled probability, the prior-corrected probability and $p^*$.
Declare or not?
(b) Which of the two corrections would you expect to remain valid if the deployment site also had
a different soil type? Why?

<details class="answer"><summary>Answer — then reveal</summary>

(a) $\sigma(3/2)=0.818$ (raw $\sigma(3)=0.953$). Prior correction: odds $4.48\times\frac{0.005/0.995}{0.2/0.8}=0.0904$
→ $p=0.083$. $p^*=1/501=0.0020$. Declare ($0.083\gg0.002$), but the display should show ≈ 8 %,
not 95 %.
(b) Neither is guaranteed. Prior correction assumes $p(x\mid y)$ is unchanged — a new soil
changes appearance (covariate/conditional shift). Temperature scaling was fitted to one
distribution; accuracy drops under shift while logit magnitudes need not, so it can remain
over-confident. Re-calibrate on labelled local data; monitor score distributions (09.6).

</details>

## Problem 4 · Sim-to-real diagnosis (interpretation + computation)

A team pretrains a thermal detector on 20,000 synthetic tiles and evaluates on real data.

- Synthetic validation AUC 0.98; real AUC 0.61.
- A domain classifier on the detector's penultimate features reaches 85 % accuracy.
- Importance weights for 100 synthetic samples (from that classifier): 80 at $w=1$, 20 at $w=6$.
- Real errors cluster at dawn and dusk; the generator samples capture times only between 10:00
  and 15:00.
- An audit of the real test set finds unlabelled real objects equal in number to 6 % of the
  labelled ones.

(a) Compute the proxy A-distance and the ESS of the weights; interpret each.
(b) Which Ben-David term does the capture-time restriction inflate, and what physics explains the
dawn/dusk failure?
(c) What is the maximum *measured* precision of a perfect detector on the audited test set?
(d) Propose three changes, in priority order, and the real-data evidence you would require
before claiming improvement.

<details class="answer"><summary>Answer — then reveal</summary>

(a) $\hat d_{\mathcal A}=2(1-2\cdot0.15)=1.4$ — domains are easily separable in the model's own
feature space. ESS $=(200)^2/800=50$: half the nominal sample; the $w=6$ region is under-sampled
by the generator.
(b) The domain divergence (real inputs outside the support of the simulator) *and* the joint-error
term: at dawn/dusk thermal contrast approaches zero and changes sign (diurnal crossover,
$T(z,t)=\bar T+A_0e^{-z/\delta}\cos(\omega t-z/\delta)$), so the labelling function in feature
space differs from midday.
(c) $1/1.06=0.943$: a perfect detector also finds the unlabelled objects, which are scored as
false positives.
(d) (1) Fix the real test labels (audit/double annotation) so measurement is trustworthy;
(2) sample capture time over 24 h with the physics-based diurnal model (and randomise
emissivity/vegetation), then re-check the domain classifier and ESS; (3) fine-tune on a small
labelled real set grouped by flight. Evidence: TSTR and fine-tuned $P_D$ at the programme's FA/ha
on a frozen, site-grouped real test set, reported per time-of-day stratum with exact CIs — never
synthetic validation AUC.

</details>

## Problem 5 · Multimodal geometry and active perception (conceptual + computation)

(a) A thermal camera is registered to an RGB camera by a homography fitted on a calibration
board at 2.0 m. Focal length 800 px, baseline 0.05 m. What residual misregistration (px) does an
object at 1.5 m show, and why can no homography remove it?
(b) A robot can point a binary sensor ($P_d=0.9$, $P_{fa}=0.1$) at one of two map cells, with
hazard beliefs 0.5 and 0.05. Compute the expected information gain (nats) of each and state which
the greedy next-best-view policy picks.
(c) Give one reason the greedy choice in (b) might be wrong for an EOD robot.

<details class="answer"><summary>Answer — then reveal</summary>

(a) Parallax residual $f\,b\,|1/Z-1/Z_0|=800\cdot0.05\cdot(0.667-0.5)=6.7$ px. A homography is
exact only for points on one plane (or for zero baseline); off-plane points have depth-dependent
disparity, so per-pixel depth (09.4) is needed for exact registration.
(b) $\mathrm{IG}=H(Y)-H(Y\mid X)$. Cell 1: $P(y=1)=0.5$, $H=0.693$; $H(Y\mid X)=H(0.9)=0.325$ →
0.368 nats. Cell 2: $P(y=1)=0.045+0.095=0.14$, $H(0.14)=0.405$ → 0.080 nats. Greedy picks cell 1.
(c) Information is not the only objective: the view might require approaching the cell with the
higher hazard belief (exposure/standoff constraints, 09.5 §6), the cell with lower belief may block
the only route, or decision value (does the observation change an action?) matters more than
entropy reduction (07.1 VOI).

</details>

## Problem 6 · Trustworthy-AI deployment review (system design / case)

A fictional vendor proposes an "autonomous clearance-assist" module for a humanitarian programme:
a quantised detector on the robot's edge computer, trained on synthetic data plus 300 real
images from one country, displaying "hazard confidence %" and auto-marking tiles below 1 % as
"clear". Its evidence pack: synthetic-test mAP 0.95, real-test recall 0.97 (random frame split),
saliency maps "showing the model looks at the object", and a statement that the model is
"robust to adversarial attack".

Write a one-page review. It must address: (i) evaluation validity, (ii) calibration and the
auto-clear rule, (iii) shift and monitoring, (iv) edge quantisation, (v) explainability claims,
(vi) the human-in-the-loop design and automation bias, (vii) robustness claims, and (viii) the
acceptance criteria you would require before any use, and for what role.

<details class="answer"><summary>Model answer points — then reveal</summary>

(i) Random frame split → leakage; synthetic mAP irrelevant; no FA/ha; no CIs; 300 real images
from one country cannot support a release-level claim ($P_D\ge0.99$ needs ≥ 299 zero-miss
positives *per representative condition*). (ii) "Confidence %" must be calibrated on real,
local data and prior-corrected; auto-clear below 1 % requires a class-conditional guarantee
(Mondrian/conformal risk control with ≥ 99 hazard calibration items per condition) and should
not exist for a prioritisation tool. (iii) Per-site recalibration; monitor score and feature
distributions, flag rate on confirmed-empty ground, and conformal coverage on QA samples; defined
drift triggers. (iv) Quantisation changes logits → re-verify accuracy *and calibration* after
quantisation on the target hardware; report latency and energy. (v) Saliency maps are not
evidence of correct reasoning (sanity-check failures, confirmation bias); require
counterfactual/occlusion tests and per-condition error analysis instead. (vi) Auto-marking
"clear" invites automation bias and deskilling; present sets/abstentions, keep humans deciding
on land release, measure operator trust calibration and workload, and log disagreements. (vii)
"Robust" is meaningless without a threat model and an evaluation (physical patch tests on
*your* system, sensor-consistency checks); state residual risk. (viii) Acceptance: blind,
site-grouped trial with pre-registered metrics ($P_D$ lower bound at a stated FA/ha per
condition), calibration and coverage on local data, HITL trial with operators, assurance case
linking hazards to evidence. Initial role: survey prioritisation only, never release.

</details>

## Project and simulator targets

- **P09** — all tests pass; the evaluation harness reports $P_D$ vs FA/ha with Clopper–Pearson
  intervals, FROC, and NMS-induced misses; your CNN's result on a flight-grouped split is
  reported as a lower bound at a stated FA/ha, per condition.
- **P12** — on the synthetic incident set, the hazard auto-clear rate is ≤ $\alpha_{\text{hazard}}$
  within its binomial CI, human-review workload is reported, and the policy refuses to run
  (clear error) when the hazard calibration set is below $(1-\alpha)/\alpha$.
- **Sim J** — reach the cost minimum at two prevalences and explain the threshold shift with
  $p^*$ and prior correction.

## Self-assessment rubric

| Band | Evidence |
|---|---|
| Novice | quotes mAP/accuracy; treats softmax output as probability; random splits |
| Developing | correct metrics and conformal arithmetic, but ignores rare-class coverage, shift or sample-size limits |
| Proficient | recall lower bounds at fixed FA/ha, class-conditional guarantees with feasible calibration sizes, grouped splits, real-data validation of synthetic pipelines |
| Expert | designs the evidence plan and assurance case; quantifies what cannot yet be claimed and what data would change that; anticipates shift, automation bias and adversarial failure |
