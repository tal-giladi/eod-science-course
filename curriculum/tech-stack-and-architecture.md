# Technology stack & course-website architecture

Deliverables **11** and **12** (`plan.md` §18). Follows the conventions of the learner's other
courses (docsify static sites with KaTeX, `_sidebar.md` navigation, `course.py` CLI tracker,
`TODO_FOR_TAL.md` handoff, GitHub Pages).

## Stack

| Layer | Choice | Why |
|---|---|---|
| Site | **docsify 4** (no build) | identical to sibling courses; Markdown in repo renders directly on GitHub Pages |
| Math | **KaTeX** 0.16 + auto-render, with a math-shielding plugin | fast, works inside HTML callouts |
| Diagrams | **Mermaid 10** (dependency graphs, flows), inline SVG, simulator canvases | versioned as text |
| Search | docsify search plugin | full-text search across lessons |
| Progress | `assets/progress.js` (localStorage; per page status, exercises/sim/code flags, confidence; dashboard; JSON export/import) + `course.py` CLI (durable, git-tracked) | browser convenience + durable record |
| Simulators | plain **HTML5 Canvas 2D** / **Three.js** (CDN, for 3D views) / vanilla JS modules | zero build, runs from file:// and Pages |
| Charts in sims | hand-rolled canvas plotting (tiny, themeable) | no heavy deps |
| Projects | **Python 3.10+**, NumPy, SciPy, matplotlib, pytest; OpenCV & PyTorch (CPU) for P09 only | ubiquitous, testable |
| Optional robotics | ROS 2 / Gazebo pointers in expert extensions (not required) | the core course must run on a laptop |
| QC | `scripts/check_links.py`, `scripts/check_site.py`, pytest | reproducible checks |

## Repository architecture

```text
eod-science-course/
├── index.html                 docsify config (plugins: math shield, KaTeX, mermaid, progress)
├── README.md                  home page: what, who, how to study, safety boundary
├── _sidebar.md                navigation (single source for course.py too)
├── assets/                    course.css, progress.js, shared images/SVG
├── curriculum/                design deliverables (this folder)
├── research/                  research notes with verified sources
├── lessons/stage-NN/          README.md (stage overview) + lesson-MM.md
├── sims/<slug>/index.html     simulators A–J (+ sims/common/ shared JS: rng, plot, ui, debrief)
├── projects/pNN-slug/         README, starter/, tests/, solution/
├── case-studies/              index + one file per case
├── capstones/                 index + one file per capstone
├── assessments/               stage gates
├── references/                glossary.md, bibliography.md, standards.md
├── progress/progress.json     CLI tracker data
├── course.py / PROGRESS.md    CLI tracker + generated progress page
├── progress.md                in-browser dashboard page
└── scripts/                   QC scripts
```

## Page-level conventions
- Lesson ids `NN.M` map to `lessons/stage-NN/lesson-0M.md`.
- Each lesson opens with a `.module-card` (prerequisites, time, level, next) and ends with the
  progress widget (injected automatically).
- Simulators embed as `<iframe class="sim-frame" src="sims/<slug>/index.html?embed=1" height="…">`
  plus an "open full screen" link.
- All sources cited from `curriculum/sources.md` by short key, e.g. `[UFC-3-340-02]`.
