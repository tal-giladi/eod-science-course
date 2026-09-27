"""bayesfusion — log-odds grid fusion, correlated errors and information-driven sensor scheduling
for Project P03.

STARTER. Implement every function whose body is `raise NotImplementedError`. Functions that
are already implemented are PROVIDED helpers (not the learning goal) — use them freely.

Setting (lesson 05.6): a search area is a grid of cells; each cell either holds a (fictional)
object of interest (X = 1) or not (X = 0). Sensors return binary alarms (Pd, Pf) or continuous
scores (Gaussian, mean 0 under H0 and mu under H1). Beliefs are stored as log-odds in nats.
Entropies and information gains are in bits.

Conventions
    p          probability that X = 1
    l          log-odds ln(p / (1 − p))   [nats]
    LLR        ln p(z | X=1) − ln p(z | X=0)   [nats]
    rng        a numpy.random.Generator
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy import stats


# ---------------------------------------------------------------------------------------------
# 0. Helpers (PROVIDED)
# ---------------------------------------------------------------------------------------------
def logit(p):
    """ln(p / (1 − p))."""
    p = np.asarray(p, dtype=float)
    return np.log(p) - np.log1p(-p)


def sigmoid(l):
    """1 / (1 + e^−l), numerically stable."""
    l = np.asarray(l, dtype=float)
    return np.exp(-np.logaddexp(0.0, -l))


def binary_entropy(p):
    """H_b(p) = −p log2 p − (1−p) log2(1−p) in bits (0 at p ∈ {0, 1})."""
    p = np.clip(np.asarray(p, dtype=float), 1e-300, 1.0)
    q = np.clip(1.0 - np.asarray(p, dtype=float), 1e-300, 1.0)
    return -(p * np.log2(p) + q * np.log2(q))


@dataclass(frozen=True)
class Sensor:
    """A binary-alarm sensor: P(alarm | X=1) = pd, P(alarm | X=0) = pf, cost per reading."""
    name: str
    pd: float
    pf: float
    cost: float = 1.0


def simulate_reading(x, sensor: Sensor, rng):
    """Draw an alarm (bool) for a cell with true state ``x`` (PROVIDED; conditionally independent)."""
    return bool(rng.random() < (sensor.pd if x else sensor.pf))


def simulate_correlated_scores(truth, mu, cov, rng):
    """Scores of N Gaussian sensors at each location (PROVIDED).

    s = mu · X + e,  e ~ N(0, cov) shared structure under both hypotheses.
    ``truth`` (n,) bool, ``mu`` (N,), ``cov`` (N, N). Returns (n, N).
    """
    truth = np.asarray(truth, dtype=bool)
    mu = np.asarray(mu, dtype=float)
    e = rng.multivariate_normal(np.zeros(mu.size), cov, size=truth.size)
    return truth[:, None] * mu[None, :] + e


def equicorr_cov(n, rho, sd=1.0):
    """Equicorrelated covariance sd² [(1−ρ) I + ρ 11ᵀ] (PROVIDED)."""
    return sd ** 2 * ((1 - rho) * np.eye(n) + rho * np.ones((n, n)))


# ---------------------------------------------------------------------------------------------
# 1. Bayes in log-odds form and inverse sensor models
# ---------------------------------------------------------------------------------------------
def fuse_ci(p0, lrs):
    """Posterior P(X=1 | readings) under conditional independence: σ(logit p0 + Σ ln LR_i)."""
    raise NotImplementedError


def llr_binary(z, pd, pf):
    """LLR of a binary reading: ln(pd/pf) for an alarm, ln((1−pd)/(1−pf)) for silence."""
    raise NotImplementedError


def llr_gaussian(s, mu, sd=1.0):
    """LLR of a Gaussian score (H0: N(0, sd²), H1: N(mu, sd²)): (mu s − mu²/2) / sd²."""
    raise NotImplementedError


def footprint_llr(z, pd, pf, kernel):
    """Inverse sensor model with a spatial footprint.

    ``kernel`` holds weights w ∈ [0, 1] (1 at the aim point). A cell at weight w is detected with
    P(alarm | X_c = 1) = pf + w (pd − pf), so the LLR for that cell is
        alarm:   ln[(pf + w(pd − pf)) / pf]
        silence: ln[(1 − pf − w(pd − pf)) / (1 − pf)]
    (0 where w = 0). Treats cells as independent — the usual occupancy-grid approximation.
    """
    raise NotImplementedError


class LogOddsGrid:
    """Occupancy-style grid of log-odds with clamping.

    Parameters
    ----------
    prior : ndarray
        Prior probability map (any shape, typically 2-D).
    lmin, lmax : float
        Clamps on the log-odds [nats] that keep the grid responsive.
    """

    def __init__(self, prior, lmin: float = -8.0, lmax: float = 8.0):
        self.l = logit(np.asarray(prior, dtype=float)).copy()
        self.lmin, self.lmax = lmin, lmax

    def update(self, llr, center=None):
        """Add evidence and clamp.

        If ``center`` is None, ``llr`` must have the grid's shape. Otherwise ``llr`` is a kernel
        with odd dimensions, centred on index ``center``; parts falling outside the grid are
        ignored.
        """
        raise NotImplementedError

    def posterior(self):
        """Probability map σ(l)."""
        return sigmoid(self.l)

    def entropy(self):
        """Per-cell entropy map [bits]."""
        return binary_entropy(self.posterior())


# ---------------------------------------------------------------------------------------------
# 2. Correlated errors: naive independence vs the joint Gaussian likelihood
# ---------------------------------------------------------------------------------------------
def llr_naive(s, mu, cov):
    """Naive-Bayes LLR: Σ_i (mu_i s_i − mu_i²/2)/σ_i², using only the diagonal of ``cov``.

    ``s`` may be (N,) or (n, N); returns a scalar or (n,).
    """
    raise NotImplementedError


def llr_joint(s, mu, cov):
    """Exact LLR of a joint Gaussian with shared covariance: μᵀC⁻¹s − ½ μᵀC⁻¹μ."""
    raise NotImplementedError


def fuse_scores(prior, S, mu, cov, method: str = "joint"):
    """Posterior per location from a score matrix ``S`` (n, N) using ``method`` ∈ {"joint", "naive"}."""
    raise NotImplementedError


def overconfidence_factor(n, rho):
    """For equicorrelated equal sensors the naive LLR is exactly 1 + (n − 1)ρ times the true LLR."""
    raise NotImplementedError


# ---------------------------------------------------------------------------------------------
# 3. Expected information gain
# ---------------------------------------------------------------------------------------------
def info_gain_binary(p, pd, pf):
    """Mutual information I(X; Z) [bits] of one binary reading, by exact enumeration of z ∈ {0, 1}.

    I = H_b(p·pd + (1−p)·pf) − [p H_b(pd) + (1−p) H_b(pf)]. Vectorised over ``p``.
    Always 0 <= I <= H_b(p).
    """
    raise NotImplementedError


def info_gain_gaussian(p, mu, sd=1.0, n_grid: int = 4001):
    """Mutual information I(X; S) [bits] of one Gaussian score (H0: N(0, sd²), H1: N(mu, sd²)).

    I = H_b(p) − E_S[H_b(P(X=1 | S))], the expectation by trapezoidal quadrature on a grid
    spanning ±10 sd around both means.
    """
    raise NotImplementedError


# ---------------------------------------------------------------------------------------------
# 4. Scheduling
# ---------------------------------------------------------------------------------------------
def run_schedule(prior, truth, sensors, budget, policy: str = "greedy", rng=None,
                 lmin: float = -8.0, lmax: float = 8.0, min_gain: float = 1e-9):
    """Spend ``budget`` on single-cell readings and fuse them into a log-odds grid.

    Each step chooses one (sensor, cell) pair whose cost fits the remaining budget:
      * ``"greedy"``: maximise info_gain_binary(p_cell, pd, pf) / cost; stop when the best
        gain per cost is <= ``min_gain``.
      * ``"random"``: uniformly random affordable sensor and cell.
    The reading is drawn with :func:`simulate_reading` from ``truth`` and fused with
    :func:`llr_binary`. Stops when no sensor is affordable.

    Returns dict(posterior, log, spent) where ``log`` is a list of
    (sensor_name, cell_index_tuple, alarm, gain_bits, cost).
    """
    raise NotImplementedError


# ---------------------------------------------------------------------------------------------
# 5. Evaluation
# ---------------------------------------------------------------------------------------------
def brier(p, y):
    """Mean squared error of probabilities against 0/1 outcomes."""
    raise NotImplementedError


def log_loss(p, y, eps: float = 1e-12):
    """Mean negative log-likelihood [nats] with p clipped to [eps, 1 − eps]."""
    raise NotImplementedError


def roc_auc(p, y):
    """AUC of a fused map as a detector: Mann–Whitney with mid-ranks for ties."""
    raise NotImplementedError


def calibration_curve(p, y, n_bins: int = 10):
    """Reliability diagram data on equal-width bins of [0, 1].

    Returns (mean_predicted, observed_frequency, counts), one entry per non-empty bin.
    """
    raise NotImplementedError
