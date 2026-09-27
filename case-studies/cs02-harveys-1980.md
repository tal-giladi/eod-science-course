# CS-2 · Harvey's Resort Hotel, 1980: deciding under deep uncertainty

<div class="module-card">

**Read after** [07.1 Decisions under uncertainty](lessons/stage-07/lesson-01.md) and [07.2 Incident management](lessons/stage-07/lesson-02.md) · **Also exercises** [03.4 Improvised hazards](lessons/stage-03/lesson-04.md), [05.3 Penetrating radiation](lessons/stage-05/lesson-03.md), [08.1 The post-blast scene](lessons/stage-08/lesson-01.md)

**Estimated time** 2 h (reading 50 min · discussion questions 70 min) · **Level** Advanced

<p class="tags"><span>decision theory</span><span>deep uncertainty</span><span>evacuation</span><span>radiography</span><span>training</span></p>
</div>

<div class="callout boundary">

**Boundary.** The device in this case is described only as "a very large improvised device".
Its construction, its internal mechanisms and the technique used in the intervention are
deliberately left out. They are not needed for the decision analysis, and describing them
would cross the course's safety boundary. The public FBI page has more detail. This course
does not reproduce it.

</div>

## Situation

In the early morning of **26 August 1980**, men dressed as delivery workers brought what looked
like an office copier into Harvey's Resort Hotel and Casino in Stateline, Nevada, on the shore
of Lake Tahoe. It was a very large improvised device. An extortion note left with it demanded
**USD 3 million** and warned the management and the bomb squad not to move it, tilt it or try
to open it. It claimed the device could not be disarmed "not even by the creator" (FBI, *Harvey's
Casino Bomb*). The note offered instructions for making the device movable in exchange for
payment.

Local bomb technicians and FBI explosives experts were called in. The device was
photographed, examined for fingerprints, **radiographed (X-rayed)** and studied for **more than
30 hours** before a plan was agreed (FBI). Harvey's and nearby casinos were evacuated. On the
afternoon of **27 August** a remotely executed intervention was attempted. The FBI's own
account calls it "the best one available at the time". It did not work. The device functioned
and left a crater five storeys high in the hotel. **Because of the evacuation, no one was
killed or injured** (FBI).

The investigation that followed identified the perpetrator, a man who had lost heavily at the
casino. He was convicted of federal extortion and bombing charges. Accomplices were also
prosecuted (FBI; Wikipedia, *Harvey's Resort Hotel bombing*). The FBI Laboratory later built a
mock-up of the device for the trial and still uses it for training (FBI).

## Technology available

| Capability | Available in 1980 | Limitation |
|---|---|---|
| Radiography | Portable X-ray, film based | Two-dimensional projections of a dense, cluttered object. Superposition hides depth. Film needs developing, which costs time on every exposure |
| Photography | Still film cameras | Documentation, not diagnosis |
| Fingerprints and trace | Standard forensic methods | Useful for the investigation, not for the decision |
| Remote means | Remote initiation of tools from a distance; teleoperated robots existed (see [CS-1](case-studies/cs01-wheelbarrow.md)) but were not standard equipment for US civilian bomb squads | Few options to *act* on the device without a person present |
| Expert knowledge | Experienced technicians and laboratory examiners | No previous case of comparable complexity. The FBI examiner recalled that "we had never seen anything quite like it" |
| Communications and computing | Telephone and radio; no digital imaging, no simulation | Analysis was manual and slow |

Radiography physics (attenuation, contrast, superposition) is covered in
[05.3](lessons/stage-05/lesson-03.md). The key point here is epistemic. **A projection image of
a complex object is an underdetermined inverse problem.** Many internal configurations fit the
same set of images. Each extra view reduces the ambiguity, but in 1980 each view cost time.

## Information available to technicians

**Known with reasonable confidence**

- The location, size and approximate mass class of the object: large enough that a function
  would severely damage a large building.
- The perpetrator's *claims*, from the note, which amounted to "do not touch it".
- What the radiographs, photographs and external examination showed.
- That the perpetrator wanted money and had set up a channel for negotiation.

**Unknown or unverifiable**

- Whether the claims in the note were true, exaggerated or partly bluff. An extortionist has an
  incentive both to exaggerate (to force payment) and to be truthful (to be believed).
- Whether the negotiation channel was genuine and whether any instructions provided would be
  honest or complete.
- Whether a time limit existed and how long it was. The note implied time pressure.
- Internal features that the radiographs could not resolve.
- How the device would respond to any given intervention. This is the crucial unknown: nobody
  had a model of the system's response that could be trusted.

## Hazards

- **Primary blast** at a scale that threatened the structure of a multi-storey building, and
  debris and fragments across a wide area. See [04.2](lessons/stage-04/lesson-02.md) and
  [04.3](lessons/stage-04/lesson-03.md).
- **Structural collapse** and secondary hazards (fire, gas, utilities).
- **Responder exposure** during any close examination.
- **Time pressure** from an unknown delay, an ongoing extortion and the economic cost of closing
  a resort district.
- **Adversarial design.** The object had been designed to defeat interference. The main
  hazard was not random failure but an intelligent opponent.

## Decisions

The case is best studied as a sequence of decisions under **deep uncertainty**, where the
probabilities themselves cannot be estimated with confidence.

### Decision point 1 — cordon and evacuation

| Known | Unknown |
|---|---|
| The potential scale of the hazard | Whether and when it would function |
| The cost of evacuating a resort district | Whether the note was a bluff |

Evacuation is a **no-regret action** in the language of robust decision-making. If the device
never functions, the cost is disruption. If it does, the evacuation decides whether anyone dies.
Its value does not depend on resolving the uncertainty about the device, and this is exactly why
it should be taken early and in full. In the event it was the decision that saved everyone.

### Decision point 2 — how much time to spend on diagnosis

| Known | Unknown |
|---|---|
| Each diagnostic step (another image, another expert) adds information | The deadline, if any |
| Each close approach exposes a person | Whether more information would change the decision |

This is a **value-of-information** problem ([07.1](lessons/stage-07/lesson-01.md)). Information
has value only if it can change the choice of action. After a certain point, more radiographs
of an object whose response cannot be modelled may not change the ranking of options. In the
meantime the risk of a delay-triggered function keeps building. The team studied the device
for more than 30 hours. With hindsight students may argue about whether that was too long or
too short, but the right question is: *what observation, if made, would have changed the
decision?*

### Decision point 3 — choose among the families of outcome

At the organisational level ([07.2](lessons/stage-07/lesson-02.md)) the options were:

| Option | Main argument for | Main argument against |
|---|---|---|
| A. Negotiate / pay for instructions | The perpetrator claims to hold the only reliable model of the device | Rewards extortion. The instructions cannot be verified. The perpetrator gains from partial compliance. It sets a precedent |
| B. Let it function in place with everyone evacuated | Zero risk to people once the evacuation is complete | Certain destruction of a large building. The time of function is unknown, so the area stays closed indefinitely |
| C. Attempt a remote intervention with everyone evacuated | Chance of saving the building. No person is exposed at the moment of action | The response of the device is unpredictable. Failure means the same outcome as B, but sooner |
| D. Manual intervention | The most control | Unacceptable exposure against a device designed to defeat interference |

Once the evacuation was in place, options B and C had **the same worst case**: the building is
lost and no one is hurt. C had an upside that B lacked. Given that structure, choosing a remote
intervention was rational even with a low probability of success. That is the sense in which
the FBI could call it the best plan available even though it failed. A good decision can have
a bad outcome, and an evaluation should separate the two. The literature calls the failure to
do so **outcome bias**.

### What went wrong, at a high level

- The intervention relied on a **model of the device** that proved incomplete. The diagnostic
  technology of the day could not see enough of the interior to resolve the ambiguity.
- The device was **novel**. There was no reference class of similar cases and no experience to
  calibrate against.
- The adversary had **designed specifically against intervention**. In game-theoretic terms the
  responders were playing against an opponent who anticipated their moves, not against nature.

What went **right** was the part of the plan that did not depend on the technical solution
working: **cordon, evacuation and standoff.**

## Technology used

- Portable **radiography** and **photography** for diagnosis and documentation.
- **Fingerprint and forensic examination** of the device and the scene.
- A **remotely initiated intervention**, so that no person was near the device at the moment of
  action.
- After the event, **evidence recovery by sifting** debris at scale (FBI), which supported the
  prosecution.

## Outcome

| Dimension | Result |
|---|---|
| Life safety | No deaths, no injuries (FBI) |
| Property | Severe damage; a five-storey crater in the hotel (FBI) |
| Extortion | No ransom paid |
| Justice | The perpetrator was identified, convicted, and died in prison in 1996 (FBI) |
| Institutional | A replica built for the trial became a long-lived training aid for the FBI Laboratory (FBI). Replica-based training scenarios were still being run on the anniversary of the event decades later (Mystery Wire, 2021) |

## Lessons learned

1. **Design the plan so that the technical solution is allowed to fail.** The life-safety
   layer (evacuation, standoff) has to be independent of the technical layer (the
   intervention). This is defence in depth, the same principle as independent safety features
   in a safety-and-arming system ([03.2](lessons/stage-03/lesson-02.md)).
2. **Take no-regret actions first.** Evacuation paid off in every scenario.
3. **Diagnosis has diminishing returns, and time costs something.** Collect the information
   that could change the decision and stop when it no longer can.
4. **Judge decisions, not outcomes.** A post-incident review that condemns the choice because it
   failed teaches the wrong lesson.
5. **Treat adversarial claims as information with an agenda.** The note was both a threat and
   evidence, and it was written to shape the responders' decisions.
6. **Novel threats defeat reference-class reasoning.** When nothing comparable has been seen
   before, the uncertainty is about the model itself, not just its parameters. Robust options
   beat optimal-looking ones.

## Technological developments that followed

The developments below were driven by many incidents and many organisations. Harvey's is one
well-known reference point among them, not their sole cause.

- **Training on complex, novel devices.** The FBI Laboratory's replica is still used in training
  (FBI). The FBI's **Hazardous Devices School** at Redstone Arsenal was founded in 1971 and is
  the only facility that trains and certifies US public-safety bomb technicians. It has trained
  more than 20,000 responders (FBI, *Inside the FBI's Hazardous Devices School*). Case-based
  training on devices of this kind became part of the culture.
- **Diagnostic imaging.** Film radiography gave way to **digital radiography** with immediate
  images. Computed tomography and dual-energy methods ([05.3](lessons/stage-05/lesson-03.md))
  followed in laboratories and security screening (Wells & Bradley, 2012). All of these reduce
  the time cost per observation and the ambiguity of each image, which are the two quantities
  that limited the 1980 team.
- **Remote platforms for civilian bomb squads.** Robots with manipulator arms and cameras
  became standard equipment ([06.1](lessons/stage-06/lesson-01.md)). They allow examination and
  intervention with no human exposure.
- **Institutional device analysis.** Centres such as the FBI's TEDAC (created in 2003) collect
  and analyse devices so that the next team faces less novelty (FBI, *TEDAC*).

## Discussion questions

1. Write down the decision in a simple form. Take options B (let it function, evacuated) and C
   (remote intervention, evacuated). Let $p$ be the probability that C succeeds, $L$ the loss of
   the building, and $c_t$ the cost per hour of keeping the district closed. Suppose that under
   B the device functions at an unknown time with expected delay $\tau_B$ hours and that C takes
   $\tau_C$ hours to prepare. Show that C is preferred for any $p > 0$ when
   $\tau_C \le \tau_B$. What changes if C could *increase* the risk to people?

<details class="answer"><summary>Answer — then reveal</summary>

Expected loss of B: $L + c_t \tau_B$. Expected loss of C: $(1-p)L + c_t \tau_C$.
C is preferred when $(1-p)L + c_t\tau_C < L + c_t\tau_B$, that is when
$pL > c_t(\tau_C - \tau_B)$. If $\tau_C \le \tau_B$ the right-hand side is $\le 0$, so any
$p>0$ makes C better. If C could expose people (for example, if the evacuation had to be
relaxed or someone had to approach), you add a term with a very large loss multiplied by a
small probability. This can reverse the ranking, and it is why the life-safety layer has to be
kept independent of the intervention.

</details>

2. Evacuation was a "no-regret" action. Name another action at such an incident that is
   no-regret, and one that looks attractive but is *not* no-regret. Explain the difference.

<details class="answer"><summary>Answer — then reveal</summary>

No-regret examples: pushing the cordon out; stopping gas and utilities; preserving the scene
and evidence; bringing specialist resources forward. Not no-regret: paying the extortion.
Its value depends entirely on the perpetrator's honesty, and it has costs (precedent, reward)
in every scenario. Similarly, a close manual examination for more information adds exposure in
every scenario and pays off only in some. No-regret actions have non-negative value in every
plausible state of the world. The others pay off only in some states.

</details>

3. With 1980 radiography, each extra view had a real time cost. Model the diagnostic phase as
   an optimal-stopping problem: each view reduces the entropy of your belief about the interior
   but increases the probability of a delay-triggered function. What stopping rule would you
   propose, and what quantities would you need to estimate? Which of them were impossible to
   estimate in 1980?

4. The FBI calls the intervention "the best one available at the time", yet it failed. Explain
   the difference between a bad decision and a bad outcome. Design a review process for an
   EOD organisation that assesses the *decision* separately from the result.

<details class="answer"><summary>Answer — then reveal</summary>

A decision is judged by the information, options and reasoning available when it was made. An
outcome also depends on chance and on factors that could not be known. A review process could:
(1) reconstruct what was known at each decision point, using the logs; (2) list the options
that were available and considered; (3) assess whether the reasoning was sound given that
information; (4) ask separately what information *could* have been obtained and at what cost;
(5) record outcome and decision quality on separate axes. Use blind review where possible, and
state explicitly that the reviewer knows the outcome, to reduce hindsight bias.

</details>

5. The perpetrator's note was written to shape the responders' behaviour. How should an
   analyst weight evidence that comes from an adversary with an incentive to deceive? Relate
   your answer to the likelihood ratios in [05.1](lessons/stage-05/lesson-01.md).

6. Which modern technologies (digital radiography, CT, robots with manipulators, simulation)
   would most have changed the 1980 decision problem? Would any of them have changed the
   *outcome*, or only the confidence of the decision?

## Sources

| Title | Organisation / author | Date | URL |
|---|---|---|---|
| Harvey's Casino Bomb | FBI History, Cases and Criminals | accessed 2026 | https://www.fbi.gov/history/cases-and-criminals/harveys-casino-bomb |
| Harvey's Resort Hotel bombing | Wikipedia | accessed 2026 | https://en.wikipedia.org/wiki/Harvey's_Resort_Hotel_bombing |
| Harvey's Casino bombing became a training ground for the FBI | Mystery Wire (news; also syndicated on Nexstar stations) | 2021 | https://www.mysterywire.com/true-crime/harveys-casino-bomb-1980/ |
| Inside the FBI's Hazardous Devices School | FBI | accessed 2026 | https://www.fbi.gov/news/stories/hazardous-devices-school |
| Technology and Explosive Device Analysis Center (TEDAC) | FBI | accessed 2026 | https://www.fbi.gov/investigate/terrorism/tedac |
| A review of X-ray explosives detection techniques for checked baggage | K. Wells, D. A. Bradley, *Applied Radiation and Isotopes* 70(8) | 2012 | https://openresearch.surrey.ac.uk/view/pdfCoverPage?instCode=44SUR_INST&filePid=13140530670002346&download=true |
| A Guide for Explosion and Bombing Scene Investigation (NCJ 181869) | NIJ Technical Working Group | Jun 2000 | https://nij.ojp.gov/library/publications/guide-explosion-and-bombing-scene-investigation |
