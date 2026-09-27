# C4 · Calibrated decision-support system for incident command

<div class="module-card">

**Prerequisites** Stage 7, 09.2, 09.6, P12; Sims A and F completed at Advanced. **Estimated time** 70–100 h. **Level** Expert.

</div>

## Problem

Design, build and evaluate a decision-support system for a **fictional** incident-command team.
It ingests a stream of heterogeneous reports (witness statements, CCTV-derived events, robot
sensor results, dog-team indications, trace alarms — each with an explicit, imperfect likelihood
model), maintains a belief over hypotheses, recommends the next information-gathering action by
value of information per minute and per unit of responder exposure, and presents uncertainty to a
human commander in a way that supports — never replaces — their judgement.

<div class="callout boundary">

**Boundary.** Hypotheses are abstract (benign / hoax / credible hazard / legacy ordnance / CBRN
component). Recommended actions are *information and isolation* actions only (Stage 7 framework);
the system never recommends how to act on a device.

</div>

## Requirements

| Id | Requirement |
|---|---|
| R1 | Belief updating with explicit likelihood tables; dependence between sources modelled (e.g. two witnesses who talked) |
| R2 | VOI-based action ranking with time, cost and exposure; myopic and two-step lookahead compared |
| R3 | Calibration of any learned component (temperature scaling) and conformal prediction sets for hypothesis classification with guaranteed coverage |
| R4 | Human interface: belief display, "what would change my mind" (most informative next observation), audit trail; tested with at least three different uncertainty visualisations |
| R5 | Evaluation on ≥ 500 simulated incidents: expected cost, time-to-decision, exposure, calibration; compare with (a) no DSS and (b) a threshold rule |
| R6 | Assurance case (09.6): claims, arguments and evidence that the DSS is fit for its intended use and fails safe (defers to the human) when outside its competence (OOD detection) |
| R7 | Automation-bias analysis: how would a wrong confident recommendation propagate, and what in the design limits it? |

## Links

[07.1](lessons/stage-07/lesson-01.md) · [07.2](lessons/stage-07/lesson-02.md) · [09.2](lessons/stage-09/lesson-02.md) · [09.6](lessons/stage-09/lesson-06.md) · [P12](projects/p12-hitl-decision/README.md) · [Sim F](sims/incident-command/index.html) · [Sim A](sims/scene-assessment/index.html) · [Case study: Harvey's 1980](case-studies/cs02-harveys-1980.md)
