# Programming projects

Twelve projects, progressively more sophisticated (see the [project plan](curriculum/project-plan.md)).
Each has a README specification, a **starter** (API with `NotImplementedError` bodies), a **pytest
suite**, and a **reference solution** to open only after you have tried.

```bash
python -m pytest projects/p01-blast-wave            # your implementation (fails until you write it)
EOD_SOLUTION=1 python -m pytest projects/p01-blast-wave   # the reference solution
```

| # | Project | Lessons | Core techniques | Level |
|---|---|---|---|---|
| P01 | [Blast-wave library & shock solver](projects/p01-blast-wave/README.md) | 01.3–01.5, 04.1 | Rankine–Hugoniot, Kinney–Graham, Friedlander, finite-volume Euler, exact Riemann | Intermediate |
| P02 | [Sensor-noise simulator](projects/p02-sensor-noise/README.md) | 05.1–05.5 | stochastic sensor models, ROC by Monte Carlo, confidence bounds, trial sizing | Intermediate |
| P03 | [Bayesian sensor fusion](projects/p03-bayesian-fusion/README.md) | 05.6 | log-odds grids, correlated errors, expected information gain, scheduling | Advanced |
| P04 | [Robot localisation](projects/p04-localization/README.md) | 06.6 | EKF, particle filter, NEES/NIS | Advanced |
| P05 | [2D robot simulator](projects/p05-robot-sim/README.md) | 06.2, 06.4, 06.5 | kinematics, ray-cast lidar, odometry, lossy delayed channel, PID | Intermediate |
| P06 | [Path planning](projects/p06-path-planning/README.md) | 06.8 | A*, risk cost maps, RRT*, coverage | Advanced |
| P07 | [SLAM](projects/p07-slam/README.md) | 06.7 | occupancy grids, ICP, EKF-SLAM, pose-graph Gauss–Newton | Expert |
| P08 | [Manipulator kinematics](projects/p08-manipulator/README.md) | 06.2, 06.3 | SE(3), PoE/DH, Jacobians, DLS IK, manipulability | Advanced |
| P09 | [Computer-vision detection](projects/p09-cv-detection/README.md) | 09.1, 09.2 | synthetic imagery, classical baseline, small CNN, recall@FAR, calibration | Advanced |
| P10 | [Synthetic EOD scene generator](projects/p10-scene-generator/README.md) | 09.3, 08.2 | procedural scenes, domain randomisation, multi-sensor renders, dataset cards | Advanced |
| P11 | [Teleoperation simulator](projects/p11-teleoperation/README.md) | 06.5, 06.9 | delay/loss channel, operator models, move-and-wait, predictive display, stability | Advanced |
| P12 | [Human-in-the-loop decision system](projects/p12-hitl-decision/README.md) | 07.1, 09.2, 09.6 | calibration, conformal sets, value of information, asymmetric costs | Expert |

The capstone [C1](capstones/c1-autonomous-mission.md) integrates P03–P12.
