"""hitl -- human-in-the-loop decision engine for FICTIONAL incidents (Project P12).

Reference solution. Pipeline:

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

CLASSES = ("clutter", "benign_item", "hazard_like")
HAZARD = 2
ACTIONS = ("declare_hazard", "declare_benign")     # full response vs release (abstract)
DEFAULT_LOSS = np.array([[20.0, 20.0, 25.0],        # declare_hazard: disruption (+ residual)
                         [0.0, 0.0, 1000.0]])       # declare_benign: catastrophic if hazardous
COMMIT, ESCALATE = 0, 1                            # decision codes; 2 + i = gather with sensor i
POLICIES = ("voi", "voi_guarded", "threshold", "always_ask")


# ----------------------------------------------------------------------------- helpers (given)
def softmax(z: np.ndarray, T: float = 1.0) -> np.ndarray:
    """Row-wise softmax of logits / T (numerically stable)."""
    a = np.asarray(z, dtype=float) / T
    a = a - a.max(axis=-1, keepdims=True)
    e = np.exp(a)
    return e / e.sum(axis=-1, keepdims=True)


def log_softmax(z: np.ndarray, T: float = 1.0) -> np.ndarray:
    a = np.asarray(z, dtype=float) / T
    m = a.max(axis=-1, keepdims=True)
    return a - m - np.log(np.exp(a - m).sum(axis=-1, keepdims=True))


def as_beliefs(B) -> np.ndarray:
    """Promote a single belief vector to a (1, K) batch."""
    B = np.asarray(B, dtype=float)
    return B[None, :] if B.ndim == 1 else B


# ----------------------------------------------------------------------------- calibration
def nll(logits: np.ndarray, y: np.ndarray, T: float = 1.0) -> float:
    """Mean negative log-likelihood of labels ``y`` under softmax(logits / T)."""
    lp = log_softmax(logits, T)
    return float(-lp[np.arange(len(y)), y].mean())


def fit_temperature(logits: np.ndarray, y: np.ndarray, T_bounds=(0.05, 20.0)) -> float:
    """T* = argmin_T NLL(T), by bounded 1-D minimisation over log T (NLL is convex in 1/T)."""
    res = minimize_scalar(lambda lt: nll(logits, y, math.exp(lt)),
                          bounds=(math.log(T_bounds[0]), math.log(T_bounds[1])),
                          method="bounded", options={"xatol": 1e-6})
    return float(math.exp(res.x))


def expected_calibration_error(probs: np.ndarray, y: np.ndarray, n_bins: int = 15) -> float:
    """Top-label ECE with equal-width confidence bins."""
    conf = probs.max(axis=1)
    correct = probs.argmax(axis=1) == y
    edges = np.linspace(0, 1, n_bins + 1)
    ece = 0.0
    for lo, hi in zip(edges[:-1], edges[1:]):
        m = (conf > lo) & (conf <= hi)
        if m.any():
            ece += m.mean() * abs(correct[m].mean() - conf[m].mean())
    return float(ece)


# ----------------------------------------------------------------------------- conformal
def conformal_threshold(scores: np.ndarray, alpha: float) -> float:
    """k-th smallest score with k = ceil((n + 1)(1 - alpha)) (computed robustly: subtract 1e-9
    before the ceiling). Returns +inf, with a warning, when k > n (calibration set too small)."""
    s = np.sort(np.asarray(scores, dtype=float))
    n = len(s)
    k = int(math.ceil((n + 1) * (1 - alpha) - 1e-9))
    if k > n:
        warnings.warn(f"calibration set too small: n={n} < (1-alpha)/alpha={(1 - alpha) / alpha:.1f}; "
                      "threshold is +inf (every set contains this label)", RuntimeWarning, stacklevel=2)
        return math.inf
    return float(s[max(k, 1) - 1])


def min_calibration_size(alpha: float) -> int:
    """Smallest n with a finite conformal threshold: n >= (1 - alpha) / alpha."""
    return int(math.ceil((1 - alpha) / alpha - 1e-9))


def lac_scores(probs: np.ndarray, y: np.ndarray) -> np.ndarray:
    """LAC non-conformity score s(x, y) = 1 - p_y(x)."""
    return 1.0 - probs[np.arange(len(y)), y]


def fit_conformal(probs: np.ndarray, y: np.ndarray, alpha: float = 0.1,
                  class_conditional: bool = False, alphas=None) -> np.ndarray:
    """Per-class thresholds q (K,). Marginal: one threshold from all calibration scores, repeated.
    Class-conditional (Mondrian): q_k from the scores of calibration points with y = k, at level
    ``alphas[k]`` (default ``alpha`` for every class)."""
    K = probs.shape[1]
    s = lac_scores(probs, y)
    if not class_conditional:
        return np.full(K, conformal_threshold(s, alpha))
    alphas = np.full(K, alpha) if alphas is None else np.asarray(alphas, dtype=float)
    return np.array([conformal_threshold(s[y == k], alphas[k]) for k in range(K)])


def prediction_sets(probs: np.ndarray, q: np.ndarray) -> np.ndarray:
    """Boolean (n, K): label k is in the set iff 1 - p_k <= q_k."""
    return (1.0 - probs) <= np.asarray(q)[None, :]


def coverage(sets: np.ndarray, y: np.ndarray) -> float:
    return float(sets[np.arange(len(y)), y].mean())


def class_coverage(sets: np.ndarray, y: np.ndarray) -> np.ndarray:
    """Coverage restricted to each true class (NaN for absent classes)."""
    hit = sets[np.arange(len(y)), y]
    return np.array([hit[y == k].mean() if np.any(y == k) else np.nan for k in range(sets.shape[1])])


# ----------------------------------------------------------------------------- decision theory
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
    second_look = Sensor("second_look", np.array([[0.90, 0.70, 0.10],
                                                  [0.10, 0.30, 0.90]]), 3.0)
    conf = np.full((3, 3), 0.015)
    np.fill_diagonal(conf, 0.97)
    return DecisionProblem(DEFAULT_LOSS.copy(), [second_look], Sensor("human", conf, 30.0), 2)


def commit_losses(B, loss) -> np.ndarray:
    """Expected loss of every commit action: (n, A) = B @ loss.T."""
    return as_beliefs(B) @ np.asarray(loss).T


def decision_threshold(loss) -> float:
    """Two-action / binary-hazard threshold p* on P(hazard) where the two actions tie, assuming
    the non-hazard classes share the same losses (true for DEFAULT_LOSS)."""
    L = np.asarray(loss)
    fa = L[0, 0] - L[1, 0]                 # cost of a false alarm
    miss = L[1, HAZARD] - L[0, HAZARD]     # extra cost of a miss
    return float(fa / (fa + miss))


def obs_probability(B, likelihood) -> np.ndarray:
    """Predictive observation probabilities P(o) = sum_s P(o|s) b(s): (n, n_obs)."""
    return as_beliefs(B) @ np.asarray(likelihood).T


def posterior(B, likelihood, o) -> np.ndarray:
    """Bayes update of every belief row on observation index ``o`` (scalar or (n,) array)."""
    B = as_beliefs(B)
    L = np.asarray(likelihood)
    lik = L[o] if np.ndim(o) == 0 else L[np.asarray(o)]
    un = B * lik
    Z = un.sum(axis=1, keepdims=True)
    return np.divide(un, Z, out=np.full_like(un, 1.0 / B.shape[1]), where=Z > 0)


def evpi(B, loss) -> np.ndarray:
    """Expected value of perfect information: min_a E[l] - E[min_a l]. Shape (n,)."""
    B = as_beliefs(B)
    L = np.asarray(loss)
    return commit_losses(B, L).min(axis=1) - B @ L.min(axis=0)


def evsi(B, loss, likelihood) -> np.ndarray:
    """Expected value of sample information of one observation from ``likelihood``. (n,)"""
    B = as_beliefs(B)
    P = obs_probability(B, likelihood)
    after = np.zeros(len(B))
    for o in range(P.shape[1]):
        after += P[:, o] * commit_losses(posterior(B, likelihood, o), loss).min(axis=1)
    return commit_losses(B, loss).min(axis=1) - after


def human_value(B, prob: DecisionProblem) -> np.ndarray:
    """Expected cost of escalating: c_h + E_answer[min_a E[l | answer]] (+inf without a human)."""
    B = as_beliefs(B)
    if prob.human is None:
        return np.full(len(B), np.inf)
    return prob.human.cost + commit_losses(B, prob.loss).min(axis=1) - evsi(B, prob.loss, prob.human.likelihood)


def q_values(B, prob: DecisionProblem, gathers_left: int) -> np.ndarray:
    """Bellman action values (n, 2 + n_sensors): [commit now, escalate, gather sensor 0, ...].
    Gathering costs c_i + sum_o P(o) V(b_o, gathers_left - 1); +inf when no gathers are left.
    Observations are conditionally independent given the class."""
    B = as_beliefs(B)
    Q = np.full((len(B), 2 + len(prob.sensors)), np.inf)
    Q[:, COMMIT] = commit_losses(B, prob.loss).min(axis=1)
    Q[:, ESCALATE] = human_value(B, prob)
    if gathers_left > 0:
        for i, s in enumerate(prob.sensors):
            P = obs_probability(B, s.likelihood)
            v = np.full(len(B), s.cost)
            for o in range(P.shape[1]):
                v += P[:, o] * value(posterior(B, s.likelihood, o), prob, gathers_left - 1)
            Q[:, 2 + i] = v
    return Q


def value(B, prob: DecisionProblem, gathers_left: int) -> np.ndarray:
    """Optimal expected cost V(b, h) = min over q_values. Always <= the commit-now loss."""
    return q_values(B, prob, gathers_left).min(axis=1)


def decide(B, prob: DecisionProblem, gathers_left: int) -> np.ndarray:
    """Decision codes (n,): argmin of q_values; ties resolved toward the lower code (commit
    before escalate before gathering -- don't pay for information that cannot help)."""
    Q = q_values(B, prob, gathers_left)
    return np.argmin(Q - 1e-9 * np.arange(Q.shape[1])[None, :] * 0 + 0.0, axis=1) if False else \
        np.argmin(np.where(Q <= Q.min(axis=1, keepdims=True) + 1e-9, np.arange(Q.shape[1])[None, :], 10 ** 6), axis=1)


# ----------------------------------------------------------------------------- incident simulator
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
        return self.temperature * self.true_log_posterior(x), y


def sample_observation(likelihood: np.ndarray, y: np.ndarray, u: np.ndarray) -> np.ndarray:
    """Draw one observation index per incident from P(o | y) by inverse CDF of the given
    uniforms ``u`` (n,) -- passing pre-drawn uniforms gives common random numbers."""
    cdf = np.cumsum(np.asarray(likelihood)[:, y], axis=0)       # (n_obs, n)
    return np.minimum((u[None, :] > cdf).sum(axis=0), cdf.shape[0] - 1)


# ----------------------------------------------------------------------------- policies & evaluation
def simulate_policy(policy: str, B0: np.ndarray, y: np.ndarray, prob: DecisionProblem,
                    rng: np.random.Generator, sets: np.ndarray | None = None) -> dict:
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
    n = len(y)
    B = as_beliefs(B0).copy()
    cost = np.zeros(n)
    gathers = np.zeros(n, dtype=int)
    escalated = np.zeros(n, dtype=bool)
    action = np.full(n, -1)
    u_gather = rng.uniform(size=(prob.max_gathers, n))
    u_human = rng.uniform(size=n)

    def draw(lik, idx, u):
        return sample_observation(lik, y[idx], u)

    def escalate(idx):
        if prob.human is None:
            raise ValueError("no human available")
        o = draw(prob.human.likelihood, idx, u_human[idx])
        B[idx] = posterior(B[idx], prob.human.likelihood, o)
        cost[idx] += prob.human.cost
        escalated[idx] = True

    active = np.arange(n)
    if policy == "always_ask":
        escalate(active)
    elif policy in ("voi", "voi_guarded"):
        for step in range(prob.max_gathers + 1):
            if len(active) == 0:
                break
            d = decide(B[active], prob, prob.max_gathers - step)
            esc = active[d == ESCALATE]
            if len(esc):
                escalate(esc)
            for i, s in enumerate(prob.sensors):
                g = active[d == 2 + i]
                if len(g):
                    o = draw(s.likelihood, g, u_gather[step, g])
                    B[g] = posterior(B[g], s.likelihood, o)
                    cost[g] += s.cost
                    gathers[g] += 1
            active = active[d >= 2]
    elif policy != "threshold":
        raise ValueError(policy)
    a = commit_losses(B, prob.loss).argmin(axis=1)
    if policy == "voi_guarded":
        if sets is None:
            raise ValueError("voi_guarded needs conformal sets")
        release = ACTIONS.index("declare_benign")
        guard = (a == release) & sets[:, HAZARD] & ~escalated
        idx = np.nonzero(guard)[0]
        if len(idx):
            escalate(idx)
            a[idx] = commit_losses(B[idx], prob.loss).argmin(axis=1)
    action[:] = a
    cost += prob.loss[a, y]
    return {"cost": cost, "action": action, "gathers": gathers, "escalated": escalated}


def summarize(run: dict, y: np.ndarray) -> dict:
    """Risk, workload and cost metrics of a simulated run.

    hazard_release_rate: P(release | hazard); hazard_auto_release_rate: P(release without human |
    hazard); false_alarm_rate: P(declare hazard | not hazard); workload: fraction escalated;
    automation_rate: 1 - workload; mean_gathers; mean_cost and its standard error."""
    release = run["action"] == ACTIONS.index("declare_benign")
    hz = y == HAZARD
    n = len(y)
    return {
        "mean_cost": float(run["cost"].mean()),
        "se_cost": float(run["cost"].std(ddof=1) / math.sqrt(n)) if n > 1 else 0.0,
        "hazard_release_rate": float(release[hz].mean()) if hz.any() else 0.0,
        "hazard_auto_release_rate": float((release & ~run["escalated"])[hz].mean()) if hz.any() else 0.0,
        "false_alarm_rate": float((~release)[~hz].mean()) if (~hz).any() else 0.0,
        "workload": float(run["escalated"].mean()),
        "automation_rate": float(1 - run["escalated"].mean()),
        "mean_gathers": float(run["gathers"].mean()),
    }


def run_pipeline(sim: IncidentSimulator | None = None, prob: DecisionProblem | None = None,
                 n_fit: int = 3000, n_cal: int = 3000, n_test: int = 5000, alpha: float = 0.1,
                 alpha_hazard: float = 0.02, seed: int = 0) -> dict:
    """End to end: fit T on a fit split, class-conditional conformal thresholds on a calibration
    split (alpha for non-hazard classes, ``alpha_hazard`` for the hazard class), then simulate every
    policy in POLICIES on a test split with common random numbers. Returns T, NLLs, conformal
    thresholds, coverage, mean set size and per-policy summaries."""
    sim = sim or IncidentSimulator()
    prob = prob or default_problem()
    rng = np.random.default_rng(seed)
    zf, yf = sim.sample(n_fit, rng)
    zc, yc = sim.sample(n_cal, rng)
    zt, yt = sim.sample(n_test, rng)
    T = fit_temperature(zf, yf)
    alphas = np.full(len(sim.priors), alpha)
    alphas[HAZARD] = alpha_hazard
    q = fit_conformal(softmax(zc, T), yc, class_conditional=True, alphas=alphas)
    Bt = softmax(zt, T)
    sets = prediction_sets(Bt, q)
    world = int(rng.integers(2 ** 32))
    results = {p: summarize(simulate_policy(p, Bt, yt, prob, np.random.default_rng(world), sets), yt)
               for p in POLICIES}
    return {"T": T, "nll_raw": nll(zt, yt, 1.0), "nll_calibrated": nll(zt, yt, T), "q": q,
            "coverage": coverage(sets, yt), "class_coverage": class_coverage(sets, yt),
            "mean_set_size": float(sets.sum(1).mean()), "policies": results}


if __name__ == "__main__":  # pragma: no cover
    out = run_pipeline()
    print(f"T = {out['T']:.3f}  NLL raw {out['nll_raw']:.3f} -> calibrated {out['nll_calibrated']:.3f}")
    print("coverage", round(out["coverage"], 3), "per class", np.round(out["class_coverage"], 3),
          "mean set size", round(out["mean_set_size"], 2))
    for p, m in out["policies"].items():
        print(f"{p:12s} " + " ".join(f"{k}={v:.4f}" for k, v in m.items()))
