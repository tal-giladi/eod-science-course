# Stage 8 · Forensics & post-blast investigation

When an explosive event has happened, the questions change from *what might happen* to *what did
happen, and how do we know?* Stage 8 treats post-blast investigation as applied science with an
unusually demanding audience — a court. It follows the evidence from the scene to the report:
running the scene as a safe, systematic measurement campaign (search theory, survey metrology,
documentation and chain of custody); reconstructing the event as an **inverse problem** (seat
location, abstract yield with honest uncertainty, 3D capture, multi-camera timelines); and the
laboratory and digital work that tests the hypotheses (separation science and spectroscopy
*principles*, consensus standards, computer-vision triage of terabytes of media, error rates and
expert testimony).

The mathematics is search-effort allocation, error propagation, least squares, Bayesian inference
with MCMC, multi-view geometry and binomial error-rate statistics — all tools an AI/robotics
engineer already owns, applied under forensic discipline. The investigative mindset links back
to Stage 7's decision logs and forward to Stage 9's trustworthy AI.

<div class="callout boundary">

**What this stage deliberately leaves out, and why.** Stage 8 teaches forensic *method* —
scientific reasoning, documentation, reconstruction and evidence handling. It contains no device
construction or component details, no explosive compositions or formulations, and no analytical
information that could guide manufacture; residues are discussed only as analytical targets and
laboratory methods only by their physical and chemical principles, with non-energetic examples.
Yields in reconstructions are abstract (YU) and are presented to show how *uncertain* such
estimates are; no relation between damage or crater size and charge size is given for use. Scene
safety, and the decision that a scene is safe to enter, belong to certified professionals.

</div>

## Lessons

| Id | Lesson | Time | Level | Simulators / projects |
|---|---|---|---|---|
| 08.1 | [The post-blast scene](lessons/stage-08/lesson-01.md) — scene safety, zoning, search patterns and coverage maths, documentation and measurement uncertainty, evidence collection, packaging and chain of custody, TWGFEX at the scene–lab interface | 6 h | Advanced | Sim E (search, evidence log) |
| 08.2 | [Reconstruction as an inverse problem](lessons/stage-08/lesson-02.md) — seat from direction lines (least squares), yield from damage with uncertainty, Bayesian inversion with MCMC, damage-pattern interpretation, photogrammetry and bundle adjustment, LiDAR, video timeline synchronisation | 7 h | Advanced | Sim E (reconstruction), P10, Capstone C3 |
| 08.3 | [Laboratory & digital forensics](lessons/stage-08/lesson-03.md) — GC-MS, LC-MS, IC, FTIR, Raman, SEM-EDS principles, orthogonal methods and likelihood ratios, OSAC/ASTM standards, TEDAC, CV evidence triage, error rates and Daubert | 5 h | Advanced | Sim E (evidence log) + offline lab exercise, P09, P10 |

**Stage total:** ≈ 18 h.

## Prerequisites

[07.2 Incident management](lessons/stage-07/lesson-02.md) (evidence preservation, secondary
hazards) · [04.2 Distance, reflection, confinement](lessons/stage-04/lesson-02.md) and
[04.3 Structural effects](lessons/stage-04/lesson-03.md) (scaling, fragility) ·
[05.7 Search theory](lessons/stage-05/lesson-07.md) · [06.7 Mapping & SLAM](lessons/stage-06/lesson-07.md)
(nonlinear least squares) · [05.4 Trace & vapour detection](lessons/stage-05/lesson-04.md).

## Simulator

- **Sim E · Post-Blast Investigation** — [`sims/post-blast/`](sims/post-blast/index.html): a
  synthetic scene with fragments, damage marks, displaced objects, "photographs" and a tape tool;
  assess scene safety, search, keep an evidence log with chain of custody, and state a seat
  hypothesis with an uncertainty radius and a yield estimate with a ×/÷ factor. The debrief scores
  calibration and documentation discipline, not only accuracy. (Laboratory analysis is an offline
  exercise in 08.3.)

## Stage gate

[Stage 8 assessment](assessments/stage-08.md) — five problems (search allocation, measurement
uncertainty, seat and yield inversion, evidence combination and error rates, digital triage) plus
an evidence-handling plan, and a simulator target: Sim E reconstruction within tolerance with a
complete custody record.

## What comes next

[Stage 9 · AI & computer vision for EOD](lessons/stage-09/lesson-01.md) deepens the detection,
calibration and trustworthy-deployment tools used in 08.3. [Case study CS07 · Boston 2013](case-studies/cs07-boston-2013.md)
and [CS03 · Oklahoma City](case-studies/cs03-oklahoma-city.md) apply Stage 8 to real
investigations; Capstone C3 builds a full post-blast digital reconstruction lab.
