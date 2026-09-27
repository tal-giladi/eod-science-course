# P06 · Path planning: A*, risk cost maps, RRT*, coverage (`planning`)

<div class="module-card">

**Lessons** [06.8 Path & motion planning](lessons/stage-06/lesson-08.md) (core) · [06.6 State estimation](lessons/stage-06/lesson-06.md) (position uncertainty) · [06.7 Mapping & SLAM](lessons/stage-06/lesson-07.md) (occupancy grids)

**Level** Advanced · **Estimated time** 12–14 h

**Builds on** [P05 Robot simulator](projects/p05-robot-sim/README.md) (optional cross-check) · [P04 Localisation](projects/p04-localization/README.md) (hazard/pose uncertainty)

<p class="tags"><span>A*</span><span>Dijkstra</span><span>cost maps</span><span>RRT*</span><span>boustrophedon coverage</span><span>smoothing</span></p>
</div>

## Goal

Implement the planners an EOD ground robot actually uses and benchmark them honestly: optimal
grid search with an admissible heuristic, a **standoff risk layer** built from *uncertain*
suspected-hazard locations, asymptotically optimal sampling-based planning in continuous space,
path smoothing, and **coverage planning** for a survey area with obstructions.

The hazards in this project are fictional points on a map with a position uncertainty. The
standoff radius is a **policy input** supplied by the team (06.8 §3, 04.4); the planner never
derives it — it only respects it exactly and prefers extra margin at an explicit exchange rate.

## Background

- Dijkstra/A*, admissibility and consistency, octile heuristic, weighted A*: [06.8](lessons/stage-06/lesson-08.md) §2.
- Layered cost maps, risk as log-survival $-\ln P_s = \int\lambda\,ds$, inflating the lethal core for position uncertainty: [06.8](lessons/stage-06/lesson-08.md) §3 and Exercise 3.
- RRT, RRT*, the $r_n$ neighbourhood radius and $\gamma^\ast$: [06.8](lessons/stage-06/lesson-08.md) §5.
- Boustrophedon cell decomposition and lane spacing $s = W(1-o)$: [06.8](lessons/stage-06/lesson-08.md) §6.
- Where the position uncertainty comes from: [06.6](lessons/stage-06/lesson-06.md); where the grid comes from: [06.7](lessons/stage-06/lesson-07.md).
- Sim G — [Robotics Engineering](sims/robotics-engineering/index.html): obstacle-course and survey
  challenges with in-browser planners (compare expansions for $h = 0$, octile, $2\times$octile).

## Requirements

1. **Grid search.** `astar(cost, start, goal, res, weight)` on 8-connected cost maps; edge cost
   $\text{res}\cdot|\Delta|\cdot(1 + \tfrac12(c_n + c_m))$; lethal = `inf`; octile heuristic;
   `weight = 0` is Dijkstra, `weight > 1` is weighted A*. Return path, cost, nodes expanded.
2. **Exact cost-to-go** by Dijkstra from the goal over the whole map (to verify admissibility).
3. **Risk layer** from hazards $(x, y, \sigma_{\text{pos}})$: lethal radius
   $r_{\text{eff}} = r_s + \sigma_{\text{pos}}\sqrt{-2\ln(1-p)}$ ($p = 0.99$ → $3.03\,\sigma_{\text{pos}}$),
   cost $w\exp(-(d-r_{\text{eff}})^2/2\sigma^2)$ outside it; several hazards add.
4. **RRT** and **RRT\*** in 2D with polygon obstacles; RRT\* chooses the best parent within
   $r_n = \min\{\gamma(\ln n/n)^{1/2}, \eta\}$, rewires, propagates cost changes to descendants,
   and records the best-solution cost history.
5. **Shortcut smoothing** with a user-supplied collision predicate (works for grid and continuous paths).
6. **Coverage**: rectangle lanes (`boustrophedon_lanes`), boustrophedon **cell decomposition** of a
   free-space grid, and a coverage path that visits every reachable free cell as a drivable
   8-connected sequence.

## API

```python
# provided helpers
PlanResult(path, cost, expanded); TreeResult(path, cost, nodes, parents, cost_history)
path_length(points); closest_approach(points, hazard_xy); cells_to_xy(path, res)
integrated_cost(path, cost, res); containment_radius(sigma, p=0.99)
point_in_polygon(p, poly); segment_free(a, b, obstacles, bounds=None); reachable(free, start)
dijkstra(cost, start, goal, res=1.0)            # = astar(..., weight=0)
# to implement
octile(a, b, res=1.0) -> float
astar(cost, start, goal, res=1.0, weight=1.0) -> PlanResult
cost_to_go(cost, goal, res=1.0) -> ndarray
risk_layer(shape, res, hazards, standoff, w=2.0, sigma=1.5, containment=0.99) -> ndarray
rrt(start, goal, obstacles, bounds, rng, n_iter=3000, step=0.5, goal_bias=0.05, goal_tol=0.5) -> TreeResult
rrt_star_radius(n, free_area, eta, gamma_scale=1.1) -> float
rrt_star(start, goal, obstacles, bounds, rng, n_iter=3000, step=1.0, goal_bias=0.05, goal_tol=1.0,
         gamma_scale=1.1, record_every=100) -> TreeResult
smooth_path(path, is_free, max_passes=3) -> ndarray
boustrophedon_lanes(x0, y0, length, width, spacing) -> (2*N, 2) waypoints
boustrophedon_decomposition(free) -> (labels, adjacency)
coverage_path(free, start) -> {"path": [(r, c), ...], "labels", "order"}
```

Grid convention: `cost[row, col]`, cell centre $(x, y) = (\text{col}\cdot\text{res}, \text{row}\cdot\text{res})$.
Continuous convention: obstacles are `(N,2)` polygons inside `bounds = (xmin, ymin, xmax, ymax)`.

## Input / output

- **Input**: cost maps (`float` arrays, `inf` = lethal) or occupancy grids from [P07](projects/p07-slam/README.md);
  hazard list $(x, y, \sigma_{\text{pos}})$ with the team's standoff $r_s$; polygon obstacles and
  bounds; start/goal; a seeded `numpy.random.Generator`; a boolean free-space grid whose cell
  size equals the sensor sweep width for coverage.
- **Output**: paths; cost, length, closest approach to each hazard, integrated cost; nodes
  expanded; RRT\* cost-vs-iterations history; coverage path, cell labels and visiting order.

## Constraints

- Python + NumPy (SciPy optional); deterministic seeds.
- A* on the 81 × 81 lesson map in well under 0.1 s; target A* on 500 × 500 in < 2 s (extension).
- RRT\* 2500 iterations on the test map in a few seconds; whole suite < 30 s.

## Expected behaviour

| Experiment | Expected |
|---|---|
| Lesson map (81 × 81, 0.25 m, hazard at (10, 10) m, $r_s = 3$, $w = 2$, $\sigma = 1.5$) | A*: cost 26.42, length 25.38 m, closest approach 6.5 m, 2115 expansions; Dijkstra same cost, 6086 expansions; weighted A* ($\varepsilon=2$): 907 expansions, cost 32.88; lethal core only: 22.49 m |
| Random cost maps | A* cost = Dijkstra cost; A* expansions ≤ Dijkstra's; octile ≤ exact cost-to-go everywhere |
| Hazard with $\sigma_{\text{pos}} = 0.5$ m, $r_s = 1$ m | lethal radius 2.52 m; the planned path's closest approach ≥ 2.52 m |
| RRT\* around a 2 × 6 m box (optimum 10.49 m) | best cost non-increasing; ≈ 10.6 m after 2500 iterations (within 5 %); RRT's first solution typically 13–17 m |
| 40 × 25 m survey, $s = 0.8$ m | 32 lanes, 1304.6 m of lanes and transits (lesson 06.8 §6) |
| Rectangle with a central obstruction | 4 boustrophedon cells; coverage path visits every free cell with < 60 % revisits |

## Test cases (`tests/test_planning.py`)

| Test | What it checks |
|---|---|
| `test_octile_values`, `test_astar_open_grid_is_octile_and_unreachable` | heuristic numbers; open-grid optimum equals octile; unreachable goal |
| `test_astar_cost_equals_dijkstra_and_expands_fewer` (6 maps) | optimality and ≤ expansions; path validity; reported cost = integrated cost |
| `test_octile_admissible_vs_exact_cost_to_go` (3 maps) | $h(n) \le h^\ast(n)$ for every cell |
| `test_weighted_astar_bound` | $C^\ast \le C_\varepsilon \le \varepsilon C^\ast$ |
| `test_lesson_risk_scenario`, `test_risk_layer_uncertainty_inflation` | lesson 06.8 numbers; inflation by 3.03σ; additivity; path respects $r_{\text{eff}}$ |
| `test_rrt_finds_collision_free_path`, `test_rrt_star_cost_non_increasing_and_near_optimal`, `test_rrt_star_radius` | collision-free paths, monotone cost history, ≤ 5 % from optimum, tree invariants, $r_n$ values |
| `test_smooth_path` | endpoints kept, never longer, collision-free; staircase → straight line |
| `test_boustrophedon_lanes_lesson`, `test_decomposition_rectangle_with_hole`, `test_coverage_visits_all_free_cells` (3 maps) | 32 lanes; partition into x-monotone cells; full coverage with a drivable path |
| `test_with_robotsim2d_if_available` | optional: `segment_free` agrees with P05 `World.segment_free` |

## Milestones

1. `octile`, `astar` (Dijkstra comes free), `cost_to_go`; reproduce the lesson's expansion counts.
2. `risk_layer`; plot paths for $w \in \{0, 2, 10\}$ and $\sigma_{\text{pos}} \in \{0, 0.5, 1\}$ m and tabulate length vs closest approach.
3. `rrt`, then `rrt_star` with rewiring and cost propagation; plot cost vs iterations for 5 seeds.
4. `smooth_path`; apply it to both A* and RRT paths.
5. `boustrophedon_lanes`, `boustrophedon_decomposition`, `coverage_path`; plot the cells and the path.
   `python solution/planning.py` draws the target figure.

## Extension challenges

1. D\* Lite (or incremental A\*) and measure replanning work after a local map change near the robot vs near the goal.
2. Hybrid-A\* with heading for the rectangular footprint; compare with A\* + smoothing on a doorway.
3. Chance-constrained A\*: inflate the lethal core along the path by the robot's pose covariance from [P04](projects/p04-localization/README.md).
4. Multi-objective planning (length, integrated risk, time outside radio coverage from 06.9) and a Pareto front.
5. Coverage with a gap model: lanes spaced by $s = W(1-o)$ with Gaussian cross-track error; choose $o$ for a 2.5 % gap probability (06.8 §6 exercise) and verify by Monte Carlo on the P05 simulator.
6. A* on a 500 × 500 map in < 2 s: array-based open list, precomputed neighbour offsets, or a C-accelerated heap.

## Hints

<details><summary>Hint 1 — A* bookkeeping</summary>

Use a lazy-deletion heap (push duplicates, skip nodes already closed) and a counter as a
tie-breaker so tuples never compare cells. Count a node as expanded when it is closed; stop when
the goal is *popped*, not when it is first generated — otherwise the result is not optimal.

</details>

<details><summary>Hint 2 — why A* expands no more than Dijkstra</summary>

With a consistent heuristic A* expands only nodes with $f(n) = g^\ast(n) + h(n) \le C^\ast$;
Dijkstra expands every node with $g^\ast(n) \le C^\ast$. Since $h \ge 0$, the first set is a
subset of the second (up to ties at exactly $C^\ast$).

</details>

<details><summary>Hint 3 — RRT* rewiring and cost propagation</summary>

When a neighbour $j$ is rewired through the new node, its cost drops by $\delta$ and so does every
node in its subtree. Keep a children list per node and push the change down the subtree;
otherwise stored costs go stale and later parent choices are wrong. Keep the best-solution cost
as a minimum over goal-connectable nodes — then it can only decrease.

</details>

<details><summary>Hint 4 — boustrophedon events</summary>

Sweep columns left to right and list each column's free runs. A run continues the previous cell
only when it overlaps exactly one previous run *and* that run overlaps exactly one current run.
Any split (IN event) or merge (OUT event) closes the affected cells and opens new ones. Inside a
cell, sweep column by column alternating direction; connect cells (and any non-adjacent
consecutive waypoints) with a shortest free path.

</details>

## How to run

```bash
python -m pytest projects/p06-path-planning                     # your starter
EOD_SOLUTION=1 python -m pytest projects/p06-path-planning      # reference solution (bash)
python projects/p06-path-planning/solution/planning.py          # benchmark figure
```

On Windows `cmd`: `set EOD_SOLUTION=1 && py -m pytest projects/p06-path-planning`.

The module is self-contained: it carries its own copies of the polygon collision helpers, so the
starter works without P05. The one P05 cross-check test adds `projects/p05-robot-sim/solution` to
`sys.path` and is skipped if P05 is absent (see the P05 README, "Using robotsim2d from other projects").
