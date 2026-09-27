"""cvdetect -- synthetic imagery, classical and CNN detectors, and detection/calibration metrics (P09).

All objects are fictional. The *target* class is "Object-K": a small capsule-shaped item with a
banded (striped) surface. *Clutter* comprises rocks, discs, sticks, boxes and plain (un-banded)
capsules -- the last is the hard negative. Images are single-channel float32 in [0, 1] and come in
three modalities: ``visible``, ``lowlight`` (photon-limited, amplified) and ``thermal`` (warm
target, blurred, low texture contrast, some warm clutter).

Layers
------
1. Generator (self-contained, numpy + scipy.ndimage, deterministic from a seed).
2. Geometry: IoU, greedy NMS.
3. Evaluation: greedy matching, FROC, recall at a fixed false-alarm rate per image, ECE,
   temperature scaling.
4. Classical baseline: OpenCV background model + edges + blobs for proposals; handcrafted features
   (orientation histograms, band energy, contrast) and a numpy logistic regression.
5. Small CNN (PyTorch, CPU) scoring the same proposals.

OpenCV and PyTorch are optional imports: only the functions that need them import them.
Boxes are ``(x1, y1, x2, y2)`` in pixel coordinates (x = column), continuous, x2 > x1.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from scipy import ndimage
from scipy.optimize import minimize_scalar

try:  # optional
    import torch
    from torch import nn
except ImportError:  # pragma: no cover
    torch, nn = None, None

MODALITIES = ("visible", "lowlight", "thermal")
CLUTTER_KINDS = ("rock", "disc", "stick", "box", "plain_capsule")

# =============================================================================================
# 1. Synthetic generator (given)
# =============================================================================================


@dataclass
class Scene:
    image: np.ndarray                 # (H, W) float32 in [0, 1]
    boxes: np.ndarray                 # (N, 4) target boxes
    clutter_boxes: np.ndarray         # (M, 4) clutter boxes (not targets)
    modality: str
    meta: dict = field(default_factory=dict)


def _grid(size):
    yy, xx = np.mgrid[0:size, 0:size].astype(np.float64)
    return xx + 0.5, yy + 0.5


def _background(rng, size, modality):
    tex = ndimage.gaussian_filter(rng.standard_normal((size, size)), rng.uniform(2.0, 6.0))
    tex = tex / (tex.std() + 1e-9)
    xx, yy = _grid(size)
    g = rng.normal(size=2) * 0.1 / size
    if modality == "thermal":
        return 0.35 + 0.03 * tex + g[0] * xx + g[1] * yy
    return rng.uniform(0.35, 0.6) + rng.uniform(0.03, 0.08) * tex + g[0] * xx + g[1] * yy


def _capsule_alpha(xx, yy, cx, cy, length, width, ang):
    """Soft mask of a capsule and the along-axis coordinate u."""
    c, s = np.cos(ang), np.sin(ang)
    dx, dy = xx - cx, yy - cy
    u, v = dx * c + dy * s, -dx * s + dy * c
    h = max(length / 2 - width / 2, 0.0)
    d = np.hypot(np.clip(np.abs(u) - h, 0, None), v)
    return np.clip(width / 2 - d + 0.5, 0, 1), u


def _ellipse_alpha(xx, yy, cx, cy, a, b, ang):
    c, s = np.cos(ang), np.sin(ang)
    dx, dy = xx - cx, yy - cy
    u, v = dx * c + dy * s, -dx * s + dy * c
    r = np.sqrt((u / a) ** 2 + (v / b) ** 2)
    return np.clip((1 - r) * min(a, b) + 0.5, 0, 1)


def _rect_alpha(xx, yy, cx, cy, a, b, ang):
    c, s = np.cos(ang), np.sin(ang)
    dx, dy = xx - cx, yy - cy
    u, v = dx * c + dy * s, -dx * s + dy * c
    return np.clip(np.minimum(a - np.abs(u), b - np.abs(v)) + 0.5, 0, 1)


def _aabb(cx, cy, hx, hy, size):
    return np.array([max(cx - hx, 0), max(cy - hy, 0), min(cx + hx, size), min(cy + hy, size)])


def _draw_target(img, rng, cx, cy, modality, xx, yy):
    length, width = rng.uniform(14, 24), rng.uniform(6, 9)
    ang = rng.uniform(0, np.pi)
    alpha, u = _capsule_alpha(xx, yy, cx, cy, length, width, ang)
    period = rng.uniform(4.0, 6.0)
    bands = np.sign(np.sin(2 * np.pi * u / period + rng.uniform(0, 2 * np.pi)))
    if modality == "thermal":
        val = rng.uniform(0.62, 0.75) + 0.03 * bands
    else:
        base = rng.uniform(0.2, 0.8)
        val = base + rng.uniform(0.08, 0.2) * bands
    img[:] = img * (1 - alpha) + val * alpha
    c, s = abs(np.cos(ang)), abs(np.sin(ang))
    return _aabb(cx, cy, length / 2 * c + width / 2 * s, length / 2 * s + width / 2 * c, img.shape[0])


def _draw_clutter(img, rng, cx, cy, modality, xx, yy, kind=None):
    kind = CLUTTER_KINDS[rng.integers(len(CLUTTER_KINDS))] if kind is None else kind
    ang = rng.uniform(0, np.pi)
    if modality == "thermal":
        temp = rng.uniform(0.25, 0.72)            # some clutter is as warm as the target
    else:
        temp = rng.uniform(0.1, 0.9)
    size = img.shape[0]
    if kind == "rock":
        a, b = rng.uniform(4, 10), rng.uniform(3, 7)
        alpha = _ellipse_alpha(xx, yy, cx, cy, a, b, ang)
        tex = ndimage.gaussian_filter(rng.standard_normal(img.shape), 1.0) * (0.02 if modality == "thermal" else 0.12)
        val, hx, hy = temp + tex, a, a
    elif kind == "disc":
        a = rng.uniform(3, 8)
        alpha = _ellipse_alpha(xx, yy, cx, cy, a, a, 0.0)
        val, hx, hy = temp, a, a
    elif kind == "stick":
        length, width = rng.uniform(15, 30), rng.uniform(2, 3.5)
        alpha, _ = _capsule_alpha(xx, yy, cx, cy, length, width, ang)
        val, hx, hy = temp, length / 2, length / 2
    elif kind == "box":
        a, b = rng.uniform(4, 9), rng.uniform(3, 7)
        alpha = _rect_alpha(xx, yy, cx, cy, a, b, ang)
        val, hx, hy = temp, a + b, a + b
    else:  # plain_capsule: target-like shape, no banding (hard negative)
        length, width = rng.uniform(14, 24), rng.uniform(6, 9)
        alpha, _ = _capsule_alpha(xx, yy, cx, cy, length, width, ang)
        blot = ndimage.gaussian_filter(rng.standard_normal(img.shape), 2.0) * (0.01 if modality == "thermal" else 0.06)
        val, hx, hy = temp + blot, length / 2, length / 2
    img[:] = img * (1 - alpha) + val * alpha
    return _aabb(cx, cy, hx, hy, size), kind


def _sensor(img, rng, modality):
    if modality == "visible":
        out = img + 0.02 * rng.standard_normal(img.shape)
    elif modality == "lowlight":
        gain, photons = 0.2, 150.0                 # 20 % light, ~30 photons at mid-grey
        sig = np.clip(img, 0, 1) * gain
        out = rng.poisson(sig * photons) / photons + 0.01 * rng.standard_normal(img.shape)
        out = out / gain                            # auto-gain amplifies the noise
    else:
        out = ndimage.gaussian_filter(img, 1.2) + 0.012 * rng.standard_normal(img.shape)
    return np.clip(out, 0, 1).astype(np.float32)


def generate_scene(seed: int, size: int = 96, modality: str = "visible", n_targets=None,
                   n_clutter=None) -> Scene:
    """Render one synthetic scene. Fully determined by ``(seed, size, modality, n_targets, n_clutter)``.

    ``n_targets`` defaults to a draw from {0, 1, 2}; ``n_clutter`` from 3..6. Objects are placed
    with a minimum spacing so that they do not overlap heavily.
    """
    if modality not in MODALITIES:
        raise ValueError(modality)
    rng = np.random.default_rng(seed)
    n_t = int(rng.integers(0, 3)) if n_targets is None else n_targets
    n_c = int(rng.integers(3, 7)) if n_clutter is None else n_clutter
    img = _background(rng, size, modality)
    xx, yy = _grid(size)
    centres = []
    for _ in range(n_t + n_c):
        for _ in range(50):
            c = rng.uniform(12, size - 12, 2)
            if all(np.hypot(*(c - o)) > 22 for o in centres):
                break
        centres.append(c)
    order = rng.permutation(n_t + n_c)
    boxes, cboxes, kinds = [], [], []
    for k in order:
        cx, cy = centres[k]
        if k < n_t:
            boxes.append(_draw_target(img, rng, cx, cy, modality, xx, yy))
        else:
            b, kind = _draw_clutter(img, rng, cx, cy, modality, xx, yy)
            cboxes.append(b)
            kinds.append(kind)
    img = _sensor(img, rng, modality)
    return Scene(img, np.array(boxes).reshape(-1, 4), np.array(cboxes).reshape(-1, 4), modality,
                 {"seed": seed, "clutter_kinds": kinds})


def generate_dataset(n: int, seed: int = 0, size: int = 96, modality: str = "visible") -> list[Scene]:
    """``n`` scenes with seeds derived deterministically from ``seed``."""
    seeds = np.random.default_rng(seed).integers(0, 2**31 - 1, n)
    return [generate_scene(int(s), size, modality) for s in seeds]


def make_patch_dataset(n: int, seed: int = 0, patch: int = 32, modality: str = "visible",
                       jitter: float = 3.0) -> tuple[np.ndarray, np.ndarray]:
    """Balanced classification set of ``patch x patch`` crops: label 1 = target centred (with
    +-jitter px), label 0 = clutter (80 %) or bare background (20 %). Returns ``(X (n,p,p), y (n,))``."""
    rng = np.random.default_rng(seed)
    xx, yy = _grid(patch)
    X, y = np.zeros((n, patch, patch), np.float32), np.zeros(n, int)
    for i in range(n):
        img = _background(rng, patch, modality)
        c = patch / 2 + rng.uniform(-jitter, jitter, 2)
        lab = i % 2
        if lab:
            _draw_target(img, rng, c[0], c[1], modality, xx, yy)
        elif rng.uniform() < 0.8:
            _draw_clutter(img, rng, c[0], c[1], modality, xx, yy)
        X[i], y[i] = _sensor(img, rng, modality), lab
    p = rng.permutation(n)
    return X[p], y[p]


def crop_patch(image: np.ndarray, cx: float, cy: float, size: int = 32) -> np.ndarray:
    """Square crop centred on (cx, cy) with reflect padding at the borders."""
    pad = size
    im = np.pad(image, pad, mode="reflect")
    x0, y0 = int(round(cx - size / 2)) + pad, int(round(cy - size / 2)) + pad
    return im[y0:y0 + size, x0:x0 + size]


# =============================================================================================
# 2. Geometry
# =============================================================================================


def iou(a, b) -> float:
    """Intersection over union of two boxes (x1, y1, x2, y2). Disjoint boxes give 0."""
    iw = max(0.0, min(a[2], b[2]) - max(a[0], b[0]))
    ih = max(0.0, min(a[3], b[3]) - max(a[1], b[1]))
    inter = iw * ih
    union = (a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - inter
    return float(inter / union) if union > 0 else 0.0


def iou_matrix(A: np.ndarray, B: np.ndarray) -> np.ndarray:
    """Vectorised pairwise IoU, shape (len(A), len(B))."""
    A, B = np.asarray(A, float).reshape(-1, 4), np.asarray(B, float).reshape(-1, 4)
    iw = np.clip(np.minimum(A[:, None, 2], B[None, :, 2]) - np.maximum(A[:, None, 0], B[None, :, 0]), 0, None)
    ih = np.clip(np.minimum(A[:, None, 3], B[None, :, 3]) - np.maximum(A[:, None, 1], B[None, :, 1]), 0, None)
    inter = iw * ih
    area = lambda X: (X[:, 2] - X[:, 0]) * (X[:, 3] - X[:, 1])
    union = area(A)[:, None] + area(B)[None, :] - inter
    return np.where(union > 0, inter / np.where(union > 0, union, 1), 0.0)


def nms(boxes: np.ndarray, scores: np.ndarray, iou_thr: float = 0.5) -> np.ndarray:
    """Greedy non-maximum suppression. Returns indices of kept boxes, highest score first.

    Keep the highest-scoring remaining box, delete every remaining box whose IoU with it exceeds
    ``iou_thr`` (strictly greater), repeat. Ties in score are broken by original index.
    """
    boxes, scores = np.asarray(boxes, float).reshape(-1, 4), np.asarray(scores, float)
    order = np.argsort(-scores, kind="stable")
    keep = []
    while order.size:
        i = order[0]
        keep.append(int(i))
        if order.size == 1:
            break
        ious = iou_matrix(boxes[i:i + 1], boxes[order[1:]])[0]
        order = order[1:][ious <= iou_thr]
    return np.array(keep, int)


# =============================================================================================
# 3. Evaluation
# =============================================================================================


def match_detections(det_boxes, det_scores, gt_boxes, iou_thr: float = 0.3) -> np.ndarray:
    """Greedy one-to-one matching in descending score order (ties: original index).

    A detection is a true positive if its best-IoU *unmatched* ground truth has IoU >= ``iou_thr``;
    that GT is then consumed. Duplicates on an already-matched GT are false positives.
    Returns a boolean array aligned with ``det_boxes``.
    """
    det_boxes = np.asarray(det_boxes, float).reshape(-1, 4)
    gt_boxes = np.asarray(gt_boxes, float).reshape(-1, 4)
    tp = np.zeros(len(det_boxes), bool)
    if len(det_boxes) == 0 or len(gt_boxes) == 0:
        return tp
    M = iou_matrix(det_boxes, gt_boxes)
    used = np.zeros(len(gt_boxes), bool)
    for i in np.argsort(-np.asarray(det_scores, float), kind="stable"):
        cand = np.where(used, -1.0, M[i])
        j = int(np.argmax(cand))
        if cand[j] >= iou_thr:
            tp[i], used[j] = True, True
    return tp


def froc_curve(detections: list, ground_truth: list, iou_thr: float = 0.3) -> dict:
    """Free-response ROC over a set of images.

    ``detections[k] = (boxes (n_k, 4), scores (n_k,))`` and ``ground_truth[k] = boxes (m_k, 4)``.
    Match each image once with :func:`match_detections`; pool all detections, sort by score
    descending, and at every *distinct* score threshold t (detections with score >= t kept) report
    ``sensitivity = TP(t) / total GT`` and ``fppi = FP(t) / n_images``.
    Returns ``{"thresholds", "sensitivity", "fppi", "n_gt", "n_images"}`` (arrays in the order of
    decreasing threshold). An empty detection set yields empty arrays.
    """
    scores, flags = [], []
    n_gt = 0
    for (b, s), g in zip(detections, ground_truth):
        s = np.asarray(s, float).reshape(-1)
        scores.append(s)
        flags.append(match_detections(b, s, g, iou_thr))
        n_gt += len(np.asarray(g).reshape(-1, 4))
    s = np.concatenate(scores) if scores else np.zeros(0)
    f = np.concatenate(flags) if flags else np.zeros(0, bool)
    order = np.argsort(-s, kind="stable")
    s, f = s[order], f[order]
    ctp, cfp = np.cumsum(f), np.cumsum(~f)
    last = np.r_[s[1:] != s[:-1], True] if len(s) else np.zeros(0, bool)   # end of each tie group
    n_img = len(ground_truth)
    return {"thresholds": s[last], "sensitivity": ctp[last] / max(n_gt, 1), "fppi": cfp[last] / max(n_img, 1),
            "n_gt": n_gt, "n_images": n_img}


def recall_at_fppi(curve: dict, fppi_max: float) -> float:
    """Highest sensitivity among operating points with ``fppi <= fppi_max`` (0 if none)."""
    ok = np.asarray(curve["fppi"]) <= fppi_max + 1e-12
    return float(np.max(np.asarray(curve["sensitivity"])[ok])) if ok.any() else 0.0


def froc_score(curve: dict, fppi_points=(0.5, 1.0, 2.0, 4.0)) -> float:
    """Mean of :func:`recall_at_fppi` over the predefined FPPI points (lesson 09.1 section 7.3)."""
    return float(np.mean([recall_at_fppi(curve, f) for f in fppi_points]))


def softmax(z: np.ndarray, T: float = 1.0) -> np.ndarray:
    """Row-wise softmax of logits divided by temperature T (numerically stable)."""
    z = np.asarray(z, float) / T
    z = z - z.max(axis=1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(axis=1, keepdims=True)


def nll(logits: np.ndarray, labels: np.ndarray, T: float = 1.0) -> float:
    """Mean negative log-likelihood of ``labels`` under ``softmax(logits / T)``."""
    z = np.asarray(logits, float) / T
    zmax = z.max(axis=1, keepdims=True)
    lse = (zmax + np.log(np.exp(z - zmax).sum(axis=1, keepdims=True)))[:, 0]
    return float(np.mean(lse - z[np.arange(len(z)), labels]))


def ece(probs: np.ndarray, labels: np.ndarray, n_bins: int = 15) -> float:
    """Top-label expected calibration error with ``n_bins`` equal-width bins on (0, 1].

    ``ECE = sum_b |S_b|/n * |acc(S_b) - conf(S_b)|`` where conf is the max probability and acc
    the fraction whose argmax equals the label. A confidence c falls in bin ``ceil(c*B) - 1``
    (clipped to [0, B-1]).
    """
    probs = np.asarray(probs, float)
    conf, pred = probs.max(1), probs.argmax(1)
    correct = (pred == np.asarray(labels)).astype(float)
    b = np.clip(np.ceil(conf * n_bins).astype(int) - 1, 0, n_bins - 1)
    total = 0.0
    for k in range(n_bins):
        m = b == k
        if m.any():
            total += m.mean() * abs(correct[m].mean() - conf[m].mean())
    return float(total)


def reliability_curve(probs: np.ndarray, labels: np.ndarray, n_bins: int = 15) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """(mean confidence, accuracy, count) per non-empty bin, for plotting (given)."""
    probs = np.asarray(probs, float)
    conf, correct = probs.max(1), (probs.argmax(1) == np.asarray(labels)).astype(float)
    b = np.clip(np.ceil(conf * n_bins).astype(int) - 1, 0, n_bins - 1)
    ks = [k for k in range(n_bins) if np.any(b == k)]
    return (np.array([conf[b == k].mean() for k in ks]), np.array([correct[b == k].mean() for k in ks]),
            np.array([(b == k).sum() for k in ks]))


def fit_temperature(logits: np.ndarray, labels: np.ndarray) -> float:
    """Temperature scaling: ``T* = argmin_T nll(logits, labels, T)``.

    NLL is convex in beta = 1/T, so a bounded 1-D search over log T (e.g. [-3, 3]) with
    ``scipy.optimize.minimize_scalar`` is reliable. Returns T > 0.
    """
    res = minimize_scalar(lambda lt: nll(logits, labels, np.exp(lt)), bounds=(-3, 3), method="bounded",
                          options={"xatol": 1e-6})
    return float(np.exp(res.x))


# =============================================================================================
# 4. Classical baseline
# =============================================================================================


def orientation_histograms(patch: np.ndarray, cells: int = 4, bins: int = 8) -> np.ndarray:
    """HOG-like feature: unsigned gradient-orientation histograms (magnitude-weighted) on a
    ``cells x cells`` grid, globally L2-normalised. Length ``cells*cells*bins``."""
    p = np.asarray(patch, float)
    gy, gx = np.gradient(p)
    mag, ang = np.hypot(gx, gy), np.mod(np.arctan2(gy, gx), np.pi)
    bidx = np.minimum((ang / np.pi * bins).astype(int), bins - 1)
    H, W = p.shape
    ci = np.minimum((np.arange(H) * cells) // H, cells - 1)
    cj = np.minimum((np.arange(W) * cells) // W, cells - 1)
    cell_id = ci[:, None] * cells + cj[None, :]
    feat = np.bincount((cell_id * bins + bidx).ravel(), weights=mag.ravel(), minlength=cells * cells * bins)
    return feat / (np.linalg.norm(feat) + 1e-9)


def band_energy(patch: np.ndarray, n_bands: int = 8) -> np.ndarray:
    """Fraction of (mean-removed) spectral energy in ``n_bands`` radial frequency bands up to
    Nyquist. Banded surfaces put energy in the 4-6 px period band."""
    p = np.asarray(patch, float)
    F = np.abs(np.fft.fftshift(np.fft.fft2(p - p.mean()))) ** 2
    H, W = p.shape
    fy, fx = np.meshgrid(np.fft.fftshift(np.fft.fftfreq(H)), np.fft.fftshift(np.fft.fftfreq(W)), indexing="ij")
    r = np.hypot(fx, fy) / 0.5
    idx = np.minimum((r * n_bands).astype(int), n_bands)
    e = np.bincount(idx.ravel(), weights=F.ravel(), minlength=n_bands + 1)[:n_bands]
    return e / (e.sum() + 1e-12)


def handcrafted_features(patch: np.ndarray) -> np.ndarray:
    """Feature vector for one patch: orientation histograms of the contrast-normalised patch,
    band energy of the central region, and centre/surround intensity statistics."""
    p = np.asarray(patch, float)
    z = (p - p.mean()) / (p.std() + 1e-3)
    H, W = p.shape
    c = p[H // 4: 3 * H // 4, W // 4: 3 * W // 4]
    ring = np.ones_like(p, bool)
    ring[H // 4: 3 * H // 4, W // 4: 3 * W // 4] = False
    stats = np.array([c.mean() - p[ring].mean(), c.std(), p.std(), c.mean(),
                      np.abs(np.diff(c, axis=0)).mean(), np.abs(np.diff(c, axis=1)).mean()])
    return np.concatenate([orientation_histograms(z), band_energy(c), stats])


def extract_features(X: np.ndarray) -> np.ndarray:
    """Stack :func:`handcrafted_features` over a batch of patches (given)."""
    return np.stack([handcrafted_features(x) for x in X])


class LogisticRegression:
    """Binary L2-regularised logistic regression, numpy only.

    ``p(y=1|x) = sigmoid(w.x + b)``. ``fit`` standardises the features (stores mean/std) and
    minimises ``mean(log-loss) + l2/2 * |w|^2`` (bias unpenalised) by Newton's method / IRLS.
    """

    def __init__(self, l2: float = 1e-2, max_iter: int = 50, tol: float = 1e-8):
        self.l2, self.max_iter, self.tol = l2, max_iter, tol
        self.w = self.b = self.mu = self.sd = None

    def _prep(self, X):
        return (np.asarray(X, float) - self.mu) / self.sd

    def fit(self, X: np.ndarray, y: np.ndarray) -> "LogisticRegression":
        X = np.asarray(X, float)
        y = np.asarray(y, float)
        self.mu, self.sd = X.mean(0), X.std(0) + 1e-9
        Z = np.c_[self._prep(X), np.ones(len(X))]
        d = Z.shape[1]
        theta = np.zeros(d)
        R = self.l2 * np.eye(d)
        R[-1, -1] = 0.0
        n = len(y)
        for _ in range(self.max_iter):
            p = 1 / (1 + np.exp(-(Z @ theta)))
            g = Z.T @ (p - y) / n + R @ theta
            Hm = (Z * (p * (1 - p))[:, None]).T @ Z / n + R + 1e-10 * np.eye(d)
            step = np.linalg.solve(Hm, g)
            theta -= step
            if np.abs(step).max() < self.tol:
                break
        self.w, self.b = theta[:-1], theta[-1]
        return self

    def decision_function(self, X: np.ndarray) -> np.ndarray:
        """Logit ``w.x_std + b``."""
        return self._prep(X) @ self.w + self.b

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """P(y = 1 | x)."""
        return 1 / (1 + np.exp(-self.decision_function(X)))


def propose_regions(image: np.ndarray, k: float = 2.0, min_area: int = 15, max_area: int = 1200,
                    use_edges: bool = True) -> np.ndarray:
    """Class-agnostic proposals with OpenCV (given; requires ``cv2``).

    Background model: heavy median blur. Foreground: ``|denoised - background| > mean + k*std``,
    optionally OR-ed with a closed Canny edge map (visible imagery). Morphological open/close,
    connected components, area filter, 2 px padding. Returns boxes (N, 4).
    """
    import cv2
    img = (np.clip(image, 0, 1) * 255).astype(np.uint8)
    den = cv2.GaussianBlur(img, (5, 5), 1.2)
    bg = cv2.medianBlur(den, 31)
    diff = cv2.absdiff(den, bg).astype(np.float32)
    mask = (diff > diff.mean() + k * diff.std()).astype(np.uint8)
    if use_edges:
        edges = cv2.Canny(den, 60, 140)
        mask |= (cv2.morphologyEx(edges, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8)) > 0).astype(np.uint8)
    kern = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kern)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    n, _, st, _ = cv2.connectedComponentsWithStats(mask, connectivity=8)
    H, W = image.shape
    boxes = []
    for i in range(1, n):
        x, y, w, h, a = st[i]
        if min_area <= a <= max_area:
            boxes.append([max(x - 2, 0), max(y - 2, 0), min(x + w + 2, W), min(y + h + 2, H)])
    return np.array(boxes, float).reshape(-1, 4)


def _patches_for(image, boxes, patch):
    return np.stack([crop_patch(image, (b[0] + b[2]) / 2, (b[1] + b[3]) / 2, patch) for b in boxes]) \
        if len(boxes) else np.zeros((0, patch, patch), np.float32)


class ClassicalDetector:
    """Proposals (:func:`propose_regions`) scored by handcrafted features + :class:`LogisticRegression`,
    followed by NMS (given; the parts it calls are yours)."""

    def __init__(self, patch: int = 32, l2: float = 1e-2, nms_iou: float = 0.3):
        self.patch, self.nms_iou = patch, nms_iou
        self.clf = LogisticRegression(l2=l2)

    def fit(self, X: np.ndarray, y: np.ndarray) -> "ClassicalDetector":
        self.clf.fit(extract_features(X), y)
        return self

    def score_patches(self, X: np.ndarray) -> np.ndarray:
        return self.clf.predict_proba(extract_features(X)) if len(X) else np.zeros(0)

    def detect(self, image: np.ndarray, use_edges: bool | None = None) -> tuple[np.ndarray, np.ndarray]:
        boxes = propose_regions(image, use_edges=True if use_edges is None else use_edges)
        s = self.score_patches(_patches_for(image, boxes, self.patch))
        keep = nms(boxes, s, self.nms_iou) if len(boxes) else np.zeros(0, int)
        return boxes[keep], s[keep]


# =============================================================================================
# 5. Small CNN (PyTorch, CPU)
# =============================================================================================


def build_cnn(n_classes: int = 2, width: int = 8):
    """A small CNN for 32x32 single-channel patches:
    conv3x3(1->w)-BN-ReLU-maxpool, conv3x3(w->2w)-BN-ReLU-maxpool, conv3x3(2w->4w)-BN-ReLU,
    global average pool, linear(4w -> n_classes). Returns a ``torch.nn.Module`` producing logits."""
    if nn is None:
        raise ImportError("PyTorch is required for build_cnn")
    w = width
    return nn.Sequential(
        nn.Conv2d(1, w, 3, padding=1), nn.BatchNorm2d(w), nn.ReLU(), nn.MaxPool2d(2),
        nn.Conv2d(w, 2 * w, 3, padding=1), nn.BatchNorm2d(2 * w), nn.ReLU(), nn.MaxPool2d(2),
        nn.Conv2d(2 * w, 4 * w, 3, padding=1), nn.BatchNorm2d(4 * w), nn.ReLU(),
        nn.AdaptiveAvgPool2d(1), nn.Flatten(), nn.Linear(4 * w, n_classes))


def _to_tensor(X):
    X = np.asarray(X, np.float32)
    X = (X - X.mean(axis=(1, 2), keepdims=True)) / (X.std(axis=(1, 2), keepdims=True) + 1e-3)
    return torch.from_numpy(X[:, None])


def train_cnn(X: np.ndarray, y: np.ndarray, epochs: int = 10, batch: int = 64, lr: float = 3e-3,
              width: int = 8, seed: int = 0, augment: bool = True, threads: int | None = 2):
    """Train :func:`build_cnn` with Adam and cross-entropy on per-patch standardised inputs.

    Deterministic under ``seed`` (``torch.manual_seed`` and a numpy generator for shuffling).
    Augmentation: random 90-degree rotations and flips (the target has no preferred orientation).
    ``threads`` caps PyTorch CPU threads while training (small models on many cores are slowed
    down, not sped up, by thread oversubscription); the previous setting is restored.
    Returns the model in eval mode.
    """
    old_threads = torch.get_num_threads()
    if threads:
        torch.set_num_threads(threads)
    torch.manual_seed(seed)
    rng = np.random.default_rng(seed)
    model = build_cnn(2, width)
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    Xt, yt = _to_tensor(X), torch.from_numpy(np.asarray(y, np.int64))
    loss_fn = nn.CrossEntropyLoss()
    for _ in range(epochs):
        model.train()
        perm = rng.permutation(len(Xt))
        for i in range(0, len(perm), batch):
            idx = torch.from_numpy(perm[i:i + batch])
            xb, yb = Xt[idx], yt[idx]
            if augment:
                xb = torch.rot90(xb, int(rng.integers(4)), dims=(2, 3))
                if rng.uniform() < 0.5:
                    xb = torch.flip(xb, dims=(3,))
            opt.zero_grad()
            loss = loss_fn(model(xb), yb)
            loss.backward()
            opt.step()
    torch.set_num_threads(old_threads)
    return model.eval()


def cnn_logits(model, X: np.ndarray, batch: int = 512) -> np.ndarray:
    """Logits (n, 2) for a batch of patches, as numpy."""
    out = []
    with torch.no_grad():
        for i in range(0, len(X), batch):
            out.append(model(_to_tensor(X[i:i + batch])).numpy())
    return np.concatenate(out) if out else np.zeros((0, 2))


class CNNDetector:
    """Same proposals as :class:`ClassicalDetector`, scored by the CNN with temperature ``T`` (given)."""

    def __init__(self, model, T: float = 1.0, patch: int = 32, nms_iou: float = 0.3):
        self.model, self.T, self.patch, self.nms_iou = model, T, patch, nms_iou

    def score_patches(self, X):
        return softmax(cnn_logits(self.model, X), self.T)[:, 1] if len(X) else np.zeros(0)

    def detect(self, image, use_edges: bool | None = None):
        boxes = propose_regions(image, use_edges=True if use_edges is None else use_edges)
        s = self.score_patches(_patches_for(image, boxes, self.patch))
        keep = nms(boxes, s, self.nms_iou) if len(boxes) else np.zeros(0, int)
        return boxes[keep], s[keep]


# =============================================================================================
# Benchmark (given)
# =============================================================================================


def evaluate_detector(detector, scenes: list[Scene], iou_thr: float = 0.3) -> dict:
    """FROC of ``detector.detect`` over ``scenes`` plus recall at 0.5/1/2 FPPI and the FROC score."""
    use_edges = scenes[0].modality == "visible" if scenes else True
    dets = [detector.detect(s.image, use_edges=use_edges) for s in scenes]
    curve = froc_curve(dets, [s.boxes for s in scenes], iou_thr)
    curve.update({f"recall@{f}fppi": recall_at_fppi(curve, f) for f in (0.5, 1.0, 2.0)})
    curve["froc_score"] = froc_score(curve)
    return curve


def run_benchmark(outdir: str = "p09_out", n_train: int = 2000, n_scenes: int = 100, epochs: int = 10,
                  seed: int = 0) -> dict:
    """Train both detectors per modality, evaluate FROC on held-out scenes, calibrate the CNN on a
    held-out patch set, and write ``froc.png``, ``reliability.png`` and ``report.md`` (given)."""
    import os
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    os.makedirs(outdir, exist_ok=True)
    report, figF, axF = {}, *plt.subplots(1, 3, figsize=(16, 4.5))
    figR, axR = plt.subplots(1, 3, figsize=(16, 4.5))
    for m_i, mod in enumerate(MODALITIES):
        Xtr, ytr = make_patch_dataset(n_train, seed + 1, modality=mod)
        Xca, yca = make_patch_dataset(n_train // 3, seed + 2, modality=mod)
        scenes = generate_dataset(n_scenes, seed + 3, modality=mod)
        det_c = ClassicalDetector().fit(Xtr, ytr)
        res = {"classical": evaluate_detector(det_c, scenes)}
        if torch is not None:
            model = train_cnn(Xtr, ytr, epochs=epochs, seed=seed)
            z = cnn_logits(model, Xca)
            T = fit_temperature(z, yca)
            res["cnn"] = evaluate_detector(CNNDetector(model, T), scenes)
            res["cnn"].update({"T": T, "ece_before": ece(softmax(z), yca), "ece_after": ece(softmax(z, T), yca),
                               "acc_patch": float((z.argmax(1) == yca).mean())})
            for TT, lab in [(1.0, "T = 1"), (T, f"T = {T:.2f}")]:
                c, a, _ = reliability_curve(softmax(z, TT), yca)
                axR[m_i].plot(c, a, "o-", label=lab)
            axR[m_i].plot([0.5, 1], [0.5, 1], "k--"); axR[m_i].legend(); axR[m_i].set_title(f"CNN reliability ({mod})")
            axR[m_i].set_xlabel("confidence"); axR[m_i].set_ylabel("accuracy")
        for name, r in res.items():
            axF[m_i].plot(r["fppi"], r["sensitivity"], label=f"{name} (FROC {r['froc_score']:.2f})")
        axF[m_i].set_xlim(0, 4); axF[m_i].set_ylim(0, 1); axF[m_i].set_title(f"FROC ({mod})")
        axF[m_i].set_xlabel("false positives per image"); axF[m_i].set_ylabel("sensitivity"); axF[m_i].legend()
        report[mod] = res
    figF.tight_layout(); figF.savefig(os.path.join(outdir, "froc.png"), dpi=110)
    figR.tight_layout(); figR.savefig(os.path.join(outdir, "reliability.png"), dpi=110)
    plt.close("all")
    lines = ["# P09 evaluation report", "", "| modality | detector | recall@0.5 | recall@1 | recall@2 | FROC score |",
             "|---|---|---|---|---|---|"]
    for mod, res in report.items():
        for name, r in res.items():
            lines.append(f"| {mod} | {name} | {r['recall@0.5fppi']:.2f} | {r['recall@1.0fppi']:.2f} | "
                         f"{r['recall@2.0fppi']:.2f} | {r['froc_score']:.2f} |")
    if torch is not None:
        lines += ["", "| modality | CNN patch acc | T | ECE before | ECE after |", "|---|---|---|---|---|"]
        for mod, res in report.items():
            c = res["cnn"]
            lines.append(f"| {mod} | {c['acc_patch']:.3f} | {c['T']:.2f} | {c['ece_before']:.3f} | {c['ece_after']:.3f} |")
    with open(os.path.join(outdir, "report.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    return report


if __name__ == "__main__":
    import time
    t0 = time.time()
    rep = run_benchmark()
    print(open("p09_out/report.md", encoding="utf-8").read())
    print(f"total {time.time() - t0:.1f} s")
