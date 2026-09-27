# Programming-project plan

Deliverable **8** (`plan.md` §12, §16). Twelve projects, progressively more sophisticated. Each
lives in `projects/pNN-slug/`:

```text
projects/pNN-slug/
  README.md          requirements · I/O · constraints · expected behaviour · test cases · extensions
  starter/…py        API skeleton; functions raise NotImplementedError
  tests/test_*.py    pytest suite the learner must make pass (run against starter by default)
  solution/…py       reference solution — open only after attempting
```

Run: `python -m pytest projects/pNN-slug` (tests import the starter); set `EOD_SOLUTION=1` to
run the same tests against the reference solution (this is how the course itself is verified).

| # | Project | Lessons | Core techniques | Deliverable | Difficulty |
|---|---|---|---|---|---|
| P01 | Blast-wave visualisation | 01.3–01.5, 04.1–04.2 | Rankine–Hugoniot, Friedlander, scaled distance, reflection ratio, numeric impulse integration, matplotlib animation | library + plots of p(t), p(Z), i(Z) for abstract yields | Intermediate |
| P02 | Sensor-noise simulator | 05.1–05.5 | stochastic sensor models (Gaussian, Poisson, clutter processes), ROC by Monte Carlo | `Sensor` classes + ROC curves | Intermediate |
| P03 | Bayesian sensor fusion | 05.6 | log-odds grid fusion, correlated-error handling, expected information gain sensor selection | fused posterior maps + sensor scheduler | Advanced |
| P04 | Robot localisation | 06.6 | EKF & particle filter for a skid-steer robot with landmarks | filter implementations + NEES consistency test | Advanced |
| P05 | 2D robot simulator | 06.2, 06.4, 06.5 | unicycle/skid-steer kinematics, lidar ray-casting, latency & packet-loss channel, PID | reusable simulator used by P06–P08, P11 | Intermediate |
| P06 | Path planning | 06.8 | A* on cost maps, RRT*, boustrophedon coverage | planners + benchmarks | Advanced |
| P07 | SLAM simulation | 06.7 | occupancy-grid mapping, EKF-SLAM, pose-graph optimisation (Gauss–Newton) | SLAM pipeline + loop-closure demo | Expert |
| P08 | Manipulator kinematics | 06.2–06.3 | homogeneous transforms, FK, numerical IK (damped least squares), Jacobian, manipulability | 3-DOF arm library + reachability/singularity maps | Advanced |
| P09 | Computer-vision detection | 09.1–09.2 | classical CV (OpenCV) baseline + small CNN (PyTorch, CPU OK) on synthetic imagery; recall@FAR | detector + evaluation report | Advanced |
| P10 | Synthetic EOD scene generator | 09.3, 08.2 | procedural 2D/2.5D scenes with fictional objects, labels, domain randomisation, sensor renders (RGB, thermal-like, X-ray-like, depth) | dataset generator + dataset card | Advanced |
| P11 | Teleoperation simulator | 06.5, 06.9 | delay/jitter/loss channel, predictive display, move-and-wait vs continuous control, operator metrics | experiment harness + analysis | Advanced |
| P12 | Human-in-the-loop decision system | 07.1, 09.2, 09.6 | calibrated classifier + conformal sets + VOI-based "ask the human / gather more data / decide" policy | decision engine + evaluation on synthetic incidents | Expert |

## Progression logic
P01–P02 exercise numerics & stochastic modelling; P03–P04 add Bayesian estimation; P05 is the
shared engine; P06–P08 add planning, mapping and manipulation on top of it; P09–P10 add learning
from synthetic data; P11–P12 put a human in the loop. Capstone C1 integrates P03–P12.

## What each README must contain (checked in QC)
Requirements · Input/output · Constraints (runtime, dependencies) · Expected behaviour ·
Test cases (in `tests/`) · Extension challenges · Links to lessons · Hints (collapsed).
