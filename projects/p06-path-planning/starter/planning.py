"""planning — grid and sampling-based path planning with risk layers and coverage (Project P06,
starter).

Grid conventions: a cost map is a 2D float array ``cost[row, col]``; cell (r, c) has centre
(x, y) = (c * res, r * res) metres. ``cost`` is the *extra* cost per metre on top of length
(>= 0), ``np.inf`` = lethal (never entered). An 8-connected move from n to m costs
    res * |step| * (1 + (cost[n] + cost[m]) / 2),   |step| in {1, sqrt(2)}
(as in lesson 06.8 §2), so every edge costs at least its length and the octile distance is an
admissible, consistent heuristic.

Continuous conventions: obstacles are a list of polygons ((N, 2) vertex arrays) inside
axis-aligned ``bounds = (xmin, ymin, xmax, ymax)``.

The module is self-contained (NumPy/SciPy); the polygon collision helpers duplicate the ones in
P05 ``robotsim2d`` so that this project does not depend on it.
"""
from __future__ import annotations

import heapq
import math
from dataclasses import dataclass, field

import numpy as np

__all__ = [
    "SQRT2", "PlanResult", "octile", "astar", "dijkstra", "cost_to_go", "path_length",
    "risk_layer", "containment_radius", "closest_approach", "integrated_cost",
    "point_in_polygon", "segment_free", "TreeResult", "rrt", "rrt_star", "smooth_path",
    "boustrophedon_lanes", "boustrophedon_decomposition", "coverage_path", "reachable", "cells_to_xy",
]

SQRT2 = math.sqrt(2.0)
_MOVES = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


# ----------------------------------------------------------------------------------------------
# Helpers (provided in the starter)
# ----------------------------------------------------------------------------------------------
@dataclass
class PlanResult:
    """Grid search result: path as a list of (row, col) cells (empty if no path), its cost,
    and the number of nodes expanded (closed)."""
    path: list
    cost: float
    expanded: int


def path_length(points) -> float:
    """Polyline length of an (N, 2) array (or list of points)."""
    p = np.asarray(points, dtype=float)
    return float(np.sum(np.hypot(*np.diff(p, axis=0).T))) if len(p) > 1 else 0.0


def closest_approach(points, hazard_xy) -> float:
    """Minimum distance from the polyline vertices to a hazard position."""
    p = np.asarray(points, dtype=float)
    return float(np.min(np.hypot(p[:, 0] - hazard_xy[0], p[:, 1] - hazard_xy[1])))


def cells_to_xy(path, res: float) -> np.ndarray:
    """(row, col) cells -> (x, y) metres."""
    return np.array([(c * res, r * res) for r, c in path], dtype=float).reshape(-1, 2)


def point_in_polygon(p, poly) -> bool:
    """Even–odd crossing test (copy of the P05 helper)."""
    x, y = float(p[0]), float(p[1])
    poly = np.asarray(poly, dtype=float)
    xi, yi = poly[:, 0], poly[:, 1]
    xj, yj = np.roll(xi, 1), np.roll(yi, 1)
    straddle = (yi > y) != (yj > y)
    with np.errstate(divide="ignore", invalid="ignore"):
        x_cross = xj + (y - yj) * (xi - xj) / (yi - yj)
    return bool(np.count_nonzero(straddle & (x < x_cross)) % 2)


def _segments_cross_any(a, b, P, Q) -> bool:
    """Does segment ab intersect any edge P[i]->Q[i]? Touching and collinear overlap count."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    eps = 1e-12

    def orient(o, u, w):
        return (u[..., 0] - o[..., 0]) * (w[..., 1] - o[..., 1]) - (u[..., 1] - o[..., 1]) * (w[..., 0] - o[..., 0])

    def on_seg(p0, p1, r):   # r (collinear) within the bounding box of p0p1
        return ((np.minimum(p0[..., 0], p1[..., 0]) - eps <= r[..., 0]) & (r[..., 0] <= np.maximum(p0[..., 0], p1[..., 0]) + eps) &
                (np.minimum(p0[..., 1], p1[..., 1]) - eps <= r[..., 1]) & (r[..., 1] <= np.maximum(p0[..., 1], p1[..., 1]) + eps))

    o1, o2 = orient(a, b, P), orient(a, b, Q)
    o3, o4 = orient(P, Q, a), orient(P, Q, b)
    proper = (o1 * o2 < 0) & (o3 * o4 < 0)
    touch = ((np.abs(o1) <= eps) & on_seg(a, b, P)) | ((np.abs(o2) <= eps) & on_seg(a, b, Q)) |             ((np.abs(o3) <= eps) & on_seg(P, Q, a)) | ((np.abs(o4) <= eps) & on_seg(P, Q, b))
    return bool(np.any(proper | touch))


def segment_free(a, b, obstacles, bounds=None) -> bool:
    """True if segment ab lies within ``bounds`` and neither crosses nor enters any polygon."""
    if bounds is not None:
        for q in (a, b):
            if not (bounds[0] <= q[0] <= bounds[2] and bounds[1] <= q[1] <= bounds[3]):
                return False
    for P in obstacles:
        P = np.asarray(P, dtype=float)
        if point_in_polygon(a, P) or point_in_polygon(b, P):
            return False
        if _segments_cross_any(a, b, P, np.roll(P, -1, axis=0)):
            return False
    return True


def containment_radius(sigma: float, p: float = 0.99) -> float:
    """Radius containing probability p of an isotropic 2D Gaussian: sigma * sqrt(-2 ln(1 - p))."""
    return sigma * math.sqrt(-2.0 * math.log(1.0 - p))


# ----------------------------------------------------------------------------------------------
# Grid search (learning goals)
# ----------------------------------------------------------------------------------------------
def octile(a, b, res: float = 1.0) -> float:
    """Octile distance between cells a=(r, c) and b: res * (max(dr, dc) + (sqrt2 - 1) min(dr, dc))."""
    raise NotImplementedError("TODO: implement octile")


def _edge_cost(cost, n, m, res, diag):
    return res * (SQRT2 if diag else 1.0) * (1.0 + 0.5 * (cost[n] + cost[m]))


def astar(cost, start, goal, res: float = 1.0, weight: float = 1.0) -> PlanResult:
    """8-connected A* with f = g + weight * octile(n, goal).

    weight = 0 gives Dijkstra; weight = 1 is optimal (octile is admissible and consistent);
    weight > 1 is weighted A* (cost <= weight * optimum). Stops when the goal is popped; the goal
    itself is not counted as expanded. Lethal (inf) cells, including start/goal, are never entered.
    Returns PlanResult([], inf, expanded) if the goal is unreachable.
    """
    raise NotImplementedError("TODO: implement astar")


def dijkstra(cost, start, goal, res: float = 1.0) -> PlanResult:
    """Uniform-cost search baseline (A* with a zero heuristic)."""
    return astar(cost, start, goal, res, weight=0.0)


def cost_to_go(cost, goal, res: float = 1.0) -> np.ndarray:
    """Exact optimal cost from every cell to ``goal`` (Dijkstra from the goal over the whole map;
    edge costs are symmetric). Unreachable or lethal cells get inf."""
    raise NotImplementedError("TODO: implement cost_to_go")


def integrated_cost(path, cost, res: float = 1.0) -> float:
    """Cost of a cell path under the edge model (equals PlanResult.cost for a planner's path)."""
    total = 0.0
    for n, m in zip(path[:-1], path[1:]):
        total += _edge_cost(cost, tuple(n), tuple(m), res, n[0] != m[0] and n[1] != m[1])
    return total


# ----------------------------------------------------------------------------------------------
# Risk layer (learning goal)
# ----------------------------------------------------------------------------------------------
def risk_layer(shape, res: float, hazards, standoff: float, w: float = 2.0, sigma: float = 1.5,
               containment: float = 0.99) -> np.ndarray:
    """Standoff cost map from uncertain hazard locations (lesson 06.8 §3).

    hazards: iterable of (x, y, sigma_pos) — estimated position (m) and isotropic 1-sigma
    position uncertainty (m). Each hazard's lethal radius is inflated to
        r_eff = standoff + containment_radius(sigma_pos, containment)
    (the 99 % containment radius is 3.03 sigma_pos). Cells with d < r_eff are inf; beyond it the
    cost is w * exp(-(d - r_eff)^2 / (2 sigma^2)). Contributions of several hazards add (hazard
    rates per metre add along a path). ``standoff`` is a policy input from the team.
    """
    raise NotImplementedError("TODO: implement risk_layer")


# ----------------------------------------------------------------------------------------------
# Sampling-based planning (learning goals)
# ----------------------------------------------------------------------------------------------
@dataclass
class TreeResult:
    """Tree planner result. path: (K, 2) array start→goal (empty (0, 2) if not found);
    cost_history: list of (iteration, best cost so far) recorded every ``record_every`` iterations."""
    path: np.ndarray
    cost: float
    nodes: np.ndarray
    parents: np.ndarray
    cost_history: list = field(default_factory=list)


def _extract(nodes, parents, idx):
    out = []
    while idx >= 0:
        out.append(nodes[idx])
        idx = parents[idx]
    return np.array(out[::-1])


def _steer(a, b, step):
    d = b - a
    L = float(np.hypot(*d))
    return b.copy() if L <= step else a + d * (step / L)


def rrt(start, goal, obstacles, bounds, rng, n_iter: int = 3000, step: float = 0.5,
        goal_bias: float = 0.05, goal_tol: float = 0.5) -> TreeResult:
    """Basic RRT: sample (goal with probability goal_bias), extend the nearest node by at most
    ``step`` if the segment is free, stop when a node within goal_tol connects freely to the goal."""
    raise NotImplementedError("TODO: implement rrt")


def rrt_star_radius(n: int, free_area: float, eta: float, gamma_scale: float = 1.1) -> float:
    """r_n = min(gamma (ln n / n)^(1/2), eta) with gamma = gamma_scale * gamma*, d = 2."""
    raise NotImplementedError("TODO: implement rrt_star_radius")


def rrt_star(start, goal, obstacles, bounds, rng, n_iter: int = 3000, step: float = 1.0,
             goal_bias: float = 0.05, goal_tol: float = 1.0, gamma_scale: float = 1.1,
             record_every: int = 100) -> TreeResult:
    """RRT* (Karaman & Frazzoli 2011) in 2D.

    For each sample: steer from the nearest node by at most ``step``; among nodes within
    r_n = rrt_star_radius(n, free_area, step) choose the parent minimising cost-to-come with a
    free segment; then rewire neighbours through the new node when that lowers their cost
    (propagating the cost change to their descendants). The best solution is
    min over nodes within goal_tol with a free segment to the goal of cost(node) + |node - goal|;
    it is non-increasing in the iteration count. Free area is estimated as the bounds area minus
    polygon areas.
    """
    raise NotImplementedError("TODO: implement rrt_star")


def smooth_path(path, is_free, max_passes: int = 3) -> np.ndarray:
    """Greedy shortcut smoothing: from each kept vertex jump to the farthest later vertex reachable
    by a free straight segment (``is_free(a, b) -> bool``). Endpoints are kept; the result is never
    longer than the input and every segment is free if the input's were."""
    raise NotImplementedError("TODO: implement smooth_path")


# ----------------------------------------------------------------------------------------------
# Coverage planning (learning goals)
# ----------------------------------------------------------------------------------------------
def boustrophedon_lanes(x0: float, y0: float, length: float, width: float, spacing: float) -> np.ndarray:
    """Lawn-mower waypoints for an obstacle-free rectangle: lanes along x, spaced ``spacing`` in y,
    first lane at y0 + spacing/2, last lane clipped to the far boundary. Returns (2*N_lanes, 2);
    N_lanes = ceil(width / spacing)."""
    raise NotImplementedError("TODO: implement boustrophedon_lanes")


def _runs(col):
    """Free runs (r0, r1) inclusive in a boolean column."""
    out, r, R = [], 0, len(col)
    while r < R:
        if col[r]:
            s = r
            while r + 1 < R and col[r + 1]:
                r += 1
            out.append((s, r))
        r += 1
    return out


def boustrophedon_decomposition(free) -> tuple:
    """Boustrophedon cell decomposition of a boolean free-space grid, sweeping a vertical line
    left→right over columns.

    Each column's free runs are intervals. A run continues the cell of the previous column's run
    iff they overlap and each overlaps no other run (no split/merge event); otherwise a new cell
    starts (a critical event). Returns (labels, adjacency): labels[r, c] = cell id >= 0 for free
    cells, -1 otherwise; adjacency = dict cell -> set of cells that touch it across a column.
    """
    raise NotImplementedError("TODO: implement boustrophedon_decomposition")


def _grid_bfs_path(free, a, b):
    """Shortest 8-connected path of free cells from a to b (inclusive), or None."""
    if a == b:
        return [a]
    R, C = free.shape
    parent = {a: None}
    q = [a]
    head = 0
    while head < len(q):
        n = q[head]
        head += 1
        for dr, dc in _MOVES:
            m = (n[0] + dr, n[1] + dc)
            if 0 <= m[0] < R and 0 <= m[1] < C and free[m] and m not in parent:
                parent[m] = n
                if m == b:
                    out = [m]
                    while parent[out[-1]] is not None:
                        out.append(parent[out[-1]])
                    return out[::-1]
                q.append(m)
    return None


def coverage_path(free, start) -> dict:
    """Coverage path over all free cells reachable from ``start`` (grid cell = sensor footprint).

    Decompose with :func:`boustrophedon_decomposition`; visit cells greedily (next = unvisited
    cell whose nearer end column is closest to the current position); sweep each cell column by
    column in alternating up/down direction, entering from the nearer end; join consecutive
    waypoints that are not neighbours with a shortest free 8-connected path. Returns
    {"path": [(r, c), ...] (consecutive cells 8-adjacent, all free), "labels", "order"}.
    """
    raise NotImplementedError("TODO: implement coverage_path")


def reachable(free, start) -> np.ndarray:
    """Boolean mask of free cells 8-connected to start (helper)."""
    R, C = free.shape
    seen = np.zeros_like(free)
    if not free[start]:
        return seen
    seen[start] = True
    stack = [start]
    while stack:
        n = stack.pop()
        for dr, dc in _MOVES:
            m = (n[0] + dr, n[1] + dc)
            if 0 <= m[0] < R and 0 <= m[1] < C and free[m] and not seen[m]:
                seen[m] = True
                stack.append(m)
    return seen


def _append_connected(free, path, cell):
    last = path[-1]
    if cell == last:
        return
    if max(abs(cell[0] - last[0]), abs(cell[1] - last[1])) == 1:
        path.append(cell)
        return
    link = _grid_bfs_path(free, last, cell)
    path.extend(link[1:])


if __name__ == "__main__":  # benchmark figure: risk-aware A*, RRT*, coverage
    import time

    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(1, 3, figsize=(16, 5))
    res, N = 0.25, 81
    hz = (10.0, 10.0, 0.0)                            # fictional suspected-item location, sigma 0
    for w_, lab in ((0.0, "lethal core only"), (2.0, "with risk layer")):
        cost = risk_layer((N, N), res, [hz], standoff=3.0, w=w_, sigma=1.5)
        t = time.perf_counter()
        r = astar(cost, (40, 0), (40, 80), res)
        xy = cells_to_xy(r.path, res)
        ax[0].plot(xy[:, 0], xy[:, 1], label=f"{lab}: {path_length(xy):.2f} m, "
                   f"closest {closest_approach(xy, hz):.1f} m, {r.expanded} exp, {1e3 * (time.perf_counter() - t):.0f} ms")
    ax[0].imshow(np.where(np.isfinite(cost), cost, 3), origin="lower", extent=(0, N * res, 0, N * res), cmap="Reds", alpha=0.5)
    ax[0].set(title="A* on a risk cost map", aspect="equal")
    ax[0].legend(fontsize=7)
    obst = [np.array([[4, 2], [6, 2], [6, 8], [4, 8]], float), np.array([[7, 0], [8, 0], [8, 4], [7, 4]], float)]
    rs = rrt_star((1, 5), (9, 5), obst, (0, 0, 10, 10), np.random.default_rng(0), n_iter=3000, step=1.0)
    for P in obst:
        ax[1].fill(*P.T, color="0.6")
    for i, p in enumerate(rs.parents):
        if p >= 0:
            ax[1].plot(*np.array([rs.nodes[p], rs.nodes[i]]).T, color="0.85", lw=0.5)
    ax[1].plot(*rs.path.T, "C3-", lw=2)
    ax[1].set(title=f"RRT* 3000 its: cost {rs.cost:.2f}", aspect="equal")
    free = np.ones((25, 40), bool)
    free[8:16, 15:25] = False
    cp = coverage_path(free, (0, 0))
    ax[2].imshow(cp["labels"], origin="lower", cmap="tab10")
    ax[2].plot([c for _, c in cp["path"]], [r for r, _ in cp["path"]], "k-", lw=0.8)
    ax[2].set(title=f"Boustrophedon coverage: {len(cp['order'])} cells, {len(cp['path'])} steps")
    plt.tight_layout()
    plt.show()
