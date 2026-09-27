"""sensornoise — stochastic sensor models, Monte-Carlo ROC and trial statistics for Project P02.

REFERENCE SOLUTION. Open only after you have attempted the starter.

Scope: generic detection-theory models of a sensor that produces a scalar *score* per location
(lesson 05.1) plus spatial clutter (false alarms per m²) and range-dependent SNR. The sensor
physics of 05.2–05.5 (EMI, GPR, X-ray, trace, thermal) enters only through the parameters of
these models; no real system's performance is claimed. Targets are fictional.

Conventions
    scores     larger = more target-like; H0 = no target, H1 = target present
    Pd, Pfa    probability of detection / of false alarm at a threshold
    conf       two-sided confidence level, e.g. 0.95
    rng        a numpy.random.Generator (pass one in; every function is reproducible)
"""
from __future__ import annotations

import math

import numpy as np
from scipy import stats


def _rng(rng):
    return rng if isinstance(rng, np.random.Generator) else np.random.default_rng(rng)


# ---------------------------------------------------------------------------------------------
# 1. Sensor models
# ---------------------------------------------------------------------------------------------
class GaussianSensor:
    """Score sensor with a persistent per-location bias plus fresh per-look noise.

    Score of look r at location j:
        s_jr = mu_H + b_j + e_jr,   b_j ~ N(0, (k_H·bias_sd)²)  (drawn once per location),
                                    e_jr ~ N(0, (k_H·noise_sd)²) (drawn for every look),
    with mu_H = mu0 or mu1 and k_H = 1 under H0, ``h1_scale`` under H1.

    The bias models everything that belongs to the *place* rather than to the look: soil,
    a nearby clutter object, geometry. Repeating a look averages the noise but never the bias.

    Parameters
    ----------
    mu0, mu1 : float   mean score without / with target
    noise_sd : float   standard deviation of the fresh noise under H0
    bias_sd  : float   standard deviation of the persistent per-location bias under H0
    h1_scale : float   ratio of H1 to H0 standard deviations (σ in the binormal model)
    """

    def __init__(self, mu0=0.0, mu1=2.0, noise_sd=1.0, bias_sd=0.0, h1_scale=1.0):
        self.mu0, self.mu1 = float(mu0), float(mu1)
        self.noise_sd, self.bias_sd, self.h1_scale = float(noise_sd), float(bias_sd), float(h1_scale)

    @property
    def sd0(self) -> float:
        """Total single-look standard deviation under H0: sqrt(bias_sd² + noise_sd²)."""
        return math.hypot(self.bias_sd, self.noise_sd)

    @property
    def d_prime(self) -> float:
        """Single-look detectability d' = (mu1 − mu0)/sd0."""
        return (self.mu1 - self.mu0) / self.sd0

    def measure(self, truth, n_repeats: int = 1, rng=None):
        """Scores for locations with boolean ``truth`` (True = target), shape (n_loc, n_repeats).

        One bias per location (shared by all its repeats), fresh noise per look.
        """
        rng = _rng(rng)
        truth = np.asarray(truth, dtype=bool)
        n = truth.size
        k = np.where(truth, self.h1_scale, 1.0)[:, None]
        mu = np.where(truth, self.mu1, self.mu0)[:, None]
        bias = rng.normal(0.0, self.bias_sd, size=(n, 1))
        noise = rng.normal(0.0, self.noise_sd, size=(n, n_repeats))
        return mu + k * (bias + noise)

    def theoretical_auc(self) -> float:
        """Binormal AUC of a single look: Φ(d' / sqrt(1 + h1_scale²))."""
        return binormal_auc(self.d_prime, self.h1_scale)


def mean_of_repeats_variance(bias_sd, noise_sd, k):
    """Error variance of the mean of k looks at one location: bias_sd² + noise_sd²/k.

    It never falls below bias_sd², however large k is.
    """
    return bias_sd ** 2 + noise_sd ** 2 / k


def effective_looks(bias_sd, noise_sd, k):
    """Number of *independent* looks that k correlated looks are worth.

    With pairwise correlation ρ = bias²/(bias² + noise²): k_eff = k / (1 + (k − 1) ρ) → 1/ρ.
    """
    rho = bias_sd ** 2 / (bias_sd ** 2 + noise_sd ** 2)
    return k / (1 + (k - 1) * rho)


class PoissonClutter:
    """Homogeneous spatial Poisson process of clutter objects (false-alarm sources).

    ``rate_per_m2`` is the intensity λ; the count in area A is Poisson(λA) and, given the count,
    positions are i.i.d. uniform.
    """

    def __init__(self, rate_per_m2: float):
        self.rate = float(rate_per_m2)

    def expected_count(self, area_m2):
        """E[N] = λ · A."""
        return self.rate * area_m2

    def sample(self, width, height, rng=None):
        """Positions of clutter objects in [0, width] × [0, height] m; array of shape (N, 2)."""
        rng = _rng(rng)
        n = rng.poisson(self.rate * width * height)
        return np.column_stack([rng.uniform(0, width, n), rng.uniform(0, height, n)])


# ---------------------------------------------------------------------------------------------
# 2. Detection probability vs SNR and range
# ---------------------------------------------------------------------------------------------
def threshold_for_pfa(pfa, mu0=0.0, sd0=1.0):
    """Neyman–Pearson threshold for Gaussian H0 scores: λ = mu0 + sd0 · Q⁻¹(pfa)."""
    return mu0 + sd0 * stats.norm.isf(pfa)


def pd_from_snr(snr_db, pfa):
    """Pd of a known signal in white Gaussian noise at a threshold set for ``pfa``.

    With d' = sqrt(SNR) (SNR as a linear power ratio):  Pd = Q(Q⁻¹(Pfa) − d').
    Pd = Pfa at SNR → 0 and Pd → 1 as SNR → ∞.
    """
    d = np.sqrt(10.0 ** (np.asarray(snr_db, dtype=float) / 10.0))
    return stats.norm.sf(stats.norm.isf(pfa) - d)


def snr_at_range(r, snr_ref_db, r_ref=1.0, path_exponent=4.0, atten_db_per_m=0.0):
    """Range-dependent SNR in dB.

    SNR(r) = SNR_ref − 10·n·log10(r / r_ref) − α (r − r_ref)
    n = geometric spreading exponent (4 for a two-way radar-like point target, 6 for a magnetic
    dipole seen by an induction sensor), α = medium attenuation in dB per metre.
    """
    r = np.asarray(r, dtype=float)
    return snr_ref_db - 10 * path_exponent * np.log10(r / r_ref) - atten_db_per_m * (r - r_ref)


def pd_at_range(r, pfa, snr_ref_db, r_ref=1.0, path_exponent=4.0, atten_db_per_m=0.0):
    """Pd vs range: :func:`pd_from_snr` composed with :func:`snr_at_range`."""
    return pd_from_snr(snr_at_range(r, snr_ref_db, r_ref, path_exponent, atten_db_per_m), pfa)


# ---------------------------------------------------------------------------------------------
# 3. ROC and AUC
# ---------------------------------------------------------------------------------------------
def empirical_roc(s0, s1):
    """Empirical ROC from H0 scores ``s0`` and H1 scores ``s1`` (decision: alarm if s >= t).

    Returns (pfa, pd, auc): arrays from (0, 0) to (1, 1), one point per distinct threshold,
    non-decreasing; ``auc`` is the trapezoidal area, which equals the Mann–Whitney statistic
    P(S1 > S0) + ½ P(S1 = S0). Vectorised: O((n0 + n1) log(n0 + n1)), no loop over thresholds.
    """
    s0 = np.asarray(s0, dtype=float).ravel()
    s1 = np.asarray(s1, dtype=float).ravel()
    thr = np.unique(np.concatenate([s0, s1]))[::-1]               # descending distinct values
    s0s, s1s = np.sort(s0), np.sort(s1)
    pfa = (s0.size - np.searchsorted(s0s, thr, side="left")) / s0.size   # P(s0 >= t)
    pd = (s1.size - np.searchsorted(s1s, thr, side="left")) / s1.size
    pfa = np.concatenate([[0.0], pfa])
    pd = np.concatenate([[0.0], pd])
    auc = float(np.sum(np.diff(pfa) * (pd[1:] + pd[:-1]) / 2))
    return pfa, pd, auc


def auc_mann_whitney(s0, s1):
    """AUC via ranks: (R1 − n1(n1+1)/2)/(n0 n1), mid-ranks for ties."""
    s0 = np.asarray(s0, dtype=float).ravel()
    s1 = np.asarray(s1, dtype=float).ravel()
    ranks = stats.rankdata(np.concatenate([s0, s1]))
    r1 = ranks[s0.size:].sum()
    return float((r1 - s1.size * (s1.size + 1) / 2) / (s0.size * s1.size))


def binormal_auc(d_prime, sigma_ratio=1.0):
    """AUC of the binormal model H0: N(0,1), H1: N(d', σ²):  Φ(d' / sqrt(1 + σ²))."""
    return float(stats.norm.cdf(d_prime / np.sqrt(1 + sigma_ratio ** 2)))


def monte_carlo_roc(sensor, n0, n1, rng=None, n_repeats=1):
    """Simulate n0 target-free and n1 target locations, score each as the mean of ``n_repeats``
    looks, and return dict(s0, s1, pfa, pd, auc)."""
    rng = _rng(rng)
    s0 = sensor.measure(np.zeros(n0, bool), n_repeats, rng).mean(axis=1)
    s1 = sensor.measure(np.ones(n1, bool), n_repeats, rng).mean(axis=1)
    pfa, pd, auc = empirical_roc(s0, s1)
    return {"s0": s0, "s1": s1, "pfa": pfa, "pd": pd, "auc": auc}


def bootstrap_auc_ci(s0, s1, n_boot=500, conf=0.95, rng=None):
    """Percentile bootstrap CI for the AUC (resample H0 and H1 scores independently)."""
    rng = _rng(rng)
    s0 = np.asarray(s0, dtype=float)
    s1 = np.asarray(s1, dtype=float)
    aucs = np.empty(n_boot)
    for b in range(n_boot):
        aucs[b] = auc_mann_whitney(rng.choice(s0, s0.size), rng.choice(s1, s1.size))
    a = (1 - conf) / 2
    return float(np.quantile(aucs, a)), float(np.quantile(aucs, 1 - a))


# ---------------------------------------------------------------------------------------------
# 4. Intervals for proportions and rates
# ---------------------------------------------------------------------------------------------
def wald_interval(k, n, conf=0.95):
    """PROVIDED (as a cautionary baseline): p̂ ± z sqrt(p̂(1−p̂)/n), clipped to [0, 1].

    Collapses to a zero-width interval at k = 0 or k = n — exactly where EOD trials live.
    """
    z = stats.norm.isf((1 - conf) / 2)
    p = k / n
    h = z * math.sqrt(p * (1 - p) / n)
    return max(0.0, p - h), min(1.0, p + h)


def wilson_interval(k, n, conf=0.95):
    """Wilson score interval for a binomial proportion.

    centre = (p̂ + z²/2n)/(1 + z²/n), half-width = z/(1 + z²/n) · sqrt(p̂(1−p̂)/n + z²/4n²).
    """
    z = stats.norm.isf((1 - conf) / 2)
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z / den * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return max(0.0, c - h), min(1.0, c + h)


def clopper_pearson(k, n, conf=0.95):
    """Exact (Clopper–Pearson) interval from Beta quantiles; guaranteed coverage >= conf."""
    a = 1 - conf
    lo = 0.0 if k == 0 else float(stats.beta.ppf(a / 2, k, n - k + 1))
    hi = 1.0 if k == n else float(stats.beta.ppf(1 - a / 2, k + 1, n - k))
    return lo, hi


def poisson_rate_ci(k, exposure, conf=0.95):
    """Exact (Garwood) interval for a Poisson rate from k events in ``exposure`` (e.g. m²).

    lo = χ²_{a/2}(2k)/2 / exposure (0 if k = 0), hi = χ²_{1−a/2}(2k+2)/2 / exposure.
    """
    a = 1 - conf
    lo = 0.0 if k == 0 else float(stats.chi2.ppf(a / 2, 2 * k)) / 2
    hi = float(stats.chi2.ppf(1 - a / 2, 2 * k + 2)) / 2
    return lo / exposure, hi / exposure


def exact_coverage(interval, p, n, conf=0.95):
    """Exact coverage probability Σ_k Binom(k; n, p) · 1[lo(k) <= p <= hi(k)] of an interval method."""
    ks = np.arange(n + 1)
    pmf = stats.binom.pmf(ks, n, p)
    cover = np.array([lo <= p <= hi for lo, hi in (interval(k, n, conf) for k in ks)])
    return float(pmf[cover].sum())


def simulate_coverage(interval, p, n, conf=0.95, n_trials=2000, rng=None):
    """Monte-Carlo coverage: fraction of simulated trials whose interval contains p."""
    rng = _rng(rng)
    ks = rng.binomial(n, p, n_trials)
    hits = 0
    for k in ks:
        lo, hi = interval(int(k), n, conf)
        hits += lo <= p <= hi
    return hits / n_trials


def empirical_rates(s0, s1, threshold, conf=0.95, method=clopper_pearson):
    """Pd and Pfa at ``threshold`` (alarm if s >= threshold) with intervals from ``method``.

    Returns dict(pd, pd_ci, pfa, pfa_ci, k1, n1, k0, n0).
    """
    s0 = np.asarray(s0)
    s1 = np.asarray(s1)
    k1, n1 = int(np.sum(s1 >= threshold)), s1.size
    k0, n0 = int(np.sum(s0 >= threshold)), s0.size
    return {"pd": k1 / n1, "pd_ci": method(k1, n1, conf), "pfa": k0 / n0,
            "pfa_ci": method(k0, n0, conf), "k1": k1, "n1": n1, "k0": k0, "n0": n0}


# ---------------------------------------------------------------------------------------------
# 5. Trial planning
# ---------------------------------------------------------------------------------------------
def n_for_demo(p0, conf=0.95, misses_allowed=0):
    """Smallest number of targets n such that passing (≤ misses_allowed misses) demonstrates
    Pd >= p0 at confidence ``conf``, i.e. P(pass | Pd = p0) <= 1 − conf.

    Zero-failure case in closed form: n = ceil(ln(1 − conf) / ln(p0)).
    """
    if misses_allowed == 0:
        return int(math.ceil(math.log(1 - conf) / math.log(p0) - 1e-12))
    n = misses_allowed + 1
    while stats.binom.cdf(misses_allowed, n, 1 - p0) > 1 - conf:
        n += 1
    return n


def demo_pass_probability(p_true, n, misses_allowed=0):
    """Probability that a detector with true Pd ``p_true`` passes an n-target, c-miss trial."""
    return float(stats.binom.cdf(misses_allowed, n, 1 - p_true))
