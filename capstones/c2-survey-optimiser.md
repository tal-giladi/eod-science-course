# C2 · Humanitarian survey optimiser

<div class="module-card">

**Prerequisites** Stage 5 (05.1–05.7), P02, P03, P06, P10. **Estimated time** 60–90 h. **Level** Advanced–Expert.

</div>

## Problem

A fictional mine-action operator must release a 2 km² area of suspected contamination to the
community. Evidence sources: historical records, community interviews (non-technical survey),
drone imagery (RGB/thermal), and ground teams with EMI-like and GPR-like detectors of known,
imperfect performance. Resources: a fixed number of team-days and drone hours.

Design a **decision-support tool** that allocates survey effort to minimise expected residual
contamination in released land subject to the budget, and that produces the documentation a
quality-assurance process needs.

## Requirements

| Id | Requirement |
|---|---|
| R1 | Spatial prior from non-technical survey evidence (Bayesian, with elicited likelihoods) |
| R2 | Drone survey model: detection probability depending on vegetation, time of day and object burial (05.5) |
| R3 | Ground-team model: sweep width / lateral-range curves (05.7), speed, false-alarm rate |
| R4 | Effort allocation: Koopman/Stone optimal allocation for exponential detection, extended to multiple sensor types with costs |
| R5 | Land-release classification per polygon: cancelled / reduced / cleared, with the residual-risk estimate and its uncertainty |
| R6 | QA sampling plan: probability of accepting a polygon as a function of residual contamination (operating characteristic curve) |
| R7 | Validation on synthetic worlds from P10 with known ground truth: compare against uniform effort and a greedy heuristic |

## Deliverables

Code, a map-based report for a fictional national authority, and a memo that explains — to a
non-statistician — what "released with residual risk X" means and how confident the operator is.

## Links

[05.1](lessons/stage-05/lesson-01.md) · [05.6](lessons/stage-05/lesson-06.md) · [05.7](lessons/stage-05/lesson-07.md) · [Case study: Laos](case-studies/cs05-laos-cluster-munitions.md) · [Case study: Kuwait](case-studies/cs04-kuwait-clearance.md) · [Sim J](sims/detection-theory/index.html)
