# C1 · Autonomous EOD robot mission (flagship capstone)

<div class="module-card">

**Prerequisites** Stages 5, 6 and 9 complete; projects P03–P08 and P10–P12 passing. **Estimated time** 100–120 h.
**Level** Expert · **Deliverables** code repository, evaluation report, design-review memo, 5-minute demo video (screen capture).

</div>

## Mission

Build a simulated EOD robot that operates in a **fictional** environment containing unknown
objects and hazards, and completes a survey-and-report mission while minimising exposure and
uncertainty. The robot must:

1. **explore** an unknown area (frontier or information-gain exploration);
2. **map** it (occupancy grid + pose graph);
3. **detect** suspicious objects (CV on synthetic RGB/thermal renders);
4. **classify** observations with calibrated probabilities;
5. **estimate uncertainty** (per object and in the map/pose);
6. **choose sensors** by value of information under energy and time budgets;
7. **report** findings (map, object list with probabilities and evidence, confidence statements);
8. **allow human-operator intervention** at defined decision points (and log them);
9. **complete the mission** while respecting standoff constraints around suspected hazards.

<div class="callout boundary">

**Boundary.** Objects are generic fictional classes ("hazard-like", "clutter", "benign") with
synthetic sensor signatures from P10. The robot never manipulates a hazard-like object; the mission
ends at *reporting*. No real ordnance, device internals or render-safe actions are modelled.

</div>

## System architecture (reference — you may deviate with justification)

```mermaid
flowchart LR
  subgraph World["Simulated world (P05 + P10)"]
    W1[terrain & obstacles] --- W2[fictional objects] --- W3[sensor renderers]
  end
  subgraph Robot
    S[Sensors: lidar, RGB, thermal, EMI-like, depth] --> EST[State estimation EKF/PF (P04)]
    S --> MAP[Mapping & pose graph (P07)]
    S --> PER[Perception: detector + calibration (P09, 09.2)]
    PER --> FUS[Object-level Bayesian fusion (P03)]
    MAP --> PLAN[Planner: frontier / info-gain + risk cost map (P06, 09.5)]
    FUS --> PLAN
    FUS --> VOI[Sensor tasking by VOI]
    VOI --> PLAN
    PLAN --> CTRL[Controller + safety supervisor]
  end
  subgraph Operator["Operator console (HITL, P11/P12)"]
    UI[Map · object list · uncertainty · approve/deny]
  end
  CTRL --> World
  FUS --> UI
  UI -->|interventions| PLAN
  CH[Comms channel: latency, loss (06.9)] --- UI
```

## Requirements

| Id | Requirement | Verification |
|---|---|---|
| R1 | Explore ≥ 90 % of reachable free space within the energy budget | coverage metric over 20 seeded worlds |
| R2 | Map accuracy: occupancy IoU ≥ 0.85 vs ground truth | computed per world |
| R3 | Pose RMSE ≤ 0.3 m with loop closures; NEES consistent (95 % bounds) | Monte Carlo |
| R4 | Hazard-like object recall ≥ 0.95 at ≤ 0.5 false reports per world | FROC over worlds |
| R5 | Reported probabilities calibrated: ECE ≤ 0.05 | reliability diagram |
| R6 | Never enters the standoff radius of any object whose P(hazard-like) > 0.05 | safety supervisor log; zero violations |
| R7 | Sensor tasking beats a fixed sensor schedule on expected cost by ≥ 20 % | A/B over worlds |
| R8 | Operator interventions: ≤ 3 per mission on average; every intervention request carries the evidence and a recommended action with its expected cost | HITL simulator (P12) |
| R9 | Loss of comms > 2 s triggers a defined safe behaviour; mission resumes on reconnect | fault-injection tests |
| R10 | Everything reproducible from a seed; runtime ≤ 10 min per world on a laptop CPU | CI script |

## Milestones

1. **World & robot** (P05 + P10): fictional worlds generator with ground-truth object list; sensors.
2. **Localisation & mapping** (P04 + P07): pose graph with loop closure; map export.
3. **Perception** (P09): detector on synthetic renders; calibration; per-object evidence records.
4. **Fusion & tasking** (P03): object-level posteriors; VOI-based sensor choice under budgets.
5. **Planning & safety** (P06): risk-aware planner with standoff constraints; safety supervisor as an independent module (the planner cannot override it — the S&A principle from 03.2 applied to software).
6. **HITL console** (P11/P12): browser or matplotlib console showing map, uncertainty ellipses, object list with probabilities; approve/deny requests; logs.
7. **Evaluation**: 20+ seeded worlds × 3 difficulty settings; metrics with confidence intervals; failure gallery.

## Evaluation report template

- Summary table of R1–R10 with pass/fail and 95 % intervals.
- Ablations: no VOI tasking; no loop closure; uncalibrated perception; no HITL.
- Failure analysis (FMEA table): failure mode · cause · effect · detection · mitigation.
- What the operator saw in the three worst missions and whether the displayed uncertainty was honest.

## Extension (expert)

- Multi-robot exploration with task allocation (auctions) and relay placement for comms (Sim G challenge 3).
- Replace the classical planner with an RL policy trained in randomised worlds; compare sim-to-sim transfer to held-out world families.
- Adversarial robustness: evaluate the detector under physical-patch-like texture perturbations of *clutter* (09.6) and report the change in false reports.
- Port the stack to ROS 2 + Gazebo ([ROS 2 docs](https://docs.ros.org/), [Nav2](https://docs.nav2.org/)).
