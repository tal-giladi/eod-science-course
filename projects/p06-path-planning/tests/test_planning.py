"""Tests for P06 planning. Run: python -m pytest projects/p06-path-planning  (EOD_SOLUTION=1 for the reference)."""
import os, sys, pathlib
_ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_ROOT / ("solution" if os.environ.get("EOD_SOLUTION") else "starter")))
import planning as mod  # noqa: E402

import math  # noqa: E402

import numpy as np  # noqa: E402
import pytest  # noqa: E402


def _random_costmap(seed, shape=(40, 40), p_lethal=0.2):
    rng = np.random.default_rng(seed)
    cost = rng.random(shape) * 3.0
    cost[rng.random(shape) < p_lethal] = np.inf
    cost[0, 0] = cost[-1, -1] = 0.0
    return cost


def _valid_grid_path(path, cost, start, goal):
    assert tuple(path[0]) == tuple(start) and tuple(path[-1]) == tuple(goal)
    for (r0, c0), (r1, c1) in zip(path[:-1], path[1:]):
        assert max(abs(r1 - r0), abs(c1 - c0)) == 1
    assert all(np.isfinite(cost[tuple(n)]) for n in path)


# ---------------------------------------------------------------- A* / Dijkstra
def test_octile_values():
    assert np.isclose(mod.octile((0, 0), (3, 7), 0.1), 0.1 * (4 + 3 * math.sqrt(2)))   # lesson: 0.824 m
    assert mod.octile((5, 5), (5, 5)) == 0.0


@pytest.mark.parametrize("seed", range(6))
def test_astar_cost_equals_dijkstra_and_expands_fewer(seed):
    cost = _random_costmap(seed)
    a = mod.astar(cost, (0, 0), (39, 39), res=0.5)
    d = mod.dijkstra(cost, (0, 0), (39, 39), res=0.5)
    if not d.path:
        assert not a.path
        return
    assert np.isclose(a.cost, d.cost, rtol=1e-12)
    assert a.expanded <= d.expanded
    _valid_grid_path(a.path, cost, (0, 0), (39, 39))
    assert np.isclose(mod.integrated_cost(a.path, cost, 0.5), a.cost)


@pytest.mark.parametrize("seed", range(3))
def test_octile_admissible_vs_exact_cost_to_go(seed):
    cost = _random_costmap(10 + seed, (30, 30), 0.15)
    goal = (29, 29)
    ctg = mod.cost_to_go(cost, goal, res=0.25)
    for r in range(30):
        for c in range(30):
            if np.isfinite(ctg[r, c]):
                assert mod.octile((r, c), goal, 0.25) <= ctg[r, c] + 1e-12
    d = mod.dijkstra(cost, (0, 0), goal, res=0.25)
    assert np.isclose(ctg[0, 0], d.cost)


def test_astar_open_grid_is_octile_and_unreachable():
    cost = np.zeros((20, 30))
    r = mod.astar(cost, (2, 3), (15, 27), res=0.1)
    assert np.isclose(r.cost, mod.octile((2, 3), (15, 27), 0.1))
    wall = np.zeros((10, 10))
    wall[:, 5] = np.inf
    r = mod.astar(wall, (0, 0), (9, 9))
    assert r.path == [] and math.isinf(r.cost)


def test_weighted_astar_bound():
    cost = _random_costmap(3)
    opt = mod.astar(cost, (0, 0), (39, 39)).cost
    w = mod.astar(cost, (0, 0), (39, 39), weight=2.0)
    assert opt - 1e-9 <= w.cost <= 2.0 * opt


# ---------------------------------------------------------------- risk layer
def test_lesson_risk_scenario():
    """Lesson 06.8 §2-§3: 81x81 grid, 0.25 m cells, hazard at (10, 10) m, standoff 3 m, w=2, sigma=1.5."""
    res, N = 0.25, 81
    cost = mod.risk_layer((N, N), res, [(10.0, 10.0, 0.0)], standoff=3.0, w=2.0, sigma=1.5)
    a = mod.astar(cost, (40, 0), (40, 80), res)
    d = mod.dijkstra(cost, (40, 0), (40, 80), res)
    xy = mod.cells_to_xy(a.path, res)
    assert np.isclose(a.cost, 26.42, atol=0.01) and np.isclose(d.cost, a.cost)
    assert np.isclose(mod.path_length(xy), 25.38, atol=0.01)
    assert np.isclose(mod.closest_approach(xy, (10, 10)), 6.5, atol=0.05)
    assert a.expanded < d.expanded                                # lesson: 2115 vs 6086
    core = mod.risk_layer((N, N), res, [(10.0, 10.0, 0.0)], standoff=3.0, w=0.0)
    xy0 = mod.cells_to_xy(mod.astar(core, (40, 0), (40, 80), res).path, res)
    assert np.isclose(mod.path_length(xy0), 22.49, atol=0.01)     # lethal core only


def test_risk_layer_uncertainty_inflation():
    assert np.isclose(mod.containment_radius(1.0, 0.99), 3.0349, atol=1e-4)
    res, N = 0.1, 101
    cost = mod.risk_layer((N, N), res, [(5.0, 5.0, 0.5)], standoff=1.0, w=2.0, sigma=1.0)
    yy, xx = np.mgrid[0:N, 0:N] * res
    d = np.hypot(xx - 5, yy - 5)
    r_eff = 1.0 + 0.5 * 3.0349
    assert np.all(np.isinf(cost[d < r_eff - 1e-6]))
    assert np.all(np.isfinite(cost[d > r_eff + 1e-6]))
    ring = (d > r_eff) & (d < r_eff + 0.1)
    assert np.all(cost[ring] <= 2.0) and np.all(cost[ring] > 1.9)
    far = d > r_eff + 6
    assert np.all(cost[far] < 1e-6)
    two = mod.risk_layer((N, N), res, [(3.0, 5.0, 0.0), (7.0, 5.0, 0.0)], standoff=0.5, w=1.0, sigma=1.0)
    one = mod.risk_layer((N, N), res, [(3.0, 5.0, 0.0)], standoff=0.5, w=1.0, sigma=1.0)
    fin = np.isfinite(two)
    assert np.all(two[fin] >= one[fin] - 1e-12)                   # contributions add
    # planned path respects the inflated standoff
    r = mod.astar(cost, (50, 0), (50, 100), res)
    assert mod.closest_approach(mod.cells_to_xy(r.path, res), (5.0, 5.0)) >= r_eff


# ---------------------------------------------------------------- sampling-based
OBST = [np.array([[4, 2], [6, 2], [6, 8], [4, 8]], float)]
BOUNDS = (0.0, 0.0, 10.0, 10.0)
OPT = 2 * math.hypot(3, 3) + 2                                   # around the box corners: 10.485


def _path_collision_free(path, obstacles, bounds):
    return all(mod.segment_free(a, b, obstacles, bounds) for a, b in zip(path[:-1], path[1:]))


def test_segment_free_helper():
    assert not mod.segment_free((1, 5), (9, 5), OBST, BOUNDS)
    assert mod.segment_free((1, 9), (9, 9), OBST, BOUNDS)
    assert not mod.segment_free((1, 9), (11, 9), OBST, BOUNDS)


def test_rrt_finds_collision_free_path():
    r = mod.rrt((1, 5), (9, 5), OBST, BOUNDS, np.random.default_rng(0), n_iter=5000, step=0.5)
    assert len(r.path) >= 2
    assert np.allclose(r.path[0], (1, 5)) and np.allclose(r.path[-1], (9, 5))
    assert _path_collision_free(r.path, OBST, BOUNDS)
    assert np.isclose(r.cost, mod.path_length(r.path))
    assert r.cost >= OPT - 1e-9


def test_rrt_star_cost_non_increasing_and_near_optimal():
    r = mod.rrt_star((1, 5), (9, 5), OBST, BOUNDS, np.random.default_rng(0), n_iter=2500, step=1.0,
                     record_every=50)
    costs = [c for _, c in r.cost_history]
    assert all(c1 <= c0 + 1e-9 for c0, c1 in zip(costs[:-1], costs[1:]))
    assert np.isfinite(costs[-1]) and np.isclose(costs[-1], r.cost)
    assert np.allclose(r.path[0], (1, 5)) and np.allclose(r.path[-1], (9, 5))
    assert _path_collision_free(r.path, OBST, BOUNDS)
    assert np.isclose(r.cost, mod.path_length(r.path))           # stored costs stay consistent after rewiring
    assert OPT - 1e-9 <= r.cost <= 1.05 * OPT
    first = next(c for c in costs if np.isfinite(c))
    assert r.cost < first                                        # it actually improved
    # tree invariant: every node's parent precedes it and edges are collision-free
    for i, p in enumerate(r.parents[1:], start=1):
        assert 0 <= p < len(r.nodes) and mod.segment_free(r.nodes[p], r.nodes[i], OBST, BOUNDS)


def test_rrt_star_radius():
    # lesson 06.8 §5: free area 100 m^2, gamma = gamma* -> r_100 = 2.97, r_1000 = 1.15
    assert np.isclose(mod.rrt_star_radius(100, 100.0, 10.0, 1.0), 2.966, atol=1e-3)
    assert np.isclose(mod.rrt_star_radius(1000, 100.0, 10.0, 1.0), 1.149, atol=1e-3)
    assert mod.rrt_star_radius(10, 100.0, 0.5) == 0.5


def test_smooth_path():
    r = mod.rrt((1, 5), (9, 5), OBST, BOUNDS, np.random.default_rng(1), n_iter=5000, step=0.5)
    free = lambda a, b: mod.segment_free(a, b, OBST, BOUNDS)  # noqa: E731
    s = mod.smooth_path(r.path, free)
    assert np.allclose(s[0], r.path[0]) and np.allclose(s[-1], r.path[-1])
    assert mod.path_length(s) <= mod.path_length(r.path) + 1e-12
    assert _path_collision_free(s, OBST, BOUNDS)
    assert len(s) <= 6 and mod.path_length(s) < min(1.15 * OPT, mod.path_length(r.path))
    # smoothing an A* staircase in free space gives the straight line
    a = mod.astar(np.zeros((10, 10)), (0, 0), (9, 5))
    xy = mod.cells_to_xy(a.path, 1.0)
    s2 = mod.smooth_path(xy, lambda p, q: True)
    assert len(s2) == 2 and np.isclose(mod.path_length(s2), math.hypot(5, 9))


# ---------------------------------------------------------------- coverage
def test_boustrophedon_lanes_lesson():
    wps = mod.boustrophedon_lanes(0, 0, 40, 25, 0.8)
    assert len(wps) // 2 == 32                                   # lesson 06.8 §6
    assert np.isclose(mod.path_length(wps), 1304.6, atol=0.1)
    assert np.all(wps[:, 1] <= 25.0)


def test_decomposition_rectangle_with_hole():
    free = np.ones((20, 30), bool)
    free[6:14, 10:20] = False
    labels, adj = mod.boustrophedon_decomposition(free)
    assert np.all((labels >= 0) == free)                         # partition of free space
    assert len(np.unique(labels[free])) == 4                     # left, below, above, right
    assert all(len(adj[k]) == 2 for k in adj)
    # each cell is x-monotone: in every column it occupies one contiguous run
    for k in np.unique(labels[free]):
        for c in range(30):
            rows = np.flatnonzero(labels[:, c] == k)
            if len(rows):
                assert rows[-1] - rows[0] + 1 == len(rows)


@pytest.mark.parametrize("seed", [0, 1, 2])
def test_coverage_visits_all_free_cells(seed):
    rng = np.random.default_rng(seed)
    free = np.ones((25, 40), bool)
    for _ in range(5):                                          # random rectangular obstructions
        r, c = rng.integers(2, 20), rng.integers(2, 35)
        free[r:r + rng.integers(2, 6), c:c + rng.integers(2, 6)] = False
    free[0, 0] = True
    out = mod.coverage_path(free, (0, 0))
    path = out["path"]
    reach = mod.reachable(free, (0, 0))
    visited = np.zeros_like(free)
    for n in path:
        assert free[n]
        visited[n] = True
    assert np.all(visited[reach])                                # every reachable free cell covered
    for (r0, c0), (r1, c1) in zip(path[:-1], path[1:]):
        assert max(abs(r1 - r0), abs(c1 - c0)) == 1               # a drivable 8-connected sequence
    assert len(path) < 1.6 * reach.sum()                          # little overlap


def test_with_robotsim2d_if_available():
    """Optional cross-check: segment_free agrees with P05 World.segment_free on random segments."""
    p05 = _ROOT.parent / "p05-robot-sim" / "solution"
    if not (p05 / "robotsim2d.py").exists():
        pytest.skip("P05 not present")
    sys.path.insert(0, str(p05))
    rs = pytest.importorskip("robotsim2d")
    world = rs.World(10.0, 10.0, OBST + [rs.regular_polygon(8, 8, 1.0, 7)])
    rng = np.random.default_rng(0)
    for _ in range(300):
        a, b = rng.uniform(0, 10, 2), rng.uniform(0, 10, 2)
        assert mod.segment_free(a, b, world.obstacles, BOUNDS) == world.segment_free(a, b)
