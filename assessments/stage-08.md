# Stage 8 gate · Forensics & post-blast investigation

Covers [08.1](lessons/stage-08/lesson-01.md), [08.2](lessons/stage-08/lesson-02.md) and
[08.3](lessons/stage-08/lesson-03.md). Work without the lessons open; state units, assumptions
and what the data *cannot* show. All scenes are fictional; yields are abstract (YU).

<div class="callout boundary">

This gate assesses forensic method — search, measurement, inference, evidence integrity and
reliability. No question asks about device construction, compositions or any operational
procedure.

</div>

## Problem 1 · Search planning (mathematical)

A fictional scene has three zones with item-location probabilities $p=(0.5, 0.3, 0.2)$ and areas
$(300, 1\,500, 6\,000)$ m². One searcher-hour sweeps 360 m² (random-search model,
POD$_i = 1-e^{-k_ie_i}$ with $k_i = 360/A_i$). The budget is 20 searcher-hours.
(a) Compute the Koopman allocation and overall POD. (b) Compare with effort proportional to area.
(c) The farthest item found so far is at 44 m: what perimeter radius and area does the NIJ rule
give, and how long is one full pass with 6 searchers at 0.1 m/s and 1 m spacing?

<details class="answer"><summary>Answer — then reveal</summary>

(a) Water-filling gives $e \approx (3.62, 9.25, 7.13)$ h; zone PODs contribute $(0.493, 0.267,
0.070)$ → overall **0.831**. (b) Area-proportional: $(0.77, 3.85, 15.38)$ h → overall **0.603**.
(c) $1.5\times44 = 66$ m; $A=\pi\cdot66^2 = 13\,685$ m²; track length 13 685 m covered by
six searchers walking a combined $6\times0.1 = 0.6$ m/s → 22 808 s ≈ **6.3 h**.

</details>

## Problem 2 · Measurement uncertainty (mathematical + design)

(a) A total station ($\sigma_d = 2$ mm + 2 ppm, $\sigma_\theta = 5''$) locates a fragment at 80 m.
Compute the radial and transverse standard uncertainties. (b) The same fragment by tape
triangulation with $\sigma_r=20$ mm at an intersection angle of 30°: compute
$\sigma_{\text{pos}}$. (c) An SfM model of the scene shows 0.4 px reprojection error and 3 cm RMS
at five independent check points. Which number goes in the report and why?

<details class="answer"><summary>Answer — then reveal</summary>

(a) Radial $2 + 0.16 = 2.16$ mm; transverse $80\cdot2.42\times10^{-5}$ m = 1.94 mm.
(b) $\sqrt2\cdot20/\sin30° = 56.6$ mm. (c) The check-point RMS (3 cm): it is the only
independent measure of *accuracy*; reprojection error measures internal consistency and is blind
to scale and systematic distortion (gauge freedom).

</details>

## Problem 3 · Seat and yield inversion (mathematical + interpretation)

Three direction lines: through (10, 0) with direction (1, 0); through (0, 10) with direction
(0, 1); through (8, 6) with direction $(1,1)/\sqrt2$. (a) Compute the least-squares seat.
(b) Glazing with an illustrative 2 kPa threshold broke out to 60 m. With $Z_{\text{th}}=42.4$ m
YU⁻¹ᐟ³ and local log-slope $n=-1.02$, estimate $W$ and its 90 % interval for $\sigma_{\ln p} =
0.4$ and $\sigma_{\ln R}=0.08$. (c) A colleague proposes reporting "$W = 2.8$ YU". Write the
sentence you would report instead, and name the nuisance parameter that dominates.

<details class="answer"><summary>Answer — then reveal</summary>

(a) $\sum P_i = \begin{bmatrix}1.5&-0.5\\-0.5&1.5\end{bmatrix}$; solving gives $\hat{\mathbf x} =
(0.5, -0.5)$. (Check: residual distances 0.5, 0.5, 0.71; sum of squares 1.0, versus 2.0 at the
origin.) With only three lines, one of which disagrees, the result should be reported with its
covariance and a note that more directions are needed.
(b) $\hat W = (60/42.4)^3 = 2.84$ YU; $\sigma_{\ln W} = 3\sqrt{(0.4/1.02)^2+0.08^2} = 1.20$;
90 % factor $e^{1.645\cdot1.20} = 7.2$ → **≈ 0.4 to 20 YU**.
(c) "The damage is consistent with an event of roughly 0.4–20 YU (90 % interval), assuming the
glazing fragility stated in Appendix X; the estimate scales directly with that assumption." The
glazing fragility (threshold) dominates — the yield–fragility degeneracy of 08.2 §4.

</details>

## Problem 4 · Combining laboratory evidence and error rates (mathematical + interpretation)

Two methods give likelihood ratios 200 and 30 for "residue of class X". A validation study of the
combined scheme found 0 false identifications in 60 blind tests.
(a) Assuming independence, what is the combined LR, and what is the posterior probability if the
prior odds are 1 : 500? (b) State the one-sided 95 % upper bound on the false-identification
rate. (c) The two methods share a sample-preparation step known to carry over a common
interferent. How should the report change?

<details class="answer"><summary>Answer — then reveal</summary>

(a) $\Lambda=6\,000$; posterior odds $6\,000/500 = 12$ → probability $12/13 = 0.92$ — far from
"6 000 to 1". (b) $1-0.05^{1/60} = 0.049$ (rule of three: 0.05) — with only 60 tests, the scheme's
error rate could be up to ≈ 5 %. (c) The independence assumption fails, so the product overstates
the evidence (08.3 Exercise 3): report a joint LR estimated from validation data on the combined
scheme, or the weaker of the two, and state the shared step as a limitation; better, re-design
with an orthogonal preparation route.

</details>

## Problem 5 · Digital triage (mathematical + design)

A tip line has received $5\times10^5$ images. (a) Using 64-bit dHash and the fair-coin model,
choose the largest Hamming threshold with fewer than one expected false pair. (b) A relevance
ranker put 41 of 45 seeded relevant images in the top 10 % of a validation set. Report recall
with a 95 % Clopper–Pearson interval. (c) Give two design rules that keep the pipeline
defensible in court.

<details class="answer"><summary>Answer — then reveal</summary>

(a) $\binom{n}{2}\approx1.25\times10^{11}$. Expected false pairs: $d^{*}=5$: 0.056; $d^{*}=6$:
0.56; $d^{*}=7$: 4.8 → **$d^{*}=6$**. (b) $41/45 = 0.91$, 95 % CI ≈ [0.79, 0.98]. (c) Hash every
original on ingest and log every transform (custody); the model only *reorders* — nothing is
discarded — and every evidential finding is confirmed by a human examiner; also report recall
per stratum (day/night, camera type) at the operating budget.

</details>

## Design question · Evidence-handling plan

For the fictional car-park scene of 08.1 (perimeter 90 m, 8 searchers, 2 days, a total station,
a laser scanner, residue sampling, 400 GB of public media expected), write a one-page
evidence-handling plan covering: entry control and logging; search zones and effort allocation;
documentation standards (photography sequence, photo log, survey control, scan registration);
collection and packaging (controls, blanks, container types, seals); the custody data model and
how its integrity is anchored externally; digital-media intake; and the hand-off to the
laboratory and the reconstruction team.

<details class="answer"><summary>What a proficient plan contains — then reveal</summary>

Single entry point and approach path with an entry log (who, when, why, where); zones and
Koopman effort with achieved-POD recording and a rule for perimeter expansion; overall → mid →
close-up photography with and without scale, a sequential photo log, no deletions, original hashes;
a three-point total-station control network, scanner registration to it and independent check
points; per-item packaging with blanks for every kit and controls from unaffected matching
surfaces, airtight containers where volatile residues may be present, tamper-evident seals; an
append-only custody log with previous-record hashes, head hash countersigned at each laboratory
intake; media ingest with SHA-256, work copies, transform log; lab requests that preserve
material for orthogonal methods; reconstruction requests fed back as targeted searches while the
scene is still held. Expert-level plans also state the error budget for positions, how search
coverage will be reported, and who has authority to release the scene.

</details>

## Simulator target

**Sim E · Post-Blast Investigation** at *Advanced* or higher: reconstruct the seat within the
scenario's tolerance **with the true seat inside your stated uncertainty region**, keep a custody
record with no breaks, and request laboratory analyses with the required blanks and controls.
Record the debrief and write three sentences: which evidence constrained the seat most, which
assumption dominated the yield interval, and what you would document differently.

## Self-assessment rubric

| Band | Evidence |
|---|---|
| Novice | computes positions and yields as single numbers; custody as a form to fill in |
| Developing | correct calculations; uncertainty stated but not propagated; independence assumed without comment |
| Proficient | optimal search allocation, propagated uncertainties, calibrated intervals, orthogonality argued, custody integrity anchored |
| Expert | designs surveys for information (boundary windows, check points), identifies degeneracies and model error, reports error rates with intervals and limits in court-ready language |
