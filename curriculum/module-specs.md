# Module specifications

Deliverable **3** (`plan.md` §20): for every module — prerequisites, learning objectives, theory,
reading, visual explanation, practical exercise, simulation, programming, assessment, time and
what comes next. Generated from the lessons by `scripts/build_nav.py`; the lesson itself is the
full specification.

## Stage 0 · Orientation

### [00.1 · What EOD is: the field, its organisations and its vocabulary](lessons/stage-00/lesson-01.md)

| Field | Specification |
|---|---|
| Prerequisites | None. This is the entry point of the course. It helps to have skimmed the [course outline](curriculum/course-outline.md). **Estimated time** 3 h (1.5 h reading · 1 h classification exercises · 0.5 h programming) |
| Estimated time | 3 h (1.5 h reading · 1 h classification exercises · 0.5 h programming) |
| Level | Beginner |
| Learning objectives | 1. Name the four professional domains of EOD and state, for each, its governing standards, the<br>2. Define EO, UXO, AXO, ERW, IED, mine and explosive hazard (EH) as IMAS and NATO use them, and<br>3. Classify a described (fictional) situation into a hazard category and a responsible organisation,<br>4. Draw the life-cycle of an explosive hazard from manufacture to final disposal and say at which<br>5. Distinguish the role titles (bomb technician, EOD operator/technician, Ammunition Technician,<br>6. Explain, with a simple reliability model, why training is long and why recertification exists. |
| Theory | 1. Four domains, one core · 2. The vocabulary: IMAS and NATO definitions · 3. The life-cycle of an explosive hazard · 4. Who does the work: role titles · 5. Why the training is long: a reliability argument · 6. The scale of the problem: a quantitative aside |
| Visual explanation | mermaid diagram + embedded simulator |
| Simulation | [scene-assessment](sims/scene-assessment/index.html) |
| Programming | [p12-hitl-decision](projects/p12-hitl-decision/README.md) |
| Reading | 6 selected items (see lesson) |
| Assessment | 7 questions + hidden-answer exercises; stage gate [assessments/stage-00.md](assessments/stage-00.md) |
| Next | [00.2 How EOD organisations operate](lessons/stage-00/lesson-02.md), then [01.1 Mechanics refresher](lessons/stage-01/lesson-01.md). |

### [00.2 · How EOD organisations operate](lessons/stage-00/lesson-02.md)

| Field | Specification |
|---|---|
| Prerequisites | [00.1 What EOD is](lessons/stage-00/lesson-01.md) (domains, terminology, life-cycle) · basic probability (Poisson processes) for §7. **Estimated time** 3 h (1.25 h theory · 0.5 h Sim A tutorial · 1.25 h data-model design exercise) |
| Estimated time | 3 h (1.25 h theory · 0.5 h Sim A tutorial · 1.25 h data-model design exercise) |
| Level | Beginner |
| Learning objectives | 1. Describe a generic EOD command structure and the responsibilities of team members, team leaders,<br>2. Explain the IMAS EOD Level 1 / 2 / 3 / 3+ ladder, US bomb-technician certification (HDS) and<br>3. List NATO AJP-3.18's five EOD capability subsets and the operating domains, and say why some<br>4. Walk a fictional incident through the conceptual life-cycle *call → isolate → assess → act →<br>5. Use Little's law and the Erlang-C model to estimate the team capacity needed for a given call<br>6. Design and test a data model for incident reporting that meets field constraints (offline, |
| Theory | 1. Command structure and roles · 2. Competence and certification · 3. NATO: capability subsets and domains · 4. The incident life-cycle (conceptual) · 5. Reporting and data · 6. Where technology plugs in · 7. Capacity: how many teams does a squad need? |
| Visual explanation | mermaid diagram + embedded simulator |
| Simulation | [scene-assessment](sims/scene-assessment/index.html) |
| Programming | [p12-hitl-decision](projects/p12-hitl-decision/README.md) |
| Reading | 6 selected items (see lesson) |
| Assessment | 5 questions + hidden-answer exercises; stage gate [assessments/stage-00.md](assessments/stage-00.md) |
| Next | [01.1 Mechanics refresher](lessons/stage-01/lesson-01.md) (physics path), or [03.1 Hazard taxonomy](lessons/stage-03/lesson-01.md) and [05.1 Detection theory](lessons/stage-05/lesson-01.md), which also depend on this lesson. |

## Stage 1 · Physics foundations

### [01.1 · Mechanics refresher for energetic events](lessons/stage-01/lesson-01.md)

| Field | Specification |
|---|---|
| Prerequisites | [00.2 How EOD organisations operate](lessons/stage-00/lesson-02.md) · single-variable and vector calculus (integrals, divergence theorem) · first-year mechanics. **Estimated time** 4 h (2 h theory · 0.5 h simulator · 1.5 h exercises & programming) |
| Estimated time | 4 h (2 h theory · 0.5 h simulator · 1.5 h exercises & programming) |
| Level | Beginner |
| Learning objectives | 1. Convert fluently between energy, work, power, force, pressure, momentum and impulse, and check<br>2. Explain why pressure can be read as an energy density, and use it to interpret overpressure<br>3. Compute the impulse delivered by a pressure pulse (triangular, exponential and Friedlander) and<br>4. Apply momentum and energy conservation to collisions (the ballistic pendulum) and explain why<br>5. State the Reynolds transport theorem and derive integral mass and momentum balances for a<br>6. Compare published energy densities of fuels, batteries and compressed gas, and explain why energy |
| Theory | 1. Quantities, units and dimensions · 2. Work, energy and power · 3. Force and pressure · 4. Momentum and impulse: the loading that matters · 5. Collisions and fragments: momentum is conserved, kinetic energy is not · 6. Conservation laws on a control volume: the Reynolds transport theorem · 7. Energy densities: what stores energy, and why density is not hazard |
| Visual explanation | mermaid diagram + embedded simulator |
| Simulation | [blast-physics](sims/blast-physics/index.html) |
| Programming | [p01-blast-wave](projects/p01-blast-wave/README.md) |
| Reading | 5 selected items (see lesson) |
| Assessment | 7 questions + hidden-answer exercises; stage gate [assessments/stage-01.md](assessments/stage-01.md) |
| Next | [01.2 Gases & thermodynamics](lessons/stage-01/lesson-02.md), then [01.3 Waves: from acoustics to shocks](lessons/stage-01/lesson-03.md). Also a prerequisite for [01.6 Structural response & fragmentation](lessons/stage-01/lesson-06.md) and [01.7 Electricity & EM](lessons/stage-01/lesson-07.md). |

### [01.2 · Gases and thermodynamics](lessons/stage-01/lesson-02.md)

| Field | Specification |
|---|---|
| Prerequisites | [01.1 Mechanics refresher](lessons/stage-01/lesson-01.md) (energy vs power, pressure as energy density, control volumes) · calculus incl. simple ODEs. **Estimated time** 4.5 h (2.5 h theory · 0.5 h simulator · 1.5 h exercises & programming) |
| Estimated time | 4.5 h (2.5 h theory · 0.5 h simulator · 1.5 h exercises & programming) |
| Level | Beginner → Intermediate |
| Learning objectives | 1. Use the ideal-gas law in mass and molar forms, and estimate when real-gas corrections matter.<br>2. Apply the first law to closed and open systems. Define internal energy, enthalpy, $c_v$, $c_p$<br>3. Derive and apply the isentropic relations, and use them to predict temperatures in fast<br>4. Compute entropy changes of an ideal gas and explain lost work in irreversible processes.<br>5. Compute the stored energy of a compressed-gas vessel with three models (Brode, isentropic,<br>6. Estimate conductive, convective and radiative heat fluxes. Use the lumped-capacitance model and |
| Theory | 1. The ideal gas, and when it is not ideal · 2. The first law, internal energy, enthalpy and specific heats · 3. Adiabatic and isentropic processes · 4. The second law and entropy · 5. Stored energy in a compressed-gas vessel · 6. Heat transfer: conduction, convection, radiation |
| Visual explanation | mermaid diagram + embedded simulator |
| Simulation | [shock-tube](sims/shock-tube/index.html) |
| Programming | [p01-blast-wave](projects/p01-blast-wave/README.md) |
| Reading | 5 selected items (see lesson) |
| Assessment | 7 questions + hidden-answer exercises; stage gate [assessments/stage-01.md](assessments/stage-01.md) |
| Next | [01.3 Waves: from acoustics to shocks](lessons/stage-01/lesson-03.md) (uses $\gamma$, isentropic relations and entropy directly), and later [02.1 Chemical energy](lessons/stage-02/lesson-01.md). |

### [01.3 · Waves: from acoustics to shocks](lessons/stage-01/lesson-03.md)

| Field | Specification |
|---|---|
| Prerequisites | [01.1 Mechanics](lessons/stage-01/lesson-01.md) (conservation laws, control volumes) · [01.2 Gases & thermodynamics](lessons/stage-01/lesson-02.md) (ideal gas, adiabatic processes, $\gamma$) · calculus incl. partial derivatives. **Estimated time** 6 h (3 h theory · 1.5 h simulator · 1.5 h programming) |
| Estimated time | 6 h (3 h theory · 1.5 h simulator · 1.5 h programming) |
| Level | Intermediate |
| Learning objectives | 1. Derive the linear acoustic wave equation from the Euler equations and explain every<br>2. Explain **why large-amplitude waves steepen** into shocks (amplitude-dependent wave speed).<br>3. Derive the **Rankine–Hugoniot** relations for a normal shock in an ideal gas and use them to<br>4. Explain why a shock is **irreversible** (entropy rises) and why that matters for how blast<br>5. Represent all of the above computationally: closed-form functions, and a finite-volume solver |
| Theory | 1. The governing equations (1D Euler) · 2. Linear acoustics · 3. Why strong waves steepen · 4. The Rankine–Hugoniot jump conditions · 5. Entropy and irreversibility |
| Visual explanation | mermaid diagram + embedded simulator |
| Simulation | [blast-physics](sims/blast-physics/index.html) |
| Programming | [p01-blast-wave](projects/p01-blast-wave/README.md) |
| Reading | 5 selected items (see lesson) |
| Assessment | 7 questions + hidden-answer exercises; stage gate [assessments/stage-01.md](assessments/stage-01.md) |
| Next | [01.4 Reflection, transmission & dynamic pressure](lessons/stage-01/lesson-04.md) and [01.5 Scaling laws](lessons/stage-01/lesson-05.md), then [04.1 Anatomy of a blast wave](lessons/stage-04/lesson-01.md). |

### [01.4 · Reflection, transmission & dynamic pressure](lessons/stage-01/lesson-04.md)

| Field | Specification |
|---|---|
| Prerequisites | [01.3 Waves: from acoustics to shocks](lessons/stage-01/lesson-03.md) (Rankine–Hugoniot, shock Mach number, acoustic impedance) · [01.1 Mechanics](lessons/stage-01/lesson-01.md) (momentum flux, drag) · [01.2 Gases & thermodynamics](lessons/stage-01/lesson-02.md) (stagnation quantities). **Estimated time** 6 h (3 h theory · 1.5 h simulator · 1.5 h programming) |
| Estimated time | 6 h (3 h theory · 1.5 h simulator · 1.5 h programming) |
| Level | Intermediate |
| Learning objectives | 1. Derive pressure reflection and transmission coefficients at a plane interface from continuity of<br>2. Derive (sketch) and use the ideal-gas normal reflection formula<br>3. Explain regular vs Mach reflection, the Mach stem and triple point, and why the reflection<br>4. Derive the peak dynamic pressure $q = \tfrac52 p_s^2/(7p_0+p_s)$ from Rankine–Hugoniot and<br>5. Estimate the **clearing time** of reflected pressure on a finite target and decide whether a<br>6. Implement these relations and cross-check them against Sim D's 2D Euler solver. |
| Theory | 1. Acoustic impedance, reflection and transmission · 2. Normal reflection of a shock from a rigid wall · 3. Oblique reflection and the Mach stem · 4. Dynamic pressure and stagnation pressure · 5. Drag loading · 6. Clearing: why small targets escape the reflected pressure |
| Visual explanation | mermaid diagram + embedded simulator |
| Simulation | [blast-physics](sims/blast-physics/index.html) |
| Programming | [p01-blast-wave](projects/p01-blast-wave/README.md) |
| Reading | 7 selected items (see lesson) |
| Assessment | 7 questions + hidden-answer exercises; stage gate [assessments/stage-01.md](assessments/stage-01.md) |
| Next | [01.5 Dimensional analysis & scaling laws](lessons/stage-01/lesson-05.md), then [04.1 Anatomy of a blast wave](lessons/stage-04/lesson-01.md) and [04.2 Distance, reflection, confinement](lessons/stage-04/lesson-02.md). |

### [01.5 · Dimensional analysis & scaling laws](lessons/stage-01/lesson-05.md)

| Field | Specification |
|---|---|
| Prerequisites | [01.3 Waves: from acoustics to shocks](lessons/stage-01/lesson-03.md) (Rankine–Hugoniot, sound speed) · [01.4 Reflection & dynamic pressure](lessons/stage-01/lesson-04.md) · linear algebra (rank, null space). **Estimated time** 5 h (2.5 h theory · 1 h simulator challenge · 1.5 h programming) |
| Estimated time | 5 h (2.5 h theory · 1 h simulator challenge · 1.5 h programming) |
| Level | Intermediate |
| Learning objectives | 1. State and prove the **Buckingham Π theorem** (via rank–nullity and unit-change invariance), and<br>2. Derive **Hopkinson–Cranz cube-root scaling** for pressures, times and impulses from similarity,<br>3. Derive **Sachs scaling** for ambient pressure and temperature and apply it to altitude.<br>4. Derive the **Taylor–Sedov** strong-blast radius law $R\propto(Et^2/\rho_0)^{1/5}$ and reproduce<br>5. Identify, with Π groups, when scaling breaks: gravity, material strength and strain rate, |
| Theory | 1. Dimensions and the dimension matrix · 2. The Buckingham Π theorem · 3. Hopkinson–Cranz (cube-root) scaling · 4. Sachs scaling: non-standard atmospheres · 5. Taylor–Sedov: the strong-blast similarity solution · 6. Where scaling breaks |
| Visual explanation | mermaid diagram + embedded simulator |
| Simulation | [blast-physics](sims/blast-physics/index.html) |
| Programming | [p01-blast-wave](projects/p01-blast-wave/README.md) |
| Reading | 9 selected items (see lesson) |
| Assessment | 8 questions + hidden-answer exercises; stage gate [assessments/stage-01.md](assessments/stage-01.md) |
| Next | [01.6 Structural response & fragmentation](lessons/stage-01/lesson-06.md), then [04.1 Anatomy of a blast wave](lessons/stage-04/lesson-01.md). |

### [01.6 · Structural response & fragmentation physics (conceptual)](lessons/stage-01/lesson-06.md)

| Field | Specification |
|---|---|
| Prerequisites | [01.1 Mechanics](lessons/stage-01/lesson-01.md) (Newton's laws, energy, impulse) · [01.4 Reflection & dynamic pressure](lessons/stage-01/lesson-04.md) (loads, drag) · [01.5 Scaling laws](lessons/stage-01/lesson-05.md) · linear ODEs. **Estimated time** 6 h (3 h theory · 1.5 h simulator · 1.5 h programming) |
| Estimated time | 6 h (3 h theory · 1.5 h simulator · 1.5 h programming) |
| Level | Intermediate |
| Learning objectives | 1. Derive the response of an undamped SDOF oscillator to rectangular and triangular pulses and the<br>2. Classify loading as impulsive, dynamic or quasi-static from $\omega t_d$ (< 0.4, between, > 40)<br>3. Derive the **P–I asymptotes** $I^*=x_c\sqrt{km}$ and $P^*=kx_c/2$ from energy balance, and<br>4. Explain Biggs's equivalent-SDOF method (load, mass and load–mass factors) for a real member.<br>5. Model fragment deceleration by drag, show exponential velocity decay with distance, and estimate<br>6. Use the **Mott distribution** as a statistical model of fragment masses and explain how the |
| Theory | 1. The SDOF oscillator · 2. Response regimes · 3. P–I diagrams from energy balance · 4. Elastic–plastic resistance and ductility · 5. Fragment deceleration by drag · 6. Ballistic range with drag and gravity · 7. Fragment statistics: the Mott distribution · 8. Hazardous fragment density and hazard distance |
| Visual explanation | mermaid diagram + embedded simulator |
| Simulation | [blast-physics](sims/blast-physics/index.html) |
| Programming | [p01-blast-wave](projects/p01-blast-wave/README.md) |
| Reading | 7 selected items (see lesson) |
| Assessment | 7 questions + hidden-answer exercises; stage gate [assessments/stage-01.md](assessments/stage-01.md) |
| Next | [01.7 Electricity & electromagnetism](lessons/stage-01/lesson-07.md); this lesson is the foundation for [04.3 Structural effects](lessons/stage-04/lesson-03.md) and [04.4 Injury, fragments & secondary hazards](lessons/stage-04/lesson-04.md). |

### [01.7 · Electricity, electromagnetism & electronics for EOD technology](lessons/stage-01/lesson-07.md)

| Field | Specification |
|---|---|
| Prerequisites | [01.1 Mechanics](lessons/stage-01/lesson-01.md) (energy, power) · vector calculus (div, curl, Stokes/Gauss) · complex exponentials and basic Fourier analysis. **Estimated time** 7 h (4 h theory · 1 h simulator · 2 h programming) |
| Estimated time | 7 h (4 h theory · 1 h simulator · 2 h programming) |
| Level | Intermediate |
| Learning objectives | 1. Apply Ohm's and Kirchhoff's laws and solve RC transients; relate time constants to filter<br>2. Compute stored energy in capacitors and batteries, and build a robot **power budget** with<br>3. Explain the transduction physics and signal chain of strain gauges, piezoelectric pressure<br>4. State Maxwell's equations, derive the EM wave equation and the **skin depth**, and apply them to<br>5. Use antenna gain, **free-space path loss** and the **Friis equation** to build a radio link<br>6. Quantify Johnson, shot and 1/f noise and SNR, and apply the **Nyquist** sampling theorem.<br>7. Explain, conceptually, why ESD and RF emissions are controlled near ordnance. |
| Theory | 1. Circuits: Ohm, Kirchhoff and RC transients · 2. Energy storage: capacitors, batteries and robot power budgets · 3. Sensors and transducers · 4. Maxwell's equations at a working level · 5. Skin depth: why metal detectors work and radar does not see through metal · 6. Antennas, propagation and the Friis equation · 7. Noise, SNR and sampling · 8. Electrical hazards to ordnance: ESD and the electromagnetic environment (concepts) |
| Visual explanation | mermaid diagram + embedded simulator |
| Simulation | [eod-robot](sims/eod-robot/index.html) |
| Programming | [p02-sensor-noise](projects/p02-sensor-noise/README.md) |
| Reading | 6 selected items (see lesson) |
| Assessment | 7 questions + hidden-answer exercises; stage gate [assessments/stage-01.md](assessments/stage-01.md) |
| Next | Stage 2 [02.1 Chemical energy](lessons/stage-02/lesson-01.md); this lesson is a prerequisite for [05.2 EMI & GPR](lessons/stage-05/lesson-02.md), [06.1 EOD robot systems](lessons/stage-06/lesson-01.md) and [06.9 Communications & fail-safe design](lessons/stage-06/lesson-09.md). |

## Stage 2 · Chemistry & energetic materials

### [02.1 · Chemical energy: where the energy comes from, and how fast it comes out](lessons/stage-02/lesson-01.md)

| Field | Specification |
|---|---|
| Prerequisites | [01.1 Mechanics](lessons/stage-01/lesson-01.md) (energy, work, power) · [01.2 Gases & thermodynamics](lessons/stage-01/lesson-02.md) (first law, enthalpy, $c_p$, ideal gas) · school chemistry (moles, balancing equations). **Estimated time** 6 h (3 h theory · 1 h worked examples · 2 h programming) |
| Estimated time | 6 h (3 h theory · 1 h worked examples · 2 h programming) |
| Level | Intermediate |
| Learning objectives | 1. Assign oxidation states and identify the oxidiser, the fuel and the number of electrons<br>2. Compute reaction enthalpies from bond energies and from standard enthalpies of formation<br>3. Compute heats of combustion per mole, per kilogram of fuel and per kilogram of fuel–air mixture,<br>4. Compute gas generation (moles, volume at STP) and the pressure rise of a constant-volume reaction.<br>5. Write and run a root-finding solver for the adiabatic flame temperature of methane–air with<br>6. Use the Arrhenius law to quantify how reaction rate depends on temperature and activation<br>7. Distinguish energy from power and use the distinction to rank hazards. |
| Theory | 1. Redox and oxidation states · 2. Bond energies: a first estimate · 3. Enthalpy of formation and Hess's law · 4. Heat of combustion: per mole, per kilogram, per kilogram of mixture · 5. Gas generation · 6. Adiabatic flame temperature · 7. Kinetics: the Arrhenius law · 8. Energy versus power |
| Visual explanation | mermaid diagram |
| Simulation | [shock-tube](sims/shock-tube/index.html) |
| Programming | in-lesson exercises |
| Reading | 4 selected items (see lesson) |
| Assessment | 8 questions + hidden-answer exercises; stage gate [assessments/stage-02.md](assessments/stage-02.md) |
| Next | [02.2 Deflagration vs detonation](lessons/stage-02/lesson-02.md), then [02.3 Sensitivity, stability, ageing & classification](lessons/stage-02/lesson-03.md). |

### [02.2 · Deflagration vs detonation: how a reaction front travels](lessons/stage-02/lesson-02.md)

| Field | Specification |
|---|---|
| Prerequisites | [02.1 Chemical energy](lessons/stage-02/lesson-01.md) (heat release, flame temperature, Arrhenius) · [01.3 Waves: from acoustics to shocks](lessons/stage-01/lesson-03.md) (Rankine–Hugoniot, shock Mach number) · [01.2 Gases & thermodynamics](lessons/stage-01/lesson-02.md). **Estimated time** 6 h (3 h theory · 1 h simulator · 2 h programming) |
| Estimated time | 6 h (3 h theory · 1 h simulator · 2 h programming) |
| Level | Intermediate |
| Learning objectives | 1. Contrast deflagration and detonation quantitatively (propagation mechanism, speed, pressure<br>2. Derive the Mallard–Le Chatelier laminar flame speed scaling $S_L \sim \sqrt{\alpha/\tau_c}$ and<br>3. Explain turbulent flame acceleration and deflagration-to-detonation transition (DDT) as a<br>4. Derive the Rayleigh line and the reactive Hugoniot, and show that the Chapman–Jouguet (CJ)<br>5. Compute the CJ velocity, pressure and temperature for an ideal-gas mixture with heat release<br>6. Describe the ZND structure (von Neumann spike, induction zone, reaction zone) and explain why<br>7. Explain from momentum conservation why detonation pressure scales as $\rho D^2$. |
| Theory | 1. Two propagation modes · 2. Laminar flames: the Mallard–Le Chatelier thermal theory · 3. Turbulent flames and flame acceleration · 4. Deflagration-to-detonation transition (concept) · 5. The Rayleigh line and the Hugoniot curve · 6. The Chapman–Jouguet condition · 7. The ZND structure · 8. Detonation cells (qualitative) · 9. Why detonation pressure scales with $\rho D^2$ |
| Visual explanation | mermaid diagram + embedded simulator |
| Simulation | [shock-tube](sims/shock-tube/index.html) |
| Programming | [p01-blast-wave](projects/p01-blast-wave/README.md) |
| Reading | 6 selected items (see lesson) |
| Assessment | 7 questions + hidden-answer exercises; stage gate [assessments/stage-02.md](assessments/stage-02.md) |
| Next | [02.3 Sensitivity, stability, ageing & classification](lessons/stage-02/lesson-03.md), then [04.1 Anatomy of a blast wave](lessons/stage-04/lesson-01.md). |

### [02.3 · Sensitivity, stability, ageing & classification](lessons/stage-02/lesson-03.md)

| Field | Specification |
|---|---|
| Prerequisites | [02.1 Chemical energy](lessons/stage-02/lesson-01.md) (Arrhenius kinetics) · [02.2 Deflagration vs detonation](lessons/stage-02/lesson-02.md) (propagation modes) · probability & statistics (likelihood, maximum-likelihood estimation) · ODEs. **Estimated time** 6 h (2.5 h theory · 1.5 h worked examples · 2 h programming) |
| Estimated time | 6 h (2.5 h theory · 1.5 h worked examples · 2 h programming) |
| Level | Intermediate |
| Learning objectives | 1. Explain the six UN Class 1 hazard divisions and the compatibility-group system, and reason<br>2. Explain what impact, friction, electrostatic-discharge and thermal sensitivity tests measure,<br>3. Derive the Bruceton (up-and-down) estimators, simulate the method in Python on a fictional<br>4. Derive the Semenov critical condition for thermal explosion, compute a critical ambient<br>5. Explain the Frank-Kamenetskii parameter and compute how the critical temperature falls as a<br>6. Model stabiliser depletion with Arrhenius kinetics, estimate a shelf life from accelerated<br>7. Explain, from first principles, why old and fired-but-failed ordnance is more hazardous than |
| Theory | 1. Decomposing "hazard" · 2. UN Class 1 hazard divisions · 3. Compatibility groups — a constraint-satisfaction problem · 4. What sensitivity tests measure — and why the answer is a distribution · 5. The Bruceton (up-and-down) method as a statistics problem · 6. Thermal explosion theory · 7. Stabiliser depletion and propellant ageing · 8. Why old and fired-but-failed ordnance is dangerous (conceptual) |
| Visual explanation | mermaid diagram |
| Simulation | [shock-tube](sims/shock-tube/index.html) |
| Programming | [p02-sensor-noise](projects/p02-sensor-noise/README.md) |
| Reading | 6 selected items (see lesson) |
| Assessment | 8 questions + hidden-answer exercises; stage gate [assessments/stage-02.md](assessments/stage-02.md) |
| Next | [03.1 Taxonomy of explosive hazards](lessons/stage-03/lesson-01.md), [03.2 Conventional munitions families](lessons/stage-03/lesson-02.md), then the [Stage 2 gate](assessments/stage-02.md). |

## Stage 3 · Hazards & ordnance recognition

### [03.1 · Taxonomy of explosive hazards](lessons/stage-03/lesson-01.md)

| Field | Specification |
|---|---|
| Prerequisites | [00.1 What EOD is](lessons/stage-00/lesson-01.md) (vocabulary, organisations) · [00.2 How EOD organisations operate](lessons/stage-00/lesson-02.md) · elementary probability (conditional probability, Bayes' rule). **Estimated time** 4 h (2 h theory · 1 h Sim H · 1 h programming) |
| Estimated time | 4 h (2 h theory · 1 h Sim H · 1 h programming) |
| Level | Beginner |
| Learning objectives | 1. Use the IMAS 04.10 terms (EO, UXO, AXO, ERW, IED, mine, submunition) precisely, and draw the<br>2. Explain the purpose and the **limits** of ammunition colour-coding and marking conventions,<br>3. Compute and interpret risk as likelihood × consequence, both as an ordinal matrix and as an<br>4. Compute a posterior distribution over hazard categories from uncertain feature observations<br>5. Choose a response category by minimising expected loss under an asymmetric loss matrix, and<br>6. Map a category to the responsible organisation type and response family at the conceptual |
| Theory | 1. The vocabulary: IMAS 04.10 and the set relations · 2. Ammunition categories and why they exist · 3. Colour-coding and markings — useful convention, unreliable evidence · 4. Risk = likelihood × consequence · 5. Probabilistic classification from uncertain features · 6. From posterior to response: asymmetric losses · 7. Category → organisation → response family |
| Visual explanation | mermaid diagram + embedded simulator |
| Simulation | [recognition-trainer](sims/recognition-trainer/index.html) |
| Programming | [p03-bayesian-fusion](projects/p03-bayesian-fusion/README.md), [p12-hitl-decision](projects/p12-hitl-decision/README.md) |
| Reading | 5 selected items (see lesson) |
| Assessment | 8 questions + hidden-answer exercises; stage gate [assessments/stage-03.md](assessments/stage-03.md) |
| Next | [03.2 Conventional munitions families](lessons/stage-03/lesson-02.md) and [03.4 Improvised explosive hazards](lessons/stage-03/lesson-04.md). |

### [03.2 · Conventional munitions families and safety-and-arming as a system](lessons/stage-03/lesson-02.md)

| Field | Specification |
|---|---|
| Prerequisites | [03.1 Taxonomy of explosive hazards](lessons/stage-03/lesson-01.md) · [02.3 Sensitivity, stability, ageing](lessons/stage-02/lesson-03.md) (sensitivity concepts) · [01.7 Electricity & EM](lessons/stage-01/lesson-07.md) (HERO/ESD as safety concepts) · probability (independence, conditional probability) · finite-state machines. **Estimated time** 5 h (2.5 h theory · 1 h Sim H · 1.5 h programming) |
| Estimated time | 5 h (2.5 h theory · 1 h Sim H · 1.5 h programming) |
| Level | Intermediate |
| Learning objectives | 1. Distinguish the four delivery families (projected, thrown, dropped, placed) by generic<br>2. Explain the explosive train as a **sensitivity–quantity ladder** and why an *interrupted*<br>3. Model safety-and-arming as a **finite-state machine** with independent environmental guards<br>4. Compute the probability of inadvertent arming for a fictional two-interlock design with a<br>5. Quantify why a fired-but-failed item's unknown state must be treated as armed, using Bayes' |
| Theory | 1. Four delivery families · 2. The explosive train as a systems concept · 3. Safety and arming as a state machine · 4. Why environments: signatures that handling cannot produce · 5. Fault tree: probability of inadvertent arming · 6. Unknown state: why a fired-but-failed item is more hazardous |
| Visual explanation | mermaid diagram + embedded simulator |
| Simulation | [recognition-trainer](sims/recognition-trainer/index.html) |
| Programming | in-lesson exercises |
| Reading | 6 selected items (see lesson) |
| Assessment | 8 questions + hidden-answer exercises; stage gate [assessments/stage-03.md](assessments/stage-03.md) |
| Next | [03.3 Landmines, cluster munitions, abandoned & historical ordnance](lessons/stage-03/lesson-03.md). |

### [03.3 · Landmines, cluster munitions, abandoned & historical ordnance](lessons/stage-03/lesson-03.md)

| Field | Specification |
|---|---|
| Prerequisites | [03.1 Taxonomy](lessons/stage-03/lesson-01.md) · [03.2 Conventional munitions & S&A](lessons/stage-03/lesson-02.md) (unknown state of used items) · [02.3 Sensitivity, stability, ageing](lessons/stage-02/lesson-03.md) (Arrhenius kinetics, stabiliser depletion) · binomial and Poisson distributions. **Estimated time** 4 h (2 h theory · 0.5 h Sim H · 1.5 h programming) |
| Estimated time | 4 h (2 h theory · 0.5 h Sim H · 1.5 h programming) |
| Level | Intermediate |
| Learning objectives | 1. Summarise the purposes and key obligations of the **Ottawa Convention**, the **Convention on<br>2. Read contamination and casualty statistics critically (what is recorded vs what exists).<br>3. Model submunition failures with binomial and Poisson distributions, including overdispersion,<br>4. Model spatial contamination density and residual hazard after imperfect clearance.<br>5. Explain, conceptually and with simple kinetic/corrosion models, how decades of burial or<br>6. Describe the particular problems of legacy WWI/WWII ordnance and underwater/dumped munitions. |
| Theory | 1. The humanitarian and legal context · 2. Reading contamination statistics · 3. Why submunition failure creates lasting contamination · 4. Overdispersion: why field failure rates vary so much · 5. Spatial contamination and residual hazard · 6. Landmines: persistence by design · 7. Legacy WWI and WWII ordnance · 8. Underwater and dumped munitions · 9. Degradation over decades |
| Visual explanation | mermaid diagram |
| Simulation | [detection-theory](sims/detection-theory/index.html), [recognition-trainer](sims/recognition-trainer/index.html) |
| Programming | [p02-sensor-noise](projects/p02-sensor-noise/README.md) |
| Reading | 8 selected items (see lesson) |
| Assessment | 8 questions + hidden-answer exercises; stage gate [assessments/stage-03.md](assessments/stage-03.md) |
| Next | [03.4 Improvised explosive hazards](lessons/stage-03/lesson-04.md); later [05.2 EMI & GPR](lessons/stage-05/lesson-02.md) and [05.7 Search theory & land release](lessons/stage-05/lesson-07.md). |

### [03.4 · Improvised explosive hazards and vehicle-related hazards (recognition level)](lessons/stage-03/lesson-04.md)

| Field | Specification |
|---|---|
| Prerequisites | [03.1 Taxonomy](lessons/stage-03/lesson-01.md) (Bayes over categories, expected-loss decisions) · [00.2 How EOD organisations operate](lessons/stage-00/lesson-02.md) · [01.5 Scaling laws](lessons/stage-01/lesson-05.md) (cube-root scaling — helpful, not essential). **Estimated time** 4 h (2 h theory · 0.5 h simulator · 1.5 h programming) |
| Estimated time | 4 h (2 h theory · 0.5 h simulator · 1.5 h programming) |
| Level | Intermediate |
| Learning objectives | 1. Distinguish an **unattended** item from a **suspicious** item using public indicator<br>2. Name the three **threat categories** used in public counter-IED language (victim-operated,<br>3. Compute the posterior probability of a real device from a report using realistic base rates,<br>4. Choose among response options by expected loss, compute decision thresholds, and compute the<br>5. Explain how public stand-off tables (e.g. the DHS-DOJ Bomb Threat Stand-Off Card) derive from<br>6. Describe the counter-IED lines of operation (attack the network, defeat the device, train the |
| Theory | 1. What makes a hazard "improvised" · 2. Unattended versus suspicious · 3. Threat categories — categories only · 4. Base rates and false alarms · 5. Decision analysis: response options, thresholds and the value of information · 6. Secondary hazards and secondary devices — awareness · 7. Vehicle-borne hazards and public stand-off tables · 8. The counter-IED framework |
| Visual explanation | mermaid diagram |
| Simulation | [detection-theory](sims/detection-theory/index.html), [incident-command](sims/incident-command/index.html), [recognition-trainer](sims/recognition-trainer/index.html) |
| Programming | [p12-hitl-decision](projects/p12-hitl-decision/README.md) |
| Reading | 6 selected items (see lesson) |
| Assessment | 8 questions + hidden-answer exercises; stage gate [assessments/stage-03.md](assessments/stage-03.md) |
| Next | Stage 4 — [04.1 Anatomy of a blast wave](lessons/stage-04/lesson-01.md) and [04.4 Injury, fragments & secondary hazards](lessons/stage-04/lesson-04.md); later [07.1 Decisions under uncertainty](lessons/stage-07/lesson-01.md). |

## Stage 4 · Blast effects

### [04.1 · Anatomy of a blast wave](lessons/stage-04/lesson-01.md)

| Field | Specification |
|---|---|
| Prerequisites | [01.3 Waves: acoustics → shocks](lessons/stage-01/lesson-03.md) (Rankine–Hugoniot, $M_s$ ↔ overpressure) · [01.4 Reflection & dynamic pressure](lessons/stage-01/lesson-04.md) · [01.5 Scaling laws](lessons/stage-01/lesson-05.md) (Hopkinson–Cranz, Sachs) · [02.2 Deflagration vs detonation](lessons/stage-02/lesson-02.md). **Estimated time** 6 h (3 h theory · 1.5 h simulator · 1.5 h programming) |
| Estimated time | 6 h (3 h theory · 1.5 h simulator · 1.5 h programming) |
| Level | Intermediate |
| Learning objectives | 1. Describe a free-field blast pressure history in terms of arrival time $t_a$, peak incident<br>2. Derive the positive-phase impulse of the Friedlander waveform,<br>3. Compute shock arrival time as $t_a = \int dr/U(r)$ using the Rankine–Hugoniot shock speed and<br>4. Evaluate the Kinney–Graham fits at a given scaled distance, state their validity range and<br>5. Explain the difference between side-on, face-on (reflected) and stagnation measurements and<br>6. Quantify how a ±20 % scatter in an empirical fit propagates into distance and equivalent-yield |
| Theory | 1. The free-field pressure history · 2. Positive-phase impulse — derivation · 3. The negative phase · 4. Empirical fits: Kinney–Graham and Kingery–Bulmash · 5. Arrival time as an integral · 6. Dynamic and reflected pressure at the gauge · 7. Measurement: what a gauge actually sees · 8. How wrong are the fits? Propagating uncertainty |
| Visual explanation | mermaid diagram + embedded simulator |
| Simulation | [blast-physics](sims/blast-physics/index.html) |
| Programming | [p01-blast-wave](projects/p01-blast-wave/README.md) |
| Reading | 7 selected items (see lesson) |
| Assessment | 8 questions + hidden-answer exercises; stage gate [assessments/stage-04.md](assessments/stage-04.md) |
| Next | [04.2 Distance, reflection, confinement & urban environments](lessons/stage-04/lesson-02.md). |

### [04.2 · Distance, reflection, confinement & urban environments](lessons/stage-04/lesson-02.md)

| Field | Specification |
|---|---|
| Prerequisites | [04.1 Anatomy of a blast wave](lessons/stage-04/lesson-01.md) · [01.4 Reflection, transmission & dynamic pressure](lessons/stage-01/lesson-04.md) (normal/oblique reflection, Mach stem) · [01.5 Scaling laws](lessons/stage-01/lesson-05.md) · [01.2 Gases & thermodynamics](lessons/stage-01/lesson-02.md) (first law, $c_v$, $\gamma$). **Estimated time** 6 h (3 h theory · 2 h simulator · 1 h programming) |
| Estimated time | 6 h (3 h theory · 2 h simulator · 1 h programming) |
| Level | Intermediate |
| Learning objectives | 1. Use scaled distance to convert a pressure criterion into a range for any yield, and state how<br>2. Justify the ground-reflection (surface-burst) factor with an image-source argument and explain<br>3. Describe regular vs Mach reflection, the triple point and why oblique loads can exceed<br>4. Derive the quasi-static pressure of energy released in a closed volume,<br>5. Explain channelling and shielding in street canyons, bound them with a simple geometric<br>6. Design and interpret probe experiments in Sim D's wall, corner, street and room scenes. |
| Theory | 1. Scaled distance in practice · 2. Ground reflection and the surface-burst factor · 3. Oblique and Mach reflection · 4. Reflection from finite targets: clearing · 5. Confined (internal) blast: two phases · 6. Venting: how the gas pressure decays · 7. Urban environments: channelling and shielding |
| Visual explanation | mermaid diagram + embedded simulator |
| Simulation | [blast-physics](sims/blast-physics/index.html) |
| Programming | [p01-blast-wave](projects/p01-blast-wave/README.md) |
| Reading | 6 selected items (see lesson) |
| Assessment | 8 questions + hidden-answer exercises; stage gate [assessments/stage-04.md](assessments/stage-04.md) |
| Next | [04.3 Structural effects](lessons/stage-04/lesson-03.md) and [04.4 Injury, fragmentation & secondary hazards](lessons/stage-04/lesson-04.md); later [08.2 Reconstruction](lessons/stage-08/lesson-02.md). |

### [04.3 · Structural effects](lessons/stage-04/lesson-03.md)

| Field | Specification |
|---|---|
| Prerequisites | [04.2 Distance, reflection, confinement & urban environments](lessons/stage-04/lesson-02.md) · [01.6 Structural response & fragmentation](lessons/stage-01/lesson-06.md) (SDOF oscillator, impulsive vs quasi-static regimes, P–I asymptotes) · ODEs, energy methods. **Estimated time** 6 h (3 h theory · 1 h simulator · 2 h programming) |
| Estimated time | 6 h (3 h theory · 1 h simulator · 2 h programming) |
| Level | Intermediate → Advanced |
| Learning objectives | 1. Explain why glazing is the dominant urban blast-injury source and compute the range at which a<br>2. Build an equivalent SDOF model of a wall or panel using load and mass transformation factors<br>3. Derive the impulsive and quasi-static asymptotes of a P–I diagram by energy balance for elastic<br>4. Explain progressive collapse and the structural principles that resist it (redundancy,<br>5. Summarise the protective-design philosophy of UFC 3-340-02 (and ASCE practice): standoff first,<br>6. Interpret quantity-distance rules $D = K\,Q^{1/3}$ as Hopkinson scaling applied to regulation, and |
| Theory | 1. The glazing hazard · 2. Walls and frames: failure modes and the equivalent SDOF system · 3. P–I diagrams from energy balance · 4. Using P–I diagrams in practice · 5. Progressive collapse — the Oklahoma City case · 6. Protective-design philosophy · 7. Quantity-distance: scaling applied to regulation |
| Visual explanation | mermaid diagram + embedded simulator |
| Simulation | [blast-physics](sims/blast-physics/index.html) |
| Programming | [p01-blast-wave](projects/p01-blast-wave/README.md) |
| Reading | 7 selected items (see lesson) |
| Assessment | 7 questions + hidden-answer exercises; stage gate [assessments/stage-04.md](assessments/stage-04.md) |
| Next | [04.4 Injury mechanisms, fragmentation & secondary hazards](lessons/stage-04/lesson-04.md); case study [Oklahoma City 1995](case-studies/cs03-oklahoma-city.md). |

### [04.4 · Injury mechanisms, fragmentation & secondary hazards](lessons/stage-04/lesson-04.md)

| Field | Specification |
|---|---|
| Prerequisites | [04.2 Distance, reflection, confinement & urban environments](lessons/stage-04/lesson-02.md) · [04.3 Structural effects](lessons/stage-04/lesson-03.md) (P–I diagrams) · [01.6 Structural response & fragmentation](lessons/stage-01/lesson-06.md) (fragment drag, statistics) · basic probability (lognormal, Monte Carlo). **Estimated time** 6 h (3 h theory · 1 h simulator · 2 h programming) |
| Estimated time | 6 h (3 h theory · 1 h simulator · 2 h programming) |
| Level | Intermediate → Advanced |
| Learning objectives | 1. Classify blast injuries as primary, secondary, tertiary or quaternary, and map each to the<br>2. Explain lung and ear injury criteria (including the Bowen curves) as P–I-style criteria, state<br>3. Compute a hazardous-fragment distance from a fragment count, a density criterion and a drag<br>4. Explain conceptually how a public stand-off chart is derived from scaled distance and<br>5. Apply time–distance–shielding reasoning and state what personal protective equipment can and<br>6. Identify secondary hazards (fire, collapse, utilities, additional devices, CBRN) and their<br>7. Build and verify a Monte Carlo model that selects an evacuation radius achieving < 1 % |
| Theory | 1. The four classes of blast injury · 2. Primary injury as a P–I criterion · 3. Tertiary injury: displacement by the blast wind · 4. Fragment hazard · 5. Public stand-off tables — how they are derived · 6. Time, distance, shielding — and what PPE can do · 7. Secondary hazards |
| Visual explanation | mermaid diagram + embedded simulator |
| Simulation | [blast-physics](sims/blast-physics/index.html) |
| Programming | [p12-hitl-decision](projects/p12-hitl-decision/README.md) |
| Reading | 6 selected items (see lesson) |
| Assessment | 8 questions + hidden-answer exercises; stage gate [assessments/stage-04.md](assessments/stage-04.md) |
| Next | [07.1 Decisions under uncertainty](lessons/stage-07/lesson-01.md) · [07.2 Incident management](lessons/stage-07/lesson-02.md) · case study [Boston 2013](case-studies/cs07-boston-2013.md). |

## Stage 5 · Detection

### [05.1 · Detection theory: ROC, base rates, costs and test & evaluation](lessons/stage-05/lesson-01.md)

| Field | Specification |
|---|---|
| Prerequisites | [00.2 How EOD organisations operate](lessons/stage-00/lesson-02.md) (land release, roles) · probability (Bayes' rule, Gaussian and binomial distributions, Poisson processes) · basic hypothesis testing. **Estimated time** 6 h (3 h theory · 1 h simulator · 2 h programming) |
| Estimated time | 6 h (3 h theory · 1 h simulator · 2 h programming) |
| Level | Intermediate |
| Learning objectives | 1. Model a detector as a binary hypothesis test; compute $P_d$, $P_{fa}$ and the ROC for Gaussian<br>2. Derive the likelihood-ratio test and state the Neyman–Pearson lemma; compute the NP threshold<br>3. Compute the positive predictive value of an alarm from base rate, $P_d$ and $P_{fa}$, and explain<br>4. Derive the Bayes-optimal threshold from misclassification costs and priors and apply it to a<br>5. Design a blind detector trial in the spirit of CWA 14747-1: compute exact confidence intervals for |
| Theory | 1. The detector as a hypothesis test · 2. The likelihood-ratio test and Neyman–Pearson · 3. ROC, AUC and what the curve does not tell you · 4. Base rates and the predictive value of an alarm · 5. Costs and the Bayes-optimal threshold · 6. False-alarm economics in humanitarian clearance · 7. Test & evaluation: blind trials in the spirit of CWA 14747-1 |
| Visual explanation | mermaid diagram + embedded simulator |
| Simulation | [detection-theory](sims/detection-theory/index.html) |
| Programming | [p02-sensor-noise](projects/p02-sensor-noise/README.md) |
| Reading | 6 selected items (see lesson) |
| Assessment | 8 questions + hidden-answer exercises; stage gate [assessments/stage-05.md](assessments/stage-05.md) |
| Next | Any of the sensor lessons — [05.2 EMI & GPR](lessons/stage-05/lesson-02.md), [05.3 Penetrating radiation](lessons/stage-05/lesson-03.md), [05.4 Trace & vapour](lessons/stage-05/lesson-04.md), [05.5 Imaging & remote sensing](lessons/stage-05/lesson-05.md) — then [05.6 Sensor fusion](lessons/stage-05/lesson-06.md). |

### [05.2 · Electromagnetic induction & ground-penetrating radar](lessons/stage-05/lesson-02.md)

| Field | Specification |
|---|---|
| Prerequisites | [05.1 Detection theory](lessons/stage-05/lesson-01.md) · [01.7 Electricity & EM](lessons/stage-01/lesson-07.md) (Faraday's law, Maxwell's equations, EM waves) · [01.3 Waves](lessons/stage-01/lesson-03.md) (wave equation, impedance) · [03.3 Mines, cluster munitions & legacy ordnance](lessons/stage-03/lesson-03.md) (why buried hazards matter). **Estimated time** 7 h (3.5 h theory · 1 h simulator · 2.5 h programming) |
| Estimated time | 7 h (3.5 h theory · 1 h simulator · 2.5 h programming) |
| Level | Intermediate |
| Learning objectives | 1. Explain induction sensing from Faraday's law: primary field, eddy currents, secondary field; compute<br>2. Relate a target's time-domain decay constant to its conductivity, permeability and size; compare<br>3. Explain magnetic viscosity and conductive-soil effects and why "minimum-metal" targets are the<br>4. Compute GPR propagation velocity, two-way time, attenuation, reflection coefficient and<br>5. Derive the diffraction hyperbola $t(x)$ for a point scatterer, fit it to data to recover depth and<br>6. For both sensors, list what they detect, their false-positive and false-negative mechanisms, and |
| Theory | 1. Induction: primary field, eddy currents, secondary field · 2. Skin depth · 3. Target response: dipole model and decay constants · 4. Pulse induction vs frequency-domain (continuous-wave) detectors · 5. Soil effects: magnetic viscosity and conductive ground · 6. The minimum-metal problem · 7. GPR: EM propagation in soil · 8. Resolution · 9. Hyperbolic signatures — derivation and fitting · 10. Clutter and dual-sensor systems |
| Visual explanation | mermaid diagram + embedded simulator |
| Simulation | [sensor-fusion](sims/sensor-fusion/index.html) |
| Programming | [p02-sensor-noise](projects/p02-sensor-noise/README.md) |
| Reading | 6 selected items (see lesson) |
| Assessment | 7 questions + hidden-answer exercises; stage gate [assessments/stage-05.md](assessments/stage-05.md) |
| Next | [05.3 Penetrating radiation](lessons/stage-05/lesson-03.md) or [05.6 Sensor fusion](lessons/stage-05/lesson-06.md) (EMI + GPR is the canonical fusion pair). |

### [05.3 · Penetrating radiation: X-ray, dual-energy, backscatter, CT and neutron methods](lessons/stage-05/lesson-03.md)

| Field | Specification |
|---|---|
| Prerequisites | [05.1 Detection theory](lessons/stage-05/lesson-01.md) · [01.7 Electricity & EM](lessons/stage-01/lesson-07.md) (photons, energy units) · linear algebra and Fourier transforms · Poisson statistics. **Estimated time** 7 h (3.5 h theory · 0.5 h simulator · 3 h programming) |
| Estimated time | 7 h (3.5 h theory · 0.5 h simulator · 3 h programming) |
| Level | Intermediate |
| Learning objectives | 1. Explain X-ray production (bremsstrahlung, characteristic lines) and compute transmission through<br>2. Explain the Z- and energy-dependence of photoelectric absorption and Compton scattering, and use<br>3. Quantify image noise from photon statistics and relate it to detectability (contrast-to-noise).<br>4. Explain backscatter imaging from Compton kinematics and state when single-sided access matters.<br>5. Derive the Radon transform and the Fourier-slice theorem; implement filtered back-projection in<br>6. Apply time–distance–shielding and ALARA quantitatively (inverse square, half-value layers).<br>7. Describe thermal/fast-neutron analysis and NQR: principle, what they measure, strengths and limits. |
| Theory | 1. X-ray generation · 2. Beer–Lambert attenuation · 3. Why attenuation depends on Z and E · 4. Dual-energy material discrimination · 5. Photon statistics and detectability · 6. Backscatter imaging · 7. Portable radiography in EOD — why, conceptually · 8. CT: the Radon transform and filtered back-projection · 9. Dose and radiation safety · 10. Neutron-based interrogation and NQR (concepts) |
| Visual explanation | mermaid diagram |
| Simulation | — |
| Programming | [p02-sensor-noise](projects/p02-sensor-noise/README.md) |
| Reading | 6 selected items (see lesson) |
| Assessment | 7 questions + hidden-answer exercises; stage gate [assessments/stage-05.md](assessments/stage-05.md) |
| Next | [05.4 Trace & vapour detection](lessons/stage-05/lesson-04.md), then [05.6 Sensor fusion](lessons/stage-05/lesson-06.md). The imaging side continues in [09.1 Perception tasks](lessons/stage-09/lesson-01.md). |

### [05.4 · Trace & vapour detection: vapour pressure, IMS, MS, colorimetry and canines](lessons/stage-05/lesson-04.md)

| Field | Specification |
|---|---|
| Prerequisites | [05.1 Detection theory](lessons/stage-05/lesson-01.md) · [01.2 Gases & thermodynamics](lessons/stage-01/lesson-02.md) (ideal gas, phase equilibrium) · [02.1 Chemical energy](lessons/stage-02/lesson-01.md) (enthalpy) · basic signal processing. **Estimated time** 6 h (3 h theory · 0.5 h simulator · 2.5 h programming) |
| Estimated time | 6 h (3 h theory · 0.5 h simulator · 2.5 h programming) |
| Level | Intermediate |
| Learning objectives | 1. Use the Clausius–Clapeyron relation to predict how vapour pressure scales with temperature, and<br>2. Explain particle vs vapour sampling and compute collected mass through a sampling/preconcentration<br>3. Explain ion-mobility spectrometry: ionisation, drift velocity $v=KE$, reduced mobility $K_0$,<br>4. Explain mass spectrometry at the level of $m/z$, resolving power and tandem selectivity, and why<br>5. Describe colorimetric tests and canine detection (Furton & Myers, 2001): principle, strengths,<br>6. Define limit of detection and relate peak-detection thresholds, the number of search windows, |
| Theory | 1. Vapour pressure and the Clausius–Clapeyron relation · 2. Sampling: particles and vapour · 3. Ion-mobility spectrometry (IMS) · 4. Mass spectrometry (basics) · 5. Colorimetric tests · 6. Canines · 7. Interferents, detection limits and ROC trade-offs · 8. Simulating an IMS spectrum and detecting peaks |
| Visual explanation | mermaid diagram |
| Simulation | — |
| Programming | [p02-sensor-noise](projects/p02-sensor-noise/README.md) |
| Reading | 6 selected items (see lesson) |
| Assessment | 7 questions + hidden-answer exercises; stage gate [assessments/stage-05.md](assessments/stage-05.md) |
| Next | [05.5 Imaging & remote sensing](lessons/stage-05/lesson-05.md), then [05.6 Sensor fusion](lessons/stage-05/lesson-06.md). |

### [05.5 · Imaging & remote sensing](lessons/stage-05/lesson-05.md)

| Field | Specification |
|---|---|
| Prerequisites | [05.1 Detection theory](lessons/stage-05/lesson-01.md) (ROC, base rates) · [01.2 Gases & thermodynamics](lessons/stage-01/lesson-02.md) (heat-transfer modes) · [01.6 Structural response](lessons/stage-01/lesson-06.md) (SDOF oscillators, resonance) · [01.7 Electricity & EM](lessons/stage-01/lesson-07.md) (EM waves, antennas) · Fourier series, the heat equation. **Estimated time** 7 h (3.5 h theory · 1 h simulator · 2.5 h programming) |
| Estimated time | 7 h (3.5 h theory · 1 h simulator · 2.5 h programming) |
| Level | Intermediate → Advanced |
| Learning objectives | 1. Explain the atmospheric windows in the millimetre-wave band. Compute the diffraction-limited<br>2. Compare active and passive mmW imaging using brightness temperature and the radiometer<br>3. Use Planck's law, Wien's law and emissivity to compute thermal-IR radiance, sensitivity and<br>4. Model the **diurnal thermal contrast** of a buried inclusion with the 1D heat equation under<br>5. Model the mine–soil system as a driven resonator. Compute its resonance and the Doppler<br>6. Apply the linear mixing model and the spectral angle to hyperspectral pixels. Size a drone |
| Theory | 1. Millimetre-wave imaging · 2. Thermal infrared · 3. Diurnal thermal contrast of buried objects · 4. Acoustic / seismic detection · 5. Hyperspectral imaging (basics) · 6. Drones for non-technical survey and photogrammetry |
| Visual explanation | mermaid diagram + embedded simulator |
| Simulation | [sensor-fusion](sims/sensor-fusion/index.html) |
| Programming | [p02-sensor-noise](projects/p02-sensor-noise/README.md) |
| Reading | 6 selected items (see lesson) |
| Assessment | 8 questions + hidden-answer exercises; stage gate [assessments/stage-05.md](assessments/stage-05.md) |
| Next | [05.6 Sensor fusion](lessons/stage-05/lesson-06.md), then [05.7 Search theory & area clearance](lessons/stage-05/lesson-07.md). |

### [05.6 · Sensor fusion](lessons/stage-05/lesson-06.md)

| Field | Specification |
|---|---|
| Prerequisites | [05.1 Detection theory](lessons/stage-05/lesson-01.md) (likelihood ratios, ROC, base rates) · at least two of [05.2](lessons/stage-05/lesson-02.md), [05.3](lessons/stage-05/lesson-03.md), [05.4](lessons/stage-05/lesson-04.md), [05.5](lessons/stage-05/lesson-05.md) · multivariate Gaussians, entropy. **Estimated time** 7 h (3 h theory · 1.5 h simulator · 2.5 h programming) |
| Estimated time | 7 h (3 h theory · 1.5 h simulator · 2.5 h programming) |
| Level | Advanced |
| Learning objectives | 1. Derive Bayesian fusion under conditional independence and implement it in log-odds form.<br>2. Derive, for a Gaussian copula, the exact overconfidence factor of naive Bayes with correlated<br>3. Compare feature-level and decision-level fusion, and derive the optimal decision-level rule<br>4. Combine evidence with Dempster's rule, compute belief and plausibility, and explain Zadeh's<br>5. Build a log-odds occupancy grid with sensor footprints and explain why clamping is needed.<br>6. Rank sensing actions by expected information gain (mutual information) and by value of |
| Theory | 1. Bayesian fusion with conditionally independent likelihoods · 2. Correlated errors: what naive Bayes does wrong · 3. Feature-level vs decision-level fusion · 4. Dempster–Shafer theory and Zadeh's paradox · 5. Occupancy-grid fusion · 6. Sensor selection: information gain and value of information |
| Visual explanation | mermaid diagram + embedded simulator |
| Simulation | [sensor-fusion](sims/sensor-fusion/index.html) |
| Programming | [p02-sensor-noise](projects/p02-sensor-noise/README.md), [p03-bayesian-fusion](projects/p03-bayesian-fusion/README.md) |
| Reading | 7 selected items (see lesson) |
| Assessment | 7 questions + hidden-answer exercises; stage gate [assessments/stage-05.md](assessments/stage-05.md) |
| Next | [05.7 Search theory & area clearance](lessons/stage-05/lesson-07.md); later [06.6 State estimation](lessons/stage-06/lesson-06.md), [07.1 Decisions under uncertainty](lessons/stage-07/lesson-01.md) and [09.4 Multimodal sensing](lessons/stage-09/lesson-04.md). |

### [05.7 · Search theory & area clearance](lessons/stage-05/lesson-07.md)

| Field | Specification |
|---|---|
| Prerequisites | [05.1 Detection theory](lessons/stage-05/lesson-01.md) · [05.6 Sensor fusion](lessons/stage-05/lesson-06.md) (posteriors, VOI) · Lagrange multipliers / KKT conditions, Poisson and binomial distributions. **Estimated time** 6 h (3 h theory · 0.5 h simulator · 2.5 h programming) |
| Estimated time | 6 h (3 h theory · 0.5 h simulator · 2.5 h programming) |
| Level | Advanced |
| Learning objectives | 1. Derive the random-search law $\text{POD} = 1-e^{-WL/A}$ and explain its assumptions.<br>2. Define the lateral range curve and sweep width. Derive the inverse-cube lateral range curve,<br>3. Derive the optimal allocation of search effort for exponential detection functions via<br>4. Describe land release (NTS → TS → clearance; cancelled / reduced / cleared land) as sequential<br>5. Compute the probability that a QA sampling plan accepts a field with a given residual<br>6. Quantify residual risk after clearance and QA with Poisson thinning, and explain what QA can and |
| Theory | 1. Random search and the exponential detection law · 2. Lateral range curves, sweep width and detection laws · 3. Optimal allocation of search effort (Koopman / Stone) · 4. Humanitarian land release (IMAS 07.11) · 5. Quality-assurance sampling (IMAS 09.20, ISO 2859-style) · 6. Residual risk |
| Visual explanation | mermaid diagram + embedded simulator |
| Simulation | [sensor-fusion](sims/sensor-fusion/index.html) |
| Programming | [p03-bayesian-fusion](projects/p03-bayesian-fusion/README.md) |
| Reading | 6 selected items (see lesson) |
| Assessment | 7 questions + hidden-answer exercises; stage gate [assessments/stage-05.md](assessments/stage-05.md) |
| Next | [06.6 State estimation](lessons/stage-06/lesson-06.md) and [07.1 Decisions under uncertainty](lessons/stage-07/lesson-01.md). Case studies: [Laos cluster munitions](case-studies/cs05-laos-cluster-munitions.md), [Kuwait clearance](case-studies/cs04-kuwait-clearance.md). |

## Stage 6 · Robotics

### [06.1 · EOD robot systems: history, architecture, requirements and test methods](lessons/stage-06/lesson-01.md)

| Field | Specification |
|---|---|
| Prerequisites | [00.2 How EOD organisations operate](lessons/stage-00/lesson-02.md) (roles, incident life-cycle) · [01.7 Electricity & EM](lessons/stage-01/lesson-07.md) (power, energy storage, RF) · basic optimisation and probability. **Estimated time** 6 h (3 h theory · 1 h simulator · 2 h design & programming) |
| Estimated time | 6 h (3 h theory · 1 h simulator · 2 h design & programming) |
| Level | Intermediate |
| Learning objectives | 1. Trace the development of EOD robots from Wheelbarrow (1972) to the US Army's common robotic<br>2. Draw and explain the reference architecture (mobility, manipulation, sensing, communications,<br>3. Break a mission need down into quantitative, testable requirements and show where they<br>4. Set up and solve a small multi-objective sizing problem, find its Pareto front and explain the<br>5. Explain why reproducible **standard test methods** (NIST / ASTM E54.09) matter. Compute how many<br>6. Discuss the human side of the system, meaning operator–robot relationships (Carpenter 2016), and |
| Theory | 1. A short engineering history · 2. Reference architecture · 3. Requirements decomposition · 4. A multi-objective sizing problem · 5. Standard test methods: NIST / ASTM E54.09 · 6. The human in the system |
| Visual explanation | mermaid diagram + embedded simulator |
| Simulation | [eod-robot](sims/eod-robot/index.html) |
| Programming | [p05-robot-sim](projects/p05-robot-sim/README.md) |
| Reading | 7 selected items (see lesson) |
| Assessment | 7 questions + hidden-answer exercises; stage gate [assessments/stage-06.md](assessments/stage-06.md) |
| Next | [06.2 Spatial mathematics](lessons/stage-06/lesson-02.md), then [06.3 Manipulators](lessons/stage-06/lesson-03.md) and [06.4 Mobile bases & control](lessons/stage-06/lesson-04.md). |

### [06.2 · Spatial mathematics: frames, rotations, transforms and cameras](lessons/stage-06/lesson-02.md)

| Field | Specification |
|---|---|
| Prerequisites | [06.1 EOD robot systems](lessons/stage-06/lesson-01.md) · linear algebra (orthogonal matrices, eigenvectors, matrix exponential) · basic ODEs. **Estimated time** 7 h (4 h theory · 1 h simulator · 2 h programming) |
| Estimated time | 7 h (4 h theory · 1 h simulator · 2 h programming) |
| Level | Intermediate (fast-track available, see [Stage 6 overview](lessons/stage-06/README.md)) |
| Learning objectives | 1. Represent orientation as rotation matrices, axis–angle, unit quaternions and Euler angles.<br>2. Derive Rodrigues' formula from the exponential map of $\mathfrak{so}(3)$, and invert it (the<br>3. Compose and invert homogeneous transforms in SE(3) and use them to move points and frames<br>4. Use twists and exponential coordinates (Lynch & Park) to describe screw motions. Compute<br>5. Project world points into an image with the pinhole model plus extrinsics, and back-project<br>6. Solve pan–tilt inverse kinematics: compute the pan and tilt angles that put a world point on |
| Theory | 1. Rotation matrices and SO(3) · 2. Axis–angle, the exponential map and Rodrigues' formula · 3. Unit quaternions · 4. Euler angles and gimbal lock · 5. Rigid motions: SE(3) and homogeneous transforms · 6. Twists, screws and exponential coordinates (Lynch & Park) · 7. Cameras: the pinhole model with extrinsics · 8. Pan–tilt unit kinematics |
| Visual explanation | mermaid diagram + embedded simulator |
| Simulation | [eod-robot](sims/eod-robot/index.html) |
| Programming | [p05-robot-sim](projects/p05-robot-sim/README.md), [p08-manipulator](projects/p08-manipulator/README.md) |
| Reading | 5 selected items (see lesson) |
| Assessment | 7 questions + hidden-answer exercises; stage gate [assessments/stage-06.md](assessments/stage-06.md) |
| Next | [06.3 Manipulators](lessons/stage-06/lesson-03.md), [06.4 Mobile bases & control](lessons/stage-06/lesson-04.md), [06.6 State estimation](lessons/stage-06/lesson-06.md). |

### [06.3 · Manipulators: kinematics, Jacobians, statics and grasping](lessons/stage-06/lesson-03.md)

| Field | Specification |
|---|---|
| Prerequisites | [06.2 Spatial mathematics](lessons/stage-06/lesson-02.md) (SE(3), twists, exponential coordinates) · linear algebra (SVD, pseudo-inverse) · Newton's method. **Estimated time** 8 h (4 h theory · 1 h simulator · 3 h programming) |
| Estimated time | 8 h (4 h theory · 1 h simulator · 3 h programming) |
| Level | Intermediate → Advanced (fast-track available) |
| Learning objectives | 1. Derive forward kinematics for a serial arm with both Denavit–Hartenberg (DH) parameters and the<br>2. Solve inverse kinematics analytically for a planar 3R arm and a 5-DOF turret arm, enumerating<br>3. Implement numerical IK (Newton–Raphson, damped least squares) and explain the convergence and<br>4. Compute the geometric Jacobian (space form, via adjoints) and verify it by finite differences.<br>5. Use the SVD of the Jacobian to classify singularities and compute Yoshikawa manipulability and<br>6. Use $\tau = J^\top F$ to compute joint torques for payloads and derive a payload-vs-reach curve.<br>7. State force-closure and form-closure conditions and size a friction grasp. |
| Theory | 1. Forward kinematics: DH parameters · 2. Forward kinematics: product of exponentials · 3. Inverse kinematics of a planar 3R arm · 4. Analytic IK of the 5-DOF turret arm · 5. The Jacobian · 6. Numerical IK: Newton–Raphson and damped least squares · 7. Singularities and manipulability · 8. Statics: $\tau = J^\top F$ and payload vs reach · 9. Grippers and grasp basics |
| Visual explanation | mermaid diagram + embedded simulator |
| Simulation | [robotics-engineering](sims/robotics-engineering/index.html) |
| Programming | [p08-manipulator](projects/p08-manipulator/README.md) |
| Reading | 7 selected items (see lesson) |
| Assessment | 7 questions + hidden-answer exercises; stage gate [assessments/stage-06.md](assessments/stage-06.md) |
| Next | [06.8 Path & motion planning](lessons/stage-06/lesson-08.md) (arm motion planning) · [06.5 Teleoperation & HMI](lessons/stage-06/lesson-05.md) (how an operator drives this arm). |

### [06.4 · Mobile bases and control: tracks, stairs, motors, batteries, PID and LQR](lessons/stage-06/lesson-04.md)

| Field | Specification |
|---|---|
| Prerequisites | [06.2 Spatial mathematics](lessons/stage-06/lesson-02.md) (SE(2)/SE(3), frames) · [01.7 Electricity & EM](lessons/stage-01/lesson-07.md) (circuits, energy storage) · Laplace transforms, linear ODEs, eigenvalues. **Estimated time** 8 h (4 h theory · 1.5 h simulator · 2.5 h programming) |
| Estimated time | 8 h (4 h theory · 1.5 h simulator · 2.5 h programming) |
| Level | Intermediate |
| Learning objectives | 1. Compare tracks, wheels and legs for EOD terrain and stairs with quantitative arguments<br>2. Derive skid-steer kinematics with the ICR (instantaneous centre of rotation) slip model,<br>3. Compute the static stability margin and tip-over angle of a tracked robot on a stair,<br>4. Size a DC drive (torque–speed line, gearing, current) and build a mission energy budget with<br>5. Derive PID gains by pole placement, explain and fix integrator windup, and implement the<br>6. Formulate a state-space model, discretise it exactly, and design an LQR controller. Explain the |
| Theory | 1. Tracks vs wheels vs legs · 2. Skid-steer kinematics and the ICR slip model · 3. The unicycle model and odometry · 4. Stability on slopes and stairs · 5. DC motors and drives · 6. Batteries and power budgets · 7. PID control: derivation, tuning, windup, discrete implementation · 8. State space and LQR |
| Visual explanation | mermaid diagram + embedded simulator |
| Simulation | [eod-robot](sims/eod-robot/index.html) |
| Programming | [p05-robot-sim](projects/p05-robot-sim/README.md) |
| Reading | 5 selected items (see lesson) |
| Assessment | 7 questions + hidden-answer exercises; stage gate [assessments/stage-06.md](assessments/stage-06.md) |
| Next | [06.5 Teleoperation & HMI](lessons/stage-06/lesson-05.md) (the human closes the outer loop), [06.6 State estimation](lessons/stage-06/lesson-06.md) (where odometry meets sensors). |

### [06.5 · Teleoperation & human–machine interfaces](lessons/stage-06/lesson-05.md)

| Field | Specification |
|---|---|
| Prerequisites | [06.2 Spatial mathematics](lessons/stage-06/lesson-02.md) (frames, camera geometry) · [06.4 Mobile bases and control](lessons/stage-06/lesson-04.md) (PID, state-space, skid-steer kinematics) · Laplace transforms and Bode/Nyquist basics. **Estimated time** 7 h (3.5 h theory · 1.5 h simulator · 2 h programming) |
| Estimated time | 7 h (3.5 h theory · 1.5 h simulator · 2 h programming) |
| Level | Advanced |
| Learning objectives | 1. Model the operator–robot loop with transmission delay and **derive the stability limit** for a<br>2. Explain Ferrell's **move-and-wait** result quantitatively and predict task time as a function of<br>3. Design a **Smith predictor** and a **predictive display**, and state exactly what model errors<br>4. Allocate functions of an EOD robot across the **four stages × ten levels** of automation of<br>5. Explain why naive force-reflecting teleoperation becomes unstable under delay, show that the<br>6. Evaluate an OCU design using Endsley's three-level SA model, **NASA-TLX** workload, a latency |
| Theory | 1. The operator in the loop: delay budget · 2. Move-and-wait (Ferrell 1965) · 3. The control-theoretic view: delay eats phase margin · 4. Smith predictor: removing the delay from the characteristic equation · 5. Predictive displays · 6. Supervisory control and levels of automation · 7. Situational awareness (Endsley 1995) · 8. Workload: NASA-TLX · 9. Force feedback and bilateral teleoperation under delay · 10. Cameras, depth perception and the OCU |
| Visual explanation | mermaid diagram + embedded simulator |
| Simulation | [eod-robot](sims/eod-robot/index.html) |
| Programming | [p11-teleoperation](projects/p11-teleoperation/README.md) |
| Reading | 9 selected items (see lesson) |
| Assessment | 8 questions + hidden-answer exercises; stage gate [assessments/stage-06.md](assessments/stage-06.md) |
| Next | [06.9 Communications, reliability & fail-safe design](lessons/stage-06/lesson-09.md), then [07.2 Incident management](lessons/stage-07/lesson-02.md). |

### [06.6 · State estimation](lessons/stage-06/lesson-06.md)

| Field | Specification |
|---|---|
| Prerequisites | [05.6 Sensor fusion](lessons/stage-05/lesson-06.md) (Bayes' rule, likelihoods) · [06.2 Spatial mathematics](lessons/stage-06/lesson-02.md) (SE(2)/SE(3)) · [06.4 Mobile bases and control](lessons/stage-06/lesson-04.md) (skid-steer kinematics) · multivariate Gaussians, linear algebra. **Estimated time** 8 h (4 h theory · 1 h simulator · 3 h programming) |
| Estimated time | 8 h (4 h theory · 1 h simulator · 3 h programming) |
| Level | Advanced |
| Learning objectives | 1. Derive the recursive **Bayes filter** from the Markov assumptions and implement it on a<br>2. Derive the **Kalman filter update as conditioning of a joint Gaussian**, and the prediction as<br>3. Linearise a range–bearing landmark model for an **EKF**, compute its Jacobians by hand, and<br>4. Implement a **particle filter** (SIR) with systematic resampling and use effective sample<br>5. Apply **NEES and NIS** chi-square tests to detect an inconsistent filter.<br>6. Design a **wheel-odometry + gyro** fusion filter for a skid-steer robot that estimates gyro |
| Theory | 1. The Bayes filter · 2. The Kalman filter as Gaussian conditioning · 3. The extended Kalman filter · 4. The unscented transform (concept, with a proof-by-example) · 5. The particle filter · 6. Is the filter honest? NEES and NIS · 7. Landmark-based localisation · 8. Odometry + IMU fusion for a tracked robot |
| Visual explanation | mermaid diagram + embedded simulator |
| Simulation | [eod-robot](sims/eod-robot/index.html) |
| Programming | [p04-localization](projects/p04-localization/README.md) |
| Reading | 4 selected items (see lesson) |
| Assessment | 8 questions + hidden-answer exercises; stage gate [assessments/stage-06.md](assessments/stage-06.md) |
| Next | [06.7 Mapping & SLAM](lessons/stage-06/lesson-07.md), then [06.8 Path & motion planning](lessons/stage-06/lesson-08.md). |

### [06.7 · Mapping & SLAM](lessons/stage-06/lesson-07.md)

| Field | Specification |
|---|---|
| Prerequisites | [06.6 State estimation](lessons/stage-06/lesson-06.md) (Bayes filter, EKF, Gaussian conditioning) · [06.2 Spatial mathematics](lessons/stage-06/lesson-02.md) (SE(2)/SE(3), composition) · SVD, sparse linear algebra, nonlinear least squares. **Estimated time** 9 h (4 h theory · 1 h simulator · 4 h programming) |
| Estimated time | 9 h (4 h theory · 1 h simulator · 4 h programming) |
| Level | Expert |
| Learning objectives | 1. Build an **occupancy grid** with log-odds updates and an inverse sensor model; explain<br>2. Derive the **closed-form rigid alignment** (Kabsch/Arun SVD solution) used inside ICP,<br>3. Formulate **EKF-SLAM**, explain why its cost is $O(n^2)$ per update in the number of<br>4. Formulate **pose-graph SLAM** as nonlinear least squares on SE(2), derive the Gauss–Newton<br>5. Explain **loop closure** and why a single false positive can destroy a map; apply **robust<br>6. Compare visual and LiDAR SLAM systems (ORB-SLAM, Cartographer and others) and extract design |
| Theory | 1. Occupancy grids with log-odds · 2. Scan matching: ICP and the closed-form alignment · 3. EKF-SLAM and its quadratic cost · 4. Pose-graph SLAM as nonlinear least squares · 5. Loop closure and robust kernels · 6. The landscape: visual and LiDAR SLAM in practice · 7. Lessons from the DARPA Subterranean Challenge |
| Visual explanation | mermaid diagram + embedded simulator |
| Simulation | [robotics-engineering](sims/robotics-engineering/index.html) |
| Programming | [p07-slam](projects/p07-slam/README.md) |
| Reading | 7 selected items (see lesson) |
| Assessment | 8 questions + hidden-answer exercises; stage gate [assessments/stage-06.md](assessments/stage-06.md) |
| Next | [06.8 Path & motion planning](lessons/stage-06/lesson-08.md), then [09.5 Active perception & autonomous exploration](lessons/stage-09/lesson-05.md). |

### [06.8 · Path & motion planning](lessons/stage-06/lesson-08.md)

| Field | Specification |
|---|---|
| Prerequisites | [06.7 Mapping & SLAM](lessons/stage-06/lesson-07.md) (occupancy grids) · [06.6 State estimation](lessons/stage-06/lesson-06.md) (covariances) · [06.3 Manipulators](lessons/stage-06/lesson-03.md) (joint space, forward kinematics) · [05.7 Search theory](lessons/stage-05/lesson-07.md) (sweep width) · algorithms (priority queues, graph search). **Estimated time** 8 h (3.5 h theory · 1.5 h simulator · 3 h programming) |
| Estimated time | 8 h (3.5 h theory · 1.5 h simulator · 3 h programming) |
| Level | Advanced |
| Learning objectives | 1. Construct the **configuration space** of a mobile base and an arm and explain obstacle<br>2. Prove that A* with an **admissible** heuristic returns an optimal path and that a<br>3. Build a layered **cost map** with lethal, inflation and **risk** layers, and interpret an<br>4. Explain **D\* Lite**'s incremental replanning (keys, $g$ vs $rhs$, $k_m$) and when it pays off.<br>5. State the guarantees of **RRT** (probabilistic completeness) and **RRT\*** (asymptotic<br>6. Plan a **boustrophedon coverage** survey from sensor sweep width, and outline **arm motion |
| Theory | 1. Configuration space · 2. Dijkstra and A\* · 3. Cost maps with risk layers · 4. Incremental replanning: D\* Lite · 5. Sampling-based planning: RRT and RRT\* · 6. Coverage planning for survey · 7. Arm motion planning (the MoveIt pipeline) · 8. Planning under uncertainty: chance constraints |
| Visual explanation | mermaid diagram + embedded simulator |
| Simulation | [robotics-engineering](sims/robotics-engineering/index.html) |
| Programming | [p06-path-planning](projects/p06-path-planning/README.md) |
| Reading | 4 selected items (see lesson) |
| Assessment | 9 questions + hidden-answer exercises; stage gate [assessments/stage-06.md](assessments/stage-06.md) |
| Next | [06.9 Communications, reliability & fail-safe design](lessons/stage-06/lesson-09.md), then [09.5 Active perception & autonomous exploration](lessons/stage-09/lesson-05.md). |

### [06.9 · Communications, reliability & fail-safe design](lessons/stage-06/lesson-09.md)

| Field | Specification |
|---|---|
| Prerequisites | [01.7 Electricity & EM](lessons/stage-01/lesson-07.md) (EM waves, RF, HERO/ESD as safety concepts) · [06.5 Teleoperation & HMI](lessons/stage-06/lesson-05.md) (delay, levels of automation) · probability (exponential and Gaussian distributions), decibels. **Estimated time** 7 h (3.5 h theory · 1.5 h simulator · 2 h programming) |
| Estimated time | 7 h (3.5 h theory · 1.5 h simulator · 2 h programming) |
| Level | Advanced |
| Learning objectives | 1. Compute free-space path loss with **Friis**, the **two-ray** ground-reflection loss and its<br>2. Build a **link budget** from transmit power, antenna gains, losses, receiver noise figure and<br>3. Compare **relays**, **mast antennas** and **tethers** quantitatively and qualitatively.<br>4. Design **loss-of-comms behaviours** (stop, retro-traverse, return-to-last-good-comms) as a<br>5. Compute mission reliability with **exponential failure** models, series/parallel and<br>6. Perform an **FMEA** (with RPN and its limitations) and a **fault tree** analysis with minimal |
| Theory | 1. Free-space propagation: Friis · 2. The ground matters: two-ray model and Fresnel zones · 3. Penetration, shadowing and fading · 4. The link budget · 5. Relays and tethers · 6. The RF environment in EOD operations (conceptual) · 7. Loss-of-comms behaviours (design options) · 8. Reliability mathematics · 9. FMEA · 10. Fault trees · 11. Safety state machines and watchdogs |
| Visual explanation | mermaid diagram + embedded simulator |
| Simulation | [eod-robot](sims/eod-robot/index.html), [robotics-engineering](sims/robotics-engineering/index.html) |
| Programming | [p11-teleoperation](projects/p11-teleoperation/README.md) |
| Reading | 4 selected items (see lesson) |
| Assessment | 8 questions + hidden-answer exercises; stage gate [assessments/stage-06.md](assessments/stage-06.md) |
| Next | [07.1 Decisions under uncertainty](lessons/stage-07/lesson-01.md), [07.2 Incident management](lessons/stage-07/lesson-02.md) and Capstone C1. |

## Stage 7 · EOD decision-making

### [07.1 · Decisions under uncertainty](lessons/stage-07/lesson-01.md)

| Field | Specification |
|---|---|
| Prerequisites | [05.1 Detection theory](lessons/stage-05/lesson-01.md) (Bayes, likelihood ratios, ROC) · [05.6 Sensor fusion](lessons/stage-05/lesson-06.md) (log-odds fusion, expected information gain) · [04.4 Injury, fragments & secondary hazards](lessons/stage-04/lesson-04.md) · [03.4 Improvised hazards](lessons/stage-03/lesson-04.md) (the suspicious-item assessment) · probability and dynamic programming. **Estimated time** 8 h (3.5 h theory · 2 h simulators · 2.5 h programming) |
| Estimated time | 8 h (3.5 h theory · 2 h simulators · 2.5 h programming) |
| Level | Advanced |
| Learning objectives | 1. Formulate an incident as a sequential decision problem: hidden state, observations, actions,<br>2. Perform Bayesian updating in odds and log-odds form, and explain why likelihood ratios — not<br>3. Derive expected-loss decisions, the **decision threshold** $p^{*}$, the **expected value of<br>4. Express **exposure minimisation** as an objective (integrated hazard over people and time) and<br>5. Explain the POMDP framing, solve a one-dimensional belief-state problem by Bellman recursion,<br>6. Recognise anchoring, confirmation bias, sunk cost and plan-continuation bias in a decision log,<br>7. Contrast naturalistic (recognition-primed) and analytic decision making, and say when each is |
| Theory | 1. The incident as a sequential decision problem · 2. Hypotheses and Bayesian updating · 3. Expected loss and the decision threshold · 4. Value of information: EVPI and EVSI · 5. Exposure minimisation as an objective · 6. The POMDP framing: belief states and Bellman recursion · 7. Cognitive biases and structural debiasing · 8. Naturalistic vs analytic decision making |
| Visual explanation | mermaid diagram + embedded simulator |
| Simulation | [incident-command](sims/incident-command/index.html), [scene-assessment](sims/scene-assessment/index.html) |
| Programming | [p12-hitl-decision](projects/p12-hitl-decision/README.md) |
| Reading | 7 selected items (see lesson) |
| Assessment | 8 questions + hidden-answer exercises; stage gate [assessments/stage-07.md](assessments/stage-07.md) |
| Next | [07.2 Incident management](lessons/stage-07/lesson-02.md), then [Project P12](projects/p12-hitl-decision/README.md) and [09.5 Active perception](lessons/stage-09/lesson-05.md). |

### [07.2 · Incident management: the conceptual framework](lessons/stage-07/lesson-02.md)

| Field | Specification |
|---|---|
| Prerequisites | [07.1 Decisions under uncertainty](lessons/stage-07/lesson-01.md) (belief, VOI, exposure) · [04.2 Distance, reflection, confinement](lessons/stage-04/lesson-02.md) (scaled distance, Kinney–Graham fit) · [04.4 Injury, fragments & secondary hazards](lessons/stage-04/lesson-04.md) (stand-off tables, glazing) · [06.5 Teleoperation & HMI](lessons/stage-06/lesson-05.md). **Estimated time** 6 h (3 h theory · 1.5 h simulator · 1.5 h programming) |
| Estimated time | 6 h (3 h theory · 1.5 h simulator · 1.5 h programming) |
| Level | Advanced |
| Learning objectives | 1. Derive a cordon radius from an explicit **risk tolerance** and an *uncertain* abstract yield,<br>2. Compare blast- and fragment-governed distances and explain why published stand-off tables are<br>3. Apply time–distance–shielding as operations on the exposure integral of 07.1.<br>4. Formulate sensor and robot tasking as a scheduling problem, prove the weighted-shortest-<br>5. Decide between evacuation and shelter-in-place with an explicit model including glazing<br>6. Place evidence preservation, escalation to specialist resources and command interfaces (ICS,<br>7. Explain the three disposal-outcome families as organisational choices and list the risk and |
| Theory | 1. Isolation logic: a cordon radius from a risk tolerance · 2. Why published stand-off tables are larger: fragments and glazing · 3. Time, distance, shielding — operations on the exposure integral · 4. Information gathering and its sources · 5. Sensor and robot tasking as a scheduling problem · 6. Secondary-hazard awareness · 7. Evacuation vs shelter-in-place · 8. Evidence preservation inside the safety envelope · 9. Escalation and specialist resources · 10. Command interfaces: ICS and unified command · 11. The families of disposal outcome (organisational level only) |
| Visual explanation | mermaid diagram + embedded simulator |
| Simulation | [scene-assessment](sims/scene-assessment/index.html) |
| Programming | [p01-blast-wave](projects/p01-blast-wave/README.md), [p12-hitl-decision](projects/p12-hitl-decision/README.md) |
| Reading | 6 selected items (see lesson) |
| Assessment | 7 questions + hidden-answer exercises; stage gate [assessments/stage-07.md](assessments/stage-07.md) |
| Next | [08.1 The post-blast scene](lessons/stage-08/lesson-01.md) and the [Stage 7 gate](assessments/stage-07.md). |

## Stage 8 · Forensics & post-blast investigation

### [08.1 · The post-blast scene](lessons/stage-08/lesson-01.md)

| Field | Specification |
|---|---|
| Prerequisites | [07.2 Incident management](lessons/stage-07/lesson-02.md) (evidence preservation, secondary hazards, ICS) · [05.7 Search theory](lessons/stage-05/lesson-07.md) (sweep width, Koopman allocation) · [04.4 Injury, fragments & secondary hazards](lessons/stage-04/lesson-04.md) · basic statistics and error propagation. **Estimated time** 6 h (3 h theory · 1 h simulator · 2 h programming) |
| Estimated time | 6 h (3 h theory · 1 h simulator · 2 h programming) |
| Level | Advanced |
| Learning objectives | 1. Explain why scene safety precedes and constrains all forensic work, and list the classes of<br>2. Size a scene perimeter from the evidence distribution and estimate the search effort it<br>3. Compute coverage, probability of detection and time for spiral, strip/grid and zone searches,<br>4. Specify a documentation plan — photography, sketches, measurements, total station and laser<br>5. Design evidence collection, packaging and chain-of-custody records that prevent contamination<br>6. Summarise the TWGFEX guidelines' requirements at the scene–laboratory interface. |
| Theory | 1. Scene safety and secondary hazards · 2. Zoning and the scene perimeter · 3. Search patterns and coverage mathematics · 4. Documentation: photography, sketches and measurements · 5. Evidence collection, packaging and chain of custody · 6. TWGFEX at the scene–laboratory interface |
| Visual explanation | mermaid diagram |
| Simulation | [post-blast](sims/post-blast/index.html) |
| Programming | in-lesson exercises |
| Reading | 7 selected items (see lesson) |
| Assessment | 9 questions + hidden-answer exercises; stage gate [assessments/stage-08.md](assessments/stage-08.md) |
| Next | [08.2 Reconstruction as an inverse problem](lessons/stage-08/lesson-02.md), then [08.3 Laboratory & digital forensics](lessons/stage-08/lesson-03.md). |

### [08.2 · Reconstruction as an inverse problem](lessons/stage-08/lesson-02.md)

| Field | Specification |
|---|---|
| Prerequisites | [08.1 The post-blast scene](lessons/stage-08/lesson-01.md) (survey data, uncertainty) · [04.2 Distance, reflection, confinement](lessons/stage-04/lesson-02.md) (scaled distance, Kinney–Graham fit) · [04.3 Structural effects](lessons/stage-04/lesson-03.md) (glazing, fragility) · [06.2 Spatial mathematics](lessons/stage-06/lesson-02.md) (camera frames) · [06.7 Mapping & SLAM](lessons/stage-06/lesson-07.md) (nonlinear least squares) · Bayesian statistics. **Estimated time** 7 h (3 h theory · 1.5 h simulator · 2.5 h programming) |
| Estimated time | 7 h (3 h theory · 1.5 h simulator · 2.5 h programming) |
| Level | Advanced |
| Learning objectives | 1. Formulate seat location and yield estimation as inverse problems, and diagnose their<br>2. Derive and apply the closed-form least-squares intersection of direction lines, with its<br>3. Propagate threshold and measurement uncertainty through Stage 4 scaling to a yield estimate,<br>4. Build a Bayesian inversion of a binary damage map, sample it with Metropolis MCMC, fuse<br>5. Explain structure-from-motion and bundle adjustment (objective, sparsity, gauge freedom and<br>6. Reconstruct a multi-camera timeline by estimating clock offsets with least squares, including |
| Theory | 1. The inverse-problem view · 2. Seat from direction evidence: least-squares line intersection · 3. How big? Yield from a damage radius — and why it is so uncertain · 4. Bayesian inversion of a damage map with MCMC · 5. Crater and damage-pattern interpretation (conceptual) · 6. 3D scene capture: photogrammetry and structure from motion · 7. LiDAR and scene registration · 8. Timeline reconstruction from video |
| Visual explanation | mermaid diagram + embedded simulator |
| Simulation | [post-blast](sims/post-blast/index.html) |
| Programming | [p10-scene-generator](projects/p10-scene-generator/README.md) |
| Reading | 6 selected items (see lesson) |
| Assessment | 7 questions + hidden-answer exercises; stage gate [assessments/stage-08.md](assessments/stage-08.md) |
| Next | [08.3 Laboratory & digital forensics](lessons/stage-08/lesson-03.md); Capstone C3 (post-blast digital reconstruction lab). |

### [08.3 · Laboratory & digital forensics](lessons/stage-08/lesson-03.md)

| Field | Specification |
|---|---|
| Prerequisites | [08.1 The post-blast scene](lessons/stage-08/lesson-01.md) (controls, blanks, custody) · [08.2 Reconstruction](lessons/stage-08/lesson-02.md) (timeline, uncertainty) · [05.4 Trace & vapour detection](lessons/stage-05/lesson-04.md) (IMS/MS basics) · [05.1 Detection theory](lessons/stage-05/lesson-01.md) (likelihood ratios, base rates) · undergraduate chemistry and physics. **Estimated time** 5 h (2.5 h theory · 0.5 h simulator · 2 h programming) |
| Estimated time | 5 h (2.5 h theory · 0.5 h simulator · 2 h programming) |
| Level | Advanced |
| Learning objectives | 1. Describe what a forensic explosives laboratory does in a post-blast case and how an<br>2. Explain the principles of GC-MS, LC-MS, ion chromatography, FTIR, Raman and SEM-EDS, and<br>3. Explain why consensus standards (TWGFEX guidelines, OSAC Registry, ASTM E2998 and E3253)<br>4. Describe the public role of the FBI's TEDAC in the US system.<br>5. Design a digital-evidence triage pipeline: hashing and custody, near-duplicate detection,<br>6. Estimate method error rates with confidence bounds from validation data, and explain the |
| Theory | 1. What the laboratory does · 2. Separation science: GC, LC and ion chromatography · 3. Mass spectrometry · 4. Vibrational spectroscopy: FTIR and Raman · 5. SEM-EDS: morphology and elements · 6. Orthogonal methods and likelihood ratios · 7. Standards and institutions · 8. Digital forensics and computer vision for evidence triage · 9. Evidential reliability: validation, error rates and bias |
| Visual explanation | mermaid diagram |
| Simulation | [post-blast](sims/post-blast/index.html) |
| Programming | [p09-cv-detection](projects/p09-cv-detection/README.md), [p10-scene-generator](projects/p10-scene-generator/README.md) |
| Reading | 6 selected items (see lesson) |
| Assessment | 8 questions + hidden-answer exercises; stage gate [assessments/stage-08.md](assessments/stage-08.md) |
| Next | [Stage 8 gate](assessments/stage-08.md), then [Stage 9 · AI & computer vision](lessons/stage-09/lesson-01.md) and [case study CS07 · Boston 2013](case-studies/cs07-boston-2013.md). |

## Stage 9 · AI & computer vision

### [09.1 · Perception tasks for EOD: detection, segmentation, anomalies and the metrics that matter](lessons/stage-09/lesson-01.md)

| Field | Specification |
|---|---|
| Prerequisites | [05.1 Detection theory](lessons/stage-05/lesson-01.md) (ROC, base rates, costs) · [05.2 EMI & GPR](lessons/stage-05/lesson-02.md) (B-scans, hyperbolas) · [05.3 Penetrating radiation](lessons/stage-05/lesson-03.md) (attenuation, dual-energy) · [05.5 Imaging & remote sensing](lessons/stage-05/lesson-05.md) (thermal contrast, hyperspectral) · [05.6 Sensor fusion](lessons/stage-05/lesson-06.md) · working knowledge of CNNs, transformers and PyTorch. **Estimated time** 8 h (4 h theory · 1 h simulator · 3 h programming) |
| Estimated time | 8 h (4 h theory · 1 h simulator · 3 h programming) |
| Level | Advanced |
| Learning objectives | 1. Derive the Bayes-optimal decision threshold under asymmetric costs and correct a classifier's<br>2. Explain the loss design of dense one-stage detectors (YOLO family: box regression with IoU<br>3. Choose between segmentation, detection and anomaly detection for a given EOD sensing task and<br>4. Implement a PatchCore-style memory-bank anomaly score and a Mahalanobis (Gaussian) score, and<br>5. Relate modality physics (RGB, thermal LWIR, X-ray transmission, GPR B-scans) to preprocessing,<br>6. Evaluate a detector with recall at fixed false-alarm rate per unit area, FROC, and exact<br>7. Design a leakage-free evaluation split for a public dataset such as AMLID or SULAND v2. |
| Theory | 1. Decisions first: cost-weighted thresholds · 2. Classification under prevalence shift · 3. Object detection · 4. Segmentation · 5. Anomaly detection: the open-set problem · 6. Modality specifics · 7. Metrics that matter · 8. Public datasets and how not to leak |
| Visual explanation | mermaid diagram + embedded simulator |
| Simulation | [detection-theory](sims/detection-theory/index.html) |
| Programming | [p09-cv-detection](projects/p09-cv-detection/README.md) |
| Reading | 6 selected items (see lesson) |
| Assessment | 7 questions + hidden-answer exercises; stage gate [assessments/stage-09.md](assessments/stage-09.md) |
| Next | [09.2 Uncertainty-aware ML](lessons/stage-09/lesson-02.md), then [09.3 Synthetic data & sim-to-real](lessons/stage-09/lesson-03.md) and [09.4 Multimodal sensing](lessons/stage-09/lesson-04.md). |

### [09.2 · Uncertainty-aware ML: calibration, ensembles, conformal prediction and abstention](lessons/stage-09/lesson-02.md)

| Field | Specification |
|---|---|
| Prerequisites | [09.1 Perception tasks](lessons/stage-09/lesson-01.md) (cost-weighted thresholds, recall at fixed FAR) · [05.1 Detection theory](lessons/stage-05/lesson-01.md) · [05.6 Sensor fusion](lessons/stage-05/lesson-06.md) (Bayesian updating) · probability (exchangeability, order statistics), information theory (entropy, mutual information). **Estimated time** 8 h (4 h theory · 1 h simulator · 3 h programming) |
| Estimated time | 8 h (4 h theory · 1 h simulator · 3 h programming) |
| Level | Advanced → Expert |
| Learning objectives | 1. Decompose predictive uncertainty into aleatoric and epistemic parts via entropy and mutual<br>2. Compute ECE and read a reliability diagram; derive the temperature-scaling optimality condition<br>3. Compare deep ensembles, MC dropout and a Laplace (Bayesian) last layer in cost, quality and<br>4. State and prove (sketch) the split-conformal coverage theorem; construct LAC, APS and RAPS<br>5. Show, with a numerical experiment, that marginal coverage can hide catastrophic coverage on a<br>6. Build risk–coverage curves and choose an abstention policy; evaluate OOD detectors with |
| Theory | 1. Aleatoric vs epistemic uncertainty · 2. Calibration and its measurement · 3. Temperature scaling · 4. Epistemic methods: ensembles, MC dropout, Bayesian last layer · 5. Conformal prediction · 6. Selective prediction and abstention · 7. Out-of-distribution detection · 8. Lab: temperature scaling and split/Mondrian conformal from scratch |
| Visual explanation | mermaid diagram + embedded simulator |
| Simulation | [sensor-fusion](sims/sensor-fusion/index.html) |
| Programming | [p09-cv-detection](projects/p09-cv-detection/README.md), [p12-hitl-decision](projects/p12-hitl-decision/README.md) |
| Reading | 5 selected items (see lesson) |
| Assessment | 7 questions + hidden-answer exercises; stage gate [assessments/stage-09.md](assessments/stage-09.md) |
| Next | [09.3 Synthetic data & sim-to-real](lessons/stage-09/lesson-03.md), [09.5 Active perception](lessons/stage-09/lesson-05.md) (uses epistemic uncertainty to choose views) and [09.6 Trustworthy deployment](lessons/stage-09/lesson-06.md). |

### [09.3 · Synthetic data & sim-to-real: generation, randomisation, adaptation and honest validation](lessons/stage-09/lesson-03.md)

| Field | Specification |
|---|---|
| Prerequisites | [09.1 Perception tasks](lessons/stage-09/lesson-01.md) (metrics, dataset leakage) · [09.2 Uncertainty-aware ML](lessons/stage-09/lesson-02.md) (calibration under shift, rare-class calibration) · [05.2 EMI & GPR](lessons/stage-05/lesson-02.md) · [05.3 Penetrating radiation](lessons/stage-05/lesson-03.md) · [05.5 Imaging & remote sensing](lessons/stage-05/lesson-05.md) · heat equation (01.2), PyTorch basics. **Estimated time** 9 h (4 h theory · 1 h simulator · 4 h programming) |
| Estimated time | 9 h (4 h theory · 1 h simulator · 4 h programming) |
| Level | Advanced → Expert |
| Learning objectives | 1. State the Ben-David domain-adaptation bound, estimate its divergence term with a domain<br>2. Design a procedural scene generator with an explicit parameter distribution, and choose between<br>3. Derive and implement simple physics-based sensor models — diurnal thermal response of soil,<br>4. Implement and critique domain adaptation: fine-tuning, DANN with gradient reversal,<br>5. Measure the sim-to-real gap with TSTR/TRTR, feature distances (Fréchet, domain-classifier<br>6. Write a dataset card and a real-data validation protocol; quantify the effect of label noise on |
| Theory | 1. The formal problem: why source accuracy is not enough · 2. Procedural scene generation · 3. Domain randomisation · 4. Physics-based sensor simulation · 5. Domain adaptation · 6. Measuring the sim-to-real gap · 7. Dataset cards and validation on real data · 8. Label noise: the SULAND v2 lesson |
| Visual explanation | mermaid diagram + embedded simulator |
| Simulation | [recognition-trainer](sims/recognition-trainer/index.html) |
| Programming | [p10-scene-generator](projects/p10-scene-generator/README.md) |
| Reading | 6 selected items (see lesson) |
| Assessment | 7 questions + hidden-answer exercises; stage gate [assessments/stage-09.md](assessments/stage-09.md) |
| Next | [09.4 Multimodal sensing](lessons/stage-09/lesson-04.md) (registration of the modalities you learn to simulate here) and [09.6 Trustworthy deployment](lessons/stage-09/lesson-06.md) (test & evaluation). |

### [09.4 · Multimodal sensing: camera, depth and thermal fusion](lessons/stage-09/lesson-04.md)

| Field | Specification |
|---|---|
| Prerequisites | [09.1 Perception tasks](lessons/stage-09/lesson-01.md) (detectors, recall at fixed FAR) · [05.5 Imaging & remote sensing](lessons/stage-05/lesson-05.md) (thermal IR physics) · [05.6 Sensor fusion](lessons/stage-05/lesson-06.md) (Bayesian fusion, correlated errors) · [06.2 Spatial mathematics](lessons/stage-06/lesson-02.md) (SE(3), camera frames) · linear algebra incl. SVD. **Estimated time** 7 h (3.5 h theory · 1 h simulator · 2.5 h programming) |
| Estimated time | 7 h (3.5 h theory · 1 h simulator · 2.5 h programming) |
| Level | Advanced |
| Learning objectives | 1. Write the pinhole projection model with intrinsics and extrinsics, and compute pixel footprint,<br>2. Derive the **plane-induced homography** between two cameras, estimate a homography by the<br>3. Budget registration error from **time offset** and motion, and specify synchronisation<br>4. Apply sensor-appropriate processing: photon-transfer noise model, histogram equalisation and<br>5. Predict depth error for stereo and time-of-flight sensors and list their outdoor failure modes.<br>6. Choose between early, mid and late fusion and design a **missing-modality** test matrix. |
| Theory | 1. Camera intrinsics: from a point to a pixel · 2. Extrinsics and the plane-induced homography · 3. Estimating a homography: the normalised DLT, and thermal–RGB targets · 4. Time synchronisation · 5. Low-light and infrared image processing · 6. Depth sensing and its outdoor failure modes · 7. Fusion architectures: early, mid, late · 8. Missing-modality robustness |
| Visual explanation | mermaid diagram + embedded simulator |
| Simulation | [sensor-fusion](sims/sensor-fusion/index.html) |
| Programming | [p03-bayesian-fusion](projects/p03-bayesian-fusion/README.md), [p09-cv-detection](projects/p09-cv-detection/README.md) |
| Reading | 6 selected items (see lesson) |
| Assessment | 7 questions + hidden-answer exercises; stage gate [assessments/stage-09.md](assessments/stage-09.md) |
| Next | [09.5 Active perception & exploration](lessons/stage-09/lesson-05.md), then [09.6 Trustworthy deployment](lessons/stage-09/lesson-06.md). |

### [09.5 · Active perception & autonomous exploration](lessons/stage-09/lesson-05.md)

| Field | Specification |
|---|---|
| Prerequisites | [09.2 Uncertainty-aware ML](lessons/stage-09/lesson-02.md) (calibrated probabilities) · [05.6 Sensor fusion](lessons/stage-05/lesson-06.md) (expected information gain) · [06.7 Mapping & SLAM](lessons/stage-06/lesson-07.md) (occupancy grids, log-odds) · [06.8 Path & motion planning](lessons/stage-06/lesson-08.md) (Dijkstra/A*, cost maps) · [07.1 Decisions under uncertainty](lessons/stage-07/lesson-01.md) (value of information, POMDP framing). **Estimated time** 7 h (3.5 h theory · 1 h simulator · 2.5 h programming) |
| Estimated time | 7 h (3.5 h theory · 1 h simulator · 2.5 h programming) |
| Level | Expert |
| Learning objectives | 1. Define active perception (Bajcsy) and cast view selection as maximising expected utility of<br>2. Compute the entropy of an occupancy/belief map and the **expected information gain** (mutual<br>3. Implement **frontier-based exploration** (Yamauchi) and a next-best-view utility, and explain<br>4. Formulate **risk-aware** exploration with chance-constrained standoff from an uncertain hazard<br>5. Explain exploration–exploitation trade-offs (UCB), the POMDP belief-update view of active<br>6. Allocate exploration targets across multiple robots with a sequential auction and state its |
| Theory | 1. Active perception · 2. Map entropy and the log-odds update · 3. Expected information gain of a measurement and of a view · 4. Next-best-view and the greedy guarantee · 5. Frontier-based exploration · 6. Risk-aware exploration: standoff from an uncertain hazard map · 7. Exploration versus exploitation · 8. Belief-space planning and POMDPs · 9. Reinforcement learning for navigation — and its caveats · 10. Multi-robot exploration and task allocation |
| Visual explanation | mermaid diagram + embedded simulator |
| Simulation | [robotics-engineering](sims/robotics-engineering/index.html), [scene-assessment](sims/scene-assessment/index.html) |
| Programming | [p06-path-planning](projects/p06-path-planning/README.md), [p07-slam](projects/p07-slam/README.md) |
| Reading | 7 selected items (see lesson) |
| Assessment | 7 questions + hidden-answer exercises; stage gate [assessments/stage-09.md](assessments/stage-09.md) |
| Next | [09.6 Trustworthy deployment](lessons/stage-09/lesson-06.md), then Capstone C1. |

### [09.6 · Trustworthy deployment: robustness, explainability, edge inference and the human in the loop](lessons/stage-09/lesson-06.md)

| Field | Specification |
|---|---|
| Prerequisites | [09.1 Perception tasks](lessons/stage-09/lesson-01.md) (recall at fixed FAR) · [09.2 Uncertainty-aware ML](lessons/stage-09/lesson-02.md) (calibration, conformal prediction) · [09.3 Synthetic data & sim-to-real](lessons/stage-09/lesson-03.md) · [05.1 Detection theory](lessons/stage-05/lesson-01.md) (ROC, base rates) · [06.5 Teleoperation & HMI](lessons/stage-06/lesson-05.md) (supervisory control, workload) · [06.6 State estimation](lessons/stage-06/lesson-06.md) (innovation tests). **Estimated time** 8 h (4 h theory · 1 h simulator · 3 h programming) |
| Estimated time | 8 h (4 h theory · 1 h simulator · 3 h programming) |
| Level | Expert |
| Learning objectives | 1. Explain why high-dimensional models are vulnerable to small perturbations (linearity argument),<br>2. Design a physical-robustness test programme inspired by adversarial-patch and RP2 methodology,<br>3. Monitor for distribution shift with input statistics (PSI), innovation tests and calibration<br>4. Compute and critique Grad-CAM-style explanations and name their documented failure modes.<br>5. Budget edge inference (quantisation error, compute/memory roofline, energy per frame) against<br>6. Design operator displays and alert policies that counter automation bias and alarm fatigue,<br>7. Size a test campaign statistically and structure an **assurance case** for a safety-relevant ML |
| Theory | 1. Adversarial examples and the linearity argument · 2. PGD as an evaluation tool; adversarial training; certification · 3. Physical-world robustness: from adversarial patches to a test programme · 4. Sensor spoofing and degradation; consistency checks · 5. Distribution-shift monitoring · 6. Explainability — and how explanations fail · 7. Edge inference: quantisation, pruning, latency and energy · 8. The human in the loop: automation bias, alarm fatigue, calibrated trust · 9. False-positive management: cost-weighted thresholds and cascades · 10. Test & evaluation and assurance cases |
| Visual explanation | mermaid diagram + embedded simulator |
| Simulation | [detection-theory](sims/detection-theory/index.html) |
| Programming | [p09-cv-detection](projects/p09-cv-detection/README.md), [p12-hitl-decision](projects/p12-hitl-decision/README.md) |
| Reading | 7 selected items (see lesson) |
| Assessment | 8 questions + hidden-answer exercises; stage gate [assessments/stage-09.md](assessments/stage-09.md) |
| Next | [Project P12 — Human-in-the-loop decision support](projects/p12-hitl-decision/README.md), Capstones, and the case studies of Stage 10 (e.g. [counter-IED robots](case-studies/cs06-counter-ied-robots.md)). |

