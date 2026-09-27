# Quality-control report

`plan.md` §24 checklist, with how each item was checked and the result (September 2026).

| Requirement | How it was checked | Result |
|---|---|---|
| External links verified | `python scripts/check_links.py --external` over every URL in the course | 228 URLs: 193 OK, 35 refuse automated access (government/publisher bot protection — see [link-report.md](curriculum/link-report.md); these were confirmed by search during research), 0 broken after re-check |
| Internal links | `python scripts/check_links.py` | 0 broken |
| Obsolete material replaced | research notes flag superseded items (e.g. IMAS 09.20 withdrawn → IMAS 07.40; IATG 02.10 vs 02.20; current DESR 6055.09 change; UFC 3-340-02 with Change 2) | applied in [sources.md](curriculum/sources.md) and [standards.md](references/standards.md) |
| Every major EOD knowledge domain covered | mapping of the 12 domains common to all training pathways → lessons | complete — see [research-synthesis.md](curriculum/research-synthesis.md) §1 |
| Prerequisite ordering | dependency graph in the [outline](curriculum/course-outline.md); every lesson card lists prerequisites; stage gates only use earlier material | consistent |
| Exercises test the preceding material | every lesson has hidden-answer exercises tied to its equations; stage gates in `assessments/` | 47 lessons, 10 stage gates |
| Simulations teach the underlying concepts | each simulator's debrief states observed / decided / missed / uncertainty / professional reasoning / physics / engineering and links back; lesson "Simulation work" sections audited against actual simulator features | aligned |
| Mathematical correctness | every numerical example re-run in Python by its author; blast formulas cross-checked against `sims/common/blast.js` and P01 (e.g. Sod p* = 0.30313, u* = 0.92745; CJ closed form vs numeric tangency); all 10 740 math segments parsed by KaTeX (`node scripts/check_math.js`) | 0 KaTeX errors |
| Code examples | lesson snippets executed by authors; projects: `EOD_SOLUTION=1 python -m pytest projects` | 224 tests pass (all 12 projects); starters fail with `NotImplementedError` only |
| No actionable construction/disarmament content | term sweep across lessons, case studies, assessments, capstones for compositions, named-explosive recipes, initiation/switching/timing terms, render-safe/tool techniques; manual review of the sensitive stages (2, 3, 7) and the Harvey's case | only conceptual, protective and organisational mentions remain; every stage README carries a boundary statement |
| Terminology consistent | glossary aligned to IMAS 04.10 / NATO AJP-3.18; lesson terms cross-linked | 250+ glossary terms |
| Difficulty increases progressively | Beginner → Expert mapping in the outline; simulators have four levels | consistent |
| Useful to a software/AI/robotics engineer | Stages 5, 6, 9 are the deepest (22 lessons); 12 test-driven projects; JS-programmable Sim G; capstone C1 integrates P03–P12 | yes |

## Known limitations

- Several government sources (navy.mil, fbi.gov, atf.gov, army.mod.uk, DTIC) block automated fetching; open them in a browser.
- The Kingery–Bulmash report is distribution-limited; the course uses the public Kinney–Graham fits and UFC 3-340-02 / IATG 01.80 summaries.
- The SS Richard Montgomery case study describes mast-removal work under way in September 2026; its outcome should be updated later.
- Some lessons exceed the 4,500-word guideline (code and tables included).
