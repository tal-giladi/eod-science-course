# Assessment plan

Deliverable **9** (`plan.md` §21). Nothing is assessed by recall of definitions. Every
assessment asks the learner to *reason*: compute, interpret, decide, build, or critique.

## Assessment types and where they occur

| Type | Form | Where | Evidence of mastery |
|---|---|---|---|
| Conceptual | "explain why", "predict what happens if", "which assumption fails" | every lesson (Assessment section) | correct causal explanation, names the governing principle |
| Mathematical | derivations & numerical problems with hidden answers | Stages 1, 2, 4, 5, 6 | correct result *and* units/dimension check *and* sanity check |
| Interpretation | read a plot, radiograph-like image, ROC, damage map, sensor log | Stages 4, 5, 8, 9 | draws the supported conclusion and states what the data cannot show |
| Simulation performance | multi-criteria score from Sims A–J debriefs | all stages | ≥ "proficient" band at the stage's target difficulty |
| Programming | pytest suites for P01–P12 + extension challenges | Stages 1, 4–9 | tests pass; learner-written tests for extensions |
| Robotics | Sim G challenges + P04–P08, P11 | Stage 6 | quantitative targets (e.g. NEES consistency, path cost, success rate under latency) |
| Case analysis | structured case write-ups (situation → information → decision → lessons → technology) | Stage 10 | identifies decision points and what information would have changed them |
| System design | design reviews: sensor suite, robot spec, HITL decision system, test plan | end of Stages 5, 6, 9; capstones | requirements traced to physics/uncertainty; failure modes addressed |

## Stage gates

Each stage ends with a **stage assessment** in `assessments/stage-NN.md`: 4–8 problems mixing
the types above, a simulator target, and one design or case question. Target: you can do them
without looking back at the lessons, and you can explain every step.

| Stage | Gate problems | Simulator target | Design/case question |
|---|---|---|---|
| 0 | 4 | Sim A tutorial complete | map a fictional incident to organisations & roles |
| 1 | 8 | Sim I: predict 5 shock states before revealing | choose which approximation applies where |
| 2 | 6 | Sim I CJ mode | explain an ageing-related hazard from first principles |
| 3 | 6 | Sim H ≥ 85 % at Advanced | response-category reasoning for mixed scenes |
| 4 | 8 | Sim D challenge set | protective-design critique of a fictional building |
| 5 | 8 | Sim C ≥ proficient at Advanced; Sim J cost minimum | sensor suite design for a fictional clearance task |
| 6 | 8 | Sim G all challenges at Advanced; Sim B mission | robot specification & failure-mode analysis |
| 7 | 4 | Sim F + Sim A at Expert | decision-log critique |
| 8 | 5 | Sim E reconstruction within tolerance | evidence-handling plan |
| 9 | 6 | P09/P12 metrics | trustworthy-AI deployment review |

## Rubric bands (used by simulators and self-assessment)

| Band | Meaning |
|---|---|
| Novice | correct only with the lesson open; misses unknowns |
| Developing | right answers, weak justification or missing uncertainty |
| Proficient | right answers with justification; identifies main unknowns and limits |
| Expert | also quantifies uncertainty, anticipates failure modes, proposes better experiments |
