# Glossary

This glossary defines the terms used across the course, in alphabetical order. Where a term is
defined in **IMAS 04.10** (mine action) or the **NATO AJP-3.18 Lexicon** (EOD doctrine), the
definition below follows that source's meaning in paraphrase, and the source is named. Physics,
robotics and ML terms use standard textbook meanings (see [curriculum/sources.md](curriculum/sources.md)).
Each entry links to the lessons where the term is introduced or used most heavily.

<div class="callout boundary">

Operational terms such as *render safe* are defined **conceptually only**: what the outcome is
and where it sits in a decision framework, never how it is achieved. See the safety boundary in
each stage README.

</div>


## A

- **Abandoned explosive ordnance (AXO)** — Explosive ordnance that was not used during an armed conflict, was left behind or dumped by a party to the conflict, and is no longer under that party's control. It may or may not have been primed, fuzed or armed (IMAS 04.10; CCW Protocol V). — [00.1](lessons/stage-00/lesson-01.md), [03.1](lessons/stage-03/lesson-01.md)
- **Acoustic impedance** — The product ρc of density and sound speed. It governs how much of an incident wave is reflected or transmitted at an interface between two media. — [01.4](lessons/stage-01/lesson-04.md)
- **Acoustic-to-seismic coupling** — Detection method in which airborne sound induces ground vibration. Buried objects change the vibration, and a vibrometer senses the difference. — [05.5](lessons/stage-05/lesson-05.md)
- **Active perception** — Perception in which the agent chooses sensing actions (viewpoint, sensor, dwell time) to reduce uncertainty about the task, rather than passively processing whatever data arrives (Bajcsy et al. 2018). — [09.5](lessons/stage-09/lesson-05.md)
- **Adiabatic flame temperature** — The temperature the products of a combustion reaction would reach if all the reaction enthalpy went into heating them, with no heat loss. It is an upper bound used to compare energy release. — [02.1](lessons/stage-02/lesson-01.md)
- **Adversarial example** — An input deliberately perturbed, digitally or physically (for example a patch placed in the scene), so that a machine-learning model makes a wrong prediction. — [09.6](lessons/stage-09/lesson-06.md)
- **AJP-3.18** — NATO Allied Joint Doctrine for EOD Support to Operations (Ed. B, 2023). It defines the EOD capability subsets and terminology. — [00.1](lessons/stage-00/lesson-01.md), [00.2](lessons/stage-00/lesson-02.md)
- **Aleatoric uncertainty** — Uncertainty due to irreducible noise or ambiguity in the data itself. More data of the same kind does not reduce it. Contrast with epistemic uncertainty. — [09.2](lessons/stage-09/lesson-02.md)
- **All reasonable effort** — IMAS concept: the documented level of effort, via information gathering, survey, clearance and quality management, that could reasonably have been expected to find contamination if it were present. Land is released on this basis, not on proof of absence. — [05.7](lessons/stage-05/lesson-07.md)
- **Ammunition Technical Officer (ATO)** — In UK usage, a commissioned officer trained as an ammunition engineer (through-life management, inspection, accident investigation) who also commands EOD and IEDD operations. The equivalent non-commissioned role is Ammunition Technician (AT). — [00.2](lessons/stage-00/lesson-02.md)
- **Anomaly detection** — Identifying inputs that differ from a model of 'normal' data. It is used when threat examples are rare or unrepresentative. — [09.1](lessons/stage-09/lesson-01.md)
- **Arrhenius equation** — k = A·exp(−Eₐ/RT): the rate constant of a thermally activated reaction grows exponentially with temperature. It underlies thermal-runaway and ageing reasoning. — [02.1](lessons/stage-02/lesson-01.md), [02.3](lessons/stage-02/lesson-03.md)
- **Arrival time** — The time between the explosive event and the arrival of the shock front at a given point. It scales with W^(1/3) under Hopkinson–Cranz scaling. — [04.1](lessons/stage-04/lesson-01.md)
- **A-scan / B-scan / C-scan** — GPR display types: a single trace versus time (A), a vertical profile along a line (B), and a horizontal slice at fixed depth or time (C). — [05.2](lessons/stage-05/lesson-02.md)
- **Attenuation (X-ray)** — The exponential reduction of beam intensity through matter, I = I₀exp(−μx), where μ depends on material and photon energy. — [05.3](lessons/stage-05/lesson-03.md)
- **Automation, levels of** — A graded scale from full manual control to full autonomy, applied separately to information acquisition, analysis, decision selection and action implementation (Parasuraman, Sheridan & Wickens 2000). — [06.5](lessons/stage-06/lesson-05.md), [09.6](lessons/stage-09/lesson-06.md)

## B

- **Backscatter (X-ray)** — Imaging from Compton-scattered photons returning towards the source side. It allows single-sided inspection and preferentially shows low-Z, organic materials near the surface. — [05.3](lessons/stage-05/lesson-03.md)
- **Base rate** — The prior probability that a hazard is present before a test result is known. When the base rate is low, even an accurate detector produces mostly false alarms (base-rate neglect). — [05.1](lessons/stage-05/lesson-01.md), [07.1](lessons/stage-07/lesson-01.md)
- **Battle area clearance (BAC)** — Systematic and controlled clearance of hazardous areas where the hazards are known not to include mines (IMAS 09.11). — [05.7](lessons/stage-05/lesson-07.md)
- **Bayes filter** — The recursive estimator that alternates a prediction step (motion model) and an update step (measurement likelihood) to maintain a belief over the state. Kalman and particle filters are implementations of it. — [06.6](lessons/stage-06/lesson-06.md)
- **Bayes' theorem** — P(H|E) = P(E|H)·P(H)/P(E): how evidence E updates the probability of hypothesis H. It is the basis of fusion, filtering and incident reasoning in this course. — [05.1](lessons/stage-05/lesson-01.md), [05.6](lessons/stage-05/lesson-06.md), [07.1](lessons/stage-07/lesson-01.md)
- **Belief state** — A probability distribution over the hidden states of a system, maintained by an agent that cannot observe the state directly. It is the state variable of a POMDP. — [07.1](lessons/stage-07/lesson-01.md), [09.5](lessons/stage-09/lesson-05.md)
- **Blast injury (primary–quaternary)** — Primary: caused by the pressure wave acting on gas-filled organs. Secondary: caused by fragments and debris. Tertiary: caused by the body being displaced. Quaternary: all other effects (burns, crush, toxic inhalation). — [04.4](lessons/stage-04/lesson-04.md)
- **Blast wave** — The pressure disturbance, led by a shock front, that propagates outward from a rapid release of energy into a surrounding fluid. — [04.1](lessons/stage-04/lesson-01.md)
- **Bomb technician** — A public-safety (police or fire) responder trained and certified to respond to suspected explosive devices. In the US, certification is by the FBI Hazardous Devices School under NBSCAB guidelines. — [00.2](lessons/stage-00/lesson-02.md)
- **Booby trap** — An apparatus designed to kill or injure that functions unexpectedly when a person disturbs an apparently harmless object or performs an apparently safe act (IMAS 04.10, after CCW Amended Protocol II). — [03.1](lessons/stage-03/lesson-01.md), [03.4](lessons/stage-03/lesson-04.md)
- **Bounding box / mAP** — Object detection outputs box locations and classes. Mean average precision (mAP) summarises precision–recall across classes and IoU thresholds. — [09.1](lessons/stage-09/lesson-01.md)
- **Buckingham Π theorem** — A physical relation among n variables involving k independent dimensions can be rewritten as a relation among n − k dimensionless groups. It is the basis of blast scaling. — [01.5](lessons/stage-01/lesson-05.md)
- **Bundle adjustment** — Joint nonlinear least-squares refinement of camera poses and 3-D points that minimises reprojection error. — [08.2](lessons/stage-08/lesson-02.md)

## C

- **Calibration (model)** — Agreement between predicted confidence and observed frequency: among predictions made with confidence p, a fraction p should be correct. Measured with reliability diagrams and ECE. — [09.2](lessons/stage-09/lesson-02.md)
- **Calibration (sensor)** — Estimating a sensor's intrinsic parameters (for example focal length and distortion) and extrinsic parameters (pose relative to other sensors) so that measurements can be registered in a common frame. — [09.4](lessons/stage-09/lesson-04.md), [08.2](lessons/stage-08/lesson-02.md)
- **CBRN** — Chemical, biological, radiological and nuclear hazards. They may overlap with explosive hazards, and CBRN EOD is a specialist NATO capability subset. — [03.1](lessons/stage-03/lesson-01.md), [04.4](lessons/stage-04/lesson-04.md)
- **Chain of custody** — The documented, unbroken record of who collected, handled, transferred and stored each item of evidence, and when. It establishes integrity for legal proceedings. — [08.1](lessons/stage-08/lesson-01.md)
- **Chapman–Jouguet (CJ) point** — The tangency point of the Rayleigh line with the equilibrium (reacted) Hugoniot. It gives the minimum steady detonation speed; there the flow behind the wave is sonic relative to the front. — [02.2](lessons/stage-02/lesson-02.md)
- **Clearance** — Tasks or actions to ensure the removal and/or destruction of all explosive ordnance from a specified area to a specified depth (IMAS 04.10, 09.10). — [05.7](lessons/stage-05/lesson-07.md)
- **Cluster munition** — A conventional munition designed to disperse or release explosive submunitions (Convention on Cluster Munitions definition, with specified exclusions). — [03.3](lessons/stage-03/lesson-03.md)
- **Clutter** — Returns from non-target objects or features (rocks, roots, metal debris, soil layering) that resemble targets and drive the false-alarm rate. — [05.2](lessons/stage-05/lesson-02.md)
- **Colorimetric test** — A presumptive chemical test that indicates a compound class by a colour change. It is fast but non-specific. — [05.4](lessons/stage-05/lesson-04.md)
- **Common robotic system** — The US Army's modular family of EOD and engineer robots (CRS-I, CRS-H, MTRS) with an interoperability profile. It was adopted after the fragmented counter-IED robot fleet. — [06.1](lessons/stage-06/lesson-01.md)
- **Compatibility group (CG)** — A letter code (A–H, J, K, L, N, S) grouping explosive articles and substances that can be stored or transported together without significantly increasing the probability or effect of an accident (UN Model Regulations; IATG 01.50). — [02.3](lessons/stage-02/lesson-03.md)
- **Computed tomography (CT)** — Reconstruction of a 3-D attenuation map from many projections taken at different angles (for example by filtered back-projection or iterative methods). — [05.3](lessons/stage-05/lesson-03.md)
- **Configuration space (C-space)** — The space of all robot configurations. Obstacles map to forbidden regions of it, and planning becomes a search for a path through free C-space. — [06.8](lessons/stage-06/lesson-08.md)
- **Confined explosion** — An explosion inside an enclosure. Loading combines the shock reflections with a longer-lasting quasi-static gas pressure that depends on the volume and venting. — [04.2](lessons/stage-04/lesson-02.md)
- **Confirmed hazardous area (CHA)** — An area where the presence of explosive ordnance has been confirmed by direct evidence (IMAS 04.10). — [05.7](lessons/stage-05/lesson-07.md)
- **Conformal prediction** — A distribution-free method that turns any model's scores into prediction sets with guaranteed marginal coverage 1 − α, under exchangeability of the calibration and test data. — [09.2](lessons/stage-09/lesson-02.md), [09.6](lessons/stage-09/lesson-06.md)
- **Conservation laws** — Conservation of mass, momentum and energy across a control volume. Applied across a shock front, they give the Rankine–Hugoniot relations. — [01.1](lessons/stage-01/lesson-01.md), [01.3](lessons/stage-01/lesson-03.md)
- **Control volume** — A fixed or moving region of space across whose boundary mass, momentum and energy fluxes are accounted for. — [01.1](lessons/stage-01/lesson-01.md)
- **Conventional munitions disposal (CMD)** — The EOD capability subset dealing with conventional (manufactured) munitions (AJP-3.18). — [00.1](lessons/stage-00/lesson-01.md), [03.2](lessons/stage-03/lesson-02.md)
- **Cordon** — The controlled perimeter established around a suspected explosive hazard to keep people at a safe distance and control access. It is set from hazard-distance reasoning and adjusted as information improves. — [07.2](lessons/stage-07/lesson-02.md)
- **Cost map** — A grid of traversal costs (obstacles, inflation, terrain, risk) used by planners. — [06.8](lessons/stage-06/lesson-08.md)
- **Counter-IED (C-IED)** — The collective effort to defeat the threat of improvised explosive devices. NATO frames it as three pillars: attack the network, defeat the device, and prepare the force. — [03.4](lessons/stage-03/lesson-04.md)
- **Coverage planning** — Planning a path that sweeps a sensor footprint over every point of a region, for example boustrophedon decomposition for area survey. — [06.8](lessons/stage-06/lesson-08.md), [05.7](lessons/stage-05/lesson-07.md)
- **Crater** — The depression formed by an explosion at or below a surface. Its dimensions depend on yield, depth of burst and soil, and are interpreted only conceptually in reconstruction. — [08.2](lessons/stage-08/lesson-02.md)

## D

- **d′ (d-prime)** — The sensitivity index of signal detection theory: the separation between the signal-plus-noise and noise distributions in units of their standard deviation. It is independent of the decision criterion. — [05.1](lessons/stage-05/lesson-01.md)
- **Deep ensemble** — Several independently trained networks whose predictions are averaged. Their disagreement estimates epistemic uncertainty (Lakshminarayanan et al. 2017). — [09.2](lessons/stage-09/lesson-02.md)
- **Deflagration** — A reaction front that propagates by heat and mass transfer (conduction, diffusion, radiation) at subsonic speed relative to the unreacted material. Pressure changes across it are small. — [02.2](lessons/stage-02/lesson-02.md)
- **Deflagration-to-detonation transition (DDT)** — The process by which an accelerating deflagration, through confinement, turbulence and shock formation, develops into a detonation. It is taught as a concept only. — [02.2](lessons/stage-02/lesson-02.md)
- **Dempster–Shafer theory** — A belief-function framework that assigns mass to sets of hypotheses. It can represent ignorance, but its combination rule can give counter-intuitive results under strong conflict (Zadeh's example). — [05.6](lessons/stage-05/lesson-06.md)
- **Denavit–Hartenberg (DH) parameters** — A four-parameter convention (a, α, d, θ) for describing each link-to-link transform of a serial manipulator. — [06.3](lessons/stage-06/lesson-03.md)
- **Detonation** — A reaction front coupled to a shock that travels supersonically into the unreacted material. The shock compression initiates the reaction, and the reaction sustains the shock. — [02.2](lessons/stage-02/lesson-02.md)
- **Dijkstra / A*** — Graph shortest-path algorithms. A* adds an admissible heuristic to focus the search on the goal. — [06.8](lessons/stage-06/lesson-08.md)
- **Distribution shift** — A difference between training and deployment data distributions (covariate, label or concept shift). It is a major cause of field failure. — [09.3](lessons/stage-09/lesson-03.md), [09.6](lessons/stage-09/lesson-06.md)
- **Domain adaptation** — Techniques that reduce performance loss when a model trained on a source distribution (for example synthetic images) is applied to a different target distribution (real images). — [09.3](lessons/stage-09/lesson-03.md)
- **Domain randomisation** — Training on synthetic data whose nuisance parameters (texture, lighting, pose, clutter) are randomised widely, so that the real world looks like just another variation (Tobin et al. 2017). — [09.3](lessons/stage-09/lesson-03.md)
- **Drag loading** — Force from dynamic pressure on an object in the flow behind a shock, F = C_d·q·A. It dominates for small or slender targets. — [01.4](lessons/stage-01/lesson-04.md), [04.3](lessons/stage-04/lesson-03.md)
- **Dual-energy X-ray** — Imaging at two photon-energy spectra. The ratio of attenuations estimates the effective atomic number (Z_eff), which allows coarse material classification (organic, inorganic, metal). — [05.3](lessons/stage-05/lesson-03.md)
- **Dynamic pressure** — q = ½ρu², the kinetic-energy density of the flow behind a shock. It produces drag loading on objects and people. For ideal air it can be written q = (5/2)Δp²/(7p₀ + Δp). — [01.4](lessons/stage-01/lesson-04.md), [04.1](lessons/stage-04/lesson-01.md)

## E

- **Edge inference** — Running models on the robot or sensor hardware, under latency, power and comms constraints. — [09.6](lessons/stage-09/lesson-06.md)
- **Effective atomic number (Z_eff)** — A single number summarising how a compound attenuates X-rays as if it were one element. It is estimated by dual-energy imaging. — [05.3](lessons/stage-05/lesson-03.md)
- **Electromagnetic induction (EMI)** — Detection of conductive or magnetic objects by the eddy currents induced in them by a time-varying primary field. The secondary field is sensed by a receive coil. It is the principle of the metal detector. — [05.2](lessons/stage-05/lesson-02.md)
- **Electrostatic discharge (ESD)** — The sudden transfer of charge between bodies at different potential. In this course it is treated as a hazard concept for sensitive materials and electronics. — [01.7](lessons/stage-01/lesson-07.md), [02.3](lessons/stage-02/lesson-03.md)
- **Endsley model** — See Situation awareness. — [06.5](lessons/stage-06/lesson-05.md)
- **Energy storage (battery model)** — Models of a battery's capacity, internal resistance and discharge. They set a robot's mission endurance and peak manipulator power. — [06.4](lessons/stage-06/lesson-04.md), [01.7](lessons/stage-01/lesson-07.md)
- **Enthalpy of formation** — The enthalpy change when one mole of a compound forms from its elements in their standard states. Combined through Hess's law, it gives reaction enthalpies. — [02.1](lessons/stage-02/lesson-01.md)
- **EOD Levels 1–3+** — The IMAS 09.30 / T&EP 09.30 competency ladder for humanitarian EOD personnel. It is used here as an organisational reference only. — [00.2](lessons/stage-00/lesson-02.md)
- **Epistemic uncertainty** — Uncertainty due to limited knowledge or data, for example on out-of-distribution inputs. It can in principle be reduced with more data. Contrast with aleatoric uncertainty. — [09.2](lessons/stage-09/lesson-02.md)
- **Evacuation distance** — A distance, from published public-safety tables, beyond which people should be moved for a given threat size. — [04.4](lessons/stage-04/lesson-04.md), [07.2](lessons/stage-07/lesson-02.md)
- **Evidence-based decision (land release)** — The IMAS principle that areas are defined, reduced or cancelled on documented evidence, not on fear or rumour alone. — [05.7](lessons/stage-05/lesson-07.md)
- **Expected calibration error (ECE)** — A binned estimate of the mean absolute gap between confidence and accuracy, weighted by bin size (Guo et al. 2017). — [09.2](lessons/stage-09/lesson-02.md)
- **Expected value of perfect information (EVPI)** — The expected gain in utility from learning the true state before deciding, compared with deciding now. It is an upper bound on the value of any real test or sensor. — [07.1](lessons/stage-07/lesson-01.md)
- **Explainability** — Methods and interfaces that let users understand why a model produced an output (saliency, exemplars, uncertainty displays). — [09.6](lessons/stage-09/lesson-06.md)
- **Explosive hazard (EH)** — NATO umbrella term for any hazard containing an explosive component, including EO and IEDs (AJP-3.18 Lexicon). — [00.1](lessons/stage-00/lesson-01.md), [03.1](lessons/stage-03/lesson-01.md)
- **Explosive ordnance disposal (EOD)** — The detection, identification, evaluation, render safe, recovery and final disposal of explosive ordnance (IMAS 04.10; AJP-3.18). This course covers its science and decision frameworks, not its procedures. — [00.1](lessons/stage-00/lesson-01.md), [00.2](lessons/stage-00/lesson-02.md)
- **Explosive ordnance (EO)** — All munitions containing explosives. For mine action, IMAS 04.10 includes mines, cluster munitions, unexploded and abandoned ordnance, booby traps, other devices and IEDs. — [00.1](lessons/stage-00/lesson-01.md), [03.1](lessons/stage-03/lesson-01.md)
- **Explosive ordnance reconnaissance (EOR)** — The investigation, detection, examination, identification and reporting of suspected EO in order to determine further action. It is one of the five NATO EOD capability subsets (AJP-3.18). — [00.1](lessons/stage-00/lesson-01.md), [07.2](lessons/stage-07/lesson-02.md)
- **Explosive remnants of war (ERW)** — Unexploded ordnance and abandoned explosive ordnance together (CCW Protocol V; IMAS 04.10). Mines are covered separately. — [00.1](lessons/stage-00/lesson-01.md), [03.1](lessons/stage-03/lesson-01.md), [03.3](lessons/stage-03/lesson-03.md)
- **Explosive train** — The ordered sequence of energetic elements, each initiating the next with increasing output and decreasing sensitivity. Taught here as a systems concept only. — [03.2](lessons/stage-03/lesson-02.md)
- **Extended Kalman filter (EKF)** — A Kalman filter for nonlinear models that linearises the motion and measurement functions about the current estimate using their Jacobians. — [06.6](lessons/stage-06/lesson-06.md), [06.7](lessons/stage-06/lesson-07.md)

## F

- **Fail-safe** — A design property where credible failures drive the system to a safe state, for example a robot stopping and holding on comms loss. — [06.9](lessons/stage-06/lesson-09.md), [03.2](lessons/stage-03/lesson-02.md)
- **Failure modes and effects analysis (FMEA)** — A bottom-up, tabular analysis listing each component's failure modes, their effects on the system, and their severity, occurrence and detectability. It is used to prioritise mitigations. — [06.9](lessons/stage-06/lesson-09.md)
- **False alarm rate (FAR)** — The number of false alarms per unit area, time or item inspected. In mine action it is often reported per m². It trades off against PoD through the detector threshold. — [05.1](lessons/stage-05/lesson-01.md), [05.2](lessons/stage-05/lesson-02.md)
- **Fault tree** — A top-down Boolean model (AND/OR gates) of the combinations of basic events that cause an undesired top event. Its minimal cut sets give the failure combinations and their probabilities. — [06.9](lessons/stage-06/lesson-09.md)
- **Feature-level fusion** — Combining sensor outputs at the level of extracted features before classification. Contrast with decision-level fusion, which combines per-sensor decisions or scores. — [05.6](lessons/stage-05/lesson-06.md)
- **Force feedback (haptics)** — Displaying contact forces from the remote manipulator to the operator's hand. It is subject to stability limits under delay. — [06.5](lessons/stage-06/lesson-05.md)
- **Forward kinematics** — Computing the end-effector pose from joint variables by composing the link transforms. — [06.3](lessons/stage-06/lesson-03.md)
- **Fragment** — A solid piece projected by an explosion. Primary fragments come from the casing; secondary fragments come from surrounding objects. Their velocity decays with drag, and their hazard is assessed statistically. — [01.6](lessons/stage-01/lesson-06.md), [04.4](lessons/stage-04/lesson-04.md)
- **Fresnel zone** — The ellipsoidal region around a radio line of sight. Obstructions within it (especially the first zone) cause diffraction loss even when the optical line of sight is clear. — [06.9](lessons/stage-06/lesson-09.md), [01.7](lessons/stage-01/lesson-07.md)
- **Friedlander waveform** — The idealised pressure–time history of a free-field blast wave: p(t) = p_max(1 − t/t_d)exp(−bt/t_d) for 0 ≤ t ≤ t_d. It has an instantaneous rise, then decay into a negative phase. — [04.1](lessons/stage-04/lesson-01.md)
- **Frontier (exploration)** — The boundary between known-free and unknown cells of a map. Frontier-based exploration drives the robot to frontiers in order to expand the map. — [09.5](lessons/stage-09/lesson-05.md), [06.8](lessons/stage-06/lesson-08.md)
- **Fuze** — The device that initiates a munition's explosive train under the intended conditions and keeps it safe otherwise. It is taught here only as a safety-and-arming systems concept. — [03.2](lessons/stage-03/lesson-02.md)

## G

- **Gaussian noise** — Additive noise with a normal distribution. It is the standard assumption behind the Kalman filter and many detection models. — [05.1](lessons/stage-05/lesson-01.md), [06.6](lessons/stage-06/lesson-06.md)
- **GICHD** — Geneva International Centre for Humanitarian Demining: custodian of IMAS and publisher of mine-action guidance. — [00.1](lessons/stage-00/lesson-01.md)
- **Glazing hazard** — Injury from glass fragments broken by relatively low overpressures. It is a dominant cause of injury in urban blasts. — [04.3](lessons/stage-04/lesson-03.md), [04.4](lessons/stage-04/lesson-04.md)
- **Graph SLAM** — SLAM formulated as a sparse nonlinear least-squares problem over a graph of poses (and landmarks) linked by measurement constraints. — [06.7](lessons/stage-06/lesson-07.md)
- **Ground-penetrating radar (GPR)** — Radar that transmits EM pulses into the ground and records reflections from dielectric contrasts. A point target appears as a hyperbola in a B-scan. — [05.2](lessons/stage-05/lesson-02.md)

## H

- **Hazard division (HD)** — The UN Class 1 subdivision (1.1–1.6) describing the predominant hazard of an explosive article or substance: mass explosion, projection, fire, minor, very insensitive with a mass-explosion hazard, or extremely insensitive articles. — [02.3](lessons/stage-02/lesson-03.md)
- **Height of burst** — The height of an explosion above a surface. Together with distance, it determines the reflection type and the Mach-stem formation. — [04.2](lessons/stage-04/lesson-02.md)
- **HERO** — Hazards of Electromagnetic Radiation to Ordnance: the possibility that RF energy induces currents in electrically initiated items. Treated as a safety concept only. — [01.7](lessons/stage-01/lesson-07.md)
- **Hess's law** — Enthalpy is a state function, so reaction enthalpy is the sum of the enthalpies of any path of steps. In particular, it equals the products' formation enthalpies minus the reactants'. — [02.1](lessons/stage-02/lesson-01.md)
- **Homogeneous transform** — A 4×4 matrix in SE(3) combining a rotation R and a translation p. Transforms compose by matrix multiplication. — [06.2](lessons/stage-06/lesson-02.md)
- **Hopkinson–Cranz scaling** — Cube-root scaling: two charges of the same explosive produce the same overpressure at the same scaled distance Z = R/W^(1/3), and impulse and time scale by W^(1/3). — [01.5](lessons/stage-01/lesson-05.md), [04.1](lessons/stage-04/lesson-01.md)
- **Hugoniot** — The locus of end states reachable from a given initial state through a single shock, in the pressure–specific-volume plane. — [01.3](lessons/stage-01/lesson-03.md), [02.2](lessons/stage-02/lesson-02.md)
- **Human-in-the-loop (HITL)** — A system design in which a human approves, corrects or overrides automated outputs at defined points in the decision chain. — [09.6](lessons/stage-09/lesson-06.md), [07.1](lessons/stage-07/lesson-01.md)
- **Hyperbola (GPR)** — The B-scan signature of a point scatterer. Its shape encodes depth and the propagation velocity of the soil. — [05.2](lessons/stage-05/lesson-02.md)
- **Hyperspectral imaging** — Imaging in many narrow contiguous spectral bands. The resulting per-pixel spectrum supports material discrimination. — [05.5](lessons/stage-05/lesson-05.md)

## I

- **IATG** — International Ammunition Technical Guidelines: the UN (UNODA / UN SaferGuard) guidelines for through-life management of conventional ammunition stockpiles. — [00.1](lessons/stage-00/lesson-01.md), [02.3](lessons/stage-02/lesson-03.md), [04.3](lessons/stage-04/lesson-03.md)
- **IED** — Improvised explosive device: a device placed or fabricated in an improvised manner that incorporates explosive or other destructive materials and is designed to destroy, incapacitate, harass or distract (AJP-3.18 / AAP-6 sense). Treated at category level only. — [03.4](lessons/stage-03/lesson-04.md)
- **IEDD** — Improvised explosive device disposal: the location, identification, rendering safe and final disposal of IEDs (IMAS 04.10; AJP-3.18). It is one of the five NATO EOD capability subsets. — [00.1](lessons/stage-00/lesson-01.md), [03.4](lessons/stage-03/lesson-04.md)
- **IMAS** — International Mine Action Standards: standards maintained by UNMAS, with GICHD as custodian, that govern humanitarian mine action. — [00.1](lessons/stage-00/lesson-01.md), [05.7](lessons/stage-05/lesson-07.md)
- **Impulse** — The time integral of force or pressure. For a blast wave, i = ∫p(t)dt over the positive phase (Pa·s). It governs the response of stiff, short-period targets. — [01.1](lessons/stage-01/lesson-01.md), [04.1](lessons/stage-04/lesson-01.md)
- **Impulsive regime** — Loading that ends before the structure responds significantly (t_d ≪ T). Response then depends on impulse, not on peak pressure. — [01.6](lessons/stage-01/lesson-06.md), [04.3](lessons/stage-04/lesson-03.md)
- **Incident command system (ICS)** — A standardised, modular command structure (command, operations, planning, logistics, finance) for managing incidents. It is the interface a bomb squad works within. — [07.2](lessons/stage-07/lesson-02.md), [00.2](lessons/stage-00/lesson-02.md)
- **Information gain** — The expected reduction in entropy of a belief from an observation. It is used to choose sensors and viewpoints. — [05.6](lessons/stage-05/lesson-06.md), [09.5](lessons/stage-09/lesson-05.md)
- **Inhabited building distance (IBD)** — The minimum separation between a potential explosion site and inhabited buildings, expressed as Z·W^(1/3) (IATG 02.20; DESR 6055.09). — [04.3](lessons/stage-04/lesson-03.md), [04.4](lessons/stage-04/lesson-04.md)
- **Intersection over union (IoU)** — The area of overlap divided by the area of union of predicted and true regions. It is used to match detections and score segmentation. — [09.1](lessons/stage-09/lesson-01.md)
- **Inverse kinematics** — Finding joint variables that achieve a desired end-effector pose. There may be multiple solutions or none. It is solved analytically or iteratively. — [06.3](lessons/stage-06/lesson-03.md)
- **Inverse problem** — Inferring causes (for example seat location or charge size in YU) from observed effects. It is typically ill-posed and needs priors or regularisation. — [08.2](lessons/stage-08/lesson-02.md), [05.5](lessons/stage-05/lesson-05.md)
- **Ion mobility spectrometry (IMS)** — Trace detection that ionises sampled vapour or particles and separates the ions by drift time in an electric field against a counter-flowing gas. — [05.4](lessons/stage-05/lesson-04.md)

## J

- **Jacobian (manipulator)** — The matrix J(q) mapping joint velocities to end-effector twist, v = J(q)q̇. It becomes singular where the arm loses a direction of motion. — [06.3](lessons/stage-06/lesson-03.md)

## K

- **Kalman filter** — The optimal recursive estimator for linear-Gaussian systems. It propagates a mean and covariance through predict and update steps. — [06.6](lessons/stage-06/lesson-06.md)
- **Kinematic chain** — Links connected by joints from the base to the end-effector. — [06.3](lessons/stage-06/lesson-03.md)
- **Kingery–Bulmash curves** — Empirical polynomial fits of blast parameters against scaled distance for TNT hemispherical surface and spherical free-air bursts. The public route to them is UFC 3-340-02 Ch. 2; they are valid for Z ≤ 40. — [04.1](lessons/stage-04/lesson-01.md), [04.2](lessons/stage-04/lesson-02.md)
- **Kinney–Graham fit** — An analytic expression for peak overpressure against scaled distance for spherical free-air TNT bursts, valid to Z ≈ 500 (IATG 01.80). — [04.1](lessons/stage-04/lesson-01.md)

## L

- **Land release** — The process of applying all reasonable effort to identify, define and remove all presence and suspicion of explosive ordnance, through non-technical survey, technical survey and/or clearance (IMAS 04.10, 07.11). — [05.7](lessons/stage-05/lesson-07.md)
- **Latency** — The delay between an operator command and the observed response, including the round-trip comms delay. Above roughly 1 s, continuous closed-loop teleoperation degrades towards move-and-wait. — [06.5](lessons/stage-06/lesson-05.md), [06.9](lessons/stage-06/lesson-09.md)
- **Lateral range curve** — The probability of detecting a target as a function of its perpendicular distance from the searcher's track. Its integral is the sweep width. — [05.7](lessons/stage-05/lesson-07.md)
- **Link budget** — The accounting, in dB, of transmit power, antenna gains, path and other losses, and receiver sensitivity. The margin is what remains for fading. — [06.9](lessons/stage-06/lesson-09.md)
- **Localisation** — Estimating a robot's pose relative to a map or frame, for example by Monte Carlo localisation. — [06.6](lessons/stage-06/lesson-06.md)
- **Loop closure** — Recognising a previously visited place in SLAM and adding a constraint that corrects accumulated drift. — [06.7](lessons/stage-06/lesson-07.md)
- **Loss of comms behaviour** — The pre-defined autonomous response of a robot when its link drops (stop, hold, retro-traverse to the last good-link point). — [06.9](lessons/stage-06/lesson-09.md)

## M

- **Mach number** — The ratio of a flow or wave speed to the local sound speed. The shock Mach number M fixes the overpressure ratio through Rankine–Hugoniot. — [01.3](lessons/stage-01/lesson-03.md)
- **Mach stem** — The near-vertical shock formed where the incident and reflected shocks merge near a surface at large incidence angles (Mach reflection). Pressures in it can exceed those at normal reflection. — [01.4](lessons/stage-01/lesson-04.md), [04.2](lessons/stage-04/lesson-02.md)
- **Magnetic susceptibility (soil)** — The soil property that produces ground signal in metal detectors, with frequency-dependent effects. It is characterised in CWA 14747-2. — [05.2](lessons/stage-05/lesson-02.md)
- **Manipulability** — A measure of how easily an arm can move its end-effector in all directions at a configuration, for example w = √det(JJᵀ). It falls to zero at singularities. — [06.3](lessons/stage-06/lesson-03.md)
- **Mass spectrometry (MS)** — Identifying compounds by the mass-to-charge ratio of their ions. It offers higher selectivity than IMS for trace detection. — [05.4](lessons/stage-05/lesson-04.md), [08.3](lessons/stage-08/lesson-03.md)
- **Millimetre-wave imaging (mmW)** — Imaging at roughly 30–300 GHz. It penetrates clothing and many dielectrics, reflects from skin and metal, and is used for concealed-object screening. — [05.5](lessons/stage-05/lesson-05.md)
- **Mine** — A munition designed to be placed under, on or near the ground or another surface and to be exploded by the presence, proximity or contact of a person or vehicle (IMAS 04.10). — [03.3](lessons/stage-03/lesson-03.md)
- **Monte Carlo dropout** — Keeping dropout active at test time and averaging several stochastic forward passes to approximate a Bayesian predictive distribution (Gal & Ghahramani 2016). — [09.2](lessons/stage-09/lesson-02.md)
- **Monte Carlo localisation (MCL)** — Particle-filter localisation against a known map. — [06.6](lessons/stage-06/lesson-06.md)
- **Move-and-wait** — The teleoperation strategy under large delay in which the operator makes a small open-loop move and then waits for feedback before the next move (Ferrell 1965). — [06.5](lessons/stage-06/lesson-05.md)
- **Multimodal fusion** — Combining complementary sensing modalities (RGB, depth, thermal, radar) after spatial and temporal registration. — [09.4](lessons/stage-09/lesson-04.md), [05.6](lessons/stage-05/lesson-06.md)

## N

- **Negative phase** — The part of a blast pressure history below ambient, after the positive phase. It is often neglected, but matters for glazing and light structures. — [04.1](lessons/stage-04/lesson-01.md)
- **Net explosive quantity (NEQ)** — The total mass of explosive substance in an item or stack, excluding packaging and casing. It is the W used in quantity-distance calculations (also called NEW). — [02.3](lessons/stage-02/lesson-03.md), [04.3](lessons/stage-04/lesson-03.md)
- **Next-best-view** — Selecting the next sensor pose that maximises expected information gain about the scene or object. — [09.5](lessons/stage-09/lesson-05.md)
- **Noise-equivalent temperature difference (NETD)** — The temperature difference that produces a signal equal to a thermal camera's noise. It is the thermal-imaging sensitivity figure, in mK. — [05.5](lessons/stage-05/lesson-05.md), [09.4](lessons/stage-09/lesson-04.md)
- **Non-technical survey (NTS)** — The collection and analysis of data, without technical intervention, about the presence, type, distribution and surroundings of EO contamination, used to define hazardous areas (IMAS 04.10). — [05.7](lessons/stage-05/lesson-07.md)
- **Normal shock** — A shock perpendicular to the flow direction. Its jump conditions are one-dimensional. — [01.3](lessons/stage-01/lesson-03.md)
- **Nuclear quadrupole resonance (NQR)** — RF spectroscopy of quadrupolar nuclei (for example ¹⁴N) in solids, with no external magnet. Its compound-specific resonances enable bulk identification, but the signals are weak. — [05.3](lessons/stage-05/lesson-03.md), [05.5](lessons/stage-05/lesson-05.md)

## O

- **Oblique reflection** — Reflection of a shock from a surface at an angle. Above a critical angle it becomes Mach reflection. — [01.4](lessons/stage-01/lesson-04.md)
- **Occupancy grid** — A map that discretises space into cells, each holding a probability (usually as log-odds) of being occupied. — [06.7](lessons/stage-06/lesson-07.md)
- **Operator control unit (OCU)** — The operator's station for a teleoperated robot: displays, input devices and the radio link. — [06.1](lessons/stage-06/lesson-01.md), [06.5](lessons/stage-06/lesson-05.md)
- **Out-of-distribution (OOD) detection** — Recognising inputs unlike the training data, so that the model can abstain. — [09.2](lessons/stage-09/lesson-02.md), [09.6](lessons/stage-09/lesson-06.md)
- **Overpressure** — Pressure above ambient, Δp = p − p₀. Peak side-on (incident) overpressure is the headline blast parameter. — [01.3](lessons/stage-01/lesson-03.md), [04.1](lessons/stage-04/lesson-01.md)

## P

- **Particle filter** — A sequential Monte Carlo Bayes filter that represents the belief as weighted samples. It handles nonlinear, non-Gaussian and multimodal problems. — [06.6](lessons/stage-06/lesson-06.md)
- **Path loss** — The reduction in radio signal power with distance and environment, modelled as free-space (∝ d²) or log-distance with exponent n. — [06.9](lessons/stage-06/lesson-09.md), [01.7](lessons/stage-01/lesson-07.md)
- **Photogrammetry** — Recovering 3-D geometry from overlapping photographs by feature matching, camera calibration and bundle adjustment (structure from motion). — [08.2](lessons/stage-08/lesson-02.md)
- **PID control** — A proportional–integral–derivative feedback controller. It is the workhorse of joint and wheel-speed loops. — [06.4](lessons/stage-06/lesson-04.md)
- **POMDP** — Partially observable Markov decision process: a sequential decision model (states, actions, observations, transition and observation models, rewards) solved over belief states. — [07.1](lessons/stage-07/lesson-01.md), [09.5](lessons/stage-09/lesson-05.md)
- **Positive phase duration (t_d)** — The time for which the pressure at a point stays above ambient after the shock arrives. — [04.1](lessons/stage-04/lesson-01.md)
- **Predictive display** — A teleoperation display that renders the model-predicted robot state immediately while delayed video catches up. — [06.5](lessons/stage-06/lesson-05.md)
- **Pressure–impulse (P–I) diagram** — Iso-damage curves in the (peak pressure, impulse) plane. The asymptotes give the impulsive and quasi-static thresholds for a given target. — [01.6](lessons/stage-01/lesson-06.md), [04.3](lessons/stage-04/lesson-03.md)
- **Probability of detection (POD / PoD)** — The probability that a detector or search reports a target that is present. It is estimated in blind trials together with FAR (CWA 14747-1). — [05.1](lessons/stage-05/lesson-01.md), [05.7](lessons/stage-05/lesson-07.md)
- **Product of exponentials (PoE)** — Manipulator forward kinematics expressed as a product of matrix exponentials of joint screw axes (Lynch & Park). — [06.3](lessons/stage-06/lesson-03.md)
- **Progressive collapse** — The spread of an initial local failure (for example the loss of a column) from element to element, resulting in collapse disproportionate to the initiating damage. — [04.3](lessons/stage-04/lesson-03.md)
- **Protective design** — The design of structures, barriers and layouts to limit blast and fragment effects to tolerable levels. — [04.3](lessons/stage-04/lesson-03.md)
- **Pulse induction (PI)** — An EMI technique that switches off the transmit current abruptly and samples the decaying eddy-current response. It is less sensitive to some soil effects than frequency-domain methods. — [05.2](lessons/stage-05/lesson-02.md)

## Q

- **Quality assurance / quality control (QA/QC)** — In mine action, QA is confidence-building oversight of processes and QC is inspection of the product (for example sampling released land) against requirements. — [05.7](lessons/stage-05/lesson-07.md)
- **Quantity-distance (QD)** — The system of minimum separation distances between explosive stocks and exposed sites, set by NEQ, hazard division and exposure type, generally as Z·W^(1/3). — [04.3](lessons/stage-04/lesson-03.md), [02.3](lessons/stage-02/lesson-03.md)
- **Quantity of explosive (W)** — The TNT-equivalent mass used in scaling. In this course it is always expressed in YU. — [01.5](lessons/stage-01/lesson-05.md)
- **Quasi-static pressure (QSP)** — The slowly decaying gas pressure left inside a confined or partly vented volume after the initial shocks have reverberated. — [04.2](lessons/stage-04/lesson-02.md)
- **Quasi-static regime** — Loading that is long compared with the structure's natural period (t_d ≫ T). Response then depends on peak pressure, not on impulse. — [01.6](lessons/stage-01/lesson-06.md), [04.3](lessons/stage-04/lesson-03.md)

## R

- **Radiography** — Transmission imaging of an object's internal structure with X-rays. In this course it is taught for its physics and image interpretation concepts. — [05.3](lessons/stage-05/lesson-03.md)
- **Rankine–Hugoniot relations** — The jump conditions across a shock, derived from conservation of mass, momentum and energy. For ideal air they link Mach number to the pressure, density and temperature ratios. — [01.3](lessons/stage-01/lesson-03.md)
- **Rarefaction wave** — An expansion wave across which pressure and density decrease smoothly. It is the counterpart of a shock in a Riemann problem. — [01.3](lessons/stage-01/lesson-03.md)
- **Rayleigh line** — A straight line in the p–v plane joining the initial and final states of a steady wave. Its slope is set by the wave speed and mass flux. — [02.2](lessons/stage-02/lesson-02.md)
- **Receiver operating characteristic (ROC)** — The curve of true-positive rate (PoD) against false-positive rate as the decision threshold varies. The best operating point depends on base rates and costs. — [05.1](lessons/stage-05/lesson-01.md), [09.1](lessons/stage-09/lesson-01.md)
- **Reflected pressure** — The peak pressure on a surface struck by a blast wave. At normal incidence it is 2 to 8 times the incident overpressure for ideal air, and higher for real gases near the source. — [01.4](lessons/stage-01/lesson-04.md), [04.2](lessons/stage-04/lesson-02.md)
- **Reflection coefficient** — The ratio of reflected to incident peak overpressure, C_r = Δp_r/Δp. It depends on incident strength and angle. — [01.4](lessons/stage-01/lesson-04.md), [04.2](lessons/stage-04/lesson-02.md)
- **Registration (multisensor)** — Aligning data from different sensors in space and time using calibrated extrinsics and synchronisation. — [09.4](lessons/stage-09/lesson-04.md)
- **Remote sensing** — Acquiring information without contact, for example from drone, aircraft or satellite imagery. — [05.5](lessons/stage-05/lesson-05.md)
- **Render safe (concept)** — The EOD outcome family of interrupting a hazard's function so that it can no longer function as designed. In this course it is defined conceptually only, as one of three disposal-outcome families (remove, destroy in place, render safe). No method is taught. — [07.2](lessons/stage-07/lesson-02.md), [00.1](lessons/stage-00/lesson-01.md)
- **Residual risk** — The risk remaining after land release or other risk treatment. Mine action accepts that it is not zero and manages it through liability and post-clearance mechanisms. — [05.7](lessons/stage-05/lesson-07.md), [07.1](lessons/stage-07/lesson-01.md)
- **Riemann problem** — An initial-value problem with piecewise-constant data and one discontinuity, as in the shock tube. Its solution is a combination of shocks, contacts and rarefactions. — [01.3](lessons/stage-01/lesson-03.md)
- **Risk-aware planning** — Planning that optimises expected cost subject to constraints on risk measures (for example chance constraints or CVaR). — [09.5](lessons/stage-09/lesson-05.md), [06.8](lessons/stage-06/lesson-08.md)
- **Risk (ISO / IATG sense)** — The combination of the probability of harm and the severity of that harm. — [07.1](lessons/stage-07/lesson-01.md), [04.3](lessons/stage-04/lesson-03.md)
- **RRT / RRT*** — Rapidly-exploring random tree: a sampling-based planner that grows a tree towards random samples. RRT* adds rewiring and is asymptotically optimal. — [06.8](lessons/stage-06/lesson-08.md)

## S

- **Sachs scaling** — A correction of blast parameters for ambient pressure and temperature (for example at altitude), with distance, pressure, impulse and time factors (IATG 01.80). — [01.5](lessons/stage-01/lesson-05.md)
- **Safety-and-arming (S&A)** — The fuze subsystem that keeps a munition safe until the intended environments occur. Modelled in this course as a state machine with at least two independent safety features driven by different environmental stimuli (public MIL-STD-1316 principle). — [03.2](lessons/stage-03/lesson-02.md)
- **Scaled distance (Z)** — Z = R/W^(1/3) (m/kg^(1/3)), with W the TNT-equivalent mass. Equal Z gives equal peak overpressure for geometrically similar bursts. — [01.5](lessons/stage-01/lesson-05.md), [04.1](lessons/stage-04/lesson-01.md), [04.4](lessons/stage-04/lesson-04.md)
- **Scene zoning** — Division of a post-blast scene into areas (for example seat, inner and outer perimeter) for safety, search and evidence control. — [08.1](lessons/stage-08/lesson-01.md)
- **Search pattern (scene)** — A systematic method of covering a scene: grid, line, spiral or zone. It is chosen for completeness and documentation. — [08.1](lessons/stage-08/lesson-01.md)
- **Search theory** — The operations-research theory of allocating search effort to maximise the probability of detection. It was founded by Koopman and extended by Stone. — [05.7](lessons/stage-05/lesson-07.md)
- **Seat of explosion** — The location of the explosive charge at the moment of functioning. It is inferred from damage and fragment patterns. — [08.2](lessons/stage-08/lesson-02.md)
- **Secondary hazard** — A hazard other than the primary item: another device, fire, structural instability, broken utilities, or CBRN release. It is assessed in every incident. — [04.4](lessons/stage-04/lesson-04.md), [07.2](lessons/stage-07/lesson-02.md)
- **Selective prediction** — A model that abstains (defers to a human) when its uncertainty exceeds a threshold, trading coverage for accuracy. — [09.2](lessons/stage-09/lesson-02.md), [09.6](lessons/stage-09/lesson-06.md)
- **Semenov theory** — The thermal-explosion theory for a well-stirred system. Runaway occurs when heat generation (Arrhenius) exceeds heat loss (Newtonian) with no stable intersection. Frank-Kamenetskii extends it to conduction-limited systems. — [02.3](lessons/stage-02/lesson-03.md)
- **Sensitivity (energetic material)** — The ease with which a material can be initiated by a given stimulus (impact, friction, ESD, heat). It is measured by standard tests and informs classification. — [02.3](lessons/stage-02/lesson-03.md)
- **Sensor fusion** — Combining measurements from several sensors to obtain better estimates or decisions than any one sensor gives. It must account for correlated errors. — [05.6](lessons/stage-05/lesson-06.md)
- **Shielding** — Interposing a barrier (structure, earth, armour) to absorb or deflect blast and fragments. — [04.4](lessons/stage-04/lesson-04.md), [07.2](lessons/stage-07/lesson-02.md)
- **Shock tube** — A tube divided by a diaphragm into high- and low-pressure sections. Bursting the diaphragm produces a shock, a contact surface and a rarefaction; it is the canonical Riemann problem. — [01.3](lessons/stage-01/lesson-03.md)
- **Shock wave** — A propagating, near-discontinuous jump in pressure, density, temperature and velocity, travelling supersonically relative to the medium ahead. — [01.3](lessons/stage-01/lesson-03.md)
- **Signal detection theory (SDT)** — The framework separating a detector's sensitivity (d′) from its decision criterion, which leads to ROC analysis. — [05.1](lessons/stage-05/lesson-01.md)
- **Single-degree-of-freedom (SDOF) model** — Representation of a structural element as an equivalent mass–spring system, m·ẍ + k·x = F(t), used to estimate blast response. — [01.6](lessons/stage-01/lesson-06.md), [04.3](lessons/stage-04/lesson-03.md)
- **Singularity (kinematic)** — A configuration where the manipulator Jacobian loses rank. The end-effector cannot move in some direction, and joint rates needed to approach it grow without bound. — [06.3](lessons/stage-06/lesson-03.md)
- **Situation awareness (SA)** — Perception of elements in the environment, comprehension of their meaning, and projection of their future status (Endsley 1995, levels 1–3). — [06.5](lessons/stage-06/lesson-05.md), [07.2](lessons/stage-07/lesson-02.md)
- **Skid-steer** — A drive in which a vehicle turns by driving its left and right tracks or wheels at different speeds. Its kinematics are affected by track slip. — [06.4](lessons/stage-06/lesson-04.md)
- **SLAM** — Simultaneous localisation and mapping: estimating a robot's trajectory and a map of an unknown environment jointly. — [06.7](lessons/stage-06/lesson-07.md)
- **SO(3) / SE(3)** — The Lie groups of 3-D rotations and of rigid-body motions (rotation plus translation). — [06.2](lessons/stage-06/lesson-02.md)
- **Sound speed** — c = √(γRT) in an ideal gas, about 343 m/s in air at 20 °C. — [01.2](lessons/stage-01/lesson-02.md), [01.3](lessons/stage-01/lesson-03.md)
- **Specific heat ratio (γ)** — γ = c_p/c_v, equal to 1.4 for diatomic ideal air. It enters sound speed and every shock relation. — [01.2](lessons/stage-01/lesson-02.md), [01.3](lessons/stage-01/lesson-03.md)
- **Stabiliser depletion** — The consumption over time of the stabilisers added to nitrocellulose-based propellants to scavenge decomposition products. Once they are depleted, autocatalytic decomposition can lead to self-heating. — [02.3](lessons/stage-02/lesson-03.md), [03.3](lessons/stage-03/lesson-03.md)
- **Stagnation pressure** — The pressure reached when a flow is brought to rest isentropically. For a blast wave, it is related to overpressure plus dynamic pressure on a facing surface. — [01.4](lessons/stage-01/lesson-04.md)
- **STANAG** — NATO Standardization Agreement: the record of nations' agreement to implement a standard. STANAG 2628 ratifies AJP-3.18. — [00.2](lessons/stage-00/lesson-02.md)
- **Standoff** — Distance between a hazard and the people or assets to be protected. It is the most effective protective measure because blast and fragment effects fall steeply with distance. — [04.4](lessons/stage-04/lesson-04.md), [07.2](lessons/stage-07/lesson-02.md)
- **Stand-off detection** — Detecting a hazard from a distance without approach or contact. It is limited by signal strength, clutter and atmospheric effects. — [05.5](lessons/stage-05/lesson-05.md), [05.4](lessons/stage-05/lesson-04.md)
- **State machine** — A model of a system as discrete states and guarded transitions. It is used in this course to abstract safety-and-arming logic and robot fail-safe behaviours. — [03.2](lessons/stage-03/lesson-02.md), [06.9](lessons/stage-06/lesson-09.md)
- **Submunition** — An explosive munition dispersed or released by a cluster munition and designed to function by detonating an explosive charge before, on or after impact. — [03.3](lessons/stage-03/lesson-03.md)
- **Supervisory control** — A control mode in which the human sets goals and monitors while the automation closes the low-level loops (Sheridan). — [06.5](lessons/stage-06/lesson-05.md), [09.5](lessons/stage-09/lesson-05.md)
- **Suspected hazardous area (SHA)** — An area where there is reasonable suspicion of EO contamination on the basis of indirect evidence (IMAS 04.10). — [05.7](lessons/stage-05/lesson-07.md)
- **Suspicious item** — An item whose characteristics or context give reasons to believe it may be hazardous. Contrast with an unattended item, which lacks such indicators. The classification drives the response. — [03.4](lessons/stage-03/lesson-04.md), [07.2](lessons/stage-07/lesson-02.md)
- **Sweep width** — In search theory, the effective width W such that the expected number of detections equals that of a perfect detector with width W. It condenses the lateral-range curve into one number. — [05.7](lessons/stage-05/lesson-07.md)
- **Synthetic data** — Training or test data generated by simulation or rendering, with free, exact labels. Its value depends on how well it covers the real distribution. — [09.3](lessons/stage-09/lesson-03.md)

## T

- **Technical exploitation** — The scientific and technical analysis of recovered material to generate intelligence and evidence. — [08.3](lessons/stage-08/lesson-03.md), [03.4](lessons/stage-03/lesson-04.md)
- **Technical survey (TS)** — The collection and analysis of data, using technical interventions, about the presence, type, distribution and surroundings of EO contamination (IMAS 04.10). — [05.7](lessons/stage-05/lesson-07.md)
- **Teleoperation** — Direct remote control of a robot by a human operator through a communication link, using feedback from the robot's sensors. — [06.5](lessons/stage-06/lesson-05.md)
- **Temperature scaling** — Post-hoc calibration that divides the logits by a single learned temperature T > 0 (Guo et al. 2017). — [09.2](lessons/stage-09/lesson-02.md)
- **Test and evaluation (T&E)** — Structured measurement of system performance against requirements, for example with blind trials, confidence intervals and representative conditions. — [05.1](lessons/stage-05/lesson-01.md), [09.6](lessons/stage-09/lesson-06.md), [06.1](lessons/stage-06/lesson-01.md)
- **Tether** — A wired link between robot and OCU. It gives robust bandwidth and immunity to jamming at the cost of range and entanglement. — [06.9](lessons/stage-06/lesson-09.md)
- **Thermal infrared (IR)** — Imaging of emitted radiation, typically at 8–14 μm. Buried objects can show up through diurnal temperature contrast. — [05.5](lessons/stage-05/lesson-05.md)
- **Thermal neutron analysis (TNA)** — Interrogation in which thermal-neutron capture produces characteristic gamma rays (for example from nitrogen), revealing elemental composition. — [05.3](lessons/stage-05/lesson-03.md)
- **Thermal runaway** — Self-accelerating heating that occurs when a reaction's heat generation grows faster with temperature than the heat loss can. — [02.3](lessons/stage-02/lesson-03.md)
- **Threat assessment** — The structured evaluation of what a hazard may be and how it may function or be targeted, at national, area and scene levels (UN IEDD Standards). — [03.4](lessons/stage-03/lesson-04.md), [07.1](lessons/stage-07/lesson-01.md)
- **Time–distance–shielding** — The three generic protective levers: minimise exposure time, maximise distance, and interpose protection. They apply to blast, fragments and radiation alike. — [07.2](lessons/stage-07/lesson-02.md), [04.4](lessons/stage-04/lesson-04.md)
- **TNT equivalence** — The mass of TNT that would produce the same blast parameter (pressure or impulse) as a given charge. It depends on the parameter and on distance. Here it is expressed in yield units (YU). — [01.5](lessons/stage-01/lesson-05.md), [04.1](lessons/stage-04/lesson-01.md)
- **Tolerable risk** — The level of risk accepted in a given context on the basis of current societal values (ISO/IEC Guide 51; IATG 02.10; IMAS). — [07.1](lessons/stage-07/lesson-01.md), [04.3](lessons/stage-04/lesson-03.md)
- **Tracked vs wheeled mobility** — The trade-off between ground pressure, traction and stair-climbing (tracks) and efficiency, speed and simplicity (wheels). — [06.4](lessons/stage-06/lesson-04.md)

## U

- **Uncertainty quantification (UQ)** — Estimating and communicating the uncertainty of predictions, both aleatoric and epistemic. — [09.2](lessons/stage-09/lesson-02.md)
- **Unexploded ordnance (UXO)** — Explosive ordnance that has been primed, fuzed, armed or otherwise prepared for use and used in an armed conflict: fired, dropped, launched or projected, and that should have exploded but did not (IMAS 04.10). — [00.1](lessons/stage-00/lesson-01.md), [03.1](lessons/stage-03/lesson-01.md)
- **Unified command** — An ICS arrangement in which agencies with jurisdiction jointly set objectives under a single plan. — [07.2](lessons/stage-07/lesson-02.md)
- **Unscented Kalman filter (UKF)** — A Kalman filter that propagates deterministically chosen sigma points through the nonlinear models instead of linearising them. — [06.6](lessons/stage-06/lesson-06.md)

## V

- **Value of information (VOI)** — The expected improvement in decision utility from obtaining an observation before acting. It is zero if no possible result would change the decision. — [07.1](lessons/stage-07/lesson-01.md), [05.6](lessons/stage-05/lesson-06.md), [09.5](lessons/stage-09/lesson-05.md)
- **Vapour pressure** — The equilibrium pressure of a substance's vapour over its condensed phase. It limits the concentration available to trace and canine detection and is strongly temperature dependent. — [05.4](lessons/stage-05/lesson-04.md)
- **Venting** — Relief of confined-explosion pressure through openings or frangible panels. It reduces the quasi-static pressure and its duration. — [04.2](lessons/stage-04/lesson-02.md)

## W

- **Workload** — The demand placed on an operator's cognitive resources. It is measured, for example, by NASA-TLX, and high workload degrades SA. — [06.5](lessons/stage-06/lesson-05.md)

## Y

- **Yield unit (YU)** — The course's abstract unit of TNT-equivalent energy release, used in all simulations and exercises instead of real quantities. — [01.5](lessons/stage-01/lesson-05.md), [04.1](lessons/stage-04/lesson-01.md)

## Z

- **Z_eff** — See Effective atomic number. — [05.3](lessons/stage-05/lesson-03.md)
- **ZND model** — Zel'dovich–von Neumann–Döring model: a detonation as a leading inert shock (von Neumann spike) followed by a finite reaction zone that ends at the CJ state. — [02.2](lessons/stage-02/lesson-02.md)

---

257 terms. Standards cited here are mapped in [references/standards.md](references/standards.md).
