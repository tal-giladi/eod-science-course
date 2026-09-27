# Stage 0 gate · Orientation

<div class="module-card">

**Covers** [00.1](lessons/stage-00/lesson-01.md) · [00.2](lessons/stage-00/lesson-02.md) · **Time** ≈ 1.5 h · **Pass** Proficient band on every problem (see [assessment plan](curriculum/assessment-plan.md)): correct answer *and* justification *and* named unknowns.

**Simulator target** Sim A tutorial completed, with the debrief read and your incident schema checked against every piece of information the sim asked you for.

</div>

Work without the lessons open. Write your answer down before revealing.

## Problem 1: classification under incomplete information *(conceptual)*

A fictional survey team in a post-conflict region reports three finds on one day:

- (a) twelve identical, unfired items in rotted crates inside a collapsed farm building that local
  people say was used by a withdrawing army;
- (b) a single small item embedded in a field, in an area where aircraft dropped "containers
  that opened in the air";
- (c) an item from (a) that has been fitted with an attached, non-military assembly and placed
  beside a road.

For each, give the hazard category (IMAS vocabulary), whether it counts as ERW, the responsible
organisation type, and the single most useful piece of missing information.

<details class="answer"><summary>Model answer</summary>

(a) **AXO**: not used, left behind, no longer under the owner's control. It is ERW. A mine-action
operator (EOD L3 team, because of the multiple items, transport and NEQ considerations) under the
national authority. Missing: whether the store was deliberately prepared for use (booby-trapped or
tampered with).
(b) **UXO**, probably a cluster-munition remnant. It is ERW. A mine-action operator, which should
also trigger survey, since strike patterns imply many items. Missing: the extent of the strike
footprint (records, other finds).
(c) **IED**. Improvisation overrides the origin of the component. It is **not** simply ERW any
more. A police bomb squad or military IEDD, depending on the legal context, with forensic
exploitation. Missing: whether the area is still subject to adversary activity (secondary hazards,
intent).
A *Proficient* answer notes that (a) and (c) share a physical object but not a category.

</details>

## Problem 2: why sustainment exists *(mathematical)*

Model a technician's per-task serious-error probability as $p(t) = p_0\,2^{t/T_{1/2}}$, which
doubles every $T_{1/2}$ months without practice, and is reset to $p_0$ by recertification. With
$p_0 = 10^{-5}$, $T_{1/2} = 12$ months and 10 tasks per month spread evenly, compare the expected
number of serious errors over 36 months with (i) no refresher and (ii) a refresher every 12 months.
Use the small-$p$ approximation (expected errors ≈ Σ p).

<details class="answer"><summary>Model answer</summary>

Expected errors ≈ $\int_0^{36} 10\,p_0\,2^{t/12}\,dt = 10p_0\cdot\frac{12}{\ln2}(2^{3}-1) = 10^{-4}\cdot17.31\cdot7 = 1.21\times10^{-2}$.
With yearly resets: $3\cdot10p_0\cdot\frac{12}{\ln 2}(2-1) = 3\cdot10^{-4}\cdot17.31 = 5.19\times10^{-3}$.
The refresher cuts expected errors by a factor of 2.3. The doubling time is invented. The
*structure* (exponential decay, periodic reset) is why HDS recertifies every 3 years and why the
Australian diploma prescribes monthly, quarterly and annual sustainment. A *Proficient* answer
questions the model: decay is likely skill-specific, and rare tasks decay fastest.

</details>

## Problem 3: sizing a squad *(mathematical)*

A fictional regional squad receives 18 calls/day. Each call commits a team for 2.5 h on average.
(a) What is the offered load? (b) Using Erlang-C, what is the smallest number of teams that keeps
$P_{\text{wait}} \le 0.2$? (c) Name two properties of real EOD call data that make this estimate
optimistic.

<details class="answer"><summary>Model answer</summary>

(a) $a = (18/24)\cdot2.5 = 1.875$ Erlang. (b) $c=3$: $P_{\text{wait}} = 0.39$. $c=4$:
$P_{\text{wait}} = 0.14$. So **4 teams**. (c) Heavy-tailed service times (a few very long
incidents) and bursty, non-Poisson arrivals (clusters after publicised incidents, hoax waves). Also
priority pre-emption, and travel times that depend on geography.

</details>

## Problem 4: map an incident to organisations and roles *(design / case)*

A fictional incident: during dredging in a river port, a crane lifts a corroded, bomb-like object.
Minutes later, an anonymous caller claims a device has been left at a nearby ferry terminal. The
country has a police bomb squad, an army EOD unit with an underwater cell, a port authority, and a
national legacy-ordnance database.

Produce: (a) the two incidents' life-cycles (call → isolate → assess → act → clear → report/exploit)
with the lead and supporting organisation at each stage; (b) where the two incidents *interact*
(shared resources, possible link between them); (c) the data records each produces and where they
go; (d) one decision that must be escalated above team level, and why.

<details class="answer"><summary>What a proficient answer contains</summary>

- **Dredged object:** legacy UXO hypothesis. Army EOD (underwater cell for the water-side
  context) leads *assess* and *act*. Police and port authority lead *isolate* (port traffic,
  evacuation). The report goes to the national legacy-ordnance database, and the port's future
  dredging plans should trigger survey.
- **Ferry terminal:** threat call, so a potential IED. Police lead the call, isolation and search,
  and the bomb squad is the technical authority if a suspicious item is found. Forensic exploitation
  follows if a device is confirmed.
- **Interaction:** competition for the same specialists and robots; the *possibility* that the
  call exploits the first incident (diversion, or a secondary hazard near the cordon), which must be
  considered but not assumed; overlapping cordons and evacuation routes. An information system
  needs linked-incident support and shared resource allocation.
- **Records:** two incidents with a link relation; versioned cordons for each; observations with
  uncertainty; decisions with rationale and authority; evidence chain of custody for the terminal
  incident.
- **Escalation:** resource prioritisation between the incidents, and any evacuation of the ferry
  terminal or port. These exceed a single team's authority and belong to the overall incident
  command (00.2 §1).

</details>

## Next

Passed? Continue to [Stage 1 · Physics foundations](lessons/stage-01/README.md).
