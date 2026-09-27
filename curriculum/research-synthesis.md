# How the curriculum was derived

`plan.md` §1 requires the curriculum to come from research on how EOD professionals are actually
trained, not from general knowledge. This page is the bridge between the raw research notes in
[`research/`](research/) and the [course outline](curriculum/course-outline.md).

| Research note | Content |
|---|---|
| [01 · Training pathways](research/01-training-pathways.md) | US joint-service school, US Army, FBI Hazardous Devices School & NBSCAB, UK DEMS / ATO, NATO EOD COE & AJP-3.18, IMAS 09.30 + T&EP 09.30/09.31 competency standards, IATG 01.90, police pathways (Canada, Israel, Australia), IABTI, universities (Missouri S&T, New Mexico Tech, Cranfield) |
| [02 · Physics, chemistry & blast sources](research/02-physics-chemistry-blast-sources.md) | textbooks, government design manuals, empirical blast fits, detonation theory |
| [03 · Detection & forensics sources](research/03-detection-forensics-sources.md) | detection technologies, T&E, post-blast investigation, case-study sources |
| [04 · Robotics & AI sources](research/04-robotics-ai-sources.md) | EOD robot history, teleoperation/HRI, free robotics textbooks, mine-action ML, NIST/ASTM response-robot test methods |

## 1. Common knowledge domains → where they live in this course

Every pathway surveyed (military, police, humanitarian, academic) converges on about twelve
domains. The mapping below is the coverage check required by `plan.md` §24.

| # | Domain (from the pathways) | Course coverage | Treatment |
|---|---|---|---|
| 1 | Safety, risk, legal & standards framework | 00.1, 00.2, 04.4, 07.2, references/standards | full |
| 2 | Explosives science (chemistry, classification, sensitivity, ageing) | 02.1–02.3 | science only — no formulations |
| 3 | Physics of effects (blast, fragmentation, thermal, structure response) | 01.1–01.6, 04.1–04.4 | full mathematics |
| 4 | Electricity & electronics fundamentals | 01.7 | physics & sensing; no initiation circuitry |
| 5 | Fuzing & explosive trains (theory) | 03.2 | *systems-engineering / state-machine* view of safety & arming only |
| 6 | Ordnance recognition by family | 03.1–03.3, Sim H | category-level, synthetic illustrations |
| 7 | Improvised devices as a system; C-IED framework | 03.4 | threat categories & indicators; no component-level design |
| 8 | Detection, search & diagnostics | 05.1–05.7, Sim C, Sim J | full physics, T&E, search theory |
| 9 | Tools, equipment, robotics, protection | 06.1–06.9, 04.4 | full engineering depth (the learner's strength) |
| 10 | Disposal methods (conceptual) | 07.2 | outcome *families* and how risk drives the choice; no procedures |
| 11 | Specialist domains (CBRN, underwater, aircraft, HME, bulk) | 03.3, expert extensions | awareness level |
| 12 | Command, reporting, forensics, ammunition management | 00.2, 07.x, 08.x, 04.3 (QD), case studies | full, conceptual for command |

## 2. Levels

The clearest public ladder is **IMAS 09.30 / T&EP 09.30**: EOD Level 1 → 2 → 3 → 3+ specialist
modules, with knowledge items escalating from *awareness* to *understand* to *explain the full
cycle*. The course's Beginner / Intermediate / Advanced / Expert labels mirror that escalation
(see the level table in the [outline](curriculum/course-outline.md)), adapted so that "Expert" means
engineering and research depth (autonomy, trustworthy AI, capstones) rather than operational
authority.

## 3. Academic vs operational

Universities teach explosives chemistry, detonation and shock physics, effects and scaling,
instrumentation, ordnance systems engineering, safety engineering and forensic science openly.
Institutions keep item-specific render-safe procedures, tool techniques, IED countermeasures,
live range work and national SOPs closed. **This course teaches the academic list in full and
the operational list only at the organisational level** — what exists, why, how it is governed
and how decisions are reasoned about.

## 4. Prerequisite structure (from the pathways)

```text
Maths ─┬─> Physics (mechanics, waves) ─> Shock/detonation ─> Blast & fragmentation ─> Protection & standoff
       └─> Chemistry (thermo, kinetics) ─> Explosives science & classification ─┘
Electricity & electronics ─> Initiation/fuzing *concepts* ─> Ordnance families ─> Specialist ordnance
                                                   └─> IED as a system ─> C-IED framework
Safety & risk ─> every practical domain
Ordnance + IED ─> Search / detection / diagnostics ─> Disposal-method concepts
Everything ─> Command, planning, reporting ─> Forensics / post-blast / exploitation
```

The course outline's dependency graph is this structure refined to lesson granularity, plus the
robotics and AI branches (Stages 6 and 9) that the pathways treat only as "tools" but which are
where the learner's background adds the most and where the field is changing fastest.

## 5. What a technician needs conceptually → course "threads"

| Conceptual need (research §8.5) | Thread through the course |
|---|---|
| Energy-release model | 01.2 → 02.1 → 02.2 |
| Effects vs distance & shielding | 01.3–01.5 → 04.x → Sim D |
| How munitions stay safe (safety/arming state machine) | 03.2 (mapped to software interlocks & fail-safes) |
| Recognition & classification | 03.x → Sim H → 09.1 |
| Systems thinking about improvised hazards | 03.4 → 07.1 |
| Risk & decisions under uncertainty | 05.1 → 05.6 → 07.x → Sims A, F → P12 |
| Standards & documentation discipline | 00.2, 05.7, 08.1, references/standards |
| Investigation mindset | 08.x → Sim E → case studies |
