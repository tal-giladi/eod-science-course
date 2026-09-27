# CS-6 · Iraq and Afghanistan: counter-IED robots at scale

<div class="module-card">

**Read after** [06.5 Teleoperation & HMI](lessons/stage-06/lesson-05.md) and [06.9 Comms & fail-safe design](lessons/stage-06/lesson-09.md) · **Also exercises** [06.1 EOD robot systems](lessons/stage-06/lesson-01.md), [03.4 Improvised hazards](lessons/stage-03/lesson-04.md), [09.6 Trustworthy deployment](lessons/stage-09/lesson-06.md)

**Estimated time** 2 h (reading 50 min · questions 70 min) · **Level** Advanced

<p class="tags"><span>robotics</span><span>acquisition</span><span>HRI</span><span>interoperability</span><span>C-IED</span><span>Sim B</span></p>
</div>

<div class="callout boundary">

**Boundary.** Nothing here describes improvised devices, how robots are used against them, or
any tactic, technique or procedure. The subject is the *system of systems*: acquisition, fleet
management, human–robot interaction and engineering lessons.

</div>

## Situation

After the invasions of Afghanistan (2001) and Iraq (2003), improvised explosive devices (IEDs)
became a principal cause of coalition casualties. A 2013 White House policy statement quoted by
RAND called IEDs "one of the most accessible weapons" available to terrorists and criminals
(RAND RR-421, 2014). The US response grew through a sequence of organisations (RAND, 2014;
GAO-12-280):

| Year | Organisation |
|---|---|
| 2003 | Army IED Task Force |
| 2004 | Army-led Joint Integrated Process Team under the Deputy Secretary of Defense |
| Jun 2005 | Joint IED Defeat Task Force |
| **14 Feb 2006** | **Joint IED Defeat Organization (JIEDDO)**, DoD Directive 2000.19E |
| later | Joint Improvised-Threat Defeat Organization (JIDO), under the Defense Threat Reduction Agency |

JIEDDO organised its work along three lines of operation: **attack the network**, **defeat the
device** and **train the force** (RAND, 2014). By early 2012 **more than USD 18 billion** had
been appropriated to it (GAO-12-280).

Unmanned ground vehicles were a central part of "defeat the device". They were used for
reconnaissance, inspection and remote handling of suspect items, so that a technician did not
have to approach.

## Technology available

| Platform | Class | Notes (public sources) |
|---|---|---|
| **TALON** (Foster-Miller / QinetiQ NA) | Medium, tracked | First deployed in Bosnia in 2000; used at Ground Zero in 2001; the manufacturer claims about 20,000 EOD missions in Iraq and Afghanistan (Wikipedia) |
| **PackBot** (iRobot) | Man-portable, tracked with flippers | Fielded in Afghanistan from 2002; the original version weighed 42 lb with camera and extendable arm (ASC, 2017/18). Modular payload bus described in Yamauchi (2004) |
| **PackBot with Fido** | PackBot + explosive-vapour sensor | Prototype built in 90 days; four units sent to Iraq for evaluation; JIEDDO then procured 120 and eventually more than 200 (ASC) |
| **Dragon Runner** and many others | Small | Part of a rapidly growing, diverse fleet |
| Heavy platforms (e.g. ANDROS, tEODor) | Heavy | Large payload and reach; less portable ([06.1](lessons/stage-06/lesson-01.md)) |

Common features: teleoperation over radio, several cameras, a manipulator arm, operator control
units (OCUs) with video displays, and almost no autonomy beyond simple functions.

## Information available to technicians and to the organisation

**At the incident**: a report or indicator; what the robot's cameras and sensors showed; pattern
knowledge from intelligence and technical exploitation of earlier incidents; the tactical
situation (threat of attack on the team).

**At the organisational level**: casualty data; field reports on which platforms worked; vendor
claims; a flood of new initiatives. What was **missing** was a single inventory of what had been
bought, how it performed, and what it cost to sustain. GAO later found that DoD had no complete
inventory of counter-IED initiatives and identified six overlapping systems worth about USD 104
million (GAO-12-280). A RAND review of JIEDDO training programmes found 20 initiatives that
service representatives considered potentially duplicative, reduced to 13 after stakeholder
meetings (RAND, 2014).

## Hazards

- **Adaptive adversary**: devices and tactics changed in response to countermeasures, including
  targeting of responders and robots ([03.4](lessons/stage-03/lesson-04.md)).
- **Direct attack** on teams during an incident.
- **Communications degradation**: terrain, distance, and interference from other electronic
  systems ([06.9](lessons/stage-06/lesson-09.md)).
- **Environment**: heat, dust, sand, rubble, stairs and culverts.
- **Human factors**: workload, poor situational awareness through cameras, fatigue, and
  attachment to robots ([06.5](lessons/stage-06/lesson-05.md)).
- **Logistics**: many robot types, each with its own spares, batteries, software and training.

## Decisions

### Decision point 1 — speed versus standardisation (acquisition)

| Known | Unknown |
|---|---|
| Casualties were rising; robots could take the exposure | Which platforms would prove best; lifetime sustainment cost; how the threat would evolve |

The choice was to **field fast**: buy what was available, prototype in weeks (Fido in 90 days),
and let the field decide. That saved time, and by the organisation's own account it saved
lives. The cost was a fragmented fleet. The Army bought **more than 7,000 unique robotic
systems**, many with proprietary software and payloads that could not move between platforms
(ASC, 2017/18).

### Decision point 2 — at the incident: robot first?

A robot-first approach extends the logic of [CS-1](case-studies/cs01-wheelbarrow.md). Every
observation or manipulation done by the robot is exposure the technician does not take. The
constraints are time (a robot is slower), capability (the task may exceed the arm or the
cameras), and the robot's own survivability and communications.

### Decision point 3 — how much autonomy?

With a human at the OCU and the adversary adapting, autonomy was kept minimal. Parasuraman,
Sheridan and Wickens (2000) give a framework for deciding *which stage* of information
processing to automate: acquisition, analysis, decision or action. Automating *acquisition and
analysis* (stabilised video, sensor fusion, mapping) is lower risk than automating *decisions
and actions* on a suspect item. See [09.6](lessons/stage-09/lesson-06.md).

### Decision point 4 — consolidate the fleet (2017–18)

| Known by 2017 | Unknown |
|---|---|
| The sustainment and training burden of a fragmented fleet | Future threats; the effect of interoperability standards on innovation |

The Army moved to **three platform classes** with a common **Unmanned Ground Vehicle
Interoperability Profile (IOP)** so that payloads could move between platforms (ASC, 2017/18;
National Defense Magazine, 2018):

| Programme | Class | Published figure |
|---|---|---|
| CRS-I (Common Robotic System – Individual) | Man-portable | ~25 lb (ASC); ~32 lb and fits in an assault pack (army.mil, 2019) |
| MTRS Inc II (Man Transportable Robotic System) | Medium | ~164 lb; USD 100 million contract (ASC) |
| CRS-H (Common Robotic System – Heavy) | Heavy | up to ~1,000 lb (ASC) |

## Technology used

- Teleoperated UGVs of several classes, with cameras, arms and some payload sensors.
- Operator control units, and later **handheld common controllers** under the IOP approach
  (National Defense Magazine, 2018).
- **Standard test methods** for response robots (NIST / ASTM E54.09), partly funded by JIEDDO,
  to measure mobility, dexterity, sensing, communications and operator proficiency in a
  reproducible way. They were also used for counter-IED operator training (NIST, 2015).

## Human–robot interaction findings

Julie Carpenter interviewed **23 EOD personnel** (22 men, 1 woman) across the US services
(University of Washington, 2013; Carpenter, 2016):

- Operators insisted the robot was a **tool**. Yet they named robots, sometimes after partners
  or celebrities, painted names on them, and in some cases held "funerals" for destroyed
  robots.
- They reported **frustration, anger and sadness** when a robot was destroyed, and said this did
  **not** affect their decisions.
- Carpenter's concern was forward-looking. As robots become more human- or animal-like,
  operators might **hesitate to send them into danger**, and that hesitation could compromise
  the mission.

For an engineer, the implication is that **the robot's social presence is a design variable.**
A consumable must be *treated* as consumable. Design choices such as anthropomorphic form,
names, "personality" and voice can shift the operator's cost function in ways nobody intended.

## Outcome

- Robots became **standard equipment** for military EOD teams. Robot-first procedures moved a
  large share of close-in exposure from people to machines. The manufacturer's claim of about
  20,000 TALON EOD missions gives a sense of scale (Wikipedia). The ASC article describes a
  destroyed robot part kept on a plaque because the robot's loss saved a soldier's life, the
  same "the robot is the consumable" logic as in 1972.
- There is no public, rigorous estimate of total lives saved. That would need counterfactual
  exposure data that has not been published.
- The **fragmented fleet** created large sustainment, training and interoperability costs. It
  led to the 2017–18 consolidation and the IOP.
- GAO criticised the lack of **strategic, outcome-related goals** and of an inventory of
  initiatives (GAO-12-280).

## Lessons learned

1. **Rapid fielding and long-term architecture pull in opposite directions.** Both are needed.
   An explicit plan to consolidate should be part of any rapid-fielding programme from day one:
   a "technical debt budget".
2. **Interfaces outlive platforms.** A common interoperability profile for payloads, controllers
   and messages is worth more than any single robot. Software engineers will recognise the
   value of stable APIs.
3. **Measure capability with standard test methods.** Vendor claims and anecdotes do not add up
   to evidence. NIST/ASTM E54.09 test methods gave reproducible metrics and a shared language
   between buyers, vendors and trainers.
4. **Keep an inventory.** You cannot manage duplication or measure outcomes without knowing what
   you have bought (GAO-12-280).
5. **Human factors are first-order.** Situational awareness through cameras, workload, latency
   and even emotional attachment affect mission outcomes ([06.5](lessons/stage-06/lesson-05.md)).
6. **Adversaries adapt to robots too.** Assume that any predictable robot behaviour will be
   studied and exploited. Design for variability and resilience ([09.6](lessons/stage-09/lesson-06.md)).

## Technological developments that followed

- **Common robotic system families** with a shared IOP: CRS-I, MTRS Inc II, CRS-H (National
  Defense Magazine, 2018; NDIA brief, 2017).
- In the UK, the **L3Harris T7** replaced Wheelbarrow in 2019 (Wikipedia, *Wheelbarrow
  (robot)*).
- **Standardised performance testing** and operator proficiency measurement (NIST test
  methods, including the C-IED training document).
- **ROS-based and open architectures** in research and increasingly in industry (ROS 2 docs),
  and research on **multi-robot, comms-denied autonomy** such as the DARPA Subterranean
  Challenge (Chung et al., 2023).
- **HRI research** on trust, attachment and interface design for EOD (Carpenter, 2016; Chen et
  al., 2007).

## Discussion questions

1. The Army bought more than 7,000 unique robotic systems. Using a simple model, suppose each
   distinct platform type needs a fixed sustainment overhead $F$ per year (spares pipeline,
   training course, software maintenance) plus a per-unit cost $c$. Compare the annual cost of
   $N=7{,}000$ units spread over $k=30$ types with the same units over $k=3$ types. At what $F/c$
   ratio does consolidation save more than 20%?

<details class="answer"><summary>Answer — then reveal</summary>

Cost $C(k) = kF + Nc$. The saving from going from 30 types to 3 is $27F$. As a fraction of
$C(30) = 30F + Nc$, it is $27F/(30F + Nc) > 0.2$, so $27F > 6F + 0.2Nc$, so $21F > 1{,}400c$,
so $F/c > 66.7$. If the fixed overhead per type exceeds about 67 unit-years of per-unit cost,
consolidation saves more than 20%. For training pipelines and software stacks this is
plausible. Consolidation also has benefits the model leaves out: operators move between units,
and payloads are shared.

</details>

2. Carpenter's interviewees said attachment did not affect their decisions. Why might
   self-report be an unreliable measure here? Design an experiment, in simulation, that could
   test whether naming or anthropomorphising a robot changes risk-taking with it.

<details class="answer"><summary>Answer — then reveal</summary>

Self-report is affected by social desirability (professionals are expected to say they are
rational), limited introspective access, and after-the-fact rationalisation. Experiment:
between-subjects in [Sim B](sims/eod-robot/index.html) or a similar simulator. One group gets an
unnamed, utilitarian robot. The other gets the same robot with a name and "personality" cues
and a short familiarisation period. The task includes decision points where sending the robot
into a risky position is optimal by the task's cost function. Measure the rate of choosing the
optimal but robot-risky action, time to decide, and physiological or self-report stress.
Pre-register the hypotheses and power the study for a modest effect.

</details>

3. Using the Parasuraman–Sheridan–Wickens model, list what you would automate on a modern EOD
   robot at each of the four stages, and what you would deliberately keep manual. Justify each
   choice using failure consequences and adversarial robustness.

4. The Fido payload was prototyped in 90 days. What processes and architecture choices make that
   speed possible, and what risks come with it? How would a common interoperability profile
   change the answer?

5. No public source rigorously estimates lives saved by robots in Iraq and Afghanistan. Design a
   study that could estimate it from incident-level data: what data would you need, which
   confounders matter, and what identification strategy would you use?

<details class="answer"><summary>Answer — then reveal</summary>

Data: incident records with whether and how the robot was used, the stage at which a human
approached, time on target, outcomes (injuries, deaths, device function), team experience,
region and period, and threat type. Confounders: robots may have been used more on
harder-looking incidents (selection), threat evolution over time, and team skill. Strategies:
exploit staggered fielding across units (difference-in-differences), robot unavailability due
to maintenance as a quasi-random instrument, or matching on incident characteristics. Report
exposure-time reduction, a quantity closer to the mechanism, alongside casualty effects.

</details>

6. Fragmented fleet versus premature standardisation: find an analogy in software (for example,
   microservices and a platform team, or framework proliferation) and use it to argue when a
   programme should switch from "let a thousand flowers bloom" to "consolidate".

## Sources

| Title | Organisation / author | Date | URL |
|---|---|---|---|
| How many robots does it take? | S. Pidgeon, US Army Acquisition Support Center (Army AL&T, Jan–Mar 2018 issue) | Nov 2017 | https://asc.army.mil/web/news-alt-jfm18-how-many-robots-does-it-take/ |
| Assessment of Joint Improvised Explosive Device Defeat Organization (JIEDDO) Training Activity (RR-421) | RAND National Defense Research Institute | 2014 | https://www.rand.org/content/dam/rand/pubs/research_reports/RR400/RR421/RAND_RR421.pdf |
| Warfighter Support: DOD Needs Strategic Outcome-Related Goals and Visibility over Its Counter-IED Efforts (GAO-12-280) | US Government Accountability Office | 22 Feb 2012 | https://www.gao.gov/products/gao-12-280 |
| Joint Improvised-Threat Defeat Organization | Wikipedia | accessed 2026 | https://en.wikipedia.org/wiki/Joint_Improvised-Threat_Defeat_Organization |
| Foster-Miller TALON | Wikipedia | accessed 2026 | https://en.wikipedia.org/wiki/Foster-Miller_TALON |
| PackBot: a versatile platform for military robotics | B. M. Yamauchi, Proc. SPIE 5422 | 2004 | https://doi.org/10.1117/12.538328 |
| Army Developing Family of Explosive Ordnance Disposal Robots | National Defense Magazine | 25 May 2018 | https://www.nationaldefensemagazine.org/articles/2018/5/25/army-developing-family-of-explosive-ordnance-disposal-robots |
| Common Robotic System (Individual) brief to NDIA | US Army PM Force Projection | Jul 2017 | https://www.ndia.org/-/media/sites/ndia/divisions/robotics/anulare_pm-fp-robotics-brief-to-ndia_final---july-2017.pdf |
| 82nd Airborne tests new portable robot for individual Soldiers | US Army | 2019 | https://www.army.mil/article/228363/82nd_airborne_tests_new_portable_robot_for_individual_soldiers |
| Emotional attachment to robots could affect outcome on battlefield | University of Washington News | 17 Sep 2013 | https://www.washington.edu/news/2013/09/17/emotional-attachment-to-robots-could-affect-outcome-on-battlefield/ |
| Culture and Human-Robot Interaction in Militarized Spaces: A War Story | J. Carpenter, Routledge | 2016 | https://www.routledge.com/Culture-and-Human-Robot-Interaction-in-Militarized-Spaces-A-War-Story/Carpenter/p/book/9781032928456 |
| A model for types and levels of human interaction with automation | R. Parasuraman, T. B. Sheridan, C. D. Wickens, IEEE Trans. SMC-A 30(3) | 2000 | https://doi.org/10.1109/3468.844354 |
| Human Performance Issues and User Interface Design for Teleoperated Robots | J. Y. C. Chen, E. C. Haas, M. J. Barnes, IEEE Trans. SMC-C 37(6) | 2007 | https://doi.org/10.1109/TSMCC.2007.905819 |
| Standard Test Methods for Response Robots | NIST / ASTM E54.09 | ongoing | https://www.nist.gov/el/intelligent-systems-division-73500/standard-test-methods-response-robots |
| C-IED Training Using Standard Test Methods for Response Robots (v2015) | NIST | 2015 | https://www.nist.gov/document/c-ied-training-using-standard-test-methods-response-robots-v2015pdf |
| Into the Robotic Depths: Analysis and Insights from the DARPA Subterranean Challenge | T. H. Chung, V. Orekhov, A. Maio, *Annual Review of Control, Robotics, and Autonomous Systems* | 2023 | https://www.annualreviews.org/content/journals/10.1146/annurev-control-062722-100728 |
| Wheelbarrow (robot) | Wikipedia | accessed 2026 | https://en.wikipedia.org/wiki/Wheelbarrow_(robot) |
