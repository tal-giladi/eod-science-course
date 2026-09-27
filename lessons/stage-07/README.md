# Stage 7 · EOD decision-making

Every earlier stage produced an *input* to a decision: blast envelopes (Stage 4), recognition
categories (Stage 3), detector likelihoods (Stage 5), remote means and their limits (Stage 6).
Stage 7 is where those inputs meet. It treats an explosive-hazard incident as what it
mathematically is — a **sequential decision problem under partial observability**, with
irreversible commitments, costly information and people exposed over time — and then maps that
framework onto the organisational toolkit of real incident management: cordons, information
gathering, tasking, evacuation or shelter, escalation, command interfaces and the families of
disposal outcome.

The mathematics is decision theory (expected loss, value of information), Bayesian filtering in
belief space (POMDP intuition, Bellman recursion) and a little scheduling theory; the human side
is cognitive bias, debiasing and naturalistic decision making. The simulators are the heart of
the stage: Sim F makes you manage a developing incident as reports arrive; Sim A makes exposure
and cordon geometry visible.

<div class="callout boundary">

**What this stage deliberately leaves out, and why.** Stage 7 teaches *how decisions are
reasoned about*, never *how an item is dealt with*. There are no render-safe or disposal
procedures, no tool techniques, no approach methods, no diagnostic steps and no guidance about
interacting with any real device or munition. Disposal outcomes appear only as four
organisational families — remove, destroy in place, render safe, and monitor/manage — and only in
terms of which risk and information factors drive the choice between them. 07.3 treats
render-safe as a *decision* (whether to expose anyone to the item at all, and when leaving it is
safer than intervening), which is teachable in the open; *how* any intervention is carried out
remains out of scope. The only "disarming method" this stage gives a non-specialist is positive
separation: do not touch, move away, keep others back, call the professionals. All hypotheses, sensors, losses and yields are
fictional or abstract (loss units LU, yield units YU); real stand-off distances come from
published public-safety tables and national doctrine. These operational skills are taught only
inside certified institutions under supervision, because partial knowledge of them is more
dangerous than none.

</div>

## Lessons

| Id | Lesson | Time | Level | Simulators / projects |
|---|---|---|---|---|
| 07.1 | [Decisions under uncertainty](lessons/stage-07/lesson-01.md) — sequential decisions, Bayesian updating, EVPI/EVSI, exposure minimisation, POMDP framing, cognitive biases, recognition-primed vs analytic decisions | 8 h | Advanced | Sim F, Sim A, P12 |
| 07.2 | [Incident management: the conceptual framework](lessons/stage-07/lesson-02.md) — cordons from risk tolerance, fragments and glazing, time–distance–shielding, information sources, tasking as scheduling, evacuation vs shelter, escalation, ICS, disposal-outcome families | 6 h | Advanced | Sim A, Sim F, P12, P01 |
| 07.3 | [Neutralisation and the decision not to intervene](lessons/stage-07/lesson-03.md) — the neutralisation *principles* (remote-first, stand-off, minimum exposure), intervene-versus-manage as two expected harms, the hands-off threshold, when leaving an item is correct even though people might touch it, monitor/manage as a first-class outcome | 5 h | Advanced | Sim A, Sim F, P12 |

**Stage total:** ≈ 19 h.

## Prerequisites

[03.4 Improvised hazards](lessons/stage-03/lesson-04.md) (the suspicious-item assessment) ·
[04.4 Injury, fragments & secondary hazards](lessons/stage-04/lesson-04.md) ·
[05.6 Sensor fusion](lessons/stage-05/lesson-06.md) ·
[06.5 Teleoperation & HMI](lessons/stage-06/lesson-05.md).

## Simulators

- **Sim F · Incident Command** — [`sims/incident-command/`](sims/incident-command/index.html):
  a timeline-driven scenario; request information, task sensors and the robot, set isolation,
  escalate or declare insufficient evidence. Scored on reasoning, not speed.
- **Sim A · Scene Assessment** — [`sims/scene-assessment/`](sims/scene-assessment/index.html):
  inspect a scene, deploy the robot's sensors, mark hazards, set a cordon and a control point,
  evacuate or shelter, under limited time and battery.

## Stage gate

[Stage 7 assessment](assessments/stage-07.md) — five problems (value of information, cordon under
uncertainty, belief-state policy, decision-log critique, intervene-or-manage) plus a simulator
target: Sim F and Sim A at *Expert*, "proficient" band or better.

## What comes next

[Stage 8 · Forensics & post-blast investigation](lessons/stage-08/README.md) begins where the
incident did not end safely — and inherits Stage 7's evidence-preservation and documentation
discipline. [Stage 9](lessons/stage-09/lesson-05.md) makes the belief-space loop autonomous
(active perception), and [Project P12](projects/p12-hitl-decision/README.md) builds the
human-in-the-loop decision engine.
