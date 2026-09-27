"""Tests for P09 (cvdetect). Run from the repo root:  python -m pytest projects/p09-cv-detection"""
import os, sys, pathlib
_ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_ROOT / ("solution" if os.environ.get("EOD_SOLUTION") else "starter")))
import cvdetect as mod  # noqa: E402

import numpy as np  # noqa: E402
import pytest  # noqa: E402


# ------------------------------------------------------------------ generator (given code)
@pytest.mark.parametrize("modality", mod.MODALITIES)
def test_generator_deterministic_with_seed(modality):
    a, b = mod.generate_scene(42, modality=modality), mod.generate_scene(42, modality=modality)
    np.testing.assert_array_equal(a.image, b.image)
    np.testing.assert_array_equal(a.boxes, b.boxes)
    c = mod.generate_scene(43, modality=modality)
    assert not np.array_equal(a.image, c.image)
    assert a.image.dtype == np.float32 and a.image.min() >= 0 and a.image.max() <= 1
    s = mod.generate_scene(7, modality=modality, n_targets=2, n_clutter=3)
    assert s.boxes.shape == (2, 4) and s.clutter_boxes.shape == (3, 4)
    assert np.all(s.boxes[:, 2] > s.boxes[:, 0]) and np.all(s.boxes[:, 3] > s.boxes[:, 1])
    assert np.all(s.boxes >= 0) and np.all(s.boxes <= 96)
    X1, y1 = mod.make_patch_dataset(20, seed=3, modality=modality)
    X2, y2 = mod.make_patch_dataset(20, seed=3, modality=modality)
    np.testing.assert_array_equal(X1, X2)
    np.testing.assert_array_equal(y1, y2)
    assert y1.sum() == 10


# ------------------------------------------------------------------ IoU and NMS
def test_iou_hand_cases():
    assert mod.iou((0, 0, 10, 10), (5, 5, 15, 15)) == pytest.approx(25 / 175)
    assert mod.iou((0, 0, 10, 10), (0, 0, 10, 10)) == pytest.approx(1.0)
    assert mod.iou((0, 0, 10, 10), (20, 0, 30, 10)) == 0.0
    assert mod.iou((0, 0, 10, 10), (10, 0, 20, 10)) == 0.0            # touching edges
    assert mod.iou((0, 0, 10, 10), (2, 2, 4, 4)) == pytest.approx(4 / 100)   # containment
    assert mod.iou((0, 0, 10, 10), (1, 1, 11, 11)) == pytest.approx(81 / 119)


def test_iou_matrix_matches_scalar():
    rng = np.random.default_rng(0)
    A = np.sort(rng.uniform(0, 50, (6, 2, 2)), axis=1).transpose(0, 2, 1).reshape(6, 4)[:, [0, 2, 1, 3]]
    B = np.sort(rng.uniform(0, 50, (4, 2, 2)), axis=1).transpose(0, 2, 1).reshape(4, 4)[:, [0, 2, 1, 3]]
    M = mod.iou_matrix(A, B)
    assert M.shape == (6, 4)
    for i in range(6):
        for j in range(4):
            assert M[i, j] == pytest.approx(mod.iou(A[i], B[j]))


def test_nms_hand_case_from_lesson():
    boxes = np.array([[0, 0, 10, 10], [1, 1, 11, 11], [8, 8, 18, 18]], float)
    keep = mod.nms(boxes, np.array([0.9, 0.8, 0.7]), iou_thr=0.5)
    assert list(keep) == [0, 2]
    keep = mod.nms(boxes, np.array([0.6, 0.8, 0.7]), iou_thr=0.5)   # box 1 now wins
    assert list(keep) == [1, 2]
    keep = mod.nms(boxes, np.array([0.9, 0.8, 0.7]), iou_thr=0.7)   # 0.68 < 0.7: all kept
    assert list(keep) == [0, 1, 2]
    assert len(mod.nms(np.zeros((0, 4)), np.zeros(0))) == 0


# ------------------------------------------------------------------ matching, FROC, recall@FPPI
def _hand_case():
    A, B, C = [0, 0, 10, 10], [20, 20, 30, 30], [5, 5, 15, 15]
    far = [60, 60, 70, 70]
    img1 = (np.array([A, far, B, [0, 0, 10, 11]], float), np.array([0.9, 0.8, 0.4, 0.7]))
    img2 = (np.array([C, [40, 0, 50, 10]], float), np.array([0.6, 0.95]))
    return [img1, img2], [np.array([A, B], float), np.array([C], float)]


def test_match_duplicates_are_false_positives():
    dets, gts = _hand_case()
    tp = mod.match_detections(*dets[0], gts[0], iou_thr=0.5)
    assert list(tp) == [True, False, True, False]


def test_froc_and_recall_at_fppi_hand_case():
    dets, gts = _hand_case()
    c = mod.froc_curve(dets, gts, iou_thr=0.5)
    # sorted scores: .95 FP, .9 TP, .8 FP, .7 FP(dup), .6 TP, .4 TP ; 3 GT, 2 images
    np.testing.assert_allclose(c["sensitivity"], [0, 1 / 3, 1 / 3, 1 / 3, 2 / 3, 1])
    np.testing.assert_allclose(c["fppi"], [0.5, 0.5, 1.0, 1.5, 1.5, 1.5])
    assert mod.recall_at_fppi(c, 0.25) == 0.0
    assert mod.recall_at_fppi(c, 0.5) == pytest.approx(1 / 3)
    assert mod.recall_at_fppi(c, 1.0) == pytest.approx(1 / 3)
    assert mod.recall_at_fppi(c, 1.5) == pytest.approx(1.0)


def test_froc_ties_are_one_operating_point():
    dets = [(np.array([[0, 0, 10, 10], [50, 50, 60, 60]], float), np.array([0.5, 0.5]))]
    c = mod.froc_curve(dets, [np.array([[0, 0, 10, 10]], float)])
    assert len(c["thresholds"]) == 1
    assert c["sensitivity"][0] == 1.0 and c["fppi"][0] == 1.0


def test_froc_score_lesson_example():
    curve = {"fppi": np.array([0.5, 1, 2, 4]), "sensitivity": np.array([0.70, 0.80, 0.88, 0.93])}
    assert mod.froc_score(curve) == pytest.approx(0.8275)


# ------------------------------------------------------------------ calibration
def test_ece_lesson_example():
    probs, labels = [], []
    for conf, n, k in [(0.95, 300, 240), (0.75, 500, 350), (0.55, 200, 112)]:
        probs += [[conf, 1 - conf]] * n
        labels += [0] * k + [1] * (n - k)
    assert mod.ece(np.array(probs), np.array(labels)) == pytest.approx(0.072, abs=1e-9)


def test_ece_of_perfectly_calibrated_predictor_is_near_zero():
    rng = np.random.default_rng(0)
    p = rng.uniform(0.5, 1.0, 200_000)
    y = (rng.uniform(size=p.size) > p).astype(int)        # class 0 correct with probability p
    assert mod.ece(np.c_[p, 1 - p], y) < 0.01
    # an over-confident predictor is caught
    q = np.clip(p + 0.1, 0, 1)
    assert mod.ece(np.c_[q, 1 - q], y) > 0.07


def test_temperature_scaling_recovers_known_temperature():
    rng = np.random.default_rng(1)
    z = rng.normal(0, 1.5, (20_000, 3))
    y = np.array([rng.choice(3, p=p) for p in mod.softmax(z)])
    logits = 2.5 * z                                          # over-confident by T = 2.5
    T = mod.fit_temperature(logits, y)
    assert T == pytest.approx(2.5, abs=0.2)
    assert mod.nll(logits, y, T) < mod.nll(logits, y, 1.0)
    np.testing.assert_array_equal(mod.softmax(logits, T).argmax(1), logits.argmax(1))
    assert mod.ece(mod.softmax(logits, T), y) < mod.ece(mod.softmax(logits), y)


# ------------------------------------------------------------------ classical baseline
def test_logistic_regression_separates_gaussians():
    rng = np.random.default_rng(2)
    X = np.r_[rng.normal(-1, 1, (500, 2)), rng.normal(1, 1, (500, 2))]
    y = np.r_[np.zeros(500), np.ones(500)]
    clf = mod.LogisticRegression(l2=1e-4).fit(X, y)
    acc = ((clf.predict_proba(X) > 0.5) == y).mean()
    assert acc > 0.9                                          # Bayes accuracy is 0.921
    # gradient of the regularised loss vanishes at the optimum
    Z = np.c_[(X - clf.mu) / clf.sd, np.ones(len(X))]
    p = clf.predict_proba(X)
    g = Z.T @ (p - y) / len(y) + np.r_[1e-4 * clf.w, 0]
    assert np.abs(g).max() < 1e-6


@pytest.fixture(scope="module")
def classical():
    Xtr, ytr = mod.make_patch_dataset(600, seed=1)
    return mod.ClassicalDetector().fit(Xtr, ytr)


def test_handcrafted_baseline_beats_chance(classical):
    Xte, yte = mod.make_patch_dataset(300, seed=2)
    det = classical
    p = det.score_patches(Xte)
    acc = ((p > 0.5) == yte).mean()
    assert acc > 0.85                                         # chance = 0.5
    # AUC by the rank statistic
    pos, neg = p[yte == 1], p[yte == 0]
    auc = (pos[:, None] > neg[None, :]).mean()
    assert auc > 0.9


def test_classical_detector_on_scenes(classical):
    pytest.importorskip("cv2")
    det = classical
    scenes = mod.generate_dataset(25, seed=5)
    res = mod.evaluate_detector(det, scenes)
    assert res["n_gt"] > 10
    # same proposals, random scores: the learned scores must do better at a fixed FPPI
    rng = np.random.default_rng(0)

    class RandomScorer(mod.ClassicalDetector):
        def score_patches(self, X):
            return rng.uniform(size=len(X))

    rand = mod.evaluate_detector(RandomScorer(), scenes)
    assert res["recall@0.5fppi"] > rand["recall@0.5fppi"] + 0.2
    assert res["recall@1.0fppi"] > 0.6


# ------------------------------------------------------------------ CNN (optional)
def test_small_cnn_trains_and_calibrates():
    pytest.importorskip("torch")
    Xtr, ytr = mod.make_patch_dataset(400, seed=11)
    Xca, yca = mod.make_patch_dataset(400, seed=12)
    model = mod.train_cnn(Xtr, ytr, epochs=3, seed=0)        # small config: a few seconds on CPU
    z = mod.cnn_logits(model, Xca)
    assert z.shape == (400, 2)
    assert (z.argmax(1) == yca).mean() > 0.75
    T = mod.fit_temperature(z, yca)
    assert mod.nll(z, yca, T) <= mod.nll(z, yca, 1.0) + 1e-12
    np.testing.assert_array_equal(mod.softmax(z, T).argmax(1), z.argmax(1))
