# CS-1 · Wheelbarrow: the origin of the remote-handling robot (Northern Ireland, 1972)

<div class="module-card">

**Read after** [06.1 EOD robot systems](lessons/stage-06/lesson-01.md) · **Also exercises** [00.2 How EOD organisations operate](lessons/stage-00/lesson-02.md), [06.5 Teleoperation & HMI](lessons/stage-06/lesson-05.md), [06.9 Comms & fail-safe design](lessons/stage-06/lesson-09.md), [07.2 Incident management](lessons/stage-07/lesson-02.md)

**Estimated time** 1.5 h (reading 45 min · discussion questions 45 min) · **Level** All

<p class="tags"><span>history</span><span>robotics</span><span>time–distance–shielding</span><span>doctrine</span><span>requirements</span></p>
</div>

<div class="callout boundary">

**Boundary.** This case study is about *why* remote means changed the profession and how that
maps onto engineering requirements. It does not describe any device, tool technique or
render-safe action, and none is needed to follow the argument.

</div>

## Situation

In 1971–72 Northern Ireland saw the most intense improvised-explosive campaign any Western army
had faced in peacetime. Army explosive ordnance disposal (EOD) was the job of Ammunition
Technical Officers and Ammunition Technicians (ATOs/ATs) of the Royal Army Ordnance Corps. The
number of incidents was huge. A 1998 House of Commons debate records **4,295 explosive incidents
handled by EOD teams in 1972 alone**. It also records that **eight operators were killed between
January 1971 and August 1972** while dealing with devices (Hansard, 1998).

The normal procedure at the time required a technician to walk up to a suspect item and work on
it by hand. This was the "long walk", and every incident exposed a highly trained person to the
full hazard. Adversaries soon learned to design against the technician: devices were built to
function when approached or disturbed, and vehicle-borne devices put very large charges into
city streets. Each lost operator was both a death and a loss of scarce, experienced capability
that took years to rebuild.

Lieutenant-Colonel Peter Miller, a retired Royal Tank Regiment officer working as a trials
officer at the Military Vehicles and Engineering Establishment (MVEE), Chertsey, proposed a
remotely controlled vehicle. The first prototype was based on the chassis of a battery-powered
garden wheelbarrow. It entered service in **late August 1972** and was developed rapidly through
many marks over the following years (Wikipedia, *Wheelbarrow (robot)*; Lisle, 2020; Hansard,
1998).

## Technology available

| Capability | State in 1972 | Consequence for the design |
|---|---|---|
| Actuation | Electric motors, lead-acid batteries, mechanical linkages | Slow, heavy, limited endurance; simple enough to repair in theatre |
| Control link | Cable (tether) or radio, both analogue | A tether gives a reliable, jamming-resistant link but limits range and can snag; radio gives freedom but can be degraded |
| Sensing | Analogue closed-circuit TV cameras of low resolution | The operator sees a narrow, low-quality view: situational awareness becomes the bottleneck |
| Manipulation | A simple boom or arm with interchangeable attachments | A modular payload interface, decades before "plug-and-play" standards |
| Mobility | A small ground vehicle (the later marks are tracked) | Terrain, not distance, decides where the robot can go |
| Computing | None on board in the modern sense | All intelligence stays with the operator: pure teleoperation |

For a robotics engineer the striking thing is how little technology it took. Wheelbarrow had no
autonomy, no perception and no computation. What made it valuable was one system property:
**it moved the human out of the hazard radius while keeping a (degraded) ability to observe and
act inside it.**

## Information available to technicians

At a 1972 incident the team usually had:

- a **warning call or a report** from the public or security forces, often incomplete and
  sometimes a deliberate lure;
- the **location and context**: a car parked where it should not be, an unattended bag, a
  building;
- **visual observation from a distance**, with binoculars;
- **pattern knowledge** from previous incidents, which was shared through intelligence and
  technical reporting.

What they did *not* have was a good view of the item itself without going close. Most of the
information needed to decide what to do sat inside the hazard radius. This is the core
structure of the problem: **information has to be bought with exposure.**

## Hazards

- **Primary blast and fragmentation** from the device. Vehicle-borne charges made the
  hazard radius very large (see [04.4](lessons/stage-04/lesson-04.md)).
- **Devices designed to target the responder**, which function on approach, movement or a
  delay.
- **Secondary devices and ambush** aimed at the cordon or at the team.
- **Hoaxes** that use up teams and teach the adversary about response patterns.
- **Organisational hazard.** With so many incidents, time pressure pushed operators to accept
  more exposure per incident.

## Decisions

The decision points below are framed at the level of the incident and of the organisation.

**Decision point 1 — at an incident: approach or wait?**

| Known | Unknown |
|---|---|
| Where the item is, the report, the local context | Whether it is real; whether it is designed to target the approach; any delay |
| The cost of delay (disruption, cordon held, public pressure) | How the device is configured |

Before remote means, the choice was essentially binary. Either a person approached, or the
team waited or accepted the consequences of the device functioning in place. With remote
means a third option appeared: **send a machine to gather information, then decide.** In
decision-theory terms (see [07.1](lessons/stage-07/lesson-01.md)), the robot is an
*information-gathering action with near-zero human exposure*. That changes the value of
information: observations that used to cost a person's exposure now cost a machine's.

**Decision point 2 — for the organisation: invest in an untested machine?**

| Known | Unknown |
|---|---|
| The loss rate among operators | Whether a crude remote vehicle could do useful work |
| That the adversary was adapting to manual procedures | How the adversary would adapt to robots |
| Cost and time to train an ATO | Reliability of the machine in the field |

The organisation chose rapid, iterative development with direct feedback from the operational
unit. The machine was tested on real tasks in Northern Ireland while the designers in England
modified it (Lisle, 2020). This is an early example of what software engineers call a tight
build–measure–learn loop.

**Decision point 3 — what does the robot replace?**

The robot was not meant to replace the technician. It changed *which parts* of the task need a
person to be present. Judgement, diagnosis and choosing among outcomes stayed human. Approach,
observation and remote manipulation moved to the machine.

## Technology used

- A remotely controlled vehicle with a camera and an arm or boom, controlled from outside the
  hazard area.
- A growing library of **attachments** mounted on a standard interface.
- Continuous upgrades through many marks (Wikipedia lists at least Mk 7 and Mk 8 variants,
  and later versions by Northrop Grumman with better sensors and mobility).

## Outcome

- The same Hansard debate records that from **September 1972 to December 1973 three operators
  died**, against eight in the previous twenty months. That was in a period of very high
  incident rates (Hansard, 1998). Other operational changes also happened in this period, so
  the reduction cannot be attributed to the robot alone. It is nevertheless the effect the
  profession itself credits.
- **More than 400 Wheelbarrows were destroyed in service.** The often-quoted estimate is that
  each loss saved at least one life (Wikipedia, *Wheelbarrow (robot)*). The robot became a
  **consumable**, and that is a design goal in its own right.
- The design was widely exported, and "many hundreds" were bought by foreign governments
  (Hansard, 1998).
- Wheelbarrow was withdrawn from British Army service in **2019** and replaced by the
  L3Harris T7 (Wikipedia).

## Lessons learned

### 1. Time–distance–shielding is an exposure integral, and remote means drive the time term to zero

Radiation protection summarises exposure reduction as *time, distance, shielding*, and EOD
doctrine adopted the same idea (see [07.2](lessons/stage-07/lesson-02.md)). A useful
engineering way to write it: if $h(\mathbf{x})$ is the hazard to a person at position
$\mathbf{x}$ should the item function, and $\lambda(t)$ is the rate at which the item might
function at time $t$, then the expected harm to a responder who follows the path
$\mathbf{x}(t)$ is

$$
\mathbb{E}[\text{harm}] \approx \int_0^{T} \lambda(t)\, h\big(\mathbf{x}(t)\big)\, dt .
$$

Distance and shielding reduce $h$. Doing the work quickly reduces $T$. A remote vehicle takes
the human's $\mathbf{x}(t)$ out of the region where $h$ is large *for the whole task*. The
integrand is then carried by a machine whose "harm" is only a cost. Two things follow:

- The value of a robot is greatest where $\lambda$ is high near the item. That is exactly the
  case where devices are designed to target the approach.
- Once the machine takes the exposure, **time is no longer the dominant cost to the human**.
  Doctrine can then trade speed for information: wait, look again, try another approach. This
  is the real doctrinal change. The profession went from "get it done fast because you are
  exposed" to "gather information because the machine is exposed".

### 2. The robot is a consumable, so design for loss

A machine that is expected to be destroyed changes the requirements. It needs low unit cost,
fast repair, spares, simple training and graceful degradation. This is the opposite of how a
high-value asset is designed. The same logic shows up in modern requirements such as the
common robotic system families (see [CS-6](case-studies/cs06-counter-ied-robots.md)).

### 3. Situational awareness becomes the bottleneck

When the operator is no longer beside the object, their understanding of the scene is limited
by what cameras and links deliver. Every later generation of EOD robot added cameras, lights,
better video and better control interfaces. These are exactly the teleoperation
human-factors problems in [06.5](lessons/stage-06/lesson-05.md) (Chen, Haas & Barnes, 2007).

### 4. The adversary adapts

Remote means changed what adversaries did as well. An EOD capability is one side of an
adaptive contest. A robot that follows a predictable routine can be exploited. This lesson
returns at a much larger scale in Iraq and Afghanistan.

### 5. Fast iteration with operators in the loop works

Wheelbarrow was developed with a short loop between users and designers. That loop, not any
single innovation, explains why a garden-wheelbarrow prototype turned into an effective
system within months.

## Technological developments that followed

- **Robot families across the world**: ANDROS (Remotec, from the 1980s), tEODor (Telerob),
  TALON (Foster-Miller, first deployed in Bosnia in 2000) and PackBot (iRobot, Afghanistan
  2002) (Wikipedia, *ANDROS*; Army Technology, *tEODor*; Wikipedia, *Foster-Miller TALON*;
  Yamauchi, 2004).
- **Radio control and video links**, followed by digital video, many cameras and then
  **manipulator arms with several degrees of freedom**. See [06.3](lessons/stage-06/lesson-03.md).
- **Standard test methods** for response robots, which measure mobility, dexterity, sensors,
  communications and operator proficiency (NIST / ASTM E54.09). These are the modern
  equivalent of the field trials that shaped Wheelbarrow.
- **Common interoperability profiles** that separate platforms from payloads, which
  generalise Wheelbarrow's interchangeable attachments (National Defense Magazine, 2018).
- **Human–robot interaction research** on EOD teams, including attachment to robots and trust
  (Carpenter, 2016).

```mermaid
flowchart LR
  A[1971-72: manual approach<br/>'long walk'] -->|8 operators killed<br/>Jan 1971 - Aug 1972| B[Requirement:<br/>remove the human<br/>from the hazard radius]
  B --> C[1972 Wheelbarrow<br/>tethered teleoperation]
  C --> D[Doctrine shift:<br/>machine buys information]
  D --> E[Adversary adapts]
  E --> F[More sensors, radio,<br/>better arms, many marks]
  F --> G[Global robot families<br/>ANDROS, tEODor, TALON, PackBot]
  G --> H[Standards & interoperability<br/>NIST E54.09, UGV IOP]
```

## Discussion questions

1. Using the exposure integral above, explain qualitatively why a robot adds the most value
   against a threat designed to function when approached, and the least value against a
   threat whose functioning is independent of the responder.

<details class="answer"><summary>Answer — then reveal</summary>

If the item may function when approached, then $\lambda(t)$ rises exactly when
$\mathbf{x}(t)$ is close to the item, so the product $\lambda h$ is concentrated in the
approach phase. Removing the human from that phase removes most of the expected harm. If the
item's functioning is independent of the responder (for example a fixed delay), $\lambda$ is
not correlated with position. Exposure is then reduced mainly by staying away and minimising
$T$, and a robot helps chiefly by shortening the human's time near the item. It still helps,
but proportionally less.

</details>

2. The machine was expected to be destroyed. List four requirements that follow from
   "the robot is a consumable". For each, say which way it pushes the design compared with a
   high-value robot such as a planetary rover.

<details class="answer"><summary>Answer — then reveal</summary>

Possible answers: (a) low unit cost, so simpler components rather than best performance;
(b) fast field repair and modular spares, which favours standard interfaces over integrated
optimisation; (c) short operator training, which favours simple and consistent controls over
feature-rich interfaces; (d) graceful degradation and a safe state on link loss, which
favours predictable behaviour over autonomy; (e) enough fleet size that losing a unit does not
stop operations. A rover is the opposite on almost every axis: one unit, very high cost, no
repair, and heavy investment in reliability and autonomy.

</details>

3. A tether gives a secure link but limits range and can snag. Radio gives freedom of movement
   but can be degraded or jammed. Frame this as a trade-off using the reliability and
   link-budget ideas in [06.9](lessons/stage-06/lesson-09.md). When would you still choose a
   tether today?

4. The Hansard figures compare eight deaths in about twenty months with three in about sixteen
   months. What confounders would you need to rule out before attributing the difference to
   the robot? How would you design an analysis if you had incident-level data?

<details class="answer"><summary>Answer — then reveal</summary>

Confounders: changes in incident rate and type; other procedural and doctrinal changes made
at the same time; changes in training and experience; changes in adversary tactics; small
numbers (with counts of 8 and 3, Poisson uncertainty is large). With incident-level data you
would model deaths (or exposure events) per incident with covariates for incident type, period
and whether remote means were used. You would look at within-period variation (incidents with
and without the robot while it was being introduced) and report intervals rather than point
estimates.

</details>

5. Why is situational awareness, rather than mobility or manipulation, the bottleneck of a
   teleoperated system? Link your answer to Endsley's three levels of situation awareness
   ([06.5](lessons/stage-06/lesson-05.md)).

## Sources

| Title | Organisation / author | Date | URL |
|---|---|---|---|
| Lieutenant-Colonel Miller (House of Commons adjournment debate) | UK Parliament, Hansard | 21 Oct 1998 | https://api.parliament.uk/historic-hansard/commons/1998/oct/21/lieutenant-colonel-miller |
| Wheelbarrow (robot) | Wikipedia (cites Parliament, press and Army Technology) | accessed 2026 | https://en.wikipedia.org/wiki/Wheelbarrow_(robot) |
| Making safe: The dirty history of a bomb disposal robot | D. Lisle, *Security Dialogue* (Queen's University Belfast) | 2020 | https://journals.sagepub.com/doi/10.1177/0967010619887849 (author copy: https://pure.qub.ac.uk/files/194511128/Safe.pdf) |
| ANDROS | Wikipedia | accessed 2026 | https://en.wikipedia.org/wiki/ANDROS |
| Foster-Miller TALON | Wikipedia | accessed 2026 | https://en.wikipedia.org/wiki/Foster-Miller_TALON |
| tEODor Explosive Ordnance (EOD) Robot | Army Technology | n.d. | https://www.army-technology.com/projects/teodor-explosive-ordnance-eod-robot/ |
| PackBot: a versatile platform for military robotics | B. M. Yamauchi, Proc. SPIE 5422 | 2004 | https://doi.org/10.1117/12.538328 |
| Human Performance Issues and User Interface Design for Teleoperated Robots | J. Y. C. Chen, E. C. Haas, M. J. Barnes, IEEE Trans. SMC-C 37(6) | 2007 | https://doi.org/10.1109/TSMCC.2007.905819 |
| Army Developing Family of Explosive Ordnance Disposal Robots | National Defense Magazine | 25 May 2018 | https://www.nationaldefensemagazine.org/articles/2018/5/25/army-developing-family-of-explosive-ordnance-disposal-robots |
| Standard Test Methods for Response Robots | NIST Intelligent Systems Division / ASTM E54.09 | ongoing | https://www.nist.gov/el/intelligent-systems-division-73500/standard-test-methods-response-robots |
| Culture and Human-Robot Interaction in Militarized Spaces: A War Story | J. Carpenter, Routledge | 2016 | https://www.routledge.com/Culture-and-Human-Robot-Interaction-in-Militarized-Spaces-A-War-Story/Carpenter/p/book/9781032928456 |
