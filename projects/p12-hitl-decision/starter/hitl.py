"""hitl -- human-in-the-loop decision engine for FICTIONAL incidents (Project P12).

STARTER -- implement every function that raises NotImplementedError
(the helpers that are already implemented are not the learning goal).

Pipeline:

    classifier logits --> temperature scaling (calibration) --> calibrated belief b(y | x)
                      --> split conformal prediction sets (marginal or class-conditional)
                      --> value-of-information policy: declare / gather more data / escalate
                      --> evaluation on simulated incidents with ground truth.

Classes are abstract ("clutter", "benign_item", "hazard_like"); losses are in abstract loss
units (LU). Nothing here models real devices or real procedures; the "decision" is a
decision-theoretic abstraction (full response vs release), as in lesson 07.1.

Array conventions: beliefs ``B`` are (n, K) row-stochastic; a loss matrix is (A, K) =
actions x true classes; a sensor likelihood is (n_obs, K) with columns P(o | class) summing to 1.
"""
from __future__ import annotations
import math
import warnings
from dataclasses import dataclass, field
import numpy as np
from scipy.optimize import minimize_scalar
CLASSES = ('clutter', 'benign_item', 'hazard_like')
HAZARD = 2
ACTIONS = ('declare_hazard', 'declare_benign')
DEFAULT_LOSS = np.array([[20.0, 20.0, 25.0], [0.0, 0.0, 1000.0]])
COMMIT, ESCALATE = (0, 1)
POLICIES = ('voi', 'voi_guarded', 'threshold', 'always_ask')


def softmax(z: np.ndarray, T: float=1.0) -> np.ndarray:
    """Row-wise softmax of logits / T (numerically stable)."""
    a = np.asarray(z, dtype=float) / T
    a = a - a.max(axis=-1, keepdims=True)
    e = np.exp(a)
    return e / e.sum(axis=-1, keepdims=True)


def log_softmax(z: np.ndarray, T: float=1.0) -> np.ndarray:
    a = np.asarray(z, dtype=float) / T
    m = a.max(axis=-1, keepdims=True)
    return a - m - np.log(np.exp(a - m).sum(axis=-1, keepdims=True))


def as_beliefs(B) -> np.ndarray:
    """Promote a single belief vector to a (1, K) batch."""
    B = np.asarray(B, dtype=float)
    return B[None, :] if B.ndim == 1 else B


def nll(logits: np.ndarray, y: np.ndarray, T: float=1.0) -> float:
    """Mean negative log-likelihood of labels ``y`` under softmax(logits / T)."""
    raise NotImplementedError('TODO: implement nll')


def fit_temperature(logits: np.ndarray, y: np.ndarray, T_bounds=(0.05, 20.0)) -> float:
    """T* = argmin_T NLL(T), by bounded 1-D minimisation over log T (NLL is convex in 1/T)."""
    raise NotImplementedError('TODO: implement fit_temperature')


def expected_calibration_error(probs: np.ndarray, y: np.ndarray, n_bins: int=15) -> float:
    """Top-label ECE with equal-width confidence bins."""
    raise NotImplementedError('TODO: implement expected_calibration_error')


def conformal_threshold(scores: np.ndarray, alpha: float) -> float:
    """k-th smallest score with k = ceil((n + 1)(1 - alpha)) (computed robustly: subtract 1e-9
    before the ceiling). Returns +inf, with a warning, when k > n (calibration set too small)."""
    raise NotImplementedError('TODO: implement conformal_threshold')


def min_calibration_size(alpha: float) -> int:
    """Smallest n with a finite conformal threshold: n >= (1 - alpha) / alpha."""
    raise NotImplementedError('TODO: implement min_calibration_size')


def lac_scores(probs: np.ndarray, y: np.ndarray) -> np.ndarray:
    """LAC non-conformity score s(x, y) = 1 - p_y(x)."""
    raise NotImplementedError('TODO: implement lac_scores')


def fit_conformal(probs: np.ndarray, y: np.ndarray, alpha: float=0.1, class_conditional: bool=False, alphas=None) -> np.ndarray:
    """Per-class thresholds q (K,). Marginal: one threshold from all calibration scores, repeated.
    Class-conditional (Mondrian): q_k from the scores of calibration points with y = k, at level
    ``alphas[k]`` (default ``alpha`` for every class)."""
    raise NotImplementedError('TODO: implement fit_conformal')


def prediction_sets(probs: np.ndarray, q: np.ndarray) -> np.ndarray:
    """Boolean (n, K): label k is in the set iff 1 - p_k <= q_k."""
    raise NotImplementedError('TODO: implement prediction_sets')


def coverage(sets: np.ndarray, y: np.ndarray) -> float:
    return float(sets[np.arange(len(y)), y].mean())


def class_coverage(sets: np.ndarray, y: np.ndarray) -> np.ndarray:
    """Coverage restricted to each true class (NaN for absent classes)."""
    hit = sets[np.arange(len(y)), y]
    return np.array([hit[y == k].mean() if np.any(y == k) else np.nan for k in range(sets.shape[1])])


@dataclass
class Sensor:
    """An information source: likelihood (n_obs, K) = P(o | class), and its cost in LU."""
    name: str
    likelihood: np.ndarray
    cost: float


@dataclass
class DecisionProblem:
    """Loss (A, K); gatherable sensors; the human (a terminal, costly, near-perfect sensor);
    maximum number of gather steps per incident."""
    loss: np.ndarray = field(default_factory=lambda: DEFAULT_LOSS.copy())
    sensors: list = field(default_factory=list)
    human: Sensor | None = None
    max_gathers: int = 2


def default_problem() -> DecisionProblem:
    """The course's fictional problem: a second-look sensor (P(+ | clutter, benign, hazard) =
    0.10, 0.30, 0.90; 3 LU) and a human analyst (97 % correct, errors spread evenly; 30 LU)."""
    second_look = Sensor('second_look', np.array([[0.9, 0.7, 0.1], [0.1, 0.3, 0.9]]), 3.0)
    conf = np.full((3, 3), 0.015)
    np.fill_diagonal(conf, 0.97)
    return DecisionProblem(DEFAULT_LOSS.copy(), [second_look], Sensor('human', conf, 30.0), 2)


def commit_losses(B, loss) -> np.ndarray:
    """Expected loss of every commit action: (n, A) = B @ loss.T."""
    raise NotImplementedError('TODO: implement commit_losses')


def decision_threshold(loss) -> float:
    """Two-action / binary-hazard threshold p* on P(hazard) where the two actions tie, assuming
    the non-hazard classes share the same losses (true for DEFAULT_LOSS)."""
    raise NotImplementedError('TODO: implement decision_threshold')


def obs_probability(B, likelihood) -> np.ndarray:
    """Predictive observation probabilities P(o) = sum_s P(o|s) b(s): (n, n_obs)."""
    raise NotImplementedError('TODO: implement obs_probability')


def posterior(B, likelihood, o) -> np.ndarray:
    """Bayes update of every belief row on observation index ``o`` (scalar or (n,) array)."""
    raise NotImplementedError('TODO: implement posterior')


def evpi(B, loss) -> np.ndarray:
    """Expected value of perfect information: min_a E[l] - E[min_a l]. Shape (n,)."""
    raise NotImplementedError('TODO: implement evpi')


def evsi(B, loss, likelihood) -> np.ndarray:
    """Expected value of sample information of one observation from ``likelihood``. (n,)"""
    raise NotImplementedError('TODO: implement evsi')


def human_value(B, prob: DecisionProblem) -> np.ndarray:
    """Expected cost of escalating: c_h + E_answer[min_a E[l | answer]] (+inf without a human)."""
    raise NotImplementedError('TODO: implement human_value')


def q_values(B, prob: DecisionProblem, gathers_left: int) -> np.ndarray:
    """Bellman action values (n, 2 + n_sensors): [commit now, escalate, gather sensor 0, ...].
    Gathering costs c_i + sum_o P(o) V(b_o, gathers_left - 1); +inf when no gathers are left.
    Observations are conditionally independent given the class."""
    raise NotImplementedError('TODO: implement q_values')


def value(B, prob: DecisionProblem, gathers_left: int) -> np.ndarray:
    """Optimal expected cost V(b, h) = min over q_values. Always <= the commit-now loss."""
    raise NotImplementedError('TODO: implement value')


def decide(B, prob: DecisionProblem, gathers_left: int) -> np.ndarray:
    """Decision codes (n,): argmin of q_values; ties resolved toward the lower code (commit
    before escalate before gathering -- don't pay for information that cannot help)."""
    raise NotImplementedError('TODO: implement decide')


@dataclass
class IncidentSimulator:
    """Fictional incidents: class y ~ priors, features x ~ N(separation * e_y, I_d); the
    "classifier" outputs over-confident logits z = temperature * log p_true(y | x), so the
    calibrated temperature is exactly ``temperature``."""
    priors: tuple = (0.6, 0.3, 0.1)
    dim: int = 4
    separation: float = 1.5
    temperature: float = 2.5

    def means(self) -> np.ndarray:
        M = np.zeros((len(self.priors), self.dim))
        for k in range(len(self.priors)):
            M[k, k % self.dim] = self.separation
        return M

    def true_log_posterior(self, x: np.ndarray) -> np.ndarray:
        M = self.means()
        ll = -0.5 * ((x[:, None, :] - M[None, :, :]) ** 2).sum(-1) + np.log(np.asarray(self.priors))[None, :]
        return log_softmax(ll)

    def sample(self, n: int, rng: np.random.Generator):
        """Return (logits (n, K), y (n,))."""
        y = rng.choice(len(self.priors), size=n, p=np.asarray(self.priors))
        x = self.means()[y] + rng.standard_normal((n, self.dim))
        return (self.temperature * self.true_log_posterior(x), y)


def sample_observation(likelihood: np.ndarray, y: np.ndarray, u: np.ndarray) -> np.ndarray:
    """Draw one observation index per incident from P(o | y) by inverse CDF of the given
    uniforms ``u`` (n,) -- passing pre-drawn uniforms gives common random numbers."""
    cdf = np.cumsum(np.asarray(likelihood)[:, y], axis=0)
    return np.minimum((u[None, :] > cdf).sum(axis=0), cdf.shape[0] - 1)


def simulate_policy(policy: str, B0: np.ndarray, y: np.ndarray, prob: DecisionProblem, rng: np.random.Generator, sets: np.ndarray | None=None) -> dict:
    """Run ``policy`` on incidents with calibrated beliefs ``B0`` and true classes ``y``.

    * ``threshold``  -- commit the Bayes action on B0 (a threshold on P(hazard)); no gathering.
    * ``always_ask`` -- escalate every incident, then commit on the posterior.
    * ``voi``        -- follow ``decide`` (Bellman VOI over gather / escalate / commit).
    * ``voi_guarded``-- as voi, but a *release* without human review is replaced by escalation
      when the hazard class is in the conformal set (``sets`` required).

    Randomness: each incident gets its own pre-drawn uniforms for gather observations and the
    human's answer, so all policies see the same world (common random numbers).
    Returns per-incident arrays: cost, action, gathers, escalated.
    """
    raise NotImplementedError('TODO: implement simulate_policy')


def summarize(run: dict, y: np.ndarray) -> dict:
    """Risk, workload and cost metrics of a simulated run.

    hazard_release_rate: P(release | hazard); hazard_auto_release_rate: P(release without human |
    hazard); false_alarm_rate: P(declare hazard | not hazard); workload: fraction escalated;
    automation_rate: 1 - workload; mean_gathers; mean_cost and its standard error."""
    raise NotImplementedError('TODO: implement summarize')


def run_pipeline(sim: IncidentSimulator | None=None, prob: DecisionProblem | None=None, n_fit: int=3000, n_cal: int=3000, n_test: int=5000, alpha: float=0.1, alpha_hazard: float=0.02, seed: int=0) -> dict:
    """End to end: fit T on a fit split, class-conditional conformal thresholds on a calibration
    split (alpha for non-hazard classes, ``alpha_hazard`` for the hazard class), then simulate every
    policy in POLICIES on a test split with common random numbers. Returns T, NLLs, conformal
    thresholds, coverage, mean set size and per-policy summaries."""
    raise NotImplementedError('TODO: implement run_pipeline')
