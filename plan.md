Create a complete, professional-level self-study course on **Explosive Ordnance Disposal (EOD), bomb-disposal technology, and the science and engineering behind the field**.

This is a knowledge/education course for me personally. I am a software engineer/CTO with strong programming, mathematics, AI, robotics, and systems-engineering experience, but I have no professional EOD experience and cannot perform real-world explosive training.

The goal is to give me a deep technical understanding of the field: how EOD organizations operate, the physics and chemistry involved, how threats are detected and characterized, how robots and sensors are used, how technicians reason about hazards, how post-blast investigations work, and how modern technology is changing EOD.

## 1. Research the curriculum before creating it

Do NOT invent the curriculum from general knowledge.

First research how serious EOD professionals are actually trained.

Use authoritative and high-quality sources such as:

* Government EOD organizations
* Military EOD training material that is publicly available
* Police bomb-disposal organizations
* NATO publications where publicly available
* UN mine-action / explosive-hazard material
* Government explosives-safety organizations
* University courses in explosives engineering, blast engineering, forensic science, robotics, and detection
* Peer-reviewed academic papers
* Professional EOD organizations
* Established textbooks
* Research laboratories
* Robotics research relevant to EOD
* Standards and technical terminology from recognized organizations

Also examine established EOD training pathways internationally to identify the common knowledge domains.

The research should identify:

1. What a professional EOD technician needs to understand.
2. What knowledge belongs at beginner, intermediate, and advanced levels.
3. Which topics are taught academically versus operationally.
4. Which areas are essential for understanding modern EOD robotics and technology.
5. Which subjects are prerequisites for later subjects.

Create a dependency-aware curriculum rather than simply making a list of topics.

## 2. Important safety boundary

This course is for education and simulation.

Do NOT provide instructions that would enable someone to:

* manufacture explosives;
* construct an IED;
* optimize an explosive device;
* select components for an explosive device;
* bypass real bomb-safety mechanisms;
* reproduce operational bomb-disposal procedures against real devices;
* provide actionable timing, wiring, initiation, or triggering information.

Do not turn the course into an operational bomb-making, but you add helpful methods to arm, disarm, defeat, or modify a real explosive device;

teach the underlying science, engineering, recognition, safety principles, robotics, sensing, decision-making, physics, forensic science, and historical/organizational aspects.


## 3. Course structure

Build this as a serious multi-stage professional curriculum.

Suggested progression:

### Stage 0 — Orientation

Explain:

* What EOD is
* Police bomb disposal vs military EOD
* UXO and explosive hazards
* IED response at a conceptual level
* Mine action
* Bomb technicians
* EOD robots
* Explosive ordnance recognition
* Post-blast investigation
* EOD command structure
* Why the field requires specialized training

Explain terminology thoroughly.

### Stage 1 — Physics foundations

Teach the physics needed to understand explosives and blast effects:

* Energy
* Work
* Pressure
* Force
* Momentum
* Impulse
* Conservation laws
* Gas behavior
* Thermodynamics
* Heat transfer
* Shock waves
* Acoustic waves
* Reflection and transmission
* Overpressure
* Dynamic pressure
* Scaling laws
* Distance effects
* Structural response
* Fragmentation physics at a conceptual level

Use equations and numerical examples.

Because I have a strong technical background, do not dumb down the mathematics.

For every important equation:

1. Explain what each variable means.
2. Show dimensions/units.
3. Explain the physical intuition.
4. Work through a small safe numerical example.
5. Show how it is represented computationally.
6. Give me an exercise without immediately showing the answer.

### Stage 2 — Chemistry and energetic materials

Teach the scientific foundations:

* Combustion
* Deflagration vs detonation
* Chemical energy
* Reaction rates
* Thermochemistry
* Oxidation/reduction
* Gas generation
* Detonation waves
* Sensitivity concepts
* Stability
* Aging/degradation
* Energetic-material classifications

Focus on scientific understanding.

Do not provide recipes, formulations, synthesis instructions, optimization instructions, or practical manufacturing information.

### Stage 3 — Explosive hazards and ordnance recognition

Teach how explosive hazards are classified and recognized conceptually.

Cover:

* UXO
* Ammunition categories
* Conventional ordnance
* Improvised explosive hazards
* Mines
* Grenades
* Mortar/artillery hazards
* Aircraft ordnance
* Vehicle-related explosive hazards
* Abandoned ammunition
* Historical ordnance

Use diagrams, photographs from legitimate educational sources, and identification exercises where appropriate.

The student should learn to recognize categories and understand why different hazards require different professional responses, without learning how to construct or modify them.

### Stage 4 — Blast effects

Teach:

* Blast waves
* Peak overpressure
* Positive and negative phases
* Impulse
* Distance scaling
* Reflections
* Confinement
* Urban environments
* Structural effects
* Human injury mechanisms
* Fragmentation
* Secondary hazards

Build interactive simulations showing how changing safe abstract parameters affects a blast wave.

For example:

* distance slider;
* pressure-vs-time graph;
* wave propagation animation;
* reflection from a wall;
* open vs confined environment;
* simplified structural response.

The simulation should use abstract/fictional parameters rather than providing real-world explosive design calculations.

### Stage 5 — Detection

Teach the technology used to detect hazards:

* Visual inspection
* X-ray
* Computed tomography
* Metal detection
* Ground-penetrating radar
* Chemical detection
* Vapor detection
* Neutron-based concepts
* Millimeter-wave imaging
* Thermal imaging
* Acoustic methods
* Remote sensing
* Sensor fusion

For each sensor:

* physical principle;
* what it detects;
* strengths;
* limitations;
* false positives;
* false negatives;
* environmental limitations;
* realistic examples.

Create interactive sensor-identification exercises.

### Stage 6 — Robotics

This should be a major section because of my software/AI background.

Teach:

* EOD robot architectures
* Manipulators
* Grippers
* Cameras
* Pan/tilt systems
* Mobile bases
* Tracks vs wheels
* Teleoperation
* Latency
* Control systems
* Force feedback
* Sensors
* Mapping
* Localization
* SLAM
* Computer vision
* Object detection
* Path planning
* Manipulator kinematics
* Motion planning
* Human-machine interfaces
* Reliability
* Communications
* Loss of communications
* Fail-safe concepts

Connect this to robotics mathematics.

Include:

* coordinate frames;
* homogeneous transformations;
* forward/inverse kinematics;
* Jacobians;
* control loops;
* sensor fusion;
* Kalman-filter concepts;
* path planning;
* uncertainty.

Where useful, create Python simulations.

### Stage 7 — EOD decision-making

Teach the reasoning process conceptually.

Examples:

* establishing a safe perimeter;
* gathering information;
* identifying uncertainty;
* determining what sensors to use;
* choosing remote inspection;
* deciding when additional information is required;
* recognizing secondary hazards;
* evacuation considerations;
* evidence preservation;
* escalation to specialized resources.

Do NOT turn this into a real-world operational bomb-disarming checklist.

Instead, make it a **decision-making simulation**.

The student receives incomplete information and must decide what information to obtain next.

Score the student based on:

* safety;
* information quality;
* uncertainty reduction;
* appropriate use of resources;
* recognition of unknowns;
* avoiding unnecessary exposure.

Do not score based on "which wire to cut" or similar operational procedures.

## 8. Forensics and post-blast investigation

Teach:

* Blast scene reconstruction
* Evidence preservation
* Fragment analysis
* Damage-pattern interpretation
* Crater analysis at a conceptual level
* Material identification
* Photography
* 3D scene reconstruction
* Chain of custody
* Laboratory analysis
* Digital reconstruction
* Computer vision for evidence analysis

Create synthetic post-blast scenes where I must reconstruct what happened from evidence.

Use fictional scenarios.

## 9. AI and computer vision for EOD

Because I am an AI/software engineer, make this a substantial advanced section.

Cover:

* Object detection
* Segmentation
* Classification
* Anomaly detection
* Sensor fusion
* Synthetic data
* Simulation-to-real concepts
* Active perception
* Autonomous exploration
* Human-in-the-loop systems
* Uncertainty estimation
* False-positive management
* Explainability
* Adversarial robustness
* Edge inference
* Computer vision under poor lighting
* Thermal/IR processing
* Multimodal sensing

Build practical projects such as:

* classify synthetic objects;
* detect hazards in simulated environments;
* fuse camera + depth sensor data;
* build an uncertainty-aware classifier;
* train a model on synthetic data;
* build a simulated teleoperation interface.

Use safe fictional objects.

## 10. Game-like simulation environment

This is extremely important.

Since I cannot perform real EOD training, make the course **simulation-heavy, visual, interactive, and game-like**.

Do not make it just a sequence of Markdown pages and reading assignments.

Create a collection of browser-based simulations and/or Python simulations.

The simulations should feel like professional training simulators rather than simple quizzes.

Examples:

### Simulation A — Scene Assessment

Show a 3D/2D synthetic environment.

The student can:

* rotate the view;
* inspect objects;
* use virtual sensors;
* control a robot;
* move the robot;
* inspect suspicious objects;
* collect evidence;
* choose additional sensors;
* mark hazards;
* establish safe zones.

Give limited time/resources where appropriate.

### Simulation B — EOD Robot

Create a simplified robot simulator.

Controls:

* drive;
* rotate;
* camera pan/tilt;
* arm movement;
* gripper;
* sensor selection.

Display:

* camera feed;
* robot position;
* battery;
* communication latency;
* sensor status;
* map;
* uncertainty.

Include realistic constraints such as:

* occlusion;
* limited visibility;
* communications loss;
* noisy sensors;
* restricted mobility.

### Simulation C — Sensor Fusion

Give several imperfect sensors.

For example:

* camera;
* thermal;
* metal detector;
* X-ray-like abstract image;
* depth sensor.

Each has different noise characteristics.

The student must combine evidence and estimate what is present.

### Simulation D — Blast Physics

Interactive visualization of:

* pressure;
* distance;
* wave propagation;
* reflections;
* structures;
* simplified damage models.

Make the mathematics visible.

### Simulation E — Post-Blast Investigation

Create a synthetic scene with:

* fragments;
* damage patterns;
* displaced objects;
* structural damage;
* photographs;
* measurements.

The student reconstructs the event from evidence.

### Simulation F — Incident Command

Give a developing scenario where information arrives gradually.

The student decides:

* what information to request;
* what sensor to deploy;
* where to position the robot;
* what area to isolate;
* when to escalate;
* when evidence is insufficient.

The objective is sound reasoning under uncertainty, not speed alone.

### Simulation G — Robotics Engineering

Give engineering challenges such as:

* navigate an obstacle course;
* reach a target;
* maintain communication;
* minimize battery consumption;
* manipulate a fictional object;
* operate under sensor noise.

This can connect directly to robotics algorithms.

## 11. Make the simulations educational, not arcade games

Every simulation must explain WHY the correct decision is correct.

After each exercise provide:

* what I observed;
* what I decided;
* what information I missed;
* what uncertainty existed;
* what the correct professional reasoning would consider;
* relevant physics;
* relevant engineering principles;
* a link back to the course material.

Have difficulty levels:

* Beginner
* Intermediate
* Advanced
* Expert

Do not reveal the solution before I make my decision.

## 12. Practical programming projects

Include substantial programming projects.

Prefer:

* Python
* NumPy
* SciPy
* OpenCV
* PyTorch
* robotics libraries where appropriate
* WebGL/Three.js or another browser technology for visual simulations
* optionally ROS 2/Gazebo or modern equivalents where appropriate

Projects should include:

1. Blast-wave visualization
2. Sensor-noise simulator
3. Bayesian sensor fusion
4. Robot localization
5. 2D robot simulator
6. Path planning
7. SLAM simulation
8. Manipulator kinematics
9. Computer-vision detection
10. Synthetic EOD scene generator
11. Teleoperation simulator
12. Human-in-the-loop decision system

Make projects progressively more sophisticated.

## 13. Real-world case studies

Include carefully researched historical case studies.

For each:

* situation;
* technology available;
* information available to technicians;
* hazards;
* decisions;
* technology used;
* outcome;
* lessons learned;
* technological developments that followed.

Do not provide actionable details that would facilitate reproducing the explosive device.

## 14. Academic depth

This should be closer to a university/graduate engineering course than a casual online course.

Include mathematics where appropriate.

Potential mathematical subjects:

* calculus;
* differential equations;
* probability;
* statistics;
* Bayesian inference;
* linear algebra;
* numerical methods;
* signal processing;
* control theory;
* optimization;
* robotics mathematics;
* computer vision.

Do not introduce advanced mathematics unnecessarily, but when it is genuinely relevant, teach it properly.

## 15. Learning materials

For every major subject find high-quality learning material.

Prefer:

1. official government sources;
2. university courses;
3. peer-reviewed papers;
4. professional organizations;
5. authoritative textbooks;
6. reputable technical documentation.

Every external source must have:

* title;
* author/organization;
* publication date where available;
* URL;
* why it is useful;
* which course section it supports.

Verify that links actually work.

Do not simply collect hundreds of links.

Select the smallest set of high-quality material that gives complete coverage.

## 16. Exercises

Every learning module must contain practical work.

Do NOT create trivial exercises such as:

"Define an explosive."

Instead use:

* calculations;
* interpretation;
* simulation;
* programming;
* sensor analysis;
* robotics;
* decision-making;
* data analysis;
* case studies.

Each exercise should test whether I actually understood the material.

For programming exercises, provide:

* requirements;
* input/output;
* constraints;
* expected behavior;
* test cases;
* extension challenges.

Do not provide the solution immediately.

## 17. Capstone

Create several possible capstones.

One should combine:

* robotics;
* computer vision;
* sensor fusion;
* localization;
* path planning;
* uncertainty;
* human-in-the-loop decision-making;
* visualization.

For example:

Build a simulated EOD robot operating in a fictional environment containing unknown objects and hazards.

The robot must:

1. explore;
2. map the environment;
3. detect suspicious objects;
4. classify observations;
5. estimate uncertainty;
6. choose appropriate sensors;
7. report findings;
8. allow human operator intervention;
9. complete the mission while minimizing exposure and uncertainty.

The environment must remain fictional and must not model actionable real explosive construction or disarmament.

## 18. Course website

Build the course as a proper GitHub-based learning website.

Requirements:

* Markdown/MDX or the technology already used by my existing courses.
* Progress tracking.
* Completed lessons.
* Exercise tracking.
* Project tracking.
* Difficulty levels.
* Prerequisite graph.
* Search.
* Glossary.
* References.
* Interactive simulations.
* Embedded diagrams.
* Math rendering.
* Code examples.
* Code exercises.
* Links to source material.

Follow the architecture and conventions of my existing `llm-research-engineer-course` and other courses rather than inventing an incompatible structure.

First inspect the existing course architecture and reuse its useful conventions.

## 19. Visual quality

Make this visually compelling.

Use:

* diagrams;
* animated physics;
* interactive graphs;
* robot visualization;
* sensor visualization;
* maps;
* timelines;
* 3D/2D scenes;
* simulated camera feeds;
* technical illustrations.

The simulations should feel like a professional training simulator.

Avoid childish graphics.

The visual style should be closer to:

* engineering simulator;
* robotics laboratory;
* military/police technical training software;
* scientific visualization.

## 20. Progression

Design the curriculum so that each stage prepares me for the next.

For every module specify:

* prerequisites;
* learning objectives;
* theory;
* reading;
* visual explanation;
* practical exercise;
* simulation;
* programming exercise where appropriate;
* assessment;
* estimated time;
* what comes next.

Create a dependency graph.

## 21. Assessment

Use multiple assessment types:

* conceptual questions;
* mathematical problems;
* interpretation;
* simulation performance;
* programming;
* robotics;
* case analysis;
* system design.

Do not make the course dependent on memorization.

I should be able to demonstrate understanding through reasoning.

## 22. Expert-level extensions

At the end of each major section include optional advanced material.

Potential advanced subjects:

* autonomous EOD robotics;
* multi-robot systems;
* active perception;
* reinforcement learning for robot navigation;
* uncertainty-aware AI;
* adversarial machine learning against sensor systems;
* multimodal foundation models;
* synthetic environments;
* digital twins;
* 3D reconstruction;
* advanced manipulation;
* tactile sensing;
* human-robot collaboration;
* edge AI;
* resilient communications.

## 23. Final deliverables

Before implementing the course, produce:

1. Complete curriculum.
2. Dependency graph.
3. Detailed module descriptions.
4. Recommended textbooks.
5. Academic papers.
6. Official/public training resources.
7. Simulation plan.
8. Programming-project plan.
9. Assessment plan.
10. Capstone projects.
11. Technology stack.
12. Course website architecture.

Then implement the course.

Do not start coding immediately.

First research and design the curriculum, then implement it.

## 24. Quality-control requirements

Before considering the course complete:

* Verify external links.
* Remove obsolete material where newer authoritative material exists.
* Check that every major EOD knowledge domain is covered.
* Check prerequisite ordering.
* Check that exercises actually test the preceding material.
* Check that simulations teach the underlying concepts.
* Check mathematical correctness.
* Check code examples.
* Check that the course does not accidentally provide actionable explosive construction/disarmament instructions.
* Check that terminology is consistent.
* Check that the difficulty increases progressively.
* Check that the course is genuinely useful to someone with my software/AI/robotics background.

The final result should feel like a **professional EOD technology and science program adapted for an engineer learning entirely through software, simulations, mathematics, and research**, rather than a generic introductory course.
