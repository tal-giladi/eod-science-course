# Build status & handoff — EOD Science & Technology course

Commit-tracked so a stopped session resumes from here. Update after every batch.

Repo: https://github.com/tal-giladi/eod-science-course · Pages: https://tal-giladi.github.io/eod-science-course/

## Batch plan
1. [x] Scaffold: docsify index, theme, progress plugin, CLAUDE.md, course.py, repo.
2. [x] Research (research/01..04): training pathways; physics/chem/blast; detection & forensics; robotics & AI.
3. [x] Design deliverables (curriculum/): outline, dependency graph, module specs, sources, textbooks,
       papers, official resources, simulation plan, project plan, assessment plan, capstones, stack, architecture.
4. [x] Stages 0–2 lessons (orientation, physics, chemistry).
5. [x] Stages 3–5 lessons (recognition, blast effects, detection).
6. [x] Stages 6–7 lessons (robotics, decision-making).
7. [x] Stages 8–9 lessons (forensics, AI/CV) + case studies.
8. [x] Simulators A–G (sims/).
9. [ ] Programming projects P01–P12 (+ tests, solutions) and capstones.
10. [ ] QC: links, maths, code tests, safety sweep, terminology, glossary, Pages.

## Log
- 2026-09-27 — scaffold created; research agents launched.
- 2026-09-27 — research 01–04 done; outline/sim/project/assessment/stack docs done; Sim D built & tested;
  exemplar lesson 01.3 done; `curriculum/AUTHORING.md` is the brief every content writer follows.
- Content being written in parallel (if a session dies, check which of these files exist and
  write the missing ones following AUTHORING.md): stage-00 (00.1, 00.2, README, gate), 01.1, 01.2,
  01.4–01.7, stage-01 README+gate, stage-02 all, stage-03 all, stage-04 all, 05.1–05.7 + README/gate,
  06.1–06.9 + README/gate, stage-07/08 all, 09.1–09.6 + README/gate, case-studies/cs01–cs09 + index,
  curriculum/sources.md, references/glossary.md, references/standards.md, references/bibliography.md.
- 2026-09-27 — all 10 simulators built & smoke-tested; lessons for stages 0–3, 5–9 done (stage 4 in progress);
  case studies, capstones, references, sidebar/module-spec generator (`scripts/build_nav.py`), link checker
  (`scripts/check_links.py`). In progress: projects P01–P12 (4 writers), stage 4 lessons, alignment of lesson
  "Simulation work" sections with actual sim features. Remaining: batch 9 finish, batch 10 QC (KaTeX render scan,
  internal+external links, pytest EOD_SOLUTION=1 on all projects, safety sweep, qc-report.md), rebuild nav, push.
- Tal asked: after the running agents finish, do not start new agents without asking him first (token budget).
