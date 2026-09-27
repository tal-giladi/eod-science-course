# How to study this course

## The loop for every lesson

1. Read **Why this matters** and the **objectives**; skim the theory headings.
2. Work the theory **with a notebook open**: re-derive the key equation, run the Python snippet,
   then do the hidden-answer exercise *before* revealing it.
3. Do the **simulation work** at your current difficulty; read the whole debrief, especially
   *what you missed* and *what uncertainty existed*.
4. Do the **practical exercises** and (where present) the **programming exercise** or project milestone.
5. Answer the **assessment** questions without looking back. If you can't explain an answer, log it:
   `python course.py struggle 04.2 "why does reflection exceed 2x?"`
6. Mark the page complete (bottom-of-page widget) and `python course.py complete 04.2`.

## Suggested pacing (part-time, ~8 h/week)

| Months | Stages | Milestones |
|---|---|---|
| 1 | 0, 1 | Sim D and Sim I challenges at Intermediate; P01 |
| 2 | 2, 3 | Sim H ≥ 85 % at Advanced; stage gates 2–3 |
| 3 | 4 | Sim D challenge at Advanced; P01 extensions |
| 4–5 | 5 | Sims C and J at Advanced; P02, P03 |
| 6–8 | 6 | Sims B and G at Advanced; P04–P08, P11 |
| 9 | 7, 8 | Sims A, F, E at Advanced; case studies |
| 10–11 | 9 | P09, P10, P12 |
| 12+ | Capstone | C1 (and optionally C2–C4) |

## Fast-track for a software/AI/robotics engineer

You may **test out** of 06.2, 06.3, 06.6 and 09.1 by passing their assessments and the matching
project tests (P08, P04, P09) without reading the lesson — but do not skip 06.1, 06.5, 06.9,
05.1, 07.x: they contain the EOD-specific constraints that your background does not supply.

## Tools

- Site: `python -m http.server 8080` in the repo root → http://localhost:8080 (or the GitHub Pages site).
- Python ≥ 3.10 with `numpy scipy matplotlib pytest` (+ `opencv-python torch` for P09).
- Projects: `python -m pytest projects/p01-blast-wave` — tests fail until you implement the starter.
