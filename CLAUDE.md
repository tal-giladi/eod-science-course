# Build guide — EOD Science & Technology course

A **docsify static course site** (no build step) plus **browser simulators** (`sims/`, plain
HTML/JS/Canvas/WebGL, no bundler) and **Python programming projects** (`projects/`, NumPy/SciPy,
pytest). Audience: Tal — software engineer/CTO, strong in programming, maths, AI, robotics,
systems; no EOD experience, cannot do live explosives training. Source brief: `plan.md`.

Published at https://tal-giladi.github.io/eod-science-course/ from
https://github.com/tal-giladi/eod-science-course.

## Layout
- `index.html` — docsify config (KaTeX, mermaid, search, copy-code, progress plugin).
- `assets/course.css`, `assets/progress.js` — theme + in-browser progress tracking (localStorage).
- `README.md` (home), `_sidebar.md` (navigation — every page MUST be linked here).
- `curriculum/` — the design deliverables (outline, dependency graph, module specs, sources,
  simulation plan, project plan, assessment plan, capstones, tech stack, architecture).
- `research/` — raw research notes that the curriculum is derived from (sources verified).
- `lessons/stage-NN/lesson-MM.md` — lessons. Id `NN.M` (e.g. `04.2`).
- `sims/<slug>/index.html` — self-contained simulators, embedded in lessons with an iframe.
- `projects/pNN-slug/` — README spec + starter code with `NotImplementedError` stubs + tests.
  Reference solutions live in `projects/pNN-slug/solution/` (read only after attempting).
- `case-studies/`, `capstones/`, `assessments/`, `references/` (glossary, bibliography).
- `course.py` + `progress/progress.json` → `PROGRESS.md` (CLI tracker, reads `_sidebar.md`).

## Lesson template (plan.md §20)
Header card (`.module-card`): prerequisites · estimated time · difficulty · what comes next.
Then: Why this matters → Learning objectives → Theory (with maths) → Visual explanation
(mermaid/SVG/sim) → Worked examples → Simulation → Practical exercises → Programming exercise
(where appropriate) → Reading (from `curriculum/sources.md`) → Assessment → Expert extension →
What comes next.

**Every important equation** (plan.md §1): variables · units/dimensions · physical intuition ·
small safe numerical example · Python representation · an exercise whose answer is hidden in
`<details class="answer">`.

Callouts: `.callout.physics|chem|hazard|safety|key|sim|exercise|boundary|eq`.

## SAFETY BOUNDARY — non-negotiable (plan.md §2)
Education & simulation only. NEVER write: explosive formulations, synthesis, manufacture,
component selection, device construction/optimization, arming, actionable timing/wiring/
initiation/triggering details. Chemistry uses general principles and textbook non-explosive
examples (e.g. methane combustion) or explicitly *fictional* materials. Blast simulators use
abstract "yield units", never "how much X to achieve Y". Decision sims score information
gathering, safety and uncertainty — never "which wire to cut". Case studies: situation, context,
technology, decisions, lessons — no device details. When in doubt, go more conceptual. Every
stage README carries a `.callout.boundary` stating what is deliberately left out and why.

you can teach helpful methods to disarm ied, and how to know when it's too risky to disarm even if it means people might touch it.

## Conventions
- Maths `$...$`/`$$...$$` (KaTeX). No bare `$` in prose outside maths.
- Python ≥3.10, numpy/scipy/matplotlib; PyTorch only where genuinely needed (flag it).
- Sims: no external deps except CDN libs from cdn.jsdelivr.net; must work opened via file:// or
  the docsify site; every sim ends with a debrief (observed / decided / missed / uncertainty /
  professional reasoning / physics / engineering / link back to lessons) and supports difficulty
  Beginner / Intermediate / Advanced / Expert. Never reveal solution before the decision.

## Local preview
`python -m http.server 8080` → http://localhost:8080. Tests: `python -m pytest projects`.

## Status / handoff
`TODO_FOR_TAL.md` tracks build progress. Commit and push after each small batch.
