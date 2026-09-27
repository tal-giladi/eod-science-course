# P09 · Computer-vision detection: classical baseline, small CNN, and metrics that matter

**Level:** Advanced · **Estimated time:** 12–16 h · **Module:** `cvdetect`

## Goal

Build a complete, honest detection experiment on synthetic imagery, entirely on a CPU:

1. A **self-contained generator** of fictional scenes in three modalities: visible, low-light
   (photon-limited) and thermal-like.
2. A **classical baseline**. OpenCV proposes regions with a background model, edges and blobs.
   Handcrafted features are then scored by a logistic regression you write in NumPy.
3. A **small CNN** (PyTorch, CPU, trains in under 2 min) that scores the same proposals.
4. **Evaluation the way 09.1 argues for.** Report recall at a fixed number of false alarms per
   image and the FROC curve, not mAP. Add calibration (ECE, reliability) and temperature scaling
   from 09.2.

The target class is **Object-K**, a fictional capsule-shaped item with a banded surface. Clutter
consists of rocks, discs, sticks, boxes and **plain capsules**. The plain capsule is the hard
negative: same shape, no banding. Nothing here depicts or describes a real object.

## Background

- [09.1 Perception tasks for EOD](lessons/stage-09/lesson-01.md): cost-weighted thresholds (§1),
  detection, IoU and NMS (§3), metrics that matter, recall at FAR and FROC (§7). The lesson's
  "Programming exercise" is the evaluation half of this project.
- [09.2 Uncertainty-aware ML](lessons/stage-09/lesson-02.md): calibration and ECE (§2),
  temperature scaling (§3). Its programming exercise wraps this project's classifier.
- Related: [P10 scene generator](projects/p10-scene-generator/README.md) (a richer generator),
  [P12 human-in-the-loop decisions](projects/p12-hitl-decision/README.md) (consumes calibrated
  scores), and [Sim J detection theory](sims/detection-theory/index.html) (operating points).

## Requirements

- `iou`, `iou_matrix` and greedy `nms`, with IoU of touching boxes = 0 and suppression when IoU
  is strictly greater than the threshold.
- `match_detections`: greedy one-to-one matching by descending score. Duplicates count as false
  positives.
- `froc_curve`: one operating point per *distinct* score (ties form a single point).
  `recall_at_fppi` returns the best sensitivity with FPPI ≤ budget. `froc_score` is the mean
  over (0.5, 1, 2, 4) FPPI.
- `ece`: top-label, equal-width bins. `fit_temperature` minimises NLL over T > 0 and must leave
  the argmax unchanged.
- `LogisticRegression`: L2-regularised, Newton/IRLS, NumPy only.
- `handcrafted_features`: at least orientation histograms, a texture/frequency descriptor and
  centre–surround contrast.
- CNN: `build_cnn`, `train_cnn`, deterministic under a seed, CPU only.

## API

```python
# given
MODALITIES = ("visible", "lowlight", "thermal");  Scene(image, boxes, clutter_boxes, modality, meta)
generate_scene(seed, size=96, modality="visible", n_targets=None, n_clutter=None) -> Scene
generate_dataset(n, seed=0, size=96, modality="visible") -> list[Scene]
make_patch_dataset(n, seed=0, patch=32, modality="visible", jitter=3.0) -> (X (n,32,32), y (n,))
crop_patch(image, cx, cy, size=32);  softmax(z, T=1.0);  reliability_curve(probs, labels, n_bins=15)
band_energy(patch, n_bands=8);  extract_features(X)
propose_regions(image, k=2.0, min_area=15, max_area=1200, use_edges=True)   # needs cv2
ClassicalDetector(patch=32, l2=1e-2, nms_iou=0.3).fit(X, y) / .score_patches(X) / .detect(image)
cnn_logits(model, X);  CNNDetector(model, T=1.0).detect(image)
evaluate_detector(detector, scenes, iou_thr=0.3) -> dict;  run_benchmark(outdir="p09_out", ...)

# yours
iou(a, b) -> float;  iou_matrix(A, B) -> (n, m);  nms(boxes, scores, iou_thr=0.5) -> kept indices
match_detections(det_boxes, det_scores, gt_boxes, iou_thr=0.3) -> bool array
froc_curve(detections, ground_truth, iou_thr=0.3) -> {"thresholds","sensitivity","fppi","n_gt","n_images"}
recall_at_fppi(curve, fppi_max) -> float;  froc_score(curve, fppi_points=(0.5, 1, 2, 4)) -> float
nll(logits, labels, T=1.0);  ece(probs, labels, n_bins=15);  fit_temperature(logits, labels) -> T
orientation_histograms(patch, cells=4, bins=8);  handcrafted_features(patch)
LogisticRegression(l2=1e-2).fit(X, y) / .decision_function(X) / .predict_proba(X)
build_cnn(n_classes=2, width=8) -> torch.nn.Module
train_cnn(X, y, epochs=10, batch=64, lr=3e-3, width=8, seed=0, augment=True, threads=2) -> model
```

## Input / Output

Images are `float32` arrays in [0, 1] of shape (96, 96). Boxes are `(x1, y1, x2, y2)` in pixel
coordinates, with x as the column. A detector returns `(boxes (n, 4), scores (n,))` per image.
Logits have shape (n, K) and probabilities are row-stochastic. `run_benchmark` writes
`p09_out/froc.png`, `p09_out/reliability.png` and `p09_out/report.md`.

## Constraints

- NumPy and SciPy for everything except proposals (OpenCV) and the CNN (PyTorch, CPU). Both are
  optional. Their tests are guarded with `pytest.importorskip` and the module imports them
  lazily.
- No scikit-learn and no detection or metrics libraries.
- The test suite runs in under 30 s (about 23 s here, most of it importing PyTorch and training
  the small-config CNN). The full benchmark takes about 2–3 min, each CNN under 1 min.
- Deterministic under seeds.

## Expected behaviour

Reference results from `python projects/p09-cv-detection/solution/cvdetect.py` (100 test scenes
per modality, IoU ≥ 0.3):

| Modality | Detector | Recall @ 0.5 FPPI | Recall @ 2 FPPI | FROC score |
|---|---|---|---|---|
| visible | classical | 0.93 | 0.94 | 0.94 |
| visible | CNN | 0.95 | 0.95 | 0.95 |
| low-light | classical | 0.55 | 0.60 | 0.58 |
| low-light | CNN | 0.51 | 0.60 | 0.57 |
| thermal | classical | 0.93 | 0.99 | 0.97 |
| thermal | CNN | 0.76 | 0.99 | 0.91 |

Read these numbers critically. In low light, recall saturates near 0.6 for *both* classifiers
because the proposal stage misses items. A better classifier cannot recover what the proposer
never offered: in a cascade, look at stage recall first. On the fitted calibration sets, the CNN
temperatures come out close to 1 (0.9–1.3) and ECE is already small (0.01–0.06). Small CNNs
trained briefly are not the over-confident giants of Guo et al., so check before assuming.

## Test cases (`tests/test_cvdetect.py`)

| Test | What it checks |
|---|---|
| `test_generator_deterministic_with_seed` (×3 modalities) | same seed → identical image and boxes; valid boxes and range; balanced patch sets |
| `test_iou_hand_cases`, `test_iou_matrix_matches_scalar` | overlap, identity, disjoint, touching, containment, the lesson 81/119 case |
| `test_nms_hand_case_from_lesson` | 09.1 §3 NMS example, score order, threshold edge |
| `test_match_duplicates_are_false_positives` | a duplicate on a matched GT is an FP |
| `test_froc_and_recall_at_fppi_hand_case` | a hand-built two-image case: exact curve and recall at 0.25/0.5/1/1.5 FPPI |
| `test_froc_ties_are_one_operating_point` | tied scores form one point |
| `test_froc_score_lesson_example` | 0.70, 0.80, 0.88, 0.93 → 0.8275 |
| `test_ece_lesson_example` | the 09.2 example, ECE = 0.072 |
| `test_ece_of_perfectly_calibrated_predictor_is_near_zero` | ECE < 0.01 when calibrated; over-confidence detected |
| `test_temperature_scaling_recovers_known_temperature` | T = 2.5 ± 0.2, NLL decreases, argmax unchanged |
| `test_logistic_regression_separates_gaussians` | accuracy near Bayes; zero gradient at the optimum |
| `test_handcrafted_baseline_beats_chance` | patch accuracy > 0.85, AUC > 0.9 (chance 0.5) |
| `test_classical_detector_on_scenes` (cv2) | learned scores beat random scores on the same proposals at fixed FPPI |
| `test_small_cnn_trains_and_calibrates` (torch) | small config (400 patches, 3 epochs) trains to > 0.75 accuracy; temperature scaling never worsens NLL |

## Milestones

1. Geometry: `iou`, `iou_matrix`, `nms`.
2. Evaluation: `match_detections`, `froc_curve`, `recall_at_fppi`, `froc_score`.
3. Calibration: `nll`, `ece`, `fit_temperature`.
4. Classical: `orientation_histograms`, `handcrafted_features`, `LogisticRegression`. Then run
   `ClassicalDetector` on scenes.
5. CNN: `build_cnn`, `train_cnn`. Then `run_benchmark` and interpret the report.

## Extension challenges

- Add proposal recall to the report (the fraction of GT covered by any proposal at IoU ≥ 0.3) and
  improve the low-light proposer, for example with denoising before background subtraction or
  multi-scale blob detection. Watch the FROC ceiling move.
- Replace the proposal stage with a fully convolutional score map and local-maximum detection.
  Compare NMS-induced misses on clustered items.
- Train on `visible`, test on `thermal`, and measure how calibration shifts across domains.
  Refit T per modality (09.2 Exercise 3).
- Class-wise ECE for the target class, plus Brier score and NLL alongside ECE.
- Point-based scoring with a halo radius and `linear_sum_assignment` (09.1 programming exercise),
  and Clopper–Pearson intervals on recall.
- Feed calibrated scores into the conformal/abstention layer of 09.2 and
  [P12](projects/p12-hitl-decision/README.md).

## Hints

<details><summary>FROC with ties</summary>

Sort all detections by score and take cumulative TP and FP sums. Keep only the *last* index of
each group of equal scores, because a threshold cannot separate tied detections. Match per image
*before* pooling. Greedy matching in score order is consistent with thresholding, so a
detection's TP/FP status never depends on detections below the threshold.

</details>

<details><summary>ECE binning</summary>

Use bin index `ceil(c * B) - 1`, clipped to [0, B-1], so that a confidence of exactly 1.0 lands in
the last bin and 0.95 lands in bin 14 of 15. The lesson example must come out to exactly 0.072.

</details>

<details><summary>Temperature scaling</summary>

Minimise over log T with a bounded scalar search. NLL is convex in β = 1/T, so the optimum is
unique. Compute log-sum-exp stably by subtracting the row maximum.

</details>

<details><summary>Features that separate the hard negative</summary>

Shape alone cannot tell an Object-K from a plain capsule. The banding can. Band energy in the
4–6 px period range of the *central* region, and dominant gradient orientation along the
capsule, both carry it. In thermal imagery the banding is blurred away. The target is warm, but
so is some clutter, so centre–surround contrast matters more there.

</details>

<details><summary>Newton for logistic regression</summary>

The Hessian `Zᵀ diag(p(1-p)) Z / n + R` is symmetric positive definite, so solve with a Cholesky
factorisation (`scipy.linalg.cho_factor` / `cho_solve`). On some BLAS builds a general LU solve
of a 150×150 system is surprisingly slow.

</details>

<details><summary>CNN on CPU</summary>

Standardise each patch, augment with 90° rotations and flips, and use width 8. Cap PyTorch
threads at about 2: tiny convolutions on many cores are *slower* because of thread
oversubscription.

</details>

## How to run

```bash
python -m pytest projects/p09-cv-detection                  # starter: fails with NotImplementedError
EOD_SOLUTION=1 python -m pytest projects/p09-cv-detection   # reference (bash)
set EOD_SOLUTION=1 && python -m pytest projects/p09-cv-detection   # Windows cmd
python projects/p09-cv-detection/solution/cvdetect.py       # full benchmark -> ./p09_out
```
