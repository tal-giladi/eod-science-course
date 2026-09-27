# EOD Science & Technology

**A graduate-level, simulation-heavy self-study program on the science, engineering, robotics,
sensing, AI and decision-making behind Explosive Ordnance Disposal — for an engineer learning
entirely through software, mathematics, simulation and research.**

Professional EOD technicians and bomb technicians train for a year or more in closed institutions,
with live ordnance. This course cannot and does not replace that. Instead it teaches what sits
*underneath* the profession — the shock physics, the chemistry of energy release, blast effects
and protection, hazard classification and recognition, detection physics and test & evaluation,
robot engineering, estimation and planning, decision-making under uncertainty, post-blast
forensic science, and AI for perception and decision support — at the depth an engineer with a
strong maths/software/robotics background can use.

<div class="callout boundary">

**Safety boundary.** This is an education and simulation course. It contains no explosive
formulations or manufacture, no device construction or component selection, no arming,
disarming, render-safe or defeat procedures, and no actionable initiation, timing or wiring
information. Operational topics are taught as concepts and decision frameworks; simulations use
fictional objects and abstract yield units. If you find an ordnance item or a suspicious object:
**do not touch it, move away, and call the emergency services.**

</div>

## What's inside

| | |
|---|---|
| **47 lessons in 10 stages** | Orientation → Physics → Chemistry → Recognition → Blast effects → Detection → Robotics → Decision-making → Forensics → AI & CV. Every important equation comes with units, intuition, a worked example, Python, and an exercise with a hidden answer. |
| **10 browser simulators** | 3D scene assessment, teleoperated robot, sensor fusion, blast physics (2D Euler solver), post-blast reconstruction, incident command, robotics-engineering challenges, recognition trainer, shock tube / CJ explorer, detection-theory lab — each with four difficulty levels and a structured debrief. |
| **12 programming projects** | blast-wave library & solver · sensor-noise simulator · Bayesian fusion · localisation · 2D robot simulator · path planning · SLAM · manipulator kinematics · CV detection · synthetic scene generator · teleoperation · human-in-the-loop decision system — each with starter code, tests and a reference solution. |
| **9 case studies** | Wheelbarrow 1972 · Harvey's 1980 · Oklahoma City 1995 · Kuwait clearance · Laos cluster munitions · counter-IED robots · Boston 2013 · WWII legacy ordnance · SS Richard Montgomery |
| **4 capstones** | autonomous EOD robot mission · humanitarian survey optimiser · post-blast reconstruction lab · calibrated decision support |
| **References** | curated sources with verified links, glossary (250+ terms), standards & doctrine map |

## Start here

1. [How to study this course](curriculum/how-to-study.md)
2. [Curriculum outline & dependency graph](curriculum/course-outline.md) — and [how it was derived](curriculum/research-synthesis.md) from real training pathways (military, police, humanitarian, academic)
3. [Stage 0 · What EOD is](lessons/stage-00/lesson-01.md)
4. [Simulators](sims/index.md) · [Projects](projects/index.md) · [Progress dashboard](dashboard.md)

## Stages

| Stage | Focus | Level |
|---|---|---|
| [0 · Orientation](lessons/stage-00/README.md) | the field, organisations, vocabulary, how EOD operates | Beginner |
| [1 · Physics foundations](lessons/stage-01/README.md) | mechanics, thermodynamics, shocks, reflection, scaling, structural response, electromagnetism | Beginner → Intermediate |
| [2 · Chemistry & energetic materials](lessons/stage-02/README.md) | thermochemistry, deflagration vs detonation, CJ/ZND, sensitivity, stability, ageing, classification | Intermediate |
| [3 · Hazards & ordnance recognition](lessons/stage-03/README.md) | taxonomy, munition families, safety-and-arming as a state machine, legacy & improvised hazards | Beginner → Intermediate |
| [4 · Blast effects](lessons/stage-04/README.md) | blast waves, reflection & confinement, structures, injury, fragments, standoff | Intermediate |
| [5 · Detection](lessons/stage-05/README.md) | detection theory, EMI/GPR, X-ray/CT/neutron, trace, imaging, fusion, search theory | Intermediate → Advanced |
| [6 · Robotics](lessons/stage-06/README.md) | EOD robots, spatial maths, manipulators, control, teleoperation, estimation, SLAM, planning, comms | Intermediate → Expert |
| [7 · Decision-making](lessons/stage-07/README.md) | decisions under uncertainty, VOI, incident management (conceptual) | Advanced |
| [8 · Forensics](lessons/stage-08/README.md) | post-blast scene, reconstruction as an inverse problem, lab & digital forensics | Advanced |
| [9 · AI & computer vision](lessons/stage-09/README.md) | perception, uncertainty, synthetic data, multimodal, active perception, trustworthy deployment | Advanced → Expert |

## Local use

```bash
python -m http.server 8080
```

Then open http://localhost:8080. Track progress with `python course.py status` (see
[PROGRESS.md](PROGRESS.md)).
