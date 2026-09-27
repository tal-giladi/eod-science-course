# Authoring brief (for everyone writing course content)

Read this whole file, then read the **exemplar lesson** `lessons/stage-01/lesson-03.md` and match
its structure, depth and tone. The curriculum is in `curriculum/course-outline.md` (lesson list +
dependency graph) and `curriculum/research-synthesis.md`. Source material with verified URLs is in
`research/01-training-pathways.md`, `research/02-physics-chemistry-blast-sources.md`,
`research/03-detection-forensics-sources.md`, `research/04-robotics-ai-sources.md` — cite from
these (title, author/org, year, URL). Do not invent sources or URLs.

## Audience
A software engineer/CTO with strong programming, mathematics, AI, robotics and systems
background; no EOD experience. **Do not dumb down the mathematics.** Graduate-engineering depth.
Connect to software/AI/robotics analogies where they genuinely help (e.g. safety-and-arming as a
state machine with interlocks).

## SAFETY BOUNDARY — absolute, overrides everything
This is an education and simulation course. NEVER write:
- explosive formulations, compositions, ratios, synthesis, manufacture, sourcing, precursors;
- how to construct, assemble, optimise, conceal or select components for any explosive device or IED;
- how to arm, disarm, defeat, neutralise, render safe, modify or bypass the safety mechanisms of any real device or munition;
- operational render-safe / disposal procedures, tool techniques, or "which wire/component to cut";
- actionable timing, wiring, initiation, triggering, switch or circuit details;
- specific details of real devices from case studies beyond what is needed to state the situation at a high level.
Allowed and encouraged: physics, chemistry *principles* (with non-explosive textbook examples such
as methane or hydrogen combustion, or explicitly fictional "compound X"), effects, protection,
hazard classification, recognition at the *category* level, detection physics, robotics,
decision-making *frameworks*, forensic science *method*, organisations, history, standards.
Operational topics are taught as *concepts and decision frameworks* only. Simulations and
exercises use fictional objects and abstract yield units (YU). When in doubt, be more
conceptual. Each stage README carries a `<div class="callout boundary">` stating what is
deliberately left out and why.

## File locations & ids
- Lesson `NN.M` → `lessons/stage-NN/lesson-0M.md` (e.g. 04.2 → `lessons/stage-04/lesson-02.md`).
- Stage overview → `lessons/stage-NN/README.md` (title, purpose, lessons table with time/level,
  boundary callout, stage-gate link).
- Stage gate → `assessments/stage-NN.md` (4–8 problems mixing types from
  `curriculum/assessment-plan.md`, answers hidden in `<details class="answer">`).
- **Links are root-relative** (docsify): `[04.1](lessons/stage-04/lesson-01.md)`,
  `sims/blast-physics/index.html`, `projects/p01-blast-wave/README.md`. Never `../`.

### Simulator slugs (embed with iframe + link, as in the exemplar)
| Id | Slug | Topic |
|---|---|---|
| A | `sims/scene-assessment/` | scene assessment, cordon, sensors, robot, hazards |
| B | `sims/eod-robot/` | teleoperated robot: drive, pan/tilt, arm, latency, comms loss |
| C | `sims/sensor-fusion/` | multiple noisy sensors, Bayesian fusion |
| D | `sims/blast-physics/` | **exists** — Friedlander, scaled distance, 2D Euler field, SDOF, P–I |
| E | `sims/post-blast/` | post-blast reconstruction |
| F | `sims/incident-command/` | developing incident, information requests, escalation |
| G | `sims/robotics-engineering/` | obstacle course, reach, comms, energy, noisy sensors, user controllers |
| H | `sims/recognition-trainer/` | category-level recognition of synthetic ordnance illustrations |
| I | `sims/shock-tube/` | Rankine–Hugoniot / shock tube / Hugoniot & CJ explorer |
| J | `sims/detection-theory/` | ROC, base rates, costs, operating points |

Embed: `<iframe class="sim-frame" src="sims/<slug>/index.html?embed=1" height="720" loading="lazy"></iframe>`
followed by `<a class="sim-link" href="sims/<slug>/index.html" target="_blank">Open Sim X full-screen ↗</a>`.

### Project slugs (`projects/<slug>/README.md`)
p01-blast-wave · p02-sensor-noise · p03-bayesian-fusion · p04-localization · p05-robot-sim ·
p06-path-planning · p07-slam · p08-manipulator · p09-cv-detection · p10-scene-generator ·
p11-teleoperation · p12-hitl-decision

### Case-study slugs (`case-studies/<slug>.md`)
cs01-wheelbarrow · cs02-harveys-1980 · cs03-oklahoma-city · cs04-kuwait-clearance ·
cs05-laos-cluster-munitions · cs06-counter-ied-robots · cs07-boston-2013 ·
cs08-wwii-legacy-ordnance · cs09-ss-richard-montgomery

## Lesson template (every lesson, in this order)
1. `# NN.M · Title`
2. `<div class="module-card">` with **Prerequisites** (links), **Estimated time** (with split),
   **Level**, **Next**, and `<p class="tags">` tags. (Blank lines inside the div, as exemplar.)
3. `## Why this matters` — the EOD relevance, concretely.
4. `## Learning objectives` — 4–7 measurable objectives.
5. `## Theory` — numbered subsections. **For every important equation:** variable table
   (symbol, meaning, SI unit, dimensions where useful), physical intuition, a small *safe*
   numerical example with checked arithmetic, a Python snippet (numpy) representing it, and an
   exercise with the answer inside `<details class="answer"><summary>Exercise k — then reveal</summary>…</details>`.
   Callouts: `<div class="callout physics|chem|hazard|safety|key|sim|exercise|boundary|eq">` with
   blank lines inside so Markdown renders.
6. `## Visual explanation` — at least one mermaid diagram (```mermaid) or an embedded simulator;
   SVG inline is fine.
7. `## Worked example` — a realistic, fictional, safe scenario worked end to end.
8. `## Simulation work` — which simulator, what to do, what to observe (callout sim).
9. `## Practical exercises` — non-trivial (calculation, interpretation, data analysis, design,
   decision-making). Never "define X". Answers hidden.
10. `## Programming exercise` (where appropriate) — Goal · Input · Output · Constraints ·
    Expected behaviour · Test cases · Extensions; link the related project.
11. `## Reading` — 3–6 items from the research files, with *why* and which part to read.
12. `## Assessment` — 4–6 questions of mixed type (conceptual, mathematical, interpretation,
    design); some answers hidden.
13. `## Expert extension` — optional advanced material (research directions, harder maths).
14. `## What comes next`.

Length: roughly 2,500–4,500 words per lesson. Maths in `$…$` / `$$…$$` (KaTeX). Never put a bare
`$` in prose (write "USD"). **Check every numerical example** (run the arithmetic in Python if you
can: `py -c "..."` works on this machine). Use SI units. Be honest about uncertainty and about
what is empirical vs derived. Distinguish established facts from simplifications.

## Style
Precise, dense, professional; no filler; no emojis; British or American spelling consistently
within a file. Use tables for comparisons. Prefer concrete numbers. Explain *why*.

## Programming projects (projects/pNN-slug/)
```text
projects/pNN-slug/
  README.md            Goal · Background (link lessons) · Requirements · API (signatures) · Input/Output ·
                       Constraints · Expected behaviour · Test cases (what tests check) · Milestones ·
                       Extension challenges · Hints (in <details>) · How to run
  starter/<module>.py  full API with docstrings; bodies raise NotImplementedError (keep small helpers
                       that are not the learning goal implemented)
  solution/<module>.py reference solution (same API)
  tests/test_<module>.py pytest suite
```
- The module name must be unique across the repo (e.g. `blastwave.py`, `sensornoise.py`).
- Tests select the implementation like this (copy exactly):
  ```python
  import os, sys, pathlib
  _ROOT = pathlib.Path(__file__).resolve().parents[1]
  sys.path.insert(0, str(_ROOT / ("solution" if os.environ.get("EOD_SOLUTION") else "starter")))
  import blastwave as mod  # noqa: E402
  ```
- Run from repo root: `python -m pytest projects/pNN-slug` (learner) and
  `EOD_SOLUTION=1 python -m pytest projects/pNN-slug` (must pass — verify it on this machine with
  `set EOD_SOLUTION=1 && py -m pytest projects/pNN-slug` in cmd, or `EOD_SOLUTION=1 py -m pytest ...` in bash).
- Dependencies: numpy, scipy, matplotlib, pytest. OpenCV/PyTorch only in P09 and only in optional
  parts guarded by `pytest.importorskip`. Tests must run in < 30 s total per project, deterministic seeds.
- Tests check behaviour and invariants (conservation, known analytic cases, consistency checks like
  NEES, optimality vs brute force on small cases), not implementation details.
- Fiction/safety rules apply: abstract yields, fictional objects.
