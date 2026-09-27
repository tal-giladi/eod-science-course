# Capstones

Deliverable **10** (`plan.md` §17). Four capstones; **C1 is the flagship** and integrates robotics,
computer vision, sensor fusion, localisation, path planning, uncertainty, human-in-the-loop
decision-making and visualisation. Each is 60–120 hours. All environments are fictional: generic
objects, abstract hazard parameters, no modelling of real device construction or disarmament.

| Capstone | Integrates | Builds on | Level |
|---|---|---|---|
| [C1 · Autonomous EOD robot mission](capstones/c1-autonomous-mission.md) | robotics · CV · fusion · localisation · planning · uncertainty · HITL · visualisation | P03–P12, Sims B/C/G | Expert |
| [C2 · Humanitarian survey optimiser](capstones/c2-survey-optimiser.md) | detection theory · search theory · fusion · drones · land release · QA sampling | 05.1–05.7, P02, P03, P06, P10 | Advanced–Expert |
| [C3 · Post-blast digital reconstruction lab](capstones/c3-reconstruction-lab.md) | blast physics · inverse problems · photogrammetry · Bayesian inference · CV triage | 04.x, 08.x, P01, P09, P10, Sim E | Advanced–Expert |
| [C4 · Calibrated decision-support system](capstones/c4-decision-support.md) | decision theory · VOI · calibration · conformal prediction · HMI · assurance | 07.x, 09.2, 09.6, P12, Sims A/F | Expert |

## How capstones are assessed

Every capstone is assessed on the same five axes, each with a written artefact:

1. **Requirements traceability** — each requirement traced to the physics/statistics that justify it.
2. **Quantitative evaluation** — metrics with uncertainty over randomised trials (seeded, reproducible).
3. **Failure analysis** — FMEA-style table of how the system fails and what the operator sees when it does.
4. **Safety-boundary statement** — what the system deliberately does not model, and why.
5. **Design review memo** — 3–5 pages written for a sceptical technical reviewer.

Rubric bands (Novice → Expert) follow [assessment-plan.md](curriculum/assessment-plan.md).
