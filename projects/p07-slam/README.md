# P07 · SLAM simulation: occupancy grids, ICP, EKF-SLAM and pose graphs

**Level:** Expert · **Estimated time:** 12–16 h · **Module:** `slam2d`

## Goal

Build a small but complete 2D SLAM toolkit and use it to demonstrate the central fact of mapping:
without loop closures, error grows with distance; one good loop closure collapses it everywhere.
You will write the four core estimators that every mapping stack on a ground robot is built from:

1. **Occupancy-grid mapping** with log-odds and an inverse sensor model, from known poses.
2. **ICP scan matching** (point-to-point) with the closed-form SVD alignment.
3. **EKF-SLAM** with range-bearing landmarks and known data association.
4. **Pose-graph optimisation** with Gauss–Newton on SE(2), using sparse normal equations
   (`scipy.sparse`), plus a loop-closure demonstration on a synthetic loop.

Everything is geometric and fictional: an 8 m × 6 m room with a pillar, a simulated 2D LiDAR and
point landmarks.

## Background

- [06.7 Mapping & SLAM](lessons/stage-06/lesson-07.md): the core lesson. Sections 1–5 are the
  specification for this project; the square-loop numbers in section 4 are a test case.
- [06.6 Localisation](lessons/stage-06/lesson-06.md): EKF prediction/update, NEES, odometry models.
- [06.2 Spatial mathematics](lessons/stage-06/lesson-02.md): rotations and rigid transforms.
- Related projects: [P04 localisation](projects/p04-localization/README.md) (the EKF you extend
  here), [P05 robot simulator](projects/p05-robot-sim/README.md) (source of richer scans),
  [P06 path planning](projects/p06-path-planning/README.md) (consumes the occupancy grid).

## Requirements

- Log-odds occupancy update along Bresenham rays; traversed cells get `l_free`, the return cell
  `l_occ`, cells beyond the return are untouched; no-return beams mark the whole ray free;
  clamping to `[l_min, l_max]`.
- `rigid_align` must return a proper rotation (det = +1) in any dimension, including for
  reflection-prone data.
- `icp` uses a k-d tree for nearest neighbours, optional outlier rejection, and returns
  convergence information.
- `EKFSLAM.predict` costs O(n): only the robot block and robot–landmark cross terms change.
  `EKFSLAM.update` initialises landmarks on first sight with correct cross-covariances, then uses
  the Joseph form.
- `build_normal_equations` assembles `H` as a `scipy.sparse` matrix from 3×3 blocks and fixes
  the gauge by anchoring one node; `optimize_pose_graph` solves with `spsolve` and returns the χ²
  history.

## API

```python
# given (implemented in the starter)
wrap(a); rot2(th); compose(a, b); inverse(a); relative(xi, xj); transform_points(pose, pts)
bresenham(x0, y0, x1, y1) -> list[(i, j)];  logodds(p); prob(L)
make_room() -> {"segments", "bounds", "solids"}
simulate_scan(pose, segments, n_beams=360, max_range=12.0, noise_std=0.0, rng=None) -> (ranges, angles)
scan_to_points(ranges, angles, max_range=12.0) -> (N, 2)
sample_walls(segments, spacing=0.03, rng=None) -> (N, 2)
make_loop_dataset(n_per_side=10, ..., seed=0) -> {"truth", "odom", "edges", "odom_edges"}
square_example() -> {"odom", "truth", "edges"}
simulate_landmark_run(landmarks, n_steps=400, ..., seed=0) -> {"poses", "controls", "measurements", ...}
unicycle_step(x, u, dt); range_bearing(x, lm)
run_ekf_slam(run, n_landmarks) -> (EKFSLAM, {"poses", "lm_trace"})
chi2(X, edges); position_errors(X, truth); build_map(...); run_loop_demo(outdir=None, seed=0)

# yours
class OccupancyGrid(width, height, resolution=0.1, origin=(0, 0), p_occ=0.7, p_free=0.35, l_min=-2, l_max=3.5):
    integrate_beam(origin_cell, end_cell, hit) -> None
    integrate_scan(pose, ranges, angles, max_range=12.0) -> None
rigid_align(P, Q) -> (R, t)
icp(source, target, R0=None, t0=None, max_iter=60, tol=1e-10, reject_dist=None) -> (R, t, info)
class EKFSLAM(n_landmarks, x0, P0=None, control_std, meas_std):
    predict(u, dt) -> None
    update(j, z) -> None
edge_error(xi, xj, z) -> (e, A, B)
build_normal_equations(X, edges, anchor=0, anchor_weight=1e8) -> (H: scipy.sparse.csc_matrix, b)
optimize_pose_graph(X0, edges, iters=20, tol=1e-9, anchor=0) -> (X, chi2_history)
```

## Input / Output

| Item | Format |
|---|---|
| Pose | `np.array([x, y, theta])`, m and rad, angle wrapped to [−π, π) |
| Scan | `(ranges, angles)`, angles in the robot frame; `range == max_range` means no return |
| Grid | `OccupancyGrid.L[j, i]` log-odds, `(i, j)` = (column, row); `probabilities()` in [0, 1] |
| Edge | `(i, j, z_ij, Omega_ij)`: pose of node j in frame i, 3×3 information matrix |
| EKF state | `mu = [x, y, θ, l1x, l1y, …]`, `Sigma` (3+2N)² |

## Constraints

- NumPy, SciPy (`scipy.sparse`, `scipy.spatial.cKDTree`), matplotlib for the demo only.
- No SLAM or registration libraries. ICP and the pose-graph solver are yours.
- The whole test suite runs in under 30 s (it takes about 3 s with the reference solution).

## Expected behaviour

- Three hits on one cell give p = 0.927; one further pass-through gives 0.872 (lesson 06.7 §1).
- `icp` recovers an exact rigid transform (12°, 0.36 m) on densely sampled walls to 10⁻⁶, and
  the relative pose between two noisy scans to within 5 cm / 1°.
- EKF-SLAM: every landmark's covariance trace is non-increasing after initialisation and ends
  well below its initial value; estimates stay within 0.3 m of the truth.
- The lesson square: max error 0.194 m before, below 0.01 m after; χ² 46.2 → 1.84.
- The synthetic loop (`make_loop_dataset`, heading bias 0.01 rad per step): max position error
  about 1.48 m from odometry, about 0.14 m after optimisation. Without the loop-closure edge the
  optimum *is* the odometry chain.
- `python projects/p07-slam/solution/slam2d.py` writes `p07_out/loop_closure.png`: trajectories,
  χ² per iteration, and maps built from the odometry and from the optimised poses.

## Test cases (`tests/test_slam2d.py`)

| Test | What it checks |
|---|---|
| `test_log_odds_lesson_numbers`, `test_log_odds_clamped` | inverse sensor model, untouched cells beyond the return, clamping |
| `test_occupancy_grid_converges_on_room` | classification accuracy against the ground-truth room rises monotonically with scans and ends above 95 % |
| `test_rigid_align_exact_and_proper_rotation` | exact recovery in 2D and 3D; det R = +1 for mirrored data |
| `test_icp_recovers_known_rigid_transform` | ICP from identity recovers a known transform |
| `test_icp_between_two_real_scans` | ICP with an odometry-like initial guess on two independent noisy scans |
| `test_ekf_slam_landmark_covariances_shrink` | monotone landmark covariances, symmetric PSD `Sigma`, accurate map |
| `test_ekf_predict_only_touches_robot_block` | prediction leaves landmark blocks unchanged |
| `test_edge_jacobians_match_finite_differences` | analytic A, B against central differences |
| `test_normal_equations_are_sparse` | `H` is `scipy.sparse`, symmetric, with block-sparse fill |
| `test_square_example_from_lesson` | the 06.7 numbers |
| `test_loop_closure_reduces_error_vs_odometry` | error reduction of 4× or more, χ² drop, anchoring, pure chain = odometry |

## Milestones

1. `integrate_beam`, `integrate_scan`: pass the occupancy tests; plot the room map.
2. `rigid_align`, then `icp`.
3. `EKFSLAM.predict` and `update`; plot landmark covariance ellipses over time.
4. `edge_error` (check the Jacobians by finite differences first), `build_normal_equations`,
   `optimize_pose_graph`; reproduce the square example, then run `run_loop_demo`.

## Extension challenges

- Replace odometry edges in the loop demo with ICP between consecutive scans (scan-matching
  odometry), and detect the loop closure by ICP against the first scan when the predicted pose is
  near it.
- Point-to-line ICP; monitor the smallest eigenvalue of its information matrix and show the
  corridor degeneracy of 06.7 §2.
- Add a *false* loop closure. Show how the map bends, then fix it with a Huber or Cauchy kernel
  (iteratively reweighted least squares) or switchable constraints.
- Levenberg–Marquardt with adaptive damping; compare iterations from a poor initial guess.
- EKF-SLAM NEES over Monte Carlo runs (06.6) to expose the inconsistency of long runs.
- Test that the optimum is invariant, up to a rigid transform, to the choice of anchor node.

## Hints

<details><summary>Occupancy grid</summary>

Bresenham returns the origin and end cells included. Update all but the last with `l_free`,
then the last with `l_occ` or `l_free`. Skip out-of-bounds cells rather than clipping indices,
or the map border fills with phantom walls. The grid origin in the test is chosen so that walls
fall in the middle of cells. Walls lying exactly on cell boundaries make grazing beams clear wall
cells.

</details>

<details><summary>ICP</summary>

Accumulate the transform as `R, t = dR @ R, dR @ t + dt`. Scans sampled uniformly in *angle*
have far walls sparsely sampled and near walls densely sampled. Point-to-point ICP can then stop
in a local minimum a few tenths of a degree from the truth, even for noise-free data. That is why
the exact-recovery test uses points sampled uniformly along the walls, and why production
systems use point-to-line or point-to-plane residuals.

</details>

<details><summary>EKF-SLAM</summary>

On first sight, the new landmark's cross-covariance with *every* existing state is
`Gp @ Sigma[:3, :]`, not only with the robot. Forgetting the landmark–landmark cross terms
makes the filter overconfident. Use the Joseph form and symmetrise, otherwise the monotonicity
test can fail from round-off.

</details>

<details><summary>Pose graph</summary>

Build COO arrays of (row, col, value) for every 3×3 block and convert once with `.tocsc()`;
duplicate entries are summed. The anchor adds `1e8 * I` to one diagonal block. Wrap the angle
residual and the updated angles. For a pure chain with an anchor, the system is square and
consistent. Gauss–Newton must return the odometry exactly, which is a useful sanity check.

</details>

## How to run

```bash
# learner (starter): tests fail with NotImplementedError until you implement the functions
python -m pytest projects/p07-slam
# reference solution
EOD_SOLUTION=1 python -m pytest projects/p07-slam        # bash
set EOD_SOLUTION=1 && python -m pytest projects/p07-slam  # Windows cmd
# loop-closure demo figure
python projects/p07-slam/solution/slam2d.py
```
