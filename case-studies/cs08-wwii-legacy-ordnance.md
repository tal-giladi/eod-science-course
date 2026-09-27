# CS-8 · WWII legacy aircraft bombs: Frankfurt 2017 and London City Airport 2018

<div class="module-card">

**Read after** [07.2 Incident management](lessons/stage-07/lesson-02.md) · **Also exercises** [02.3 Sensitivity, stability & ageing](lessons/stage-02/lesson-03.md), [03.2 Conventional munitions](lessons/stage-03/lesson-02.md), [03.3 Legacy ordnance](lessons/stage-03/lesson-03.md), [04.4 Injury, fragments & secondary hazards](lessons/stage-04/lesson-04.md), [01.5 Scaling laws](lessons/stage-01/lesson-05.md)

**Estimated time** 1.5 h (reading 40 min · questions 50 min) · **Level** Intermediate

<p class="tags"><span>legacy UXO</span><span>evacuation</span><span>risk communication</span><span>infrastructure</span><span>aerial-photo analysis</span></p>
</div>

<div class="callout boundary">

**Boundary.** Both bombs are described by type and mass only, as in the press. How they work and
how they were made safe or removed is not discussed. The subject is the civil decision problem:
evacuation, disruption and communication.

</div>

## Situation

More than 80 years after the Second World War, aircraft bombs that failed to function are still
found regularly under European cities, rivers and docks. They usually turn up during
construction. German officials find **more than 2,000 tons of unexploded bombs every year**
(PBS NewsHour / AP, 2017). Two well-reported cases show the range of responses.

### Frankfurt am Main, 29 August – 3 September 2017

Construction workers on a site near Goethe University found a British
"blockbuster" air mine of the HC 4000 type. Its mass is reported as **1.4 t** (Smithsonian) or
**1.8 t** (PBS/AP; France 24). The city ordered an evacuation of about **1.5 km radius** (PBS
reports "about a mile") on Sunday 3 September. About **60,000 people** left, the largest
evacuation in post-war Germany. The zone included **two hospitals**, from which premature babies
and intensive-care patients were moved, care homes, the opera and the Bundesbank. More than
1,000 emergency workers took part. Some residents **refused to leave**, which delayed the work.
Officials warned that people could be removed by force. The state ordnance-disposal service
(Kampfmittelräumdienst) made the bomb safe that day (PBS/AP; France 24; Smithsonian).
Koblenz had evacuated about 21,000 people for another bomb the day before (PBS/AP).

### London City Airport, 11–13 February 2018

During pre-planned work at **George V Dock** next to London City Airport, workers found a
**500 kg WWII bomb**, about 1.5 m long, embedded in dense silt on Sunday 11 February. The
Metropolitan Police set a **214 m exclusion zone** that took in several residential streets.
The airport **closed**. All flights on Monday were cancelled, affecting up to **16,000
passengers** on 261 scheduled flights. **Royal Navy** specialists freed the bomb from the silt so
it could be floated, towed it out, and destroyed it in a controlled explosion in the Thames
estuary. The airport reopened on Tuesday (PBS/AP; ABC News Australia; The Points Guy/AP).

## Technology available

| Capability | Role |
|---|---|
| **Historical aerial-photograph analysis** | German state bomb-disposal services examine Allied wartime aerial photographs (NRW alone cites about 330,000 images) to flag suspect areas before construction. On-site geophysical inspection is recommended where contamination is possible (Bezirksregierung Düsseldorf). UK practice is set out in CIRIA C681 (2009), a staged risk-assessment process for construction |
| **Geophysical survey** | Magnetometry and electromagnetic methods to locate large ferrous objects before excavation ([05.2](lessons/stage-05/lesson-02.md)) |
| **Recognition** | Identifying bomb type and origin from visible features ([03.2](lessons/stage-03/lesson-02.md)) |
| **Public alerting** | Police door-to-door checks, sirens, apps, media, social media |
| **Logistics** | Hospital patient transfer, shelters, transport, traffic control |
| **Maritime / diving** (London) | Underwater work, flotation and towing |

## Information available to decision-makers

| Known | Unknown |
|---|---|
| Bomb type and approximate mass (from recognition) | Internal condition after 70+ years ([02.3](lessons/stage-02/lesson-03.md)) |
| Exact location; surrounding buildings and population | Whether the fuzing had been disturbed by the find or by excavation |
| Population at risk, hospitals and critical infrastructure in any candidate radius | How many residents would comply with an evacuation, and how quickly |
| Historical base rate: most such items are made safe without incident | Tail risk: rare events where legacy bombs have functioned during handling |

The essential point is that the **probability of a function is low but not zero, and the
consequence is very large and very local.** This is the classic low-probability,
high-consequence risk profile, and the decision depends heavily on how people perceive it.

## Hazards

- **Blast and fragmentation** from a large charge in an urban setting
  ([04.2](lessons/stage-04/lesson-02.md), [04.4](lessons/stage-04/lesson-04.md)).
- **Ageing effects**: corrosion and degradation of components and explosive fill over decades can
  make an item's condition unpredictable ([02.3](lessons/stage-02/lesson-03.md)).
- **Evacuation hazards**: moving intensive-care patients and premature infants carries clinical
  risk of its own. Traffic and crowding create other risks.
- **Non-compliance**: people who stay inside the zone raise the consequence term and delay the
  work.
- **Economic and infrastructure disruption**: airport closure, business interruption, transport.

## Decisions

### Decision point 1 — how large an exclusion zone?

The radius is chosen from published national safety distances, the item's type and mass, the
planned procedure, the local environment (buildings, water, sediment), and national policy
([07.2](lessons/stage-07/lesson-02.md)). Frankfurt used about 1.5 km. London used 214 m.

A naive physical comparison uses cube-root (Hopkinson–Cranz) scaling, $R \propto W^{1/3}$
([01.5](lessons/stage-01/lesson-05.md)). The mass ratio is $1{,}400/500 = 2.8$ (or 3.6 using the
1.8 t figure). That gives a distance ratio of only $2.8^{1/3}\approx1.41$ (or about 1.53). The
actual ratio of radii was about $1{,}500/214 \approx 7$. **The two zones were not chosen by
scaling one from the other.** They reflect different items, different planned procedures (make
safe in place versus free, float and remove for disposal elsewhere), different environments and
different national practice. The exercise shows that exclusion distances are *policy*
decisions informed by physics, not physics alone.

### Decision point 2 — when and how to evacuate

| Known | Unknown |
|---|---|
| Sunday gives the lowest traffic and business disruption | How long the evacuation will take; compliance |
| Hospitals need a day's notice to move patients | Whether the item's condition allows waiting |

Frankfurt planned a Sunday operation and moved hospital patients the day before (France 24). The
trade-off is between the risk of **waiting** (the item's condition is unknown) and the risk of
**rushing** (incomplete evacuation, clinical risk to patients).

### Decision point 3 — enforce or persuade?

Some Frankfurt residents refused to leave, which delayed the work, and officials warned of
forced removal (PBS/AP). Every non-compliant person inside the zone extends the time everyone
else spends evacuated, and increases the consequence if something goes wrong. That creates a
**public-goods problem**: an individual's decision to stay imposes costs on 60,000 others.

### Decision point 4 — remove or deal with it in place? (London)

The London item was in a dock next to an operating airport. It was freed from the silt,
**floated and towed** to the estuary for controlled destruction (PBS/AP; ABC Australia). The
decision moved the residual hazard away from the population and infrastructure, at the cost of
a longer operation and a closed airport. It is one of the *families of disposal outcome* in
[07.2](lessons/stage-07/lesson-02.md) (remove, destroy in place, render safe), chosen at the
level of risk and infrastructure impact.

## Technology used

- Aerial-photo evaluation and geophysical survey as the pre-construction baseline (Germany; UK
  CIRIA C681 practice).
- Police and municipal alerting, door-to-door clearance of the zone, and verification that the
  zone was empty.
- Specialist state (Germany) or military (UK) ordnance-disposal teams.
- Maritime support for flotation and towing in London.

## Outcome

| | Frankfurt 2017 | London City 2018 |
|---|---|---|
| Item | British HC 4000 air mine, 1.4–1.8 t (reported) | WWII bomb, 500 kg |
| Found | During construction, 29 Aug | During pre-planned dock works, 11 Feb |
| Exclusion zone | ~1.5 km radius (~7 km²) | 214 m radius (~0.14 km²) |
| People displaced / affected | ~60,000 residents; two hospitals | Residents of several streets; up to 16,000 air passengers |
| Duration of disruption | One day of evacuation | Airport closed about two days |
| Result | Made safe in place; no injuries | Removed and destroyed at sea; no injuries |

Frankfurt's zone implies an average density of about $60{,}000/7.07\ \text{km}^2 \approx
8{,}500$ people/km². That shows why an extra 100 m of radius in a dense city can mean thousands
more people displaced.

## Lessons learned

1. **Legacy UXO is a municipal logistics problem.** The technical work may take hours. The
   evacuation (hospitals, care homes, compliance, traffic) is the bulk of the effort and the
   risk.
2. **Pre-construction risk assessment pays.** Aerial-photo analysis and geophysical survey before
   digging cut surprise finds under live sites. That is the upstream control.
3. **Exclusion distances encode policy and procedure, not just mass.** Communicate the *reason*
   for a zone, not just its size.
4. **Compliance is part of the safety system.** Risk communication (clear, early, repeated,
   trusted messengers) is an engineering control as much as any cordon.
5. **Critical infrastructure makes "remove" attractive.** Moving the hazard away can beat dealing
   with it in place when the surroundings are high value, even if the operation takes longer.
6. **Low-probability, high-consequence risks are judged by perception.** A small absolute risk
   still justifies large precautions, because the consequence is catastrophic and the precaution
   is temporary.

## Technological developments that followed

- **Large, systematically used aerial-photo archives** for suspect-area mapping. NRW's
  bomb-disposal service cites about 330,000 Allied images (Bezirksregierung Düsseldorf).
- **Remote sensing and AI** methods developed in mine action for survey (GICHD & ICRC, 2021)
  are natural candidates for archival imagery, for example detecting craters and possible
  entry holes. This is an application of the detection methods in
  [09.1](lessons/stage-09/lesson-01.md), with the domain-shift problems of
  [09.3](lessons/stage-09/lesson-03.md).
- **Geophysics and data fusion** (magnetometry, EM, GPR) for pre-construction survey
  ([05.2](lessons/stage-05/lesson-02.md), [05.6](lessons/stage-05/lesson-06.md)).
- **CIRIA C785** (UK, August 2019), *UXO risk management guide for land-based projects*, which
  updates the C681 approach and covers the life of a site from land transaction to demolition
  (CIRIA).

## Discussion questions

1. Use cube-root scaling to ask what radius would be "equivalent" to London's 214 m for a 1.4 t
   item. Why is that number (about 300 m) so different from Frankfurt's 1.5 km? List at least
   three reasons, none of which are about the bomb's mass.

<details class="answer"><summary>Answer — then reveal</summary>

$214 \times (1{,}400/500)^{1/3} \approx 214 \times 1.41 \approx 302$ m. Reasons for the
difference: (a) different planned procedures (make safe in place versus remove), with different
worst-case scenarios; (b) the environment (London's item was in water and silt at a dock;
Frankfurt's was in open ground among buildings); (c) national practice and published safety
distance tables differ, and these may be based on fragment throw rather than blast; (d)
different bomb designs (an air mine designed for blast versus a general-purpose bomb) with
different hazard profiles; (e) risk tolerance and the population and hospitals inside
candidate radii.

</details>

2. In Frankfurt, suppose each hour of delay costs 60,000 person-hours of displacement. If 50
   non-compliant residents delay the operation by two hours, what is the cost they impose on
   others, per non-compliant person? How would you use this number in public communication, if
   at all?

<details class="answer"><summary>Answer — then reveal</summary>

$2 \times 60{,}000 = 120{,}000$ person-hours, or $120{,}000/50 = 2{,}400$ person-hours
(about 100 person-days) per non-compliant person. In communication it is better used
positively: "leaving on time gets everyone home sooner". Blaming individuals can harden
resistance. Operationally, it justifies investing in door-to-door verification and support
for people who *cannot* leave easily (the elderly, the disabled, pet owners), who are often
confused with people who *will not* leave.

</details>

3. Construct a simple risk comparison for "evacuate hospital patients" versus "keep them in place
   with shielding" for a legacy-bomb operation. Which terms are known, which are estimated, and
   which are really value judgements?

4. Aerial-photo analysis flags suspect areas before construction. Frame it as a detection
   problem: what are the "positives", what are the false positives and false negatives, and how
   would you set the threshold for requiring an on-site geophysical survey?

5. London chose remove-and-destroy-at-sea, which kept the airport closed for about two days.
   Build a simple decision table (options × outcomes × costs) comparing that with a hypothetical
   option that deals with the item in place. What information would you need that is not in the
   public record?

6. Write the three-sentence public message you would send at the start of the Frankfurt
   evacuation. Explain each choice of wording in terms of risk perception.

## Sources

| Title | Organisation / author | Date | URL |
|---|---|---|---|
| WWII bomb defused in Frankfurt after 60,000 evacuate | PBS NewsHour / Associated Press | 3 Sep 2017 | https://www.pbs.org/newshour/world/wwii-bomb-defused-frankfurt-60000-evacuate |
| 'Blockbuster' WWII bomb in Frankfurt forces evacuation of 60,000 | France 24 / AFP | 3 Sep 2017 | https://www.france24.com/en/20170903-blockbuster-wwii-bomb-frankfurt-forces-evacuation-60000 |
| Frankfurt evacuates 60,000 people due to unexploded WWII bomb | Smithsonian Magazine | Sep 2017 | https://www.smithsonianmag.com/smart-news/frankfurt-evacuates-60000-people-due-unexploded-wwii-bomb-180964741/ |
| London City Airport shuts down after discovery of unexploded WWII bomb | PBS NewsHour / Associated Press | 12 Feb 2018 | https://www.pbs.org/newshour/world/london-city-airport-shuts-down-after-discovery-of-unexploded-wwii-bomb |
| WWII bomb removed from London City Airport | ABC News (Australia) | 12 Feb 2018 | https://www.abc.net.au/news/2018-02-12/wwii-bomb-closes-london-city-airport/9424338 |
| London City Airport closed due to WWII bomb | The Points Guy (citing AP) | 12 Feb 2018 | https://thepointsguy.com/news/london-city-airport-closed-ww2-bomb/ |
| Auswertung von Luftbildern (evaluation of wartime aerial photographs) | Bezirksregierung Düsseldorf (NRW state authority) | accessed 2026 | https://www.brd.nrw.de/themen/ordnung-sicherheit/kampfmittelbeseitigung/auswertung-von-luftbildern |
| C681 Unexploded ordnance (UXO): a guide for the construction industry | CIRIA (K. Stone et al.) | Jul 2009 | https://www.ciria.org/CIRIA/CIRIA/Item_Detail.aspx?iProductCode=C681 |
| C785 Unexploded ordnance (UXO) risk management guide for land-based projects | CIRIA | Aug 2019 | https://www.ciria.org/ItemDetail?iProductCode=C785&Category=BOOK&WebsiteKey=3f18c87a-d62b-4eca-8ef4-9b09309c1c91 |
| Webinar Report: The Use of Remote Sensing and Artificial Intelligence in the Mine Action Sector | GICHD and ICRC | Apr 2021 | https://www.gichd.org/fileadmin/uploads/gichd/Publications/ICRC_GICHD_Webinar_Report_-_The_Use_of_Remote_Sensing_and_Artificial_Intelligence_in_the_Mine_Action_Sector.pdf |
