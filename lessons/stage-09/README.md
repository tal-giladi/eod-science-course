# Stage 9 · AI and computer vision for EOD

Stages 5 and 6 gave you sensors and robots; Stage 7 gave you a decision framework that consumes
likelihoods. Stage 9 builds the learned perception layer between them and treats it with the
rigour a safety-critical system demands. The machine learning is graduate level — detection
losses and assignment, anomaly detection, calibration, conformal prediction, domain adaptation,
multimodal geometry, information-gain planning, adversarial robustness — but every lesson is
organised around the data realities that make EOD different from benchmark ML:

- **tiny datasets** of mostly inert surrogates, collected by a handful of experts;
- **extreme class imbalance** — one item per $10^2$–$10^4$ m², most images empty;
- **cost asymmetry** — a miss can kill, a false alarm costs technician minutes;
- **domain shift** — new country, soil, season, altitude or sensor on every deployment;
- **safety-critical recall** that must be *demonstrated* on real data with honest confidence
  bounds, not asserted from a benchmark mAP.

The throughline: choose the task and the metric from the decision (09.1), make the scores mean
something and guarantee coverage of the hazard class (09.2), manufacture the data you cannot
collect and prove it transfers (09.3), fuse modalities correctly (09.4), let the robot choose
where to look (09.5), and deploy with a human in the loop under an assurance case (09.6).

<div class="callout boundary">

**What this stage deliberately leaves out, and why.** Stage 9 is about *perception, uncertainty
and evaluation*. It contains no information about how any device or munition functions, is
constructed or is rendered safe, and no guidance on defeating or evading detection systems:
adversarial-robustness material (09.6) is framed as *evaluation of your own system* against
published threat models, never as instructions for attacking fielded equipment. All generated
objects are fictional geometric shapes with invented material parameters; simulated physics is
*detection* physics only (heat conduction in soil, X-ray attenuation, radar propagation).
Datasets named are public research datasets of inert or surrogate items, discussed at the level of
their structure and evaluation, not of the features that distinguish specific real item types.
Recognition of real ordnance belongs to certified training under supervision.

</div>

## Lessons

| Id | Lesson | Time | Level | Simulators / projects |
|---|---|---|---|---|
| 09.1 | [Perception tasks for EOD](lessons/stage-09/lesson-01.md) — cost-weighted thresholds, prior shift, YOLO vs DETR (IoU/GIoU, focal loss, NMS, Hungarian matching), segmentation losses, anomaly detection (Mahalanobis, autoencoders, PatchCore), RGB/thermal/X-ray/GPR specifics, recall at fixed FA/ha, FROC, exact binomial bounds, mAP pitfalls, AMLID/RIT/SULAND | 8 h | Advanced | Sim J, P09 |
| 09.2 | [Uncertainty-aware ML](lessons/stage-09/lesson-02.md) — aleatoric vs epistemic, ECE and reliability, temperature scaling, deep ensembles, MC dropout, Laplace last layer, split conformal (proof), APS/RAPS, Mondrian conformal for asymmetric risk, selective prediction, OOD detection | 8 h | Advanced → Expert | Sim C, P09, P12 |
| 09.3 | [Synthetic data & sim-to-real](lessons/stage-09/lesson-03.md) — Ben-David bound, procedural generation, domain randomisation, physics-based thermal/X-ray/GPR simulation, fine-tuning, DANN, pseudo-labels, importance weighting, measuring the gap, dataset cards, label noise (SULAND v2) | 9 h | Advanced → Expert | Sim H, P10 |
| 09.4 | [Multimodal sensing](lessons/stage-09/lesson-04.md) — camera models, extrinsics and homographies, thermal–RGB registration, time synchronisation, low-light/IR processing, depth sensing, early/mid/late fusion, missing modalities | 7 h | Advanced | Sim C, P09 |
| 09.5 | [Active perception & autonomous exploration](lessons/stage-09/lesson-05.md) — map entropy, expected information gain, next-best-view, frontier exploration, risk-aware standoff, belief-space planning, RL caveats, multi-robot allocation | 7 h | Expert | Sim G, Sim A, P06, P07 |
| 09.6 | [Trustworthy deployment](lessons/stage-09/lesson-06.md) — adversarial robustness and physical-world testing, spoofing and consistency checks, shift monitoring, explainability and its failures, edge inference, automation bias and calibrated trust, false-positive management, T&E and assurance cases | 8 h | Expert | Sim J, P12 |

**Stage total:** ≈ 47 h (outline estimate 48 h).

## Prerequisites

[05.1 Detection theory](lessons/stage-05/lesson-01.md) ·
[05.6 Sensor fusion](lessons/stage-05/lesson-06.md) ·
[06.2 Spatial mathematics](lessons/stage-06/lesson-02.md) (for 09.4) ·
[06.7 Mapping & SLAM](lessons/stage-06/lesson-07.md) and [06.8 Planning](lessons/stage-06/lesson-08.md) (for 09.5) ·
[07.1 Decisions under uncertainty](lessons/stage-07/lesson-01.md) (for 09.5–09.6).
Assumed from your background: deep learning (CNNs, transformers, PyTorch), probability and
information theory, linear algebra.

## Projects

- [P09 · Computer-vision detection](projects/p09-cv-detection/README.md) — classical baseline +
  small CNN on synthetic imagery; protocol-correct evaluation ($P_D$ vs FA/ha, exact CIs).
- [P10 · Synthetic EOD scene generator](projects/p10-scene-generator/README.md) — procedural
  scenes with fictional objects, physics-based sensor renders, dataset card.
- [P12 · Human-in-the-loop decision system](projects/p12-hitl-decision/README.md) — calibrated
  classifier + conformal sets + VOI-based "ask the human / gather more data / decide" policy.

## Stage gate

[Stage 9 assessment](assessments/stage-09.md) — six problems (operating point and evidence,
conformal guarantees for the hazard class, calibration under prior shift, sim-to-real diagnosis,
multimodal/active-perception reasoning, and a trustworthy-AI deployment review) plus project
targets for P09 and P12.

## What comes next

[Stage 10 case studies](case-studies/index.md) — especially
[counter-IED robots](case-studies/cs06-counter-ied-robots.md) and
[Laos cluster-munition clearance](case-studies/cs05-laos-cluster-munitions.md) — put the
evaluation and deployment questions of this stage into historical context, and
[Capstone C1](capstones/index.md) integrates perception, uncertainty and active exploration on a
full autonomous robot mission.
